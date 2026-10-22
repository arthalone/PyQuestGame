# -*- coding: utf-8 -*-
"""
Conteúdo do PyQuest: lições, quizzes e desafios dos capítulos 1 a 17,
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

# ---------------------------------------------------------------------------
# PARTE II: PROJETO ALIEN INVASION (capítulos 12 a 14)
# Usa o "pygame de treino" do motor: Rect, Sprite, Group, eventos e constantes,
# sem janela. O aluno pratica a lógica; no PC, o mesmo código roda no pygame real.
# ---------------------------------------------------------------------------

def _c(s):
    """Tira a quebra de linha do começo e do fim de um bloco de código."""
    return s.strip("\n")


def _pg():
    import sys
    return sys.modules["pygame"]


def _ev(tipo, tecla):
    pg = _pg()
    return pg.event.Event(getattr(pg, tipo), key=getattr(pg, tecla))


def _sprite_simples(x, y, w=10, h=10):
    pg = _pg()

    class Coisa(pg.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.rect = pg.Rect(x, y, w, h)
    return Coisa()


class _Cfg:
    """Objeto de configurações genérico usado nos testes."""

    def __init__(self, **k):
        self.__dict__.update(k)


# ----------------------------- testes do cap. 12 -----------------------------

_SETTINGS_12 = {
    "screen_width": 1200, "screen_height": 800, "bg_color": (230, 230, 230),
    "ship_speed": 1.5, "bullet_speed": 2.0, "bullet_width": 3, "bullet_height": 15,
    "bullet_color": (60, 60, 60), "bullets_allowed": 3,
}


def _teste_settings(ns):
    s = ns["Settings"]()
    return all(getattr(s, k, None) == v for k, v in _SETTINGS_12.items())


def _teste_posicionar(ns):
    R = _pg().Rect
    f = ns["posicionar_nave"]
    a = R(0, 0, 60, 48)
    r1 = f(R(0, 0, 1200, 800), a)
    b = R(5, 5, 40, 30)
    r2 = f(R(0, 0, 800, 600), b)
    return (a.topleft == (570, 752) and r1 is a and b.topleft == (380, 570) and r2 is b)


def _teste_foguete(ns):
    R = _pg().Rect
    tela = R(0, 0, 300, 200)
    n = ns["Ship"](_Cfg(ship_speed=2.5), tela)
    if n.rect.size != (60, 48) or n.rect.midbottom != (150, 200):
        return False
    if any(getattr(n, f, None) is not False for f in ("moving_right", "moving_left", "moving_up", "moving_down")):
        return False
    n.update()
    if n.rect.topleft != (120, 152):
        return False
    n.moving_up = True
    for _ in range(4):
        n.update()
    if n.rect.y != 142 or n.y != 142.0:
        return False
    for _ in range(200):
        n.update()
    if n.rect.top < -3 or n.rect.top > 0:
        return False
    n.moving_up = False
    n.moving_right = True
    for _ in range(200):
        n.update()
    if n.rect.right < 300 or n.rect.right > 303:
        return False
    n.moving_right = False
    n.moving_down = True
    for _ in range(200):
        n.update()
    if n.rect.bottom < 200 or n.rect.bottom > 203:
        return False
    n.moving_down = False
    n.moving_left = True
    for _ in range(300):
        n.update()
    return -3 <= n.rect.left <= 0


def _teste_teclas(ns):
    f, Nave = ns["checar_teclas"], ns["Nave"]
    n = Nave()
    f(_ev("KEYDOWN", "K_RIGHT"), n)
    if n.moving_right is not True or n.moving_left is not False:
        return False
    f(_ev("KEYDOWN", "K_LEFT"), n)
    if n.moving_left is not True:
        return False
    f(_ev("KEYUP", "K_RIGHT"), n)
    if n.moving_right is not False or n.moving_left is not True:
        return False
    f(_ev("KEYUP", "K_LEFT"), n)
    if n.moving_left is not False:
        return False
    f(_ev("KEYDOWN", "K_SPACE"), n)
    return n.moving_right is False and n.moving_left is False


def _teste_bala(ns):
    pg = _pg()
    B = ns["Bullet"]
    if not issubclass(B, pg.sprite.Sprite):
        return False
    cfg = _Cfg(bullet_width=3, bullet_height=15, bullet_speed=2.0)
    b = B(cfg, pg.Rect(570, 752, 60, 48))
    if b.rect.size != (3, 15) or b.rect.midtop != (600, 752):
        return False
    g = pg.sprite.Group(b)
    g.update()
    g.update()
    if b.rect.y != 748 or b.y != 748.0:
        return False
    b2 = B(_Cfg(bullet_width=5, bullet_height=10, bullet_speed=0.5), pg.Rect(0, 100, 20, 20))
    for _ in range(3):
        b2.update()
    return b2.rect.size == (5, 10) and b2.rect.midtop == (10, 98) and b2.y == 98.5


def _teste_hangar(ns):
    pg = _pg()
    disparar, atualizar = ns["disparar"], ns["atualizar_balas"]
    cfg = ns["Settings"]()
    nave = pg.Rect(570, 752, 60, 48)
    balas = pg.sprite.Group()
    res = [disparar(balas, cfg, nave) for _ in range(5)]
    if res != [True, True, True, False, False] or len(balas) != 3:
        return False
    for _ in range(100):
        atualizar(balas)
    if len(balas) != 3:
        return False
    for _ in range(300):
        atualizar(balas)
    if len(balas) != 0:
        return False
    if disparar(balas, cfg, nave) is not True or len(balas) != 1:
        return False
    # bala que acabou de sair pelo topo some, as outras ficam
    b = next(iter(balas))
    b.y = -14.0
    b.rect.y = -14
    disparar(balas, cfg, nave)
    atualizar(balas)
    return len(balas) == 1


# ----------------------------- testes do cap. 13 -----------------------------

def _frota_ref(lt, at, la, aa):
    pos = []
    x, y = la, aa
    while y < at - 3 * aa:
        while x < lt - 2 * la:
            pos.append((x, y))
            x += 2 * la
        x = la
        y += 2 * aa
    return pos


def _teste_frota(ns):
    f = ns["posicoes_frota"]
    for args in [(600, 400, 60, 50), (1200, 800, 60, 58), (500, 300, 100, 40), (200, 200, 90, 60)]:
        r = f(*args)
        if [tuple(p) for p in (r or [])] != _frota_ref(*args):
            return False
    return True


def _teste_bordas(ns):
    pg = _pg()
    A = ns["Alien"]
    tela = pg.Rect(0, 0, 400, 300)
    a = A(100, 20)
    if not isinstance(a, pg.sprite.Sprite) or a.rect.topleft != (100, 20) or a.rect.size != (60, 50):
        return False
    if a.x != 100.0 or a.check_edges(tela) is not False:
        return False
    return (A(340, 0).check_edges(tela) is True and A(0, 0).check_edges(tela) is True
            and A(339, 0).check_edges(tela) is False and A(1, 0).check_edges(tela) is False
            and A(350, 0).check_edges(tela) is True)


def _teste_meia_volta(ns):
    pg = _pg()
    f = ns["mudar_direcao"]
    cfg = _Cfg(fleet_drop_speed=10, fleet_direction=1)
    aliens = pg.sprite.Group(_sprite_simples(0, 50), _sprite_simples(100, 50), _sprite_simples(0, 150))
    f(aliens, cfg)
    if cfg.fleet_direction != -1 or sorted(a.rect.y for a in aliens) != [60, 60, 160]:
        return False
    cfg.fleet_drop_speed = 25
    f(aliens, cfg)
    return cfg.fleet_direction == 1 and sorted(a.rect.y for a in aliens) == [85, 85, 185]


def _teste_colisoes(ns):
    pg = _pg()
    f = ns["checar_colisoes"]
    balas = pg.sprite.Group(_sprite_simples(10, 10, 3, 15), _sprite_simples(500, 500, 3, 15),
                            _sprite_simples(205, 100, 3, 15))
    aliens = pg.sprite.Group(_sprite_simples(0, 0, 60, 50), _sprite_simples(200, 100, 60, 50),
                             _sprite_simples(150, 90, 60, 50), _sprite_simples(800, 0, 60, 50))
    n = f(balas, aliens)
    if n != 3 or len(balas) != 1 or len(aliens) != 1:
        return False
    return f(pg.sprite.Group(), aliens) == 0 and len(aliens) == 1


def _teste_stats13(ns):
    G = ns["GameStats"]
    cfg = _Cfg(ship_limit=3)
    s = G(cfg)
    if s.ships_left != 3 or s.game_active is not True:
        return False
    s.ships_left = 0
    cfg.ship_limit = 5
    s.reset_stats()
    return s.ships_left == 5


def _teste_invasao(ns):
    pg = _pg()
    S, A, G = ns["Settings"], ns["Alien"], ns["GameStats"]
    atualizar, atingida, chao = ns["atualizar_frota"], ns["nave_atingida"], ns["aliens_no_chao"]
    cfg = S()
    tela = pg.Rect(0, 0, 400, 300)
    aliens = pg.sprite.Group(A(cfg, 100, 20), A(cfg, 300, 20), A(cfg, 100, 100))
    for _ in range(39):
        atualizar(aliens, cfg, tela)
    if cfg.fleet_direction != 1 or sorted(a.rect.x for a in aliens) != [139, 139, 339]:
        return False
    atualizar(aliens, cfg, tela)          # chega na borda (right = 400)
    atualizar(aliens, cfg, tela)          # vira, desce e anda para a esquerda
    if cfg.fleet_direction != -1 or sorted(a.rect.y for a in aliens) != [30, 30, 110]:
        return False
    if sorted(a.rect.x for a in aliens) != [139, 139, 339]:
        return False
    if chao(aliens, tela) is not False:
        return False
    aliens.add(A(cfg, 0, 250))
    if chao(aliens, tela) is not True:
        return False
    stats = G(cfg)
    balas = pg.sprite.Group(_sprite_simples(0, 0))
    atingida(stats, aliens, balas)
    if stats.ships_left != 2 or len(aliens) != 0 or len(balas) != 0 or stats.game_active is not True:
        return False
    atingida(stats, aliens, balas)
    atingida(stats, aliens, balas)
    if stats.ships_left != 0 or stats.game_active is not True:
        return False
    atingida(stats, aliens, balas)
    return stats.game_active is False and stats.ships_left == 0


# ----------------------------- testes do cap. 14 -----------------------------

def _teste_play(ns):
    R = _pg().Rect
    f = ns["clicou_play"]
    b = R(500, 375, 200, 50)
    return (f(b, (600, 400), False) is True and f(b, (600, 400), True) is False
            and f(b, (10, 10), False) is False and f(b, (500, 375), False) is True
            and f(b, (700, 400), False) is False)


def _teste_acelerar(ns):
    s = ns["Settings"]()
    base = {"ship_speed": 1.5, "bullet_speed": 2.5, "alien_speed": 1.0, "fleet_direction": 1,
            "alien_points": 50, "speedup_scale": 1.1, "score_scale": 1.5}
    if any(getattr(s, k, None) != v for k, v in base.items()):
        return False
    s.increase_speed()
    if (round(s.ship_speed, 3), round(s.bullet_speed, 3), round(s.alien_speed, 3), s.alien_points) != (1.65, 2.75, 1.1, 75):
        return False
    s.increase_speed()
    if (round(s.alien_speed, 3), s.alien_points) != (1.21, 112):
        return False
    s.fleet_direction = -1
    s.initialize_dynamic_settings()
    return (s.ship_speed, s.alien_speed, s.alien_points, s.fleet_direction) == (1.5, 1.0, 50, 1)


def _teste_placar(ns):
    f = ns["formatar_placar"]
    return (f(12347) == "12.350" and f(0) == "0" and f(1234567) == "1.234.570"
            and f(998) == "1.000" and f(42) == "40")


def _teste_recorde(ns):
    G = ns["GameStats"]
    cfg = _Cfg(ship_limit=3)
    s = G(cfg)
    if (s.score, s.level, s.ships_left, s.high_score) != (0, 1, 3, 0):
        return False
    s.score = 1500
    s.check_high_score()
    if s.high_score != 1500:
        return False
    s.reset_stats()
    if s.score != 0 or s.high_score != 1500:
        return False
    s.score = 700
    s.level = 4
    s.check_high_score()
    if s.high_score != 1500:
        return False
    s.reset_stats()
    return s.level == 1


def _saida_placar(inicial):
    rec = inicial
    linhas = [f"Recorde carregado: {rec}"]
    rec = max(rec, 150)
    linhas.append(f"Pontos: 150 | Recorde: {rec}")
    rec = max(rec, 900)
    linhas.append(f"Pontos: 900 | Recorde: {rec}")
    linhas.append(f"Nova partida: pontos 0, nível 1, vidas 3, recorde {rec}")
    return "\n".join(linhas), rec


def _casos_placar_eterno():
    casos = []
    for arq in ["800", None, "5000"]:
        esperado, final = _saida_placar(int(arq) if arq else 0)
        ctx = {"__arquivos__": {"recorde.json": arq}} if arq else {}
        casos.append(caso([classe("GameStats"), saida(esperado), arquivo_json("recorde.json", final)], ctx))
    return casos


# ---------------------------------------------------------------------------
# CAPÍTULO 12: Alien Invasion, a nave
# ---------------------------------------------------------------------------

CAP12 = {
    "num": 12,
    "titulo": "Alien Invasion: a Nave",
    "subtitulo": "Projeto do jogo: Settings, Rect, teclado e tiros",
    "licoes": [
        {
            "titulo": "Planejando o jogo",
            "texto": [
                "Começa a Parte II do livro: **projetos**! O primeiro é o **Alien Invasion**: você controla uma nave "
                "na parte de baixo da tela e atira numa frota de alienígenas que vai descendo.",
                "O livro usa a biblioteca **pygame**, que abre janelas e desenha imagens. Aqui não há janela, então o "
                "PyQuest traz um **pygame de treino**: as mesmas peças (`Rect`, `Sprite`, `Group`, eventos e teclas), "
                "só que sem gráficos. Você treina a **lógica**, que é o coração do jogo. No seu PC, depois de "
                "`pip install pygame`, o mesmo código ganha imagens.",
                "## O laço do jogo",
                "Todo jogo é um `while True:` que roda dezenas de vezes por segundo. Cada volta é um **quadro**, e em cada "
                "um o jogo faz três coisas: lê os eventos (teclas e mouse), atualiza as posições e redesenha a tela.",
                "## A classe Settings",
                "Em vez de espalhar números pelo código, o livro guarda todas as configurações numa classe `Settings`. "
                "Quer uma nave mais rápida? Você muda em um lugar só.",
            ],
            "exemplo": _c('''
class Settings:
    """Guarda as configurações do Alien Invasion."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5


settings = Settings()
print(f"Tela de {settings.screen_width}x{settings.screen_height}")

# Um laço de jogo simulado, com só 3 quadros
quadro = 0
while quadro < 3:
    quadro += 1
    print(f"Quadro {quadro}: ler eventos -> atualizar -> desenhar")
'''),
        },
        {
            "titulo": "Rect: tudo é um retângulo",
            "texto": [
                "No pygame, cada elemento do jogo (a nave, um tiro, um alienígena e até a tela) é tratado como um "
                "retângulo, um `Rect`. Assim fica fácil calcular posições e colisões.",
                "`pygame.Rect(x, y, largura, altura)` cria um retângulo. O ponto (0, 0) é o **canto superior esquerdo** "
                "da tela, e o `y` cresce **para baixo**.",
                "Um Rect tem atributos prontos: `left`, `right`, `top`, `bottom`, `centerx`, `centery`, `center`, "
                "`midtop`, `midbottom`... Mudar qualquer um deles move o retângulo inteiro.",
                "## Nave no meio, embaixo",
                "O livro posiciona a nave com `self.rect.midbottom = self.screen_rect.midbottom`: o meio da base da nave "
                "fica no meio da base da tela.",
            ],
            "exemplo": _c('''
import pygame

tela = pygame.display.set_mode((1200, 800))
tela_rect = tela.get_rect()
print("Tela:", tela_rect)

