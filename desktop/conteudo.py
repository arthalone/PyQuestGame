# -*- coding: utf-8 -*-
"""
Conteúdo do PyQuest: lições, quizzes e desafios dos capítulos 1 a 5,
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

CAPITULOS = [CAP1, CAP2, CAP3, CAP4, CAP5]
