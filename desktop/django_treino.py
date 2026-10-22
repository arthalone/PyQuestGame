# -*- coding: utf-8 -*-
"""
"Django de treino" do PyQuest.

Uma versão pequena do Django, só com as peças usadas no projeto Learning Log do livro:
models e ORM em memória, URLs, views, templates, formulários, usuários e login,
e um Client de teste que "abre" as páginas. Tudo roda num arquivo só, sem servidor.
O mesmo código, separado nos arquivos certos, funciona no Django de verdade.
"""
import datetime as _dt
import functools
import hashlib
import html as _html
import itertools
import re
import sys
import types

__version__ = "5.0-treino"

# ---------------------------------------------------------------------------
# Exceções (mesmos nomes do Django)
# ---------------------------------------------------------------------------


class ObjectDoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class FieldError(Exception):
    pass


class ValidationError(Exception):
    pass


class ImproperlyConfigured(Exception):
    pass


class Http404(Exception):
    pass


class NoReverseMatch(Exception):
    pass


class Resolver404(Exception):
    pass


class TemplateDoesNotExist(Exception):
    pass


class TemplateSyntaxError(Exception):
    pass


# ---------------------------------------------------------------------------
# Relógio previsível (cada objeto criado avança 1 minuto)
# ---------------------------------------------------------------------------

_INICIO = _dt.datetime(2026, 3, 2, 9, 0, tzinfo=_dt.timezone.utc)
_RELOGIO = [_INICIO]


def _agora():
    _RELOGIO[0] = _RELOGIO[0] + _dt.timedelta(minutes=1)
    return _RELOGIO[0]


# ---------------------------------------------------------------------------
# Strings seguras (não são escapadas nos templates)
# ---------------------------------------------------------------------------


class SafeString(str):
    __html__ = str.__str__


def mark_safe(s):
    return SafeString(s)


def _esc(v):
    if isinstance(v, SafeString):
        return v
    return SafeString(_html.escape(str(v), quote=True))


# ---------------------------------------------------------------------------
# Models e ORM em memória
# ---------------------------------------------------------------------------

_NADA = object()
_REGISTRO = {}          # nome do model (minúsculo) -> classe
_contador = itertools.count()

CASCADE = "CASCADE"
PROTECT = "PROTECT"
SET_NULL = "SET_NULL"
DO_NOTHING = "DO_NOTHING"


class Field:
    tipo_input = "text"

    def __init__(self, verbose_name=None, *, max_length=None, default=_NADA, null=False, blank=False,
                 auto_now_add=False, auto_now=False, unique=False, choices=None, help_text="", **extra):
        self.verbose_name = verbose_name
        self.max_length = max_length
        self.default = default
        self.null = null
        self.blank = blank
        self.auto_now_add = auto_now_add
        self.auto_now = auto_now
        self.unique = unique
        self.choices = choices
        self.ordem = next(_contador)
        self.nome = None

    def padrao(self):
        if self.default is _NADA:
            return None
        return self.default() if callable(self.default) else self.default

    def converter(self, v):
        return v

    def __repr__(self):
        return f"<django.db.models.{type(self).__name__}: {self.nome}>"


class AutoField(Field):
    pass


class CharField(Field):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        if self.max_length is None:
            raise TypeError("CharField precisa de max_length (ex.: models.CharField(max_length=200)).")


class EmailField(CharField):
    tipo_input = "email"

    def __init__(self, *a, max_length=254, **k):
        super().__init__(*a, max_length=max_length, **k)


class SlugField(CharField):
    def __init__(self, *a, max_length=50, **k):
        super().__init__(*a, max_length=max_length, **k)


class URLField(CharField):
    tipo_input = "url"

    def __init__(self, *a, max_length=200, **k):
        super().__init__(*a, max_length=max_length, **k)


class TextField(Field):
    pass


class IntegerField(Field):
    tipo_input = "number"

    def converter(self, v):
        if v in (None, ""):
            return None
        return int(v)


class PositiveIntegerField(IntegerField):
    pass


class FloatField(Field):
    tipo_input = "number"

    def converter(self, v):
        if v in (None, ""):
            return None
        return float(v)


class BooleanField(Field):
    tipo_input = "checkbox"

    def __init__(self, *a, **k):
        k.setdefault("default", False)
        super().__init__(*a, **k)

    def converter(self, v):
        return v not in (None, "", "false", "False", "0", False, "off")


class DateTimeField(Field):
    tipo_input = "datetime-local"


class DateField(Field):
    tipo_input = "date"


class ForeignKey(Field):
    def __init__(self, to, on_delete=None, related_name=None, **k):
        if on_delete is None:
            raise TypeError("ForeignKey precisa de on_delete (ex.: on_delete=models.CASCADE).")
        super().__init__(**k)
        self.to = to
        self.on_delete = on_delete
        self.related_name = related_name

    def alvo(self):
        to = self.to
        if isinstance(to, str):
            nome = to.split(".")[-1].lower()
            if nome == "self":
                return self.dono
            if nome not in _REGISTRO:
                raise ImproperlyConfigured(f"Model '{to}' não encontrado.")
            return _REGISTRO[nome]
        return to


class OneToOneField(ForeignKey):
    pass


class _Opcoes:
    def __init__(self, meta, nome):
        self.object_name = nome
        self.model_name = nome.lower()
        self.verbose_name = getattr(meta, "verbose_name", None) or re.sub(r"(?<!^)([A-Z])", r" \1", nome).lower()
        self.verbose_name_plural = getattr(meta, "verbose_name_plural", None) or self.verbose_name + "s"
        self.ordering = list(getattr(meta, "ordering", []) or [])


class ModelBase(type):
    def __new__(mcs, nome, bases, attrs):
        campos = {}
        for k, v in list(attrs.items()):
            if isinstance(v, Field):
                v.nome = k
                campos[k] = v
                attrs.pop(k)
        meta = attrs.pop("Meta", None)
        cls = super().__new__(mcs, nome, bases, attrs)
        if attrs.get("__module__") == __name__ and nome == "Model":
            return cls
        herdados = {}
        for b in reversed(cls.__mro__[1:]):
            herdados.update({k: v for k, v in getattr(b, "_campos", {}).items() if k != "id"})
        id_campo = AutoField()
        id_campo.nome = "id"
        cls._campos = {"id": id_campo, **herdados, **dict(sorted(campos.items(), key=lambda kv: kv[1].ordem))}
        for c in campos.values():
            c.dono = cls
        cls._meta = _Opcoes(meta, nome)
        cls._dados = []
        cls._prox_id = [1]
        cls.objects = Manager(cls)
        cls.DoesNotExist = type("DoesNotExist", (ObjectDoesNotExist,), {"__module__": cls.__module__})
        cls.MultipleObjectsReturned = type("MultipleObjectsReturned", (MultipleObjectsReturned,), {})
        _REGISTRO[nome.lower()] = cls
        return cls


class Model(metaclass=ModelBase):
    def __init__(self, *args, **kwargs):
        campos = [c for c in self._campos.values()]
        for c, v in zip(campos, args):
            kwargs.setdefault(c.nome, v)
        for c in campos:
            if isinstance(c, ForeignKey):
                if c.nome in kwargs:
                    v = kwargs.pop(c.nome)
                elif c.nome + "_id" in kwargs:
                    i = kwargs.pop(c.nome + "_id")
                    v = c.alvo().objects.get(id=i) if i is not None else None
                else:
                    v = None
                object.__setattr__(self, c.nome, v)
            else:
                object.__setattr__(self, c.nome, kwargs.pop(c.nome) if c.nome in kwargs else c.padrao())
        for k, v in kwargs.items():
            raise TypeError(f"{type(self).__name__}() recebeu um argumento inesperado: '{k}'")

    @property
    def pk(self):
        return self.id

    def __getattr__(self, nome):
        if nome.startswith("_"):
            raise AttributeError(nome)
        campos = type(self).__dict__.get("_campos") or getattr(type(self), "_campos", {})
        if nome.endswith("_id") and nome[:-3] in campos and isinstance(campos[nome[:-3]], ForeignKey):
            alvo = object.__getattribute__(self, nome[:-3])
            return alvo.id if alvo is not None else None
        for m in list(_REGISTRO.values()):
            for c in m._campos.values():
                if isinstance(c, ForeignKey):
                    try:
                        alvo = c.alvo()
                    except ImproperlyConfigured:
                        continue
                    if issubclass(type(self), alvo):
                        acesso = c.related_name or (m._meta.model_name + "_set")
                        if acesso == nome:
                            return RelatedManager(m, c.nome, self)
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{nome}'")

    def save(self, *a, **k):
        for c in self._campos.values():
            if isinstance(c, (DateTimeField, DateField)):
                if (c.auto_now_add and getattr(self, c.nome) is None) or c.auto_now:
                    agora = _agora()
                    object.__setattr__(self, c.nome, agora if isinstance(c, DateTimeField) else agora.date())
        for c in self._campos.values():
            if isinstance(c, ForeignKey) and getattr(self, c.nome) is None and not c.null:
                raise IntegrityError(f"NOT NULL constraint failed: {self._meta.model_name}.{c.nome}_id")
            if c.unique and c.nome != "id":
                v = getattr(self, c.nome)
                if any(o is not self and getattr(o, c.nome) == v for o in self._dados):
                    raise IntegrityError(f"UNIQUE constraint failed: {self._meta.model_name}.{c.nome}")
        if self.id is None:
            object.__setattr__(self, "id", self._prox_id[0])
            self._prox_id[0] += 1
            self._dados.append(self)
        elif self not in self._dados:
            self._dados.append(self)

    def delete(self):
        for m in list(_REGISTRO.values()):
            for c in m._campos.values():
                if isinstance(c, ForeignKey):
                    try:
                        alvo = c.alvo()
                    except ImproperlyConfigured:
                        continue
                    if issubclass(type(self), alvo):
                        for o in [o for o in m._dados if getattr(o, c.nome) is self]:
                            if c.on_delete == CASCADE:
                                o.delete()
                            elif c.on_delete == SET_NULL:
                                object.__setattr__(o, c.nome, None)
                            elif c.on_delete == PROTECT:
                                raise ProtectedError("Não dá para apagar: outros objetos dependem deste.")
        if self in self._dados:
            self._dados.remove(self)
        n = type(self).__name__
        object.__setattr__(self, "id", None)
        return 1, {n: 1}

    def refresh_from_db(self):
        pass

    def __str__(self):
        return f"{type(self).__name__} object ({self.id})"

    def __repr__(self):
        return f"<{type(self).__name__}: {self}>"

    def __eq__(self, outro):
        if not isinstance(outro, Model) or type(outro)._meta.model_name != type(self)._meta.model_name:
            return False
        if self.id is None:
            return self is outro
        return self.id == outro.id

    def __hash__(self):
        return hash((type(self).__name__, self.id if self.id is not None else id(self)))