nave = pygame.Rect(0, 0, 60, 48)
nave.midbottom = tela_rect.midbottom
print("Nave:", nave)
print("Esquerda:", nave.left, "| Direita:", nave.right, "| Topo:", nave.top)
'''),
        },
        {
            "titulo": "Pilotando a nave",
            "texto": [
                "Quando o jogador aperta uma tecla, o pygame gera um evento `KEYDOWN`; quando solta, `KEYUP`. "
                "O `event.key` diz qual foi: `pygame.K_RIGHT`, `pygame.K_LEFT`, `pygame.K_SPACE`...",
                "Para a nave andar **enquanto** a tecla estiver apertada, o livro usa **flags**: `moving_right = True` "
                "no KEYDOWN e `False` no KEYUP. O método `update()` confere as flags a cada quadro.",
                "## Por que self.x?",
                "Um Rect só guarda números inteiros. Com velocidade 1.5, a parte decimal se perderia. Por isso a nave "
                "guarda a posição num `self.x` decimal e copia para o retângulo: `self.rect.x = self.x`.",
                "Para não sair da tela: só anda para a direita se `self.rect.right < self.screen_rect.right`, e para "
                "a esquerda se `self.rect.left > 0`.",
            ],
            "exemplo": _c('''
import pygame


class Settings:
    def __init__(self):
        self.ship_speed = 1.5


class Ship:
    def __init__(self, settings, screen_rect):
        self.settings = settings
        self.screen_rect = screen_rect
        self.rect = pygame.Rect(0, 0, 60, 48)
        self.rect.midbottom = screen_rect.midbottom
        self.x = float(self.rect.x)
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x


nave = Ship(Settings(), pygame.Rect(0, 0, 1200, 800))

evento = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
if evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
    nave.moving_right = True

for quadro in range(4):
    nave.update()
    print(f"Quadro {quadro + 1}: x = {nave.x}  rect.x = {nave.rect.x}")
'''),
        },
        {
            "titulo": "Fogo! Sprites e grupos",
            "texto": [
                "Os tiros herdam da classe `Sprite` do pygame. Sprites podem ser guardados num **grupo** "
                "(`pygame.sprite.Group`), uma espécie de lista turbinada.",
                "Com o grupo, `balas.update()` chama o `update()` de **cada** bala de uma vez, e `len(balas)` diz quantas existem.",
                "Cada `Bullet` nasce no topo da nave (`self.rect.midtop = nave.rect.midtop`) e sobe: o `y` **diminui** a cada quadro.",
                "## Limpando as balas",
                "Balas que saem pelo topo continuariam existindo, gastando memória. O livro remove as que têm "
                "`bullet.rect.bottom <= 0`. Para remover sem bagunçar o laço, percorra uma **cópia**: `for bullet in balas.copy():`.",
                "E para não virar uma chuva de tiros: só crie uma bala nova se `len(balas) < settings.bullets_allowed`.",
            ],
            "exemplo": _c('''
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, nave_rect, velocidade):
        super().__init__()
        self.rect = pygame.Rect(0, 0, 3, 15)
        self.rect.midtop = nave_rect.midtop
        self.y = float(self.rect.y)
        self.velocidade = velocidade

    def update(self):
        self.y -= self.velocidade
        self.rect.y = self.y


nave = pygame.Rect(570, 752, 60, 48)
balas = pygame.sprite.Group()
balas.add(Bullet(nave, 300))
balas.add(Bullet(nave, 200))
print("Balas:", len(balas))

for quadro in range(3):
    balas.update()
    for bala in balas.copy():
        if bala.rect.bottom <= 0:
            balas.remove(bala)
    print(f"Quadro {quadro + 1}: {len(balas)} bala(s) na tela")
'''),
        },
    ],
    "quiz": [
        {"pergunta": "Por que o Alien Invasion junta as configurações numa classe Settings?",
         "opcoes": ["Porque o pygame exige", "Para mudar os valores do jogo num lugar só",
                    "Para o jogo rodar mais rápido", "Para salvar o recorde"], "correta": 1,
         "explicacao": "Com tudo em Settings, ajustar velocidade, cores ou tamanhos é mudar uma linha."},
        {"pergunta": "No pygame, onde fica o ponto (0, 0) da tela?",
         "opcoes": ["No centro", "No canto inferior esquerdo", "No canto superior esquerdo", "No canto superior direito"],
         "correta": 2, "explicacao": "A origem é o canto superior esquerdo, e o y cresce para baixo."},
        {"pergunta": "O que é mostrado?", "codigo": "r = pygame.Rect(100, 50, 40, 20)\nprint(r.right, r.bottom)",
         "opcoes": ["140 70", "40 20", "100 50", "60 30"], "correta": 0,
         "explicacao": "right = x + largura (100 + 40) e bottom = y + altura (50 + 20)."},
        {"pergunta": "Por que a nave guarda a posição em self.x, além do rect?",
         "opcoes": ["Para guardar o nome da nave", "Porque o Rect só guarda inteiros e a velocidade tem decimais",
                    "Para desenhar a imagem", "Porque rect.x não existe"], "correta": 1,
         "explicacao": "self.x acumula os decimais (1.5, 3.0, 4.5...) e o rect recebe a parte inteira."},
        {"pergunta": "Qual evento acontece quando o jogador SOLTA uma tecla?",
         "opcoes": ["KEYDOWN", "KEYUP", "QUIT", "MOUSEBUTTONDOWN"], "correta": 1,
         "explicacao": "KEYDOWN é apertar, KEYUP é soltar."},
        {"pergunta": "O que `balas.update()` faz quando balas é um Group?",
         "opcoes": ["Apaga todas as balas", "Chama update() em cada bala do grupo", "Cria uma bala nova", "Nada"],
         "correta": 1, "explicacao": "O grupo repassa a chamada para cada sprite que ele contém."},
        {"pergunta": "Por que o laço que remove balas percorre `balas.copy()`?",
         "opcoes": ["Para duplicar as balas", "Para não alterar o grupo enquanto ele é percorrido",
                    "Porque copy() é mais rápido", "Para salvar as balas num arquivo"], "correta": 1,
         "explicacao": "Remover itens da mesma coleção que você está percorrendo pode pular itens. A cópia evita isso."},
    ],
    "desafios": [
        {
            "titulo": "Painel de controle",
            "enunciado": "Crie a classe `Settings` com estes atributos no __init__ (os mesmos do livro):\n"
                         "• screen_width = 1200, screen_height = 800, bg_color = (230, 230, 230)\n"
                         "• ship_speed = 1.5\n"
                         "• bullet_speed = 2.0, bullet_width = 3, bullet_height = 15, bullet_color = (60, 60, 60)\n"
                         "• bullets_allowed = 3",
            "inicial": "class Settings:\n    pass\n",
            "dica": "Dentro de def __init__(self):, escreva uma linha self.nome = valor para cada atributo.",
            "solucao": _c('''
class Settings:
    """Guarda as configurações do Alien Invasion."""

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.5
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3
'''),
            "casos": [caso([classe("Settings"),
                            regra(lambda o, n, c: _teste_settings(n),
                                  "Algum atributo de Settings está faltando ou com o valor diferente. Confira cada um no enunciado.")])],
        },
        {
            "titulo": "Nave a postos",
            "enunciado": "Crie a função `posicionar_nave(tela_rect, nave_rect)` que coloca a nave no meio da base da tela "
                         "(o midbottom da nave igual ao midbottom da tela) e devolve o próprio nave_rect.\n\n"
                         "Exemplo: tela Rect(0, 0, 1200, 800) e nave Rect(0, 0, 60, 48) → nave fica em <rect(570, 752, 60, 48)>.",
            "inicial": _c('''
import pygame


def posicionar_nave(tela_rect, nave_rect):
    pass


tela = pygame.Rect(0, 0, 1200, 800)
nave = pygame.Rect(0, 0, 60, 48)
print(posicionar_nave(tela, nave))
''') + "\n",
            "dica": "Uma linha resolve: nave_rect.midbottom = tela_rect.midbottom. Depois, return nave_rect.",
            "solucao": _c('''
import pygame


def posicionar_nave(tela_rect, nave_rect):
    nave_rect.midbottom = tela_rect.midbottom
    return nave_rect


tela = pygame.Rect(0, 0, 1200, 800)
nave = pygame.Rect(0, 0, 60, 48)
print(posicionar_nave(tela, nave))
'''),
            "casos": [caso([funcao("posicionar_nave"),
                            regra(lambda o, n, c: _teste_posicionar(n),
                                  "Teste: numa tela 1200x800, a nave 60x48 deveria ficar em (570, 752); numa tela 800x600, "
                                  "uma nave 40x30 deveria ficar em (380, 570). A função também precisa devolver o nave_rect.")])],
        },
        {
            "titulo": "Foguete em 4 direções",
            "enunciado": "Inspirado no exercício do foguete do livro: crie a classe `Ship(settings, screen_rect)`.\n"
                         "• rect de 60x48 começando no meio da base da tela; self.x e self.y decimais\n"
                         "• flags moving_right, moving_left, moving_up e moving_down (todas False)\n"
                         "• update(): anda settings.ship_speed na direção de cada flag ligada, sem sair da tela "
                         "(right < tela.right, left > 0, top > 0, bottom < tela.bottom) e copia x e y para o rect",
            "inicial": _c('''
import pygame


class Ship:
    def __init__(self, settings, screen_rect):
        self.settings = settings
        self.screen_rect = screen_rect
        self.rect = pygame.Rect(0, 0, 60, 48)
        self.rect.midbottom = screen_rect.midbottom
        # Crie self.x, self.y e as 4 flags

    def update(self):
        pass
''') + "\n",
            "dica": "self.y = float(self.rect.y). No update, quatro ifs (um por flag) e, no fim, self.rect.x = self.x e self.rect.y = self.y. "
                    "Lembre: para subir, o y DIMINUI.",
            "solucao": _c('''
import pygame


class Ship:
    def __init__(self, settings, screen_rect):
        self.settings = settings
        self.screen_rect = screen_rect
        self.rect = pygame.Rect(0, 0, 60, 48)
        self.rect.midbottom = screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        self.rect.x = self.x
        self.rect.y = self.y
'''),
            "casos": [caso([classe("Ship"),
                            regra(lambda o, n, c: _teste_foguete(n),
                                  "Teste numa tela 300x200 com ship_speed 2.5: a nave começa em (120, 152) com as 4 flags False; "
                                  "update() sem flags não a move; com moving_up, 4 updates levam o y a 142; e em cada direção ela "
                                  "precisa parar na borda da tela, sem passar dela.")])],
        },
        {
            "titulo": "Teclado de bordo",
            "enunciado": "Crie a função `checar_teclas(evento, nave)`:\n"
                         "• KEYDOWN de K_RIGHT liga nave.moving_right; KEYDOWN de K_LEFT liga nave.moving_left\n"
                         "• KEYUP de K_RIGHT desliga moving_right; KEYUP de K_LEFT desliga moving_left\n"
                         "• outras teclas não mudam nada",
            "inicial": _c('''
import pygame


class Nave:
    def __init__(self):
        self.moving_right = False
        self.moving_left = False


def checar_teclas(evento, nave):
    pass


nave = Nave()
checar_teclas(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT), nave)
print("Direita:", nave.moving_right)
''') + "\n",
            "dica": "Primeiro teste evento.type == pygame.KEYDOWN (ou KEYUP). Dentro, teste evento.key == pygame.K_RIGHT ou pygame.K_LEFT.",
            "solucao": _c('''
import pygame


class Nave:
    def __init__(self):
        self.moving_right = False
        self.moving_left = False


def checar_teclas(evento, nave):
    if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_RIGHT:
            nave.moving_right = True
        elif evento.key == pygame.K_LEFT:
            nave.moving_left = True
    elif evento.type == pygame.KEYUP:
        if evento.key == pygame.K_RIGHT:
            nave.moving_right = False
        elif evento.key == pygame.K_LEFT:
            nave.moving_left = False


nave = Nave()
checar_teclas(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT), nave)
print("Direita:", nave.moving_right)
'''),
            "casos": [caso([funcao("checar_teclas"),
                            regra(lambda o, n, c: _teste_teclas(n),
                                  "Teste: apertar → (KEYDOWN) direita e esquerda ligam as flags; soltar (KEYUP) desliga só a "
                                  "flag daquela tecla; a barra de espaço não muda nenhuma flag.")])],
        },
        {
            "titulo": "Primeiro disparo",
            "enunciado": "Crie a classe `Bullet(settings, nave_rect)`, filha de `Sprite`:\n"
                         "• chame super().__init__()\n"
                         "• rect com settings.bullet_width x settings.bullet_height, com o midtop no midtop da nave\n"
                         "• self.y decimal\n"
                         "• update(): sobe settings.bullet_speed (o y diminui) e copia para rect.y",
            "inicial": _c('''
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    pass
''') + "\n",
            "dica": "self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height) e depois "
                    "self.rect.midtop = nave_rect.midtop. Guarde settings em self.settings para usar no update.",
            "solucao": _c('''
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, settings, nave_rect):
        super().__init__()
        self.settings = settings
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.midtop = nave_rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
'''),
            "casos": [caso([classe("Bullet"),
                            regra(lambda o, n, c: _teste_bala(n),
                                  "Teste: Bullet precisa herdar de Sprite; com bala 3x15 e nave em Rect(570, 752, 60, 48), "
                                  "o midtop da bala é (600, 752); depois de 2 updates com velocidade 2.0, o y vai a 748. "
                                  "O tamanho e a velocidade devem vir de settings.")])],
        },
        {
            "titulo": "Caça-bugs: a nave empacada",
            "enunciado": "A nave deveria andar 1.5 por quadro e terminar em 585, mas o programa mostra 570. "
                         "Encontre o que falta e conserte.",
            "inicial": _c('''
import pygame


class Ship:
    def __init__(self, speed):
        self.speed = speed
        self.rect = pygame.Rect(570, 752, 60, 48)
        self.x = float(self.rect.x)
        self.moving_right = True

    def update(self):
        if self.moving_right:
            self.x += self.speed


nave = Ship(1.5)
for _ in range(10):
    nave.update()
print(nave.rect.x)
''') + "\n",
            "dica": "O self.x muda, mas o retângulo da nave nunca fica sabendo disso.",
            "solucao": _c('''
import pygame


class Ship:
    def __init__(self, speed):
        self.speed = speed
        self.rect = pygame.Rect(570, 752, 60, 48)
        self.x = float(self.rect.x)
        self.moving_right = True

    def update(self):
        if self.moving_right:
            self.x += self.speed
        self.rect.x = self.x


nave = Ship(1.5)
for _ in range(10):
    nave.update()
print(nave.rect.x)
'''),
            "casos": [caso([saida("585")])],
        },
    ],
    "chefe": {
        "titulo": "O Hangar",
        "enunciado": "A Settings e a Bullet já estão prontas. Escreva duas funções:\n\n"
                     "• `disparar(balas, settings, nave_rect)`: se len(balas) for menor que settings.bullets_allowed, cria uma "
                     "Bullet, adiciona ao grupo e devolve True. Se o limite já foi atingido, não cria nada e devolve False.\n"
                     "• `atualizar_balas(balas)`: atualiza todas as balas e remove do grupo as que têm rect.bottom <= 0.",
        "inicial": _c('''
import pygame
from pygame.sprite import Sprite


class Settings:
    def __init__(self):
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 3


class Bullet(Sprite):
    def __init__(self, settings, nave_rect):
        super().__init__()
        self.settings = settings
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.midtop = nave_rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y


def disparar(balas, settings, nave_rect):
    pass


def atualizar_balas(balas):
    pass


# Teste rápido
settings = Settings()
nave = pygame.Rect(570, 752, 60, 48)
balas = pygame.sprite.Group()
for _ in range(5):
    print("Disparou?", disparar(balas, settings, nave))
print("Balas no ar:", len(balas))
''') + "\n",
        "dica": "Em atualizar_balas: primeiro balas.update(); depois for bala in balas.copy(): if bala.rect.bottom <= 0: balas.remove(bala).",
        "solucao": _c('''
import pygame
from pygame.sprite import Sprite


class Settings:
    def __init__(self):
        self.bullet_speed = 2.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullets_allowed = 3


class Bullet(Sprite):
    def __init__(self, settings, nave_rect):
        super().__init__()
        self.settings = settings
        self.rect = pygame.Rect(0, 0, settings.bullet_width, settings.bullet_height)
        self.rect.midtop = nave_rect.midtop
        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y


def disparar(balas, settings, nave_rect):
    if len(balas) < settings.bullets_allowed:
        balas.add(Bullet(settings, nave_rect))
        return True
    return False


def atualizar_balas(balas):
    balas.update()
    for bala in balas.copy():
        if bala.rect.bottom <= 0:
            balas.remove(bala)


# Teste rápido
settings = Settings()
nave = pygame.Rect(570, 752, 60, 48)
balas = pygame.sprite.Group()
for _ in range(5):
    print("Disparou?", disparar(balas, settings, nave))
