# -*- coding: utf-8 -*-
"""Motor de execução e verificação do código do aluno."""
import builtins
import copy
import io
import os
import shutil
import sys
import tempfile
import warnings

import django_treino

ARQ = "<seu código>"
os.environ.setdefault("MPLBACKEND", "Agg")  # gráficos viram imagens, sem abrir janelas
warnings.filterwarnings("ignore", message=".*non-interactive.*")
warnings.filterwarnings("ignore", message=".*Matplotlib is currently using agg.*")
MAX_PASSOS = 300_000
MAX_SAIDA = 50_000


class LimiteExcedido(Exception):
    pass


DICAS_ERRO = {
    "SyntaxError": "O Python não entendeu essa linha. Confira aspas, parênteses e os dois-pontos (:) no fim de if/for/while/def/class.",
    "IndentationError": "Problema de indentação. Blocos depois de ':' precisam de 4 espaços; linhas soltas não devem ter espaços no início.",
    "TabError": "Misturou Tab e espaços. Use só espaços (a tecla Tab do editor já insere 4 espaços).",
    "NameError": "Esse nome não existe. Erro de digitação? A variável foi criada ANTES de ser usada?",
    "TypeError": "Tipos incompatíveis ou argumentos errados. Ex.: juntar texto com número usando +, ou chamar uma função com argumentos faltando.",
    "IndexError": "Índice fora da lista. Os índices começam em 0, e o último é sempre [-1].",
    "AttributeError": "Esse valor não tem esse método ou atributo. Confira o nome e, em classes, se usou self.",
    "ValueError": "Valor inválido. Ex.: int('abc'), ou remove() de um item que não está na lista.",
    "ZeroDivisionError": "Divisão por zero não existe em matemática, nem em Python!",
    "KeyError": "Essa chave não existe no dicionário. Use .get() para evitar o erro.",
    "FileNotFoundError": "Arquivo não encontrado. Confira o nome do arquivo (e se ele foi criado antes).",
    "EOFError": "O programa pediu mais respostas com input() do que o teste forneceu. Confira a condição de parada do laço.",
    "AssertionError": "Um assert falhou: o valor obtido não era o esperado.",
    "RecursionError": "A função chamou a si mesma vezes demais.",
    "DoesNotExist": "Nenhum objeto combina com essa busca. Confira o id ou use get_object_or_404().",
    "NoReverseMatch": "O Django não achou essa URL pelo nome. Confira o app_name, o name do path() e se passou os argumentos (como o id).",
    "TemplateDoesNotExist": "Template não encontrado. Confira o nome no dicionário TEMPLATES e no render().",
    "TemplateSyntaxError": "Erro de escrita no template. Confira se cada {% for %}, {% if %} e {% block %} foi fechado.",
    "FieldError": "Esse campo não existe no model. Confira o nome usado no filter() ou no order_by().",
    "IntegrityError": "O banco recusou o objeto: falta um campo obrigatório (como o topic ou o owner) ou há um valor repetido.",
    "ModuleNotFoundError": "Módulo não encontrado. Para gráficos, o app precisa do matplotlib (no PC: pip install matplotlib).",
}


# ---------------------------------------------------------------------------
# "pygame de treino": as mesmas peças do pygame usadas no Alien Invasion
# (Rect, Sprite, Group, eventos e constantes), mas sem janela nem gráficos.
# Assim o aluno pratica a LÓGICA do jogo aqui e roda o mesmo código no
# pygame de verdade no PC.
# ---------------------------------------------------------------------------