class IntegrityError(Exception):
    pass


class ProtectedError(Exception):
    pass


_LOOKUPS = {"exact", "iexact", "contains", "icontains", "gt", "gte", "lt", "lte", "in", "startswith",
            "istartswith", "endswith", "isnull"}


def _valor_caminho(obj, partes, model):
    v = obj
    for p in partes:
        if v is None:
            return None
        if p == "pk":
            p = "id"
        if isinstance(v, Model) and p not in v._campos and not p.endswith("_id"):
            raise FieldError(f"Cannot resolve keyword '{p}' into field. Choices are: {', '.join(v._campos)}")
        v = getattr(v, p)
    return v


def _casa(obj, filtros):
    for chave, esperado in filtros.items():
        partes = chave.split("__")
        lookup = "exact"
        if len(partes) > 1 and partes[-1] in _LOOKUPS:
            lookup = partes.pop()
        v = _valor_caminho(obj, partes, type(obj))
        if isinstance(v, Model) and not isinstance(esperado, Model) and esperado is not None:
            v = v.id
        if lookup == "exact":
            ok = v == esperado
        elif lookup == "iexact":
            ok = str(v).lower() == str(esperado).lower()
        elif lookup == "contains":
            ok = str(esperado) in str(v)
        elif lookup == "icontains":
            ok = str(esperado).lower() in str(v).lower()
        elif lookup == "startswith":
            ok = str(v).startswith(str(esperado))
        elif lookup == "istartswith":
            ok = str(v).lower().startswith(str(esperado).lower())
        elif lookup == "endswith":
            ok = str(v).endswith(str(esperado))
        elif lookup == "in":
            ok = v in esperado
        elif lookup == "isnull":
            ok = (v is None) == bool(esperado)
        else:
            if v is None:
                return False
            ok = {"gt": v > esperado, "gte": v >= esperado, "lt": v < esperado, "lte": v <= esperado}[lookup]
        if not ok:
            return False
    return True


class QuerySet:
    def __init__(self, model, itens=None):
        self.model = model
        if itens is None:
            itens = list(model._dados)
            if model._meta.ordering:
                itens = _ordenar(itens, model._meta.ordering)
        self._itens = itens

    def _novo(self, itens):
        return QuerySet(self.model, itens)

    def all(self):
        return self._novo(list(self._itens))

    def filter(self, *a, **kw):
        return self._novo([o for o in self._itens if _casa(o, kw)])

    def exclude(self, **kw):
        return self._novo([o for o in self._itens if not _casa(o, kw)])

    def get(self, *a, **kw):
        if a and not kw:
            raise TypeError("Use get(campo=valor), por exemplo: Topic.objects.get(id=1)")
        r = [o for o in self._itens if _casa(o, kw)]
        if not r:
            raise self.model.DoesNotExist(f"{self.model.__name__} matching query does not exist.")
        if len(r) > 1:
            raise self.model.MultipleObjectsReturned(
                f"get() returned more than one {self.model.__name__} -- it returned {len(r)}!")
        return r[0]

    def order_by(self, *campos):
        return self._novo(_ordenar(list(self._itens), campos))

    def reverse(self):
        return self._novo(list(reversed(self._itens)))

    def count(self):
        return len(self._itens)

    def exists(self):
        return bool(self._itens)

    def first(self):
        return self._itens[0] if self._itens else None

    def last(self):
        return self._itens[-1] if self._itens else None

    def values_list(self, *campos, flat=False):
        if flat:
            return [getattr(o, campos[0]) for o in self._itens]
        return [tuple(getattr(o, c) for c in campos) for o in self._itens]

    def delete(self):
        n = len(self._itens)
        for o in list(self._itens):
            o.delete()
        return n, {self.model.__name__: n}

    def update(self, **kw):
        for o in self._itens:
            for k, v in kw.items():
                object.__setattr__(o, k, v)
        return len(self._itens)

    def __iter__(self):
        return iter(list(self._itens))

    def __len__(self):
        return len(self._itens)

    def __bool__(self):
        return bool(self._itens)

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self._novo(self._itens[i])
        return self._itens[i]

    def __contains__(self, o):
        return o in self._itens

    def __eq__(self, outro):
        if isinstance(outro, QuerySet):
            return self._itens == outro._itens
        if isinstance(outro, list):
            return self._itens == outro
        return NotImplemented

    def __repr__(self):
        itens = ", ".join(repr(o) for o in self._itens[:21])
        return f"<QuerySet [{itens}]>"


def _ordenar(itens, campos):
    for campo in reversed(list(campos)):
        desc = campo.startswith("-")
        nome = campo.lstrip("-")
        if nome == "pk":
            nome = "id"

        def chave(o, nome=nome):
            v = _valor_caminho(o, nome.split("__"), type(o))
            if isinstance(v, Model):
                v = v.id
            return (v is None, v)
        itens = sorted(itens, key=chave, reverse=desc)
    return itens


class Manager:
    def __init__(self, model):
        self.model = model

    def get_queryset(self):
        return QuerySet(self.model)

    def __getattr__(self, nome):
        if nome.startswith("_"):
            raise AttributeError(nome)
        return getattr(self.get_queryset(), nome)

    def create(self, **kw):
        o = self.model(**kw)
        o.save()
        return o

    def get_or_create(self, defaults=None, **kw):
        try:
            return self.get(**kw), False
        except self.model.DoesNotExist:
            return self.create(**{**kw, **(defaults or {})}), True

    def __iter__(self):
        raise TypeError(f"'Manager' object is not iterable. Use {self.model.__name__}.objects.all()")

    def __repr__(self):
        return f"<django.db.models.manager.Manager object>"


class RelatedManager(Manager):
    def __init__(self, model, campo, instancia):
        super().__init__(model)
        self.campo = campo
        self.instancia = instancia

    def get_queryset(self):
        return QuerySet(self.model).filter(**{self.campo: self.instancia})

    def create(self, **kw):
        kw[self.campo] = self.instancia
        return super().create(**kw)

    def add(self, *objs):
        for o in objs:
            object.__setattr__(o, self.campo, self.instancia)
            o.save()


# ---------------------------------------------------------------------------
# Usuários e autenticação
# ---------------------------------------------------------------------------


def _hash(senha):
    return "pbkdf2_sha256$treino$" + hashlib.sha256(("pyquest:" + str(senha)).encode()).hexdigest()[:32]


class UserManager(Manager):
    def create_user(self, username, email=None, password=None, **extra):
        u = self.model(username=username, email=email or "", **extra)
        u.set_password(password)
        u.save()
        return u

    def create_superuser(self, username, email=None, password=None, **extra):
        return self.create_user(username, email, password, is_staff=True, is_superuser=True, **extra)


class User(Model):
    username = CharField(max_length=150, unique=True)
    password = CharField(max_length=128)
    email = EmailField(blank=True, default="")
    first_name = CharField(max_length=150, blank=True, default="")
    last_name = CharField(max_length=150, blank=True, default="")
    is_staff = BooleanField(default=False)
    is_superuser = BooleanField(default=False)
    is_active = BooleanField(default=True)

    is_authenticated = True
    is_anonymous = False

    def set_password(self, senha):
        object.__setattr__(self, "password", _hash(senha) if senha is not None else "!")

    def check_password(self, senha):
        return self.password == _hash(senha)

    def get_username(self):
        return self.username

    def __str__(self):
        return self.username