print("Balas no ar:", len(balas))
'''),
        "casos": [caso([funcao("disparar"), funcao("atualizar_balas"),
                        regra(lambda o, n, c: _teste_hangar(n),
                              "Teste: 5 disparos seguidos devem devolver True, True, True, False, False (limite de 3); "
                              "as balas continuam no ar depois de 100 atualizações e somem todas depois que passam do topo "
                              "(rect.bottom <= 0); aí dá para disparar de novo.")])],
    },
}


# ---------------------------------------------------------------------------
# CAPÍTULO 13: Alien Invasion, os alienígenas
# ---------------------------------------------------------------------------

CAP13 = {
    "num": 13,
    "titulo": "Alien Invasion: Alienígenas!",
    "subtitulo": "A frota, colisões, vidas e fim de jogo",
    "licoes": [
        {
            "titulo": "Montando a frota",
            "texto": [
                "Hora dos inimigos! Cada alienígena é um `Sprite` com seu `rect`, e todos ficam num grupo `aliens`.",
                "Para encher a tela, o livro usa dois laços `while`. O de dentro preenche uma **linha**: começa em "
                "`x = largura_do_alien` e avança `2 * largura_do_alien` (um alien e um espaço vazio), enquanto "
                "`x < largura_da_tela - 2 * largura_do_alien`.",
                "O de fora cria várias **linhas**: começa em `y = altura_do_alien`, avança `2 * altura_do_alien` e para "
                "quando `y` chega a `altura_da_tela - 3 * altura_do_alien`. Esse espaço sobrando embaixo é para a nave "
                "ter tempo de atirar.",
                "Repare que no fim de cada linha o `x` volta ao começo.",
            ],
            "exemplo": _c('''
largura_tela, altura_tela = 600, 400
largura_alien, altura_alien = 60, 50

posicoes = []
x, y = largura_alien, altura_alien
while y < altura_tela - 3 * altura_alien:
    while x < largura_tela - 2 * largura_alien:
        posicoes.append((x, y))
        x += 2 * largura_alien
    x = largura_alien          # volta para o começo da próxima linha
    y += 2 * altura_alien

print(f"{len(posicoes)} alienígenas:")
for p in posicoes:
    print(p)
'''),
        },
        {
            "titulo": "A frota marcha",
            "texto": [
                "A frota anda de lado e, ao bater numa borda, **desce** e **inverte** a direção.",
                "O livro guarda isso em Settings: `alien_speed` (velocidade), `fleet_drop_speed` (quanto desce) e "
                "`fleet_direction`, que vale `1` para a direita e `-1` para a esquerda. Multiplicar pela direção "
                "evita um if: `self.x += speed * direction`.",
                "Cada alien tem `check_edges()`, que devolve True se ele encostou numa borda: "
                "`self.rect.right >= screen_rect.right or self.rect.left <= 0`.",
                "A cada quadro: se **algum** alien está na borda, a frota toda desce e `fleet_direction *= -1` "
                "(basta um, por isso o `break`). Depois, todos andam.",
            ],
            "exemplo": _c('''
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, x):
        super().__init__()
        self.rect = pygame.Rect(x, 20, 60, 50)
        self.x = float(x)

    def check_edges(self, tela):
        return self.rect.right >= tela.right or self.rect.left <= 0


tela = pygame.Rect(0, 0, 300, 200)
velocidade, direcao, queda = 40, 1, 10
aliens = pygame.sprite.Group(Alien(60), Alien(160))

for quadro in range(5):
    for alien in aliens:
        if alien.check_edges(tela):
            for a in aliens:
                a.rect.y += queda
            direcao *= -1
            print("  Borda! A frota desce e vira.")
            break
    for alien in aliens:
        alien.x += velocidade * direcao
        alien.rect.x = alien.x
    print(f"Quadro {quadro + 1}:", [(a.rect.x, a.rect.y) for a in aliens])
'''),
        },
        {
            "titulo": "Acertando os alvos",
            "texto": [
                "Uma **colisão** acontece quando dois retângulos se sobrepõem. O pygame confere isso para você.",
                "`pygame.sprite.groupcollide(balas, aliens, True, True)` compara cada bala com cada alien e devolve um "
                "dicionário `{bala: [aliens atingidos]}`. Os dois `True` mandam remover a bala e o alien que se tocaram.",
                "Quando a frota acaba (`if not aliens:`), o livro esvazia as balas com `balas.empty()` e cria uma frota nova.",
                "`pygame.sprite.spritecollideany(nave, aliens)` devolve o primeiro alien que encostou na nave, ou `None` se nenhum encostou.",
            ],
            "exemplo": _c('''
import pygame
from pygame.sprite import Sprite


class Coisa(Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)


balas = pygame.sprite.Group(Coisa(30, 40, 3, 15), Coisa(500, 300, 3, 15))
aliens = pygame.sprite.Group(Coisa(0, 0, 60, 50), Coisa(200, 0, 60, 50))

colisoes = pygame.sprite.groupcollide(balas, aliens, True, True)
print("Batidas:", len(colisoes))
print("Balas restantes:", len(balas), "| Aliens restantes:", len(aliens))

nave = Coisa(210, 30, 60, 48)
atingiu = pygame.sprite.spritecollideany(nave, aliens)
print("Algum alien encostou na nave?", atingiu is not None)
'''),
        },
        {
            "titulo": "Vidas e fim de jogo",
            "texto": [
                "O livro cria a classe `GameStats` para guardar as estatísticas da partida. O número de naves vem de "
                "`settings.ship_limit`, e o método `reset_stats()` recomeça os valores numa nova partida.",
                "Quando a nave é atingida (ou um alien chega à base da tela): se ainda há naves (`ships_left > 0`), tira "
                "uma, esvazia aliens e balas e recomeça a fase. Senão, `game_active = False` e o jogo acaba.",
                "A flag `game_active` diz se o laço do jogo deve continuar atualizando tudo.",
            ],
            "exemplo": _c('''
class Settings:
    def __init__(self):
        self.ship_limit = 2


class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit


stats = GameStats(Settings())
for batida in range(4):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        print(f"Nave atingida! Restam {stats.ships_left}.")
    else:
        stats.game_active = False
        print("GAME OVER")
        break
'''),
        },
    ],
    "quiz": [
        {"pergunta": "Na criação da frota, por que x avança `2 * largura_do_alien`?",
         "opcoes": ["Para os aliens ficarem colados", "Para deixar um espaço do tamanho de um alien entre eles",
                    "Porque a tela tem duas metades", "Para dobrar a velocidade"], "correta": 1,
         "explicacao": "Um alien ocupa uma largura e o espaço vazio ao lado ocupa outra."},
        {"pergunta": "O que `fleet_direction = -1` significa?",
         "opcoes": ["A frota desce", "A frota anda para a esquerda", "A frota para", "A frota sobe"], "correta": 1,
         "explicacao": "speed * -1 dá um valor negativo, e o x diminui: a frota vai para a esquerda."},
        {"pergunta": "O que é mostrado?", "codigo": "direcao = 1\ndirecao *= -1\ndirecao *= -1\nprint(direcao)",
         "opcoes": ["1", "-1", "0", "Erro"], "correta": 0,
         "explicacao": "Inverter duas vezes volta ao valor original."},
        {"pergunta": "O que `groupcollide(balas, aliens, True, False)` faz com quem colidiu?",
         "opcoes": ["Remove as balas e mantém os aliens", "Remove os dois", "Remove os aliens e mantém as balas", "Não remove nada"],
         "correta": 0, "explicacao": "O primeiro True vale para o primeiro grupo (balas); o False mantém os aliens."},
        {"pergunta": "O que `spritecollideany(nave, aliens)` devolve se nenhum alien encosta na nave?",
         "opcoes": ["False", "0", "None", "Uma lista vazia"], "correta": 2,
         "explicacao": "Sem colisão, o resultado é None. Com colisão, é o alien que encostou."},
        {"pergunta": "Quando um alien chega à base da tela, o livro trata isso como...",
         "opcoes": ["Ponto para o jogador", "Nada acontece", "A nave foi atingida", "Uma nova fase sem perder vida"],
         "correta": 2, "explicacao": "Deixar um alien passar custa uma nave, igual a uma batida."},
        {"pergunta": "Para que serve a flag game_active?",
         "opcoes": ["Guardar a pontuação", "Saber se o jogo está rodando ou terminou", "Contar os aliens", "Mudar a cor da tela"],
         "correta": 1, "explicacao": "Com game_active False, o laço para de mover a nave, as balas e os aliens."},
    ],
    "desafios": [
        {
            "titulo": "Quantos cabem?",
            "enunciado": "Crie a função `posicoes_frota(largura_tela, altura_tela, largura_alien, altura_alien)` que devolve "
                         "a lista de tuplas (x, y) de cada alien, usando o mesmo método da lição:\n"
                         "• x começa em largura_alien e avança 2 * largura_alien enquanto x < largura_tela - 2 * largura_alien\n"
                         "• y começa em altura_alien e avança 2 * altura_alien enquanto y < altura_tela - 3 * altura_alien\n\n"
                         "Exemplo: posicoes_frota(600, 400, 60, 50) devolve 8 posições, de (60, 50) até (420, 150).",
            "inicial": _c('''
def posicoes_frota(largura_tela, altura_tela, largura_alien, altura_alien):
    posicoes = []
    # Seu código aqui
    return posicoes


print(posicoes_frota(600, 400, 60, 50))
''') + "\n",
            "dica": "Dois while, um dentro do outro. Não esqueça de voltar o x para largura_alien no fim de cada linha!",
            "solucao": _c('''
def posicoes_frota(largura_tela, altura_tela, largura_alien, altura_alien):
    posicoes = []
    x, y = largura_alien, altura_alien
    while y < altura_tela - 3 * altura_alien:
        while x < largura_tela - 2 * largura_alien:
            posicoes.append((x, y))
            x += 2 * largura_alien
        x = largura_alien
        y += 2 * altura_alien
    return posicoes


print(posicoes_frota(600, 400, 60, 50))
'''),
            "casos": [caso([funcao("posicoes_frota"),
                            regra(lambda o, n, c: _teste_frota(n),
                                  "As posições não bateram. Teste: posicoes_frota(600, 400, 60, 50) deveria dar "
                                  f"{_frota_ref(600, 400, 60, 50)}. Também testo telas e aliens de outros tamanhos.")])],
        },
        {
            "titulo": "Radar de bordas",
            "enunciado": "Crie a classe `Alien(x, y)`, filha de `Sprite`:\n"
                         "• rect de 60x50 com o canto superior esquerdo em (x, y) e self.x decimal\n"
                         "• check_edges(screen_rect): devolve True se o alien encostou na borda direita (right >= tela.right) "
                         "ou na esquerda (left <= 0); senão, False",
            "inicial": _c('''
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    pass
''') + "\n",
            "dica": "return self.rect.right >= screen_rect.right or self.rect.left <= 0",
            "solucao": _c('''
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 60, 50)
        self.x = float(self.rect.x)

    def check_edges(self, screen_rect):
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
'''),
            "casos": [caso([classe("Alien"),
                            regra(lambda o, n, c: _teste_bordas(n),
                                  "Teste numa tela de 400 de largura: Alien(100, 20) não está na borda; Alien(340, 0) "
                                  "(right = 400) e Alien(0, 0) estão; Alien(339, 0) e Alien(1, 0) não estão. O alien "
                                  "precisa herdar de Sprite e ter rect de 60x50.")])],
        },
        {
            "titulo": "Meia-volta, volver!",
            "enunciado": "Crie a função `mudar_direcao(aliens, settings)`: desce cada alien do grupo "
                         "settings.fleet_drop_speed pixels (rect.y) e inverte settings.fleet_direction (1 vira -1 e vice-versa).",
            "inicial": _c('''
def mudar_direcao(aliens, settings):
    pass
''') + "\n",
            "dica": "Um for nos aliens com alien.rect.y += settings.fleet_drop_speed e, FORA do for, settings.fleet_direction *= -1.",
            "solucao": _c('''
def mudar_direcao(aliens, settings):
    for alien in aliens:
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1
'''),
            "casos": [caso([funcao("mudar_direcao"),
                            regra(lambda o, n, c: _teste_meia_volta(n),
                                  "Teste: aliens em y = 50, 50 e 150 com fleet_drop_speed 10 devem ir para 60, 60 e 160, e a "
                                  "direção de 1 para -1. Chamando de novo (com queda 25), voltam a 1 e descem mais 25. "
                                  "A direção deve inverter UMA vez por chamada.")])],
        },
        {
            "titulo": "Tiro certeiro",
            "enunciado": "Crie a função `checar_colisoes(balas, aliens)` que usa pygame.sprite.groupcollide para remover as "
                         "balas e os aliens que se tocaram e devolve QUANTOS aliens foram destruídos.\n\n"
                         "Atenção: uma bala pode atingir mais de um alien ao mesmo tempo.",
            "inicial": _c('''
import pygame


def checar_colisoes(balas, aliens):
    pass
''') + "\n",
            "dica": "colisoes = pygame.sprite.groupcollide(balas, aliens, True, True). Depois some len(lista) para cada lista em colisoes.values().",
            "solucao": _c('''
import pygame


def checar_colisoes(balas, aliens):
    colisoes = pygame.sprite.groupcollide(balas, aliens, True, True)
    total = 0
    for atingidos in colisoes.values():
        total += len(atingidos)
    return total
'''),
            "casos": [caso([funcao("checar_colisoes"),
                            regra(lambda o, n, c: _teste_colisoes(n),
                                  "Teste: 3 balas e 4 aliens, em que uma bala acerta 1 alien, outra acerta 2 de uma vez e a "
                                  "terceira erra. Deveria devolver 3, sobrando 1 bala e 1 alien. Sem balas, devolve 0.")])],
        },
        {
            "titulo": "Estatísticas da partida",
            "enunciado": "Crie a classe `GameStats(settings)`:\n"
                         "• guarda settings, chama reset_stats() e cria game_active = True\n"
                         "• reset_stats(): ships_left recebe settings.ship_limit",
            "inicial": "class GameStats:\n    pass\n",
            "dica": "No __init__: self.settings = settings, self.reset_stats(), self.game_active = True.",
            "solucao": _c('''
class GameStats:
    """Guarda as estatísticas do Alien Invasion."""

    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
'''),
            "casos": [caso([classe("GameStats"),
                            regra(lambda o, n, c: _teste_stats13(n),
                                  "Teste: com ship_limit 3, GameStats começa com ships_left 3 e game_active True; depois de "
                                  "mudar ship_limit para 5, reset_stats() deixa ships_left em 5.")])],
        },
        {
            "titulo": "Caça-bugs: a frota teimosa",
            "enunciado": "A frota desce direitinho, mas nunca muda de direção: o programa mostra 1 em vez de -1. Conserte.",
            "inicial": _c('''
class Settings:
    def __init__(self):
        self.fleet_direction = 1
        self.fleet_drop_speed = 10


def mudar_direcao(settings, alturas):
    for i in range(len(alturas)):
        alturas[i] += settings.fleet_drop_speed
    settings.fleet_direction * -1


settings = Settings()
alturas = [50, 50, 150]
mudar_direcao(settings, alturas)
print(settings.fleet_direction)
print(alturas)
''') + "\n",
            "dica": "Fazer uma conta não guarda o resultado em lugar nenhum. Falta um sinal de atribuição.",
            "solucao": _c('''
class Settings:
    def __init__(self):
        self.fleet_direction = 1
        self.fleet_drop_speed = 10


def mudar_direcao(settings, alturas):
    for i in range(len(alturas)):
        alturas[i] += settings.fleet_drop_speed
    settings.fleet_direction *= -1


settings = Settings()
alturas = [50, 50, 150]
mudar_direcao(settings, alturas)
print(settings.fleet_direction)
print(alturas)
'''),
            "casos": [caso([saida("-1\n[60, 60, 160]")])],
        },
    ],
    "chefe": {
        "titulo": "A Invasão",
        "enunciado": "Settings, Alien e GameStats já estão prontos. Escreva três funções:\n\n"
                     "• `atualizar_frota(aliens, settings, screen_rect)`: se ALGUM alien estiver na borda (check_edges), "
                     "desce todos settings.fleet_drop_speed e inverte settings.fleet_direction (só uma vez). Depois, "
                     "chama aliens.update().\n"
                     "• `aliens_no_chao(aliens, screen_rect)`: devolve True se algum alien tem rect.bottom >= screen_rect.bottom.\n"
                     "• `nave_atingida(stats, aliens, balas)`: se stats.ships_left > 0, tira uma nave e esvazia aliens e "
                     "balas. Senão, stats.game_active = False.",
        "inicial": _c('''
