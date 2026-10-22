# -*- coding: utf-8 -*-
"""Motor de execução e verificação do código do aluno."""
import builtins
import copy
import io
import os
import shutil
import sys
import tempfile

ARQ = "<seu código>"
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
}


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
    passos = [0]
    antigo_out = sys.stdout
    erro = None
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
    ns["__saida_limpa__"] = out.limpa.getvalue()

    saida = out.tela.getvalue()
    if len(saida) > MAX_SAIDA:
        saida = saida[:MAX_SAIDA] + "\n... (saída cortada)"
    return saida, ns, erro


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
        if e.__traceback__ and any(f.tb_frame.f_code.co_filename == ARQ for f in _tb(e.__traceback__)):
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
