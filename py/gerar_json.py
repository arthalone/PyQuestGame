# Gera conteudo.json (usado pela interface) a partir de conteudo.py.
# Rode sempre que editar conteudo.py:  python py/gerar_json.py
import os
import sys

aqui = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, aqui)
import ponte  # noqa: E402

destino = os.path.join(aqui, "..", "conteudo.json")
with open(destino, "w", encoding="utf-8") as f:
    f.write(ponte.dados())
print("conteudo.json atualizado.")
