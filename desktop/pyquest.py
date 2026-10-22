# -*- coding: utf-8 -*-
"""
PyQuest: aprenda Python jogando.
Baseado na sequência dos capítulos 1 a 11 do livro "Curso Intensivo de Python" (Eric Matthes).

Execute com:  python pyquest.py
"""
import datetime
import json
import keyword
import os
import random
import re
import sys
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox

import motor
from conteudo import CAPITULOS

VERSAO = "1.0"

# ---------------------------------------------------------------------------
# Visual
# ---------------------------------------------------------------------------
C = {
    "bg": "#1e1f29", "painel": "#262836", "painel2": "#2f3242", "borda": "#44475a",
    "texto": "#f8f8f2", "mudo": "#8b93b8", "verde": "#50fa7b", "amarelo": "#f1fa8c",
    "roxo": "#bd93f9", "rosa": "#ff79c6", "vermelho": "#ff5555", "laranja": "#ffb86c",
    "ciano": "#8be9fd", "editor": "#181920", "escuro": "#14151b",
}


def clarear(hexcor, f=0.18):
    hexcor = hexcor.lstrip("#")
    r, g, b = (int(hexcor[i:i + 2], 16) for i in (0, 2, 4))
    r, g, b = (int(v + (255 - v) * f) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


# ---------------------------------------------------------------------------
# Regras do jogo
# ---------------------------------------------------------------------------
NIVEIS = [
    (0, "Ovo de Píton"), (100, "Filhote de Cobra"), (250, "Serpente Curiosa"),
    (450, "Aprendiz de Código"), (700, "Domador de Strings"), (1000, "Mestre das Listas"),
    (1300, "Cavaleiro do For"), (1650, "Guardião do If"), (2000, "Senhor dos Dicionários"),
    (2400, "Domador de Laços"), (2850, "Arquiteto de Funções"), (3350, "Mestre das Classes"),
    (3900, "Pythonista"), (4500, "Lenda do Terminal"),
]

XP_LICAO = 10
XP_QUIZ_ACERTO = 5
XP_QUIZ_PASSOU = 20
XP_DESAFIO = 30
XP_CHEFE = 100
XP_SOLUCAO = 5
QUIZ_APROVACAO = 0.7
TEMPO_RELAMPAGO = 60

CONQUISTAS = [
    ("ola_mundo", "Olá, Mundo!", "Execute seu primeiro código."),
    ("primeiro_desafio", "Primeira Vitória", "Resolva seu primeiro desafio."),
    ("leitor", "Rato de Biblioteca", "Conclua 10 lições."),
    ("quiz_perfeito", "Gabaritou!", "Acerte 100% de um quiz."),
    ("combo5", "Em Chamas", "Faça um combo de 5 acertos seguidos num quiz."),
    ("autodidata", "Autodidata", "Resolva 5 desafios sem usar dicas."),
    ("persistente", "Persistente", "Vença um desafio depois de 3 ou mais tentativas."),
    ("cacador", "Caçador de Chefões", "Derrote seu primeiro chefão."),
    ("lenda", "Lenda da Jornada", "Derrote todos os chefões."),
    ("streak3", "Constância", "Estude 3 dias seguidos."),
    ("streak7", "Hábito de Ferro", "Estude 7 dias seguidos."),
    ("raio", "Raio Veloz", "Faça 8 ou mais acertos no Desafio Relâmpago."),
    ("cientista", "Cientista Maluco", "Execute 15 experimentos no Laboratório."),
    ("mil_xp", "Mil Pontos", "Alcance 1000 XP."),
]
CONQ_DICT = {c[0]: c for c in CONQUISTAS}


def nivel_de(xp):
    idx = 0
    for i, (minimo, _) in enumerate(NIVEIS):
        if xp >= minimo:
            idx = i
    ini = NIVEIS[idx][0]
    prox = NIVEIS[idx + 1][0] if idx + 1 < len(NIVEIS) else None
    return idx + 1, NIVEIS[idx][1], ini, prox


# ---------------------------------------------------------------------------
# Progresso salvo em disco
# ---------------------------------------------------------------------------
def pasta_dados():
    base = os.environ.get("APPDATA") or os.path.expanduser("~")
    p = os.path.join(base, "PyQuest")
    os.makedirs(p, exist_ok=True)
    return p


class Progresso:
    PADRAO = {
        "xp": 0, "feitos": [], "quiz_melhor": {}, "conquistas": [], "streak": 0,
        "ultimo_dia": "", "codigo": {}, "tentativas": {}, "dicas": [], "solucoes": [],
        "sem_dica": 0, "lab_execucoes": 0, "execucoes": 0, "recorde_relampago": 0,
    }

    def __init__(self):
        self.arq = os.path.join(pasta_dados(), "progresso.json")
        self.d = json.loads(json.dumps(self.PADRAO))
        try:
            with open(self.arq, encoding="utf-8") as f:
                self.d.update(json.load(f))
        except (OSError, ValueError):
            pass

    def __getattr__(self, k):
        if k in ("d", "arq"):
            raise AttributeError(k)
        return self.d[k]

    def salvar(self):
        tmp = self.arq + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(self.d, f, ensure_ascii=False, indent=1)
            os.replace(tmp, self.arq)
        except OSError:
            pass

    def feito(self, i):
        return i in self.d["feitos"]

    def marcar(self, i):
        if i not in self.d["feitos"]:
            self.d["feitos"].append(i)

    def zerar(self):
        self.d = json.loads(json.dumps(self.PADRAO))
        self.salvar()


# ---------------------------------------------------------------------------
# Realce de sintaxe
# ---------------------------------------------------------------------------
RE_KW = re.compile(r"\b(" + "|".join(keyword.kwlist) + r")\b")
RE_BI = re.compile(r"\b(print|len|range|list|str|int|float|sorted|sum|min|max|tuple|input|type|bool|"
                   r"dict|set|abs|round|enumerate|zip)\b")
RE_NUM = re.compile(r"\b\d[\d_]*(?:\.\d+)?\b")
RE_STR_COM = re.compile(r"(?P<com>#[^\n]*)|(?P<str>[fFrRbB]{0,2}(?:\"\"\"[\s\S]*?(?:\"\"\"|$)|'''[\s\S]*?(?:'''|$)|"
                        r"\"(?:\\.|[^\"\\\n])*\"?|'(?:\\.|[^'\\\n])*'?))")


def realcar(t):
    txt = t.get("1.0", "end-1c")
    for tag in ("kw", "bi", "num", "str", "com"):
        t.tag_remove(tag, "1.0", "end")
    for tag, pat in (("kw", RE_KW), ("bi", RE_BI), ("num", RE_NUM)):
        for m in pat.finditer(txt):
            t.tag_add(tag, f"1.0+{m.start()}c", f"1.0+{m.end()}c")
    for m in RE_STR_COM.finditer(txt):
        tag = "com" if m.group("com") else "str"
        t.tag_add(tag, f"1.0+{m.start()}c", f"1.0+{m.end()}c")


def contar_linhas_visiveis(t):
    try:
        r = t.count("1.0", "end", "displaylines")
        if isinstance(r, tuple):
            r = r[0]
        return int(r or 1)
    except tk.TclError:
        return int(t.index("end-1c").split(".")[0])


# ---------------------------------------------------------------------------
# Widgets
# ---------------------------------------------------------------------------
class Botao(tk.Label):
    def __init__(self, master, texto, cmd, cor=None, fg=None, fonte=None, padx=16, pady=7, ativo=True):
        cor = cor or C["verde"]
        super().__init__(master, text=texto, bg=cor, fg=fg or C["escuro"], font=fonte,
                         padx=padx, pady=pady, cursor="hand2")
        self.cor, self.fg_ok, self.cmd = cor, fg or C["escuro"], cmd
        self.ativo = True
        self.bind("<Enter>", lambda e: self._hover(True))
        self.bind("<Leave>", lambda e: self._hover(False))
        self.bind("<Button-1>", self._click)
        self.set_ativo(ativo)

    def _hover(self, on):
        try:
            if self.ativo:
                self.config(bg=clarear(self.cor) if on else self.cor)
        except tk.TclError:
            pass

    def _click(self, e=None):
        if self.ativo and self.cmd:
            self.cmd()

    def set_ativo(self, a):
        self.ativo = a
        self.config(bg=self.cor if a else C["borda"], fg=self.fg_ok if a else C["mudo"],
                    cursor="hand2" if a else "arrow")


class Rolavel(tk.Frame):
    """Frame com rolagem vertical."""

    def __init__(self, master, bg):
        super().__init__(master, bg=bg)
        self.canvas = tk.Canvas(self, bg=bg, highlightthickness=0, bd=0)
        self.sb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.interno = tk.Frame(self.canvas, bg=bg)
        self.win = self.canvas.create_window((0, 0), window=self.interno, anchor="nw")
        self.interno.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfigure(self.win, width=e.width))
        self.canvas.configure(yscrollcommand=self.sb.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.sb.pack(side="right", fill="y")
        self.bind_all("<MouseWheel>", self._roda)
        self.bind_all("<Button-4>", self._roda)
        self.bind_all("<Button-5>", self._roda)

    def _roda(self, e):
        if isinstance(e.widget, tk.Text) and str(e.widget.cget("state")) == "normal":
            return
        try:
            if e.num == 4:
                d = -1
            elif e.num == 5:
                d = 1
            else:
                d = -1 if e.delta > 0 else 1
            self.canvas.yview_scroll(d * 2, "units")
        except tk.TclError:
            pass


def barra(master, frac, largura=200, altura=10, cor=None, bg=None):
    cv = tk.Canvas(master, width=largura, height=altura, bg=bg or C["painel"], highlightthickness=0, bd=0)
    cv.create_rectangle(0, 0, largura, altura, fill=C["borda"], width=0)
    w = max(0, min(1, frac)) * largura
    if w > 0:
        cv.create_rectangle(0, 0, w, altura, fill=cor or C["verde"], width=0)
    return cv


class Editor(tk.Frame):
    """Editor de código com numeração de linhas, realce e auto-indentação."""

    def __init__(self, master, app, codigo="", altura=12, somente_leitura=False, ao_mudar=None):
        super().__init__(master, bg=C["editor"], highlightthickness=1, highlightbackground=C["borda"])
        self.app, self.ro, self.ao_mudar = app, somente_leitura, ao_mudar
        f = app.F["code"]
        self.nums = tk.Text(self, width=3, height=1, padx=8, pady=8, bg=C["editor"], fg="#5b6078", font=f,
                            relief="flat", bd=0, highlightthickness=0, state="disabled", takefocus=0,
                            cursor="arrow")
        self.t = tk.Text(self, bg=C["editor"], fg=C["texto"], insertbackground=C["verde"], font=f,
                         undo=True, wrap="none", height=altura, relief="flat", bd=0, padx=8, pady=8,
                         highlightthickness=0, selectbackground=C["borda"], insertwidth=2)
        self.sb = tk.Scrollbar(self, orient="vertical", command=self._yview)
        self.t.configure(yscrollcommand=self._on_scroll)
        self.nums.pack(side="left", fill="y")
        self.t.pack(side="left", fill="both", expand=True)
        if not somente_leitura:
            self.sb.pack(side="right", fill="y")
        self.t.tag_configure("kw", foreground=C["rosa"])
        self.t.tag_configure("bi", foreground=C["ciano"])
        self.t.tag_configure("num", foreground=C["roxo"])
        self.t.tag_configure("str", foreground=C["amarelo"])
        self.t.tag_configure("com", foreground="#6c7393")
        self.t.bind("<Tab>", self._tab)
        self.t.bind("<Return>", self._enter)
        self.t.bind("<BackSpace>", self._backspace)
        self.t.bind("<KeyRelease>", self._mudou)
        self.set(codigo)

    def _yview(self, *a):
        self.t.yview(*a)
        self.nums.yview(*a)

    def _on_scroll(self, a, b):
        self.sb.set(a, b)
        self.nums.yview_moveto(a)

    def _tab(self, e):
        self.t.insert("insert", "    ")
        return "break"

    def _enter(self, e):
        linha = self.t.get("insert linestart", "insert")
        ind = re.match(r"[ \t]*", linha).group()
        if linha.rstrip().endswith(":"):
            ind += "    "
        self.t.insert("insert", "\n" + ind)
        self.t.see("insert")
        self._mudou()
        return "break"

    def _backspace(self, e):
        if self.t.tag_ranges("sel"):
            return None
        antes = self.t.get("insert linestart", "insert")
        if antes and antes.strip() == "" and len(antes) % 4 == 0:
            self.t.delete("insert-4c", "insert")
            return "break"
        return None

    def _mudou(self, e=None):
        realcar(self.t)
        self._numerar()
        if self.ao_mudar:
            self.ao_mudar(self.get())

    def _numerar(self):
        n = int(self.t.index("end-1c").split(".")[0])
        self.nums.configure(state="normal")
        self.nums.delete("1.0", "end")
        self.nums.insert("1.0", "\n".join(str(i) for i in range(1, n + 1)))
        self.nums.configure(state="disabled", width=max(2, len(str(n))))
        self.nums.yview_moveto(self.t.yview()[0])

    def get(self):
        return self.t.get("1.0", "end-1c")

    def set(self, codigo):
        self.t.configure(state="normal")
        self.t.delete("1.0", "end")
        self.t.insert("1.0", codigo)
        self.t.edit_reset()
        realcar(self.t)
        self._numerar()
        if self.ro:
            n = int(self.t.index("end-1c").split(".")[0])
            self.t.configure(state="disabled", height=n)


class Saida(tk.Frame):
    def __init__(self, master, app, altura=8):
        super().__init__(master, bg=C["escuro"], highlightthickness=1, highlightbackground=C["borda"])
        cab = tk.Frame(self, bg=C["escuro"])
        cab.pack(fill="x")
        tk.Label(cab, text="SAÍDA", font=app.F["mini"], fg=C["mudo"], bg=C["escuro"], padx=10, pady=4).pack(side="left")
        self.t = tk.Text(self, bg=C["escuro"], fg=C["texto"], font=app.F["code_p"], height=altura, relief="flat",
                         bd=0, padx=10, pady=4, wrap="word", highlightthickness=0, state="disabled")
        sb = tk.Scrollbar(self, command=self.t.yview)
        self.t.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.t.pack(fill="both", expand=True)
        self.t.tag_configure("erro", foreground=C["vermelho"])
        self.t.tag_configure("ok", foreground=C["verde"])
        self.t.tag_configure("info", foreground=C["mudo"])
        self.t.tag_configure("aviso", foreground=C["laranja"])

    def limpar(self):
        self.t.configure(state="normal")
        self.t.delete("1.0", "end")
        self.t.configure(state="disabled")

    def escrever(self, texto, tag=None):
        self.t.configure(state="normal")
        self.t.insert("end", texto, tag)
        self.t.configure(state="disabled")
        self.t.see("end")


# ---------------------------------------------------------------------------
# Aplicativo
# ---------------------------------------------------------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PyQuest: Python Gamificado")
        self.geometry("1220x780")
        self.minsize(1020, 660)
        self.configure(bg=C["bg"])
        self.p = Progresso()
        self._fontes()
        self._afters, self._binds = [], []
        self._fila_toast, self._toast_on = [], False

        self.sidebar = tk.Frame(self, bg=C["painel"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        self.main = tk.Frame(self, bg=C["bg"])
        self.main.pack(side="left", fill="both", expand=True)

        self.protocol("WM_DELETE_WINDOW", self._fechar)
        self.construir_sidebar()
        self.ir(self.tela_mapa)
        self.after(700, self.bonus_diario)

    # ---------------- infraestrutura ----------------
    def _fontes(self):
        fams = set(tkfont.families(self))
        ui = next((f for f in ("Segoe UI", "Inter", "Helvetica Neue", "DejaVu Sans") if f in fams), "TkDefaultFont")
        mono = next((f for f in ("Cascadia Mono", "Consolas", "Menlo", "DejaVu Sans Mono") if f in fams), "TkFixedFont")
        self.F = {
            "h1": (ui, 22, "bold"), "h2": (ui, 16, "bold"), "h3": (ui, 12, "bold"),
            "n": (ui, 11), "nb": (ui, 11, "bold"), "p": (ui, 10), "mini": (ui, 9, "bold"),
            "big": (ui, 44, "bold"), "code": (mono, 12), "code_p": (mono, 11), "logo": (ui, 24, "bold"),
            "btn": (ui, 10, "bold"),
        }

    def _fechar(self):
        self.p.salvar()
        self.destroy()

    def depois(self, ms, fn):
        a = self.after(ms, fn)
        self._afters.append(a)
        return a

    def atalho(self, seq, fn):
        self.bind(seq, fn)
        self._binds.append(seq)

    def ir(self, tela, *args):
        for a in self._afters:
            try:
                self.after_cancel(a)
            except tk.TclError:
                pass
        self._afters.clear()
        for s in self._binds:
            self.unbind(s)
        self._binds.clear()
        for ev in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.unbind_all(ev)
        for w in self.main.winfo_children():
            w.destroy()
        self.p.salvar()
        tela(*args)

    def lbl(self, master, texto, fonte="n", fg=None, bg=None, wrap=0, **kw):
        return tk.Label(master, text=texto, font=self.F[fonte], fg=fg or C["texto"], bg=bg or master.cget("bg"),
                        wraplength=wrap, justify="left", anchor="w", **kw)

    def botao(self, master, texto, cmd, cor=None, fg=None, ativo=True, padx=16, pady=7):
        return Botao(master, texto, cmd, cor=cor, fg=fg, fonte=self.F["btn"], ativo=ativo, padx=padx, pady=pady)

    def voltar(self, master, texto, cmd):
        b = tk.Label(master, text="←  " + texto, font=self.F["nb"], fg=C["mudo"], bg=master.cget("bg"), cursor="hand2")
        b.bind("<Button-1>", lambda e: cmd())
        b.bind("<Enter>", lambda e: b.config(fg=C["texto"]))
        b.bind("<Leave>", lambda e: b.config(fg=C["mudo"]))
        return b

    # ---------------- toasts ----------------
    def toast(self, texto, cor=None):
        self._fila_toast.append((texto, cor or C["amarelo"]))
        if not self._toast_on:
            self._prox_toast()

    def _prox_toast(self):
        if not self._fila_toast:
            self._toast_on = False
            return
        self._toast_on = True
        texto, cor = self._fila_toast.pop(0)
        fr = tk.Frame(self, bg=cor, padx=2, pady=2)
        tk.Label(fr, text=texto, font=self.F["nb"], bg=C["painel2"], fg=cor, padx=18, pady=10).pack()
        fr.place(relx=1.0, x=-24, y=22, anchor="ne")
        fr.lift()

        def fim():
            fr.destroy()
            self._prox_toast()
        self.after(2300, fim)

    # ---------------- XP / conquistas ----------------
    def ganhar_xp(self, qtd, motivo=""):
        if qtd <= 0:
            return
        antes = nivel_de(self.p.xp)[0]
        self.p.d["xp"] += qtd
        self.toast(f"+{qtd} XP   {motivo}".strip())
        n, titulo, _, _ = nivel_de(self.p.xp)
        if n > antes:
            self.toast(f"SUBIU DE NÍVEL!  Nível {n}: {titulo}", C["roxo"])
        self.checar_conquistas()
        self.p.salvar()
        self.construir_sidebar()

    def conquistar(self, cid):
        if cid in self.p.conquistas:
            return
        self.p.d["conquistas"].append(cid)
        self.toast(f"★ Conquista: {CONQ_DICT[cid][1]}", C["rosa"])
        self.p.salvar()

    def checar_conquistas(self):
        feitos = self.p.feitos
        if sum(1 for f in feitos if "-l" in f) >= 10:
            self.conquistar("leitor")
        if any(f.endswith("-chefe") for f in feitos):
            self.conquistar("cacador")
        if all(f"c{c['num']}-chefe" in feitos for c in CAPITULOS):
            self.conquistar("lenda")
        if any("-d" in f for f in feitos):
            self.conquistar("primeiro_desafio")
        if self.p.sem_dica >= 5:
            self.conquistar("autodidata")
        if self.p.streak >= 3:
            self.conquistar("streak3")
        if self.p.streak >= 7:
            self.conquistar("streak7")
        if self.p.xp >= 1000:
            self.conquistar("mil_xp")

    def bonus_diario(self):
        hoje = datetime.date.today()
        ult = self.p.ultimo_dia
        if ult == hoje.isoformat():
            return
        ontem = (hoje - datetime.timedelta(days=1)).isoformat()
        self.p.d["streak"] = self.p.streak + 1 if ult == ontem else 1
        self.p.d["ultimo_dia"] = hoje.isoformat()
        bonus = 10 + 2 * min(self.p.streak - 1, 10)
        dias = self.p.streak
        self.ganhar_xp(bonus, f"Bônus diário ({dias} dia{'s' if dias > 1 else ''} seguido{'s' if dias > 1 else ''})")

    # ---------------- estrutura dos capítulos ----------------
    @staticmethod
    def cap(n):
        return CAPITULOS[n - 1]

    def ids_cap(self, n):
        c = self.cap(n)
        ids = [f"c{n}-l{i}" for i in range(len(c["licoes"]))]
        ids.append(f"c{n}-quiz")
        ids += [f"c{n}-d{i}" for i in range(len(c["desafios"]))]
        ids.append(f"c{n}-chefe")
        return ids

    def frac_cap(self, n):
        ids = self.ids_cap(n)
        return sum(self.p.feito(i) for i in ids) / len(ids)

    def cap_liberado(self, n):
        return n == 1 or self.p.feito(f"c{n - 1}-chefe")

    def chefe_liberado(self, n):
        c = self.cap(n)
        feitos = sum(self.p.feito(f"c{n}-d{i}") for i in range(len(c["desafios"])))
        return self.p.feito(f"c{n}-quiz") and feitos >= min(3, len(c["desafios"]))

    def proximo_passo(self):
        for c in CAPITULOS:
            n = c["num"]
            if not self.cap_liberado(n):
                break
            for i, l in enumerate(c["licoes"]):
                if not self.p.feito(f"c{n}-l{i}"):
                    return f"Cap. {n} · Lição: {l['titulo']}", lambda n=n, i=i: self.ir(self.tela_licao, n, i)
            if not self.p.feito(f"c{n}-quiz"):
                return f"Cap. {n} · Quiz do capítulo", lambda n=n: self.ir(self.tela_quiz, n)
            for i, d in enumerate(c["desafios"]):
                if not self.p.feito(f"c{n}-d{i}"):
                    return f"Cap. {n} · Desafio: {d['titulo']}", lambda n=n, i=i: self.ir(self.tela_desafio, n, i)
            if not self.p.feito(f"c{n}-chefe"):
                return f"Cap. {n} · CHEFÃO: {c['chefe']['titulo']}", lambda n=n: self.ir(self.tela_desafio, n, "chefe")
        return None, None

    # ---------------- barra lateral ----------------
    def construir_sidebar(self):
        sb = self.sidebar
        for w in sb.winfo_children():
            w.destroy()
        topo = tk.Frame(sb, bg=C["painel"], padx=20, pady=20)
        topo.pack(fill="x")
        logo = tk.Frame(topo, bg=C["painel"])
        logo.pack(anchor="w")
        tk.Label(logo, text="Py", font=self.F["logo"], fg=C["verde"], bg=C["painel"]).pack(side="left")
        tk.Label(logo, text="Quest", font=self.F["logo"], fg=C["texto"], bg=C["painel"]).pack(side="left")
        self.lbl(topo, "Python gamificado", "p", C["mudo"]).pack(anchor="w")

        perfil = tk.Frame(sb, bg=C["painel2"], padx=16, pady=14)
        perfil.pack(fill="x", padx=14)
        n, titulo, ini, prox = nivel_de(self.p.xp)
        linha = tk.Frame(perfil, bg=C["painel2"])
        linha.pack(fill="x")
        tk.Label(linha, text=f" {n} ", font=self.F["h2"], bg=C["roxo"], fg=C["escuro"]).pack(side="left")
        info = tk.Frame(linha, bg=C["painel2"], padx=10)
        info.pack(side="left", fill="x")
        self.lbl(info, "NÍVEL", "mini", C["mudo"]).pack(anchor="w")
        self.lbl(info, titulo, "nb").pack(anchor="w")
        frac = 1 if prox is None else (self.p.xp - ini) / (prox - ini)
        barra(perfil, frac, 196, 10, C["verde"], C["painel2"]).pack(anchor="w", pady=(12, 4))
        txt = f"{self.p.xp} XP" + (f"  ·  faltam {prox - self.p.xp} para o nível {n + 1}" if prox else "  ·  nível máximo!")
        self.lbl(perfil, txt, "p", C["mudo"], wrap=220).pack(anchor="w")
        st = tk.Frame(perfil, bg=C["painel2"])
        st.pack(fill="x", pady=(10, 0))
        self.lbl(st, f"✹ {self.p.streak} dia(s) seguidos", "p", C["laranja"]).pack(side="left")
        self.lbl(st, f"★ {len(self.p.conquistas)}/{len(CONQUISTAS)}", "p", C["rosa"]).pack(side="right")

        nav = tk.Frame(sb, bg=C["painel"], pady=16)
        nav.pack(fill="x")
        for texto, tela in (("☰   Mapa da Jornada", self.tela_mapa), ("⚡   Desafio Relâmpago", self.tela_relampago),
                            ("✎   Laboratório", self.tela_lab), ("★   Conquistas", self.tela_conquistas)):
            b = tk.Label(nav, text=texto, font=self.F["n"], fg=C["texto"], bg=C["painel"], anchor="w",
                         padx=26, pady=10, cursor="hand2")
            b.pack(fill="x")
            b.bind("<Button-1>", lambda e, t=tela: self.ir(t))
            b.bind("<Enter>", lambda e, b=b: b.config(bg=C["painel2"]))
            b.bind("<Leave>", lambda e, b=b: b.config(bg=C["painel"]))

        rod = tk.Frame(sb, bg=C["painel"], padx=20, pady=16)
        rod.pack(side="bottom", fill="x")
        self.lbl(rod, "Baseado nos capítulos 1–11 do livro Curso Intensivo de Python (Eric Matthes)", "p", C["mudo"],
                 wrap=220).pack(anchor="w")

    # ---------------- tela: mapa ----------------
    def tela_mapa(self):
        r = Rolavel(self.main, C["bg"])
        r.pack(fill="both", expand=True)
        f = tk.Frame(r.interno, bg=C["bg"], padx=36, pady=28)
        f.pack(fill="both", expand=True)
        self.lbl(f, "Mapa da Jornada", "h1").pack(anchor="w")
        self.lbl(f, "Leia as lições, passe no quiz, resolva desafios e derrote o chefão de cada capítulo "
                    "para liberar o próximo.", "n", C["mudo"], wrap=760).pack(anchor="w", pady=(4, 18))

        if self.p.xp <= 30 and not self.p.feitos:
            bv = tk.Frame(f, bg=C["painel2"], padx=20, pady=16, highlightthickness=1, highlightbackground=C["roxo"])
            bv.pack(fill="x", pady=(0, 16))
            self.lbl(bv, "Bem-vindo(a), aventureiro(a)!", "h3", C["roxo"]).pack(anchor="w")
            self.lbl(bv, "Cada atividade dá XP. Junte XP para subir de nível, mantenha sua sequência de dias "
                         "estudando e colecione conquistas. Os desafios rodam Python de verdade e corrigem "
                         "seu código na hora. Dica: Ctrl+Enter executa o código no editor.",
                     "n", wrap=760).pack(anchor="w", pady=(6, 0))

        texto, cmd = self.proximo_passo()
        cont = tk.Frame(f, bg=C["painel"], padx=20, pady=16)
        cont.pack(fill="x", pady=(0, 22))
        if texto:
            esq = tk.Frame(cont, bg=C["painel"])
            esq.pack(side="left", fill="x", expand=True)
            self.lbl(esq, "PRÓXIMO PASSO", "mini", C["verde"]).pack(anchor="w")
            self.lbl(esq, texto, "h3").pack(anchor="w", pady=(2, 0))
            self.botao(cont, "Continuar  ▶", cmd).pack(side="right")
        else:
            self.lbl(cont, "Você completou a jornada! Use o Relâmpago e o Laboratório para continuar treinando.",
                     "h3", C["verde"], wrap=760).pack(anchor="w")

        for c in CAPITULOS:
            self._card_cap(f, c)

    def _card_cap(self, master, c):
        n = c["num"]
        lib = self.cap_liberado(n)
        frac = self.frac_cap(n)
        completo = self.p.feito(f"c{n}-chefe")
        cor = C["verde"] if completo else (C["roxo"] if lib else C["borda"])
        card = tk.Frame(master, bg=C["painel"], highlightthickness=0)
        card.pack(fill="x", pady=6)
        tk.Frame(card, bg=cor, width=6).pack(side="left", fill="y")
        corpo = tk.Frame(card, bg=C["painel"], padx=18, pady=14)
        corpo.pack(side="left", fill="x", expand=True)
        tk.Label(corpo, text=f"{n}", font=self.F["h1"], width=2, bg=C["painel"],
                 fg=cor if lib else C["mudo"]).pack(side="left", padx=(0, 14))
        meio = tk.Frame(corpo, bg=C["painel"])
        meio.pack(side="left", fill="x", expand=True)
        self.lbl(meio, c["titulo"], "h2", C["texto"] if lib else C["mudo"]).pack(anchor="w")
        self.lbl(meio, c["subtitulo"], "p", C["mudo"]).pack(anchor="w")
        lin = tk.Frame(meio, bg=C["painel"])
        lin.pack(anchor="w", pady=(8, 0))
        barra(lin, frac, 260, 8, C["verde"] if completo else C["roxo"]).pack(side="left")
        estado = "★ Concluído" if completo else (f"{int(frac * 100)}%" if lib else "⛔ Derrote o chefão anterior")
        self.lbl(lin, "   " + estado, "p", C["verde"] if completo else C["mudo"]).pack(side="left")
        if lib:
            self.botao(corpo, "Entrar", lambda: self.ir(self.tela_capitulo, n),
                       cor=C["verde"] if not completo else C["painel2"],
                       fg=C["escuro"] if not completo else C["texto"]).pack(side="right")

    # ---------------- tela: capítulo ----------------
    def tela_capitulo(self, n):
        c = self.cap(n)
        r = Rolavel(self.main, C["bg"])
        r.pack(fill="both", expand=True)
        f = tk.Frame(r.interno, bg=C["bg"], padx=36, pady=24)
        f.pack(fill="both", expand=True)
        self.voltar(f, "Mapa", lambda: self.ir(self.tela_mapa)).pack(anchor="w")
        self.lbl(f, f"CAPÍTULO {n}", "mini", C["roxo"]).pack(anchor="w", pady=(16, 0))
        self.lbl(f, c["titulo"], "h1").pack(anchor="w")
        self.lbl(f, c["subtitulo"], "n", C["mudo"]).pack(anchor="w")
        lin = tk.Frame(f, bg=C["bg"])
        lin.pack(anchor="w", pady=(10, 10))
        barra(lin, self.frac_cap(n), 360, 10, C["verde"], C["bg"]).pack(side="left")
        self.lbl(lin, f"   {int(self.frac_cap(n) * 100)}% do capítulo", "p", C["mudo"]).pack(side="left")

        self._secao(f, "LIÇÕES")
        for i, l in enumerate(c["licoes"]):
            self._linha_item(f, f"c{n}-l{i}", f"Lição {i + 1}: {l['titulo']}", f"+{XP_LICAO} XP",
                             "Rever" if self.p.feito(f"c{n}-l{i}") else "Ler",
                             lambda i=i: self.ir(self.tela_licao, n, i))

        self._secao(f, "QUIZ")
        qid = f"c{n}-quiz"
        melhor = self.p.quiz_melhor.get(qid, 0)
        tot = len(c["quiz"])
        self._linha_item(f, qid, f"Quiz do capítulo ({tot} perguntas)  ·  melhor: {melhor}/{tot}",
                         f"até +{tot * XP_QUIZ_ACERTO + XP_QUIZ_PASSOU} XP", "Jogar",
                         lambda: self.ir(self.tela_quiz, n))

        self._secao(f, "DESAFIOS DE CÓDIGO")
        for i, d in enumerate(c["desafios"]):
            self._linha_item(f, f"c{n}-d{i}", d["titulo"], f"+{XP_DESAFIO} XP",
                             "Refazer" if self.p.feito(f"c{n}-d{i}") else "Resolver",
                             lambda i=i: self.ir(self.tela_desafio, n, i))

        self._secao(f, "CHEFÃO")
        lib = self.chefe_liberado(n)
        self._linha_item(f, f"c{n}-chefe", "♛  " + c["chefe"]["titulo"], f"+{XP_CHEFE} XP",
                         "Enfrentar" if lib else "Bloqueado", lambda: self.ir(self.tela_desafio, n, "chefe"),
                         ativo=lib, destaque=True,
                         obs=None if lib else "Passe no quiz e resolva pelo menos 3 desafios para liberar.")

    def _secao(self, master, texto):
        self.lbl(master, texto, "mini", C["mudo"]).pack(anchor="w", pady=(18, 6))

    def _linha_item(self, master, iid, titulo, xp, txt_btn, cmd, ativo=True, destaque=False, obs=None):
        feito = self.p.feito(iid)
        row = tk.Frame(master, bg=C["painel"], padx=16, pady=10,
                       highlightthickness=1 if destaque else 0, highlightbackground=C["laranja"])
        row.pack(fill="x", pady=3)
        icone, cor = ("✔", C["verde"]) if feito else (("○", C["mudo"]) if ativo else ("⛔", C["mudo"]))
        tk.Label(row, text=icone, font=self.F["h3"], fg=cor, bg=C["painel"], width=2).pack(side="left")
        meio = tk.Frame(row, bg=C["painel"])
        meio.pack(side="left", fill="x", expand=True, padx=8)
        self.lbl(meio, titulo, "nb", C["texto"] if ativo else C["mudo"]).pack(anchor="w")
        if obs:
            self.lbl(meio, obs, "p", C["mudo"]).pack(anchor="w")
        self.botao(row, txt_btn, cmd, cor=C["painel2"] if feito else (C["laranja"] if destaque else C["verde"]),
                   fg=C["texto"] if feito else None, ativo=ativo, padx=14, pady=5).pack(side="right")
        self.lbl(row, xp + "   ", "p", C["amarelo"] if not feito else C["mudo"]).pack(side="right")

    # ---------------- tela: lição ----------------
    def _texto_rico(self, master, paragrafos, largura=820):
        t = tk.Text(master, bg=master.cget("bg"), fg=C["texto"], font=self.F["n"], wrap="word", relief="flat",
                    bd=0, highlightthickness=0, padx=0, pady=0, cursor="arrow", spacing1=2, spacing3=8, height=1)
        t.tag_configure("h", font=self.F["h3"], foreground=C["roxo"], spacing1=10)
        t.tag_configure("code", font=self.F["code_p"], foreground=C["amarelo"], background=C["editor"])
        t.tag_configure("b", font=self.F["nb"], foreground=C["verde"])
        t.tag_configure("i", foreground=C["ciano"])
        for p in paragrafos:
            if p.startswith("## "):
                t.insert("end", p[3:] + "\n", "h")
                continue
            for parte in re.split(r"(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)", p):
                if not parte:
                    continue
                if parte.startswith("`"):
                    t.insert("end", " " + parte[1:-1] + " ", "code")
                elif parte.startswith("**"):
                    t.insert("end", parte[2:-2], "b")
                elif parte.startswith("*") and parte.endswith("*") and len(parte) > 2:
                    t.insert("end", parte[1:-1], "i")
                else:
                    t.insert("end", parte)
            t.insert("end", "\n")
        t.configure(state="disabled")

        def ajustar(e=None):
            t.configure(height=contar_linhas_visiveis(t))
        t.bind("<Configure>", ajustar)
        self.after(50, ajustar)
        return t

    def tela_licao(self, n, i):
        c = self.cap(n)
        l = c["licoes"][i]
        lid = f"c{n}-l{i}"
        r = Rolavel(self.main, C["bg"])
        r.pack(fill="both", expand=True)
        f = tk.Frame(r.interno, bg=C["bg"], padx=40, pady=24)
        f.pack(fill="both", expand=True)
        self.voltar(f, f"Capítulo {n}", lambda: self.ir(self.tela_capitulo, n)).pack(anchor="w")
        self.lbl(f, f"LIÇÃO {i + 1} DE {len(c['licoes'])}  ·  {c['titulo'].upper()}", "mini", C["roxo"]).pack(anchor="w", pady=(16, 2))
        self.lbl(f, l["titulo"], "h1").pack(anchor="w", pady=(0, 14))
        self._texto_rico(f, l["texto"]).pack(fill="x")

        self.lbl(f, "EXEMPLO", "mini", C["mudo"]).pack(anchor="w", pady=(16, 6))
        ed = Editor(f, self, l["exemplo"], somente_leitura=True)
        ed.pack(fill="x")
        bar = tk.Frame(f, bg=C["bg"])
        bar.pack(fill="x", pady=(8, 0))
        out_holder = tk.Frame(f, bg=C["bg"])
        out_holder.pack(fill="x")
        out = Saida(out_holder, self, altura=6)

        def rodar():
            out.limpar()
            s, ns, e = motor.executar(l["exemplo"], l.get("ctx"))
            out.escrever(s)
            if e:
                out.escrever(motor.descrever_erro(e) + "\n", "erro")
            out.pack(fill="x", pady=(8, 0))
            self.p.d["execucoes"] += 1
            self.conquistar("ola_mundo")

        self.botao(bar, "▶  Executar exemplo", rodar, cor=C["ciano"]).pack(side="left")
        self.botao(bar, "✎  Abrir no Laboratório", lambda: self._abrir_lab(l["exemplo"]), cor=C["painel2"],
                   fg=C["texto"]).pack(side="left", padx=8)

        nav = tk.Frame(f, bg=C["bg"])
        nav.pack(fill="x", pady=(26, 10))
        ult = i + 1 >= len(c["licoes"])

        def concluir():
            if not self.p.feito(lid):
                self.p.marcar(lid)
                self.ganhar_xp(XP_LICAO, "Lição concluída")
            if ult:
                self.ir(self.tela_capitulo, n)
            else:
                self.ir(self.tela_licao, n, i + 1)

        txt = ("Concluir e voltar ao capítulo" if ult else "Concluir e ir para a próxima  →") \
            + ("" if self.p.feito(lid) else f"   (+{XP_LICAO} XP)")
        self.botao(nav, txt, concluir).pack(side="right")
        if i > 0:
            self.botao(nav, "←  Lição anterior", lambda: self.ir(self.tela_licao, n, i - 1),
                       cor=C["painel2"], fg=C["texto"]).pack(side="left")

    def _abrir_lab(self, codigo):
        self.p.d["codigo"]["lab"] = codigo
        self.ir(self.tela_lab)

    # ---------------- tela: quiz ----------------
    def _embaralhar(self, perguntas):
        out = []
        for q in perguntas:
            ops = list(enumerate(q["opcoes"]))
            random.shuffle(ops)
            nq = dict(q)
            nq["opcoes"] = [o for _, o in ops]
            nq["correta"] = [k for k, _ in ops].index(q["correta"])
            out.append(nq)
        random.shuffle(out)
        return out

    def tela_quiz(self, n):
        c = self.cap(n)
        est = {"qs": self._embaralhar(c["quiz"]), "i": 0, "acertos": 0, "combo": 0, "max_combo": 0}
        moldura = tk.Frame(self.main, bg=C["bg"], padx=40, pady=24)
        moldura.pack(fill="both", expand=True)
        self.voltar(moldura, f"Capítulo {n}", lambda: self.ir(self.tela_capitulo, n)).pack(anchor="w")
        area = tk.Frame(moldura, bg=C["bg"])
        area.pack(fill="both", expand=True, pady=(14, 0))

        def render():
            for w in area.winfo_children():
                w.destroy()
            if est["i"] >= len(est["qs"]):
                return resultado()
            q = est["qs"][est["i"]]
            top = tk.Frame(area, bg=C["bg"])
            top.pack(fill="x")
            self.lbl(top, f"QUIZ · CAPÍTULO {n}   ·   PERGUNTA {est['i'] + 1}/{len(est['qs'])}", "mini", C["roxo"]).pack(side="left")
            if est["combo"] >= 2:
                self.lbl(top, f"✹ COMBO x{est['combo']}", "nb", C["laranja"]).pack(side="right")
            barra(area, est["i"] / len(est["qs"]), 600, 6, C["roxo"], C["bg"]).pack(anchor="w", pady=(8, 18))
            self.lbl(area, q["pergunta"], "h2", wrap=820).pack(anchor="w")
            if q.get("codigo"):
                Editor(area, self, q["codigo"], somente_leitura=True).pack(fill="x", pady=(12, 0))
            ops = tk.Frame(area, bg=C["bg"])
            ops.pack(fill="x", pady=(16, 0))
            botoes = []
            fb = tk.Frame(area, bg=C["bg"])

            def responder(k):
                if est.get("respondida"):
                    return
                est["respondida"] = True
                certo = k == q["correta"]
                for j, b in enumerate(botoes):
                    b.unbind("<Button-1>")
                    b.unbind("<Enter>")
                    b.unbind("<Leave>")
                    b.config(cursor="arrow")
                    if j == q["correta"]:
                        b.config(bg="#1f4d33", fg=C["verde"])
                    elif j == k:
                        b.config(bg="#5a2430", fg=C["vermelho"])
                if certo:
                    est["acertos"] += 1
                    est["combo"] += 1
                    est["max_combo"] = max(est["max_combo"], est["combo"])
                    msg, cor = ("Correto!" + (f"  Combo x{est['combo']}!" if est["combo"] >= 2 else "")), C["verde"]
                else:
                    est["combo"] = 0
                    msg, cor = "Não foi dessa vez.", C["vermelho"]
                fb.pack(fill="x", pady=(16, 0))
                self.lbl(fb, msg, "h3", cor).pack(anchor="w")
                self.lbl(fb, q["explicacao"], "n", C["mudo"], wrap=820).pack(anchor="w", pady=(4, 10))
                prox = "Ver resultado" if est["i"] + 1 >= len(est["qs"]) else "Próxima  →  (Enter)"
                self.botao(fb, prox, avancar).pack(anchor="w")

            def avancar(e=None):
                if not est.get("respondida"):
                    return
                est["respondida"] = False
                est["i"] += 1
                render()

            for k, op in enumerate(q["opcoes"]):
                b = tk.Label(ops, text=f"  {k + 1}   {op}", font=self.F["n"], bg=C["painel"], fg=C["texto"],
                             anchor="w", padx=14, pady=10, cursor="hand2", wraplength=800, justify="left")
                b.pack(fill="x", pady=3)
                b.bind("<Button-1>", lambda e, k=k: responder(k))
                b.bind("<Enter>", lambda e, b=b: b.config(bg=C["painel2"]))
                b.bind("<Leave>", lambda e, b=b: b.config(bg=C["painel"]))
                botoes.append(b)
            for k in range(len(q["opcoes"])):
                self.atalho(str(k + 1), lambda e, k=k: responder(k))
            self.atalho("<Return>", avancar)

        def resultado():
            tot = len(est["qs"])
            a = est["acertos"]
            qid = f"c{n}-quiz"
            passou = a / tot >= QUIZ_APROVACAO
            ganho = 0
            melhor = self.p.quiz_melhor.get(qid, 0)
            if a > melhor:
                ganho += (a - melhor) * XP_QUIZ_ACERTO
                self.p.d["quiz_melhor"][qid] = a
            if passou and not self.p.feito(qid):
                self.p.marcar(qid)
                ganho += XP_QUIZ_PASSOU
            estrelas = 3 if a == tot else (2 if a / tot >= 0.85 else (1 if passou else 0))
            box = tk.Frame(area, bg=C["painel"], padx=40, pady=30)
            box.pack(pady=30)
            tk.Label(box, text="★" * estrelas + "☆" * (3 - estrelas), font=self.F["big"], fg=C["amarelo"],
                     bg=C["painel"]).pack()
            tk.Label(box, text=f"{a} / {tot}", font=self.F["h1"], fg=C["texto"], bg=C["painel"]).pack()
            msg = ("Perfeito! Você dominou este capítulo." if a == tot else
                   "Aprovado! Os desafios de código estão liberados." if passou else
                   f"Você precisa de {int(QUIZ_APROVACAO * 100)}% para passar. Revise as lições e tente de novo!")
            tk.Label(box, text=msg, font=self.F["n"], fg=C["verde"] if passou else C["laranja"], bg=C["painel"],
                     wraplength=460).pack(pady=(8, 4))
            tk.Label(box, text=f"Maior combo: {est['max_combo']}", font=self.F["p"], fg=C["mudo"], bg=C["painel"]).pack()
            if ganho == 0 and a <= melhor:
                tk.Label(box, text="(XP só é ganho quando você supera seu recorde)", font=self.F["p"],
                         fg=C["mudo"], bg=C["painel"]).pack()
            bt = tk.Frame(box, bg=C["painel"])
            bt.pack(pady=(18, 0))
            self.botao(bt, "Jogar de novo", lambda: self.ir(self.tela_quiz, n), cor=C["painel2"], fg=C["texto"]).pack(side="left", padx=4)
            self.botao(bt, "Voltar ao capítulo", lambda: self.ir(self.tela_capitulo, n)).pack(side="left", padx=4)
            if a == tot:
                self.conquistar("quiz_perfeito")
            if est["max_combo"] >= 5:
                self.conquistar("combo5")
            if ganho:
                self.ganhar_xp(ganho, "Quiz")
            else:
                self.p.salvar()

        render()

    # ---------------- tela: desafio ----------------
    def tela_desafio(self, n, i):
        c = self.cap(n)
        chefe = i == "chefe"
        d = c["chefe"] if chefe else c["desafios"][i]
        did = f"c{n}-chefe" if chefe else f"c{n}-d{i}"
        if chefe and not self.chefe_liberado(n):
            return self.ir(self.tela_capitulo, n)
        ctx = d["casos"][0]["ctx"]
        tent = self.p.tentativas.get(did, 0)

        raiz = tk.Frame(self.main, bg=C["bg"], padx=28, pady=18)
        raiz.pack(fill="both", expand=True)
        cab = tk.Frame(raiz, bg=C["bg"])
        cab.pack(fill="x")
        self.voltar(cab, f"Capítulo {n}", lambda: self.ir(self.tela_capitulo, n)).pack(side="left")
        if self.p.feito(did):
            self.lbl(cab, "✔ Concluído", "nb", C["verde"]).pack(side="right")
        tipo = "CHEFÃO" if chefe else f"DESAFIO {i + 1} DE {len(c['desafios'])}"
        self.lbl(raiz, f"{tipo}  ·  CAPÍTULO {n}", "mini", C["laranja"] if chefe else C["roxo"]).pack(anchor="w", pady=(12, 0))
        self.lbl(raiz, ("♛  " if chefe else "") + d["titulo"], "h1").pack(anchor="w", pady=(0, 10))

        corpo = tk.Frame(raiz, bg=C["bg"])
        corpo.pack(fill="both", expand=True)
        corpo.columnconfigure(0, weight=2, uniform="c")
        corpo.columnconfigure(1, weight=3, uniform="c")
        corpo.rowconfigure(0, weight=1)

        # coluna esquerda: enunciado
        esq = tk.Frame(corpo, bg=C["painel"], padx=18, pady=16)
        esq.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        base_xp = XP_CHEFE if chefe else XP_DESAFIO
        self.lbl(esq, "MISSÃO", "mini", C["mudo"]).pack(anchor="w")
        enun = tk.Text(esq, bg=C["painel"], fg=C["texto"], font=self.F["n"], wrap="word", relief="flat", bd=0,
                       highlightthickness=0, height=10, cursor="arrow", spacing3=4)
        enun.insert("1.0", d["enunciado"])
        enun.configure(state="disabled")
        enun.pack(fill="both", expand=True, pady=(6, 8))
        if ctx:
            self.lbl(esq, "DADOS DO TESTE (usados no Executar)", "mini", C["mudo"]).pack(anchor="w")
            self.lbl(esq, motor.descrever_contexto(ctx).replace("; ", "\n"), "code_p", C["ciano"],
                     wrap=360).pack(anchor="w", pady=(2, 4))
            if len(d["casos"]) > 1:
                self.lbl(esq, f"O Verificar testa {len(d['casos'])} situações diferentes.", "p", C["mudo"]).pack(anchor="w")
        recompensa = self.lbl(esq, "", "nb", C["amarelo"])
        recompensa.pack(anchor="w", pady=(10, 0))
        dica_box = tk.Frame(esq, bg=C["painel"])
        dica_box.pack(fill="x")

        def atualizar_recompensa():
            if self.p.feito(did):
                recompensa.config(text="Recompensa já recebida. Treine à vontade!", fg=C["mudo"])
            elif did in self.p.solucoes:
                recompensa.config(text=f"Recompensa: +{XP_SOLUCAO} XP (solução vista)", fg=C["laranja"])
            elif did in self.p.dicas:
                recompensa.config(text=f"Recompensa: +{base_xp // 2} XP (dica usada)", fg=C["amarelo"])
            else:
                recompensa.config(text=f"Recompensa: +{base_xp} XP", fg=C["amarelo"])
        atualizar_recompensa()

        def mostrar_dica():
            for w in dica_box.winfo_children():
                w.destroy()
            fr = tk.Frame(dica_box, bg=C["painel2"], padx=12, pady=10)
            fr.pack(fill="x", pady=(10, 0))
            self.lbl(fr, "DICA", "mini", C["amarelo"]).pack(anchor="w")
            self.lbl(fr, d["dica"], "p", wrap=360).pack(anchor="w")

        if did in self.p.dicas:
            mostrar_dica()

        # coluna direita: editor + saída
        dir_ = tk.Frame(corpo, bg=C["bg"])
        dir_.grid(row=0, column=1, sticky="nsew")
        codigo_ini = self.p.codigo.get(did, d["inicial"])

        def guardar(txt):
            self.p.d["codigo"][did] = txt
        ed = Editor(dir_, self, codigo_ini, altura=14, ao_mudar=guardar)
        ed.pack(fill="both", expand=True)
        bar = tk.Frame(dir_, bg=C["bg"])
        bar.pack(fill="x", pady=8)
        out = Saida(dir_, self, altura=9)
        out.pack(fill="both")

        def executar(e=None):
            out.limpar()
            s, ns, err = motor.executar(ed.get(), ctx)
            self.p.d["execucoes"] += 1
            if s:
                out.escrever(s)
            if err:
                out.escrever(("\n" if s and not s.endswith("\n") else "") + motor.descrever_erro(err) + "\n", "erro")
            elif not s:
                out.escrever("(o programa rodou, mas não mostrou nada)\n", "info")
            else:
                self.conquistar("ola_mundo")
            return "break"

        def verificar():
            out.limpar()
            ok, msg = motor.verificar(d, ed.get())
            if not ok:
                self.p.d["tentativas"][did] = self.p.tentativas.get(did, 0) + 1
                t = self.p.tentativas[did]
                out.escrever("✘ Ainda não. ", "erro")
                out.escrever(msg + "\n", "erro")
                if t >= 3 and did not in self.p.solucoes and not self.p.feito(did):
                    out.escrever(f"\n{t} tentativas. Se quiser, o botão 'Ver solução' já está liberado.\n", "info")
                b_sol.set_ativo(t >= 3 or self.p.feito(did))
                self.p.salvar()
                return
            out.escrever("✔ " + msg + "\n", "ok")
            if not self.p.feito(did):
                if did in self.p.solucoes:
                    ganho = XP_SOLUCAO
                elif did in self.p.dicas:
                    ganho = base_xp // 2
                else:
                    ganho = base_xp
                    self.p.d["sem_dica"] += 1
                if self.p.tentativas.get(did, 0) >= 3:
                    self.conquistar("persistente")
                self.p.marcar(did)
                self.ganhar_xp(ganho, "Chefão derrotado!" if chefe else "Desafio concluído")
                if chefe and n < len(CAPITULOS):
                    self.toast(f"Capítulo {n + 1} desbloqueado: {self.cap(n + 1)['titulo']}", C["verde"])
            vitoria()

        def vitoria():
            win = tk.Frame(dir_, bg=C["painel"], padx=16, pady=12, highlightthickness=2,
                           highlightbackground=C["verde"])
            win.place(relx=0.5, rely=0.35, anchor="center")
            tk.Label(win, text="♛ CHEFÃO DERROTADO!" if chefe else "✔ DESAFIO CONCLUÍDO!", font=self.F["h2"],
                     fg=C["verde"], bg=C["painel"]).pack(padx=20, pady=(6, 10))
            bt = tk.Frame(win, bg=C["painel"])
            bt.pack()
            self.botao(bt, "Continuar no editor", win.destroy, cor=C["painel2"], fg=C["texto"]).pack(side="left", padx=4)
            if chefe:
                if n < len(CAPITULOS):
                    self.botao(bt, f"Ir para o Capítulo {n + 1}  →", lambda: self.ir(self.tela_capitulo, n + 1)).pack(side="left", padx=4)
                else:
                    self.botao(bt, "Ver conquistas  →", lambda: self.ir(self.tela_conquistas)).pack(side="left", padx=4)
            elif i + 1 < len(c["desafios"]):
                self.botao(bt, "Próximo desafio  →", lambda: self.ir(self.tela_desafio, n, i + 1)).pack(side="left", padx=4)
            else:
                self.botao(bt, "Voltar ao capítulo  →", lambda: self.ir(self.tela_capitulo, n)).pack(side="left", padx=4)

        def pedir_dica():
            if did not in self.p.dicas:
                if not self.p.feito(did) and not messagebox.askyesno(
                        "Usar dica?", "Usar a dica reduz a recompensa deste desafio pela metade. Continuar?"):
                    return
                self.p.d["dicas"].append(did)
                self.p.salvar()
            mostrar_dica()
            atualizar_recompensa()

        def ver_solucao():
            if did not in self.p.solucoes and not self.p.feito(did):
                if not messagebox.askyesno("Ver solução?", f"Ver a solução reduz a recompensa para {XP_SOLUCAO} XP. "
                                                         "Você ainda vai precisar verificar o código. Continuar?"):
                    return
                self.p.d["solucoes"].append(did)
                self.p.salvar()
            out.limpar()
            out.escrever("Uma solução possível:\n\n", "info")
            out.escrever(d["solucao"] + "\n", "ok")
            out.escrever("\nEntenda cada linha, digite (ou adapte) no editor e clique em Verificar.\n", "info")
            atualizar_recompensa()

        def reiniciar():
            if messagebox.askyesno("Recomeçar?", "Apagar seu código e voltar ao código inicial?"):
                ed.set(d["inicial"])
                guardar(d["inicial"])

        self.botao(bar, "▶  Executar", executar, cor=C["ciano"]).pack(side="left")
        self.botao(bar, "✔  Verificar", verificar).pack(side="left", padx=8)
        self.botao(bar, "Dica", pedir_dica, cor=C["amarelo"]).pack(side="left")
        b_sol = self.botao(bar, "Ver solução", ver_solucao, cor=C["laranja"],
                           ativo=tent >= 3 or self.p.feito(did) or did in self.p.solucoes)
        b_sol.pack(side="left", padx=8)
        self.botao(bar, "↺", reiniciar, cor=C["painel2"], fg=C["texto"], padx=10).pack(side="right")
        self.lbl(bar, "Ctrl+Enter executa  ", "p", C["mudo"]).pack(side="right")
        self.atalho("<Control-Return>", executar)
        out.escrever("Escreva seu código, clique em Executar para testar e em Verificar para validar.\n", "info")
        ed.t.focus_set()
        ed.t.mark_set("insert", "end")

    # ---------------- tela: relâmpago ----------------
    def tela_relampago(self):
        f = tk.Frame(self.main, bg=C["bg"], padx=40, pady=28)
        f.pack(fill="both", expand=True)
        self.lbl(f, "⚡ Desafio Relâmpago", "h1").pack(anchor="w")
        self.lbl(f, f"{TEMPO_RELAMPAGO} segundos para responder o máximo de perguntas dos capítulos que você já "
                    "liberou. Cada erro custa 3 segundos. +2 XP por acerto (máx. 20 XP por partida).",
                 "n", C["mudo"], wrap=780).pack(anchor="w", pady=(4, 20))
        pool = []
        for c in CAPITULOS:
            if self.cap_liberado(c["num"]):
                pool += c["quiz"]
        area = tk.Frame(f, bg=C["bg"])
        area.pack(fill="both", expand=True)
        box = tk.Frame(area, bg=C["painel"], padx=40, pady=30)
        box.pack(pady=20)
        tk.Label(box, text="⚡", font=self.F["big"], fg=C["amarelo"], bg=C["painel"]).pack()
        tk.Label(box, text=f"Recorde: {self.p.recorde_relampago} acertos", font=self.F["h3"], fg=C["texto"],
                 bg=C["painel"]).pack(pady=(4, 2))
        tk.Label(box, text=f"{len(pool)} perguntas disponíveis", font=self.F["p"], fg=C["mudo"], bg=C["painel"]).pack()
        self.botao(box, "Começar!", lambda: self._jogo_relampago(area, pool)).pack(pady=(18, 0))

    def _jogo_relampago(self, area, pool):
        est = {"fila": self._embaralhar(pool), "acertos": 0, "erros": 0, "tempo": TEMPO_RELAMPAGO, "fim": False}

        def tick():
            if est["fim"]:
                return
            est["tempo"] -= 1
            atualizar_tempo()
            if est["tempo"] <= 0:
                return terminar()
            self.depois(1000, tick)

        def atualizar_tempo():
            try:
                cor = C["vermelho"] if est["tempo"] <= 10 else C["amarelo"]
                lbl_t.config(text=f"⏱ {max(0, est['tempo'])}s", fg=cor)
                lbl_p.config(text=f"✔ {est['acertos']}   ✘ {est['erros']}")
            except tk.TclError:
                pass

        def proxima():
            for w in qa.winfo_children():
                w.destroy()
            if not est["fila"]:
                est["fila"] = self._embaralhar(pool)
            q = est["fila"].pop()
            self.lbl(qa, q["pergunta"], "h3", wrap=780).pack(anchor="w")
            if q.get("codigo"):
                Editor(qa, self, q["codigo"], somente_leitura=True).pack(fill="x", pady=(8, 0))
            for k, op in enumerate(q["opcoes"]):
                b = tk.Label(qa, text=f"  {k + 1}   {op}", font=self.F["n"], bg=C["painel"], fg=C["texto"],
                             anchor="w", padx=14, pady=8, cursor="hand2")
                b.pack(fill="x", pady=3)
                b.bind("<Button-1>", lambda e, k=k: responder(q, k))
            for k in range(4):
                self.atalho(str(k + 1), lambda e, k=k: responder(q, k) if k < len(q["opcoes"]) else None)

        def responder(q, k):
            if est["fim"]:
                return
            if k == q["correta"]:
                est["acertos"] += 1
                flash(C["verde"])
            else:
                est["erros"] += 1
                est["tempo"] -= 3
                flash(C["vermelho"])
            atualizar_tempo()
            if est["tempo"] <= 0:
                return terminar()
            proxima()

        def flash(cor):
            topo.config(bg=cor)
            self.depois(180, lambda: topo.winfo_exists() and topo.config(bg=C["bg"]))

        def terminar():
            if est["fim"]:
                return
            est["fim"] = True
            for w in area.winfo_children():
                w.destroy()
            a = est["acertos"]
            novo = a > self.p.recorde_relampago
            if novo:
                self.p.d["recorde_relampago"] = a
            box = tk.Frame(area, bg=C["painel"], padx=40, pady=30)
            box.pack(pady=20)
            tk.Label(box, text="Tempo esgotado!", font=self.F["h2"], fg=C["texto"], bg=C["painel"]).pack()
            tk.Label(box, text=str(a), font=self.F["big"], fg=C["amarelo"], bg=C["painel"]).pack()
            tk.Label(box, text=f"acertos  ·  {est['erros']} erros", font=self.F["n"], fg=C["mudo"], bg=C["painel"]).pack()
            if novo and a > 0:
                tk.Label(box, text="★ NOVO RECORDE! ★", font=self.F["h3"], fg=C["rosa"], bg=C["painel"]).pack(pady=(8, 0))
            self.botao(box, "Jogar de novo", lambda: self.ir(self.tela_relampago)).pack(pady=(16, 0))
            if a >= 8:
                self.conquistar("raio")
            self.ganhar_xp(min(20, a * 2), "Relâmpago")
            self.p.salvar()

        for w in area.winfo_children():
            w.destroy()
        topo = tk.Frame(area, bg=C["bg"], pady=4)
        topo.pack(fill="x")
        inner = tk.Frame(topo, bg=C["painel"], padx=16, pady=10)
        inner.pack(fill="x", padx=3, pady=3)
        lbl_t = tk.Label(inner, text="", font=self.F["h2"], bg=C["painel"], fg=C["amarelo"])
        lbl_t.pack(side="left")
        lbl_p = tk.Label(inner, text="", font=self.F["h3"], bg=C["painel"], fg=C["texto"])
        lbl_p.pack(side="right")
        qa = tk.Frame(area, bg=C["bg"], pady=16)
        qa.pack(fill="both", expand=True)
        atualizar_tempo()
        proxima()
        self.depois(1000, tick)

    # ---------------- tela: laboratório ----------------
    def tela_lab(self):
        f = tk.Frame(self.main, bg=C["bg"], padx=28, pady=22)
        f.pack(fill="both", expand=True)
        self.lbl(f, "✎ Laboratório", "h1").pack(anchor="w")
        self.lbl(f, "Espaço livre para experimentar. Nada aqui vale nota: teste ideias, quebre coisas e aprenda!",
                 "n", C["mudo"]).pack(anchor="w", pady=(2, 12))
        padrao = "# Experimente à vontade!\nlinguagens = ['python', 'c', 'rust']\nfor l in linguagens:\n    print(l.title())\n"

        def guardar(txt):
            self.p.d["codigo"]["lab"] = txt
        ed = Editor(f, self, self.p.codigo.get("lab", padrao), altura=16, ao_mudar=guardar)
        ed.pack(fill="both", expand=True)
        bar = tk.Frame(f, bg=C["bg"])
        bar.pack(fill="x", pady=8)
        out = Saida(f, self, altura=10)
        out.pack(fill="both")

        def executar(e=None):
            out.limpar()
            s, ns, err = motor.executar(ed.get())
            out.escrever(s)
            if err:
                out.escrever(("\n" if s and not s.endswith("\n") else "") + motor.descrever_erro(err) + "\n", "erro")
            else:
                vs = motor.variaveis_usuario(ns)
                vs = {k: v for k, v in vs.items() if not callable(v) and not hasattr(v, "__file__")}
                if vs:
                    out.escrever("\n── variáveis ──\n", "info")
                    for k, v in list(vs.items())[:15]:
                        out.escrever(f"{k} = {v!r}"[:200] + "\n", "info")
                self.conquistar("ola_mundo")
            self.p.d["lab_execucoes"] += 1
            self.p.d["execucoes"] += 1
            if self.p.lab_execucoes >= 15:
                self.conquistar("cientista")
            return "break"

        self.botao(bar, "▶  Executar", executar, cor=C["ciano"]).pack(side="left")
        self.botao(bar, "Limpar saída", out.limpar, cor=C["painel2"], fg=C["texto"]).pack(side="left", padx=8)
        self.lbl(bar, "Ctrl+Enter executa", "p", C["mudo"]).pack(side="right")
        self.atalho("<Control-Return>", executar)
        ed.t.focus_set()

    # ---------------- tela: conquistas ----------------
    def tela_conquistas(self):
        r = Rolavel(self.main, C["bg"])
        r.pack(fill="both", expand=True)
        f = tk.Frame(r.interno, bg=C["bg"], padx=36, pady=28)
        f.pack(fill="both", expand=True)
        self.lbl(f, "★ Conquistas e estatísticas", "h1").pack(anchor="w")

        stats = tk.Frame(f, bg=C["bg"])
        stats.pack(fill="x", pady=(16, 8))
        feitos = self.p.feitos
        n, titulo, _, _ = nivel_de(self.p.xp)
        dados = [
            ("XP total", str(self.p.xp), C["amarelo"]),
            ("Nível", f"{n}", C["roxo"]),
            ("Lições", str(sum(1 for x in feitos if "-l" in x)), C["ciano"]),
            ("Desafios", str(sum(1 for x in feitos if "-d" in x)), C["verde"]),
            ("Chefões", f"{sum(1 for x in feitos if x.endswith('-chefe'))}/{len(CAPITULOS)}", C["laranja"]),
            ("Recorde ⚡", str(self.p.recorde_relampago), C["rosa"]),
            ("Sequência", f"{self.p.streak} d", C["laranja"]),
        ]
        for k, (rot, val, cor) in enumerate(dados):
            box = tk.Frame(stats, bg=C["painel"], padx=14, pady=10)
            box.grid(row=0, column=k, padx=(0, 8), sticky="nsew")
            stats.columnconfigure(k, weight=1)
            tk.Label(box, text=val, font=self.F["h2"], fg=cor, bg=C["painel"]).pack(anchor="w")
            tk.Label(box, text=rot, font=self.F["p"], fg=C["mudo"], bg=C["painel"]).pack(anchor="w")

        self.lbl(f, "MEDALHAS", "mini", C["mudo"]).pack(anchor="w", pady=(18, 8))
        grade = tk.Frame(f, bg=C["bg"])
        grade.pack(fill="x")
        for k, (cid, nome, desc) in enumerate(CONQUISTAS):
            tem = cid in self.p.conquistas
            box = tk.Frame(grade, bg=C["painel"] if tem else C["painel2"], padx=14, pady=12,
                           highlightthickness=1, highlightbackground=C["rosa"] if tem else C["painel2"])
            box.grid(row=k // 2, column=k % 2, sticky="nsew", padx=(0, 8), pady=4)
            grade.columnconfigure(k % 2, weight=1)
            tk.Label(box, text="★" if tem else "☆", font=self.F["h1"], fg=C["rosa"] if tem else C["borda"],
                     bg=box.cget("bg")).pack(side="left", padx=(0, 12))
            tx = tk.Frame(box, bg=box.cget("bg"))
            tx.pack(side="left", fill="x")
            tk.Label(tx, text=nome, font=self.F["nb"], fg=C["texto"] if tem else C["mudo"], bg=box.cget("bg")).pack(anchor="w")
            tk.Label(tx, text=desc, font=self.F["p"], fg=C["mudo"], bg=box.cget("bg")).pack(anchor="w")

        rod = tk.Frame(f, bg=C["bg"])
        rod.pack(fill="x", pady=(30, 0))
        self.lbl(rod, f"Progresso salvo em: {self.p.arq}", "p", C["mudo"]).pack(side="left")

        def zerar():
            if messagebox.askyesno("Zerar progresso", "Isso apaga TODO o seu XP, conquistas e códigos. Tem certeza?"):
                self.p.zerar()
                self.construir_sidebar()
                self.ir(self.tela_mapa)
        self.botao(rod, "Zerar progresso", zerar, cor=C["vermelho"]).pack(side="right")


def main():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass
    App().mainloop()


if __name__ == "__main__":
    main()