User.objects = UserManager(User)


class AnonymousUser:
    id = None
    pk = None
    username = ""
    is_authenticated = False
    is_anonymous = True
    is_staff = False
    is_superuser = False

    def __str__(self):
        return "AnonymousUser"

    def __repr__(self):
        return "<AnonymousUser>"

    def __eq__(self, o):
        return isinstance(o, AnonymousUser)

    def __hash__(self):
        return 1


def authenticate(request=None, username=None, password=None, **k):
    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return None
    return u if u.check_password(password) and u.is_active else None


def login(request, user, backend=None):
    request.user = user
    request.session["_auth_user_id"] = user.id


def logout(request):
    request.user = AnonymousUser()
    request.session.clear()


def get_user_model():
    return User


# ---------------------------------------------------------------------------
# Requisições e respostas
# ---------------------------------------------------------------------------


class QueryDict(dict):
    def getlist(self, k, default=None):
        v = self.get(k, default)
        return v if isinstance(v, list) else ([] if v is None else [v])

    def get(self, k, default=None):
        v = super().get(k, default)
        if isinstance(v, list):
            return v[-1] if v else default
        return v


class HttpRequest:
    def __init__(self, method="GET", path="/", GET=None, POST=None, user=None, session=None):
        self.method = method
        self.path = path
        self.path_info = path
        self.GET = QueryDict(GET or {})
        self.POST = QueryDict(POST or {})
        self.user = user if user is not None else AnonymousUser()
        self.session = session if session is not None else {}
        self.META = {"HTTP_HOST": "localhost:8000"}
        self.FILES = {}
        self.resolver_match = None

    def get_full_path(self):
        return self.path

    def build_absolute_uri(self, local=None):
        return "http://localhost:8000" + (local or self.path)

    def __repr__(self):
        return f"<WSGIRequest: {self.method} '{self.path}'>"


class HttpResponse:
    status_padrao = 200

    def __init__(self, content="", status=None, content_type="text/html; charset=utf-8"):
        self.content = content if isinstance(content, str) else str(content)
        self.status_code = status if status is not None else self.status_padrao
        self.headers = {"Content-Type": content_type}
        self.context = None
        self.templates = []
        self.url = None

    @property
    def text(self):
        return self.content

    def __getitem__(self, k):
        return self.headers[k]

    def __repr__(self):
        extra = f', url="{self.url}"' if self.url else ""
        return f'<{type(self).__name__} status_code={self.status_code}{extra}>'


class HttpResponseRedirect(HttpResponse):
    status_padrao = 302

    def __init__(self, url, *a, **k):
        super().__init__("", *a, **k)
        self.url = str(url)
        self.headers["Location"] = self.url


class HttpResponsePermanentRedirect(HttpResponseRedirect):
    status_padrao = 301


class HttpResponseNotFound(HttpResponse):
    status_padrao = 404


class HttpResponseForbidden(HttpResponse):
    status_padrao = 403


class JsonResponse(HttpResponse):
    def __init__(self, data, **k):
        import json
        super().__init__(json.dumps(data, ensure_ascii=False), content_type="application/json", **k)


# ---------------------------------------------------------------------------
# Configurações
# ---------------------------------------------------------------------------


class _Settings:
    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.__dict__.clear()
        self.DEBUG = True
        self.LOGIN_URL = "/accounts/login/"
        self.LOGIN_REDIRECT_URL = "/accounts/profile/"
        self.LOGOUT_REDIRECT_URL = None
        self.ALLOWED_HOSTS = []
        self.INSTALLED_APPS = []
        self.AUTH_USER_MODEL = "auth.User"
        self.SECRET_KEY = "django-insecure-treino"

    def configure(self, **k):
        self.__dict__.update(k)


settings = _Settings()

# ---------------------------------------------------------------------------
# URLs
# ---------------------------------------------------------------------------

_CONV = {"int": (r"[0-9]+", int), "str": (r"[^/]+", str), "slug": (r"[-a-zA-Z0-9_]+", str),
         "path": (r".+", str), "uuid": (r"[0-9a-f-]+", str)}


class URLPattern:
    def __init__(self, rota, view, kwargs=None, name=None):
        self.rota = rota
        self.view = view
        self.default_args = kwargs or {}
        self.name = name
        self.conversores = {}
        partes, pos = [], 0
        for m in re.finditer(r"<(?:(\w+):)?(\w+)>", rota):
            partes.append(re.escape(rota[pos:m.start()]))
            conv = m.group(1) or "str"
            if conv not in _CONV:
                raise ImproperlyConfigured(f"Conversor de URL desconhecido: '{conv}'")
            self.conversores[m.group(2)] = _CONV[conv][1]
            partes.append(f"(?P<{m.group(2)}>{_CONV[conv][0]})")
            pos = m.end()
        partes.append(re.escape(rota[pos:]))
        self.regex = "".join(partes)

    def __repr__(self):
        return f"<URLPattern '{self.rota}'" + (f" [name='{self.name}']>" if self.name else ">")


class URLResolver:
    def __init__(self, rota, padroes, app_name=None, namespace=None):
        self.rota = rota
        self.padroes = padroes
        self.app_name = app_name
        self.namespace = namespace or app_name

    def __repr__(self):
        return f"<URLResolver '{self.rota}' ({self.namespace})>"


def _padroes_auth():
    return ([path("login/", _view_login, name="login"), path("logout/", _view_logout, name="logout")], None)


def include(arg, namespace=None):
    if isinstance(arg, str):
        if arg == "django.contrib.auth.urls":
            return _padroes_auth() + (namespace,)
        raise ImproperlyConfigured(
            f"No PyQuest não há arquivos separados: em vez de include('{arg}'), use include((lista_de_urls, 'nome_do_app')).")
    if isinstance(arg, tuple):
        padroes, app = arg[0], arg[1]
        return (list(padroes), app, namespace or app)
    if isinstance(arg, list):
        return (arg, None, namespace)
    if hasattr(arg, "urlpatterns"):
        return (list(arg.urlpatterns), getattr(arg, "app_name", None), namespace or getattr(arg, "app_name", None))
    raise ImproperlyConfigured("include() recebeu algo inesperado.")


def path(rota, view, kwargs=None, name=None):
    if isinstance(view, tuple):
        padroes, app, ns = (view + (None,))[:3]
        return URLResolver(rota, padroes, app, ns or app)
    if not callable(view):
        raise ImproperlyConfigured(f"A view de path('{rota}', ...) precisa ser uma função.")
    if rota.startswith("/"):
        raise ImproperlyConfigured(f"Rotas não começam com barra: use '{rota.lstrip('/')}' em vez de '{rota}'.")
    return URLPattern(rota, view, kwargs, name)


def re_path(rota, view, kwargs=None, name=None):
    p = path(rota.lstrip("^").rstrip("$"), view, kwargs, name)
    if isinstance(p, URLPattern):
        p.regex = rota.lstrip("^").rstrip("$")
    return p


class _Conf:
    """URLs e templates do código do aluno (lidos do namespace dele)."""

    def __init__(self, ns):
        self.ns = ns
        self.app_name = ns.get("app_name")
        self.padroes = list(ns.get("urlpatterns") or [])

    def raiz(self):
        if self.app_name and not any(isinstance(p, URLResolver) for p in self.padroes):
            return [URLResolver("", self.padroes, self.app_name, self.app_name)]
        return self.padroes

    def templates(self):
        return self.ns.get("TEMPLATES") if isinstance(self.ns.get("TEMPLATES"), dict) else {}


_CONF_ATIVA = [None]


def _conf_atual():
    if _CONF_ATIVA[0] is not None:
        return _CONF_ATIVA[0]
    f = sys._getframe(1)
    while f is not None:
        g = f.f_globals
        if g.get("__name__") == "__main__" and ("urlpatterns" in g or "TEMPLATES" in g):
            return _Conf(g)
        f = f.f_back
    return _Conf({})


def _iterar(padroes, prefixo="", nss=()):
    for p in padroes:
        if isinstance(p, URLResolver):
            novos = nss + ((p.namespace,) if p.namespace else ())
            yield from _iterar(p.padroes, prefixo + p.rota, novos)
        else:
            yield p, prefixo, nss


def reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None):
    conf = _conf_atual()
    args = list(args or [])
    kwargs = dict(kwargs or {})
    partes = viewname.split(":")
    nome, nss = partes[-1], tuple(partes[:-1])
    tentados = []
    for p, prefixo, pnss in _iterar(conf.raiz()):
        if p.name != nome or pnss != nss:
            continue
        rota = prefixo + p.rota
        chaves = list(p.conversores)
        tentados.append(prefixo + p.regex)
        if args and len(args) == len(chaves) and not kwargs:
            valores = dict(zip(chaves, args))
        elif kwargs and set(kwargs) == set(chaves):
            valores = kwargs
        elif not args and not kwargs and not chaves:
            valores = {}
        else:
            continue
        url = re.sub(r"<(?:\w+:)?(\w+)>", lambda m: str(valores[m.group(1)]), rota)
        return "/" + url
    desc = f"with arguments '{tuple(args)}'" if args else (f"with keyword arguments '{kwargs}'" if kwargs else "with no arguments")
    if tentados:
        raise NoReverseMatch(f"Reverse for '{nome}' {desc} not found. {len(tentados)} pattern(s) tried: {tentados}")
    if nss:
        raise NoReverseMatch(f"Reverse for '{viewname}' not found. Confira o app_name ('{':'.join(nss)}') e o name do path().")
    raise NoReverseMatch(f"Reverse for '{nome}' not found. '{nome}' is not a valid view function or pattern name.")


def resolve(caminho, conf=None):
    conf = conf or _conf_atual()
    alvo = caminho.lstrip("/")
    for p, prefixo, nss in _iterar(conf.raiz()):
        m = re.fullmatch(re.escape(prefixo) + p.regex if "<" not in prefixo else prefixo + p.regex, alvo)
        if m:
            kw = {k: p.conversores.get(k, str)(v) for k, v in m.groupdict().items()}
            kw.update(p.default_args)
            return p.view, kw, p, nss
    raise Resolver404(caminho)


def _resolver_url(destino, *args, **kwargs):
    if hasattr(destino, "get_absolute_url"):
        return destino.get_absolute_url()
    destino = str(destino)
    if destino.startswith(("/", "http://", "https://", ".")) or "?" in destino:
        return destino
    return reverse(destino, args=args, kwargs=kwargs)


# ---------------------------------------------------------------------------
# Atalhos (django.shortcuts)
# ---------------------------------------------------------------------------


def redirect(to, *args, permanent=False, **kwargs):
    url = _resolver_url(to, *args, **kwargs)
    return (HttpResponsePermanentRedirect if permanent else HttpResponseRedirect)(url)


def get_object_or_404(klass, *a, **kw):
    qs = klass.objects if isinstance(klass, ModelBase) else klass
    try:
        return qs.get(**kw)
    except ObjectDoesNotExist:
        nome = klass.__name__ if isinstance(klass, ModelBase) else "objeto"
        raise Http404(f"No {nome} matches the given query.")


def get_list_or_404(klass, **kw):
    r = list(klass.objects.filter(**kw))
    if not r:
        raise Http404("Lista vazia.")
    return r


def _buscar_template(nome, conf):
    tpls = conf.templates()
    if nome in tpls:
        return tpls[nome]
    curto = nome.split("/")[-1]
    for k, v in tpls.items():
        if k.split("/")[-1] == curto and k.endswith(nome.split("/", 1)[-1]):
            return v
    if nome in _TEMPLATES_INTERNOS:
        return _TEMPLATES_INTERNOS[nome]
    raise TemplateDoesNotExist(f"{nome} (crie esse template no dicionário TEMPLATES)")


def render(request, template_name, context=None, status=None, **k):
    conf = _conf_atual()
    if isinstance(template_name, (list, tuple)):
        template_name = template_name[0]
    ctx = dict(context or {})
    base = {"request": request, "user": getattr(request, "user", AnonymousUser()),
            "csrf_token": "treino123", "perms": {}}
    texto = Template(_buscar_template(template_name, conf), conf=conf, nome=template_name).render(
        Context({**base, **ctx}))
    r = HttpResponse(texto, status=status)
    r.context = ctx
    r.templates = [template_name]
    return r


def render_to_string(template_name, context=None, request=None):
    conf = _conf_atual()
    return Template(_buscar_template(template_name, conf), conf=conf, nome=template_name).render(Context(context or {}))


# ---------------------------------------------------------------------------
# Decoradores
# ---------------------------------------------------------------------------


def login_required(funcao=None, login_url=None, redirect_field_name="next"):
    def decorar(view):
        @functools.wraps(view)
        def embrulho(request, *a, **k):
            if not request.user.is_authenticated:
                url = _resolver_url(login_url or settings.LOGIN_URL)
                return HttpResponseRedirect(f"{url}?{redirect_field_name}={request.path}")
            return view(request, *a, **k)
        return embrulho
    return decorar(funcao) if funcao else decorar


def require_POST(view):
    @functools.wraps(view)
    def embrulho(request, *a, **k):
        if request.method != "POST":
            return HttpResponse("Method Not Allowed", status=405)
        return view(request, *a, **k)
    return embrulho


# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------


class Context(dict):
    pass


_MESES = ["Jan.", "Feb.", "March", "April", "May", "June", "July", "Aug.", "Sept.", "Oct.", "Nov.", "Dec."]
_MESES_LONGOS = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                 "October", "November", "December"]
_MESES_CURTOS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def _formatar_data(v, fmt):
    if not isinstance(v, (_dt.date, _dt.datetime)):
        return ""
    out = []
    escapar = False
    for ch in fmt:
        if escapar:
            out.append(ch)
            escapar = False
            continue
        if ch == "\\":
            escapar = True
            continue
        tem_hora = isinstance(v, _dt.datetime)
        tabela = {
            "d": f"{v.day:02d}", "j": str(v.day), "m": f"{v.month:02d}", "n": str(v.month),
            "M": _MESES_CURTOS[v.month - 1], "N": _MESES[v.month - 1], "F": _MESES_LONGOS[v.month - 1],
            "Y": str(v.year), "y": f"{v.year % 100:02d}",
            "H": f"{v.hour:02d}" if tem_hora else "00", "G": str(v.hour) if tem_hora else "0",
            "i": f"{v.minute:02d}" if tem_hora else "00", "s": f"{v.second:02d}" if tem_hora else "00",
            "D": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][v.weekday()],
            "l": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][v.weekday()],
        }
        out.append(tabela.get(ch, ch))
    return "".join(out)


def _filtro(nome, v, arg):
    if nome == "date":
        return _formatar_data(v, arg if arg is not None else "N j, Y")
    if nome == "time":
        return _formatar_data(v, arg if arg is not None else "H:i")
    if nome == "upper":
        return str(v).upper()
    if nome == "lower":
        return str(v).lower()
    if nome == "title":
        return str(v).title()
    if nome == "capfirst":
        s = str(v)
        return s[:1].upper() + s[1:]
    if nome == "length":
        try:
            return len(v)
        except TypeError:
            return 0
    if nome == "default":
        return v if v else arg
    if nome == "default_if_none":
        return arg if v is None else v
    if nome == "truncatechars":
        s, n = str(v), int(arg)
        return s if len(s) <= n else s[:max(n - 1, 0)] + "…"
    if nome == "truncatewords":
        palavras, n = str(v).split(), int(arg)
        return " ".join(palavras[:n]) + (" …" if len(palavras) > n else "")
    if nome == "linebreaks":
        paragrafos = re.split(r"\n{2,}", str(_esc(v)).replace("\r\n", "\n").strip())
        return SafeString("\n\n".join("<p>" + p.replace("\n", "<br>") + "</p>" for p in paragrafos if p))
    if nome == "linebreaksbr":
        return SafeString(str(_esc(v)).replace("\n", "<br>"))
    if nome == "safe":
        return SafeString(str(v))
    if nome == "escape":
        return _esc(v)
    if nome == "join":
        return str(arg).join(str(x) for x in v)
    if nome == "add":
        try:
            return int(v) + int(arg)
        except (TypeError, ValueError):
            return str(v) + str(arg)
    if nome == "pluralize":
        sufixo = arg if arg is not None else "s"
        um, varios = (sufixo.split(",") + [""])[:2] if "," in sufixo else ("", sufixo)
        try:
            n = len(v) if not isinstance(v, (int, float)) else v
        except TypeError:
            n = 0
        return um if n == 1 else varios
    if nome == "first":
        return v[0] if v else ""
    if nome == "last":
        return v[-1] if v else ""
    if nome == "slugify":
        return re.sub(r"[^a-z0-9]+", "-", str(v).lower()).strip("-")
    if nome == "yesno":
        opcoes = (arg or "yes,no").split(",")
        return opcoes[0] if v else opcoes[1]
    raise TemplateSyntaxError(f"Invalid filter: '{nome}'")


_TOKEN = re.compile(r"({{.*?}}|{%.*?%}|{#.*?#})", re.S)


def _dividir_args(s):
    return re.findall(r"""(?:[^\s"']+|"[^"]*"|'[^']*')+""", s)


class _No:
    pass


class _Texto(_No):
    def __init__(self, t):
        self.t = t

    def render(self, ctx, tpl):
        return self.t


class _Var(_No):
    def __init__(self, expr):
        self.expr = expr.strip()

    def render(self, ctx, tpl):
        v = tpl.avaliar(self.expr, ctx)
        if v is None:
            return "None"
        return str(_esc(v)) if tpl.autoescape else str(v)


