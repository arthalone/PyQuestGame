# PyQuest Online: como colocar no ar

O site é estático (HTML + JavaScript) e o Python roda no navegador de cada jogador (Pyodide).
O login com Google, o progresso e o ranking ficam no **Supabase**. Tudo cabe nos planos gratuitos.

Tempo estimado: 30 a 40 minutos, só na primeira vez.

---

## 0. Testar no seu PC (opcional)

Dê dois cliques em `Testar_local.bat`. O site abre em http://localhost:8000 no **modo offline**
(sem login e sem ranking, mas com tudo o resto funcionando).

> Abrir o `index.html` direto com dois cliques não funciona: o Python precisa de um servidor, mesmo que local.

---

## 1. Criar o banco no Supabase

1. Entre em https://supabase.com e clique em **Start your project**. Dá para entrar com sua conta do GitHub.
2. **New project**: dê um nome (ex.: `pyquest`), crie uma senha forte para o banco e escolha a região **South America (São Paulo)**.
3. Espere o projeto ficar pronto (1 a 2 minutos).
4. No menu da esquerda, abra **SQL Editor** › **New query**.
5. Abra o arquivo `supabase/schema.sql`, copie **tudo**, cole no editor e clique em **Run**. Deve aparecer "Success".
6. Vá em **Project Settings › API** e copie:
   - **Project URL** (algo como `https://abcd1234.supabase.co`)
   - **anon public** key
7. Abra o `config.js` e cole os dois valores entre as aspas:

```js
window.PYQUEST_CONFIG = {
  SUPABASE_URL: "https://abcd1234.supabase.co",
  SUPABASE_ANON_KEY: "eyJhbGciOi...",
};
```

> A chave *anon* é pública por design: o banco é protegido pelas regras do `schema.sql`.
> **Nunca** coloque a chave `service_role` no site.

---

## 2. Publicar no GitHub Pages

1. No GitHub, clique em **New repository**. Nome: `pyquest`, visibilidade **Public**, crie.
2. Na página do repositório, clique em **uploading an existing file** e arraste **todo o conteúdo desta pasta `web`**
   (os arquivos e as pastas `py` e `supabase`, não a pasta `web` em si). Clique em **Commit changes**.
3. Vá em **Settings › Pages**. Em *Source*, escolha **Deploy from a branch**, branch **main**, pasta **/ (root)** e salve.
4. Em 1 ou 2 minutos o site estará em: `https://SEU-USUARIO.github.io/pyquest/`

---

## 3. Ligar o login com Google

### 3a. No Google Cloud
1. Acesse https://console.cloud.google.com e crie um projeto (ex.: `PyQuest`).
2. Menu › **APIs e serviços › Tela de consentimento OAuth** (ou "Google Auth Platform"):
   tipo **Externo**, nome do app `PyQuest`, seu e-mail de suporte e de contato. Salve.
   Depois, em **Público-alvo**, clique em **Publicar app** para qualquer pessoa conseguir entrar.
3. **Credenciais › Criar credenciais › ID do cliente OAuth**:
   - Tipo: **Aplicativo da Web**
   - Em **URIs de redirecionamento autorizados**, adicione:
     `https://abcd1234.supabase.co/auth/v1/callback` (use a SUA Project URL + `/auth/v1/callback`)
4. Copie o **ID do cliente** e a **Chave secreta do cliente**.

### 3b. No Supabase
1. **Authentication › Sign In / Providers › Google**: ative, cole o ID e a chave secreta, salve.
2. **Authentication › URL Configuration**:
   - **Site URL**: `https://SEU-USUARIO.github.io/pyquest/`
   - **Redirect URLs**: adicione `https://SEU-USUARIO.github.io/pyquest/` e `http://localhost:8000/`

Pronto: abra o site, clique em **Entrar** e jogue. Seu apelido começa como `Jogador12345`
e pode ser trocado na aba **Perfil**.

---

## Atualizar o site depois

- Mudou lições/desafios em `py/conteudo.py`? Rode `atualizar_conteudo.bat` (gera o `conteudo.json`)
  e envie para o GitHub os dois arquivos.
  Se criou ou removeu itens, rode de novo o `supabase/schema.sql` (ele atualiza a tabela de XP).
- Mudou outro arquivo? É só enviar de novo para o GitHub. O site atualiza em 1 ou 2 minutos.

## Como funciona o ranking

- **Esta semana**: XP ganho desde segunda-feira 00h (Brasília). **Geral**: XP de sempre.
- **Relâmpago**: melhor número de acertos em 60 segundos.
- O XP de cada item é decidido pelo servidor (tabela `itens`), não pelo navegador.

## Limite importante (anti-trapaça)

Como o código é corrigido no navegador, alguém com conhecimento técnico consegue marcar itens como
concluídos sem resolvê-los. O servidor impede XP inventado, itens repetidos e bônus diário duplicado,
então o máximo que um trapaceiro alcança é o mesmo XP de quem completou tudo (~1.670 + bônus diários).
O ranking **semanal** e a **sequência de dias** ainda premiam quem joga de verdade.
Se o site crescer, dá para mover a correção para um servidor.