import pygame
from pygame.sprite import Sprite


class Settings:
    def __init__(self):
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.ship_limit = 3


class Alien(Sprite):
    def __init__(self, settings, x, y):
        super().__init__()
        self.settings = settings
        self.rect = pygame.Rect(x, y, 60, 50)
        self.x = float(x)

    def check_edges(self, screen_rect):
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x


class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit


def atualizar_frota(aliens, settings, screen_rect):
    pass


def aliens_no_chao(aliens, screen_rect):
    pass


def nave_atingida(stats, aliens, balas):
    pass
''') + "\n",
        "dica": "Em atualizar_frota: for alien in aliens: if alien.check_edges(screen_rect): (desça todos e inverta) e break. "
                "Fora do for, aliens.update(). Para esvaziar um grupo: aliens.empty().",
        "solucao": _c('''
import pygame
from pygame.sprite import Sprite


class Settings:
    def __init__(self):
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.ship_limit = 3


class Alien(Sprite):
    def __init__(self, settings, x, y):
        super().__init__()
        self.settings = settings
        self.rect = pygame.Rect(x, y, 60, 50)
        self.x = float(x)

    def check_edges(self, screen_rect):
        return self.rect.right >= screen_rect.right or self.rect.left <= 0

    def update(self):
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x


class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit


def atualizar_frota(aliens, settings, screen_rect):
    for alien in aliens:
        if alien.check_edges(screen_rect):
            for a in aliens:
                a.rect.y += settings.fleet_drop_speed
            settings.fleet_direction *= -1
            break
    aliens.update()


def aliens_no_chao(aliens, screen_rect):
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            return True
    return False


def nave_atingida(stats, aliens, balas):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        aliens.empty()
        balas.empty()
    else:
        stats.game_active = False
'''),
        "casos": [caso([funcao("atualizar_frota"), funcao("aliens_no_chao"), funcao("nave_atingida"),
                        regra(lambda o, n, c: _teste_invasao(n),
                              "Teste numa tela 400x300 com 3 aliens: a frota anda 1 pixel por quadro para a direita; quando "
                              "um alien encosta na borda, a frota toda desce 10 e passa a andar para a esquerda (virando uma "
                              "vez só). aliens_no_chao detecta um alien com bottom >= 300. nave_atingida tira naves "
                              "(3 → 2 → 1 → 0), esvazia aliens e balas e, quando não há mais naves, faz game_active = False.")])],
    },
}


# ---------------------------------------------------------------------------
# CAPÍTULO 14: Alien Invasion, pontuação
# ---------------------------------------------------------------------------

CAP14 = {
    "num": 14,
    "titulo": "Alien Invasion: Placar",
    "subtitulo": "Botão Play, níveis, pontos e recorde",
    "licoes": [
        {
            "titulo": "O botão Play",
            "texto": [
                "Agora o jogo começa **parado** (`game_active = False`) e espera o jogador clicar em **Play**.",
                "O botão é só um `Rect` no centro da tela. Quando chega um evento `MOUSEBUTTONDOWN`, o livro pega a "
                "posição do mouse com `pygame.mouse.get_pos()` e testa `botao.rect.collidepoint(posicao)`: True se o "
                "ponto está dentro do retângulo.",
                "## Cuidado com o botão invisível",
                "Durante a partida o botão não aparece, mas a área dele continua lá! Por isso o livro só reage ao clique "
                "se `not game_active`. Ao começar: zera as estatísticas, esvazia aliens e balas, cria a frota e liga "
                "`game_active`.",
            ],
            "exemplo": _c('''
import pygame

tela = pygame.Rect(0, 0, 1200, 800)
botao = pygame.Rect(0, 0, 200, 50)
botao.center = tela.center
print("Botão Play em:", botao)

game_active = False
for clique in [(10, 10), (600, 400), (610, 410)]:
    if botao.collidepoint(clique) and not game_active:
        game_active = True
        print(clique, "-> Partida começou!")
    else:
        print(clique, "-> nada acontece")
'''),
        },
        {
            "titulo": "Subindo de nível",
            "texto": [
                "Quando a frota é destruída, o jogo fica mais rápido. O livro separa as configurações em dois tipos:",
                "• **Fixas** (tamanho da tela, `speedup_scale = 1.1`...), definidas no `__init__`.",
                "• **Dinâmicas** (velocidades da nave, das balas e dos aliens), definidas em `initialize_dynamic_settings()`.",
                "`increase_speed()` multiplica as velocidades por `speedup_scale`. Ao clicar em Play de novo, o jogo chama "
                "`initialize_dynamic_settings()` para voltar tudo ao normal.",
            ],
            "exemplo": _c('''
class Settings:
    def __init__(self):
        self.speedup_scale = 1.1
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.alien_speed = 1.0

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale


s = Settings()
for nivel in range(1, 5):
    print(f"Nível {nivel}: nave {s.ship_speed:.2f}, aliens {s.alien_speed:.2f}")
    s.increase_speed()

s.initialize_dynamic_settings()
print("Nova partida: aliens", s.alien_speed)
'''),
        },
        {
            "titulo": "Marcando pontos",
            "texto": [
                "A pontuação mora em `GameStats`: `self.score = 0` dentro de `reset_stats()`, porque ela zera a cada partida.",
                "Cada alien vale `settings.alien_points` (50 no começo). Como `groupcollide` devolve `{bala: [aliens]}`, "
                "o livro soma assim, para contar todos os aliens que uma bala acertou:",
                "`for aliens in colisoes.values(): stats.score += settings.alien_points * len(aliens)`",
                "A cada nível os aliens valem mais: `alien_points = int(alien_points * score_scale)`, com `score_scale = 1.5`.",
                "## Placar arredondado",
                "O livro arredonda para dezenas com `round(score, -1)` e separa os milhares com `f\"{numero:,}\"`. Esse "
                "formato usa vírgula, como nos EUA. Em português, troque por ponto com `.replace(',', '.')`.",
            ],
            "exemplo": _c('''
alien_points = 50
score = 0

colisoes = {"bala1": ["alien1"], "bala2": ["alien2", "alien3"]}
for atingidos in colisoes.values():
    score += alien_points * len(atingidos)
print("Pontos:", score)

alien_points = int(alien_points * 1.5)
print("No próximo nível cada alien vale", alien_points)

placar = 1234567
print(f"{round(placar, -1):,}")
print(f"{round(placar, -1):,}".replace(",", "."))
'''),
        },
        {
            "titulo": "Recorde e nível",
            "texto": [
                "O recorde (`high_score`) fica no `__init__` de GameStats, **não** em `reset_stats()`. Assim ele sobrevive "
                "a uma nova partida.",
                "`check_high_score()` compara: se `score > high_score`, o recorde passa a ser a pontuação atual.",
                "O nível (`level`) começa em 1 em `reset_stats()` e sobe sempre que a frota é destruída.",
                "## Recorde para sempre",
                "Um exercício do livro junta tudo com o capítulo 10: salvar o recorde num arquivo JSON ao sair e "
                "carregá-lo ao abrir o jogo, usando `Path`, `json.dumps` e `json.loads`.",
            ],
            "exemplo": _c('''
import json
from pathlib import Path

path = Path("recorde.json")
if path.exists():
    recorde = json.loads(path.read_text())
else:
    recorde = 0
print("Recorde carregado:", recorde)

pontos = 2450
if pontos > recorde:
    recorde = pontos
    print("Novo recorde!")

path.write_text(json.dumps(recorde))
print("Arquivo salvo:", path.read_text())
'''),
        },
    ],
    "quiz": [
        {"pergunta": "Por que conferir `not game_active` antes de reagir ao clique no Play?",
         "opcoes": ["Para o botão mudar de cor", "Porque a área do botão continua clicável mesmo invisível durante o jogo",
                    "Para salvar o recorde", "Porque o mouse não funciona durante o jogo"], "correta": 1,
         "explicacao": "Sem esse teste, clicar naquela região no meio da partida reiniciaria o jogo."},
        {"pergunta": "O que `rect.collidepoint(pos)` verifica?",
         "opcoes": ["Se dois retângulos se tocam", "Se o ponto pos está dentro do retângulo", "Se o mouse foi clicado",
                    "A distância até pos"], "correta": 1,
         "explicacao": "collidepoint testa um ponto; colliderect testa outro retângulo."},
        {"pergunta": "O que é mostrado?", "codigo": "speed = 1.0\nfor _ in range(2):\n    speed *= 1.1\nprint(round(speed, 2))",
         "opcoes": ["1.2", "1.21", "2.2", "1.1"], "correta": 1,
         "explicacao": "1.0 × 1.1 × 1.1 = 1.21. A velocidade cresce em porcentagem, não somando."},
        {"pergunta": "Por que high_score fica no __init__ de GameStats e não em reset_stats()?",
         "opcoes": ["Por estilo", "Para não zerar o recorde a cada nova partida",
                    "Porque reset_stats não pode ter atributos", "Para o jogo ficar mais rápido"], "correta": 1,
         "explicacao": "reset_stats() roda a cada partida; o __init__ roda uma vez só."},
        {"pergunta": "O que é mostrado?", "codigo": "print(f\"{round(12347, -1):,}\")",
         "opcoes": ["12347", "12,350", "12.350", "12,340"], "correta": 1,
         "explicacao": "round(..., -1) arredonda para 12350 e :, coloca a vírgula dos milhares."},
        {"pergunta": "Um tiro acerta 2 aliens ao mesmo tempo, e cada um vale 50. Seguindo o livro, quantos pontos o jogador ganha?",
         "opcoes": ["50", "100", "0", "25"], "correta": 1,
         "explicacao": "alien_points * len(aliens) = 50 * 2 = 100."},
        {"pergunta": "Por que chamar initialize_dynamic_settings() quando o jogador clica em Play?",
         "opcoes": ["Para voltar as velocidades ao início numa nova partida", "Para abrir a janela",
                    "Para salvar o jogo", "Para trocar a cor do botão"], "correta": 0,
         "explicacao": "Senão a nova partida começaria na velocidade em que a anterior terminou."},
    ],
    "desafios": [
        {
            "titulo": "Clique no Play",
            "enunciado": "Crie a função `clicou_play(botao_rect, pos, game_active)` que devolve True só quando o ponto pos "
                         "está dentro do botão E o jogo não está ativo.",
            "inicial": _c('''
import pygame


def clicou_play(botao_rect, pos, game_active):
    pass


botao = pygame.Rect(500, 375, 200, 50)
print(clicou_play(botao, (600, 400), False))
''') + "\n",
            "dica": "return botao_rect.collidepoint(pos) and not game_active",
            "solucao": _c('''
import pygame


def clicou_play(botao_rect, pos, game_active):
    return botao_rect.collidepoint(pos) and not game_active


botao = pygame.Rect(500, 375, 200, 50)
print(clicou_play(botao, (600, 400), False))
'''),
            "casos": [caso([funcao("clicou_play"),
                            regra(lambda o, n, c: _teste_play(n),
                                  "Teste com o botão Rect(500, 375, 200, 50): clicar em (600, 400) com o jogo parado → True; "
                                  "com o jogo ativo → False; clicar em (10, 10) → False.")])],
        },
        {
            "titulo": "Acelerando",
            "enunciado": "Crie a classe `Settings`:\n"
                         "• no __init__: speedup_scale = 1.1, score_scale = 1.5 e uma chamada a initialize_dynamic_settings()\n"
                         "• initialize_dynamic_settings(): ship_speed = 1.5, bullet_speed = 2.5, alien_speed = 1.0, "
                         "fleet_direction = 1, alien_points = 50\n"
                         "• increase_speed(): multiplica as três velocidades por speedup_scale e faz "
                         "alien_points = int(alien_points * score_scale)",
            "inicial": "class Settings:\n    pass\n",
            "dica": "Use self.speedup_scale e self.score_scale dentro de increase_speed(). O int() corta os decimais dos pontos.",
            "solucao": _c('''
class Settings:
    def __init__(self):
        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
'''),
            "casos": [caso([classe("Settings"),
                            regra(lambda o, n, c: _teste_acelerar(n),
                                  "Teste: os valores iniciais devem ser os do enunciado; depois de increase_speed(), "
                                  "ship_speed ≈ 1.65, bullet_speed ≈ 2.75, alien_speed ≈ 1.1 e alien_points = 75; depois de "
                                  "outro, alien_points = 112; e initialize_dynamic_settings() volta tudo ao início (inclusive "
                                  "fleet_direction = 1).")])],
        },
        {
            "titulo": "Somando pontos",
            "enunciado": "Crie a função `pontos_colisoes(colisoes, alien_points)` que recebe o dicionário devolvido por "
                         "groupcollide ({bala: [aliens]}) e devolve quantos pontos ganhar.\n\n"
                         "Exemplo: pontos_colisoes({'b1': ['a1'], 'b2': ['a2', 'a3']}, 50) devolve 150.",
            "inicial": _c('''
def pontos_colisoes(colisoes, alien_points):
    pass


print(pontos_colisoes({"b1": ["a1"], "b2": ["a2", "a3"]}, 50))
''') + "\n",
            "dica": "Percorra colisoes.values() e some alien_points * len(lista).",
            "solucao": _c('''
def pontos_colisoes(colisoes, alien_points):
    total = 0
    for atingidos in colisoes.values():
        total += alien_points * len(atingidos)
    return total


print(pontos_colisoes({"b1": ["a1"], "b2": ["a2", "a3"]}, 50))
'''),
            "casos": [caso([funcao("pontos_colisoes"),
                            chama("pontos_colisoes", ({"b1": ["a1"], "b2": ["a2", "a3"]}, 50), 150),
                            chama("pontos_colisoes", ({}, 50), 0),
                            chama("pontos_colisoes", ({"b": ["a", "b", "c", "d"]}, 75), 300)])],
        },
        {
            "titulo": "Placar brasileiro",
            "enunciado": "Crie a função `formatar_placar(score)` que arredonda para a dezena mais próxima e separa os "
                         "milhares com PONTO.\n\nExemplos: 12347 → '12.350'; 1234567 → '1.234.570'; 42 → '40'.",
            "inicial": _c('''
def formatar_placar(score):
    pass


print(formatar_placar(12347))
''') + "\n",
            "dica": "f\"{round(score, -1):,}\" dá '12,350'. Depois troque a vírgula por ponto com .replace(',', '.').",
            "solucao": _c('''
def formatar_placar(score):
    return f"{round(score, -1):,}".replace(",", ".")


print(formatar_placar(12347))
'''),
            "casos": [caso([funcao("formatar_placar"),
                            regra(lambda o, n, c: _teste_placar(n),
                                  "Teste: formatar_placar(12347) → '12.350', (1234567) → '1.234.570', (998) → '1.000', "
                                  "(42) → '40' e (0) → '0'. O resultado precisa ser uma string.")])],
        },
        {
            "titulo": "Novo recorde",
            "enunciado": "Crie a classe `GameStats(settings)`:\n"
                         "• no __init__: guarda settings, chama reset_stats() e cria high_score = 0\n"
                         "• reset_stats(): ships_left = settings.ship_limit, score = 0, level = 1\n"
                         "• check_high_score(): se score > high_score, high_score recebe score",
            "inicial": "class GameStats:\n    pass\n",
            "dica": "O high_score fica no __init__, fora do reset_stats(), para não zerar a cada partida.",
            "solucao": _c('''
class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
'''),
            "casos": [caso([classe("GameStats"),
                            regra(lambda o, n, c: _teste_recorde(n),
                                  "Teste: começa com score 0, level 1, ships_left = ship_limit e high_score 0; com score 1500, "
                                  "check_high_score() leva o recorde a 1500; reset_stats() zera score e level, mas mantém o "
                                  "recorde; uma partida de 700 pontos não muda o recorde.")])],
        },
        {
            "titulo": "Caça-bugs: o recorde que some",
            "enunciado": "O jogador fez 1500 pontos, depois 700. O recorde deveria ser 1500, mas o programa mostra 700. "
                         "Conserte a classe para mostrar 'Recorde: 1500'.",
            "inicial": _c('''
class GameStats:
    def __init__(self):
        self.reset_stats()

    def reset_stats(self):
        self.score = 0
        self.high_score = 0

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score


stats = GameStats()
stats.score = 1500
stats.check_high_score()

