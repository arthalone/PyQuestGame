# -*- coding: utf-8 -*-
"""Ponte entre o JavaScript (Web Worker) e o motor/conteúdo em Python."""
import json

import motor
from conteudo import CAPITULOS


def _desafio_publico(d):
    return {
        "titulo": d["titulo"], "enunciado": d["enunciado"], "inicial": d["inicial"],
        "dica": d["dica"], "solucao": d["solucao"],
        "ctx": d["casos"][0]["ctx"], "ncasos": len(d["casos"]),
    }


def dados():
    caps = []
    for c in CAPITULOS:
        caps.append({
            "num": c["num"], "titulo": c["titulo"], "subtitulo": c["subtitulo"],
            "licoes": c["licoes"], "quiz": c["quiz"],
            "desafios": [_desafio_publico(d) for d in c["desafios"]],
            "chefe": _desafio_publico(c["chefe"]),
        })
    return json.dumps(caps, ensure_ascii=False)


def _desafio(cap, idx):
    c = CAPITULOS[int(cap) - 1]
    return c["chefe"] if idx == "chefe" else c["desafios"][int(idx)]


def _variaveis(ns):
    out = {}
    for k, v in motor.variaveis_usuario(ns).items():
        if callable(v) or hasattr(v, "__file__"):
            continue
        out[k] = repr(v)[:200]
        if len(out) >= 15:
            break
    return out


def executar(codigo, ctx_json="{}"):
    ctx = json.loads(ctx_json or "{}")
    saida, ns, erro = motor.executar(codigo, ctx)
    return json.dumps({
        "saida": saida,
        "erro": motor.descrever_erro(erro) if erro is not None else None,
        "vars": _variaveis(ns) if erro is None else {},
    }, ensure_ascii=False)


def verificar(cap, idx, codigo):
    ok, msg = motor.verificar(_desafio(cap, idx), codigo)
    return json.dumps({"ok": ok, "msg": msg}, ensure_ascii=False)