class _For(_No):
    def __init__(self, nomes, alvo, corpo, vazio, invertido):
        self.nomes, self.alvo, self.corpo, self.vazio, self.invertido = nomes, alvo, corpo, vazio, invertido

    def render(self, ctx, tpl):
        seq = tpl.avaliar(self.alvo, ctx)
        if seq is None or seq == "":
            seq = []
        if isinstance(seq, Manager):
            raise TemplateSyntaxError(f"'{self.alvo}' é um Manager. Use {self.alvo}.all no for.")
        itens = list(seq)
        if self.invertido:
            itens.reverse()
        if not itens:
            return tpl.render_nos(self.vazio, ctx)
        out = []
        pai = ctx.get("forloop")
        for i, item in enumerate(itens):
            novo = Context(ctx)
            novo["forloop"] = {"counter": i + 1, "counter0": i, "first": i == 0, "last": i == len(itens) - 1,
                               "revcounter": len(itens) - i, "parentloop": pai}
            if len(self.nomes) == 1:
                novo[self.nomes[0]] = item
            else:
                for n, v in zip(self.nomes, item):
                    novo[n] = v
            out.append(tpl.render_nos(self.corpo, novo))
        return "".join(out)


class _If(_No):
    def __init__(self, ramos):
        self.ramos = ramos  # lista de (condição ou None, corpo)

    def render(self, ctx, tpl):
        for cond, corpo in self.ramos:
            if cond is None or tpl.condicao(cond, ctx):
                return tpl.render_nos(corpo, ctx)
        return ""


class _Url(_No):
    def __init__(self, args):
        self.args = args

    def render(self, ctx, tpl):
        partes = list(self.args)
        como = None
        if len(partes) >= 2 and partes[-2] == "as":
            como = partes[-1]
            partes = partes[:-2]
        if not partes:
            raise TemplateSyntaxError("'url' precisa do nome da URL, por exemplo {% url 'learning_logs:index' %}")
        nome = tpl.avaliar(partes[0], ctx)
        args, kwargs = [], {}
        for p in partes[1:]:
            if "=" in p and not p.startswith(("'", '"')):
                k, v = p.split("=", 1)
                kwargs[k] = tpl.avaliar(v, ctx)
            else:
                args.append(tpl.avaliar(p, ctx))
        _CONF_ATIVA_TEMP = _CONF_ATIVA[0]
        try:
            if _CONF_ATIVA[0] is None and tpl.conf is not None:
                _CONF_ATIVA[0] = tpl.conf
            url = reverse(str(nome), args=args, kwargs=kwargs)
        finally:
            _CONF_ATIVA[0] = _CONF_ATIVA_TEMP
        if como:
            ctx[como] = url
            return ""
        return url


class _Bloco(_No):
    def __init__(self, nome, corpo):
        self.nome, self.corpo = nome, corpo

    def render(self, ctx, tpl):
        corpo = tpl.blocos_filho.get(self.nome, self.corpo)
        return tpl.render_nos(corpo, ctx)


class _Simples(_No):
    def __init__(self, f):
        self.f = f

    def render(self, ctx, tpl):
        return self.f(ctx, tpl)


class _With(_No):
    def __init__(self, atribs, corpo):
        self.atribs, self.corpo = atribs, corpo

    def render(self, ctx, tpl):
        novo = Context(ctx)
        for k, v in self.atribs:
            novo[k] = tpl.avaliar(v, ctx)
        return tpl.render_nos(self.corpo, novo)


class _Extends(_No):
    def __init__(self, nome):
        self.nome = nome


class _Include(_No):
    def __init__(self, nome):
        self.nome = nome

    def render(self, ctx, tpl):
        nome = tpl.avaliar(self.nome, ctx)
        sub = Template(_buscar_template(nome, tpl.conf or _conf_atual()), conf=tpl.conf, nome=nome, prof=tpl.prof + 1)
        return sub.render(ctx)


_TAGS_IGNORADAS = {"load", "bootstrap_css", "bootstrap_javascript", "bootstrap_messages", "spaceless",
                   "endspaceless", "autoescape", "endautoescape"}


class Template:
    def __init__(self, texto, conf=None, nome="<template>", prof=0):
        if prof > 10:
            raise TemplateSyntaxError("Templates se estendendo em círculo (extends demais).")
        self.texto = texto
        self.conf = conf
        self.nome = nome
        self.prof = prof
        self.autoescape = True
        self.blocos_filho = {}
        tokens = [t for t in _TOKEN.split(texto) if t]
        self.pos = 0
        self.tokens = tokens
        self.nos = self._parse(())
        if self.pos < len(self.tokens):
            raise TemplateSyntaxError(f"Tag inesperada: {self.tokens[self.pos]}")

    # ---- parser ----
    def _parse(self, fins):
        nos = []
        while self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            if tok.startswith("{#"):
                self.pos += 1
                continue
            if tok.startswith("{{"):
                nos.append(_Var(tok[2:-2]))
                self.pos += 1
                continue
            if not tok.startswith("{%"):
                nos.append(_Texto(tok))
                self.pos += 1
                continue
            conteudo = tok[2:-2].strip()
            partes = _dividir_args(conteudo)
            if not partes:
                raise TemplateSyntaxError("Tag vazia {% %}.")
            tag = partes[0]
            if tag in fins:
                return nos
            self.pos += 1
            if tag == "for":
                if "in" not in partes:
                    raise TemplateSyntaxError("Use {% for item in lista %}.")
                i = partes.index("in")
                nomes = [n.strip() for n in " ".join(partes[1:i]).split(",") if n.strip()]
                resto = partes[i + 1:]
                invertido = bool(resto) and resto[-1] == "reversed"
                alvo = " ".join(resto[:-1] if invertido else resto)
                corpo = self._parse(("empty", "endfor"))
                vazio = []
                if self._tag_atual() == "empty":
                    self.pos += 1
                    vazio = self._parse(("endfor",))
                self._esperar("endfor")
                nos.append(_For(nomes, alvo, corpo, vazio, invertido))
            elif tag == "if":
                ramos = []
                cond = " ".join(partes[1:])
                while True:
                    corpo = self._parse(("elif", "else", "endif"))
                    ramos.append((cond, corpo))
                    t = self._tag_atual()
                    if t == "elif":
                        cond = " ".join(_dividir_args(self.tokens[self.pos][2:-2].strip())[1:])
                        self.pos += 1
                        continue
                    if t == "else":
                        self.pos += 1
                        ramos.append((None, self._parse(("endif",))))
                    self._esperar("endif")
                    break
                nos.append(_If(ramos))
            elif tag == "block":
                if len(partes) < 2:
                    raise TemplateSyntaxError("Use {% block nome %}.")
                corpo = self._parse(("endblock",))
                self._esperar("endblock")
                nos.append(_Bloco(partes[1], corpo))
            elif tag == "with":
                atribs = [tuple(p.split("=", 1)) for p in partes[1:] if "=" in p]
                corpo = self._parse(("endwith",))
                self._esperar("endwith")
                nos.append(_With(atribs, corpo))
            elif tag == "comment":
                self._parse(("endcomment",))
                self._esperar("endcomment")
            elif tag == "extends":
                nos.append(_Extends(partes[1]))
            elif tag == "include":
                nos.append(_Include(partes[1]))
            elif tag == "url":
                nos.append(_Url(partes[1:]))
            elif tag == "csrf_token":
                nos.append(_Texto('<input type="hidden" name="csrfmiddlewaretoken" value="treino123">'))
            elif tag == "bootstrap_form":
                alvo = partes[1]
                nos.append(_Simples(lambda ctx, tpl, alvo=alvo: str(_form_html(tpl.avaliar(alvo, ctx), bootstrap=True))))
            elif tag == "bootstrap_button":
                texto = partes[1].strip("'\"") if len(partes) > 1 else "Enviar"
                for p in partes[2:]:
                    if p.startswith("content="):
                        texto = p.split("=", 1)[1].strip("'\"")
                if len(partes) > 1 and partes[1].startswith("content="):
                    texto = partes[1].split("=", 1)[1].strip("'\"")
                nos.append(_Texto(f'<button class="btn btn-primary" type="submit">{_html.escape(texto)}</button>'))
            elif tag in _TAGS_IGNORADAS:
                pass
            elif tag in ("endfor", "endif", "endblock", "empty", "else", "elif", "endwith", "endcomment"):
                raise TemplateSyntaxError(f"{{% {tag} %}} sem a tag de abertura correspondente.")
            else:
                raise TemplateSyntaxError(f"Invalid block tag: '{tag}'")
        if fins:
            raise TemplateSyntaxError(f"Faltou fechar com {{% {fins[-1]} %}}.")
        return nos

    def _tag_atual(self):
        if self.pos >= len(self.tokens):
            return None
        t = self.tokens[self.pos]
        if not t.startswith("{%"):
            return None
        p = _dividir_args(t[2:-2].strip())
        return p[0] if p else None

    def _esperar(self, tag):
        if self._tag_atual() != tag:
            raise TemplateSyntaxError(f"Faltou {{% {tag} %}}.")
        self.pos += 1

    # ---- avaliação ----
    def avaliar(self, expr, ctx):
        partes = re.split(r"\|(?=(?:[^'\"]|'[^']*'|\"[^\"]*\")*$)", expr.strip())
        v = self._valor(partes[0].strip(), ctx)
        for f in partes[1:]:
            f = f.strip()
            if ":" in f:
                nome, arg = f.split(":", 1)
                arg = self._valor(arg.strip(), ctx)
            else:
                nome, arg = f, None
            v = _filtro(nome.strip(), v, arg)
        return v

    def _valor(self, t, ctx):
        if not t:
            return ""
        if (t[0] == t[-1]) and t[0] in "'\"" and len(t) >= 2:
            return t[1:-1]
        if re.fullmatch(r"-?\d+", t):
            return int(t)
        if re.fullmatch(r"-?\d+\.\d+", t):
            return float(t)
        if t in ("True", "False", "None"):
            return {"True": True, "False": False, "None": None}[t]
        partes = t.split(".")
        if partes[0] not in ctx:
            return ""
        v = ctx[partes[0]]
        for p in partes[1:]:
            try:
                if isinstance(v, dict) and p in v:
                    v = v[p]
                elif re.fullmatch(r"\d+", p) and not hasattr(v, p):
                    v = v[int(p)]
                else:
                    v = getattr(v, p)
            except (AttributeError, KeyError, IndexError, TypeError):
                return ""
            if callable(v) and not isinstance(v, (type, Manager)):
                try:
                    v = v()
                except TypeError:
                    return ""
        if callable(v) and not isinstance(v, (type, Manager)) and not isinstance(v, (str, int)):
            try:
                v = v()
            except TypeError:
                pass
        return v

    def condicao(self, cond, ctx):
        for parte in re.split(r"\s+or\s+", cond):
            if all(self._cond_simples(e.strip(), ctx) for e in re.split(r"\s+and\s+", parte)):
                return True
        return False

    def _cond_simples(self, e, ctx):
        neg = False
        while e.startswith("not "):
            neg = not neg
            e = e[4:].strip()
        m = re.match(r"(.+?)\s*(==|!=|>=|<=|>|<|\snot in\s|\sin\s)\s*(.+)$", e)
        if m:
            a, op, b = self.avaliar(m.group(1), ctx), m.group(2).strip(), self.avaliar(m.group(3), ctx)
            try:
                r = {"==": lambda: a == b, "!=": lambda: a != b, ">": lambda: a > b, "<": lambda: a < b,
                     ">=": lambda: a >= b, "<=": lambda: a <= b, "in": lambda: a in b,
                     "not in": lambda: a not in b}[op]()
            except TypeError:
                r = False
        else:
            v = self.avaliar(e, ctx)
            if isinstance(v, Manager):
                v = v.exists()
            r = bool(v)
        return r != neg

    # ---- renderização ----
    def render_nos(self, nos, ctx):
        return "".join(n.render(ctx, self) for n in nos)

    def render(self, ctx=None):
        ctx = ctx if isinstance(ctx, Context) else Context(ctx or {})
        anterior = _CONF_ATIVA[0]
        if anterior is None and self.conf is not None:
            _CONF_ATIVA[0] = self.conf
        try:
            ext = next((n for n in self.nos if isinstance(n, _Extends)), None)
            if ext is None:
                return self.render_nos(self.nos, ctx)
            nome = self.avaliar(ext.nome, ctx)
            pai = Template(_buscar_template(nome, self.conf or _conf_atual()), conf=self.conf, nome=nome,
                           prof=self.prof + 1)
            blocos = {}

            def coletar(nos):
                for n in nos:
                    if isinstance(n, _Bloco):
                        blocos[n.nome] = n.corpo
                        coletar(n.corpo)
            coletar(self.nos)
            pai.blocos_filho = {**blocos, **{k: v for k, v in self.blocos_filho.items()}}
            return pai.render(ctx)
        finally:
            _CONF_ATIVA[0] = anterior