stats.reset_stats()      # nova partida
stats.score = 700
stats.check_high_score()
print(f"Recorde: {stats.high_score}")
''') + "\n",
            "dica": "Qual método roda a cada nova partida? O recorde não deveria estar nele.",
            "solucao": _c('''
class GameStats:
    def __init__(self):
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        self.score = 0

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score


stats = GameStats()
stats.score = 1500
stats.check_high_score()

stats.reset_stats()      # nova partida
stats.score = 700
stats.check_high_score()
print(f"Recorde: {stats.high_score}")
'''),
            "casos": [caso([saida("Recorde: 1500")])],
        },
    ],
    "chefe": {
        "titulo": "O Placar Eterno",
        "enunciado": "Crie a classe `GameStats(settings)`, que guarda o recorde no arquivo 'recorde.json':\n\n"
                     "• __init__: guarda settings, chama reset_stats(), cria game_active = False e carrega high_score do "
                     "arquivo (se ele não existir, high_score = 0)\n"
                     "• reset_stats(): ships_left = settings.ship_limit, score = 0, level = 1\n"
                     "• registrar_abates(colisoes): soma settings.alien_points * len(aliens) para cada lista do dicionário "
                     "e, se o score passar do recorde, atualiza o high_score\n"
                     "• salvar_recorde(): grava o high_score no arquivo como JSON\n\n"
                     "A simulação no fim do código já está pronta. O Verificar roda com o arquivo valendo 800, sem arquivo e valendo 5000.",
        "inicial": _c('''
import json
from pathlib import Path


class Settings:
    def __init__(self):
        self.ship_limit = 3
        self.alien_points = 50


class GameStats:
    pass


# --- Simulação de uma partida (não precisa mexer) ---
settings = Settings()
stats = GameStats(settings)
print(f"Recorde carregado: {stats.high_score}")
stats.registrar_abates({"bala1": ["alien1", "alien2"], "bala2": ["alien3"]})
print(f"Pontos: {stats.score} | Recorde: {stats.high_score}")
stats.registrar_abates({"bala3": ["alien"] * 15})
print(f"Pontos: {stats.score} | Recorde: {stats.high_score}")
stats.reset_stats()
print(f"Nova partida: pontos {stats.score}, nível {stats.level}, vidas {stats.ships_left}, recorde {stats.high_score}")
stats.salvar_recorde()
''') + "\n",
        "dica": "Para carregar: path = Path('recorde.json'); if path.exists(): self.high_score = json.loads(path.read_text()). "
                "Para salvar: path.write_text(json.dumps(self.high_score)).",
        "solucao": _c('''
import json
from pathlib import Path


class Settings:
    def __init__(self):
        self.ship_limit = 3
        self.alien_points = 50


class GameStats:
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = False
        self.path = Path("recorde.json")
        if self.path.exists():
            self.high_score = json.loads(self.path.read_text())
        else:
            self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def registrar_abates(self, colisoes):
        for aliens in colisoes.values():
            self.score += self.settings.alien_points * len(aliens)
        if self.score > self.high_score:
            self.high_score = self.score

    def salvar_recorde(self):
        self.path.write_text(json.dumps(self.high_score))


# --- Simulação de uma partida (não precisa mexer) ---
settings = Settings()
stats = GameStats(settings)
print(f"Recorde carregado: {stats.high_score}")
stats.registrar_abates({"bala1": ["alien1", "alien2"], "bala2": ["alien3"]})
print(f"Pontos: {stats.score} | Recorde: {stats.high_score}")
stats.registrar_abates({"bala3": ["alien"] * 15})
print(f"Pontos: {stats.score} | Recorde: {stats.high_score}")
stats.reset_stats()
print(f"Nova partida: pontos {stats.score}, nível {stats.level}, vidas {stats.ships_left}, recorde {stats.high_score}")
stats.salvar_recorde()
'''),
        "casos": _casos_placar_eterno(),
    },
}


# ---------------------------------------------------------------------------
# PARTE II: PROJETO VISUALIZAÇÃO DE DADOS (capítulos 15 a 17)
# Gráficos com matplotlib (viram imagens no painel de saída), arquivos CSV/JSON
# de exemplo e um "requests de treino" com respostas simuladas.
# ---------------------------------------------------------------------------

import random as _random


def _eixos(ns):
    return [ax for f in ns.get("__figuras__", []) for ax in f.axes]


def _linhas(ns):
    return [l for ax in _eixos(ns) for l in ax.lines]


def _num(v):
    try:
        return round(float(v), 6)
    except (TypeError, ValueError):
        return v


def _ys(linha):
    return [_num(v) for v in linha.get_ydata()]


def _xs(linha):
    return [_num(v) for v in linha.get_xdata()]


def _pontos_scatter(ns):
    out = []
    for ax in _eixos(ns):
        for c in ax.collections:
            if type(c).__name__ == "PathCollection":
                out.append([(round(float(x), 6), round(float(y), 6)) for x, y in c.get_offsets()])
    return out


def _barras(ns, horizontal=False):
    out = []
    for ax in _eixos(ns):
        rects = [p for p in ax.patches if type(p).__name__ == "Rectangle"]
        if rects:
            if horizontal:
                out.append([round(float(p.get_width()), 6) for p in rects])
            else:
                out.append([(round(p.get_x() + p.get_width() / 2, 6), round(float(p.get_height()), 6)) for p in rects])
    return out


def _tem_preenchimento(ns):
    return any("PolyCollection" in type(c).__name__ for ax in _eixos(ns) for c in ax.collections)


def tem_grafico(n=1):
    return (lambda o, ns, c: len(ns.get("__figuras__", [])) >= n,
            "Nenhum gráfico foi criado. Use fig, ax = plt.subplots() e desenhe nele." if n == 1
            else f"Crie pelo menos {n} gráficos.")


def titulo_com(trecho):
    return (lambda o, ns, c: any(trecho.lower() in ax.get_title().lower() for ax in _eixos(ns)),
            f"O gráfico precisa de um título com '{trecho}' (ax.set_title).")


def rotulos_eixos():
    return (lambda o, ns, c: any(ax.get_xlabel().strip() and ax.get_ylabel().strip() for ax in _eixos(ns)),
            "Dê nome aos eixos com ax.set_xlabel(...) e ax.set_ylabel(...).")


def linha_com(ys, msg=None):
    alvo = [_num(v) for v in ys]
    return (lambda o, ns, c: any(_ys(l) == alvo for l in _linhas(ns)),
            msg or f"O gráfico precisa de uma linha (ax.plot) com os valores y = {ys}.")


# ------------------------- dados de exemplo (simulados) -------------------------

def _clima(estacao, seed, dias=31, faltas=(), base=22, ano=2025, mes=7):
    r = _random.Random(seed)
    linhas = ["ESTACAO,DATA,CHUVA_MM,TMAX,TMIN"]
    dados = []
    for d in range(1, dias + 1):
        data = f"{ano}-{mes:02d}-{d:02d}"
        tmax = base + r.randint(-4, 6)
        tmin = tmax - r.randint(6, 11)
        chuva = r.choice([0, 0, 0, 1.2, 3.5, 8.0, 12.4])
        if d in faltas:
            linhas.append(f"{estacao},{data},,,")
            dados.append((data, None, None))
        else:
            linhas.append(f"{estacao},{data},{chuva},{tmax},{tmin}")
            dados.append((data, tmax, tmin))
    return "\n".join(linhas) + "\n", dados


CLIMA_A, DADOS_A = _clima("SERRA AZUL", 7)
CLIMA_B, DADOS_B = _clima("VALE VERDE", 21, dias=30, base=27, mes=1, ano=2026)
CLIMA_FALTA_A, DADOS_FALTA_A = _clima("SERRA AZUL", 7, faltas=(3, 17, 18))
CLIMA_FALTA_B, DADOS_FALTA_B = _clima("VALE VERDE", 21, dias=30, base=27, mes=1, ano=2026, faltas=(9,))


def _terremotos(seed, n):
    import json
    lugares = ["Ilha da Neblina", "Serra do Trovão", "Baía dos Ventos", "Vale Esquecido", "Cabo das Gaivotas",
               "Planalto Rubro", "Fossa Profunda", "Arquipélago Sereno", "Costa Dourada", "Lago Espelhado",
               "Monte Fumegante", "Deserto de Sal"]
    r = _random.Random(seed)
    feats = []
    for i in range(n):
        mag = round(r.uniform(2.5, 7.2), 1)
        lon = round(r.uniform(-170, 170), 2)
        lat = round(r.uniform(-60, 65), 2)
        lugar = f"{r.randint(5, 180)} km de {lugares[(i * 7 + seed) % len(lugares)]}"
        feats.append({"type": "Feature",
                      "properties": {"mag": mag, "place": lugar, "title": f"M {mag} - {lugar}"},
                      "geometry": {"type": "Point", "coordinates": [lon, lat, round(r.uniform(5, 300), 1)]}})
    dados = {"type": "FeatureCollection",
             "metadata": {"title": "Terremotos de exemplo (dados simulados)", "count": n},
             "features": feats}
    return json.dumps(dados, ensure_ascii=False, indent=2), feats


TERREMOTOS_A, FEATS_A = _terremotos(3, 12)
TERREMOTOS_B, FEATS_B = _terremotos(11, 9)


def _clima_ctx(texto, nome="clima.csv"):
    return {"__arquivos__": {nome: texto}}


def _quake_ctx(texto):
    return {"__arquivos__": {"terremotos.json": texto}}


# ------------------------------ testes do cap. 15 ------------------------------

def _teste_passeio(ns):
    R = ns["RandomWalk"]
    w = R()
    if getattr(w, "num_points", None) != 5000:
        return False
    w = R(300)
    w.fill_walk()
    xs, ys = w.x_values, w.y_values
    if len(xs) != 300 or len(ys) != 300 or xs[0] != 0 or ys[0] != 0:
        return False
    passos = [(xs[i + 1] - xs[i], ys[i + 1] - ys[i]) for i in range(299)]
    if any(dx == 0 and dy == 0 for dx, dy in passos):
        return False
    if any(abs(dx) > 4 or abs(dy) > 4 for dx, dy in passos):
        return False
    return len(set(passos)) > 5


def _teste_dado(ns):
    D = ns["Die"]
    d = D()
    if d.num_sides != 6:
        return False
    vistos = {d.roll() for _ in range(600)}
    if vistos != set(range(1, 7)):
        return False
    d10 = D(10)
    vistos = {d10.roll() for _ in range(1000)}
    return vistos == set(range(1, 11))


def _teste_cassino(ns):
    f = ns["somar_dados"]
    r = f(500)
    if len(r) != 500 or min(r) < 2 or max(r) > 12 or len(set(r)) < 9:
        return False
    for barras in _barras(ns):
        xs = [round(x) for x, _ in barras]
        if xs == list(range(2, 13)) and sum(h for _, h in barras) == 1000:
            return True
    return False


# ------------------------------ testes do cap. 16 ------------------------------

def _resumo_clima(dados):
    validos = [d for d in dados if d[1] is not None]
    mx = max(validos, key=lambda d: d[1])
    mn = min(validos, key=lambda d: d[2])
    faltas = [d[0] for d in dados if d[1] is None]
    return mx, mn, faltas, validos


def _casos_meteorologista():
    casos = []
    for texto, dados in ((CLIMA_FALTA_A, DADOS_FALTA_A), (CLIMA_FALTA_B, DADOS_FALTA_B)):
        mx, mn, faltas, validos = _resumo_clima(dados)
        esperado = (f"Máxima do período: {mx[1]} em {mx[0]}\n"
                    f"Mínima do período: {mn[2]} em {mn[0]}\n"
                    f"Dias sem dados: {len(faltas)}")
        casos.append(caso([
            saida(esperado), tem_grafico(),
            linha_com([d[1] for d in validos], "O gráfico precisa de uma linha com as máximas dos dias válidos."),
            linha_com([d[2] for d in validos], "O gráfico precisa de uma linha com as mínimas dos dias válidos."),
            regra(lambda o, n, c: _tem_preenchimento(n),
                  "Pinte o espaço entre as linhas com ax.fill_between(datas, maximas, minimas, alpha=0.1)."),
        ], _clima_ctx(texto)))
    return casos


def _casos_maximas():
    casos = []
    for texto, dados in ((CLIMA_A, DADOS_A), (CLIMA_B, DADOS_B)):
        maximas = [d[1] for d in dados]
        casos.append(caso([var_igual("maximas", maximas), tem_grafico(), linha_com(maximas)], _clima_ctx(texto)))
    return casos


def _casos_faltando():
    casos = []
    for texto, dados in ((CLIMA_FALTA_A, DADOS_FALTA_A), (CLIMA_FALTA_B, DADOS_FALTA_B)):
        validos = [d for d in dados if d[1] is not None]
        linhas_txt = "\n".join(f"Faltando dados para {d[0]}" for d in dados if d[1] is None)
        esperado = linhas_txt + f"\nDias válidos: {len(validos)}"
        casos.append(caso([saida(esperado), var_igual("maximas", [d[1] for d in validos])], _clima_ctx(texto)))
    return casos


def _casos_cabecalho():
    return [caso([saida("0 ESTACAO\n1 DATA\n2 CHUVA_MM\n3 TMAX\n4 TMIN")], _clima_ctx(CLIMA_A))]


def _casos_bug_csv():
    casos = []
    for texto, dados in ((CLIMA_A, DADOS_A), (CLIMA_B, DADOS_B)):
        casos.append(caso([saida(f"Maior máxima: {max(d[1] for d in dados)}")], _clima_ctx(texto)))
    return casos


def _casos_fortes():
    casos = []
    for texto, feats in ((TERREMOTOS_A, FEATS_A), (TERREMOTOS_B, FEATS_B)):
        fortes = [f["properties"]["title"] for f in feats if f["properties"]["mag"] >= 5]
        esperado = f"Total de terremotos: {len(feats)}\nFortes (5 ou mais): {len(fortes)}\n" + "\n".join(fortes)
        casos.append(caso([saida(esperado)], _quake_ctx(texto)))
    return casos


def _casos_mapa():
    casos = []
    for texto, feats in ((TERREMOTOS_A, FEATS_A), (TERREMOTOS_B, FEATS_B)):
        pts = [(round(f["geometry"]["coordinates"][0], 6), round(f["geometry"]["coordinates"][1], 6)) for f in feats]
        mags = [f["properties"]["mag"] for f in feats]
        casos.append(caso([
            var_igual("mags", mags), tem_grafico(),
            regra(lambda o, n, c, pts=pts: pts in _pontos_scatter(n),
                  "O gráfico de dispersão precisa ter x = longitude e y = latitude de cada terremoto, na ordem do arquivo."),
        ], _quake_ctx(texto)))
    return casos


# ------------------------------ testes do cap. 17 ------------------------------

def _api_itens(ling):
    import sys
    return sys.modules["requests"].get(
        f"https://api.github.com/search/repositories?q=language:{ling}+sort:stars").json()["items"]


def _esperado_top3():
    linhas = []
    for repo in _api_itens("python")[:3]:
        linhas.append(f"{repo['name']} (de {repo['owner']['login']}): {repo['stargazers_count']} estrelas")
    return "\n".join(linhas)


def _esperado_status():
    import sys
    r = sys.modules["requests"].get("https://api.github.com/search/repositories?q=language:python+sort:stars")
    return f"Status: {r.status_code}\nTotal de repositórios: {r.json()['total_count']}"


def _esperado_hn():
    import sys
    rq = sys.modules["requests"]
    ids = rq.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:5]
    itens = [rq.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json").json() for i in ids]
    itens.sort(key=lambda d: d["descendants"], reverse=True)
    return "\n".join(f"{d['title']} - {d['descendants']} comentários" for d in itens)


def _teste_buscar(ns):
    f = ns["buscar"]
    ok = f("https://hacker-news.firebaseio.com/v0/item/40101.json")
    if not isinstance(ok, dict) or ok.get("id") != 40101:
        return False
    return f("https://api.github.com/nao-existe") is None


def _teste_barras_api(ns):
    estrelas = [r["stargazers_count"] for r in _api_itens("python")]
    alvo = [round(float(v), 6) for v in estrelas]
    return any(sorted(b) == sorted(alvo) for b in _barras(ns, horizontal=True))


def _teste_ranking(ns):
    f = ns["ranking_linguagem"]
    for ling in ("python", "javascript", "rust"):
        esperado = sorted(((r["name"], r["stargazers_count"]) for r in _api_itens(ling)),
                          key=lambda t: t[1], reverse=True)[:5]
        res = f(ling)
        if [tuple(t) for t in (res or [])] != esperado:
            return False
    return f("cobol") == []


# ---------------------------------------------------------------------------
# CAPÍTULO 15: Gerando dados
# ---------------------------------------------------------------------------

CAP15 = {
    "num": 15,
    "titulo": "Dados: Gerando Gráficos",
    "subtitulo": "matplotlib, dispersão, passeio aleatório e dados",
    "licoes": [
        {
            "titulo": "Seu primeiro gráfico",
            "texto": [
                "Começa o projeto de **visualização de dados**: transformar números em imagens que contam uma história.",
                "A biblioteca mais usada é a **matplotlib**. Por convenção, importamos assim: `import matplotlib.pyplot as plt`.",
                "`fig, ax = plt.subplots()` cria uma **figura** (a imagem inteira) e um **eixo** `ax` (o gráfico em si). "
                "`ax.plot(x, y)` desenha uma linha ligando os pontos.",
                "Dê nome a tudo: `ax.set_title()`, `ax.set_xlabel()` e `ax.set_ylabel()`. "
                "`linewidth=3` engrossa a linha e `ax.tick_params(labelsize=14)` aumenta os números dos eixos.",
                "No fim, `plt.show()` mostra o gráfico. Aqui no PyQuest, ele aparece como imagem embaixo da saída. "
                "(Na primeira vez, o site leva alguns segundos para carregar o matplotlib.)",
            ],
            "exemplo": _c('''
