# -*- coding: utf-8 -*-
"""
Conteúdo do PyQuest: lições, quizzes e desafios dos capítulos 1 a 11,
seguindo a sequência de temas do livro "Curso Intensivo de Python" (Eric Matthes).
Os textos e exercícios são originais, criados para este app.
"""
import re
import unicodedata


# ---------------------------------------------------------------------------
# Ferramentas de verificação
# Cada condição é uma tupla (funcao(saida, ns, codigo) -> bool, mensagem_de_falha)
# ---------------------------------------------------------------------------

def _sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")


def normalizar(s, flex=False):
    linhas = [l.rstrip() for l in s.strip().splitlines()]
    t = "\n".join(linhas)
    if flex:
        t = _sem_acento(t).lower()
        t = re.sub(r"[ \t]+", " ", t)
    return t


def linhas(s):
    return [l for l in s.strip().splitlines() if l.strip()]


def saida(esperado, flex=False):
    def f(out, ns, code):
        return normalizar(out, flex) == normalizar(esperado, flex)
    return (f, "A saída não ficou igual à esperada. O esperado era:\n" + esperado)


def min_linhas(n):
    return (lambda out, ns, code: len(linhas(out)) >= n,
            f"Seu programa precisa mostrar pelo menos {n} linhas (não vazias).")


def n_linhas(n):
    return (lambda out, ns, code: len(linhas(out)) == n,
            f"Seu programa precisa mostrar exatamente {n} linhas (não vazias).")


def var_existe(nome, tipo=None):
    def f(out, ns, code):
        if nome not in ns:
            return False
        return tipo is None or isinstance(ns[nome], tipo)
    tipo_txt = f" do tipo {tipo.__name__}" if tipo else ""
    return (f, f"Crie uma variável chamada `{nome}`{tipo_txt}.")


def var_igual(nome, valor):
    return (lambda out, ns, code: nome in ns and ns[nome] == valor,
            f"A variável `{nome}` deveria terminar valendo: {valor!r}")


def tem(trecho, msg=None):
    return (lambda out, ns, code: trecho in code,
            msg or f"Seu código precisa usar `{trecho}`.")


def nao_tem(trecho, msg=None):
    return (lambda out, ns, code: trecho not in code,
            msg or f"Tente resolver sem escrever `{trecho}` diretamente.")


def regra(fn, msg):
    return (fn, msg)


def caso(conds, ctx=None):
    return {"ctx": ctx or {}, "conds": conds}


# ---------------------------------------------------------------------------
# CAPÍTULO 1
# ---------------------------------------------------------------------------