# ---------------------------------------------------------------------------
# Formulários
# ---------------------------------------------------------------------------


class Widget:
    input_type = "text"

    def __init__(self, attrs=None):
        self.attrs = dict(attrs or {})


class TextInput(Widget):
    pass


class Textarea(Widget):
    pass


class PasswordInput(Widget):
    input_type = "password"


class EmailInput(Widget):
    input_type = "email"


class NumberInput(Widget):
    input_type = "number"


class CheckboxInput(Widget):
    input_type = "checkbox"


class _CampoForm:
    """Descreve um campo de formulário (vindo do model ou declarado)."""

    def __init__(self, nome, rotulo, obrigatorio=True, max_length=None, textarea=False, tipo="text",
                 widget=None, conversor=None, ajuda=""):
        self.nome, self.rotulo, self.obrigatorio = nome, rotulo, obrigatorio
        self.max_length, self.textarea, self.tipo = max_length, textarea, tipo
        self.widget, self.conversor, self.ajuda = widget, conversor, ajuda


class BoundField:
    def __init__(self, form, campo):
        self.form, self.campo = form, campo
        self.name = campo.nome
        self.label = campo.rotulo
        self.errors = form.errors.get(campo.nome, [])

    @property
    def value(self):
        return self.form._valor_inicial(self.campo.nome)

    def __str__(self):
        return str(_input_html(self.form, self.campo))


def _rotulo_padrao(nome):
    return nome.replace("_", " ").capitalize()


class BaseForm:
    campos_declarados = []

    def __init__(self, data=None, files=None, instance=None, initial=None, **k):
        self.data = QueryDict(data) if data is not None else QueryDict()
        self.is_bound = data is not None
        self.initial = dict(initial or {})
        self.errors = {}
        self.cleaned_data = {}
        self._validado = False

    def _campos(self):
        return self.campos_declarados

    @property
    def fields(self):
        return {c.nome: c for c in self._campos()}

    def __getitem__(self, nome):
        return BoundField(self, self.fields[nome])

    def __iter__(self):
        return iter(BoundField(self, c) for c in self._campos())

    def _valor_inicial(self, nome):
        if self.is_bound:
            return self.data.get(nome, "")
        return self.initial.get(nome, "")

    def full_clean(self):
        self.errors = {}
        self.cleaned_data = {}
        for c in self._campos():
            bruto = self.data.get(c.nome, "")
            if bruto is None:
                bruto = ""
            valor = bruto.strip() if isinstance(bruto, str) and c.tipo != "password" else bruto
            if c.tipo == "checkbox":
                self.cleaned_data[c.nome] = valor not in ("", "off", "false", "False", None)
                continue
            if valor in ("", None):
                if c.obrigatorio:
                    self.errors.setdefault(c.nome, []).append("Este campo é obrigatório.")
                self.cleaned_data[c.nome] = "" if not c.conversor else None
                continue
            if c.max_length and len(str(valor)) > c.max_length:
                self.errors.setdefault(c.nome, []).append(
                    f"Certifique-se de que o valor tenha no máximo {c.max_length} caracteres (ele possui {len(str(valor))}).")
                continue
            if c.conversor:
                try:
                    valor = c.conversor(valor)
                except (TypeError, ValueError):
                    self.errors.setdefault(c.nome, []).append("Informe um número válido.")
                    continue
            self.cleaned_data[c.nome] = valor
        self.clean_extra()
        self._validado = True

    def clean_extra(self):
        pass

    def add_error(self, campo, erro):
        self.errors.setdefault(campo or "__all__", []).append(str(erro))

    def is_valid(self):
        if not self.is_bound:
            return False
        self.full_clean()
        return not self.errors

    def non_field_errors(self):
        return self.errors.get("__all__", [])

    def as_div(self):
        return _form_html(self)

    def as_p(self):
        return _form_html(self, tag="p")

    def __str__(self):
        return str(_form_html(self))


def _input_html(form, c):
    valor = form._valor_inicial(c.nome)
    attrs = dict(c.widget.attrs) if c.widget else {}
    extra = "".join(f' {k}="{_html.escape(str(v))}"' for k, v in attrs.items() if k not in ("class",))
    classe = attrs.get("class", "")
    classe_attr = f' class="{classe}"' if classe else ""
    obrig = " required" if c.obrigatorio else ""
    ident = f"id_{c.nome}"
    if c.textarea or isinstance(c.widget, Textarea):
        cols = "" if "cols" in attrs else ' cols="40"'
        rows = "" if "rows" in attrs else ' rows="10"'
        return SafeString(f'<textarea name="{c.nome}"{cols}{rows}{classe_attr}{extra}{obrig} id="{ident}">'
                          f'{_html.escape(str(valor or ""))}</textarea>')
    tipo = c.widget.input_type if c.widget and not isinstance(c.widget, TextInput) else c.tipo
    ml = f' maxlength="{c.max_length}"' if c.max_length else ""
    val = f' value="{_html.escape(str(valor))}"' if valor not in ("", None) and tipo != "password" else ""
    return SafeString(f'<input type="{tipo}" name="{c.nome}"{val}{ml}{classe_attr}{extra}{obrig} id="{ident}">')