class _Rect:
    def __init__(self, *args):
        if len(args) == 1:
            args = tuple(args[0]) if not isinstance(args[0], _Rect) else (
                args[0].x, args[0].y, args[0].width, args[0].height)
        if len(args) == 2:
            (x, y), (w, h) = args
        elif len(args) == 4:
            x, y, w, h = args
        else:
            raise TypeError("Rect precisa de (x, y, largura, altura)")
        object.__setattr__(self, "_d", [int(x), int(y), int(w), int(h)])

    # leitura/escrita dos atributos de posição, como no pygame
    def __getattr__(self, nome):
        x, y, w, h = self._d
        tab = {
            "x": x, "y": y, "left": x, "top": y, "width": w, "height": h, "w": w, "h": h,
            "right": x + w, "bottom": y + h, "centerx": x + w // 2, "centery": y + h // 2,
            "center": (x + w // 2, y + h // 2), "topleft": (x, y), "topright": (x + w, y),
            "bottomleft": (x, y + h), "bottomright": (x + w, y + h),
            "midtop": (x + w // 2, y), "midbottom": (x + w // 2, y + h),
            "midleft": (x, y + h // 2), "midright": (x + w, y + h // 2), "size": (w, h),
        }
        if nome in tab:
            return tab[nome]
        raise AttributeError(f"'Rect' não tem o atributo '{nome}'")

    def __setattr__(self, nome, v):
        d = self._d
        w, h = d[2], d[3]
        if nome in ("x", "left"):
            d[0] = int(v)
        elif nome in ("y", "top"):
            d[1] = int(v)
        elif nome in ("width", "w"):
            d[2] = int(v)
        elif nome in ("height", "h"):
            d[3] = int(v)
        elif nome == "right":
            d[0] = int(v) - w
        elif nome == "bottom":
            d[1] = int(v) - h
        elif nome == "centerx":
            d[0] = int(v) - w // 2
        elif nome == "centery":
            d[1] = int(v) - h // 2
        elif nome == "size":
            d[2], d[3] = int(v[0]), int(v[1])
        elif nome in ("center", "topleft", "topright", "bottomleft", "bottomright",
                      "midtop", "midbottom", "midleft", "midright"):
            px, py = v
            hx = {"center": w // 2, "topleft": 0, "topright": w, "bottomleft": 0, "bottomright": w,
                  "midtop": w // 2, "midbottom": w // 2, "midleft": 0, "midright": w}[nome]
            hy = {"center": h // 2, "topleft": 0, "topright": 0, "bottomleft": h, "bottomright": h,
                  "midtop": 0, "midbottom": h, "midleft": h // 2, "midright": h // 2}[nome]
            d[0], d[1] = int(px) - hx, int(py) - hy
        else:
            raise AttributeError(f"'Rect' não tem o atributo '{nome}'")

    def colliderect(self, o):
        return (self.width > 0 and self.height > 0 and o.width > 0 and o.height > 0
                and self.left < o.right and o.left < self.right
                and self.top < o.bottom and o.top < self.bottom)

    def collidepoint(self, *p):
        px, py = p[0] if len(p) == 1 else p
        return self.left <= px < self.right and self.top <= py < self.bottom

    def copy(self):
        return _Rect(*self._d)

    def move(self, dx, dy):
        return _Rect(self.x + dx, self.y + dy, self.width, self.height)

    def move_ip(self, dx, dy):
        self._d[0] += int(dx)
        self._d[1] += int(dy)

    def __eq__(self, o):
        try:
            return list(self._d) == [int(v) for v in (o._d if isinstance(o, _Rect) else o)]
        except TypeError:
            return False

    def __iter__(self):
        return iter(self._d)

    def __repr__(self):
        return "<rect({}, {}, {}, {})>".format(*self._d)

    def __deepcopy__(self, memo):
        return self.copy()


class _Surface:
    def __init__(self, size=(1200, 800), *a, **k):
        self._w, self._h = int(size[0]), int(size[1])

    def get_rect(self, **k):
        r = _Rect(0, 0, self._w, self._h)
        for nome, v in k.items():
            setattr(r, nome, v)
        return r

    def get_width(self):
        return self._w

    def get_height(self):
        return self._h

    def get_size(self):
        return (self._w, self._h)

    def fill(self, *a, **k):
        pass

    def blit(self, *a, **k):
        pass


class _Sprite:
    def __init__(self, *grupos):
        self.__g = set()
        for g in grupos:
            g.add(self)

    def _grupos(self):
        try:
            return self.__g
        except AttributeError:  # o aluno esqueceu de chamar super().__init__()
            object.__setattr__(self, "_Sprite__g", set())
            return self.__g

    def update(self, *a, **k):
        pass

    def kill(self):
        for g in list(self._grupos()):
            g.remove(self)

    def alive(self):
        return bool(self._grupos())

    def groups(self):
        return list(self._grupos())


class _Group:
    def __init__(self, *sprites):
        self._s = []
        self.add(*sprites)

    def add(self, *sprites):
        for s in sprites:
            if isinstance(s, (list, tuple, _Group)):
                self.add(*s)
            elif s not in self._s:
                self._s.append(s)
                s._grupos().add(self)

    def remove(self, *sprites):
        for s in sprites:
            if s in self._s:
                self._s.remove(s)
                s._grupos().discard(self)

    def has(self, *sprites):
        return all(s in self._s for s in sprites)

    def sprites(self):
        return list(self._s)

    def copy(self):
        return _Group(*self._s)

    def empty(self):
        self.remove(*list(self._s))

    def update(self, *a, **k):
        for s in list(self._s):
            s.update(*a, **k)

    def draw(self, *a, **k):
        pass

    def __iter__(self):
        return iter(list(self._s))

    def __len__(self):
        return len(self._s)

    def __bool__(self):
        return bool(self._s)

    def __contains__(self, s):
        return s in self._s

    def __repr__(self):
        return f"<Group({len(self._s)} sprites)>"

    def __hash__(self):
        return id(self)


def _groupcollide(g1, g2, dokill1, dokill2):
    res = {}
    for a in list(g1):
        atingidos = [b for b in list(g2) if a.rect.colliderect(b.rect)]
        if atingidos:
            res[a] = atingidos
    for a, bs in res.items():
        if dokill1:
            a.kill()
        if dokill2:
            for b in bs:
                b.kill()
    return res


def _spritecollideany(sprite, grupo):
    for b in list(grupo):
        if sprite.rect.colliderect(b.rect):
            return b
    return None


class _Event:
    def __init__(self, tipo, dic=None, **attrs):
        self.type = tipo
        self.__dict__.update(dic or {})
        self.__dict__.update(attrs)

    def __repr__(self):
        extra = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items() if k != "type")
        return f"<Event({self.type}{', ' + extra if extra else ''})>"


def _criar_pygame():
    import types
    pg = types.ModuleType("pygame")
    pg.__doc__ = "pygame de treino do PyQuest (sem janela)."
    pg.__file__ = "pygame_de_treino"
    pg.Rect = _Rect
    pg.Surface = _Surface
    pg.QUIT, pg.KEYDOWN, pg.KEYUP, pg.MOUSEBUTTONDOWN = 256, 768, 769, 1025
    pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN = 1073741904, 1073741903, 1073741906, 1073741905
    pg.K_SPACE, pg.K_q, pg.K_p, pg.K_RETURN, pg.K_ESCAPE = 32, 113, 112, 13, 27
    pg.FULLSCREEN = 1
    pg.init = lambda: (6, 0)
    pg.quit = lambda: None

    sprite = types.ModuleType("pygame.sprite")
    sprite.Sprite, sprite.Group = _Sprite, _Group
    sprite.groupcollide, sprite.spritecollideany = _groupcollide, _spritecollideany
    pg.sprite = sprite

    event = types.ModuleType("pygame.event")
    event.Event = _Event
    event.get = lambda *a, **k: []
    pg.event = event

    display = types.ModuleType("pygame.display")
    display.set_mode = lambda size=(1200, 800), *a, **k: _Surface(size if size and size[0] else (1200, 800))
    display.set_caption = lambda *a, **k: None
    display.flip = lambda *a, **k: None
    pg.display = display

    image = types.ModuleType("pygame.image")
    image.load = lambda *a, **k: _Surface((60, 48))
    pg.image = image

    draw = types.ModuleType("pygame.draw")
    draw.rect = lambda *a, **k: None
    pg.draw = draw

    mouse = types.ModuleType("pygame.mouse")
    mouse.get_pos = lambda: (0, 0)
    mouse.set_visible = lambda *a: None
    pg.mouse = mouse

    class _Clock:
        def tick(self, *a):
            return 16
    tempo = types.ModuleType("pygame.time")
    tempo.Clock = _Clock
    pg.time = tempo

    class _Font:
        def __init__(self, *a, **k):
            pass

        def render(self, texto, *a, **k):
            return _Surface((len(str(texto)) * 12, 30))
    font = types.ModuleType("pygame.font")
    font.SysFont = font.Font = _Font
    pg.font = font
    return pg


for _cls, _nome, _mod in ((_Rect, "Rect", "pygame"), (_Surface, "Surface", "pygame"),
                          (_Sprite, "Sprite", "pygame.sprite"), (_Group, "Group", "pygame.sprite"),
                          (_Event, "Event", "pygame.event")):
    _cls.__name__ = _cls.__qualname__ = _nome
    _cls.__module__ = _mod

_PYGAME = _criar_pygame()


# ---------------------------------------------------------------------------
# "requests de treino": uma API de mentira, com respostas fixas e simuladas,
# no formato das APIs do GitHub e do Hacker News usadas no livro.
# Nada sai do computador. Com o requests de verdade, o mesmo código busca dados reais.
# ---------------------------------------------------------------------------

_DONOS = ["estudio-alfa", "coletivo-py", "lab-aurora", "turma-beta", "dev-ipe", "nuvem-clara",
          "casa-do-codigo-livre", "grupo-orion", "oficina-kiwi", "time-maracuja", "rede-jabuti", "ninho-dev"]
_NOMES = {
    "python": ["cobra-veloz", "pyfacil", "dados-em-foco", "robo-tarefas", "web-rapida", "mini-ia",
               "gerador-de-graficos", "testes-sem-dor", "cli-amigavel", "planilha-py", "jogo-da-cobrinha", "api-relampago"],
    "javascript": ["botao-magico", "tela-viva", "react-lite", "anima-js", "formulario-feliz", "mapa-interativo",
                   "cliente-http", "graficos-web", "editor-online", "mini-loja"],
    "rust": ["ferrugem-rapida", "servidor-seguro", "motor-2d", "parser-turbo", "cofre-de-dados", "terminal-colorido"],
}
_ESTRELAS = {"python": 98000, "javascript": 120000, "rust": 64000}


def _repos(ling):
    nomes = _NOMES.get(ling, [])
    base = _ESTRELAS.get(ling, 0)
    itens = []
    for i, nome in enumerate(nomes):
        dono = _DONOS[(i * 5 + len(ling)) % len(_DONOS)]
        estrelas = int(base * (0.83 ** i)) - (i * 137) % 1000
        itens.append({
            "id": 1000 + i, "name": nome, "full_name": f"{dono}/{nome}",
            "owner": {"login": dono}, "stargazers_count": estrelas,
            "forks_count": estrelas // 7, "language": ling.title() if ling != "javascript" else "JavaScript",
            "html_url": f"https://github.com/{dono}/{nome}",
            "description": f"Projeto de exemplo ({nome.replace('-', ' ')})",
            "created_at": f"20{14 + i % 9}-0{1 + i % 9}-1{i % 9}T12:00:00Z",
            "updated_at": "2026-10-01T08:30:00Z",
        })
    return itens


_HN = [
    (40101, "Como aprendi Python fazendo jogos", 312, 128),
    (40102, "Mostre seu projeto: um gráfico do clima da minha cidade", 254, 97),
    (40103, "Por que testes automatizados economizam tempo", 198, 143),
    (40104, "Um guia gentil para APIs web", 176, 41),
    (40105, "Pergunte: qual foi seu primeiro programa?", 150, 215),
    (40106, "Visualizando um passeio aleatório", 133, 18),
    (40107, "Dicionários em Python, explicados com café", 120, 66),
    (40108, "O que aprendi lendo código de outras pessoas", 99, 52),
    (40109, "Mostre seu projeto: placar de jogo salvo em JSON", 87, 9),
    (40110, "Classes sem medo", 64, 30),
]


class _Resposta:
    def __init__(self, status, dados, url):
        import json as _json
        self.status_code = status
        self.ok = status < 400
        self.url = url
        self._dados = dados
        self.text = _json.dumps(dados, ensure_ascii=False)
        self.headers = {"Content-Type": "application/json"}

    def json(self):
        import copy as _copy
        return _copy.deepcopy(self._dados)

    def raise_for_status(self):
        if not self.ok:
            raise _RequestsHTTPError(f"{self.status_code} Erro para a URL: {self.url}")

    def __repr__(self):
        return f"<Response [{self.status_code}]>"


class _RequestsHTTPError(Exception):
    pass


def _api_get(url, params=None, headers=None, timeout=None, **k):
    import re as _re
    from urllib.parse import unquote_plus
    url = str(url)
    if params:
        url += ("&" if "?" in url else "?") + "&".join(f"{a}={b}" for a, b in params.items())
    u = unquote_plus(url)
    if u.startswith("https://api.github.com/search/repositories"):
        m = _re.search(r"language:([A-Za-z+#]+)", u)
        ling = m.group(1).lower() if m else ""
        itens = _repos(ling)
        return _Resposta(200, {"total_count": len(itens) * 1013 if itens else 0,
                               "incomplete_results": False, "items": itens}, url)
    if u.rstrip("/") == "https://hacker-news.firebaseio.com/v0/topstories.json":
        return _Resposta(200, [h[0] for h in _HN], url)
    m = _re.fullmatch(r"https://hacker-news\.firebaseio\.com/v0/item/(\d+)\.json", u)
    if m:
        for i, titulo, pontos, coment in _HN:
            if i == int(m.group(1)):
                return _Resposta(200, {"id": i, "type": "story", "by": _DONOS[i % len(_DONOS)], "title": titulo,
                                       "score": pontos, "descendants": coment,
                                       "url": f"https://exemplo.com/artigo/{i}"}, url)
        return _Resposta(200, None, url)
    return _Resposta(404, {"message": "Not Found"}, url)


def _criar_requests():
    import types
    rq = types.ModuleType("requests")
    rq.__doc__ = "requests de treino do PyQuest (respostas simuladas, sem internet)."
    rq.__file__ = "requests_de_treino"
    rq.get = _api_get
    rq.Response = _Resposta
    rq.HTTPError = _RequestsHTTPError
    exc = types.ModuleType("requests.exceptions")
    exc.HTTPError = _RequestsHTTPError
    rq.exceptions = exc
    return rq


_REQUESTS = _criar_requests()
_Resposta.__name__ = _Resposta.__qualname__ = "Response"
_Resposta.__module__ = "requests"
_RequestsHTTPError.__name__ = _RequestsHTTPError.__qualname__ = "HTTPError"


def _instalar_pygame():
    django_treino.instalar()
    sys.modules["requests"] = _REQUESTS
    sys.modules["requests.exceptions"] = _REQUESTS.exceptions
    sys.modules["pygame"] = _PYGAME
    for sub in ("sprite", "event", "display", "image", "draw", "mouse", "time", "font"):
        sys.modules["pygame." + sub] = getattr(_PYGAME, sub)


class _Saida(io.TextIOBase):
    """Guarda duas versões da saída: a da tela (com as perguntas do input) e a limpa (só prints)."""

    def __init__(self):
        super().__init__()
        self.tela = io.StringIO()
        self.limpa = io.StringIO()

    def writable(self):
        return True

    def write(self, s):
        s = str(s)
        self.tela.write(s)
        self.limpa.write(s)
        return len(s)

    def tamanho(self):
        return self.tela.tell()


def _tracer(passos, estourou):
    def local(frame, event, arg):
        if event == "line":
            passos[0] += 1
            if passos[0] > MAX_PASSOS or estourou():
                raise LimiteExcedido()
        return local

    def glob(frame, event, arg):
        return local if frame.f_code.co_filename == ARQ else None
    return glob


def executar(codigo, ctx=None):
    """Executa o código e devolve (saida_da_tela, namespace, erro_ou_None).

    ctx pode ter:
      "__entradas__": lista de respostas para input()
      "__arquivos__": {nome: conteúdo} criados antes de rodar
    Depois de rodar, o namespace ganha:
      "__saida_limpa__": saída sem as perguntas do input()
      "__arquivos_saida__": {nome: conteúdo} dos arquivos da pasta do aluno
    """
    out = _Saida()
    ctx = copy.deepcopy(ctx or {})
    entradas = ctx.pop("__entradas__", None)
    arquivos = ctx.pop("__arquivos__", None) or {}
    env = ctx.pop("__env__", None) or {}
    fila = list(entradas) if entradas is not None else None

    def fake_input(prompt=""):
        prompt = str(prompt)
        if fila is None:
            resp = ""
        elif not fila:
            raise EOFError("o programa pediu mais entradas do que o teste forneceu")
        else:
            resp = str(fila.pop(0))
        out.tela.write(prompt + resp + "\n")
        return resp

    bins = dict(vars(builtins))
    bins["input"] = fake_input
    bins["exit"] = bins["quit"] = lambda *a: (_ for _ in ()).throw(SystemExit())
    ns = {"__name__": "__main__", "__builtins__": bins}
    ns.update(ctx)

    try:
        obj = compile(codigo, ARQ, "exec")
    except SyntaxError as e:  # inclui IndentationError
        ns["__saida_limpa__"] = ""
        ns["__arquivos_saida__"] = {}
        return "", ns, e

    pasta = tempfile.mkdtemp(prefix="pyquest_")
    for nome, conteudo in arquivos.items():
        with open(os.path.join(pasta, nome), "w", encoding="utf-8") as f:
            f.write(conteudo)
    try:
        cwd_antigo = os.getcwd()
    except OSError:
        cwd_antigo = None

    sys.modules.pop("this", None)  # para "import this" mostrar o Zen toda vez
    _instalar_pygame()
    _plt_antes = sys.modules.get("matplotlib.pyplot")
    if _plt_antes is not None:
        _plt_antes.close("all")
    passos = [0]
    antigo_out = sys.stdout
    erro = None
    env_antigo = {k: os.environ.get(k) for k in env}
    for k, v in env.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = str(v)
    sys.stdout = out
    os.chdir(pasta)
    sys.settrace(_tracer(passos, lambda: out.tamanho() > MAX_SAIDA))
    try:
        exec(obj, ns)
    except SystemExit:
        pass
    except BaseException as e:  # noqa
        erro = e
    finally:
        sys.settrace(None)
        sys.stdout = antigo_out
        for k, v in env_antigo.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        if cwd_antigo:
            try:
                os.chdir(cwd_antigo)
            except OSError:
                pass

    saidas = {}
    for raiz, _, nomes in os.walk(pasta):
        for nome in nomes:
            caminho = os.path.join(raiz, nome)
            rel = os.path.relpath(caminho, pasta).replace(os.sep, "/")
            try:
                with open(caminho, encoding="utf-8") as f:
                    saidas[rel] = f.read()
            except (OSError, UnicodeDecodeError):
                pass
    shutil.rmtree(pasta, ignore_errors=True)
    ns["__arquivos_saida__"] = saidas
    ns["__imagens__"], ns["__figuras__"] = _capturar_graficos()
    ns["__saida_limpa__"] = out.limpa.getvalue()

    saida = out.tela.getvalue()
    if len(saida) > MAX_SAIDA:
        saida = saida[:MAX_SAIDA] + "\n... (saída cortada)"
    return saida, ns, erro


MAX_GRAFICOS = 4


def _capturar_graficos():
    """Transforma as figuras abertas do matplotlib em PNGs (base64)."""
    plt = sys.modules.get("matplotlib.pyplot")
    if plt is None:
        return [], []
    import base64
    imagens, figuras = [], []
    try:
        for num in plt.get_fignums()[:MAX_GRAFICOS]:
            fig = plt.figure(num)
            figuras.append(fig)
            largura = max(fig.get_size_inches()[0], 1)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=min(100, 1000 / largura), bbox_inches="tight")
            imagens.append(base64.b64encode(buf.getvalue()).decode("ascii"))
    except Exception:  # noqa  (um gráfico com problema não derruba a execução)
        pass
    finally:
        plt.close("all")
    return imagens, figuras


def descrever_erro(e):
    """Texto amigável (pt-BR) para um erro."""
    if isinstance(e, LimiteExcedido):
        return ("Seu código executou passos demais ou imprimiu texto demais. "
                "Será que há um laço que nunca termina?")
    nome = type(e).__name__
    linha = None
    if isinstance(e, SyntaxError):
        linha = e.lineno
        detalhe = e.msg
    else:
        tb = e.__traceback__
        while tb:
            if tb.tb_frame.f_code.co_filename == ARQ:
                linha = tb.tb_lineno
            tb = tb.tb_next
        detalhe = str(e)
    cab = nome + (f" na linha {linha}" if linha else "") + (f": {detalhe}" if detalhe else "")
    dica = DICAS_ERRO.get(nome)
    if nome == "ValueError" and "HttpResponse" in str(detalhe):
        dica = "A view precisa terminar com return render(...), return redirect(...) ou return HttpResponse(...)."
    return cab + (f"\nDica: {dica}" if dica else "")


def variaveis_usuario(ns):
    return {k: v for k, v in ns.items() if not k.startswith("__")}


def _avaliar(fn, saida, ns, codigo):
    """Roda uma condição de correção com limite de passos (ela pode chamar funções do aluno)."""
    out = _Saida()
    antigo = sys.stdout
    sys.stdout = out
    sys.settrace(_tracer([0], lambda: out.tamanho() > MAX_SAIDA))
    try:
        return bool(fn(saida, ns, codigo)), None
    except LimiteExcedido:
        return False, "Ao testar seu código, ele executou passos demais. Há algum laço que nunca termina?"
    except Exception as e:  # noqa
        if e.__traceback__ and any(f.tb_frame.f_code.co_filename == ARQ
                                   or f.tb_frame.f_code.co_filename.endswith("django_treino.py")
                                   for f in _tb(e.__traceback__)):
            return False, "Ao testar seu código, aconteceu um erro:\n" + descrever_erro(e)
        return False, None
    finally:
        sys.settrace(None)
        sys.stdout = antigo


def _tb(tb):
    while tb:
        yield tb
        tb = tb.tb_next


def descrever_contexto(ctx):
    partes = []
    if "__entradas__" in ctx:
        ent = ctx["__entradas__"]
        partes.append("entradas digitadas: " + (", ".join(repr(x) for x in ent) if ent else "(nenhuma)"))
    if ctx.get("__arquivos__"):
        partes.append("arquivos: " + ", ".join(ctx["__arquivos__"]))
    if ctx.get("__env__"):
        partes.append("variáveis de ambiente: " + ", ".join(
            f"{k}={v!r}" if v is not None else f"{k} (não existe)" for k, v in ctx["__env__"].items()))
    for k, v in ctx.items():
        if not k.startswith("__"):
            partes.append(f"{k} = {v!r}")
    return "; ".join(partes)


def verificar(desafio, codigo):
    """Roda todos os casos. Devolve (ok, mensagem)."""
    casos = desafio["casos"]
    for caso in casos:
        ctx = caso["ctx"]
        saida_tela, ns, erro = executar(codigo, ctx)
        saida = ns.get("__saida_limpa__", saida_tela)
        pref = ""
        if ctx:
            pref = "Teste com " + descrever_contexto(ctx) + ":\n"
        if erro is not None:
            return False, pref + descrever_erro(erro)
        for fn, msg in caso["conds"]:
            ok, extra_erro = _avaliar(fn, saida, ns, codigo)
            if not ok:
                extra = ""
                if extra_erro:
                    extra = "\n\n" + extra_erro
                elif saida_tela.strip():
                    extra = "\n\nSua saída foi:\n" + saida_tela.strip()[:800]
                return False, pref + msg + extra
    n = len(casos)
    return True, ("Todos os testes passaram!" if n == 1 else f"Todos os {n} testes passaram!")