import matplotlib.pyplot as plt

entradas = [1, 2, 3, 4, 5]
quadrados = [1, 4, 9, 16, 25]

fig, ax = plt.subplots()
ax.plot(entradas, quadrados, linewidth=3)

ax.set_title("Números ao quadrado", fontsize=20)
ax.set_xlabel("Valor", fontsize=12)
ax.set_ylabel("Quadrado do valor", fontsize=12)
ax.tick_params(labelsize=12)

plt.show()
'''),
        },
        {
            "titulo": "Estilos e dispersão",
            "texto": [
                "`plt.style.use('ggplot')` muda a aparência do gráfico todo. Veja os estilos disponíveis com "
                "`print(plt.style.available)`.",
                "`ax.scatter(x, y)` desenha **pontos soltos**, sem ligar. Ótimo para muitos dados.",
                "Uma list comprehension gera os valores rapidinho: `y = [x**2 for x in x_values]`.",
                "## Cores que contam algo",
                "`c=y, cmap=plt.cm.Blues` pinta cada ponto conforme o seu valor: os pequenos ficam claros e os grandes, escuros. "
                "Isso é um **mapa de cores**.",
                "`ax.axis([0, 1100, 0, 1_100_000])` define o intervalo de cada eixo, e `plt.savefig('grafico.png')` salva a imagem num arquivo.",
            ],
            "exemplo": _c('''
import matplotlib.pyplot as plt

x_values = range(1, 1001)
y_values = [x**2 for x in x_values]

plt.style.use("ggplot")
fig, ax = plt.subplots()
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=10)

ax.set_title("Quadrados de 1 a 1000")
ax.set_xlabel("Valor")
ax.set_ylabel("Quadrado")
ax.axis([0, 1100, 0, 1_100_000])
ax.ticklabel_format(style="plain")

plt.show()
'''),
        },
        {
            "titulo": "O passeio aleatório",
            "texto": [
                "Um **passeio aleatório** é um caminho em que cada passo vai para uma direção sorteada. Ele aparece em "
                "física, biologia e finanças.",
                "A classe `RandomWalk` do livro guarda as listas `x_values` e `y_values`, começando em `[0]`. "
                "O método `fill_walk()` sorteia passos até ter `num_points` pontos:",
                "• a direção (`choice([1, -1])`) e a distância (`choice([0, 1, 2, 3, 4])`), para x e para y;",
                "• passos parados (x e y iguais a zero) são descartados com `continue`.",
                "Para ver o caminho, pinte os pontos pela ordem: `c=range(num_points)`. "
                "Cada execução gera um desenho diferente!",
            ],
            "exemplo": _c('''
from random import choice
import matplotlib.pyplot as plt


class RandomWalk:
    def __init__(self, num_points=5000):
        self.num_points = num_points
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        while len(self.x_values) < self.num_points:
            x_step = choice([1, -1]) * choice([0, 1, 2, 3, 4])
            y_step = choice([1, -1]) * choice([0, 1, 2, 3, 4])
            if x_step == 0 and y_step == 0:
                continue
            self.x_values.append(self.x_values[-1] + x_step)
            self.y_values.append(self.y_values[-1] + y_step)


rw = RandomWalk(3000)
rw.fill_walk()

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(rw.x_values, rw.y_values, c=range(rw.num_points), cmap=plt.cm.Blues, s=4)
ax.scatter(0, 0, c="green", s=60)
ax.scatter(rw.x_values[-1], rw.y_values[-1], c="red", s=60)
ax.set_aspect("equal")
ax.set_title("Passeio aleatório: verde = início, vermelho = fim")
plt.show()
'''),
        },
        {
            "titulo": "Rolando dados",
            "texto": [
                "Com `randint` simulamos dados. A classe `Die` do livro tem `num_sides` (padrão 6) e o método `roll()`.",
                "Rolando mil vezes e contando cada face com `resultados.count(valor)`, temos as **frequências**. "
                "Um gráfico de **barras** (`ax.bar(x, alturas)`) mostra se o dado é justo.",
                "Somando DOIS dados, o 7 aparece muito mais que o 2 ou o 12: há mais combinações que dão 7.",
                "O livro usa a biblioteca **Plotly** para essa parte, que gera gráficos interativos. Aqui usamos o "
                "matplotlib, mas a ideia é a mesma.",
            ],
            "exemplo": _c('''
from random import randint
import matplotlib.pyplot as plt


class Die:
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return randint(1, self.num_sides)


d1, d2 = Die(), Die()
resultados = [d1.roll() + d2.roll() for _ in range(1000)]

somas = list(range(2, 13))
frequencias = [resultados.count(s) for s in somas]
print(dict(zip(somas, frequencias)))

fig, ax = plt.subplots()
ax.bar(somas, frequencias)
ax.set_xticks(somas)
ax.set_title("Dois dados de 6 lados, 1000 vezes")
ax.set_xlabel("Soma")
ax.set_ylabel("Frequência")
plt.show()
'''),
        },
    ],
    "quiz": [
        {"pergunta": "Qual é a forma mais comum de importar o matplotlib?",
         "opcoes": ["import matplotlib as m", "import matplotlib.pyplot as plt", "from plot import *", "import pyplot"],
         "correta": 1, "explicacao": "plt é o apelido padrão para matplotlib.pyplot."},
        {"pergunta": "O que `fig, ax = plt.subplots()` cria?",
         "opcoes": ["Só uma lista", "Uma figura e um eixo (o gráfico) para desenhar", "Um arquivo PNG", "Uma janela de jogo"],
         "correta": 1, "explicacao": "fig é a imagem toda; ax é a área onde você desenha."},
        {"pergunta": "Qual é a diferença entre ax.plot() e ax.scatter()?",
         "opcoes": ["Nenhuma", "plot liga os pontos com linha; scatter desenha pontos soltos",
                    "scatter só aceita 2 pontos", "plot só funciona com textos"], "correta": 1,
         "explicacao": "Linha para tendências, dispersão para muitos pontos individuais."},
        {"pergunta": "O que é mostrado?", "codigo": "x = [1, 2, 3]\ny = [v**2 for v in x]\nprint(y)",
         "opcoes": ["[1, 2, 3]", "[2, 4, 6]", "[1, 4, 9]", "[1, 8, 27]"], "correta": 2,
         "explicacao": "A list comprehension eleva cada valor ao quadrado."},
        {"pergunta": "No passeio aleatório, por que descartar o passo com x_step e y_step iguais a 0?",
         "opcoes": ["Porque daria erro", "Porque o ponto não sairia do lugar", "Para o gráfico ficar azul", "Para economizar memória"],
         "correta": 1, "explicacao": "Um passo (0, 0) repetiria o mesmo ponto."},
        {"pergunta": "O que `c=y_values, cmap=plt.cm.Blues` faz num scatter?",
         "opcoes": ["Pinta tudo de azul igual", "Pinta cada ponto num tom de azul conforme seu valor",
                    "Deixa o fundo azul", "Esconde os pontos"], "correta": 1,
         "explicacao": "É um mapa de cores: valores menores ficam claros, maiores ficam escuros."},
        {"pergunta": "Somando dois dados de 6 lados, qual soma aparece com mais frequência?",
         "opcoes": ["2", "7", "12", "Todas iguais"], "correta": 1,
         "explicacao": "Há 6 combinações que dão 7, contra só 1 para o 2 e 1 para o 12."},
    ],
    "desafios": [
        {
            "titulo": "Cubos",
            "enunciado": "Faça um gráfico de LINHA com os cubos de 1 a 5 (x = 1, 2, 3, 4, 5 e y = 1, 8, 27, 64, 125). "
                         "Use o título 'Cubos' e dê nome aos dois eixos.",
            "inicial": "import matplotlib.pyplot as plt\n\n# Seu código aqui\n",
            "dica": "y = [x**3 for x in x_values]; depois fig, ax = plt.subplots() e ax.plot(x_values, y).",
            "solucao": _c('''
import matplotlib.pyplot as plt

x_values = [1, 2, 3, 4, 5]
cubos = [x**3 for x in x_values]

fig, ax = plt.subplots()
ax.plot(x_values, cubos, linewidth=3)
ax.set_title("Cubos")
ax.set_xlabel("Valor")
ax.set_ylabel("Cubo do valor")
plt.show()
'''),
            "casos": [caso([tem_grafico(), linha_com([1, 8, 27, 64, 125]), titulo_com("Cubos"), rotulos_eixos()])],
        },
        {
            "titulo": "Chuva de pontos",
            "enunciado": "Faça um gráfico de DISPERSÃO (ax.scatter) com os números de 1 a 50 no eixo x e seus quadrados no "
                         "eixo y, colorindo os pontos pelo valor de y com o mapa de cores plt.cm.Greens.",
            "inicial": "import matplotlib.pyplot as plt\n\n# Seu código aqui\n",
            "dica": "x_values = range(1, 51). No scatter: c=y_values, cmap=plt.cm.Greens.",
            "solucao": _c('''
import matplotlib.pyplot as plt

x_values = range(1, 51)
y_values = [x**2 for x in x_values]

fig, ax = plt.subplots()
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Greens, s=20)
ax.set_title("Quadrados de 1 a 50")
plt.show()
'''),
            "casos": [caso([tem_grafico(),
                            regra(lambda o, n, c: [(float(x), float(x * x)) for x in range(1, 51)] in _pontos_scatter(n),
                                  "O scatter precisa ter os 50 pontos (x, x²) para x de 1 a 50."),
                            tem("cmap", "Use o parâmetro cmap para colorir os pontos.")])],
        },
        {
            "titulo": "O andarilho",
            "enunciado": "Crie a classe `RandomWalk(num_points=5000)` com x_values e y_values começando em [0] e o método "
                         "fill_walk(), que sorteia passos (direção 1 ou -1, distância de 0 a 4, para x e para y), descarta "
                         "passos parados e para quando houver num_points pontos.",
            "inicial": "from random import choice\n\n\nclass RandomWalk:\n    pass\n",
            "dica": "while len(self.x_values) < self.num_points: ... e use continue quando x_step == 0 and y_step == 0.",
            "solucao": _c('''
from random import choice


class RandomWalk:
    def __init__(self, num_points=5000):
        self.num_points = num_points
        self.x_values = [0]
        self.y_values = [0]

    def fill_walk(self):
        while len(self.x_values) < self.num_points:
            x_step = choice([1, -1]) * choice([0, 1, 2, 3, 4])
            y_step = choice([1, -1]) * choice([0, 1, 2, 3, 4])
            if x_step == 0 and y_step == 0:
                continue
            self.x_values.append(self.x_values[-1] + x_step)
            self.y_values.append(self.y_values[-1] + y_step)
'''),
            "casos": [caso([classe("RandomWalk"),
                            regra(lambda o, n, c: _teste_passeio(n),
                                  "Teste: RandomWalk() tem num_points 5000; RandomWalk(300).fill_walk() gera listas com 300 "
                                  "pontos começando em 0, sem passos parados e com passos de no máximo 4 em cada direção.")])],
        },
        {
            "titulo": "Dado justo",
            "enunciado": "Crie a classe `Die(num_sides=6)` com o método roll(), que devolve um número aleatório de 1 até num_sides.",
            "inicial": "from random import randint\n\n\nclass Die:\n    pass\n",
            "dica": "return randint(1, self.num_sides)",
            "solucao": _c('''
from random import randint


class Die:
    def __init__(self, num_sides=6):
        self.num_sides = num_sides

    def roll(self):
        return randint(1, self.num_sides)
'''),
            "casos": [caso([classe("Die"),
                            regra(lambda o, n, c: _teste_dado(n),
                                  "Teste: Die() tem 6 lados e, em 600 rolagens, sai cada valor de 1 a 6 (e nada fora disso); "
                                  "Die(10) sorteia de 1 a 10.")])],
        },
        {
            "titulo": "Contando frequências",
            "enunciado": "Crie a função `frequencias(resultados, lados)` que devolve uma lista com quantas vezes cada face "
                         "(de 1 até lados) apareceu.\n\nExemplo: frequencias([1, 3, 3, 6], 6) devolve [1, 0, 2, 0, 0, 1].",
            "inicial": "def frequencias(resultados, lados):\n    pass\n\n\nprint(frequencias([1, 3, 3, 6], 6))\n",
            "dica": "[resultados.count(face) for face in range(1, lados + 1)]",
            "solucao": _c('''
def frequencias(resultados, lados):
    return [resultados.count(face) for face in range(1, lados + 1)]


print(frequencias([1, 3, 3, 6], 6))
'''),
            "casos": [caso([funcao("frequencias"),
                            chama("frequencias", ([1, 3, 3, 6], 6), [1, 0, 2, 0, 0, 1]),
                            chama("frequencias", ([], 4), [0, 0, 0, 0]),
                            chama("frequencias", ([2, 2, 2, 8, 1], 8), [1, 3, 0, 0, 0, 0, 0, 1])])],
        },
        {
            "titulo": "Caça-bugs: a curva torta",
            "enunciado": "O gráfico deveria mostrar os quadrados de 1 a 5 (1, 4, 9, 16, 25), mas a curva começa no zero e "
                         "termina no 16. Conserte.",
            "inicial": _c('''
import matplotlib.pyplot as plt

x_values = [1, 2, 3, 4, 5]
quadrados = [n**2 for n in range(5)]

fig, ax = plt.subplots()
ax.plot(x_values, quadrados)
ax.set_title("Quadrados")
plt.show()
''') + "\n",
            "dica": "range(5) vai de 0 a 4. De onde deveriam vir os valores?",
            "solucao": _c('''
import matplotlib.pyplot as plt

x_values = [1, 2, 3, 4, 5]
quadrados = [n**2 for n in x_values]

fig, ax = plt.subplots()
ax.plot(x_values, quadrados)
ax.set_title("Quadrados")
plt.show()
'''),
            "casos": [caso([tem_grafico(), linha_com([1, 4, 9, 16, 25])])],
        },
    ],
    "chefe": {
        "titulo": "O Cassino dos Dados",
        "enunciado": "Crie a função `somar_dados(n)`, que rola dois dados de 6 lados n vezes e devolve a lista com as somas.\n\n"
                     "Depois, use-a com n = 1000 e faça um gráfico de BARRAS com as frequências de cada soma de 2 a 12 "
                     "(uma barra para cada soma, em ordem). Coloque título e nome nos eixos.",
        "inicial": "from random import randint\nimport matplotlib.pyplot as plt\n\n\ndef somar_dados(n):\n    pass\n",
        "dica": "resultados = somar_dados(1000); somas = list(range(2, 13)); frequencias = [resultados.count(s) for s in somas]; "
                "ax.bar(somas, frequencias).",
        "solucao": _c('''
from random import randint
import matplotlib.pyplot as plt


def somar_dados(n):
    return [randint(1, 6) + randint(1, 6) for _ in range(n)]


resultados = somar_dados(1000)
somas = list(range(2, 13))
frequencias = [resultados.count(s) for s in somas]