def _form_html(form, tag="div", bootstrap=False):
    if not isinstance(form, BaseForm):
        return SafeString("")
    out = []
    for erro in form.non_field_errors():
        out.append(f'<ul class="errorlist nonfield"><li>{_html.escape(erro)}</li></ul>')
    for c in form._campos():
        partes = []
        if c.rotulo:
            partes.append(f'<label for="id_{c.nome}">{_html.escape(c.rotulo)}:</label>')
        erros = form.errors.get(c.nome, [])
        if erros:
            partes.append('<ul class="errorlist">' + "".join(f"<li>{_html.escape(e)}</li>" for e in erros) + "</ul>")
        partes.append(str(_input_html(form, c)))
        if c.ajuda:
            partes.append(f'<div class="helptext">{_html.escape(c.ajuda)}</div>')
        cls = ' class="mb-3"' if bootstrap else ""
        out.append(f"<{tag}{cls}>\n    " + "\n    ".join(partes) + f"\n</{tag}>")
    return SafeString("\n".join(out))


class ModelForm(BaseForm):
    def __init__(self, data=None, files=None, instance=None, initial=None, **k):
        super().__init__(data, files, instance, initial)
        meta = getattr(type(self), "Meta", None)
        if meta is None or not hasattr(meta, "model"):
            raise ValueError("ModelForm precisa de uma class Meta com model = ... e fields = [...].")
        self._model = meta.model
        if not hasattr(meta, "fields") and not hasattr(meta, "exclude"):
            raise ImproperlyConfigured(
                f"Creating a ModelForm without either the 'fields' attribute or the 'exclude' attribute is prohibited; "
                f"form {type(self).__name__} needs updating.")
        self.instance = instance if instance is not None else self._model()

    def _campos(self):
        meta = type(self).Meta
        nomes = getattr(meta, "fields", None)
        if nomes == "__all__" or nomes is None:
            exc = set(getattr(meta, "exclude", []) or [])
            nomes = [n for n, c in self._model._campos.items() if n != "id" and n not in exc
                     and not getattr(c, "auto_now_add", False) and not getattr(c, "auto_now", False)]
        rotulos = getattr(meta, "labels", {}) or {}
        widgets = getattr(meta, "widgets", {}) or {}
        campos = []
        for n in nomes:
            if n not in self._model._campos:
                raise FieldError(f"Unknown field(s) ({n}) specified for {self._model.__name__}")
            f = self._model._campos[n]
            rot = rotulos.get(n, f.verbose_name.capitalize() if f.verbose_name else _rotulo_padrao(n))
            if isinstance(f, ForeignKey):
                conv = (lambda v, f=f: f.alvo().objects.get(id=int(v)))
            elif isinstance(f, (IntegerField, FloatField)):
                conv = f.converter
            else:
                conv = None
            campos.append(_CampoForm(n, rot, obrigatorio=not f.blank and not isinstance(f, BooleanField),
                                     max_length=f.max_length, textarea=isinstance(f, TextField),
                                     tipo=f.tipo_input, widget=widgets.get(n), conversor=conv))
        return campos

    def _valor_inicial(self, nome):
        if self.is_bound:
            return self.data.get(nome, "")
        if nome in self.initial:
            return self.initial[nome]
        v = getattr(self.instance, nome, "")
        if isinstance(v, Model):
            return v.id
        return "" if v is None else v

    def save(self, commit=True):
        if not self._validado:
            self.is_valid()
        if self.errors:
            raise ValueError(f"The {self._model.__name__} could not be created because the data didn't validate.")
        for k, v in self.cleaned_data.items():
            object.__setattr__(self.instance, k, v)
        if commit:
            self.instance.save()
        return self.instance


class Form(BaseForm):
    pass


class UserCreationForm(BaseForm):
    campos_declarados = [
        _CampoForm("username", "Username", max_length=150,
                   ajuda="Obrigatório. 150 caracteres ou menos. Letras, números e @/./+/-/_ apenas."),
        _CampoForm("password1", "Password", tipo="password"),
        _CampoForm("password2", "Password confirmation", tipo="password",
                   ajuda="Informe a mesma senha de antes, para verificação."),
    ]

    def __init__(self, data=None, *a, **k):
        super().__init__(data, *a, **k)
        self.instance = None

    def clean_extra(self):
        d = self.cleaned_data
        u = d.get("username")
        if u and User.objects.filter(username=u).exists():
            self.add_error("username", "Um usuário com este nome de usuário já existe.")
        if u and not re.fullmatch(r"[\w.@+-]+", u):
            self.add_error("username", "Informe um nome de usuário válido.")
        p1, p2 = d.get("password1"), d.get("password2")
        if p1 and p2 and p1 != p2:
            self.add_error("password2", "Os dois campos de senha não correspondem.")
        elif p1:
            if len(p1) < 8:
                self.add_error("password2", "Esta senha é muito curta. Ela precisa conter pelo menos 8 caracteres.")
            if p1.isdigit():
                self.add_error("password2", "Esta senha é inteiramente numérica.")

    def save(self, commit=True):
        if not self._validado:
            self.is_valid()
        if self.errors:
            raise ValueError("The User could not be created because the data didn't validate.")
        u = User(username=self.cleaned_data["username"])
        u.set_password(self.cleaned_data["password1"])
        if commit:
            u.save()
        self.instance = u
        return u


class AuthenticationForm(BaseForm):
    campos_declarados = [_CampoForm("username", "Username", max_length=150),
                         _CampoForm("password", "Password", tipo="password")]

    def __init__(self, request=None, data=None, *a, **k):
        super().__init__(data, *a, **k)
        self.request = request
        self.user_cache = None

    def clean_extra(self):
        u, p = self.cleaned_data.get("username"), self.cleaned_data.get("password")
        if u and p:
            self.user_cache = authenticate(self.request, username=u, password=p)
            if self.user_cache is None:
                self.add_error(None, "Por favor, entre com um usuário e senha corretos.")

    def get_user(self):
        return self.user_cache


# Views prontas de login/logout (include('django.contrib.auth.urls'))
_TEMPLATES_INTERNOS = {
    "registration/login.html": "<h1>Log in</h1>\n<form method=\"post\">{% csrf_token %}{{ form.as_div }}"
                               "<button>Log in</button></form>",
    "registration/logged_out.html": "<p>Você saiu da sua conta.</p>",
}


def _view_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            destino = request.GET.get("next") or request.POST.get("next") or settings.LOGIN_REDIRECT_URL
            return redirect(destino)
    else:
        form = AuthenticationForm(request)
    return render(request, "registration/login.html", {"form": form, "next": request.GET.get("next", "")})


def _view_logout(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed (GET): use um formulário com method=\"post\" para sair.", status=405)
    logout(request)
    if settings.LOGOUT_REDIRECT_URL:
        return redirect(settings.LOGOUT_REDIRECT_URL)
    return render(request, "registration/logged_out.html", {})


# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------


class _AdminSite:
    def __init__(self):
        self._registry = {}
        self.urls = ([], "admin", "admin")

    def register(self, modelo, admin_class=None, **k):
        modelos = modelo if isinstance(modelo, (list, tuple)) else [modelo]
        for m in modelos:
            if m in self._registry:
                raise ImproperlyConfigured(f"The model {m.__name__} is already registered.")
            self._registry[m] = admin_class

    def is_registered(self, modelo):
        return modelo in self._registry


class ModelAdmin:
    pass


# ---------------------------------------------------------------------------
# Client de teste: um "navegador" que abre as páginas do seu código
# ---------------------------------------------------------------------------


