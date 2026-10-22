# -*- coding: utf-8 -*-
"""Motor de execução e verificação do código do aluno."""
import builtins
import copy
import io
import sys

ARQ = "<seu código>"
MAX_PASSOS = 300_000
MAX_SAIDA = 50_000


class LimiteExcedido(Exception):
    pass


DICAS_ERRO = {
    "SyntaxError": "O Python não entendeu essa linha. Confira aspas, parênteses e os dois-pontos (:) no fim de if/for/else.",
    "IndentationError": "Problema de indentação. Blocos depois de ':' precisam de 4 espaços; linhas soltas não devem ter espaços no início.",
    "TabError": "Misturou Tab e espaços. Use só espaços (a tecla Tab do editor já insere 4 espaços).",
    "NameError": "Esse nome não existe. Erro de digitação? A variável foi criada ANTES de ser usada?",
    "TypeError": "Tipos incompatíveis. Ex.: juntar texto com número usando +. Prefira uma f-string.",
    "IndexError": "Índice fora da lista. Os índices começam em 0, e o último é sempre [-1].",
    "AttributeError": "Esse tipo de valor não tem esse método. Confira o nome (ex.: .upper(), .append()).",
    "ValueError": "Valor inválido. Ex.: remove() de um item que não está na lista.",
    "ZeroDivisionError": "Divisão por zero não existe em matemática, nem em Python!",
    "KeyError": "Essa chave não existe.",
}


def executar(codigo, ctx=None):
    """Executa o código e devolve (saida, namespace, erro_ou_None)."""
    buf = io.StringIO()

    def fake_input(prompt=""):
        buf.write(str(prompt) + "\n")
        return ""

    bins = dict(vars(builtins))
    bins["input"] = fake_input
    bins["exit"] = bins["quit"] = lambda *a: (_ for _ in ()).throw(SystemExit())
    ns = {"__name__": "__main__", "__builtins__": bins}
    if ctx:
        ns.update(copy.deepcopy(ctx))

    try:
        obj = compile(codigo, ARQ, "exec")
    except SyntaxError as e:  # inclui IndentationError
        return "", ns, e

    passos = [0]

    def local(frame, event, arg):
        if event == "line":
            passos[0] += 1
            if passos[0] > MAX_PASSOS:
                raise LimiteExcedido()
            if buf.tell() > MAX_SAIDA:
                raise LimiteExcedido()
        return local

    def glob(frame, event, arg):
        return local if frame.f_code.co_filename == ARQ else None

    sys.modules.pop("this", None)  # para "import this" mostrar o Zen toda vez
    antigo_out = sys.stdout
    erro = None
    sys.stdout = buf
    sys.settrace(glob)
    try:
        exec(obj, ns)
    except SystemExit:
        pass
    except BaseException as e:  # noqa
        erro = e
    finally:
        sys.settrace(None)
        sys.stdout = antigo_out
    saida = buf.getvalue()
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


def verificar(desafio, codigo):
    """Roda todos os casos. Devolve (ok, mensagem)."""
    casos = desafio["casos"]
    for i, caso in enumerate(casos):
        ctx = caso["ctx"]
        saida, ns, erro = executar(codigo, ctx)
        pref = ""
        if ctx:
            pref = "Teste com " + ", ".join(f"{k} = {v!r}" for k, v in ctx.items()) + ":\n"
        if erro is not None:
            return False, pref + descrever_erro(erro)
        for fn, msg in caso["conds"]:
            try:
                ok = fn(saida, ns, codigo)
            except Exception:
                ok = False
            if not ok:
                extra = ""
                if saida.strip():
                    extra = "\n\nSua saída foi:\n" + saida.strip()[:800]
                return False, pref + msg + extra
    n = len(casos)
    return True, ("Todos os testes passaram!" if n == 1 else f"Todos os {n} testes passaram!")