fig, ax = plt.subplots()
ax.bar(somas, frequencias)
ax.set_xticks(somas)
ax.set_title("Soma de dois dados (1000 rolagens)")
ax.set_xlabel("Soma")
ax.set_ylabel("Frequência")
plt.show()
'''),
        "casos": [caso([funcao("somar_dados"), tem_grafico(), rotulos_eixos(),
                        regra(lambda o, n, c: _teste_cassino(n),
                              "Teste: somar_dados(500) devolve 500 somas entre 2 e 12; e o gráfico precisa ter 11 barras, "
                              "nas posições 2 a 12, somando 1000 no total.")])],
    },
}


# ---------------------------------------------------------------------------
# CAPÍTULO 16: Baixando dados
# ---------------------------------------------------------------------------

CAP16 = {
    "num": 16,
    "titulo": "Dados: CSV e JSON",
    "subtitulo": "Clima em CSV, datas, dados faltando e terremotos em JSON",
    "licoes": [
        {
            "titulo": "Lendo um CSV",
            "texto": [
                "Muitos dados chegam em **CSV** (valores separados por vírgula): cada linha é um registro, e a primeira "
                "costuma ser o **cabeçalho** com o nome das colunas.",
                "O módulo `csv` faz o trabalho pesado: `reader = csv.reader(linhas)` transforma cada linha numa lista. "
                "`next(reader)` pega a próxima linha; usado uma vez, pega o cabeçalho.",
                "Com `enumerate(cabecalho)` você descobre o índice de cada coluna.",
                "Nesta lição há um arquivo de exemplo, `clima.csv`, com dados **simulados** de uma estação meteorológica fictícia.",
            ],
            "exemplo": _c('''
import csv
from pathlib import Path

linhas = Path("clima.csv").read_text().splitlines()
reader = csv.reader(linhas)
cabecalho = next(reader)

for indice, coluna in enumerate(cabecalho):
    print(indice, coluna)

maximas = []
for linha in reader:
    maximas.append(int(linha[3]))
print("Máximas:", maximas)
'''),
            "ctx": _clima_ctx(CLIMA_A),
        },
        {
            "titulo": "Datas e gráficos no tempo",
            "texto": [
                "No CSV, a data é só texto: `'2025-07-04'`. Para o Python entender, use `datetime.strptime(texto, '%Y-%m-%d')`.",
                "`%Y` é o ano com 4 dígitos, `%m` o mês e `%d` o dia. Há outros, como `%B` (nome do mês) e `%H` (hora).",
                "Com datas de verdade no eixo x, o matplotlib organiza o calendário sozinho. `fig.autofmt_xdate()` inclina "
                "as datas para não ficarem encavaladas.",
            ],
            "exemplo": _c('''
import csv
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

reader = csv.reader(Path("clima.csv").read_text().splitlines())
next(reader)

datas, maximas = [], []
for linha in reader:
    datas.append(datetime.strptime(linha[1], "%Y-%m-%d"))
    maximas.append(int(linha[3]))

print("Primeiro dia:", datas[0].strftime("%d/%m/%Y"))

fig, ax = plt.subplots()
ax.plot(datas, maximas, color="red")
ax.set_title("Temperaturas máximas, julho de 2025")
ax.set_ylabel("Temperatura (°C)")
fig.autofmt_xdate()
plt.show()
'''),
            "ctx": _clima_ctx(CLIMA_A),
        },
        {
            "titulo": "Máximas, mínimas e dados faltando",
            "texto": [
                "Dá para desenhar várias linhas no mesmo eixo: chame `ax.plot()` uma vez para cada.",
                "`ax.fill_between(datas, maximas, minimas, facecolor='blue', alpha=0.1)` pinta o espaço entre as duas "
                "linhas. `alpha` é a transparência (0 = invisível, 1 = sólido).",
                "## Dados faltando",
                "Estações quebram, e o CSV fica com campos vazios. `int('')` causa `ValueError`. A solução do livro é um "
                "`try`/`except`/`else`: se der erro, avisa e pula o dia; senão, guarda os valores.",
            ],
            "exemplo": _c('''
import csv
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt

reader = csv.reader(Path("clima.csv").read_text().splitlines())
next(reader)

datas, maximas, minimas = [], [], []
for linha in reader:
    data = datetime.strptime(linha[1], "%Y-%m-%d")
    try:
        maxima = int(linha[3])
        minima = int(linha[4])
    except ValueError:
        print(f"Faltando dados para {data.date()}")
    else:
        datas.append(data)
        maximas.append(maxima)
        minimas.append(minima)

fig, ax = plt.subplots()
ax.plot(datas, maximas, color="red", alpha=0.6)
ax.plot(datas, minimas, color="blue", alpha=0.6)
ax.fill_between(datas, maximas, minimas, facecolor="blue", alpha=0.1)
ax.set_title("Máximas e mínimas (dados simulados)")
fig.autofmt_xdate()
plt.show()
'''),
            "ctx": _clima_ctx(CLIMA_FALTA_A),
        },
        {
            "titulo": "Terremotos em JSON",
            "texto": [
                "Dados geográficos costumam vir em **GeoJSON**, um JSON com uma lista de `features`. Cada feature tem "
                "`properties` (magnitude, local, título) e `geometry`, com as coordenadas `[longitude, latitude, profundidade]`.",
                "`json.loads(texto)` transforma o arquivo em dicionários e listas. Daí é só navegar: "
                "`feature['properties']['mag']`, `feature['geometry']['coordinates'][0]`...",
                "O livro desenha os terremotos num mapa-múndi com o Plotly. Aqui usamos um scatter: longitude no x, "
                "latitude no y, e o tamanho do ponto conforme a magnitude.",
                "O arquivo `terremotos.json` desta lição traz terremotos **simulados**, em lugares inventados.",
            ],
            "exemplo": _c('''
import json
from pathlib import Path
import matplotlib.pyplot as plt

dados = json.loads(Path("terremotos.json").read_text())
print(dados["metadata"]["title"])
terremotos = dados["features"]
print("Quantidade:", len(terremotos))

mags, lons, lats = [], [], []
for t in terremotos:
    mags.append(t["properties"]["mag"])
    lons.append(t["geometry"]["coordinates"][0])
    lats.append(t["geometry"]["coordinates"][1])

print("Primeiro:", terremotos[0]["properties"]["title"])

fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(lons, lats, s=[m**3 for m in mags], c=mags, cmap=plt.cm.Reds, alpha=0.7)
ax.axis([-180, 180, -90, 90])
ax.set_title("Terremotos (tamanho = magnitude)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.show()
'''),
            "ctx": _quake_ctx(TERREMOTOS_A),
        },
    ],
    "quiz": [
        {"pergunta": "O que `next(reader)` faz logo depois de criar o csv.reader?",
         "opcoes": ["Pula o arquivo todo", "Pega a primeira linha (geralmente o cabeçalho)", "Fecha o arquivo", "Conta as linhas"],
         "correta": 1, "explicacao": "next() devolve a próxima linha; a primeira é o cabeçalho."},
        {"pergunta": "Em `datetime.strptime('2025-07-04', '%Y-%m-%d')`, o que é `%m`?",
         "opcoes": ["Minutos", "Mês", "Milissegundos", "O nome do mês"], "correta": 1,
         "explicacao": "%m é o mês com dois dígitos; %M (maiúsculo) seria minutos."},
        {"pergunta": "O que `alpha=0.1` faz num gráfico?",
         "opcoes": ["Deixa a cor quase transparente", "Ordena os dados", "Aumenta a linha", "Muda o título"], "correta": 0,
         "explicacao": "alpha vai de 0 (invisível) a 1 (sólido)."},
        {"pergunta": "O que acontece com `int('')`?",
         "opcoes": ["Devolve 0", "Devolve None", "Dá ValueError", "Devolve ''"], "correta": 2,
         "explicacao": "Texto vazio não é um número. Por isso o try/except para dados faltando."},
        {"pergunta": "O que é mostrado?",
         "codigo": "import json\nd = json.loads('{\"geometry\": {\"coordinates\": [-70.5, 18.2, 10]}}')\nprint(d['geometry']['coordinates'][1])",
         "opcoes": ["-70.5", "18.2", "10", "Erro"], "correta": 1,
         "explicacao": "No GeoJSON, a ordem é [longitude, latitude, profundidade]: o índice 1 é a latitude."},
        {"pergunta": "Para que serve `fig.autofmt_xdate()`?",
         "opcoes": ["Converter textos em datas", "Inclinar as datas do eixo x para não se sobreporem", "Ordenar as datas", "Apagar datas repetidas"],
         "correta": 1, "explicacao": "Ela só ajusta a aparência dos rótulos de data."},
        {"pergunta": "Qual método pinta a área entre duas linhas?",
         "opcoes": ["ax.paint()", "ax.fill_between()", "ax.area()", "ax.shade()"], "correta": 1,
         "explicacao": "fill_between(x, y1, y2) preenche entre as curvas y1 e y2."},
    ],
    "desafios": [
        {
            "titulo": "Cabeçalho do CSV",
            "enunciado": "Leia o arquivo 'clima.csv' e mostre cada coluna do cabeçalho com o seu índice, no formato '0 ESTACAO'.",
            "inicial": "import csv\nfrom pathlib import Path\n\n# Seu código aqui\n",
            "dica": "reader = csv.reader(Path('clima.csv').read_text().splitlines()); cabecalho = next(reader); for i, col in enumerate(cabecalho): print(i, col)",
            "solucao": _c('''
import csv
from pathlib import Path

reader = csv.reader(Path("clima.csv").read_text().splitlines())
cabecalho = next(reader)
for indice, coluna in enumerate(cabecalho):
    print(indice, coluna)
'''),
            "casos": _casos_cabecalho(),
        },
        {
            "titulo": "As máximas do mês",
            "enunciado": "Leia 'clima.csv' (colunas: ESTACAO, DATA, CHUVA_MM, TMAX, TMIN), guarde as temperaturas máximas "
                         "como inteiros na lista `maximas` e desenhe um gráfico de linha com elas.\n\n"
                         "O Verificar testa com arquivos de duas estações diferentes.",
            "inicial": "import csv\nfrom pathlib import Path\nimport matplotlib.pyplot as plt\n\n# Seu código aqui\n",
            "dica": "Pule o cabeçalho com next(reader). A coluna TMAX é a de índice 3.",
            "solucao": _c('''
import csv
from pathlib import Path
import matplotlib.pyplot as plt

reader = csv.reader(Path("clima.csv").read_text().splitlines())
next(reader)
maximas = []
for linha in reader:
    maximas.append(int(linha[3]))

fig, ax = plt.subplots()
ax.plot(maximas, color="red")
ax.set_title("Temperaturas máximas")
plt.show()
'''),
            "casos": _casos_maximas(),
        },
        {
            "titulo": "Texto que vira data",
            "enunciado": "Crie a função `converter(texto)` que recebe uma data no formato do CSV ('2025-07-04') e devolve um "
                         "objeto datetime. Crie também `formatar(data)`, que devolve a data no estilo brasileiro: '04/07/2025'.",
            "inicial": "from datetime import datetime\n\n\ndef converter(texto):\n    pass\n\n\ndef formatar(data):\n    pass\n",
            "dica": "datetime.strptime(texto, '%Y-%m-%d') para ler e data.strftime('%d/%m/%Y') para escrever.",
            "solucao": _c('''
from datetime import datetime


def converter(texto):
    return datetime.strptime(texto, "%Y-%m-%d")


def formatar(data):
    return data.strftime("%d/%m/%Y")
'''),
            "casos": [caso([funcao("converter"), funcao("formatar"),
                            regra(lambda o, n, c: n["converter"]("2025-07-04").timetuple()[:3] == (2025, 7, 4)
                                  and type(n["converter"]("2026-01-31")).__name__ == "datetime",
                                  "converter('2025-07-04') deveria devolver o datetime de 4 de julho de 2025."),
                            regra(lambda o, n, c: n["formatar"](n["converter"]("2025-07-04")) == "04/07/2025"
                                  and n["formatar"](n["converter"]("2026-12-25")) == "25/12/2026",
                                  "formatar(converter('2025-07-04')) deveria devolver '04/07/2025'.")])],
        },
        {
            "titulo": "Estação com defeito",
            "enunciado": "O arquivo 'clima.csv' tem dias com campos vazios. Leia o arquivo e:\n"
                         "• para cada dia sem dados, mostre 'Faltando dados para AAAA-MM-DD'\n"
                         "• guarde as máximas dos dias válidos na lista `maximas`\n"
                         "• no fim, mostre 'Dias válidos: N'",
            "inicial": "import csv\nfrom pathlib import Path\n\n# Seu código aqui\n",
            "dica": "Dentro do for: try: maxima = int(linha[3]) / except ValueError: print(...) / else: maximas.append(maxima).",
            "solucao": _c('''
import csv
from pathlib import Path

reader = csv.reader(Path("clima.csv").read_text().splitlines())
next(reader)
maximas = []
for linha in reader:
    try:
        maxima = int(linha[3])
    except ValueError:
        print(f"Faltando dados para {linha[1]}")
    else:
        maximas.append(maxima)

print(f"Dias válidos: {len(maximas)}")
'''),
            "casos": _casos_faltando(),
        },
        {
            "titulo": "Terremotos fortes",
            "enunciado": "Leia 'terremotos.json' e mostre:\n"
                         "• 'Total de terremotos: N'\n"
                         "• 'Fortes (5 ou mais): N'\n"
                         "• depois, o título (properties → title) de cada terremoto com magnitude 5 ou mais, na ordem do arquivo",
            "inicial": "import json\nfrom pathlib import Path\n\n# Seu código aqui\n",
            "dica": "fortes = [t for t in dados['features'] if t['properties']['mag'] >= 5]",
            "solucao": _c('''
import json
from pathlib import Path

dados = json.loads(Path("terremotos.json").read_text())
terremotos = dados["features"]
fortes = [t for t in terremotos if t["properties"]["mag"] >= 5]

print(f"Total de terremotos: {len(terremotos)}")
print(f"Fortes (5 ou mais): {len(fortes)}")
for t in fortes:
    print(t["properties"]["title"])
'''),
            "casos": _casos_fortes(),
        },
        {
            "titulo": "Mapa dos tremores",
            "enunciado": "Leia 'terremotos.json', guarde as magnitudes na lista `mags` e faça um scatter com a longitude "
                         "no eixo x e a latitude no eixo y de cada terremoto (na ordem do arquivo). Use as magnitudes para "
                         "o tamanho ou a cor dos pontos.",
            "inicial": "import json\nfrom pathlib import Path\nimport matplotlib.pyplot as plt\n\n# Seu código aqui\n",
            "dica": "coordinates é [longitude, latitude, profundidade]: lon = [0] e lat = [1].",
            "solucao": _c('''
import json
from pathlib import Path
import matplotlib.pyplot as plt

dados = json.loads(Path("terremotos.json").read_text())
mags, lons, lats = [], [], []
for t in dados["features"]:
    mags.append(t["properties"]["mag"])
    lons.append(t["geometry"]["coordinates"][0])
    lats.append(t["geometry"]["coordinates"][1])

fig, ax = plt.subplots()
ax.scatter(lons, lats, s=[m**3 for m in mags], c=mags, cmap=plt.cm.Reds)
ax.set_title("Terremotos")
plt.show()
'''),
            "casos": _casos_mapa(),
        },
        {
            "titulo": "Caça-bugs: o cabeçalho intruso",
            "enunciado": "Este programa dá ValueError logo na primeira linha lida. Conserte para mostrar 'Maior máxima: N'.",
            "inicial": _c('''
import csv
from pathlib import Path

reader = csv.reader(Path("clima.csv").read_text().splitlines())

maximas = []
for linha in reader:
    maximas.append(int(linha[3]))

print(f"Maior máxima: {max(maximas)}")
''') + "\n",
            "dica": "A primeira linha do CSV é o cabeçalho. int('TMAX') não dá certo!",
            "solucao": _c('''
import csv
from pathlib import Path

reader = csv.reader(Path("clima.csv").read_text().splitlines())
next(reader)

maximas = []
for linha in reader:
    maximas.append(int(linha[3]))

print(f"Maior máxima: {max(maximas)}")
'''),
            "casos": _casos_bug_csv(),
        },
    ],
    "chefe": {
        "titulo": "O Meteorologista",
        "enunciado": "Leia 'clima.csv' (com dias faltando!) e:\n"
                     "1. Monte as listas de datas, máximas e mínimas só com os dias válidos.\n"
                     "2. Faça um gráfico com a linha das máximas, a linha das mínimas e o espaço entre elas pintado (fill_between).\n"
                     "3. Mostre exatamente:\n"
                     "Máxima do período: T em AAAA-MM-DD\n"
                     "Mínima do período: T em AAAA-MM-DD\n"
                     "Dias sem dados: N\n\n"
                     "A máxima do período é a maior TMAX; a mínima é a menor TMIN. Em caso de empate, vale o primeiro dia. "
                     "Não mostre mais nada na tela. O Verificar testa duas estações.",
        "inicial": "import csv\nfrom pathlib import Path\nimport matplotlib.pyplot as plt\n\n# Seu código aqui\n",
        "dica": "Guarde as datas como texto (linha[1]) para imprimir. Para achar o dia da máxima: i = maximas.index(max(maximas)) e datas[i].",
        "solucao": _c('''
import csv
from pathlib import Path
import matplotlib.pyplot as plt

reader = csv.reader(Path("clima.csv").read_text().splitlines())
next(reader)

datas, maximas, minimas = [], [], []
faltando = 0
for linha in reader:
    try:
        maxima = int(linha[3])
        minima = int(linha[4])
    except ValueError:
        faltando += 1
    else:
        datas.append(linha[1])
        maximas.append(maxima)
        minimas.append(minima)

i_max = maximas.index(max(maximas))
i_min = minimas.index(min(minimas))
print(f"Máxima do período: {maximas[i_max]} em {datas[i_max]}")
print(f"Mínima do período: {minimas[i_min]} em {datas[i_min]}")
print(f"Dias sem dados: {faltando}")

fig, ax = plt.subplots()
ax.plot(datas, maximas, color="red")
ax.plot(datas, minimas, color="blue")
ax.fill_between(datas, maximas, minimas, facecolor="blue", alpha=0.1)
ax.set_title("Máximas e mínimas")
fig.autofmt_xdate()
plt.show()
'''),
        "casos": _casos_meteorologista(),
    },
}


# ---------------------------------------------------------------------------
# CAPÍTULO 17: Trabalhando com APIs
# ---------------------------------------------------------------------------

_URL_GH = "https://api.github.com/search/repositories?q=language:python+sort:stars+stars:>10000"

CAP17 = {
    "num": 17,
    "titulo": "Dados: APIs da Web",
    "subtitulo": "requests, respostas em JSON, GitHub e Hacker News",
    "licoes": [
        {
            "titulo": "O que é uma API",
            "texto": [
                "Uma **API web** é um endereço (URL) feito para programas, não para pessoas: em vez de uma página, ele devolve "
                "**dados**, quase sempre em JSON.",
                "O pacote `requests` faz o pedido: `r = requests.get(url, headers=headers)`. `r.status_code` diz se deu "
                "certo (**200** é sucesso; **404** é não encontrado).",
                "## API de treino",
                "O PyQuest traz um **requests de treino**: ele responde às mesmas URLs do livro (busca de repositórios do "
                "GitHub e Hacker News), mas com dados **simulados e fixos**, sem usar a internet. Assim todo mundo tem o "
                "mesmo resultado e a correção funciona. No seu PC, com `pip install requests`, o mesmo código busca dados reais.",
            ],
            "exemplo": _c(f'''
import requests

url = "{_URL_GH}"
headers = {{"Accept": "application/vnd.github.v3+json"}}
r = requests.get(url, headers=headers)
print(f"Status: {{r.status_code}}")

resposta = r.json()
print("Chaves:", list(resposta.keys()))
print("Total de repositórios:", resposta["total_count"])
'''),
        },
        {
            "titulo": "Explorando a resposta",
            "texto": [
                "`r.json()` transforma a resposta num dicionário Python. Na busca do GitHub, a chave `items` é uma lista "
                "de repositórios, e cada um é outro dicionário cheio de informações.",
                "Antes de usar, **explore**: veja quantas chaves existem e imprima as que interessam, como `name`, "
                "`owner['login']`, `stargazers_count` e `html_url`.",
                "APIs reais têm **limite de pedidos** por minuto. Por isso, guarde a resposta numa variável em vez de "
                "pedir de novo toda hora.",
            ],
            "exemplo": _c(f'''
import requests

r = requests.get("{_URL_GH}")
repos = r.json()["items"]
print("Repositórios recebidos:", len(repos))

primeiro = repos[0]
print("Chaves de um repositório:", len(primeiro))

for repo in repos[:4]:
    print()
    print("Nome:", repo["name"])
    print("Dono:", repo["owner"]["login"])
    print("Estrelas:", repo["stargazers_count"])
    print("Link:", repo["html_url"])
'''),
        },
        {
            "titulo": "Gráfico dos repositórios",
            "texto": [
                "Com os dados em listas, o gráfico é rápido. Nomes longos ficam melhores num gráfico de **barras "
                "horizontais**: `ax.barh(nomes, estrelas)`.",
                "`ax.invert_yaxis()` coloca o maior no topo.",
                "O livro usa o Plotly aqui, que deixa passar o mouse sobre as barras e clicar nos links. A lógica de "
                "montar as listas é a mesma.",
            ],
            "exemplo": _c(f'''
import requests
import matplotlib.pyplot as plt

repos = requests.get("{_URL_GH}").json()["items"]

nomes, estrelas = [], []
for repo in repos:
    nomes.append(repo["name"])
    estrelas.append(repo["stargazers_count"])

fig, ax = plt.subplots(figsize=(8, 5))
ax.barh(nomes, estrelas, color="steelblue")
ax.invert_yaxis()
ax.set_title("Projetos Python mais estrelados (dados de treino)")
ax.set_xlabel("Estrelas")
plt.show()
'''),
        },
        {
            "titulo": "Hacker News e ordenação",
            "texto": [
                "A API do Hacker News funciona em duas etapas: `topstories.json` devolve uma lista de **IDs**, e "
                "`item/<id>.json` devolve os detalhes de cada notícia.",
                "Juntando os dicionários numa lista, dá para ordenar por qualquer campo. O livro usa "
                "`sorted(lista, key=itemgetter('comments'), reverse=True)`. Um `lambda` faz o mesmo: "
                "`key=lambda d: d['descendants']`.",
                "Em `descendants` está o número de comentários. Algumas notícias reais não têm essa chave, por isso o "
                "livro usa `.get('descendants', 0)`.",
            ],
            "exemplo": _c('''
from operator import itemgetter
import requests

url = "https://hacker-news.firebaseio.com/v0/topstories.json"
ids = requests.get(url).json()

noticias = []
for id_noticia in ids[:6]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{id_noticia}.json"
    d = requests.get(url).json()
    noticias.append({"titulo": d["title"], "comentarios": d.get("descendants", 0)})

noticias = sorted(noticias, key=itemgetter("comentarios"), reverse=True)
for n in noticias:
    print(f"{n['comentarios']:>4} comentários | {n['titulo']}")
'''),
        },
    ],
    "quiz": [
        {"pergunta": "O que uma API web normalmente devolve?",
         "opcoes": ["Uma página bonita", "Dados (geralmente em JSON) para programas", "Um arquivo .exe", "Imagens apenas"],
         "correta": 1, "explicacao": "APIs são feitas para programas lerem dados."},
        {"pergunta": "Qual status_code indica sucesso?",
         "opcoes": ["404", "500", "200", "301"], "correta": 2, "explicacao": "200 = OK. 404 = não encontrado."},
        {"pergunta": "O que `r.json()` faz?",
         "opcoes": ["Salva um arquivo", "Transforma a resposta em dicionários e listas do Python", "Envia dados", "Fecha a conexão"],
         "correta": 1, "explicacao": "É como um json.loads() da resposta."},
        {"pergunta": "Na API de busca do GitHub, onde fica a lista de repositórios?",
         "opcoes": ["resposta['repos']", "resposta['items']", "resposta['total_count']", "resposta[0]"], "correta": 1,
         "explicacao": "total_count é só o número; a lista está em items."},
        {"pergunta": "O que é mostrado?",
         "codigo": "noticias = [{'t': 'a', 'c': 5}, {'t': 'b', 'c': 9}]\nnoticias.sort(key=lambda d: d['c'], reverse=True)\nprint(noticias[0]['t'])",
         "opcoes": ["a", "b", "5", "9"], "correta": 1,
         "explicacao": "Ordenando por 'c' do maior para o menor, a notícia 'b' (9) vem primeiro."},
        {"pergunta": "Por que usar `d.get('descendants', 0)` em vez de `d['descendants']`?",
         "opcoes": ["É mais rápido", "Para não dar KeyError se a chave não existir", "Para ordenar", "Para converter em texto"],
         "correta": 1, "explicacao": "get() devolve o valor padrão quando a chave falta."},
        {"pergunta": "Por que guardar a resposta da API numa variável em vez de pedir de novo?",
         "opcoes": ["APIs têm limite de pedidos e cada pedido demora", "Porque requests só funciona uma vez",
                    "Para o JSON virar CSV", "Não faz diferença"], "correta": 0,
         "explicacao": "Pedir uma vez e reaproveitar é mais rápido e respeita os limites da API."},
    ],
    "desafios": [
        {
            "titulo": "Primeiro contato",
            "enunciado": f"Faça um pedido para a URL de busca do GitHub:\n{_URL_GH}\n\n"
                         "e mostre:\nStatus: 200\nTotal de repositórios: N",
            "inicial": f'import requests\n\nurl = "{_URL_GH}"\n# Seu código aqui\n',
            "dica": "r = requests.get(url); r.status_code e r.json()['total_count'].",
            "solucao": _c(f'''
import requests

url = "{_URL_GH}"
r = requests.get(url)
print(f"Status: {{r.status_code}}")
print(f"Total de repositórios: {{r.json()['total_count']}}")
'''),
            "casos": [caso([regra(lambda o, n, c: normalizar(o) == normalizar(_esperado_status()),
                                  "A saída não ficou como esperado. Use os valores que vêm da resposta (status_code e total_count).")])],
        },
        {
            "titulo": "Pódio dos repositórios",
            "enunciado": "Usando a mesma busca, mostre os 3 primeiros repositórios no formato:\n"
                         "nome (de dono): N estrelas",
            "inicial": f'import requests\n\nurl = "{_URL_GH}"\n# Seu código aqui\n',
            "dica": "for repo in r.json()['items'][:3]: print(f\"{repo['name']} (de {repo['owner']['login']}): {repo['stargazers_count']} estrelas\")",
            "solucao": _c(f'''
import requests

url = "{_URL_GH}"
repos = requests.get(url).json()["items"]
for repo in repos[:3]:
    print(f"{{repo['name']}} (de {{repo['owner']['login']}}): {{repo['stargazers_count']}} estrelas")
'''),
            "casos": [caso([regra(lambda o, n, c: normalizar(o) == normalizar(_esperado_top3()),
                                  "A saída não bateu. Formato de cada linha: nome (de dono): N estrelas, para os 3 primeiros itens.")])],
        },
        {
            "titulo": "Estrelas no gráfico",
            "enunciado": "Faça um gráfico de barras HORIZONTAIS (ax.barh) com o nome e as estrelas de TODOS os "
                         "repositórios da busca do GitHub.",
            "inicial": f'import requests\nimport matplotlib.pyplot as plt\n\nurl = "{_URL_GH}"\n# Seu código aqui\n',
            "dica": "Monte as listas nomes e estrelas num for e depois ax.barh(nomes, estrelas).",
            "solucao": _c(f'''
import requests
import matplotlib.pyplot as plt

url = "{_URL_GH}"
repos = requests.get(url).json()["items"]
nomes = [repo["name"] for repo in repos]
estrelas = [repo["stargazers_count"] for repo in repos]

fig, ax = plt.subplots()
ax.barh(nomes, estrelas)
ax.set_title("Repositórios mais estrelados")
plt.show()
'''),
            "casos": [caso([tem_grafico(),
                            regra(lambda o, n, c: _teste_barras_api(n),
                                  "O gráfico precisa ter uma barra horizontal para cada repositório, com o tamanho igual às estrelas.")])],
        },
        {
            "titulo": "Pedido com cuidado",
            "enunciado": "Crie a função `buscar(url)` que faz o pedido e devolve r.json() quando o status for 200. "
                         "Para qualquer outro status, devolve None.",
            "inicial": "import requests\n\n\ndef buscar(url):\n    pass\n",
            "dica": "if r.status_code == 200: return r.json() e, fora do if, return None.",
            "solucao": _c('''
import requests


def buscar(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None
'''),
            "casos": [caso([funcao("buscar"),
                            regra(lambda o, n, c: _teste_buscar(n),
                                  "Teste: buscar('https://hacker-news.firebaseio.com/v0/item/40101.json') deveria devolver o "
                                  "dicionário da notícia; buscar('https://api.github.com/nao-existe') (status 404) deveria devolver None.")])],
        },
        {
            "titulo": "Mais comentadas",
            "enunciado": "Pegue os 5 primeiros IDs de https://hacker-news.firebaseio.com/v0/topstories.json, busque cada "
                         "notícia em https://hacker-news.firebaseio.com/v0/item/<id>.json e mostre as 5 da mais comentada "
                         "para a menos comentada, no formato:\ntítulo - N comentários\n\n(N está na chave 'descendants'.)",
            "inicial": "import requests\n\n# Seu código aqui\n",
            "dica": "Guarde os dicionários numa lista e ordene com sorted(lista, key=lambda d: d['descendants'], reverse=True).",
            "solucao": _c('''
import requests

ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()
noticias = []
for id_noticia in ids[:5]:
    url = f"https://hacker-news.firebaseio.com/v0/item/{id_noticia}.json"
    noticias.append(requests.get(url).json())

noticias = sorted(noticias, key=lambda d: d["descendants"], reverse=True)
for d in noticias:
    print(f"{d['title']} - {d['descendants']} comentários")
'''),
            "casos": [caso([regra(lambda o, n, c: normalizar(o) == normalizar(_esperado_hn()),
                                  "A saída não bateu. Confira se usou só os 5 primeiros IDs e se ordenou do mais comentado para o menos.")])],
        },
        {
            "titulo": "Caça-bugs: o método esquecido",
            "enunciado": "Este programa dá TypeError ('method' object is not subscriptable). Conserte para mostrar o total.",
            "inicial": _c(f'''
import requests

r = requests.get("{_URL_GH}")
dados = r.json
print("Total:", dados["total_count"])
''') + "\n",
            "dica": "json é um método. Métodos precisam de parênteses para rodar.",
            "solucao": _c(f'''
import requests

r = requests.get("{_URL_GH}")
dados = r.json()
print("Total:", dados["total_count"])
'''),
            "casos": [caso([regra(lambda o, n, c: normalizar(o) == normalizar(_esperado_status().splitlines()[1].replace("Total de repositórios", "Total")),
                                  "A saída deveria ser 'Total: N', com o total_count da resposta.")])],
        },
    ],
    "chefe": {
        "titulo": "O Explorador de APIs",
        "enunciado": "Crie a função `ranking_linguagem(linguagem)` que busca os repositórios de uma linguagem na URL\n"
                     "https://api.github.com/search/repositories?q=language:<linguagem>+sort:stars\n\n"
                     "e devolve uma lista com até 5 tuplas (nome, estrelas), da mais estrelada para a menos estrelada.\n"
                     "Se a linguagem não tiver repositórios, devolve uma lista vazia.\n\n"
                     "A API de treino conhece python, javascript e rust.",
        "inicial": "import requests\n\n\ndef ranking_linguagem(linguagem):\n    pass\n\n\nprint(ranking_linguagem('rust'))\n",
        "dica": "Monte a URL com f-string, pegue r.json()['items'], crie as tuplas (repo['name'], repo['stargazers_count']), "
                "ordene por estrelas com reverse=True e corte com [:5].",
        "solucao": _c('''
import requests


def ranking_linguagem(linguagem):
    url = f"https://api.github.com/search/repositories?q=language:{linguagem}+sort:stars"
    repos = requests.get(url).json()["items"]
    pares = [(repo["name"], repo["stargazers_count"]) for repo in repos]
    pares.sort(key=lambda par: par[1], reverse=True)
    return pares[:5]


print(ranking_linguagem("rust"))
'''),
        "casos": [caso([funcao("ranking_linguagem"),
                        regra(lambda o, n, c: _teste_ranking(n),
                              "Teste: para python, javascript e rust, a função deve devolver as 5 tuplas (nome, estrelas) mais "
                              "estreladas, em ordem decrescente; para 'cobol', devolve [].")])],
    },
}


CAPITULOS = [CAP1, CAP2, CAP3, CAP4, CAP5, CAP6, CAP7, CAP8, CAP9, CAP10, CAP11, CAP12, CAP13, CAP14,
             CAP15, CAP16, CAP17]