class Client:
    def __init__(self, ns=None):
        if ns is None:
            f = sys._getframe(1)
            ns = f.f_globals
        self._ns = ns
        self.user = None
        self.session = {}

    def _conf(self):
        return _Conf(self._ns)

    def login(self, username=None, password=None, **k):
        u = authenticate(username=username, password=password)
        if u is None:
            return False
        self.user = u
        self.session = {"_auth_user_id": u.id}
        return True

    def force_login(self, user, backend=None):
        self.user = user
        self.session = {"_auth_user_id": user.id}

    def logout(self):
        self.user = None
        self.session = {}

    def get(self, caminho, data=None, follow=False, **k):
        return self._req("GET", caminho, data, follow)

    def post(self, caminho, data=None, follow=False, **k):
        return self._req("POST", caminho, data, follow)

    def _req(self, metodo, caminho, data, follow, saltos=0):
        caminho = str(caminho)
        consulta = {}
        if "?" in caminho:
            caminho, qs = caminho.split("?", 1)
            for par in qs.split("&"):
                if par:
                    k, _, v = par.partition("=")
                    consulta[k] = v
        get = dict(consulta)
        post = {}
        if metodo == "GET" and data:
            get.update({k: str(v) for k, v in data.items()})
        elif data:
            post = {k: (v if isinstance(v, list) else str(v)) for k, v in data.items()}
        conf = self._conf()
        for chave in ("LOGIN_URL", "LOGIN_REDIRECT_URL", "LOGOUT_REDIRECT_URL", "DEBUG", "ALLOWED_HOSTS"):
            if chave in self._ns:
                setattr(settings, chave, self._ns[chave])
        req = HttpRequest(metodo, caminho, get, post, self.user or AnonymousUser(), dict(self.session))
        anterior = _CONF_ATIVA[0]
        _CONF_ATIVA[0] = conf
        try:
            try:
                view, kwargs, padrao, nss = resolve(caminho, conf)
            except Resolver404:
                resp = self._pagina_404(req, conf, f"Nenhuma URL combina com '{caminho}'.")
            else:
                req.resolver_match = types.SimpleNamespace(url_name=padrao.name, namespaces=list(nss),
                                                           view_name=":".join(list(nss) + [padrao.name or ""]),
                                                           kwargs=kwargs)
                try:
                    resp = view(req, **kwargs)
                except Http404 as e:
                    resp = self._pagina_404(req, conf, str(e))
                except PermissionDenied:
                    resp = HttpResponseForbidden("<h1>403 Forbidden</h1>")
                if resp is None:
                    raise ValueError(f"The view {getattr(view, '__name__', 'view')} didn't return an HttpResponse "
                                     f"object. It returned None instead. (Faltou um return na view?)")
                if not isinstance(resp, HttpResponse):
                    raise ValueError(f"A view {getattr(view, '__name__', 'view')} devolveu {type(resp).__name__}, "
                                     f"mas precisa devolver um HttpResponse (use render, redirect ou HttpResponse).")
        finally:
            _CONF_ATIVA[0] = anterior
        if req.user is not None and req.user.is_authenticated:
            self.user = req.user
        else:
            self.user = None
        self.session = dict(req.session)
        resp.request = {"PATH_INFO": caminho, "REQUEST_METHOD": metodo}
        resp.wsgi_request = req
        resp.redirect_chain = []
        if follow and isinstance(resp, HttpResponseRedirect) and saltos < 10:
            seguinte = self._req("GET", resp.url, None, True, saltos + 1)
            seguinte.redirect_chain = [(resp.url, resp.status_code)] + seguinte.redirect_chain
            return seguinte
        return resp

    def _pagina_404(self, req, conf, motivo):
        if "404.html" in conf.templates():
            texto = Template(conf.templates()["404.html"], conf=conf, nome="404.html").render(
                Context({"request": req, "user": req.user, "exception": motivo}))
            return HttpResponseNotFound(texto)
        return HttpResponseNotFound(f"<h1>Not Found</h1><p>{_html.escape(motivo)}</p>")


class PermissionDenied(Exception):
    pass


def assertContains(resp, texto, status_code=200):
    assert resp.status_code == status_code, f"Status {resp.status_code}, esperado {status_code}"
    assert str(texto) in resp.content, f"'{texto}' não aparece na página"


# ---------------------------------------------------------------------------
# Montagem dos módulos "django.*"
# ---------------------------------------------------------------------------


def _timezone_now():
    return _agora()


def reiniciar():
    """Zera o estado entre execuções (banco em memória, relógio, configurações)."""
    for nome in list(_REGISTRO):
        if _REGISTRO[nome] is not User:
            del _REGISTRO[nome]
    _REGISTRO["user"] = User
    User._dados.clear()
    User._prox_id[0] = 1
    _RELOGIO[0] = _INICIO
    _CONF_ATIVA[0] = None
    settings.reiniciar()
    admin_site._registry.clear()


admin_site = _AdminSite()


def _modulo(nome, **attrs):
    m = types.ModuleType(nome)
    m.__file__ = "django_de_treino"
    m.__dict__.update(attrs)
    return m


def _criar_modulos():
    mods = {}
    mods["django"] = _modulo("django", VERSION=(5, 0, 0, "treino", 0), __version__=__version__,
                             get_version=lambda: __version__, setup=lambda: None)
    models = _modulo(
        "django.db.models", Model=Model, CharField=CharField, TextField=TextField, IntegerField=IntegerField,
        PositiveIntegerField=PositiveIntegerField, FloatField=FloatField, BooleanField=BooleanField,
        DateTimeField=DateTimeField, DateField=DateField, EmailField=EmailField, SlugField=SlugField,
        URLField=URLField, ForeignKey=ForeignKey, OneToOneField=OneToOneField, CASCADE=CASCADE, PROTECT=PROTECT,
        SET_NULL=SET_NULL, DO_NOTHING=DO_NOTHING, Manager=Manager, QuerySet=QuerySet, AutoField=AutoField)
    mods["django.db.models"] = models
    mods["django.db"] = _modulo("django.db", models=models, IntegrityError=IntegrityError)
    mods["django.core"] = _modulo("django.core")
    mods["django.core.exceptions"] = _modulo(
        "django.core.exceptions", ObjectDoesNotExist=ObjectDoesNotExist, ValidationError=ValidationError,
        FieldError=FieldError, ImproperlyConfigured=ImproperlyConfigured, PermissionDenied=PermissionDenied,
        MultipleObjectsReturned=MultipleObjectsReturned)
    mods["django.http"] = _modulo(
        "django.http", HttpRequest=HttpRequest, HttpResponse=HttpResponse, HttpResponseRedirect=HttpResponseRedirect,
        HttpResponsePermanentRedirect=HttpResponsePermanentRedirect, HttpResponseNotFound=HttpResponseNotFound,
        HttpResponseForbidden=HttpResponseForbidden, JsonResponse=JsonResponse, Http404=Http404, QueryDict=QueryDict)
    mods["django.shortcuts"] = _modulo("django.shortcuts", render=render, redirect=redirect,
                                       get_object_or_404=get_object_or_404, get_list_or_404=get_list_or_404)
    mods["django.urls"] = _modulo("django.urls", path=path, re_path=re_path, include=include, reverse=reverse,
                                  resolve=resolve, NoReverseMatch=NoReverseMatch, Resolver404=Resolver404)
    mods["django.conf"] = _modulo("django.conf", settings=settings)
    mods["django.template"] = _modulo("django.template", Template=Template, Context=Context,
                                      TemplateDoesNotExist=TemplateDoesNotExist, TemplateSyntaxError=TemplateSyntaxError)
    mods["django.template.loader"] = _modulo("django.template.loader", render_to_string=render_to_string)
    mods["django.utils"] = _modulo("django.utils")
    mods["django.utils.timezone"] = _modulo("django.utils.timezone", now=_timezone_now)
    mods["django.utils.safestring"] = _modulo("django.utils.safestring", mark_safe=mark_safe, SafeString=SafeString)
    mods["django.utils.html"] = _modulo("django.utils.html", escape=_esc)
    widgets = dict(Widget=Widget, TextInput=TextInput, Textarea=Textarea, PasswordInput=PasswordInput,
                   EmailInput=EmailInput, NumberInput=NumberInput, CheckboxInput=CheckboxInput)
    mods["django.forms"] = _modulo("django.forms", ModelForm=ModelForm, Form=Form, ValidationError=ValidationError,
                                   **widgets)
    mods["django.contrib"] = _modulo("django.contrib")
    auth_models = _modulo("django.contrib.auth.models", User=User, AnonymousUser=AnonymousUser)
    mods["django.contrib.auth.models"] = auth_models
    mods["django.contrib.auth"] = _modulo("django.contrib.auth", authenticate=authenticate, login=login,
                                          logout=logout, get_user_model=get_user_model, models=auth_models)
    mods["django.contrib.auth.forms"] = _modulo("django.contrib.auth.forms", UserCreationForm=UserCreationForm,
                                                AuthenticationForm=AuthenticationForm)
    mods["django.contrib.auth.decorators"] = _modulo("django.contrib.auth.decorators", login_required=login_required)
    mods["django.contrib.admin"] = _modulo("django.contrib.admin", site=admin_site, ModelAdmin=ModelAdmin,
                                           register=lambda *ms: (lambda cls: [admin_site.register(m, cls) for m in ms] and cls))
    mods["django.views"] = _modulo("django.views")
    mods["django.views.decorators"] = _modulo("django.views.decorators")
    mods["django.views.decorators.http"] = _modulo("django.views.decorators.http", require_POST=require_POST)
    mods["django.test"] = _modulo("django.test", Client=Client)
    return mods


_MODULOS = _criar_modulos()

for _cls, _mod in ((Model, "django.db.models"), (QuerySet, "django.db.models.query"), (Manager, "django.db.models"),
                   (User, "django.contrib.auth.models"), (HttpResponse, "django.http"),
                   (HttpResponseRedirect, "django.http"), (HttpResponseNotFound, "django.http"),
                   (Http404, "django.http"), (NoReverseMatch, "django.urls"),
                   (TemplateDoesNotExist, "django.template"), (TemplateSyntaxError, "django.template"),
                   (ModelForm, "django.forms"), (Client, "django.test")):
    _cls.__module__ = _mod


def instalar():
    reiniciar()
    sys.modules.update(_MODULOS)