CAP1 = {
    "num": 1,
    "titulo": "Primeiros Passos",
    "subtitulo": "Seu primeiro programa e a função print()",
    "licoes": [
        {
            "titulo": "Como o Python roda seu código",
            "texto": [
                "Um programa em Python é só um arquivo de texto com a extensão `.py`. "
                "Quem lê esse arquivo e executa as instruções, uma linha por vez, de cima para baixo, "
                "é o **interpretador** Python.",
                "Aqui no PyQuest o interpretador já vem embutido: você escreve o código no editor e "
                "aperta **Executar** (ou Ctrl+Enter). O resultado aparece no painel de saída.",
                "## Por que Python?",
                "Python é usado em sites, ciência de dados, automação, jogos e inteligência artificial. "
                "A sintaxe é limpa e fácil de ler, o que faz dela uma ótima primeira linguagem.",
                "Experimente rodar o exemplo abaixo. É o clássico primeiro programa de todo mundo!",
            ],
            "exemplo": 'print("Olá, mundo Python!")',
        },
        {
            "titulo": "A função print()",
            "texto": [
                "`print()` mostra algo na tela. O texto vai entre aspas, que podem ser duplas `\"...\"` "
                "ou simples `'...'`. Um texto entre aspas se chama **string**.",
                "Cada `print()` escreve em uma nova linha. Um `print()` vazio gera uma linha em branco.",
                "Você também pode passar vários valores separados por vírgula: o Python coloca um espaço "
                "entre eles automaticamente.",
                "## Dica",
                "Se o seu texto tem um apóstrofo (como em *Joana D'Arc*), use aspas duplas por fora: "
                "`print(\"Joana D'Arc\")`.",
            ],
            "exemplo": 'print("Linha 1")\nprint()\nprint("Python", "é", "divertido")\nprint(\'Ela disse: "oi!"\')',
        },
        {
            "titulo": "Erros fazem parte do jogo",
            "texto": [
                "Todo programador vê mensagens de erro o tempo todo. A mensagem que o Python mostra se chama "
                "**traceback** e diz *onde* e *qual* foi o problema.",
                "Os mais comuns no começo:",
                "• `SyntaxError`: o Python não entendeu a linha (faltou fechar aspas ou parênteses, por exemplo).",
                "• `NameError`: você usou um nome que não existe, como `prnt` no lugar de `print`.",
                "Leia sempre a **última linha** do erro e confira o número da linha indicada. "
                "Rode o exemplo e veja um erro de propósito!",
            ],
            "exemplo": 'print("Este funciona")\nprnt("Este tem um erro de digitação")',
        },
    ],
    "quiz": [
        {"pergunta": "Qual comando mostra um texto na tela em Python?",
         "opcoes": ["show()", "print()", "echo()", "write()"], "correta": 1,
         "explicacao": "print() é a função que exibe valores na saída."},
        {"pergunta": "O que este código mostra?", "codigo": 'print("Py", "thon")',
         "opcoes": ["Python", "Py thon", "Py,thon", "Erro"], "correta": 1,
         "explicacao": "Valores separados por vírgula no print() recebem um espaço entre eles."},
        {"pergunta": "Qual é a extensão de um arquivo Python?",
         "opcoes": [".pt", ".pyt", ".py", ".python"], "correta": 2,
         "explicacao": "Arquivos Python terminam em .py, como ola_mundo.py."},
        {"pergunta": "Qual o problema desta linha?", "codigo": 'print("Bom dia)',
         "opcoes": ["Falta fechar as aspas", "print está escrito errado", "Não tem problema", "Falta um ponto e vírgula"],
         "correta": 0, "explicacao": "A string abriu com \" mas não fechou. Isso gera um SyntaxError."},
        {"pergunta": "Que erro aparece ao rodar `prnt(\"oi\")`?",
         "opcoes": ["SyntaxError", "TypeError", "NameError", "Nenhum"], "correta": 2,
         "explicacao": "prnt não existe, então o Python reclama de um nome desconhecido: NameError."},
        {"pergunta": "O que faz um `print()` sem nada dentro?",
         "opcoes": ["Dá erro", "Mostra a palavra None", "Mostra uma linha em branco", "Fecha o programa"],
         "correta": 2, "explicacao": "print() vazio imprime só a quebra de linha, ou seja, uma linha em branco."},
    ],
    "desafios": [
        {
            "titulo": "Olá, Mundo!",
            "enunciado": "Escreva um programa que mostre exatamente:\n\nOlá, mundo!",
            "inicial": "# Escreva seu código abaixo\n",
            "dica": "Use print() com o texto entre aspas: print(\"...\")",
            "solucao": 'print("Olá, mundo!")',
            "casos": [caso([saida("Olá, mundo!", flex=True)])],
        },
        {
            "titulo": "Apresentação",
            "enunciado": "Mostre 3 linhas sobre você:\n1. Seu nome\n2. Sua cidade\n3. Sua comida favorita",
            "inicial": "# Use um print() para cada linha\n",
            "dica": "Três print() seguidos, cada um com uma informação.",
            "solucao": 'print("Arth")\nprint("São Paulo")\nprint("Pizza")',
            "casos": [caso([n_linhas(3), tem("print")])],
        },
        {
            "titulo": "Caça-bugs: aspas perdidas",
            "enunciado": "Este código tem dois bugs. Conserte para que a saída seja:\n\n"
                         "Bem-vindo ao curso\nPython é demais!",
            "inicial": 'print("Bem-vindo ao curso)\nprint(\'Python é demais!")\n',
            "dica": "Cada string precisa abrir e fechar com o MESMO tipo de aspas.",
            "solucao": 'print("Bem-vindo ao curso")\nprint("Python é demais!")',
            "casos": [caso([saida("Bem-vindo ao curso\nPython é demais!", flex=True)])],
        },
        {
            "titulo": "Arte no terminal",
            "enunciado": "Desenhe uma figura usando print() e o caractere *. "
                         "Ela precisa ter pelo menos 4 linhas. Exemplo de triângulo:\n\n*\n**\n***\n****",
            "inicial": "# Seja criativo!\n",
            "dica": "Cada linha da figura é um print() diferente.",
            "solucao": 'print("*")\nprint("**")\nprint("***")\nprint("****")',
            "casos": [caso([min_linhas(4),
                            regra(lambda o, n, c: o.count("*") >= 4, "Use o caractere * no seu desenho.")])],
        },
    ],
    "chefe": {
        "titulo": "O Guardião do Terminal",
        "enunciado": "O Guardião só deixa passar quem mostrar um cartão de visitas assim (4 linhas):\n\n"
                     "==========\n<seu nome>\nAprendiz de Python\n==========\n\n"
                     "Regras: a 1ª e a 4ª linhas devem ter só sinais de = (pelo menos 10) e ser iguais. "
                     "A 3ª linha deve ser exatamente 'Aprendiz de Python'.",
        "inicial": "# Derrote o Guardião!\n",
        "dica": "print(\"==========\") cria a moldura. Lembre que são 4 print() no total.",
        "solucao": 'print("==========")\nprint("Arth")\nprint("Aprendiz de Python")\nprint("==========")',
        "casos": [caso([
            n_linhas(4),
            regra(lambda o, n, c: set(linhas(o)[0].strip()) == {"="} and len(linhas(o)[0].strip()) >= 10,
                  "A 1ª linha deve ter apenas sinais de = (pelo menos 10)."),
            regra(lambda o, n, c: linhas(o)[0].strip() == linhas(o)[3].strip(),
                  "A 1ª e a 4ª linhas devem ser iguais."),
            regra(lambda o, n, c: linhas(o)[2].strip() == "Aprendiz de Python",
                  "A 3ª linha deve ser exatamente: Aprendiz de Python"),
        ])],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 2
# ---------------------------------------------------------------------------

CAP2 = {
    "num": 2,
    "titulo": "Variáveis e Tipos Simples",
    "subtitulo": "Strings, números, f-strings e comentários",
    "licoes": [
        {
            "titulo": "Variáveis: etiquetas para valores",
            "texto": [
                "Uma **variável** é um nome que aponta para um valor: `mensagem = \"Oi\"`. "
                "Depois você usa o nome no lugar do valor. Se atribuir outro valor, o novo substitui o antigo.",
                "## Regras para nomes",
                "• Só letras, números e _ (underline). Não pode começar com número: `1nome` é inválido.",
                "• Sem espaços: use `nome_usuario`, não `nome usuario`.",
                "• Não use palavras reservadas do Python, como `print`, `if` ou `for`.",
                "• Prefira nomes curtos e claros: `idade` é melhor que `i` ou `idade_da_pessoa_cadastrada`.",
                "Se você digitar o nome errado depois, o Python dá `NameError`. Ele não corrige ortografia!",
            ],
            "exemplo": 'mensagem = "Olá, aprendiz!"\nprint(mensagem)\n\nmensagem = "Agora a mensagem mudou."\nprint(mensagem)',
        },
        {
            "titulo": "Strings e seus métodos",
            "texto": [
                "Strings têm **métodos**, ações que você chama com um ponto: `nome.title()`.",
                "• `title()` deixa cada palavra com inicial maiúscula.",
                "• `upper()` deixa TUDO MAIÚSCULO e `lower()` deixa tudo minúsculo.",
                "• `strip()`, `lstrip()` e `rstrip()` removem espaços extras (dos dois lados, da esquerda, da direita).",
                "• `removeprefix('...')` e `removesuffix('...')` tiram um pedaço do início ou do fim.",
                "## f-strings",
                "Para colocar variáveis dentro de um texto, use uma **f-string**: um f antes das aspas e as "
                "variáveis entre chaves: `f\"Olá, {nome}!\"`.",
                "## Caracteres especiais",
                "`\\n` quebra a linha e `\\t` insere uma tabulação.",
            ],
            "exemplo": 'primeiro = "ada"\nultimo = "lovelace"\nnome = f"{primeiro} {ultimo}"\n\nprint(nome.title())\nprint(nome.upper())\nprint(f"Olá, {nome.title()}!")\nprint("Linguagens:\\n\\tPython\\n\\tC")\n\nsite = "https://python.org"\nprint(site.removeprefix("https://"))',
        },
        {
            "titulo": "Números",
            "texto": [
                "Python trabalha com **inteiros** (`int`, como 7) e **floats** (`float`, números com ponto, como 7.5).",
                "Operadores: `+` soma, `-` subtrai, `*` multiplica, `/` divide e `**` é potência (`2 ** 3` é 8).",
                "Atenção: a divisão `/` sempre gera float. `4 / 2` dá `2.0`.",
                "## Truques úteis",
                "• Underlines deixam números grandes legíveis: `populacao = 14_000_000`.",
                "• Atribuição múltipla: `x, y, z = 0, 0, 0`.",
                "• Constantes (valores que não devem mudar) usam MAIÚSCULAS: `MAX_PONTOS = 100`.",
                "## Cuidado com tipos",
                "`\"Tenho \" + 25` dá `TypeError`, porque não dá para somar texto com número. "
                "Use uma f-string: `f\"Tenho {25} anos\"`.",
            ],
            "exemplo": 'print(2 + 3)\nprint(10 / 4)\nprint(2 ** 10)\n\npopulacao = 14_000_000\nprint(populacao)\n\nx, y, z = 1, 2, 3\nprint(x, y, z)\n\nidade = 25\nprint(f"Tenho {idade} anos")',
        },
        {
            "titulo": "Comentários e o Zen do Python",
            "texto": [
                "Tudo depois de `#` numa linha é um **comentário**: o Python ignora. Use comentários para "
                "explicar o *porquê* do seu código, para outras pessoas e para você no futuro.",
                "## O Zen do Python",
                "Python tem uma filosofia escondida. Rode `import this` para ler os princípios, como "
                "\"Bonito é melhor que feio\" e \"Simples é melhor que complexo\".",
            ],
            "exemplo": '# Este programa mostra o Zen do Python\nimport this',
        },
    ],
    "quiz": [
        {"pergunta": "Qual destes é um nome de variável válido?",
         "opcoes": ["2nome", "nome usuario", "nome_usuario", "nome-usuario"], "correta": 2,
         "explicacao": "Só letras, números e _; sem espaços, sem hífen e sem começar com número."},
        {"pergunta": "O que este código mostra?", "codigo": 'nome = "ada lovelace"\nprint(nome.title())',
         "opcoes": ["ADA LOVELACE", "Ada lovelace", "Ada Lovelace", "ada lovelace"], "correta": 2,
         "explicacao": "title() coloca a primeira letra de cada palavra em maiúscula."},
        {"pergunta": "O que este código mostra?", "codigo": 'a = 2\nb = 3\nprint(f"{a} + {b} = {a + b}")',
         "opcoes": ["a + b = a + b", "2 + 3 = 5", "{a} + {b} = {a + b}", "2 + 3 = 23"], "correta": 1,
         "explicacao": "Numa f-string, o que está entre chaves é calculado e trocado pelo valor."},
        {"pergunta": "Qual o resultado de `4 / 2`?",
         "opcoes": ["2", "2.0", "0.5", "Erro"], "correta": 1,
         "explicacao": "A divisão com / sempre resulta em float."},
        {"pergunta": "Quanto vale `2 ** 3`?",
         "opcoes": ["6", "8", "9", "23"], "correta": 1,
         "explicacao": "** é potência: 2 × 2 × 2 = 8."},
        {"pergunta": "O que `\"  python  \".strip()` retorna?",
         "opcoes": ["'python'", "'  python'", "'python  '", "'PYTHON'"], "correta": 0,
         "explicacao": "strip() remove espaços em branco dos dois lados."},
        {"pergunta": "O que acontece ao rodar isto?", "codigo": 'idade = 30\nprint("Idade: " + idade)',
         "opcoes": ["Mostra Idade: 30", "SyntaxError", "TypeError", "NameError"], "correta": 2,
         "explicacao": "Não dá para concatenar str com int. Use f\"Idade: {idade}\"."},
        {"pergunta": "Para que serve o # no código?",
         "opcoes": ["Cria uma variável", "Marca um comentário", "Multiplica números", "Importa módulos"],
         "correta": 1, "explicacao": "O Python ignora tudo depois do # na linha."},
    ],
    "desafios": [
        {
            "titulo": "Mensagem pessoal",
            "enunciado": "Crie uma variável `nome` com um nome qualquer e, usando uma f-string, mostre:\n\n"
                         "Olá, <nome>! Vamos aprender Python hoje?",
            "inicial": 'nome = ""\n',
            "dica": 'print(f"Olá, {nome}! Vamos aprender Python hoje?")',
            "solucao": 'nome = "Arth"\nprint(f"Olá, {nome}! Vamos aprender Python hoje?")',
            "casos": [caso([
                var_existe("nome", str),
                regra(lambda o, n, c: isinstance(n.get("nome"), str) and n["nome"].strip() != "",
                      "A variável `nome` não pode ficar vazia."),
                regra(lambda o, n, c: normalizar(o) == f"Olá, {n.get('nome')}! Vamos aprender Python hoje?",
                      "A saída deve ser: Olá, <nome>! Vamos aprender Python hoje?"),
                tem('f"', "Use uma f-string (f\"...\")."),
            ])],
        },
        {
            "titulo": "Três caras do mesmo nome",
            "enunciado": "A variável `nome` já vem pronta. Mostre o nome em 3 linhas:\n"
                         "1. tudo minúsculo\n2. TUDO MAIÚSCULO\n3. Com Iniciais Maiúsculas\n\n"
                         "Use os métodos de string, não reescreva o texto!",
            "inicial": 'nome = "aLaN tUrInG"\n',
            "dica": "nome.lower(), nome.upper() e nome.title()",
            "solucao": 'nome = "aLaN tUrInG"\nprint(nome.lower())\nprint(nome.upper())\nprint(nome.title())',
            "casos": [caso([saida("alan turing\nALAN TURING\nAlan Turing"),
                            tem(".lower()"), tem(".upper()"), tem(".title()")])],
        },
        {
            "titulo": "Faxina de strings",
            "enunciado": "Limpe os dados abaixo e mostre:\n\nGrace Hopper\nrelatorio\n\n"
                         "Use strip() na primeira variável e removesuffix() na segunda.",
            "inicial": 'cientista = "\\t   Grace Hopper  \\n"\narquivo = "relatorio.txt"\n',
            "dica": 'cientista.strip() e arquivo.removesuffix(".txt")',
            "solucao": 'cientista = "\\t   Grace Hopper  \\n"\narquivo = "relatorio.txt"\nprint(cientista.strip())\nprint(arquivo.removesuffix(".txt"))',
            "casos": [caso([
                regra(lambda o, n, c: o.splitlines()[:1] == ["Grace Hopper"] if o else False,
                      "A primeira linha deve ser exatamente 'Grace Hopper', sem espaços extras."),
                saida("Grace Hopper\nrelatorio"), tem("strip("), tem("removesuffix(")])],
        },
        {
            "titulo": "Os quatro caminhos para o 8",
            "enunciado": "Mostre o número 8 quatro vezes, uma por linha, usando uma operação diferente "
                         "em cada print(): soma, subtração, multiplicação e divisão.\n\n"
                         "Exemplo: print(5 + 3)",
            "inicial": "",
            "dica": "Divisão gera float, então 16 / 2 mostra 8.0, e tudo bem!",
            "solucao": "print(5 + 3)\nprint(10 - 2)\nprint(2 * 4)\nprint(16 / 2)",
            "casos": [caso([
                n_linhas(4),
                regra(lambda o, n, c: all(l.strip() in ("8", "8.0") for l in linhas(o)),
                      "Todas as linhas devem mostrar 8 (ou 8.0)."),
                tem("+"), tem("-"), tem("*"), tem("/")])],
        },
        {
            "titulo": "Caça-bugs: texto + número",
            "enunciado": "Este programa quebra com TypeError. Conserte para mostrar:\n\nTenho 25 anos e 1.75 de altura",
            "inicial": 'idade = 25\naltura = 1.75\nprint("Tenho " + idade + " anos e " + altura + " de altura")\n',
            "dica": "Troque a concatenação por uma f-string: f\"Tenho {idade} anos ...\"",
            "solucao": 'idade = 25\naltura = 1.75\nprint(f"Tenho {idade} anos e {altura} de altura")',
            "casos": [caso([saida("Tenho 25 anos e 1.75 de altura")])],
        },
    ],
    "chefe": {
        "titulo": "A Esfinge das Strings",
        "enunciado": "A Esfinge te entrega dados bagunçados. Responda o enigma:\n\n"
                     "1. Crie `nome_completo` com o primeiro nome e o sobrenome limpos e com iniciais maiúsculas.\n"
                     "2. Calcule `idade` usando as variáveis de ano (não escreva o número na mão!).\n"
                     "3. Mostre: Linus Torvalds tem 57 anos.",
        "inicial": 'primeiro = "   linus"\nsobrenome = "TORVALDS   "\nano_nascimento = 1969\nano_atual = 2026\n\n',
        "dica": 'nome_completo = f"{primeiro.strip()} {sobrenome.strip()}".title()  e  idade = ano_atual - ano_nascimento',
        "solucao": 'primeiro = "   linus"\nsobrenome = "TORVALDS   "\nano_nascimento = 1969\nano_atual = 2026\n\n'
                   'nome_completo = f"{primeiro.strip()} {sobrenome.strip()}".title()\nidade = ano_atual - ano_nascimento\n'
                   'print(f"{nome_completo} tem {idade} anos.")',
        "casos": [caso([var_igual("nome_completo", "Linus Torvalds"), var_igual("idade", 57),
                        nao_tem("57", "Calcule a idade com as variáveis, sem escrever 57."),
                        saida("Linus Torvalds tem 57 anos.")])],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 3
# ---------------------------------------------------------------------------

CAP3 = {
    "num": 3,
    "titulo": "Introdução às Listas",
    "subtitulo": "Guardar, acessar, mudar e organizar coleções",
    "licoes": [
        {
            "titulo": "O que é uma lista",
            "texto": [
                "Uma **lista** guarda vários itens em ordem, entre colchetes e separados por vírgula: "
                "`bikes = ['caloi', 'trek', 'specialized']`.",
                "Para pegar um item, use o **índice** dele entre colchetes. A contagem começa em **0**: "
                "`bikes[0]` é 'caloi'.",
                "Índices negativos contam do fim: `bikes[-1]` é o último, `bikes[-2]` o penúltimo.",
                "Itens de lista funcionam como qualquer valor, inclusive dentro de f-strings.",
            ],
            "exemplo": "bikes = ['caloi', 'trek', 'specialized']\nprint(bikes)\nprint(bikes[0])\nprint(bikes[-1].title())\nprint(f\"Minha primeira bike foi uma {bikes[0].title()}.\")",
        },
        {
            "titulo": "Mudar, adicionar e remover",
            "texto": [
                "• Mudar: `lista[0] = 'novo'`.",
                "• Adicionar ao fim: `lista.append('item')`.",
                "• Inserir numa posição: `lista.insert(0, 'item')`.",
                "• Apagar por posição: `del lista[1]`.",
                "• `lista.pop()` remove o último item **e devolve** ele para você usar. "
                "`lista.pop(0)` faz o mesmo com o item da posição 0.",
                "• `lista.remove('valor')` apaga pelo valor (só a primeira ocorrência).",
                "## Qual usar?",
                "Se você não vai usar o item removido, `del` ou `remove()`. Se vai usar, `pop()`.",
            ],
            "exemplo": "motos = ['honda', 'yamaha', 'suzuki']\nmotos[0] = 'ducati'\nmotos.append('bmw')\nmotos.insert(1, 'kawasaki')\nprint(motos)\n\nvendida = motos.pop()\nprint(f\"Vendi a {vendida}.\")\nmotos.remove('suzuki')\ndel motos[0]\nprint(motos)",
        },
        {
            "titulo": "Organizando listas",
            "texto": [
                "• `lista.sort()` ordena a própria lista **para sempre**. `sort(reverse=True)` ordena ao contrário.",
                "• `sorted(lista)` devolve uma cópia ordenada e a original continua igual.",
                "• `lista.reverse()` inverte a ordem atual.",
                "• `len(lista)` diz quantos itens ela tem.",
                "## Cuidado: IndexError",
                "Numa lista de 3 itens, os índices vão de 0 a 2. Pedir `lista[3]` dá `IndexError`. "
                "Para o último item, use sempre `lista[-1]`.",
            ],
            "exemplo": "carros = ['volvo', 'audi', 'fiat', 'byd']\nprint(sorted(carros))\nprint(carros)\ncarros.sort(reverse=True)\nprint(carros)\ncarros.reverse()\nprint(carros)\nprint(len(carros))",
        },
    ],
    "quiz": [
        {"pergunta": "O que é mostrado?", "codigo": "motos = ['honda', 'yamaha', 'suzuki']\nprint(motos[1])",
         "opcoes": ["honda", "yamaha", "suzuki", "IndexError"], "correta": 1,
         "explicacao": "Índices começam em 0, então [1] é o segundo item."},
        {"pergunta": "Como pegar o ÚLTIMO item de qualquer lista?",
         "opcoes": ["lista[0]", "lista[last]", "lista[-1]", "lista[len]"], "correta": 2,
         "explicacao": "-1 sempre aponta para o último item."},
        {"pergunta": "Qual a diferença entre sort() e sorted()?",
         "opcoes": ["Nenhuma", "sort() muda a lista; sorted() devolve uma cópia ordenada",
                    "sorted() muda a lista; sort() devolve cópia", "sort() só funciona com números"],
         "correta": 1, "explicacao": "sort() é permanente; sorted() é temporário."},
        {"pergunta": "`lista.pop()` sem argumento remove...",
         "opcoes": ["o primeiro item", "o último item", "um item aleatório", "todos os itens"], "correta": 1,
         "explicacao": "Sem índice, pop() remove e devolve o último."},
        {"pergunta": "Quanto vale `len(['a', 'b', 'c'])`?",
         "opcoes": ["2", "3", "4", "'abc'"], "correta": 1, "explicacao": "len() conta os itens: 3."},
        {"pergunta": "O que acontece?", "codigo": "cores = ['azul', 'verde', 'rosa']\nprint(cores[3])",
         "opcoes": ["Mostra rosa", "Mostra azul", "IndexError", "Mostra None"], "correta": 2,
         "explicacao": "Os índices vão de 0 a 2. O 3 não existe."},
        {"pergunta": "Qual o resultado?", "codigo": "x = ['a', 'b', 'a']\nx.remove('a')\nprint(x)",
         "opcoes": ["['b']", "['b', 'a']", "['a', 'b']", "Erro"], "correta": 1,
         "explicacao": "remove() apaga só a primeira ocorrência do valor."},
    ],
    "desafios": [
        {
            "titulo": "Recado para os amigos",
            "enunciado": "Crie uma lista `amigos` com pelo menos 3 nomes. Depois mostre uma mensagem para "
                         "cada um (uma por linha), acessando os itens pelo índice.\n\nExemplo: Oi, Ana! Bora codar?",
            "inicial": "amigos = []\n",
            "dica": "print(f\"Oi, {amigos[0]}! Bora codar?\") e repita com [1] e [2].",
            "solucao": "amigos = ['Ana', 'Beto', 'Caio']\nprint(f\"Oi, {amigos[0]}! Bora codar?\")\nprint(f\"Oi, {amigos[1]}! Bora codar?\")\nprint(f\"Oi, {amigos[2]}! Bora codar?\")",
            "casos": [caso([
                var_existe("amigos", list),
                regra(lambda o, n, c: isinstance(n.get("amigos"), list) and len(n["amigos"]) >= 3,
                      "A lista `amigos` precisa de pelo menos 3 nomes."),
                min_linhas(3),
                regra(lambda o, n, c: isinstance(n.get("amigos"), list) and
                      all(str(a) in o for a in n["amigos"][:3]),
                      "Cada um dos 3 primeiros amigos precisa aparecer na saída."),
                tem("amigos[", "Acesse os itens pelo índice, como amigos[0]."),
            ])],
        },
        {
            "titulo": "Lista de convidados",
            "enunciado": "Você vai dar um jantar. Faça estas mudanças, NESTA ordem, e no fim mostre a lista:\n"
                         "1. 'Alan' não pode ir: troque-o por 'Linus' (mesma posição).\n"
                         "2. Insira 'Guido' no começo da lista.\n"
                         "3. Adicione 'Margaret' no final.\n\n"
                         "Resultado: ['Guido', 'Ada', 'Linus', 'Grace', 'Margaret']",
            "inicial": "convidados = ['Ada', 'Alan', 'Grace']\n",
            "dica": "convidados[1] = 'Linus', depois insert(0, ...) e append(...).",
            "solucao": "convidados = ['Ada', 'Alan', 'Grace']\nconvidados[1] = 'Linus'\nconvidados.insert(0, 'Guido')\nconvidados.append('Margaret')\nprint(convidados)",
            "casos": [caso([var_igual("convidados", ['Guido', 'Ada', 'Linus', 'Grace', 'Margaret']),
                            tem("insert("), tem("append("),
                            saida("['Guido', 'Ada', 'Linus', 'Grace', 'Margaret']")])],
        },
        {
            "titulo": "A mesa encolheu",
            "enunciado": "A mesa só cabe 2 pessoas! Use pop() três vezes para tirar os últimos convidados "
                         "e, a cada um, mostre:\n\nDesculpe, <nome>, não cabe mais ninguém.\n\n"
                         "No fim, a lista deve ficar ['Ana', 'Bia'].",
            "inicial": "convidados = ['Ana', 'Bia', 'Caio', 'Duda', 'Edu']\n",
            "dica": "removido = convidados.pop() e depois print(f\"Desculpe, {removido}, ...\")",
            "solucao": "convidados = ['Ana', 'Bia', 'Caio', 'Duda', 'Edu']\n"
                       "removido = convidados.pop()\nprint(f\"Desculpe, {removido}, não cabe mais ninguém.\")\n"
                       "removido = convidados.pop()\nprint(f\"Desculpe, {removido}, não cabe mais ninguém.\")\n"
                       "removido = convidados.pop()\nprint(f\"Desculpe, {removido}, não cabe mais ninguém.\")",
            "casos": [caso([var_igual("convidados", ['Ana', 'Bia']), tem("pop("),
                            saida("Desculpe, Edu, não cabe mais ninguém.\nDesculpe, Duda, não cabe mais ninguém.\n"
                                  "Desculpe, Caio, não cabe mais ninguém.", flex=True)])],
        },
        {
            "titulo": "Viagens dos sonhos",
            "enunciado": "Mostre, nesta ordem (4 linhas):\n"
                         "1. A lista em ordem alfabética, sem alterar a original (sorted)\n"
                         "2. A lista original\n"
                         "3. A lista em ordem alfabética inversa, também sem alterar\n"
                         "4. Ordene a lista de verdade com sort() e mostre",
            "inicial": "lugares = ['tóquio', 'lisboa', 'cairo', 'quito', 'oslo']\n",
            "dica": "sorted(lugares, reverse=True) faz a ordem inversa temporária.",
            "solucao": "lugares = ['tóquio', 'lisboa', 'cairo', 'quito', 'oslo']\nprint(sorted(lugares))\nprint(lugares)\nprint(sorted(lugares, reverse=True))\nlugares.sort()\nprint(lugares)",
            "casos": [caso([
                saida("['cairo', 'lisboa', 'oslo', 'quito', 'tóquio']\n['tóquio', 'lisboa', 'cairo', 'quito', 'oslo']\n"
                      "['tóquio', 'quito', 'oslo', 'lisboa', 'cairo']\n['cairo', 'lisboa', 'oslo', 'quito', 'tóquio']"),
                tem("sorted("), tem(".sort(")])],
        },
        {
            "titulo": "Caça-bugs: fora da lista",
            "enunciado": "O programador queria mostrar a ÚLTIMA fruta, mas o código dá IndexError. "
                         "Conserte de um jeito que funcione mesmo se a lista crescer.",
            "inicial": "frutas = ['maçã', 'banana', 'uva']\nprint(frutas[3])\n",
            "dica": "Qual índice sempre aponta para o último item?",
            "solucao": "frutas = ['maçã', 'banana', 'uva']\nprint(frutas[-1])",
            "casos": [caso([saida("uva"), tem("[-1]", "Use o índice -1, que funciona para qualquer tamanho.")])],
        },
    ],
    "chefe": {
        "titulo": "O Dragão da Lista",
        "enunciado": "O dragão guarda um tesouro de números. Para vencê-lo, faça em ordem:\n"
                     "1. Adicione 50 ao final\n2. Remova o 7 (pelo valor)\n3. Insira 1 no começo\n"
                     "4. Ordene do maior para o menor\n"
                     "5. Mostre usando índices e len():\n\nMaior: 88 | Menor: 1 | Itens: 6",
        "inicial": "tesouro = [42, 7, 19, 3, 88]\n",
        "dica": "Depois de sort(reverse=True), o maior está em [0] e o menor em [-1].",
        "solucao": "tesouro = [42, 7, 19, 3, 88]\ntesouro.append(50)\ntesouro.remove(7)\ntesouro.insert(0, 1)\n"
                   "tesouro.sort(reverse=True)\nprint(f\"Maior: {tesouro[0]} | Menor: {tesouro[-1]} | Itens: {len(tesouro)}\")",
        "casos": [caso([var_igual("tesouro", [88, 50, 42, 19, 3, 1]), tem("len("), tem(".remove("),
                        saida("Maior: 88 | Menor: 1 | Itens: 6")])],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 4
# ---------------------------------------------------------------------------

CAP4 = {
    "num": 4,
    "titulo": "Trabalhando com Listas",
    "subtitulo": "Laços for, range(), fatias e tuplas",
    "licoes": [
        {
            "titulo": "Percorrendo listas com for",
            "texto": [
                "O laço `for` repete um bloco de código para cada item de uma lista:",
                "`for magico in magicos:` lê-se \"para cada mágico na lista de mágicos\".",
                "O que fica **indentado** (4 espaços) depois dos dois-pontos faz parte do laço e roda a cada volta. "
                "O que volta para a margem roda uma vez só, depois que o laço termina.",
                "## Erros clássicos",
                "• Esquecer os dois-pontos `:` no fim da linha do for, que dá `SyntaxError`.",
                "• Esquecer de indentar o bloco, que dá `IndentationError`.",
                "• Indentar algo que deveria rodar só uma vez: o código roda, mas repete sem querer (erro de lógica!).",
            ],
            "exemplo": "magicos = ['alice', 'david', 'carolina']\nfor magico in magicos:\n    print(f\"{magico.title()}, que truque incrível!\")\n    print(f\"Mal posso esperar pelo próximo, {magico.title()}.\\n\")\n\nprint(\"Obrigado a todos, foi um ótimo show!\")",
        },
        {
            "titulo": "Listas numéricas e range()",
            "texto": [
                "`range(1, 5)` gera 1, 2, 3, 4. O último número NÃO entra.",
                "`range(2, 11, 2)` conta de 2 em 2. `list(range(...))` transforma o resultado numa lista.",
                "Funções úteis com números: `min()`, `max()` e `sum()`.",
                "## List comprehension",
                "Um jeito compacto de criar listas num laço só: "
                "`quadrados = [n ** 2 for n in range(1, 11)]`.",
            ],
            "exemplo": "for n in range(1, 5):\n    print(n)\n\npares = list(range(2, 11, 2))\nprint(pares)\nprint(min(pares), max(pares), sum(pares))\n\nquadrados = [n ** 2 for n in range(1, 11)]\nprint(quadrados)",
        },
        {
            "titulo": "Fatias e cópias",
            "texto": [
                "Uma **fatia** pega um pedaço da lista: `jogadores[0:3]` pega os índices 0, 1 e 2.",
                "• `[:2]` vai do começo até antes do 2. • `[2:]` vai do 2 até o fim. • `[-3:]` pega os 3 últimos.",
                "Dá para usar fatias num for: `for j in jogadores[:3]:`.",
                "## Copiando listas",
                "`copia = original[:]` cria uma lista nova e independente. "
                "Já `copia = original` só cria outro nome para a MESMA lista, então mudar uma muda a outra!",
            ],
            "exemplo": "jogadores = ['ana', 'bia', 'caio', 'duda', 'edu']\nprint(jogadores[1:4])\nprint(jogadores[:2])\nprint(jogadores[-3:])\n\nmeus = ['pizza', 'lasanha']\nde_amigo = meus[:]\nmeus.append('sushi')\nde_amigo.append('tacos')\nprint(meus)\nprint(de_amigo)",
        },
        {
            "titulo": "Tuplas",
            "texto": [
                "Uma **tupla** é como uma lista que não pode mudar. Usa parênteses: `dimensoes = (200, 50)`.",
                "Você lê os itens normalmente (`dimensoes[0]`) e pode percorrer com for, mas "
                "`dimensoes[0] = 10` dá `TypeError`.",
                "Tupla de um item só precisa de vírgula: `(3,)`.",
                "Para \"mudar\" uma tupla, atribua uma tupla inteira nova à variável.",
            ],
            "exemplo": "dimensoes = (200, 50)\nfor d in dimensoes:\n    print(d)\n\ndimensoes = (400, 100)\nprint(dimensoes)",
        },
    ],
    "quiz": [
        {"pergunta": "O que é mostrado?", "codigo": "for x in range(1, 4):\n    print(x)",
         "opcoes": ["1 2 3 4", "0 1 2 3", "1 2 3", "1 2 3 (numa linha só)"], "correta": 2,
         "explicacao": "range(1, 4) vai de 1 a 3, um número por linha."},
        {"pergunta": "Qual o resultado de `list(range(2, 11, 2))`?",
         "opcoes": ["[2, 4, 6, 8]", "[2, 4, 6, 8, 10]", "[2, 11, 2]", "[0, 2, 4, 6, 8, 10]"], "correta": 1,
         "explicacao": "Começa em 2, pula de 2 em 2 e para antes de 11."},
        {"pergunta": "O que esta comprehension gera?", "codigo": "[x * 10 for x in range(1, 4)]",
         "opcoes": ["[10, 20, 30]", "[1, 2, 3]", "[10, 20, 30, 40]", "[0, 10, 20]"], "correta": 0,
         "explicacao": "Para x = 1, 2, 3 calcula x * 10."},
        {"pergunta": "Qual o resultado?", "codigo": "nums = [10, 20, 30, 40]\nprint(nums[1:3])",
         "opcoes": ["[10, 20]", "[20, 30]", "[20, 30, 40]", "[10, 20, 30]"], "correta": 1,
         "explicacao": "A fatia [1:3] pega os índices 1 e 2."},
        {"pergunta": "Qual destes cria uma CÓPIA independente da lista?",
         "opcoes": ["nova = lista", "nova = lista[:]", "nova == lista", "nova = lista[0]"], "correta": 1,
         "explicacao": "[:] fatia a lista inteira e cria uma nova."},
        {"pergunta": "O que acontece?", "codigo": "t = (1, 2, 3)\nt[0] = 5",
         "opcoes": ["t vira (5, 2, 3)", "TypeError", "IndexError", "Nada"], "correta": 1,
         "explicacao": "Tuplas são imutáveis: não aceitam mudar item."},
        {"pergunta": "Quantas vezes 'fim' é mostrado?", "codigo": "for n in [1, 2, 3]:\n    print(n)\nprint('fim')",
         "opcoes": ["0", "1", "3", "4"], "correta": 1,
         "explicacao": "O print('fim') não está indentado, então roda uma vez, depois do laço."},
        {"pergunta": "Esqueceu os `:` no fim de `for x in lista`. Que erro aparece?",
         "opcoes": ["NameError", "SyntaxError", "TypeError", "Nenhum"], "correta": 1,
         "explicacao": "Faltar os dois-pontos é um erro de sintaxe."},
    ],
    "desafios": [
        {
            "titulo": "Noite da pizza",
            "enunciado": "Crie uma lista `pizzas` com pelo menos 3 sabores. Use um for para mostrar\n"
                         "Eu gosto de pizza de <sabor>.\npara cada uma. Depois do laço (uma vez só), mostre:\n"
                         "Eu realmente amo pizza!",
            "inicial": "pizzas = []\n",
            "dica": "O último print fica SEM indentação, fora do for.",
            "solucao": "pizzas = ['calabresa', 'mussarela', 'portuguesa']\nfor pizza in pizzas:\n    print(f\"Eu gosto de pizza de {pizza}.\")\nprint(\"Eu realmente amo pizza!\")",
            "casos": [caso([
                var_existe("pizzas", list),
                regra(lambda o, n, c: isinstance(n.get("pizzas"), list) and len(n["pizzas"]) >= 3,
                      "A lista precisa de pelo menos 3 sabores."),
                regra(lambda o, n, c: isinstance(n.get("pizzas"), list) and normalizar(o) == "\n".join(
                    [f"Eu gosto de pizza de {p}." for p in n["pizzas"]] + ["Eu realmente amo pizza!"]),
                      "Confira o texto: uma linha 'Eu gosto de pizza de <sabor>.' por sabor e, no fim, "
                      "'Eu realmente amo pizza!' uma única vez."),
                tem("for ")])],
        },
        {
            "titulo": "Contando até 20",
            "enunciado": "Use um for com range() para mostrar os números de 1 a 20, um por linha.",
            "inicial": "",
            "dica": "range(1, 21). O último número não entra!",
            "solucao": "for n in range(1, 21):\n    print(n)",
            "casos": [caso([saida("\n".join(str(i) for i in range(1, 21))), tem("range("), tem("for ")])],
        },
        {
            "titulo": "Cubos instantâneos",
            "enunciado": "Usando UMA list comprehension, crie a lista `cubos` com os cubos de 1 a 10 "
                         "(1, 8, 27, ..., 1000) e mostre a lista.",
            "inicial": "cubos = \n",
            "dica": "[n ** 3 for n in range(1, 11)]",
            "solucao": "cubos = [n ** 3 for n in range(1, 11)]\nprint(cubos)",
            "casos": [caso([var_igual("cubos", [n ** 3 for n in range(1, 11)]),
                            regra(lambda o, n, c: re.search(r"\[[^\]]*for[^\]]*in[^\]]*\]", c) is not None,
                                  "Use uma list comprehension: [ ... for ... in ... ]."),
                            saida(str([n ** 3 for n in range(1, 11)]))])],
        },
        {
            "titulo": "Fatiando o bolo",
            "enunciado": "Usando fatias da lista `fatias`, crie três variáveis:\n"
                         "• `inicio` com os 3 primeiros itens\n• `meio` com os 3 do meio\n• `fim` com os 3 últimos\n"
                         "e mostre as três (uma por linha).",
            "inicial": "fatias = ['morango', 'chocolate', 'limão', 'coco', 'nozes', 'banana', 'uva', 'menta', 'café']\n",
            "dica": "fatias[:3], fatias[3:6] e fatias[-3:]",
            "solucao": "fatias = ['morango', 'chocolate', 'limão', 'coco', 'nozes', 'banana', 'uva', 'menta', 'café']\n"
                       "inicio = fatias[:3]\nmeio = fatias[3:6]\nfim = fatias[-3:]\nprint(inicio)\nprint(meio)\nprint(fim)",
            "casos": [caso([var_igual("inicio", ['morango', 'chocolate', 'limão']),
                            var_igual("meio", ['coco', 'nozes', 'banana']),
                            var_igual("fim", ['uva', 'menta', 'café']),
                            regra(lambda o, n, c: c.count("'morango'") <= 1, "Use fatias, sem reescrever os itens."),
                            n_linhas(3)])],
        },
        {
            "titulo": "Buffet imutável",
            "enunciado": "Crie uma TUPLA `cardapio` com 5 pratos e mostre cada um com um for. "
                         "Depois o restaurante mudou dois pratos: atribua uma nova tupla de 5 pratos "
                         "a `cardapio` e mostre de novo com outro for.",
            "inicial": "cardapio = ()\n",
            "dica": "Tuplas usam parênteses. Para mudar, crie uma tupla inteira nova.",
            "solucao": "cardapio = ('arroz', 'feijão', 'salada', 'frango', 'pudim')\nfor prato in cardapio:\n    print(prato)\n\n"
                       "cardapio = ('arroz', 'feijão', 'salada', 'peixe', 'mousse')\nfor prato in cardapio:\n    print(prato)",
            "casos": [caso([var_existe("cardapio", tuple),
                            regra(lambda o, n, c: isinstance(n.get("cardapio"), tuple) and len(n["cardapio"]) == 5,
                                  "A tupla final deve ter 5 pratos."),
                            regra(lambda o, n, c: c.count("for ") >= 2, "Use dois laços for."),
                            n_linhas(10)])],
        },
        {
            "titulo": "Caça-bugs: indentação",
            "enunciado": "Este show está quebrado. Conserte para mostrar um elogio para cada mágico "
                         "e o agradecimento UMA vez só no final:\n\n"
                         "Alice, que truque incrível!\nDavid, que truque incrível!\nCarolina, que truque incrível!\n"
                         "Obrigado a todos!",
            "inicial": "magicos = ['alice', 'david', 'carolina']\nfor magico in magicos\nprint(f\"{magico.title()}, que truque incrível!\")\n    print(\"Obrigado a todos!\")\n",
            "dica": "Faltam os dois-pontos, o print do elogio vai pra dentro do for e o agradecimento sai dele.",
            "solucao": "magicos = ['alice', 'david', 'carolina']\nfor magico in magicos:\n    print(f\"{magico.title()}, que truque incrível!\")\nprint(\"Obrigado a todos!\")",
            "casos": [caso([saida("Alice, que truque incrível!\nDavid, que truque incrível!\n"
                                  "Carolina, que truque incrível!\nObrigado a todos!", flex=True)])],
        },
    ],
    "chefe": {
        "titulo": "A Hidra dos Laços",
        "enunciado": "Cada cabeça da Hidra é um número par! Para vencê-la:\n"
                     "1. Crie `pares` com os números pares de 2 a 50 usando range()\n"
                     "2. Calcule `soma` com sum()\n"
                     "3. Mostre: Soma dos pares: 650\n"
                     "4. Com um for numa FATIA, mostre os 5 últimos pares, um por linha (42 a 50).",
        "inicial": "",
        "dica": "pares = list(range(2, 51, 2)). Para os 5 últimos, percorra a fatia pares[-5:].",
        "solucao": "pares = list(range(2, 51, 2))\nsoma = sum(pares)\nprint(f\"Soma dos pares: {soma}\")\nfor p in pares[-5:]:\n    print(p)",
        "casos": [caso([var_igual("pares", list(range(2, 51, 2))), var_igual("soma", 650),
                        tem("range("), tem("sum("), tem("[-5:]", "Use a fatia [-5:] no for."),
                        saida("Soma dos pares: 650\n42\n44\n46\n48\n50")])],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 5
# ---------------------------------------------------------------------------

def _fase(idade):
    if idade < 2:
        return "bebê"
    elif idade < 13:
        return "criança"
    elif idade < 20:
        return "adolescente"
    elif idade < 65:
        return "adulto"
    return "idoso"


def _nota(n):
    if n < 0 or n > 100:
        return "Nota inválida"
    if n >= 90:
        c = "A"
    elif n >= 80:
        c = "B"
    elif n >= 70:
        c = "C"
    elif n >= 60:
        c = "D"
    else:
        c = "F"
    out = [c, "Aprovado" if n >= 60 else "Reprovado"]
    if n == 100:
        out.append("Perfeito!")
    return "\n".join(out)


def _frutas(lista):
    out = []
    for f in ["banana", "manga", "uva", "kiwi", "caju"]:
        if f in lista:
            out.append(f"Você gosta mesmo de {f}!")
    return "\n".join(out)


def _usuarios(lista):
    if not lista:
        return "Precisamos encontrar alguns usuários!"
    out = []
    for u in lista:
        if u == "admin":
            out.append("Olá, admin, quer ver o relatório de status?")
        else:
            out.append(f"Olá, {u}, obrigado por entrar de novo.")
    return "\n".join(out)


CAP5 = {
    "num": 5,
    "titulo": "Instruções if",
    "subtitulo": "Testes condicionais e decisões no código",
    "licoes": [
        {
            "titulo": "Testes condicionais",
            "texto": [
                "Um **teste condicional** é uma expressão que vale `True` (verdadeiro) ou `False` (falso).",
                "• `==` pergunta se é igual (`=` sozinho atribui valor, não compara!).",
                "• `!=` pergunta se é diferente.",
                "• `<`, `<=`, `>`, `>=` comparam números.",
                "• O teste diferencia maiúsculas: `'Audi' == 'audi'` é False. Use `.lower()` para comparar sem isso.",
                "## Combinando testes",
                "• `and`: os dois lados precisam ser True. • `or`: basta um lado ser True.",
                "• `in` e `not in` verificam se um valor está (ou não) numa lista.",
            ],
            "exemplo": "carro = 'Audi'\nprint(carro == 'audi')\nprint(carro.lower() == 'audi')\n\nidade = 19\nprint(idade >= 18 and idade < 21)\n\nbanidos = ['ana', 'edu']\nusuario = 'bia'\nprint(usuario not in banidos)",
        },
        {
            "titulo": "if, elif e else",
            "texto": [
                "`if condição:` roda o bloco indentado só se a condição for True.",
                "`else:` roda quando o if (e todos os elif) falharem.",
                "`elif` testa outras condições em sequência. O Python para no **primeiro** teste verdadeiro.",
                "## Vários testes independentes",
                "Se mais de uma coisa pode ser verdade ao mesmo tempo, use vários `if` separados em vez de "
                "`elif`. Assim todos são verificados.",
                "O `else` é opcional. Às vezes um `elif` final deixa o código mais claro.",
            ],
            "exemplo": "idade = 12\n\nif idade < 4:\n    preco = 0\nelif idade < 18:\n    preco = 25\nelse:\n    preco = 40\n\nprint(f\"Seu ingresso custa R$ {preco}.\")\n\ncoberturas = ['queijo', 'cebola']\nif 'queijo' in coberturas:\n    print('Adicionando queijo.')\nif 'bacon' in coberturas:\n    print('Adicionando bacon.')\nif 'cebola' in coberturas:\n    print('Adicionando cebola.')",
        },
        {
            "titulo": "if com listas",
            "texto": [
                "Juntando `for` e `if` você trata itens especiais: dentro do laço, um if decide o que fazer com cada item.",
                "## Lista vazia?",
                "Uma lista vazia vale False num if. Então `if pedidos:` significa \"se tem pedidos\".",
                "## Comparando duas listas",
                "Percorra uma lista e use `in` para checar se cada item existe na outra.",
            ],
            "exemplo": "disponiveis = ['queijo', 'tomate', 'milho']\npedidos = ['queijo', 'abacaxi', 'milho']\n\nif pedidos:\n    for item in pedidos:\n        if item in disponiveis:\n            print(f\"Adicionando {item}.\")\n        else:\n            print(f\"Desculpe, não temos {item}.\")\nelse:\n    print('Pizza simples, então?')",
        },
    ],
    "quiz": [
        {"pergunta": "Qual o valor de `'Audi' == 'audi'`?",
         "opcoes": ["True", "False", "Erro", "None"], "correta": 1,
         "explicacao": "A comparação diferencia maiúsculas de minúsculas."},
        {"pergunta": "Com x = 5, quanto vale `x > 3 and x < 4`?",
         "opcoes": ["True", "False", "5", "Erro"], "correta": 1,
         "explicacao": "x > 3 é True, mas x < 4 é False. Com and, basta um falso para dar False."},
        {"pergunta": "Qual o valor de `'maçã' in ['banana', 'maçã']`?",
         "opcoes": ["True", "False", "1", "'maçã'"], "correta": 0,
         "explicacao": "in verifica se o valor está na lista."},
        {"pergunta": "O que é mostrado?", "codigo": "idade = 12\nif idade < 4:\n    print('grátis')\nelif idade < 18:\n    print('meia')\nelse:\n    print('inteira')",
         "opcoes": ["grátis", "meia", "inteira", "meia e inteira"], "correta": 1,
         "explicacao": "12 não é < 4, mas é < 18. O elif roda e o resto é ignorado."},
        {"pergunta": "Se `lista = []`, o bloco de `if lista:` roda?",
         "opcoes": ["Sim", "Não", "Dá erro", "Só se tiver else"], "correta": 1,
         "explicacao": "Lista vazia vale False num teste."},
        {"pergunta": "Qual a diferença entre `=` e `==`?",
         "opcoes": ["Nenhuma", "= atribui; == compara", "= compara; == atribui", "== só funciona com números"],
         "correta": 1, "explicacao": "Um sinal guarda valor, dois sinais perguntam se é igual."},
        {"pergunta": "Quantas linhas são mostradas?", "codigo": "x = 10\nif x > 5:\n    print('a')\nif x > 8:\n    print('b')\nif x > 20:\n    print('c')",
         "opcoes": ["1", "2", "3", "0"], "correta": 1,
         "explicacao": "São ifs independentes: 'a' e 'b' passam, 'c' não."},
    ],
    "desafios": [
        {
            "titulo": "Pontos alienígenas",
            "enunciado": "Um alienígena foi abatido! A variável `cor` já existe (o verificador testa várias cores). "
                         "Mostre:\n• 'verde': Você ganhou 5 pontos!\n• 'amarelo': Você ganhou 10 pontos!\n"
                         "• qualquer outra: Você ganhou 15 pontos!",
            "inicial": "# A variável cor é fornecida. Para testar, ela começa como 'verde'.\n\n",
            "dica": "if cor == 'verde': ... elif cor == 'amarelo': ... else: ...",
            "solucao": "if cor == 'verde':\n    print('Você ganhou 5 pontos!')\nelif cor == 'amarelo':\n    print('Você ganhou 10 pontos!')\nelse:\n    print('Você ganhou 15 pontos!')",
            "casos": [caso([saida("Você ganhou 5 pontos!", flex=True)], {"cor": "verde"}),
                      caso([saida("Você ganhou 10 pontos!", flex=True)], {"cor": "amarelo"}),
                      caso([saida("Você ganhou 15 pontos!", flex=True)], {"cor": "vermelho"}),
                      caso([saida("Você ganhou 15 pontos!", flex=True)], {"cor": "azul"})],
        },
        {
            "titulo": "Fases da vida",
            "enunciado": "A variável `idade` é fornecida. Mostre só a palavra da fase:\n"
                         "• menos de 2: bebê\n• menos de 13: criança\n• menos de 20: adolescente\n"
                         "• menos de 65: adulto\n• 65 ou mais: idoso",
            "inicial": "# A variável idade é fornecida. Para testar, ela começa como 1.\n\n",
            "dica": "Uma cadeia if / elif / elif / elif / else, dos menores para os maiores.",
            "solucao": "if idade < 2:\n    print('bebê')\nelif idade < 13:\n    print('criança')\nelif idade < 20:\n    print('adolescente')\nelif idade < 65:\n    print('adulto')\nelse:\n    print('idoso')",
            "casos": [caso([saida(_fase(i), flex=True)], {"idade": i}) for i in [1, 2, 12, 13, 19, 20, 64, 65, 90]],
        },
        {
            "titulo": "Frutas favoritas",
            "enunciado": "A lista `frutas_favoritas` é fornecida. Escreva IFs independentes (não elif) checando, "
                         "nesta ordem: banana, manga, uva, kiwi, caju. Para cada uma que estiver na lista, mostre:\n\n"
                         "Você gosta mesmo de <fruta>!",
            "inicial": "# frutas_favoritas é fornecida. Para testar, começa como ['manga', 'uva', 'caju'].\n\n",
            "dica": "if 'banana' in frutas_favoritas: ...  (5 ifs separados)",
            "solucao": "\n".join(f"if '{f}' in frutas_favoritas:\n    print('Você gosta mesmo de {f}!')"
                                  for f in ["banana", "manga", "uva", "kiwi", "caju"]),
            "casos": [caso([saida(_frutas(l), flex=True), tem(" in ")], {"frutas_favoritas": l})
                      for l in [['manga', 'uva', 'caju'], ['banana', 'kiwi'], ['caju', 'banana', 'manga', 'uva', 'kiwi']]],
        },
        {
            "titulo": "Olá, admin",
            "enunciado": "A lista `usuarios` é fornecida.\n• Se estiver vazia: Precisamos encontrar alguns usuários!\n"
                         "• Senão, para cada usuário:\n   – se for 'admin': Olá, admin, quer ver o relatório de status?\n"
                         "   – outros: Olá, <nome>, obrigado por entrar de novo.",
            "inicial": "# usuarios é fornecida. Para testar, começa como ['admin', 'ana', 'beto'].\n\n",
            "dica": "if usuarios: for u in usuarios: if u == 'admin': ... else: ...  e um else final para a lista vazia.",
            "solucao": "if usuarios:\n    for u in usuarios:\n        if u == 'admin':\n            print('Olá, admin, quer ver o relatório de status?')\n        else:\n            print(f'Olá, {u}, obrigado por entrar de novo.')\nelse:\n    print('Precisamos encontrar alguns usuários!')",
            "casos": [caso([saida(_usuarios(l), flex=True)], {"usuarios": l})
                      for l in [['admin', 'ana', 'beto'], [], ['carla', 'admin']]],
        },
        {
            "titulo": "Caça-bugs: o número da sorte",
            "enunciado": "A variável `numero` é fornecida. Conserte os bugs para mostrar 'Sorte!' quando "
                         "numero for 7, e 'Tente de novo.' nos outros casos.",
            "inicial": "# numero é fornecido. Para testar, começa como 7.\nif numero = 7:\n    print('Sorte!')\nelse\n    print('Tente de novo.')\n",
            "dica": "Comparar usa ==, e o else também precisa de dois-pontos.",
            "solucao": "if numero == 7:\n    print('Sorte!')\nelse:\n    print('Tente de novo.')",
            "casos": [caso([saida("Sorte!")], {"numero": 7}), caso([saida("Tente de novo.")], {"numero": 3}),
                      caso([saida("Tente de novo.")], {"numero": 70})],
        },
    ],
    "chefe": {
        "titulo": "O Rei Condicional",
        "enunciado": "O Rei vai testar seu sistema de notas com vários valores de `nota` (fornecida).\n\n"
                     "• Se a nota for menor que 0 ou maior que 100: mostre só 'Nota inválida'.\n"
                     "• Senão, na 1ª linha o conceito: 90+ A, 80+ B, 70+ C, 60+ D, abaixo F.\n"
                     "• Na 2ª linha: 'Aprovado' (60 ou mais) ou 'Reprovado'.\n"
                     "• Se for exatamente 100, uma 3ª linha: 'Perfeito!'",
        "inicial": "# nota é fornecida. Para testar, começa como 100.\n\n",
        "dica": "Comece com if nota < 0 or nota > 100: ... else: e dentro do else monte o conceito com if/elif.",
        "solucao": "if nota < 0 or nota > 100:\n    print('Nota inválida')\nelse:\n    if nota >= 90:\n        print('A')\n    elif nota >= 80:\n        print('B')\n    elif nota >= 70:\n        print('C')\n    elif nota >= 60:\n        print('D')\n    else:\n        print('F')\n    if nota >= 60:\n        print('Aprovado')\n    else:\n        print('Reprovado')\n    if nota == 100:\n        print('Perfeito!')",
        "casos": [caso([saida(_nota(n), flex=True)], {"nota": n}) for n in [100, 95, 85, 70, 65, 60, 59, 0, -5, 101]],
    },
}

# ---------------------------------------------------------------------------
# Ferramentas extras de verificação (capítulos 6 a 11)
# ---------------------------------------------------------------------------

def _fmt_chamada(nome, args, kwargs):
    partes = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in (kwargs or {}).items()]
    return f"{nome}({', '.join(partes)})"


def chama(nome, args, esperado, kwargs=None, msg=None):
    def f(out, ns, code):
        return callable(ns.get(nome)) and ns[nome](*args, **(kwargs or {})) == esperado
    return (f, msg or f"{_fmt_chamada(nome, args, kwargs)} deveria devolver {esperado!r}.")


def funcao(nome):
    return (lambda out, ns, code: callable(ns.get(nome)),
            f"Crie a função `{nome}`.")


def classe(nome):
    return (lambda out, ns, code: isinstance(ns.get(nome), type),
            f"Crie a classe `{nome}`.")


def arquivo_igual(nome, esperado):
    def f(out, ns, code):
        conteudo = ns.get("__arquivos_saida__", {}).get(nome)
        return conteudo is not None and normalizar(conteudo) == normalizar(esperado)
    return (f, f"O arquivo '{nome}' deveria conter:\n{esperado}")


def arquivo_json(nome, esperado):
    import json

    def f(out, ns, code):
        conteudo = ns.get("__arquivos_saida__", {}).get(nome)
        if conteudo is None:
            return False
        try:
            return json.loads(conteudo) == esperado
        except ValueError:
            return False
    return (f, f"O arquivo '{nome}' deveria conter o JSON: {json.dumps(esperado, ensure_ascii=False)}")


def entradas(*valores):
    return {"__entradas__": list(valores)}


def _testes_do_aluno(ns):
    return [v for k, v in ns.items() if k.startswith("test_") and callable(v)]


def min_testes(n):
    return (lambda out, ns, code: len(_testes_do_aluno(ns)) >= n,
            f"Escreva pelo menos {n} função(ões) de teste com nome começando em test_.")


def testes_passam():
    def f(out, ns, code):
        for t in _testes_do_aluno(ns):
            t()
        return True
    return (f, "Algum dos seus testes falhou com o código correto. Confira os valores esperados nos asserts.")


def testes_pegam(nome, impostor, descricao):
    """Troca `nome` por uma versão com bug: algum teste do aluno precisa falhar."""
    def f(out, ns, code):
        original = ns.get(nome)
        ns[nome] = impostor
        try:
            for t in _testes_do_aluno(ns):
                try:
                    t()
                except Exception:
                    return True
            return False
        finally:
            ns[nome] = original
    return (f, f"Seus testes não perceberam um bug: {descricao}. Escreva um teste que pegue esse erro.")


# ---------------------------------------------------------------------------
# CAPÍTULO 6: Dicionários
# ---------------------------------------------------------------------------

def _rios(rios):
    out = [f"{r.title()} passa por {p.title()}." for r, p in rios.items()]
    out.append("Rios: " + ", ".join(r.title() for r in rios))
    out.append("Países: " + ", ".join(p.title() for p in rios.values()))
    return "\n".join(out)


def _contagem(palavras):
    c = {}
    for p in palavras:
        c[p] = c.get(p, 0) + 1
    return c


def _times(jogadores):
    soma = {}
    campeao = jogadores[0]
    for j in jogadores:
        soma[j["time"]] = soma.get(j["time"], 0) + j["pontos"]
        if j["pontos"] > campeao["pontos"]:
            campeao = j
    linhas = [f"{t}: {soma[t]}" for t in sorted(soma)]
    linhas.append(f"Campeão: {campeao['nome'].title()}")
    return soma, "\n".join(linhas)


_JOG1 = [{'nome': 'ana', 'pontos': 120, 'time': 'azul'}, {'nome': 'beto', 'pontos': 80, 'time': 'verde'},
         {'nome': 'carla', 'pontos': 150, 'time': 'azul'}, {'nome': 'davi', 'pontos': 95, 'time': 'verde'}]
_JOG2 = [{'nome': 'edu', 'pontos': 40, 'time': 'roxo'}, {'nome': 'fabi', 'pontos': 200, 'time': 'amarelo'},
         {'nome': 'gil', 'pontos': 70, 'time': 'roxo'}]

CAP6 = {
    "num": 6,
    "titulo": "Dicionários",
    "subtitulo": "Pares chave-valor, laços e aninhamento",
    "licoes": [
        {
            "titulo": "Dicionários: pares chave-valor",
            "texto": [
                "Um **dicionário** guarda pares **chave: valor** entre chaves: `alien = {'cor': 'verde', 'pontos': 5}`.",
                "Para ler um valor, use a chave entre colchetes: `alien['cor']` devolve 'verde'.",
                "## Mudando o dicionário",
                "• Adicionar ou mudar um valor: `alien['x'] = 10`.",
                "• Remover um par: `del alien['pontos']`.",
                "• Começar vazio e ir preenchendo: `alien = {}`.",
                "## Chaves que não existem",
                "`alien['velocidade']` dá `KeyError` se a chave não existir. O método `get()` evita o erro e devolve um valor padrão: "
                "`alien.get('velocidade', 'sem velocidade')`.",
            ],
            "exemplo": "alien = {'cor': 'verde', 'pontos': 5}\nprint(alien['cor'])\nprint(f\"Você ganhou {alien['pontos']} pontos!\")\n\n"
                       "alien['x'] = 0\nalien['y'] = 25\nalien['cor'] = 'amarelo'\nprint(alien)\n\n"
                       "del alien['pontos']\nprint(alien.get('pontos', 'Sem pontos definidos.'))",
        },
        {
            "titulo": "Percorrendo dicionários",
            "texto": [
                "`for chave, valor in d.items():` percorre todos os pares.",
                "`for chave in d.keys():` (ou só `for chave in d:`) percorre as chaves, e `d.values()` dá os valores.",
                "`sorted(d.keys())` percorre as chaves em ordem alfabética.",
                "`set(d.values())` remove valores repetidos. Um **set** é uma coleção sem repetição: `{'python', 'c'}`.",
                "`len(d)` diz quantos pares o dicionário tem.",
                "## Dica: juntando textos",
                "`', '.join(lista_de_textos)` junta vários textos separados por vírgula: `', '.join(['a', 'b'])` dá 'a, b'.",
            ],
            "exemplo": "linguagens = {\n    'ana': 'python',\n    'beto': 'c',\n    'carla': 'rust',\n    'davi': 'python',\n}\n"
                       "for nome, ling in linguagens.items():\n    print(f\"{nome.title()} gosta de {ling.title()}.\")\n\n"
                       "for nome in sorted(linguagens.keys()):\n    print(f\"Obrigado por responder, {nome.title()}!\")\n\n"
                       "citadas = sorted(set(linguagens.values()))\nprint('Linguagens citadas: ' + ', '.join(citadas))",
        },
        {
            "titulo": "Aninhamento",
            "texto": [
                "Você pode colocar dicionários dentro de listas, listas dentro de dicionários e até dicionários dentro de dicionários.",
                "• **Lista de dicionários**: vários aliens, cada um com suas informações.",
                "• **Lista dentro de dicionário**: uma pizza com várias coberturas: `{'massa': 'fina', 'coberturas': ['queijo', 'tomate']}`.",
                "• **Dicionário de dicionários**: usuários, cada um com nome, cidade etc.",
                "Evite aninhar demais: se ficar difícil de ler, provavelmente existe um jeito mais simples (como as classes, no capítulo 9).",
            ],
            "exemplo": "aliens = []\nfor numero in range(3):\n    aliens.append({'cor': 'verde', 'pontos': 5})\naliens[0]['cor'] = 'amarelo'\n"
                       "for alien in aliens:\n    print(alien)\n\n"
                       "pizza = {'massa': 'fina', 'coberturas': ['queijo', 'tomate']}\nprint(f\"Pizza de massa {pizza['massa']} com:\")\n"
                       "for c in pizza['coberturas']:\n    print(f\"  - {c}\")\n\n"
                       "usuarios = {\n    'aeinstein': {'nome': 'albert', 'cidade': 'princeton'},\n    'mcurie': {'nome': 'marie', 'cidade': 'paris'},\n}\n"
                       "for login, info in usuarios.items():\n    print(f\"{login}: {info['nome'].title()} mora em {info['cidade'].title()}\")",
        },
    ],
    "quiz": [
        {"pergunta": "O que é mostrado?", "codigo": "alien = {'cor': 'verde', 'pontos': 5}\nprint(alien['pontos'])",
         "opcoes": ["5", "pontos", "verde", "KeyError"], "correta": 0,
         "explicacao": "A chave 'pontos' está ligada ao valor 5."},
        {"pergunta": "O que `d.get('x', 0)` devolve se a chave 'x' não existe?",
         "opcoes": ["KeyError", "None", "0", "'x'"], "correta": 2,
         "explicacao": "get() devolve o valor padrão (o segundo argumento) quando a chave não existe."},
        {"pergunta": "Qual laço percorre chaves e valores ao mesmo tempo?",
         "opcoes": ["for k in d:", "for k, v in d.items():", "for v in d.values():", "for k, v in d:"], "correta": 1,
         "explicacao": "items() devolve os pares (chave, valor)."},
        {"pergunta": "O que acontece?", "codigo": "d = {'a': 1}\nprint(d['b'])",
         "opcoes": ["Mostra None", "Mostra 0", "KeyError", "IndexError"], "correta": 2,
         "explicacao": "Acessar uma chave inexistente com colchetes dá KeyError."},
        {"pergunta": "Quanto vale `len({'a': 1, 'b': 2, 'a': 3})`?",
         "opcoes": ["3", "2", "1", "Erro"], "correta": 1,
         "explicacao": "Chaves são únicas: o segundo 'a' substitui o primeiro. Sobram 2 pares."},
        {"pergunta": "O que `set(['py', 'c', 'py'])` gera?",
         "opcoes": ["['py', 'c', 'py']", "{'py', 'c'}", "('py', 'c')", "Erro"], "correta": 1,
         "explicacao": "Um set guarda cada valor uma única vez."},
        {"pergunta": "Como adicionar a chave 'nivel' com valor 2 ao dicionário `jogador`?",
         "opcoes": ["jogador.append('nivel', 2)", "jogador['nivel'] = 2", "jogador.add(nivel=2)", "jogador + {'nivel': 2}"],
         "correta": 1, "explicacao": "Basta atribuir um valor à nova chave."},
    ],
    "desafios": [
        {
            "titulo": "Ficha pessoal",
            "enunciado": "Crie um dicionário `pessoa` com as chaves 'nome', 'sobrenome', 'idade' e 'cidade'. "
                         "Depois, com um for e .items(), mostre cada informação neste formato:\n\nnome: Ana",
            "inicial": "pessoa = {\n    \n}\n",
            "dica": "for chave, valor in pessoa.items():\n    print(f\"{chave}: {valor}\")",
            "solucao": "pessoa = {\n    'nome': 'Ana',\n    'sobrenome': 'Silva',\n    'idade': 28,\n    'cidade': 'Recife',\n}\n"
                       "for chave, valor in pessoa.items():\n    print(f\"{chave}: {valor}\")",
            "casos": [caso([
                var_existe("pessoa", dict),
                regra(lambda o, n, c: set(n["pessoa"]) == {"nome", "sobrenome", "idade", "cidade"},
                      "O dicionário precisa ter exatamente as chaves nome, sobrenome, idade e cidade."),
                regra(lambda o, n, c: normalizar(o) == "\n".join(f"{k}: {v}" for k, v in n["pessoa"].items()),
                      "Mostre uma linha 'chave: valor' para cada item, na ordem do dicionário."),
                tem(".items()")])],
        },
        {
            "titulo": "Glossário de Python",
            "enunciado": "Crie um dicionário `glossario` com pelo menos 5 termos de Python e seus significados "
                         "(ex.: 'lista': 'coleção ordenada de itens'). Mostre todos em ordem alfabética, um por linha:\n\n"
                         "lista: coleção ordenada de itens",
            "inicial": "glossario = {}\n",
            "dica": "for termo in sorted(glossario):\n    print(f\"{termo}: {glossario[termo]}\")",
            "solucao": "glossario = {\n    'lista': 'coleção ordenada de itens',\n    'tupla': 'lista que não pode mudar',\n"
                       "    'dicionário': 'pares de chave e valor',\n    'for': 'laço que percorre itens',\n"
                       "    'if': 'decide o que fazer',\n}\nfor termo in sorted(glossario):\n    print(f\"{termo}: {glossario[termo]}\")",
            "casos": [caso([
                var_existe("glossario", dict),
                regra(lambda o, n, c: len(n["glossario"]) >= 5, "O glossário precisa de pelo menos 5 termos."),
                regra(lambda o, n, c: normalizar(o) == "\n".join(f"{t}: {n['glossario'][t]}" for t in sorted(n["glossario"])),
                      "Mostre 'termo: significado' para cada termo, em ordem alfabética."),
                tem("sorted(")])],
        },
        {
            "titulo": "Rios do mundo",
            "enunciado": "O dicionário `rios` é fornecido (rio: país). Mostre:\n"
                         "1. Para cada rio: <Rio> passa por <País>.\n"
                         "2. Uma linha com os rios: Rios: Nilo, Amazonas, Yangtzé\n"
                         "3. Uma linha com os países: Países: Egito, Brasil, China\n\n"
                         "Todos os nomes com iniciais maiúsculas.",
            "inicial": "# rios é fornecido. Para testar: {'nilo': 'egito', 'amazonas': 'brasil', 'yangtzé': 'china'}\n\n",
            "dica": "Para as linhas 2 e 3, monte uma lista com os nomes em title() e use ', '.join(lista).",
            "solucao": "for rio, pais in rios.items():\n    print(f\"{rio.title()} passa por {pais.title()}.\")\n\n"
                       "nomes = []\nfor rio in rios.keys():\n    nomes.append(rio.title())\nprint('Rios: ' + ', '.join(nomes))\n\n"
                       "paises = []\nfor pais in rios.values():\n    paises.append(pais.title())\nprint('Países: ' + ', '.join(paises))",
            "casos": [caso([saida(_rios(r))], {"rios": r}) for r in [
                {'nilo': 'egito', 'amazonas': 'brasil', 'yangtzé': 'china'},
                {'são francisco': 'brasil', 'danúbio': 'áustria'}]],
        },
        {
            "titulo": "Contador de palavras",
            "enunciado": "A lista `palavras` é fornecida. Crie o dicionário `contagem` com quantas vezes cada palavra aparece, "
                         "usando o método get(), e mostre o dicionário com print(contagem).",
            "inicial": "# palavras é fornecida. Para testar: ['python', 'é', 'legal', 'python', 'muito', 'legal', 'python']\n\ncontagem = {}\n",
            "dica": "for p in palavras:\n    contagem[p] = contagem.get(p, 0) + 1",
            "solucao": "contagem = {}\nfor p in palavras:\n    contagem[p] = contagem.get(p, 0) + 1\nprint(contagem)",
            "casos": [caso([var_igual("contagem", _contagem(p)), tem(".get("), saida(str(_contagem(p)))], {"palavras": p})
                      for p in [['python', 'é', 'legal', 'python', 'muito', 'legal', 'python'], ['a', 'b', 'a'], []]],
        },
        {
            "titulo": "Caça-bugs: a chave sumida",
            "enunciado": "Este código quebra com KeyError quando o usuário não tem e-mail. Conserte usando get() para mostrar "
                         "'sem e-mail' quando a chave não existir. O verificador também testa um usuário que TEM e-mail.",
            "inicial": "# usuario é fornecido. Para testar: {'nome': 'ana', 'nivel': 3}\nprint(usuario['email'])\n",
            "dica": "usuario.get('email', 'sem e-mail')",
            "solucao": "print(usuario.get('email', 'sem e-mail'))",
            "casos": [caso([saida("sem e-mail"), tem(".get(")], {"usuario": {'nome': 'ana', 'nivel': 3}}),
                      caso([saida("bia@exemplo.com")], {"usuario": {'nome': 'bia', 'email': 'bia@exemplo.com'}})],
        },
    ],
    "chefe": {
        "titulo": "O Oráculo dos Times",
        "enunciado": "A lista `jogadores` (fornecida) tem um dicionário por jogador, com 'nome', 'pontos' e 'time'.\n"
                     "1. Crie o dicionário `pontos_por_time`, somando os pontos de cada time.\n"
                     "2. Mostre cada time em ordem alfabética: azul: 270\n"
                     "3. Mostre o jogador com mais pontos: Campeão: Carla\n\n"
                     "O Oráculo vai testar com times e jogadores diferentes!",
        "inicial": "# jogadores é fornecida. Para testar:\n# [{'nome': 'ana', 'pontos': 120, 'time': 'azul'}, ...]\n\n",
        "dica": "Comece com pontos_por_time = {} e campeao = jogadores[0]. No for, some com get() e troque o campeão quando achar mais pontos.",
        "solucao": "pontos_por_time = {}\ncampeao = jogadores[0]\nfor j in jogadores:\n    time = j['time']\n"
                   "    pontos_por_time[time] = pontos_por_time.get(time, 0) + j['pontos']\n"
                   "    if j['pontos'] > campeao['pontos']:\n        campeao = j\n\n"
                   "for time in sorted(pontos_por_time):\n    print(f\"{time}: {pontos_por_time[time]}\")\n"
                   "print(f\"Campeão: {campeao['nome'].title()}\")",
        "casos": [caso([var_igual("pontos_por_time", _times(j)[0]), saida(_times(j)[1])], {"jogadores": j}) for j in [_JOG1, _JOG2]],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 7: Entrada do usuário e laços while
# ---------------------------------------------------------------------------

def _ingressos(idades):
    out = []
    for i in idades:
        if i == "sair":
            break
        i = int(i)
        out.append("Grátis." if i < 3 else "R$ 10." if i <= 12 else "R$ 15.")
    return "\n".join(out)


def _lanchonete(pedidos):
    restantes = [p for p in pedidos if p != "pastrami"]
    linhas = ["O pastrami acabou."] + [f"Preparei seu sanduíche de {s}." for s in restantes]
    return restantes, "\n".join(linhas)


def _adivinha(segredo, palpites):
    out = []
    t = 0
    for p in palpites:
        if p == "desisto":
            out.append(f"O número era {segredo}.")
            break
        t += 1
        p = int(p)
        if p < segredo:
            out.append("Mais alto!")
        elif p > segredo:
            out.append("Mais baixo!")
        else:
            out.append(f"Acertou! Tentativas: {t}")
            break
    return "\n".join(out)


CAP7 = {
    "num": 7,
    "titulo": "Entrada e laços while",
    "subtitulo": "input(), while, break e continue",
    "licoes": [
        {
            "titulo": "input(): conversando com o usuário",
            "texto": [
                "`input('pergunta')` mostra a pergunta, espera a pessoa digitar e devolve o que ela digitou.",
                "O que vem do input é **sempre texto** (str). Para fazer contas, converta: `idade = int(input('Idade? '))`.",
                "O operador `%` (módulo) dá o resto da divisão: `7 % 2` é 1. Se `n % 2 == 0`, o número é par.",
                "## Como funciona aqui",
                "No PyQuest ninguém digita durante a execução: os exemplos e os testes já trazem as respostas prontas, "
                "que aparecem na saída logo depois de cada pergunta.",
            ],
            "ctx": {"__entradas__": ["Ana", "17"]},
            "exemplo": "nome = input(\"Qual é o seu nome? \")\nidade = int(input(\"Quantos anos você tem? \"))\n"
                       "print(f\"Olá, {nome}! Ano que vem você terá {idade + 1} anos.\")\n\n"
                       "if idade % 2 == 0:\n    print(\"Sua idade é um número par.\")\nelse:\n    print(\"Sua idade é um número ímpar.\")",
        },
        {
            "titulo": "O laço while",
            "texto": [
                "`while condição:` repete o bloco **enquanto** a condição for verdadeira.",
                "Use while quando você não sabe quantas voltas o laço vai dar, como ao ler respostas até a pessoa digitar 'sair'.",
                "`contador += 1` é o mesmo que `contador = contador + 1`.",
                "• `break` sai do laço na hora.",
                "• `continue` pula para a próxima volta.",
                "• Uma **flag** (como `ativo = True`) ajuda a controlar laços com várias formas de parar.",
                "## Cuidado com o laço infinito",
                "Se a condição nunca ficar falsa, o laço não termina. Esqueceu de somar 1 no contador? Laço infinito! "
                "O PyQuest interrompe programas que rodam tempo demais.",
            ],
            "ctx": {"__entradas__": ["oi", "tudo bem?", "sair"]},
            "exemplo": "contador = 1\nwhile contador <= 5:\n    print(contador)\n    contador += 1\n\n"
                       "mensagem = ''\nwhile mensagem != 'sair':\n    mensagem = input(\"Diga algo (ou 'sair'): \")\n"
                       "    if mensagem != 'sair':\n        print(f\"Você disse: {mensagem}\")\n\n"
                       "n = 0\nwhile n < 10:\n    n += 1\n    if n % 2 == 0:\n        continue\n    print(n, 'é ímpar')",
        },
        {
            "titulo": "while com listas e dicionários",
            "texto": [
                "Não modifique uma lista dentro de um `for` que a percorre. Para mover ou apagar itens, use `while`.",
                "• Mover itens: `while pendentes:` com `item = pendentes.pop()` e depois `confirmados.append(item)`.",
                "• Apagar todas as ocorrências: `while 'gato' in pets: pets.remove('gato')`.",
                "• Preencher um dicionário com respostas: leia a pergunta no laço e guarde em `respostas[nome] = resposta`.",
            ],
            "ctx": {"__entradas__": ["Ana", "Japão", "sim", "Beto", "Peru", "nao"]},
            "exemplo": "pendentes = ['ana', 'beto', 'carla']\nconfirmados = []\nwhile pendentes:\n    usuario = pendentes.pop()\n"
                       "    print(f\"Confirmando: {usuario.title()}\")\n    confirmados.append(usuario)\nprint(confirmados)\n\n"
                       "pets = ['gato', 'cachorro', 'gato', 'peixe', 'gato']\nwhile 'gato' in pets:\n    pets.remove('gato')\nprint(pets)\n\n"
                       "respostas = {}\ncontinuar = 'sim'\nwhile continuar == 'sim':\n    nome = input(\"Seu nome: \")\n"
                       "    lugar = input(\"Que lugar você quer conhecer? \")\n    respostas[nome] = lugar\n"
                       "    continuar = input(\"Mais alguém vai responder? (sim/nao) \")\nprint(respostas)",
        },
    ],
    "quiz": [
        {"pergunta": "Qual o tipo do valor devolvido por `input()`?",
         "opcoes": ["int", "str", "float", "Depende do que foi digitado"], "correta": 1,
         "explicacao": "input() sempre devolve texto. Converta com int() ou float() para fazer contas."},
        {"pergunta": "Quanto vale `int('5') + 1`?", "opcoes": ["'51'", "6", "Erro", "'6'"], "correta": 1,
         "explicacao": "int('5') vira o número 5, e 5 + 1 = 6."},
        {"pergunta": "Quanto vale `17 % 5`?", "opcoes": ["3", "2", "3.4", "12"], "correta": 1,
         "explicacao": "17 dividido por 5 dá 3 e sobra 2. O % devolve o resto."},
        {"pergunta": "Quantas linhas são mostradas?", "codigo": "n = 1\nwhile n < 4:\n    print(n)\n    n += 1",
         "opcoes": ["3", "4", "2", "Infinitas"], "correta": 0,
         "explicacao": "Mostra 1, 2 e 3. Quando n vira 4, a condição n < 4 fica falsa."},
        {"pergunta": "O que `break` faz dentro de um laço?",
         "opcoes": ["Pula para a próxima volta", "Sai do laço imediatamente", "Para o programa todo", "Reinicia o laço"],
         "correta": 1, "explicacao": "break encerra o laço. Quem pula para a próxima volta é o continue."},
        {"pergunta": "Por que este laço nunca termina?", "codigo": "x = 1\nwhile x <= 3:\n    print(x)",
         "opcoes": ["Faltam os dois-pontos", "x nunca muda, então x <= 3 é sempre True", "print está errado", "while não aceita <="],
         "correta": 1, "explicacao": "Faltou x += 1 dentro do laço."},
        {"pergunta": "Qual o jeito certo de remover TODAS as ocorrências de 'gato' da lista pets?",
         "opcoes": ["pets.remove('gato')", "while 'gato' in pets: pets.remove('gato')", "del pets['gato']", "pets.pop('gato')"],
         "correta": 1, "explicacao": "remove() apaga só a primeira. O while repete até não sobrar nenhuma."},
    ],
    "desafios": [
        {
            "titulo": "Locadora de carros",
            "enunciado": "Pergunte com input() que carro a pessoa quer alugar e responda:\n\nVou ver se tenho um <carro> disponível.",
            "inicial": "# Use input() para perguntar o carro\n",
            "dica": "carro = input(\"Que carro você quer alugar? \")",
            "solucao": "carro = input(\"Que carro você quer alugar? \")\nprint(f\"Vou ver se tenho um {carro} disponível.\")",
            "casos": [caso([saida(f"Vou ver se tenho um {c} disponível.", flex=True), tem("input(")], entradas(c))
                      for c in ["Fusca", "Uno"]],
        },
        {
            "titulo": "Par ou ímpar",
            "enunciado": "Leia um número inteiro com input() e mostre '<n> é par.' ou '<n> é ímpar.'",
            "inicial": "",
            "dica": "numero = int(input(\"Digite um número: \")) e depois teste numero % 2 == 0.",
            "solucao": "numero = int(input(\"Digite um número: \"))\nif numero % 2 == 0:\n    print(f\"{numero} é par.\")\n"
                       "else:\n    print(f\"{numero} é ímpar.\")",
            "casos": [caso([saida(f"{n} é {'par' if n % 2 == 0 else 'ímpar'}.", flex=True)], entradas(str(n))) for n in [4, 7, 0]],
        },
        {
            "titulo": "Montando a pizza",
            "enunciado": "Peça coberturas com input() repetidamente até a pessoa digitar 'sair'. Para cada cobertura, mostre "
                         "'Adicionando <cobertura>.'. No fim, mostre 'Pizza pronta!'.",
            "inicial": "",
            "dica": "while True: leia a cobertura; se for 'sair', break; senão, mostre a mensagem.",
            "solucao": "while True:\n    cobertura = input(\"Cobertura (ou 'sair'): \")\n    if cobertura == 'sair':\n        break\n"
                       "    print(f\"Adicionando {cobertura}.\")\nprint(\"Pizza pronta!\")",
            "casos": [caso([saida("\n".join([f"Adicionando {x}." for x in e[:-1]] + ["Pizza pronta!"]), flex=True),
                            tem("while")], entradas(*e))
                      for e in [["queijo", "tomate", "sair"], ["sair"], ["bacon", "sair"]]],
        },
        {
            "titulo": "Bilheteria do cinema",
            "enunciado": "Leia idades com input() até a pessoa digitar 'sair'. Para cada idade, mostre o preço:\n"
                         "• menos de 3 anos: Grátis.\n• de 3 a 12 anos: R$ 10.\n• mais de 12 anos: R$ 15.",
            "inicial": "",
            "dica": "Leia como texto, teste se é 'sair' e só depois converta com int().",
            "solucao": "while True:\n    resposta = input(\"Idade (ou 'sair'): \")\n    if resposta == 'sair':\n        break\n"
                       "    idade = int(resposta)\n    if idade < 3:\n        print(\"Grátis.\")\n    elif idade <= 12:\n"
                       "        print(\"R$ 10.\")\n    else:\n        print(\"R$ 15.\")",
            "casos": [caso([saida(_ingressos(e), flex=True)], entradas(*e))
                      for e in [["2", "10", "30", "sair"], ["12", "3", "13", "sair"], ["sair"]]],
        },
        {
            "titulo": "Lanchonete sem pastrami",
            "enunciado": "A lista `pedidos` é fornecida. O pastrami acabou!\n"
                         "1. Mostre 'O pastrami acabou.' e remova TODOS os 'pastrami' de pedidos usando while.\n"
                         "2. Crie a lista `prontos`. Enquanto houver pedidos, tire o PRIMEIRO com pop(0), mostre "
                         "'Preparei seu sanduíche de <s>.' e coloque-o em prontos.",
            "inicial": "# pedidos é fornecida. Para testar: ['misto', 'pastrami', 'atum', 'pastrami', 'queijo']\n\n",
            "dica": "while 'pastrami' in pedidos: ... e depois while pedidos: s = pedidos.pop(0)",
            "solucao": "print(\"O pastrami acabou.\")\nwhile 'pastrami' in pedidos:\n    pedidos.remove('pastrami')\n\n"
                       "prontos = []\nwhile pedidos:\n    s = pedidos.pop(0)\n    print(f\"Preparei seu sanduíche de {s}.\")\n    prontos.append(s)",
            "casos": [caso([var_igual("pedidos", []), var_igual("prontos", _lanchonete(p)[0]), saida(_lanchonete(p)[1]),
                            tem("while")], {"pedidos": p})
                      for p in [['misto', 'pastrami', 'atum', 'pastrami', 'queijo'], ['pastrami', 'frango']]],
        },
        {
            "titulo": "Caça-bugs: o laço sem fim",
            "enunciado": "Este laço deveria mostrar os números de 1 a 5, mas nunca termina. Conserte!",
            "inicial": "contador = 1\nwhile contador <= 5:\n    print(contador)\n",
            "dica": "O contador precisa mudar dentro do laço.",
            "solucao": "contador = 1\nwhile contador <= 5:\n    print(contador)\n    contador += 1",
            "casos": [caso([saida("1\n2\n3\n4\n5")])],
        },
    ],
    "chefe": {
        "titulo": "A Esfinge dos Números",
        "enunciado": "A variável `segredo` (fornecida) guarda um número. Leia palpites com input() até:\n"
                     "• acertar: mostre 'Acertou! Tentativas: <n>' e pare;\n"
                     "• a pessoa digitar 'desisto': mostre 'O número era <segredo>.' e pare.\n"
                     "Para cada palpite errado, mostre 'Mais alto!' (se o palpite for menor que o segredo) ou 'Mais baixo!'.",
        "inicial": "# segredo é fornecido. Para testar: segredo = 42, palpites 50, 30 e 42.\n\n",
        "dica": "tentativas = 0 antes do laço. Dentro: leia, trate 'desisto', converta com int(), some 1 em tentativas e compare.",
        "solucao": "tentativas = 0\nwhile True:\n    palpite = input(\"Seu palpite: \")\n    if palpite == 'desisto':\n"
                   "        print(f\"O número era {segredo}.\")\n        break\n    palpite = int(palpite)\n    tentativas += 1\n"
                   "    if palpite < segredo:\n        print(\"Mais alto!\")\n    elif palpite > segredo:\n        print(\"Mais baixo!\")\n"
                   "    else:\n        print(f\"Acertou! Tentativas: {tentativas}\")\n        break",
        "casos": [caso([saida(_adivinha(s, p), flex=True)], {"segredo": s, "__entradas__": p})
                  for s, p in [(42, ["50", "30", "42"]), (7, ["7"]), (10, ["3", "desisto"]), (5, ["9", "1", "4", "6", "5"])]],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 8: Funções
# ---------------------------------------------------------------------------

CAP8 = {
    "num": 8,
    "titulo": "Funções",
    "subtitulo": "def, argumentos, return, *args e **kwargs",
    "licoes": [
        {
            "titulo": "Definindo funções",
            "texto": [
                "Uma **função** é um bloco de código com nome, que você escreve uma vez e usa quantas vezes quiser.",
                "`def saudar():` define a função, e o bloco indentado é o corpo. Para usar, **chame** a função: `saudar()`.",
                "Um texto com três aspas logo abaixo do def é a **docstring**: ela explica o que a função faz.",
                "## Parâmetros e argumentos",
                "Em `def saudar(nome):`, `nome` é um **parâmetro**. Na chamada `saudar('ana')`, `'ana'` é o **argumento**, "
                "o valor que entra no parâmetro.",
            ],
            "exemplo": "def saudar(nome):\n    \"\"\"Mostra uma saudação simples.\"\"\"\n    print(f\"Olá, {nome.title()}!\")\n\n"
                       "saudar('ana')\nsaudar('beto')",
        },
        {
            "titulo": "Tipos de argumento",
            "texto": [
                "• **Posicionais**: a ordem importa. `descrever_pet('rex', 'cachorro')`.",
                "• **Nomeados**: você diz qual é qual, e a ordem não importa. `descrever_pet(tipo='gato', nome='mimi')`.",
                "• **Valor padrão**: `def descrever_pet(nome, tipo='cachorro'):` deixa o argumento opcional. "
                "Parâmetros com padrão vêm depois dos sem padrão.",
                "Chamar a função com argumentos faltando ou sobrando dá `TypeError`, e a mensagem diz qual argumento faltou.",
            ],
            "exemplo": "def descrever_pet(nome, tipo='cachorro'):\n    print(f\"Tenho um {tipo} chamado {nome.title()}.\")\n\n"
                       "descrever_pet('rex')\ndescrever_pet('mimi', 'gato')\ndescrever_pet(tipo='hamster', nome='bolinha')",
        },
        {
            "titulo": "Devolvendo valores com return",
            "texto": [
                "`return` devolve um valor para quem chamou a função. Assim você guarda o resultado numa variável e usa depois.",
                "Uma função sem return devolve `None`. Um erro comum é usar `print` dentro da função e achar que ela devolveu o valor.",
                "Funções podem devolver qualquer coisa: números, textos, listas e dicionários.",
                "Um parâmetro opcional pode começar vazio, como `meio=''`, e você testa `if meio:` dentro da função.",
            ],
            "exemplo": "def nome_completo(primeiro, ultimo, meio=''):\n    if meio:\n        nome = f\"{primeiro} {meio} {ultimo}\"\n"
                       "    else:\n        nome = f\"{primeiro} {ultimo}\"\n    return nome.title()\n\n"
                       "def criar_pessoa(nome, idade=None):\n    pessoa = {'nome': nome}\n    if idade:\n        pessoa['idade'] = idade\n"
                       "    return pessoa\n\nmusico = nome_completo('jimi', 'hendrix')\nprint(musico)\n"
                       "print(nome_completo('john', 'hooker', 'lee'))\nprint(criar_pessoa('ana', 30))",
        },
        {
            "titulo": "Listas, *args, **kwargs e módulos",
            "texto": [
                "Quando você passa uma lista para uma função, ela pode **modificar** a lista original. "
                "Para proteger o original, passe uma cópia: `funcao(lista[:])`.",
                "`*coberturas` junta qualquer quantidade de argumentos numa tupla: `fazer_pizza(30, 'queijo', 'tomate')`.",
                "`**info` junta argumentos nomeados extras num dicionário: `criar_perfil('ana', cidade='recife')`.",
                "## Módulos",
                "Funções podem ficar em outros arquivos (módulos) e ser importadas: `from math import sqrt` ou `import random`. "
                "Aqui no PyQuest você usa os módulos da biblioteca padrão do Python.",
            ],
            "exemplo": "def fazer_pizza(tamanho, *coberturas):\n    print(f\"Pizza de {tamanho} cm com:\")\n    for c in coberturas:\n"
                       "        print(f\"- {c}\")\n\ndef criar_perfil(nome, **info):\n    info['nome'] = nome\n    return info\n\n"
                       "fazer_pizza(30, 'queijo')\nfazer_pizza(40, 'queijo', 'tomate', 'milho')\n"
                       "print(criar_perfil('ana', cidade='recife', curso='python'))\n\nfrom math import sqrt\nprint(sqrt(81))",
        },
    ],
    "quiz": [
        {"pergunta": "Como se define uma função em Python?",
         "opcoes": ["function saudar():", "def saudar():", "func saudar()", "define saudar:"], "correta": 1,
         "explicacao": "Funções começam com def, o nome, os parênteses e os dois-pontos."},
        {"pergunta": "O que este código mostra?", "codigo": "def dobro(x):\n    return x * 2\n\nprint(dobro(dobro(3)))",
         "opcoes": ["6", "12", "9", "Erro"], "correta": 1,
         "explicacao": "dobro(3) é 6, e dobro(6) é 12."},
        {"pergunta": "Com `def f(nome, idade=10):`, qual chamada dá erro?",
         "opcoes": ["f('ana')", "f('ana', 20)", "f(idade=5, nome='ana')", "f()"], "correta": 3,
         "explicacao": "nome não tem valor padrão, então é obrigatório."},
        {"pergunta": "O que uma função sem return devolve?", "opcoes": ["0", "''", "None", "Erro"], "correta": 2,
         "explicacao": "Sem return, a função devolve None."},
        {"pergunta": "Dentro de `def f(*nums):`, o que é `nums`?",
         "opcoes": ["Uma lista", "Uma tupla", "Um dicionário", "Um número"], "correta": 1,
         "explicacao": "*args junta os argumentos numa tupla."},
        {"pergunta": "E dentro de `def f(**info):`, o que é `info`?",
         "opcoes": ["Uma lista", "Uma tupla", "Um dicionário", "Uma string"], "correta": 2,
         "explicacao": "**kwargs junta os argumentos nomeados num dicionário."},
        {"pergunta": "O que é mostrado?", "codigo": "def add(lista):\n    lista.append(4)\n\nnums = [1, 2, 3]\nadd(nums)\nprint(nums)",
         "opcoes": ["[1, 2, 3]", "[1, 2, 3, 4]", "[4]", "None"], "correta": 1,
         "explicacao": "A função recebe a mesma lista e a modifica."},
    ],
    "desafios": [
        {
            "titulo": "Boas-vindas",
            "enunciado": "Crie a função `boas_vindas(nome)` que DEVOLVE (com return) o texto:\n\nBem-vindo(a), <Nome>!\n\n"
                         "com o nome com iniciais maiúsculas.",
            "inicial": "def boas_vindas(nome):\n    pass\n",
            "dica": "return f\"Bem-vindo(a), {nome.title()}!\"",
            "solucao": "def boas_vindas(nome):\n    return f\"Bem-vindo(a), {nome.title()}!\"",
            "casos": [caso([funcao("boas_vindas"), chama("boas_vindas", ["ana"], "Bem-vindo(a), Ana!"),
                            chama("boas_vindas", ["joão silva"], "Bem-vindo(a), João Silva!"), tem("return")])],
        },
        {
            "titulo": "Fábrica de camisetas",
            "enunciado": "Crie `fazer_camiseta(tamanho='G', mensagem='Eu amo Python')` que devolve:\n\n"
                         "Camiseta <tamanho> com a frase: <mensagem>\n\n"
                         "O verificador vai chamar a função com e sem argumentos, inclusive com argumentos nomeados.",
            "inicial": "def fazer_camiseta():\n    pass\n",
            "dica": "Os valores padrão ficam na própria linha do def: def fazer_camiseta(tamanho='G', mensagem='Eu amo Python'):",
            "solucao": "def fazer_camiseta(tamanho='G', mensagem='Eu amo Python'):\n"
                       "    return f\"Camiseta {tamanho} com a frase: {mensagem}\"",
            "casos": [caso([
                chama("fazer_camiseta", [], "Camiseta G com a frase: Eu amo Python"),
                chama("fazer_camiseta", ["M"], "Camiseta M com a frase: Eu amo Python"),
                chama("fazer_camiseta", [], "Camiseta G com a frase: Olá!", {"mensagem": "Olá!"}),
                chama("fazer_camiseta", ["P", "Código é arte"], "Camiseta P com a frase: Código é arte")])],
        },
        {
            "titulo": "Nome completo",
            "enunciado": "Crie `nome_completo(primeiro, ultimo, meio='')` que devolve o nome com iniciais maiúsculas, "
                         "incluindo o nome do meio só quando ele for informado.\n\n"
                         "nome_completo('john', 'hooker', 'lee') → 'John Lee Hooker'",
            "inicial": "def nome_completo(primeiro, ultimo, meio=''):\n    pass\n",
            "dica": "if meio: monte com os três nomes; senão, com dois. Depois use .title().",
            "solucao": "def nome_completo(primeiro, ultimo, meio=''):\n    if meio:\n        nome = f\"{primeiro} {meio} {ultimo}\"\n"
                       "    else:\n        nome = f\"{primeiro} {ultimo}\"\n    return nome.title()",
            "casos": [caso([chama("nome_completo", ["ada", "lovelace"], "Ada Lovelace"),
                            chama("nome_completo", ["john", "hooker", "lee"], "John Lee Hooker"),
                            chama("nome_completo", ["grace", "hopper"], "Grace Brewster Hopper", {"meio": "brewster"})])],
        },
        {
            "titulo": "Álbum musical",
            "enunciado": "Crie `criar_album(artista, titulo, faixas=None)` que devolve um dicionário com as chaves 'artista' e "
                         "'titulo'. Se `faixas` for informado, inclua também a chave 'faixas'.",
            "inicial": "def criar_album(artista, titulo, faixas=None):\n    pass\n",
            "dica": "album = {'artista': artista, 'titulo': titulo} e depois if faixas: album['faixas'] = faixas",
            "solucao": "def criar_album(artista, titulo, faixas=None):\n    album = {'artista': artista, 'titulo': titulo}\n"
                       "    if faixas:\n        album['faixas'] = faixas\n    return album",
            "casos": [caso([chama("criar_album", ["Gal Costa", "Fa-tal"], {'artista': 'Gal Costa', 'titulo': 'Fa-tal'}),
                            chama("criar_album", ["Tim Maia", "Racional"], {'artista': 'Tim Maia', 'titulo': 'Racional', 'faixas': 9},
                                  {"faixas": 9})])],
        },
        {
            "titulo": "Somador universal",
            "enunciado": "Crie `somar(*numeros)` que devolve a soma de quantos números receber. `somar()` deve devolver 0.",
            "inicial": "def somar():\n    pass\n",
            "dica": "Comece com total = 0 e percorra numeros com for.",
            "solucao": "def somar(*numeros):\n    total = 0\n    for n in numeros:\n        total += n\n    return total",
            "casos": [caso([chama("somar", [], 0), chama("somar", [5], 5), chama("somar", [1, 2, 3], 6),
                            chama("somar", [10, -4, 2.5], 8.5), tem("*")])],
        },
        {
            "titulo": "Caça-bugs: print não é return",
            "enunciado": "Este código quebra com TypeError: a função MOSTRA o dobro, mas não DEVOLVE nada. "
                         "Conserte para que o programa mostre 9.",
            "inicial": "def dobro(n):\n    print(n * 2)\n\nresultado = dobro(4) + 1\nprint(resultado)\n",
            "dica": "Troque o print dentro da função por return.",
            "solucao": "def dobro(n):\n    return n * 2\n\nresultado = dobro(4) + 1\nprint(resultado)",
            "casos": [caso([saida("9"), chama("dobro", [7], 14)])],
        },
    ],
    "chefe": {
        "titulo": "O Mago das Funções",
        "enunciado": "Crie três funções que trabalham juntas:\n"
                     "1. `media(notas)`: devolve a média de uma lista de notas, arredondada com round(valor, 1). Lista vazia devolve 0.\n"
                     "2. `situacao(notas, minima=6)`: devolve 'Aprovado' se a média for maior ou igual a `minima`, senão 'Reprovado'. "
                     "Use a função media!\n"
                     "3. `boletim(nome, *notas)`: devolve, por exemplo, 'Ana: média 7.5 - Aprovado' (nome com inicial maiúscula).",
        "inicial": "def media(notas):\n    pass\n\n\ndef situacao(notas, minima=6):\n    pass\n\n\ndef boletim(nome, *notas):\n    pass\n",
        "dica": "Em boletim, notas é uma tupla: transforme em lista com list(notas) e reaproveite media() e situacao().",
        "solucao": "def media(notas):\n    if not notas:\n        return 0\n    return round(sum(notas) / len(notas), 1)\n\n\n"
                   "def situacao(notas, minima=6):\n    if media(notas) >= minima:\n        return 'Aprovado'\n    return 'Reprovado'\n\n\n"
                   "def boletim(nome, *notas):\n    notas = list(notas)\n    return f\"{nome.title()}: média {media(notas)} - {situacao(notas)}\"",
        "casos": [caso([
            chama("media", [[7, 8]], 7.5), chama("media", [[]], 0), chama("media", [[5, 6, 7]], 6.0),
            chama("media", [[10, 9, 9]], 9.3),
            chama("situacao", [[5, 6]], "Reprovado"), chama("situacao", [[5, 6]], "Aprovado", {"minima": 5}),
            chama("situacao", [[6, 6]], "Aprovado"),
            chama("boletim", ["ana", 7, 8], "Ana: média 7.5 - Aprovado"),
            chama("boletim", ["beto", 3, 4, 5], "Beto: média 4.0 - Reprovado")])],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 9: Classes
# ---------------------------------------------------------------------------

def _teste_usuario(ns):
    u = ns["Usuario"]("ada", "lovelace")
    if u.saudacao() != "Olá, Ada Lovelace!" or u.tentativas_login != 0:
        return False
    u.incrementar_tentativas()
    u.incrementar_tentativas()
    if u.tentativas_login != 2:
        return False
    u.zerar_tentativas()
    return u.tentativas_login == 0


def _teste_clientes(ns):
    r = ns["Restaurante"]("Bom Prato")
    if r.clientes_atendidos != 0:
        return False
    r.atender(10)
    if r.clientes_atendidos != 10:
        return False
    r.definir_clientes(30)
    if r.clientes_atendidos != 30:
        return False
    r.definir_clientes(5)
    if r.clientes_atendidos != 30:
        return False
    r.atender(2)
    return r.clientes_atendidos == 32


def _teste_banco_basico(ns):
    C = ns["ContaBancaria"]
    c = C("ana")
    if c.titular != "ana" or c.saldo != 0:
        return False
    if c.depositar(100) is not True or c.saldo != 100:
        return False
    if c.depositar(0) is not False or c.depositar(-5) is not False or c.saldo != 100:
        return False
    if c.sacar(30) is not True or c.saldo != 70:
        return False
    if c.sacar(500) is not False or c.sacar(-1) is not False or c.saldo != 70:
        return False
    return C("beto", 50).saldo == 50


def _teste_poupanca(ns):
    P = ns["ContaPoupanca"]
    if not issubclass(P, ns["ContaBancaria"]):
        return False
    p = P("carla", 1000)
    if p.taxa != 0.01:
        return False
    p.render()
    if p.saldo != 1010.0:
        return False
    p2 = P("davi", 200, 0.05)
    p2.render()
    p2.render()
    return p2.saldo == 220.5 and p2.sacar(20) is True and p2.saldo == 200.5


CAP9 = {
    "num": 9,
    "titulo": "Classes",
    "subtitulo": "Objetos, atributos, métodos e herança",
    "licoes": [
        {
            "titulo": "Criando uma classe",
            "texto": [
                "Uma **classe** é um molde para criar objetos. Cada objeto criado a partir dela é uma **instância**.",
                "`__init__` é um método especial que roda sempre que você cria uma instância. "
                "O primeiro parâmetro, `self`, é a própria instância.",
                "Atributos com `self.` (como `self.nome = nome`) ficam guardados no objeto e podem ser usados em todos os métodos.",
                "**Métodos** são funções dentro da classe: `def sentar(self):`.",
                "Por convenção, nomes de classes usam MaiúsculasJuntas: `Cachorro`, `CarroEletrico`.",
            ],
            "exemplo": "class Cachorro:\n    \"\"\"Um modelo simples de cachorro.\"\"\"\n\n    def __init__(self, nome, idade):\n"
                       "        self.nome = nome\n        self.idade = idade\n\n    def sentar(self):\n        print(f\"{self.nome} sentou.\")\n\n"
                       "    def rolar(self):\n        print(f\"{self.nome} rolou!\")\n\n\nmeu_cachorro = Cachorro('Rex', 6)\n"
                       "print(f\"Meu cachorro se chama {meu_cachorro.nome} e tem {meu_cachorro.idade} anos.\")\n"
                       "meu_cachorro.sentar()\noutro = Cachorro('Luna', 3)\noutro.rolar()",
        },
        {
            "titulo": "Mudando atributos",
            "texto": [
                "Um atributo pode ter um valor inicial sem vir como parâmetro: `self.km = 0` dentro do `__init__`.",
                "Há três jeitos de mudar um atributo:",
                "• Direto: `meu_carro.km = 23`.",
                "• Com um método que define o valor, como `meu_carro.atualizar_km(23)`. Assim você pode validar, "
                "por exemplo, impedir que o hodômetro volte.",
                "• Com um método que soma: `meu_carro.rodar(100)`.",
            ],
            "exemplo": "class Carro:\n    def __init__(self, marca, modelo, ano):\n        self.marca = marca\n        self.modelo = modelo\n"
                       "        self.ano = ano\n        self.km = 0\n\n    def descricao(self):\n"
                       "        return f\"{self.ano} {self.marca.title()} {self.modelo.title()}\"\n\n"
                       "    def atualizar_km(self, km):\n        if km >= self.km:\n            self.km = km\n        else:\n"
                       "            print(\"Você não pode voltar o hodômetro!\")\n\n    def rodar(self, km):\n        self.km += km\n\n\n"
                       "carro = Carro('fiat', 'uno', 2010)\nprint(carro.descricao())\ncarro.atualizar_km(5000)\ncarro.rodar(120)\n"
                       "print(f\"Rodou {carro.km} km.\")\ncarro.atualizar_km(10)",
        },
        {
            "titulo": "Herança",
            "texto": [
                "Uma classe **filha** herda atributos e métodos de uma classe **mãe**: `class CarroEletrico(Carro):`.",
                "No `__init__` da filha, chame `super().__init__(...)` para rodar o `__init__` da mãe.",
                "A filha pode ter atributos e métodos próprios e também **sobrescrever** métodos da mãe, "
                "criando um método com o mesmo nome.",
                "## Instâncias como atributos",
                "Quando uma classe cresce demais, separe partes em outra classe: `self.bateria = Bateria()`.",
            ],
            "exemplo": "class Carro:\n    def __init__(self, marca, modelo):\n        self.marca = marca\n        self.modelo = modelo\n\n"
                       "    def descricao(self):\n        return f\"{self.marca.title()} {self.modelo.title()}\"\n\n"
                       "    def abastecer(self):\n        print(\"Tanque cheio!\")\n\n\nclass Bateria:\n    def __init__(self, kwh=40):\n"
                       "        self.kwh = kwh\n\n    def autonomia(self):\n        if self.kwh == 40:\n            return 260\n        return 400\n\n\n"
                       "class CarroEletrico(Carro):\n    def __init__(self, marca, modelo):\n        super().__init__(marca, modelo)\n"
                       "        self.bateria = Bateria()\n\n    def abastecer(self):\n        print(\"Carro elétrico não tem tanque!\")\n\n\n"
                       "tesla = CarroEletrico('tesla', 'model 3')\nprint(tesla.descricao())\n"
                       "print(f\"Autonomia: {tesla.bateria.autonomia()} km\")\ntesla.abastecer()",
        },
        {
            "titulo": "A biblioteca padrão",
            "texto": [
                "Python vem com muitos módulos prontos: a **biblioteca padrão**. O módulo `random`, por exemplo, sorteia números e itens.",
                "`from random import randint, choice`: `randint(1, 6)` sorteia um inteiro de 1 a 6 e `choice(lista)` sorteia um item.",
                "Em projetos maiores, cada classe pode ficar em seu próprio arquivo (módulo) e ser importada: `from carro import Carro`.",
                "Os sorteios mudam a cada execução: rode o exemplo várias vezes!",
            ],
            "exemplo": "from random import randint, choice\n\n\nclass Dado:\n    def __init__(self, lados=6):\n        self.lados = lados\n\n"
                       "    def rolar(self):\n        return randint(1, self.lados)\n\n\nd6 = Dado()\nd20 = Dado(20)\n"
                       "print('D6:', [d6.rolar() for _ in range(5)])\nprint('D20:', d20.rolar())\n"
                       "print('Sorteado:', choice(['ana', 'beto', 'carla']))",
        },
    ],
    "quiz": [
        {"pergunta": "Qual método roda automaticamente ao criar uma instância?",
         "opcoes": ["__start__", "__init__", "__new_obj__", "criar()"], "correta": 1,
         "explicacao": "__init__ prepara a instância assim que ela é criada."},
        {"pergunta": "Para que serve o `self`?",
         "opcoes": ["É o nome da classe", "Representa a própria instância", "Só é usado em herança", "Guarda variáveis globais"],
         "correta": 1, "explicacao": "self dá acesso aos atributos e métodos daquela instância."},
        {"pergunta": "O que é mostrado?",
         "codigo": "class Gato:\n    def __init__(self, nome):\n        self.nome = nome\n\ng = Gato('mimi')\nprint(g.nome.title())",
         "opcoes": ["mimi", "Mimi", "Gato", "Erro"], "correta": 1,
         "explicacao": "g.nome é 'mimi', e title() deixa a inicial maiúscula."},
        {"pergunta": "Como declarar que `Eletrico` herda de `Carro`?",
         "opcoes": ["class Eletrico extends Carro:", "class Eletrico(Carro):", "class Eletrico < Carro:", "class Eletrico: Carro"],
         "correta": 1, "explicacao": "A classe mãe vai entre parênteses."},
        {"pergunta": "O que `super().__init__(marca)` faz?",
         "opcoes": ["Cria uma nova classe", "Chama o __init__ da classe mãe", "Apaga a instância", "Importa um módulo"],
         "correta": 1, "explicacao": "super() dá acesso aos métodos da classe mãe."},
        {"pergunta": "Qual o resultado?",
         "codigo": "class Contador:\n    def __init__(self):\n        self.valor = 0\n\n    def somar(self):\n        self.valor += 1\n\n"
                   "c = Contador()\nc.somar()\nc.somar()\nprint(c.valor)",
         "opcoes": ["0", "1", "2", "Erro"], "correta": 2,
         "explicacao": "Cada chamada de somar() soma 1 em self.valor."},
        {"pergunta": "Qual é a convenção de nome para classes?",
         "opcoes": ["carro_eletrico", "CarroEletrico", "CARRO_ELETRICO", "carroeletrico"], "correta": 1,
         "explicacao": "Classes usam MaiúsculasJuntas (CamelCase)."},
    ],
    "desafios": [
        {
            "titulo": "Restaurante",
            "enunciado": "Crie a classe `Restaurante` com:\n"
                         "• __init__(self, nome, cozinha), guardando os dois atributos\n"
                         "• descrever(self): devolve '<nome> serve comida <cozinha>.'\n"
                         "• abrir(self): devolve '<nome> está aberto!'",
            "inicial": "class Restaurante:\n    pass\n",
            "dica": "self.nome = nome e self.cozinha = cozinha no __init__. Os métodos usam return com f-string.",
            "solucao": "class Restaurante:\n    def __init__(self, nome, cozinha):\n        self.nome = nome\n        self.cozinha = cozinha\n\n"
                       "    def descrever(self):\n        return f\"{self.nome} serve comida {self.cozinha}.\"\n\n"
                       "    def abrir(self):\n        return f\"{self.nome} está aberto!\"",
            "casos": [caso([
                classe("Restaurante"),
                regra(lambda o, n, c: n["Restaurante"]("Sabor de Casa", "mineira").cozinha == "mineira",
                      "Guarde os atributos nome e cozinha no __init__."),
                regra(lambda o, n, c: n["Restaurante"]("Sabor de Casa", "mineira").descrever() == "Sabor de Casa serve comida mineira.",
                      "Restaurante('Sabor de Casa', 'mineira').descrever() deveria devolver 'Sabor de Casa serve comida mineira.'"),
                regra(lambda o, n, c: n["Restaurante"]("Kyoto", "japonesa").abrir() == "Kyoto está aberto!",
                      "Restaurante('Kyoto', 'japonesa').abrir() deveria devolver 'Kyoto está aberto!'")])],
        },
        {
            "titulo": "Usuário do sistema",
            "enunciado": "Crie a classe `Usuario` com:\n"
                         "• atributos nome, sobrenome e tentativas_login (começa em 0)\n"
                         "• saudacao(): devolve 'Olá, <Nome> <Sobrenome>!' com iniciais maiúsculas\n"
                         "• incrementar_tentativas(): soma 1 em tentativas_login\n"
                         "• zerar_tentativas(): volta tentativas_login para 0",
            "inicial": "class Usuario:\n    pass\n",
            "dica": "self.tentativas_login = 0 no __init__, sem precisar de parâmetro.",
            "solucao": "class Usuario:\n    def __init__(self, nome, sobrenome):\n        self.nome = nome\n        self.sobrenome = sobrenome\n"
                       "        self.tentativas_login = 0\n\n    def saudacao(self):\n"
                       "        return f\"Olá, {self.nome.title()} {self.sobrenome.title()}!\"\n\n"
                       "    def incrementar_tentativas(self):\n        self.tentativas_login += 1\n\n"
                       "    def zerar_tentativas(self):\n        self.tentativas_login = 0",
            "casos": [caso([classe("Usuario"),
                            regra(lambda o, n, c: _teste_usuario(n),
                                  "Teste: Usuario('ada', 'lovelace') deve saudar com 'Olá, Ada Lovelace!', começar com 0 tentativas, "
                                  "ir para 2 após duas chamadas de incrementar_tentativas() e voltar a 0 com zerar_tentativas().")])],
        },
        {
            "titulo": "Clientes atendidos",
            "enunciado": "Crie a classe `Restaurante(nome)` com o atributo clientes_atendidos começando em 0 e os métodos:\n"
                         "• atender(n): soma n clientes\n"
                         "• definir_clientes(n): define o valor, mas nunca deixa diminuir",
            "inicial": "class Restaurante:\n    pass\n",
            "dica": "Em definir_clientes, só atribua se n >= self.clientes_atendidos.",
            "solucao": "class Restaurante:\n    def __init__(self, nome):\n        self.nome = nome\n        self.clientes_atendidos = 0\n\n"
                       "    def atender(self, n):\n        self.clientes_atendidos += n\n\n    def definir_clientes(self, n):\n"
                       "        if n >= self.clientes_atendidos:\n            self.clientes_atendidos = n",
            "casos": [caso([classe("Restaurante"),
                            regra(lambda o, n, c: _teste_clientes(n),
                                  "Teste: começa em 0; atender(10) → 10; definir_clientes(30) → 30; definir_clientes(5) "
                                  "não pode diminuir (continua 30); atender(2) → 32.")])],
        },
        {
            "titulo": "Sorveteria (herança)",
            "enunciado": "Crie `Sorveteria`, filha de `Restaurante`, com:\n"
                         "• __init__(self, nome, sabores): chame super().__init__ com a cozinha 'gelada' e guarde a lista sabores\n"
                         "• listar_sabores(): devolve, por exemplo, 'Sabores: chocolate, morango'",
            "inicial": "class Restaurante:\n    def __init__(self, nome, cozinha):\n        self.nome = nome\n        self.cozinha = cozinha\n\n"
                       "    def descrever(self):\n        return f\"{self.nome} serve comida {self.cozinha}.\"\n\n\n# Crie a classe Sorveteria abaixo\n",
            "dica": "super().__init__(nome, 'gelada') e depois self.sabores = sabores. Use ', '.join(self.sabores).",
            "solucao": "class Restaurante:\n    def __init__(self, nome, cozinha):\n        self.nome = nome\n        self.cozinha = cozinha\n\n"
                       "    def descrever(self):\n        return f\"{self.nome} serve comida {self.cozinha}.\"\n\n\n"
                       "class Sorveteria(Restaurante):\n    def __init__(self, nome, sabores):\n        super().__init__(nome, 'gelada')\n"
                       "        self.sabores = sabores\n\n    def listar_sabores(self):\n        return 'Sabores: ' + ', '.join(self.sabores)",
            "casos": [caso([
                classe("Sorveteria"),
                regra(lambda o, n, c: issubclass(n["Sorveteria"], n["Restaurante"]), "Sorveteria precisa herdar de Restaurante."),
                regra(lambda o, n, c: n["Sorveteria"]("Gelato", ["chocolate"]).descrever() == "Gelato serve comida gelada.",
                      "Sorveteria('Gelato', [...]).descrever() deveria devolver 'Gelato serve comida gelada.'"),
                regra(lambda o, n, c: n["Sorveteria"]("Gelato", ["chocolate", "morango"]).listar_sabores() == "Sabores: chocolate, morango",
                      "listar_sabores() deveria devolver 'Sabores: chocolate, morango'."),
                tem("super().__init__")])],
        },
        {
            "titulo": "Admin com privilégios",
            "enunciado": "Crie duas classes:\n"
                         "• `Privilegios(lista)`: guarda a lista no atributo privilegios e tem os métodos pode(acao), que devolve "
                         "True ou False, e listar(), que devolve 'Pode: banir usuário, apagar post'\n"
                         "• `Admin(nome)`: guarda o nome e tem o atributo privilegios, uma INSTÂNCIA de Privilegios com "
                         "['banir usuário', 'apagar post']",
            "inicial": "class Privilegios:\n    pass\n\n\nclass Admin:\n    pass\n",
            "dica": "No __init__ do Admin: self.privilegios = Privilegios(['banir usuário', 'apagar post'])",
            "solucao": "class Privilegios:\n    def __init__(self, lista):\n        self.privilegios = lista\n\n    def pode(self, acao):\n"
                       "        return acao in self.privilegios\n\n    def listar(self):\n        return 'Pode: ' + ', '.join(self.privilegios)\n\n\n"
                       "class Admin:\n    def __init__(self, nome):\n        self.nome = nome\n"
                       "        self.privilegios = Privilegios(['banir usuário', 'apagar post'])",
            "casos": [caso([
                classe("Privilegios"), classe("Admin"),
                regra(lambda o, n, c: isinstance(n["Admin"]("ana").privilegios, n["Privilegios"]),
                      "O atributo privilegios do Admin precisa ser uma instância de Privilegios."),
                regra(lambda o, n, c: n["Admin"]("ana").privilegios.pode("apagar post") is True
                      and n["Admin"]("ana").privilegios.pode("voar") is False,
                      "pode('apagar post') deveria dar True e pode('voar') deveria dar False."),
                regra(lambda o, n, c: n["Admin"]("ana").privilegios.listar() == "Pode: banir usuário, apagar post",
                      "listar() deveria devolver 'Pode: banir usuário, apagar post'.")])],
        },
        {
            "titulo": "Caça-bugs: o self esquecido",
            "enunciado": "Este código dá AttributeError. Descubra o que falta e conserte para mostrar 2.",
            "inicial": "class Contador:\n    def __init__(self):\n        valor = 0\n\n    def somar(self):\n        self.valor += 1\n\n\n"
                       "c = Contador()\nc.somar()\nc.somar()\nprint(c.valor)\n",
            "dica": "Uma variável sem self. some quando o __init__ termina.",
            "solucao": "class Contador:\n    def __init__(self):\n        self.valor = 0\n\n    def somar(self):\n        self.valor += 1\n\n\n"
                       "c = Contador()\nc.somar()\nc.somar()\nprint(c.valor)",
            "casos": [caso([saida("2")])],
        },
    ],
    "chefe": {
        "titulo": "O Banco Real",
        "enunciado": "Crie a classe `ContaBancaria`:\n"
                     "• __init__(self, titular, saldo=0)\n"
                     "• depositar(valor): soma ao saldo e devolve True. Valores menores ou iguais a zero são recusados (devolve False).\n"
                     "• sacar(valor): tira do saldo e devolve True. Se o valor for maior que o saldo ou <= 0, recusa e devolve False.\n\n"
                     "Depois crie `ContaPoupanca`, filha de ContaBancaria, com o parâmetro extra `taxa` (padrão 0.01) e o método "
                     "`render()`, que soma ao saldo o valor saldo * taxa e arredonda o saldo com round(..., 2).",
        "inicial": "class ContaBancaria:\n    pass\n\n\nclass ContaPoupanca:\n    pass\n",
        "dica": "ContaPoupanca.__init__(self, titular, saldo=0, taxa=0.01): chame super().__init__(titular, saldo) e guarde self.taxa.",
        "solucao": "class ContaBancaria:\n    def __init__(self, titular, saldo=0):\n        self.titular = titular\n        self.saldo = saldo\n\n"
                   "    def depositar(self, valor):\n        if valor <= 0:\n            return False\n        self.saldo += valor\n        return True\n\n"
                   "    def sacar(self, valor):\n        if valor <= 0 or valor > self.saldo:\n            return False\n"
                   "        self.saldo -= valor\n        return True\n\n\nclass ContaPoupanca(ContaBancaria):\n"
                   "    def __init__(self, titular, saldo=0, taxa=0.01):\n        super().__init__(titular, saldo)\n        self.taxa = taxa\n\n"
                   "    def render(self):\n        self.saldo = round(self.saldo + self.saldo * self.taxa, 2)",
        "casos": [caso([
            classe("ContaBancaria"), classe("ContaPoupanca"),
            regra(lambda o, n, c: _teste_banco_basico(n),
                  "Teste da ContaBancaria: começa com saldo 0 (ou o informado); depositar(100) → True e saldo 100; "
                  "depósitos <= 0 → False; sacar(30) → True e saldo 70; sacar(500) ou sacar(-1) → False sem mudar o saldo."),
            regra(lambda o, n, c: _teste_poupanca(n),
                  "Teste da ContaPoupanca: herda de ContaBancaria; taxa padrão 0.01; com saldo 1000, render() deixa 1010.0; "
                  "com saldo 200 e taxa 0.05, dois render() deixam 220.5.")])],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 10: Arquivos e exceções
# ---------------------------------------------------------------------------

def _diario(texto):
    linhas = texto.splitlines()
    return "\n".join([f"O diário tem {len(linhas)} linhas."] + [f"- {l}" for l in linhas])


def _gatos(arqs):
    out = []
    for nome in ["gatos.txt", "cachorros.txt"]:
        if nome in arqs:
            out.append(arqs[nome].rstrip())
        else:
            out.append(f"Arquivo {nome} não encontrado.")
    return "\n".join(out)


def _arquivista(texto):
    notas = {}
    invalidas = 0
    for linha in texto.splitlines():
        nome, nota = linha.split(",")
        try:
            notas[nome] = float(nota)
        except ValueError:
            invalidas += 1
    media = round(sum(notas.values()) / len(notas), 1)
    aprovados = sorted(n for n, v in notas.items() if v >= 6)
    return {"media": media, "aprovados": aprovados, "invalidas": invalidas}


_NOTAS1 = "ana,8.5\nbeto,dez\ncarla,6\ndavi,4.5\neva,9\nfabio,sete\n"
_NOTAS2 = "gil,5\nhelena,7.5\nigor,x\n"

CAP10 = {
    "num": 10,
    "titulo": "Arquivos e exceções",
    "subtitulo": "pathlib, try/except e json",
    "licoes": [
        {
            "titulo": "Lendo arquivos",
            "texto": [
                "Com o módulo `pathlib`, ler um arquivo de texto é simples: `conteudo = Path('pi.txt').read_text()`.",
                "`read_text()` devolve o arquivo inteiro como uma string. `splitlines()` transforma essa string numa lista de linhas.",
                "Em cada linha, `strip()` remove os espaços das pontas.",
                "## Arquivos no PyQuest",
                "Cada execução ganha uma pasta própria e temporária. Os exemplos e os testes criam os arquivos de que precisam "
                "antes de rodar o seu código.",
            ],
            "ctx": {"__arquivos__": {"pi_digitos.txt": "3.1415926535\n  8979323846\n  2643383279\n"}},
            "exemplo": "from pathlib import Path\n\ncaminho = Path('pi_digitos.txt')\nconteudo = caminho.read_text()\n"
                       "linhas = conteudo.splitlines()\n\npi = ''\nfor linha in linhas:\n    pi += linha.strip()\n\n"
                       "print(pi)\nprint(f\"Tenho {len(pi)} caracteres de pi.\")\nprint('1415' in pi)",
        },
        {
            "titulo": "Escrevendo arquivos",
            "texto": [
                "`Path('arquivo.txt').write_text('conteúdo')` cria o arquivo ou **substitui** todo o conteúdo, se ele já existir.",
                "Só é possível escrever strings. Para números, converta com `str()` ou use f-strings.",
                "Para várias linhas, monte uma string com `\\n` no fim de cada linha e escreva tudo de uma vez.",
                "`Path('arquivo.txt').exists()` diz se o arquivo existe.",
            ],
            "exemplo": "from pathlib import Path\n\nlinhas = ['Eu amo programar.', 'Eu amo criar jogos.']\ntexto = ''\n"
                       "for linha in linhas:\n    texto += linha + '\\n'\n\npath = Path('programacao.txt')\npath.write_text(texto)\n"
                       "print(path.exists())\nprint(path.read_text())",
        },
        {
            "titulo": "Exceções: try e except",
            "texto": [
                "Quando algo dá errado, o Python lança uma **exceção**, como `ZeroDivisionError` ou `FileNotFoundError`. "
                "Se ninguém tratar, o programa para.",
                "Com `try`/`except` você trata o erro e o programa continua:",
                "• O código arriscado vai no `try`.",
                "• O que fazer se der erro vai no `except TipoDoErro:`.",
                "• O `else` roda só quando o `try` deu certo.",
                "Às vezes o melhor é falhar em silêncio: use `pass` dentro do except.",
                "## Erros comuns",
                "`int('abc')` dá `ValueError`. Ler um arquivo que não existe dá `FileNotFoundError`.",
            ],
            "ctx": {"__entradas__": ["10", "0", "10", "4"]},
            "exemplo": "for tentativa in range(2):\n    a = input(\"Primeiro número: \")\n    b = input(\"Segundo número: \")\n"
                       "    try:\n        resultado = int(a) / int(b)\n    except ZeroDivisionError:\n"
                       "        print(\"Não dá para dividir por zero!\")\n    else:\n        print(f\"Resultado: {resultado}\")\n\n"
                       "from pathlib import Path\ntry:\n    Path('nao_existe.txt').read_text()\nexcept FileNotFoundError:\n"
                       "    print(\"Desculpe, o arquivo não existe.\")",
        },
        {
            "titulo": "Guardando dados com json",
            "texto": [
                "O módulo `json` transforma listas e dicionários em texto, e de volta, para você salvar dados em arquivos.",
                "• `json.dumps(dados)` gera o texto; `json.loads(texto)` reconstrói os dados.",
                "• Junto com pathlib: `path.write_text(json.dumps(dados))` e `dados = json.loads(path.read_text())`.",
                "Um uso clássico: lembrar o nome do usuário. Se o arquivo existe, cumprimente; se não, pergunte e salve.",
            ],
            "ctx": {"__entradas__": ["Ana"]},
            "exemplo": "import json\nfrom pathlib import Path\n\nnumeros = [2, 3, 5, 7, 11]\nPath('numeros.json').write_text(json.dumps(numeros))\n"
                       "print(json.loads(Path('numeros.json').read_text()))\n\npath = Path('usuario.json')\nif path.exists():\n"
                       "    nome = json.loads(path.read_text())\n    print(f\"Bem-vindo de volta, {nome}!\")\nelse:\n"
                       "    nome = input(\"Qual é o seu nome? \")\n    path.write_text(json.dumps(nome))\n"
                       "    print(f\"Vou lembrar de você, {nome}!\")",
        },
    ],
    "quiz": [
        {"pergunta": "O que `Path('a.txt').read_text()` devolve?",
         "opcoes": ["Uma lista de linhas", "Uma string com todo o conteúdo", "O número de linhas", "None"], "correta": 1,
         "explicacao": "read_text() devolve o arquivo inteiro como texto. Para ter as linhas, use splitlines()."},
        {"pergunta": "O que `write_text()` faz se o arquivo já existe?",
         "opcoes": ["Dá erro", "Acrescenta no fim", "Substitui todo o conteúdo", "Cria uma cópia"], "correta": 2,
         "explicacao": "write_text() sobrescreve o arquivo inteiro."},
        {"pergunta": "Qual exceção acontece em `int('abc')`?",
         "opcoes": ["TypeError", "ValueError", "NameError", "KeyError"], "correta": 1,
         "explicacao": "O tipo (str) é aceito, mas o valor 'abc' não vira número: ValueError."},
        {"pergunta": "Quando o bloco `else` de um try roda?",
         "opcoes": ["Sempre", "Só quando ocorre erro", "Só quando o try termina sem erro", "Nunca"], "correta": 2,
         "explicacao": "O else é o caminho de sucesso do try."},
        {"pergunta": "O que é mostrado?", "codigo": "try:\n    print(10 / 0)\nexcept ZeroDivisionError:\n    print('ops')",
         "opcoes": ["ops", "Infinity", "ZeroDivisionError", "0"], "correta": 0,
         "explicacao": "A divisão por zero é capturada pelo except."},
        {"pergunta": "Para que serve `json.dumps(dados)`?",
         "opcoes": ["Ler um arquivo", "Transformar dados Python em texto JSON", "Apagar dados", "Converter texto em número"],
         "correta": 1, "explicacao": "dumps gera o texto; loads faz o caminho de volta."},
        {"pergunta": "Ler um arquivo que não existe causa...",
         "opcoes": ["ValueError", "FileNotFoundError", "IndexError", "Nada"], "correta": 1,
         "explicacao": "Use try/except FileNotFoundError para tratar esse caso."},
    ],
    "desafios": [
        {
            "titulo": "Leitor de diário",
            "enunciado": "O arquivo 'diario.txt' já existe na pasta. Leia-o com pathlib e mostre:\n\nO diário tem <n> linhas.\n\n"
                         "e depois cada linha precedida de '- '.",
            "inicial": "from pathlib import Path\n\n",
            "dica": "linhas = Path('diario.txt').read_text().splitlines()",
            "solucao": "from pathlib import Path\n\nlinhas = Path('diario.txt').read_text().splitlines()\n"
                       "print(f\"O diário tem {len(linhas)} linhas.\")\nfor linha in linhas:\n    print(f\"- {linha}\")",
            "casos": [caso([saida(_diario(t))], {"__arquivos__": {"diario.txt": t}}) for t in [
                "Hoje aprendi dicionários.\nAmanhã vou estudar classes.\nPython é demais!\n",
                "Dia 1: comecei o PyQuest.\n"]],
        },
        {
            "titulo": "Livro de visitas",
            "enunciado": "Peça nomes com input() até a pessoa digitar 'sair'. Para cada visitante, mostre 'Obrigado, <nome>!'. "
                         "No fim, grave todos os nomes no arquivo 'visitas.txt', um por linha.",
            "inicial": "from pathlib import Path\n\n",
            "dica": "Guarde os nomes numa lista e depois monte o texto com nome + '\\n' para cada um.",
            "solucao": "from pathlib import Path\n\nnomes = []\nwhile True:\n    nome = input(\"Seu nome (ou 'sair'): \")\n"
                       "    if nome == 'sair':\n        break\n    print(f\"Obrigado, {nome}!\")\n    nomes.append(nome)\n\n"
                       "texto = ''\nfor nome in nomes:\n    texto += nome + '\\n'\nPath('visitas.txt').write_text(texto)",
            "casos": [caso([saida("\n".join(f"Obrigado, {x}!" for x in e[:-1]), flex=True),
                            arquivo_igual("visitas.txt", "\n".join(e[:-1]))], entradas(*e))
                      for e in [["Ana", "Beto", "sair"], ["Carla", "sair"]]],
        },
        {
            "titulo": "Calculadora à prova de erros",
            "enunciado": "Leia dois números com input(). Se os dois forem inteiros válidos, mostre 'Soma: <resultado>'. "
                         "Se algum não for número, mostre 'Digite apenas números!' (use try/except ValueError).",
            "inicial": "",
            "dica": "Coloque as duas conversões com int() dentro do try.",
            "solucao": "a = input(\"Primeiro número: \")\nb = input(\"Segundo número: \")\ntry:\n    soma = int(a) + int(b)\n"
                       "except ValueError:\n    print(\"Digite apenas números!\")\nelse:\n    print(f\"Soma: {soma}\")",
            "casos": [caso([saida(r, flex=True), tem("except")], entradas(a, b)) for a, b, r in [
                ("3", "4", "Soma: 7"), ("3", "abc", "Digite apenas números!"), ("x", "2", "Digite apenas números!"),
                ("-5", "10", "Soma: 5")]],
        },
        {
            "titulo": "Gatos e cachorros",
            "enunciado": "Tente ler os arquivos 'gatos.txt' e 'cachorros.txt', nessa ordem. Para cada um que existir, mostre o "
                         "conteúdo (sem a linha em branco do fim). Se não existir, mostre 'Arquivo <nome> não encontrado.' e continue.",
            "inicial": "from pathlib import Path\n\n",
            "dica": "for nome in ['gatos.txt', 'cachorros.txt']: e um try/except FileNotFoundError dentro do laço.",
            "solucao": "from pathlib import Path\n\nfor nome in ['gatos.txt', 'cachorros.txt']:\n    try:\n"
                       "        conteudo = Path(nome).read_text()\n    except FileNotFoundError:\n"
                       "        print(f\"Arquivo {nome} não encontrado.\")\n    else:\n        print(conteudo.rstrip())",
            "casos": [caso([saida(_gatos(a))], {"__arquivos__": a}) for a in [
                {"gatos.txt": "mimi\nfrajola\n", "cachorros.txt": "rex\nbidu\n"},
                {"cachorros.txt": "pluto\n"}, {}]],
        },
        {
            "titulo": "Número favorito",
            "enunciado": "Peça o número favorito com input(), converta para int e salve no arquivo 'favorito.json' usando "
                         "json.dumps. Depois LEIA o arquivo de volta com json.loads e mostre:\n\nSeu número favorito é <n>.",
            "inicial": "import json\nfrom pathlib import Path\n\n",
            "dica": "path = Path('favorito.json'); path.write_text(json.dumps(numero)); lido = json.loads(path.read_text())",
            "solucao": "import json\nfrom pathlib import Path\n\nnumero = int(input(\"Seu número favorito: \"))\npath = Path('favorito.json')\n"
                       "path.write_text(json.dumps(numero))\n\nlido = json.loads(path.read_text())\n"
                       "print(f\"Seu número favorito é {lido}.\")",
            "casos": [caso([arquivo_json("favorito.json", int(n)), saida(f"Seu número favorito é {n}.", flex=True),
                            tem("json.loads")], entradas(n)) for n in ["7", "42"]],
        },
        {
            "titulo": "Caça-bugs: divisão perigosa",
            "enunciado": "Quando o divisor é 0, este programa quebra. Use try/except para mostrar 'Não dá para dividir por zero.' "
                         "nesse caso. Nos outros, mostre o resultado normalmente.",
            "inicial": "a = int(input(\"Dividendo: \"))\nb = int(input(\"Divisor: \"))\nprint(a / b)\n",
            "dica": "try: print(a / b) except ZeroDivisionError: ...",
            "solucao": "a = int(input(\"Dividendo: \"))\nb = int(input(\"Divisor: \"))\ntry:\n    print(a / b)\n"
                       "except ZeroDivisionError:\n    print(\"Não dá para dividir por zero.\")",
            "casos": [caso([saida("5.0")], entradas("10", "2")),
                      caso([saida("Não dá para dividir por zero.", flex=True), tem("except")], entradas("7", "0"))],
        },
    ],
    "chefe": {
        "titulo": "O Arquivista",
        "enunciado": "O arquivo 'notas.txt' tem uma linha por aluno, no formato nome,nota. Algumas notas estão quebradas (ex.: 'beto,dez').\n"
                     "1. Leia o arquivo. Para separar nome e nota, use nome, nota = linha.split(',').\n"
                     "2. Converta cada nota com float(). Ignore as linhas inválidas, mas conte quantas foram (use try/except).\n"
                     "3. Salve em 'relatorio.json' um dicionário com: 'media' (média das notas válidas, com round(..., 1)), "
                     "'aprovados' (nomes com nota >= 6, em ordem alfabética) e 'invalidas' (quantidade de linhas inválidas).\n"
                     "4. Mostre: Média da turma: <media>",
        "inicial": "import json\nfrom pathlib import Path\n\n",
        "dica": "Guarde as notas válidas num dicionário {nome: nota}. Depois calcule a média com sum(...) / len(...).",
        "solucao": "import json\nfrom pathlib import Path\n\nnotas = {}\ninvalidas = 0\nfor linha in Path('notas.txt').read_text().splitlines():\n"
                   "    nome, nota = linha.split(',')\n    try:\n        notas[nome] = float(nota)\n    except ValueError:\n"
                   "        invalidas += 1\n\nmedia = round(sum(notas.values()) / len(notas), 1)\naprovados = []\n"
                   "for nome, nota in notas.items():\n    if nota >= 6:\n        aprovados.append(nome)\naprovados.sort()\n\n"
                   "relatorio = {'media': media, 'aprovados': aprovados, 'invalidas': invalidas}\n"
                   "Path('relatorio.json').write_text(json.dumps(relatorio))\nprint(f\"Média da turma: {media}\")",
        "casos": [caso([arquivo_json("relatorio.json", _arquivista(t)), saida(f"Média da turma: {_arquivista(t)['media']}", flex=True),
                        tem("except")], {"__arquivos__": {"notas.txt": t}}) for t in [_NOTAS1, _NOTAS2]],
    },
}

# ---------------------------------------------------------------------------
# CAPÍTULO 11: Testando o código
# ---------------------------------------------------------------------------

class _FuncPadraoErrado:
    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def dar_aumento(self, valor=50):
        self.salario += valor


class _FuncIgnoraValor:
    def __init__(self, nome, salario):
        self.nome = nome
        self.salario = salario

    def dar_aumento(self, valor=500):
        self.salario += 500


def _senha_ref(senha, ignorar=None):
    problemas = []
    if len(senha) < 8 and ignorar != "curta":
        problemas.append("curta")
    if not any(c.isdigit() for c in senha) and ignorar != "numero":
        problemas.append("sem número")
    if not any(c.isupper() for c in senha) and ignorar != "maiuscula":
        problemas.append("sem maiúscula")
    return problemas


CAP11 = {
    "num": 11,
    "titulo": "Testando o código",
    "subtitulo": "assert, funções de teste e pytest",
    "licoes": [
        {
            "titulo": "Por que testar?",
            "texto": [
                "Testes automáticos conferem se o seu código faz o que deveria. Quando você muda algo, eles avisam se "
                "quebrou o que já funcionava.",
                "O jeito mais simples de testar é o `assert`: `assert condição`. Se a condição for falsa, o Python lança `AssertionError`.",
                "Um bom teste chama o código com uma entrada conhecida e confere o resultado: `assert dobro(4) == 8`.",
            ],
            "exemplo": "def formatar_nome(primeiro, ultimo):\n    return f\"{primeiro} {ultimo}\".title()\n\n"
                       "assert formatar_nome('janis', 'joplin') == 'Janis Joplin'\nprint(\"Primeiro teste passou!\")\n\n"
                       "assert formatar_nome('ada', 'lovelace') == 'Ada lovelace'\nprint(\"Esta linha nunca aparece.\")",
        },
        {
            "titulo": "Funções de teste e pytest",
            "texto": [
                "Os testes ficam organizados em funções cujo nome começa com `test_`. Cada função testa um comportamento.",
                "No seu computador, a ferramenta **pytest** encontra e roda essas funções sozinha: instale com `pip install pytest`, "
                "salve os testes num arquivo como `test_nomes.py` e rode `pytest` no terminal.",
                "Aqui no PyQuest, o verificador faz o papel do pytest: ele roda todas as suas funções `test_...` e ainda tenta "
                "enganá-las com versões do código que têm bugs, para ver se os seus testes percebem!",
                "## Teste que falha também ajuda",
                "Quando um teste falha, leia a mensagem: ela mostra o que era esperado. Conserte o **código**, "
                "a menos que o próprio teste esteja errado.",
            ],
            "exemplo": "def formatar_nome(primeiro, ultimo, meio=''):\n    if meio:\n        completo = f\"{primeiro} {meio} {ultimo}\"\n"
                       "    else:\n        completo = f\"{primeiro} {ultimo}\"\n    return completo.title()\n\n\n"
                       "def test_primeiro_ultimo():\n    assert formatar_nome('janis', 'joplin') == 'Janis Joplin'\n\n\n"
                       "def test_com_nome_do_meio():\n    assert formatar_nome('wolfgang', 'mozart', 'amadeus') == 'Wolfgang Amadeus Mozart'\n\n\n"
                       "# Rodando os testes \"na mão\", como o pytest faria:\ntest_primeiro_ultimo()\ntest_com_nome_do_meio()\n"
                       "print(\"2 testes passaram!\")",
        },
        {
            "titulo": "Testando classes",
            "texto": [
                "Para testar uma classe, crie uma instância e confira os atributos e os resultados dos métodos.",
                "Quando vários testes precisam do mesmo objeto, o pytest oferece **fixtures**: uma função marcada com "
                "`@pytest.fixture` que cria o objeto e é passada aos testes como parâmetro. Aqui você pode simplesmente "
                "criar o objeto dentro de cada teste.",
                "Teste também os **casos-limite**: lista vazia, zero, valores negativos. É onde os bugs se escondem!",
            ],
            "exemplo": "class Pesquisa:\n    def __init__(self, pergunta):\n        self.pergunta = pergunta\n        self.respostas = []\n\n"
                       "    def guardar(self, resposta):\n        self.respostas.append(resposta)\n\n\n"
                       "def test_guarda_uma_resposta():\n    p = Pesquisa('Qual sua linguagem favorita?')\n    p.guardar('python')\n"
                       "    assert 'python' in p.respostas\n\n\ndef test_guarda_tres_respostas():\n"
                       "    p = Pesquisa('Qual sua linguagem favorita?')\n    for r in ['python', 'c', 'rust']:\n        p.guardar(r)\n"
                       "    assert len(p.respostas) == 3\n\n\ntest_guarda_uma_resposta()\ntest_guarda_tres_respostas()\n"
                       "print(\"Pesquisa testada com sucesso!\")",
        },
    ],
    "quiz": [
        {"pergunta": "O que acontece quando um `assert` falha?",
         "opcoes": ["Nada", "O Python lança AssertionError", "Mostra False e continua", "O arquivo é apagado"], "correta": 1,
         "explicacao": "Um assert falso interrompe o programa com AssertionError."},
        {"pergunta": "Como o pytest reconhece uma função de teste?",
         "opcoes": ["Pelo nome começando com test_", "Por ter assert", "Por estar no fim do arquivo", "Por ter return True"],
         "correta": 0, "explicacao": "O pytest procura funções (e arquivos) cujo nome começa com test_."},
        {"pergunta": "Qual é um bom teste para `dobro(n)`?",
         "opcoes": ["assert dobro", "assert dobro(4) == 8", "print(dobro(4))", "dobro(4) == 8 (sem assert)"], "correta": 1,
         "explicacao": "O teste chama a função com uma entrada conhecida e confere o resultado com assert."},
        {"pergunta": "Um teste falhou. O que fazer primeiro?",
         "opcoes": ["Apagar o teste", "Ler a mensagem e descobrir se o erro está no código ou no teste",
                    "Rodar de novo até passar", "Trocar assert por print"], "correta": 1,
         "explicacao": "A mensagem de falha mostra o que era esperado e o que veio."},
        {"pergunta": "Para que serve uma fixture no pytest?",
         "opcoes": ["Criar objetos reutilizáveis pelos testes", "Corrigir bugs sozinha", "Instalar o pytest", "Mostrar gráficos"],
         "correta": 0, "explicacao": "Fixtures preparam dados ou objetos usados por vários testes."},
        {"pergunta": "Qual comando roda os testes no terminal?",
         "opcoes": ["python test", "pytest", "run tests", "pip test"], "correta": 1,
         "explicacao": "Com o pytest instalado, basta rodar pytest na pasta do projeto."},
        {"pergunta": "Por que testar casos-limite (lista vazia, zero...)?",
         "opcoes": ["Porque é obrigatório", "Porque é onde os bugs costumam se esconder", "Para o código ficar mais rápido", "Não é recomendado"],
         "correta": 1, "explicacao": "Os extremos costumam revelar erros que os casos comuns escondem."},
    ],
    "desafios": [
        {
            "titulo": "Primeiro teste",
            "enunciado": "A função `cidade_pais` já está pronta. Escreva a função de teste `test_cidade_pais()` que confere, com "
                         "assert, que cidade_pais('santiago', 'chile') devolve 'Santiago, Chile'.\n\n"
                         "O verificador vai trocar a função por versões com bug para ver se o seu teste percebe!",
            "inicial": "def cidade_pais(cidade, pais):\n    return f\"{cidade}, {pais}\".title()\n\n\n# Escreva seu teste abaixo\n",
            "dica": "def test_cidade_pais():\n    assert cidade_pais('santiago', 'chile') == 'Santiago, Chile'",
            "solucao": "def cidade_pais(cidade, pais):\n    return f\"{cidade}, {pais}\".title()\n\n\n"
                       "def test_cidade_pais():\n    assert cidade_pais('santiago', 'chile') == 'Santiago, Chile'",
            "casos": [caso([
                min_testes(1), testes_passam(),
                testes_pegam("cidade_pais", lambda c, p: f"{c}, {p}", "a função esqueceu das maiúsculas"),
                testes_pegam("cidade_pais", lambda c, p: f"{p}, {c}".title(), "a função trocou a ordem de cidade e país")])],
        },
        {
            "titulo": "Testando a população",
            "enunciado": "Melhore `cidade_pais(cidade, pais, populacao=None)`: quando a população for informada, ela devolve "
                         "'Santiago, Chile - população 5000000'. Depois escreva dois testes:\n"
                         "• test_cidade_pais (sem população)\n• test_cidade_pais_populacao (com população)",
            "inicial": "def cidade_pais(cidade, pais):\n    return f\"{cidade}, {pais}\".title()\n\n\n# Escreva seus testes abaixo\n",
            "dica": "Monte o texto com title() e, se populacao, acrescente f\" - população {populacao}\".",
            "solucao": "def cidade_pais(cidade, pais, populacao=None):\n    texto = f\"{cidade}, {pais}\".title()\n    if populacao:\n"
                       "        texto += f\" - população {populacao}\"\n    return texto\n\n\n"
                       "def test_cidade_pais():\n    assert cidade_pais('santiago', 'chile') == 'Santiago, Chile'\n\n\n"
                       "def test_cidade_pais_populacao():\n"
                       "    assert cidade_pais('santiago', 'chile', 5000000) == 'Santiago, Chile - população 5000000'",
            "casos": [caso([
                chama("cidade_pais", ["lima", "peru"], "Lima, Peru"),
                chama("cidade_pais", ["lima", "peru", 10000000], "Lima, Peru - população 10000000"),
                regra(lambda o, n, c: callable(n.get("test_cidade_pais")) and callable(n.get("test_cidade_pais_populacao")),
                      "Escreva as funções test_cidade_pais e test_cidade_pais_populacao."),
                testes_passam(),
                testes_pegam("cidade_pais", lambda c, p, populacao=None: f"{c}, {p}".title(), "a população foi ignorada"),
                testes_pegam("cidade_pais", lambda c, p, populacao=None: f"{c}, {p}".title() + (f" ({populacao})" if populacao else ""),
                             "a população saiu no formato errado")])],
        },
        {
            "titulo": "Os testes acusam",
            "enunciado": "A função `eh_bissexto(ano)` tem um bug, e os testes mostram isso. Rode, leia o erro e conserte a FUNÇÃO "
                         "(não mexa nos testes).\n\nRegra: um ano é bissexto se for divisível por 4, exceto os divisíveis por 100, "
                         "a não ser que também sejam divisíveis por 400.",
            "inicial": "def eh_bissexto(ano):\n    return ano % 4 == 0\n\n\ndef test_comum():\n    assert eh_bissexto(2023) == False\n\n\n"
                       "def test_divisivel_por_4():\n    assert eh_bissexto(2024) == True\n\n\ndef test_seculo():\n"
                       "    assert eh_bissexto(1900) == False\n\n\ndef test_divisivel_por_400():\n    assert eh_bissexto(2000) == True\n\n\n"
                       "test_comum()\ntest_divisivel_por_4()\ntest_seculo()\ntest_divisivel_por_400()\nprint(\"Todos os testes passaram!\")\n",
            "dica": "Divisível por 400 → True. Senão, divisível por 100 → False. Senão, divisível por 4 → True.",
            "solucao": "def eh_bissexto(ano):\n    if ano % 400 == 0:\n        return True\n    if ano % 100 == 0:\n        return False\n"
                       "    return ano % 4 == 0\n\n\ndef test_comum():\n    assert eh_bissexto(2023) == False\n\n\n"
                       "def test_divisivel_por_4():\n    assert eh_bissexto(2024) == True\n\n\ndef test_seculo():\n"
                       "    assert eh_bissexto(1900) == False\n\n\ndef test_divisivel_por_400():\n    assert eh_bissexto(2000) == True\n\n\n"
                       "test_comum()\ntest_divisivel_por_4()\ntest_seculo()\ntest_divisivel_por_400()\nprint(\"Todos os testes passaram!\")",
            "casos": [caso([saida("Todos os testes passaram!"), min_testes(4),
                            chama("eh_bissexto", [2100], False), chama("eh_bissexto", [2400], True),
                            chama("eh_bissexto", [1996], True), chama("eh_bissexto", [2019], False)])],
        },
        {
            "titulo": "Testando o funcionário",
            "enunciado": "A classe `Funcionario` já existe. Escreva dois testes:\n"
                         "• test_aumento_padrao: um funcionário com salário 3000 recebe dar_aumento() e fica com 3500\n"
                         "• test_aumento_personalizado: com salário 3000, dar_aumento(1000) deixa 4000",
            "inicial": "class Funcionario:\n    def __init__(self, nome, salario):\n        self.nome = nome\n        self.salario = salario\n\n"
                       "    def dar_aumento(self, valor=500):\n        self.salario += valor\n\n\n# Escreva seus testes abaixo\n",
            "dica": "Dentro do teste: f = Funcionario('ana', 3000); f.dar_aumento(); assert f.salario == 3500",
            "solucao": "class Funcionario:\n    def __init__(self, nome, salario):\n        self.nome = nome\n        self.salario = salario\n\n"
                       "    def dar_aumento(self, valor=500):\n        self.salario += valor\n\n\n"
                       "def test_aumento_padrao():\n    f = Funcionario('ana', 3000)\n    f.dar_aumento()\n    assert f.salario == 3500\n\n\n"
                       "def test_aumento_personalizado():\n    f = Funcionario('beto', 3000)\n    f.dar_aumento(1000)\n    assert f.salario == 4000",
            "casos": [caso([min_testes(2), testes_passam(),
                            testes_pegam("Funcionario", _FuncPadraoErrado, "o aumento padrão estava errado"),
                            testes_pegam("Funcionario", _FuncIgnoraValor, "o valor do aumento personalizado era ignorado")])],
        },
        {
            "titulo": "Caça-bugs: o teste errado",
            "enunciado": "Aqui a FUNÇÃO está certa, mas o TESTE está errado e falha. Conserte o teste para conferir o "
                         "comportamento correto: media([2, 4, 9]) é 5.0.",
            "inicial": "def media(numeros):\n    return sum(numeros) / len(numeros)\n\n\ndef test_media():\n"
                       "    assert media([2, 4, 9]) == 15\n\n\ntest_media()\nprint(\"Teste passou!\")\n",
            "dica": "Calcule de cabeça: (2 + 4 + 9) / 3.",
            "solucao": "def media(numeros):\n    return sum(numeros) / len(numeros)\n\n\ndef test_media():\n"
                       "    assert media([2, 4, 9]) == 5.0\n\n\ntest_media()\nprint(\"Teste passou!\")",
            "casos": [caso([saida("Teste passou!"), testes_passam(), chama("media", [[2, 4, 9]], 5.0,
                                                                          msg="Não mude a função media: ela já estava certa."),
                            testes_pegam("media", lambda nums: sum(nums), "a função esqueceu de dividir")])],
        },
    ],
    "chefe": {
        "titulo": "O Juiz dos Testes",
        "enunciado": "Crie `validar_senha(senha)` que devolve uma LISTA com os problemas encontrados, nesta ordem "
                     "(lista vazia = senha boa):\n"
                     "• 'curta' se tiver menos de 8 caracteres\n"
                     "• 'sem número' se não tiver nenhum dígito\n"
                     "• 'sem maiúscula' se não tiver nenhuma letra maiúscula\n\n"
                     "Depois escreva pelo menos 3 testes test_... O Juiz vai rodar os seus testes contra 3 versões com bug, "
                     "e eles precisam pegar todas!",
        "inicial": "def validar_senha(senha):\n    pass\n\n\n# Escreva seus testes abaixo\n",
        "dica": "Percorra a senha com for: c.isdigit() diz se é número e c.isupper() se é maiúscula. "
                "Faça um teste para cada regra.",
        "solucao": "def validar_senha(senha):\n    problemas = []\n    if len(senha) < 8:\n        problemas.append('curta')\n"
                   "    tem_numero = False\n    tem_maiuscula = False\n    for c in senha:\n        if c.isdigit():\n"
                   "            tem_numero = True\n        if c.isupper():\n            tem_maiuscula = True\n    if not tem_numero:\n"
                   "        problemas.append('sem número')\n    if not tem_maiuscula:\n        problemas.append('sem maiúscula')\n"
                   "    return problemas\n\n\ndef test_senha_boa():\n    assert validar_senha('Python2026') == []\n\n\n"
                   "def test_senha_curta():\n    assert validar_senha('Py1') == ['curta']\n\n\n"
                   "def test_sem_numero():\n    assert validar_senha('PythonLegal') == ['sem número']\n\n\n"
                   "def test_sem_maiuscula():\n    assert validar_senha('python2026') == ['sem maiúscula']",
        "casos": [caso([
            chama("validar_senha", ["Python2026"], []),
            chama("validar_senha", ["abc"], ["curta", "sem número", "sem maiúscula"]),
            chama("validar_senha", ["SenhaForte"], ["sem número"]),
            chama("validar_senha", ["Ab1"], ["curta"]),
            chama("validar_senha", ["12345678"], ["sem maiúscula"]),
            min_testes(3), testes_passam(),
            testes_pegam("validar_senha", lambda s: _senha_ref(s, "curta"), "a versão com bug não checava o tamanho"),
            testes_pegam("validar_senha", lambda s: _senha_ref(s, "numero"), "a versão com bug não checava os números"),
            testes_pegam("validar_senha", lambda s: _senha_ref(s, "maiuscula"), "a versão com bug não checava as maiúsculas")])],
    },
}

CAPITULOS = [CAP1, CAP2, CAP3, CAP4, CAP5, CAP6, CAP7, CAP8, CAP9, CAP10, CAP11]
