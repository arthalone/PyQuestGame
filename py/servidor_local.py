# Servidor local para testar o PyQuest: python py/servidor_local.py
import functools
import http.server
import mimetypes
import os
import webbrowser

mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("text/css", ".css")

PASTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PORTA = 8000
Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=PASTA)
print(f"PyQuest em http://localhost:{PORTA}  (Ctrl+C ou feche a janela para parar)")
webbrowser.open(f"http://localhost:{PORTA}")
http.server.ThreadingHTTPServer(("127.0.0.1", PORTA), Handler).serve_forever()
