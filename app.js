/* PyQuest Online: aprenda Python jogando. */
"use strict";
(() => {
  const CFG = window.PYQUEST_CONFIG || {};
  const app = document.getElementById("app");
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => Array.from(el.querySelectorAll(s));
  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // =====================================================================
  // Regras do jogo (os valores de XP espelham a tabela "itens" do servidor)
  // =====================================================================
  const NIVEIS = [
    [0, "Ovo de Píton"], [100, "Filhote de Cobra"], [250, "Serpente Curiosa"],
    [450, "Aprendiz de Código"], [700, "Domador de Strings"], [1000, "Mestre das Listas"],
    [1300, "Cavaleiro do For"], [1650, "Guardião do If"], [2000, "Senhor dos Dicionários"],
    [2400, "Domador de Laços"], [2850, "Arquiteto de Funções"], [3350, "Mestre das Classes"],
    [3900, "Pythonista"], [4400, "Piloto Estelar"], [4900, "Analista de Dados"],
    [5500, "Mestre dos Projetos"], [6100, "Desenvolvedor Web"], [6650, "Arquiteto Django"], [7100, "Lenda do Terminal"],
  ];
  const XP = { licao: 10, quiz: 50, desafio: 30, chefe: 100, bonus: 10, solucao: 5 };
  const APROVACAO = 0.7;
  const TEMPO_RELAMPAGO = 60;
  const CONQUISTAS = [
    ["ola_mundo", "Olá, Mundo!", "Execute seu primeiro código."],
    ["primeiro_desafio", "Primeira Vitória", "Resolva seu primeiro desafio."],
    ["leitor", "Rato de Biblioteca", "Conclua 10 lições."],
    ["quiz_perfeito", "Gabaritou!", "Acerte 100% de um quiz."],
    ["combo5", "Em Chamas", "Faça um combo de 5 acertos seguidos num quiz."],
    ["autodidata", "Autodidata", "Resolva 5 desafios sem usar dicas."],
    ["persistente", "Persistente", "Vença um desafio depois de 3 ou mais tentativas."],
    ["cacador", "Caçador de Chefões", "Derrote seu primeiro chefão."],
    ["lenda", "Lenda da Jornada", "Derrote todos os chefões."],
    ["streak3", "Constância", "Estude 3 dias seguidos."],
    ["streak7", "Hábito de Ferro", "Estude 7 dias seguidos."],
    ["raio", "Raio Veloz", "Faça 8 ou mais acertos no Desafio Relâmpago."],
    ["cientista", "Cientista Maluco", "Execute 15 experimentos no Laboratório."],
    ["mil_xp", "Mil Pontos", "Alcance 1000 XP."],
  ];
  const CONQ = Object.fromEntries(CONQUISTAS.map((c) => [c[0], c]));
  const ULTIMO_FUNDAMENTO = 11;
  const PROJETOS = [
    { id: "alien", titulo: "Alien Invasion", icone: "🚀", caps: [12, 13, 14],
      desc: "Monte um jogo de nave: movimento, tiros, frota de alienígenas, colisões, placar e recorde." },
    { id: "dados", titulo: "Visualização de Dados", icone: "📊", caps: [15, 16, 17],
      desc: "Transforme números em gráficos: matplotlib, passeio aleatório, dados de clima em CSV, terremotos em JSON e APIs da web." },
    { id: "web", titulo: "Learning Log (Django)", icone: "🌐", caps: [18, 19, 20],
      desc: "Construa um app web de verdade: models, páginas, formulários, contas de usuário, estilo com Bootstrap e deploy." },
  ];
  const projetoDoCap = (n) => PROJETOS.find((p) => p.caps.includes(n));

  function nivelDe(xp) {
    let i = 0;
    NIVEIS.forEach(([min], k) => { if (xp >= min) i = k; });
    return { n: i + 1, titulo: NIVEIS[i][1], ini: NIVEIS[i][0], prox: NIVEIS[i + 1] ? NIVEIS[i + 1][0] : null };
  }
  function tipoItem(id) {
    if (/-l\d+$/.test(id)) return "licao";
    if (id.endsWith("-quiz")) return "quiz";
    if (id.endsWith("-chefe")) return "chefe";
    return "desafio";
  }
  function xpItem(id, ajuda) {
    const base = XP[tipoItem(id)];
    if (ajuda === "solucao") return XP.solucao;
    if (ajuda === "dica") return Math.floor(base / 2);
    return base;
  }
  const fmtDia = (d) => d.toISOString().slice(0, 10);
  const hojeSP = () => new Intl.DateTimeFormat("en-CA", { timeZone: "America/Sao_Paulo", year: "numeric", month: "2-digit", day: "2-digit" }).format(new Date());

  // =====================================================================
  // Estado local (cache) + sincronização com o Supabase
  // =====================================================================
  const PADRAO = () => ({
    feitos: {}, bonus: [], quiz_melhor: {}, codigo: {}, tentativas: {}, dicas: [], solucoes: [],
    conquistas: [], recorde: 0, lab: 0, sem_dica: 0, pend: { progresso: [], relampago: [] },
  });
  const CHAVE_CONVIDADO = "pyquest_v1_convidado";
  let S = PADRAO();
  let chaveLS = CHAVE_CONVIDADO;

  function carregar(chave) {
    chaveLS = chave;
    try { S = Object.assign(PADRAO(), JSON.parse(localStorage.getItem(chave) || "{}")); } catch { S = PADRAO(); }
    S.pend = Object.assign({ progresso: [], relampago: [] }, S.pend);
  }
  let salvarT = null;
  function salvar() {
    clearTimeout(salvarT);
    salvarT = setTimeout(() => { try { localStorage.setItem(chaveLS, JSON.stringify(S)); } catch { /* sem storage */ } }, 150);
  }
  const feito = (id) => !!S.feitos[id];
  const xpTotal = () => Object.values(S.feitos).reduce((a, f) => a + (f.xp || 0), 0) + S.bonus.length * XP.bonus;
  function sequencia() {
    const dias = new Set(S.bonus);
    const d = new Date(hojeSP() + "T12:00:00Z");
    if (!dias.has(fmtDia(d))) d.setUTCDate(d.getUTCDate() - 1);
    let n = 0;
    while (dias.has(fmtDia(d))) { n++; d.setUTCDate(d.getUTCDate() - 1); }
    return n;
  }

  let sb = null, usuario = null, perfil = null, souAdmin = null;
  if (CFG.SUPABASE_URL && CFG.SUPABASE_ANON_KEY && window.supabase) {
    try {
      sb = window.supabase.createClient(CFG.SUPABASE_URL, CFG.SUPABASE_ANON_KEY, {
        auth: { flowType: "pkce", detectSessionInUrl: true, persistSession: true },
      });
    } catch (e) { console.warn("Supabase indisponível", e); sb = null; }
  }

  async function entrarGoogle() {
    if (!sb) return toast("Login indisponível: o site está em modo offline.", "vermelho");
    const { error } = await sb.auth.signInWithOAuth({
      provider: "google", options: { redirectTo: location.origin + location.pathname },
    });
    if (error) toast("Não foi possível entrar: " + error.message, "vermelho");
  }
  async function sair() {
    if (sb) await sb.auth.signOut();
  }

  function mesclarConvidado(c) {
    for (const [k, v] of Object.entries(c.feitos)) {
      if (!S.feitos[k]) {
        S.feitos[k] = v;
        S.pend.progresso.push({ item_id: k, ajuda: v.ajuda || "nenhuma" });
      }
    }
    for (const [k, v] of Object.entries(c.quiz_melhor)) S.quiz_melhor[k] = Math.max(v, S.quiz_melhor[k] || 0);
    for (const [k, v] of Object.entries(c.codigo)) if (!(k in S.codigo)) S.codigo[k] = v;
    S.conquistas = [...new Set([...S.conquistas, ...c.conquistas])];
    S.dicas = [...new Set([...S.dicas, ...c.dicas])];
    S.solucoes = [...new Set([...S.solucoes, ...c.solucoes])];
    S.sem_dica = Math.max(S.sem_dica, c.sem_dica);
    S.lab = Math.max(S.lab, c.lab);
    if (c.recorde > S.recorde) { S.recorde = c.recorde; S.pend.relampago.push(c.recorde); }
    try { localStorage.removeItem(CHAVE_CONVIDADO); } catch { /* */ }
  }

  async function sincronizar() {
    if (!sb || !usuario) return;
    try {
      if (S.pend.progresso.length) {
        const { error } = await sb.from("progresso").upsert(
          S.pend.progresso.map((p) => ({ ...p, user_id: usuario.id })),
          { onConflict: "user_id,item_id", ignoreDuplicates: true });
        if (!error) S.pend.progresso = [];
      }
      if (S.pend.relampago.length) {
        const max = Math.max(...S.pend.relampago);
        await sb.from("relampago").insert({ user_id: usuario.id, acertos: Math.min(60, max) });
        S.pend.relampago = [];
      }
      const [pr, bo, pf, rl] = await Promise.all([
        sb.from("progresso").select("item_id,ajuda,xp"),
        sb.from("bonus_diario").select("dia"),
        sb.from("perfis").select("apelido").eq("id", usuario.id).maybeSingle(),
        sb.from("relampago").select("acertos").order("acertos", { ascending: false }).limit(1),
      ]);
      if (!pr.error) {
        const f = {};
        for (const r of pr.data) f[r.item_id] = { ajuda: r.ajuda, xp: r.xp };
        for (const p of S.pend.progresso) if (S.feitos[p.item_id]) f[p.item_id] = S.feitos[p.item_id];
        S.feitos = f;
      }
      if (!bo.error) S.bonus = bo.data.map((r) => r.dia);
      if (!pf.error && pf.data) perfil = pf.data;
      if (!rl.error && rl.data[0]) S.recorde = Math.max(S.recorde, rl.data[0].acertos);
      salvar();
    } catch (e) { console.warn("Falha ao sincronizar", e); }
  }

  async function aoMudarSessao(session, forcar = false) {
    const novo = session?.user || null;
    if (!forcar && (novo?.id || null) === (usuario?.id || null)) return;
    const eraConvidado = chaveLS === CHAVE_CONVIDADO ? S : null;
    usuario = novo;
    souAdmin = null;
    if (usuario) {
      carregar("pyquest_v1_" + usuario.id);
      if (eraConvidado && Object.keys(eraConvidado.feitos).length) mesclarConvidado(eraConvidado);
      await sincronizar();
      if (location.search.includes("code=")) history.replaceState(null, "", location.pathname + location.hash);
    } else {
      perfil = null;
      carregar(CHAVE_CONVIDADO);
    }
    bonusDiario();
    desenharConta();
    rota();
  }

  // =====================================================================
  // Recompensas e conquistas
  // =====================================================================
  function toast(texto, cor = "amarelo") {
    const el = document.createElement("div");
    el.className = "toast";
    el.style.borderColor = `var(--${cor})`;
    el.style.color = `var(--${cor})`;
    el.textContent = texto;
    const caixa = $("#toasts");
    caixa.appendChild(el);
    while (caixa.children.length > 4) caixa.firstChild.remove();
    setTimeout(() => el.remove(), 3400);
  }

  function anunciarXP(xp, motivo, nivelAntes) {
    if (xp > 0) toast(`+${xp} XP · ${motivo}`);
    const nv = nivelDe(xpTotal());
    if (nv.n > nivelAntes) toast(`Subiu de nível! Nível ${nv.n}: ${nv.titulo}`, "roxo");
    checarConquistas();
    desenharConta();
  }

  function concluir(id, ajuda, motivo) {
    if (feito(id)) return 0;
    const antes = nivelDe(xpTotal()).n;
    const xp = xpItem(id, ajuda);
    S.feitos[id] = { ajuda, xp };
    salvar();
    anunciarXP(xp, motivo, antes);
    if (sb && usuario) {
      sb.from("progresso").insert({ user_id: usuario.id, item_id: id, ajuda }).then(({ error }) => {
        if (error && error.code !== "23505") { S.pend.progresso.push({ item_id: id, ajuda }); salvar(); }
      });
    }
    return xp;
  }

  function bonusDiario() {
    const hoje = hojeSP();
    if (S.bonus.includes(hoje)) return;
    const antes = nivelDe(xpTotal()).n;
    S.bonus.push(hoje);
    salvar();
    const seq = sequencia();
    anunciarXP(XP.bonus, `Bônus diário (${seq} dia${seq > 1 ? "s" : ""} seguido${seq > 1 ? "s" : ""})`, antes);
    if (sb && usuario) sb.from("bonus_diario").insert({ user_id: usuario.id }).then(() => {});
  }

  function conquistar(id) {
    if (S.conquistas.includes(id)) return;
    S.conquistas.push(id);
    salvar();
    toast(`★ Conquista: ${CONQ[id][1]}`, "rosa");
  }

  function checarConquistas() {
    const ids = Object.keys(S.feitos);
    if (ids.filter((i) => tipoItem(i) === "licao").length >= 10) conquistar("leitor");
    if (ids.some((i) => tipoItem(i) === "desafio")) conquistar("primeiro_desafio");
    if (ids.some((i) => tipoItem(i) === "chefe")) conquistar("cacador");
    if (CAPS.length && CAPS.every((c) => feito(`c${c.num}-chefe`))) conquistar("lenda");
    if (S.sem_dica >= 5) conquistar("autodidata");
    const seq = sequencia();
    if (seq >= 3) conquistar("streak3");
    if (seq >= 7) conquistar("streak7");
    if (xpTotal() >= 1000) conquistar("mil_xp");
  }

  // =====================================================================
  // Python no navegador (Pyodide num Web Worker)
  // =====================================================================
  const Py = {
    w: null, seq: 0, pend: new Map(), pronto: false, aquecendo: null, mpl: false,
    usaMpl: (codigo) => /\bmatplotlib\b/.test(codigo || ""),
    novo() {
      this.w = new Worker("worker.js?v=5");
      this.w.onmessage = (e) => {
        const { id, ok, r, erro } = e.data;
        const p = this.pend.get(id);
        if (!p) return;
        clearTimeout(p.t);
        this.pend.delete(id);
        if (ok) { this.pronto = true; p.res(r); } else p.rej(new Error(erro));
      };
      this.w.onerror = (e) => {
        e.preventDefault();
        const erro = new Error("carregar");
        for (const p of this.pend.values()) { clearTimeout(p.t); p.rej(erro); }
        this.pend.clear();
        this.w.terminate();
        this.w = null;
        this.aquecendo = null;
      };
    },
    chamar(tipo, args = {}) {
      if (!this.w) this.novo();
      return new Promise((res, rej) => {
        const id = ++this.seq;
        const pesado = !this.pronto || (this.usaMpl(args.codigo) && !this.mpl);
        const ms = pesado ? 120000 : 20000;
        const t = setTimeout(() => {
          this.pend.delete(id);
          const eraPronto = this.pronto;
          this.reiniciar();
          rej(new Error(eraPronto ? "tempo" : "carregar"));
        }, ms);
        this.pend.set(id, { res: (v) => { if (this.usaMpl(args.codigo)) this.mpl = true; res(v); }, rej, t });
        this.w.postMessage({ id, tipo, args });
      });
    },
    aquecer() {
      if (!this.aquecendo) this.aquecendo = this.chamar("ping").catch(() => { this.aquecendo = null; });
      return this.aquecendo;
    },
    reiniciar() {
      if (this.w) this.w.terminate();
      this.w = null;
      this.pronto = false;
      this.mpl = false;
      this.aquecendo = null;
      for (const p of this.pend.values()) { clearTimeout(p.t); p.rej(new Error("reiniciado")); }
      this.pend.clear();
    },
  };
  function msgErroPy(e) {
    if (e.message === "tempo") return "Seu código demorou demais e foi interrompido. Será que há um laço infinito?";
    if (e.message === "carregar") return "Não consegui carregar o Python. Confira sua conexão e tente de novo.";
    return "Erro interno: " + e.message;
  }

  // =====================================================================
  // Componentes
  // =====================================================================
  const KW = "False None True and as assert async await break class continue def del elif else except finally for from global if import in is lambda nonlocal not or pass raise return try while with yield".split(" ");
  const BI = "print len range list str int float sorted sum min max tuple input type bool dict set abs round enumerate zip".split(" ");
  const RX = new RegExp(
    String.raw`(#[^\n]*)|([fFrRbB]{0,2}(?:"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:\\.|[^"\\\n])*"?|'(?:\\.|[^'\\\n])*'?))` +
    String.raw`|\b(${KW.join("|")})\b|\b(${BI.join("|")})\b|\b(\d[\d_]*(?:\.\d+)?)\b`, "g");
  function realcar(codigo) {
    let out = "", i = 0, m;
    RX.lastIndex = 0;
    while ((m = RX.exec(codigo))) {
      if (m[0] === "") { RX.lastIndex++; continue; }
      out += esc(codigo.slice(i, m.index));
      const cls = m[1] ? "com" : m[2] ? "str" : m[3] ? "kw" : m[4] ? "bi" : "num";
      out += `<span class="hl-${cls}">${esc(m[0])}</span>`;
      i = m.index + m[0].length;
    }
    return out + esc(codigo.slice(i));
  }
  const pyRepr = (v) => JSON.stringify(v).replace(/"/g, "'");
  function descreverCtx(ctx) {
    if (!ctx) return "";
    const linhas = [];
    if (ctx.__entradas__) linhas.push("entradas digitadas: " + (ctx.__entradas__.length ? ctx.__entradas__.map(pyRepr).join(", ") : "(nenhuma)"));
    if (ctx.__arquivos__ && Object.keys(ctx.__arquivos__).length) linhas.push("arquivos na pasta: " + Object.keys(ctx.__arquivos__).join(", "));
    if (ctx.__env__ && Object.keys(ctx.__env__).length) linhas.push("variáveis de ambiente: " + Object.entries(ctx.__env__).map(([k, v]) => v === null ? `${k} (não existe)` : `${k}=${pyRepr(v)}`).join(", "));
    for (const [k, v] of Object.entries(ctx)) if (!k.startsWith("__")) linhas.push(`${k} = ${pyRepr(v)}`);
    return linhas.join("\n");
  }
  const blocoCodigo = (codigo) => `<pre class="codigo">${realcar(codigo)}</pre>`;

  function rico(paragrafos) {
    return paragrafos.map((p) => {
      if (p.startsWith("## ")) return `<h3>${esc(p.slice(3))}</h3>`;
      const html = p.split(/(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*)/).map((parte) => {
        if (!parte) return "";
        if (parte.startsWith("`")) return `<code>${esc(parte.slice(1, -1))}</code>`;
        if (parte.startsWith("**")) return `<strong>${esc(parte.slice(2, -2))}</strong>`;
        if (parte.length > 2 && parte.startsWith("*") && parte.endsWith("*")) return `<em>${esc(parte.slice(1, -1))}</em>`;
        return esc(parte);
      }).join("");
      return `<p>${html}</p>`;
    }).join("");
  }

  function criarEditor(el, codigo, { aoMudar, aoExecutar } = {}) {
    if (window.CodeMirror) {
      const cm = window.CodeMirror(el, {
        value: codigo, mode: "python", theme: "dracula", lineNumbers: true, indentUnit: 4, tabSize: 4,
        indentWithTabs: false, viewportMargin: Infinity,
        extraKeys: {
          Tab: (c) => (c.somethingSelected() ? c.indentSelection("add") : c.replaceSelection("    ")),
          "Shift-Tab": (c) => c.indentSelection("subtract"),
          "Ctrl-Enter": () => aoExecutar && aoExecutar(),
          "Cmd-Enter": () => aoExecutar && aoExecutar(),
        },
      });
      cm.on("change", () => aoMudar && aoMudar(cm.getValue()));
      setTimeout(() => cm.refresh(), 0);
      return { get: () => cm.getValue(), set: (v) => cm.setValue(v), foco: () => cm.focus() };
    }
    const ta = document.createElement("textarea");
    ta.className = "fallback";
    ta.spellcheck = false;
    ta.value = codigo;
    el.appendChild(ta);
    ta.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        e.preventDefault();
        ta.setRangeText("    ", ta.selectionStart, ta.selectionEnd, "end");
      } else if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) {
        e.preventDefault();
        if (aoExecutar) aoExecutar();
      } else if (e.key === "Enter") {
        const ini = ta.value.lastIndexOf("\n", ta.selectionStart - 1) + 1;
        const linha = ta.value.slice(ini, ta.selectionStart);
        let ind = linha.match(/^[ \t]*/)[0];
        if (linha.trimEnd().endsWith(":")) ind += "    ";
        e.preventDefault();
        ta.setRangeText("\n" + ind, ta.selectionStart, ta.selectionEnd, "end");
      }
      if (aoMudar) setTimeout(() => aoMudar(ta.value), 0);
    });
    ta.addEventListener("input", () => aoMudar && aoMudar(ta.value));
    return { get: () => ta.value, set: (v) => { ta.value = v; }, foco: () => ta.focus() };
  }

  function criarSaida(el) {
    el.innerHTML = `<div class="saida"><div class="cab mini">Saída</div><pre></pre><div class="graficos"></div></div>`;
    const pre = $("pre", el), gr = $(".graficos", el);
    return {
      limpar() { pre.textContent = ""; gr.innerHTML = ""; },
      img(b64) {
        const im = document.createElement("img");
        im.src = "data:image/png;base64," + b64;
        im.alt = "Gráfico gerado pelo seu código";
        gr.appendChild(im);
      },
      add(txt, cls) {
        const s = document.createElement("span");
        if (cls) s.className = cls;
        s.textContent = txt;
        pre.appendChild(s);
        pre.scrollTop = pre.scrollHeight;
      },
    };
  }

  async function rodarCodigo(codigo, ctx, saida, { vars = false } = {}) {
    saida.limpar();
    avisoCarregando(codigo, saida);
    try {
      const r = await Py.chamar("executar", { codigo, ctx });
      saida.limpar();
      if (r.saida) saida.add(r.saida);
      (r.imagens || []).forEach((b) => saida.img(b));
      if (r.erro) saida.add((r.saida && !r.saida.endsWith("\n") ? "\n" : "") + r.erro + "\n", "s-erro");
      else if (!r.saida && !(r.imagens || []).length) saida.add("(o programa rodou, mas não mostrou nada)\n", "s-info");
      if (!r.erro && vars && Object.keys(r.vars).length) {
        saida.add("\n── variáveis ──\n" + Object.entries(r.vars).map(([k, v]) => `${k} = ${v}`).join("\n") + "\n", "s-info");
      }
      if (!r.erro) conquistar("ola_mundo");
      return r;
    } catch (e) {
      saida.limpar();
      saida.add(msgErroPy(e) + "\n", "s-erro");
      return null;
    }
  }

  function avisoCarregando(codigo, saida) {
    if (!Py.pronto) saida.add("Carregando o Python (só demora na primeira vez)…\n", "s-info");
    if (Py.usaMpl(codigo) && !Py.mpl) saida.add("Carregando o matplotlib para os gráficos (só na primeira vez, pode levar uns 20 segundos)…\n", "s-info");
  }

  function modal(html, { classe = "" } = {}) {
    const fundo = document.createElement("div");
    fundo.className = "modal-fundo";
    fundo.innerHTML = `<div class="modal ${classe}">${html}</div>`;
    document.body.appendChild(fundo);
    const fechar = () => fundo.remove();
    fundo.addEventListener("click", (e) => { if (e.target === fundo) fechar(); });
    return { el: $(".modal", fundo), fechar };
  }
  function confirmar(titulo, texto, ok = "Continuar") {
    return new Promise((res) => {
      const m = modal(`<h2>${esc(titulo)}</h2><p class="mudo">${esc(texto)}</p>
        <div class="linha"><button class="btn neutro" data-v="0">Cancelar</button><button class="btn" data-v="1">${esc(ok)}</button></div>`);
      m.el.addEventListener("click", (e) => {
        const v = e.target.dataset.v;
        if (v !== undefined) { m.fechar(); res(v === "1"); }
      });
    });
  }

  async function compartilhar(texto) {
    const url = location.origin + location.pathname;
    try {
      if (navigator.share) { await navigator.share({ title: "PyQuest", text: texto, url }); return; }
      await navigator.clipboard.writeText(`${texto} ${url}`);
      toast("Texto copiado! Cole onde quiser.", "verde");
    } catch { /* cancelado */ }
  }

  // =====================================================================
  // Estrutura dos capítulos
  // =====================================================================
  let CAPS = [];
  const cap = (n) => CAPS[n - 1];
  function idsCap(n) {
    const c = cap(n);
    return [...c.licoes.map((_, i) => `c${n}-l${i}`), `c${n}-quiz`, ...c.desafios.map((_, i) => `c${n}-d${i}`), `c${n}-chefe`];
  }
  const fracCap = (n) => { const ids = idsCap(n); return ids.filter(feito).length / ids.length; };
  function capLiberado(n) {
    if (n === 1) return true;
    const pj = projetoDoCap(n);
    if (pj && pj.caps[0] === n) return feito(`c${ULTIMO_FUNDAMENTO}-chefe`);
    return feito(`c${n - 1}-chefe`);
  }
  function chefeLiberado(n) {
    const c = cap(n);
    const d = c.desafios.filter((_, i) => feito(`c${n}-d${i}`)).length;
    return feito(`c${n}-quiz`) && d >= Math.min(3, c.desafios.length);
  }
  function proximoPasso() {
    for (const c of CAPS) {
      const n = c.num;
      if (!capLiberado(n)) continue;
      for (let i = 0; i < c.licoes.length; i++)
        if (!feito(`c${n}-l${i}`)) return [`Cap. ${n} · Lição: ${c.licoes[i].titulo}`, `#/licao/${n}/${i}`];
      if (!feito(`c${n}-quiz`)) return [`Cap. ${n} · Quiz do capítulo`, `#/quiz/${n}`];
      for (let i = 0; i < c.desafios.length; i++)
        if (!feito(`c${n}-d${i}`)) return [`Cap. ${n} · Desafio: ${c.desafios[i].titulo}`, `#/desafio/${n}/${i}`];
      if (!feito(`c${n}-chefe`)) return [`Cap. ${n} · CHEFÃO: ${c.chefe.titulo}`, `#/desafio/${n}/chefe`];
    }
    return null;
  }

  // =====================================================================
  // Topo
  // =====================================================================
  function desenharConta() {
    const xp = xpTotal();
    const nv = nivelDe(xp);
    const seq = sequencia();
    let html = `<a class="chip-xp" href="#/perfil" title="${esc(nv.titulo)}"><span class="nv">${nv.n}</span>
      <span class="txt">${xp} XP</span>${seq ? `<span class="st">✹ ${seq}</span>` : ""}</a>`;
    if (sb && !usuario) html += `<button class="btn google pq" id="btn-entrar">Entrar</button>`;
    $("#conta").innerHTML = html;
    const b = $("#btn-entrar");
    if (b) b.onclick = entrarGoogle;
  }
  const botaoGoogle = (txt = "Entrar com Google") => `<button class="btn google grande js-google">
    <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true"><path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9 3.6l6.7-6.7C35.6 2.4 30.2 0 24 0 14.6 0 6.6 5.4 2.7 13.2l7.8 6.1C12.4 13.6 17.7 9.5 24 9.5z"/><path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-3.1-.4-4.5H24v9h12.7c-.6 3-2.3 5.5-4.8 7.2l7.5 5.8c4.4-4 7.1-10 7.1-17.5z"/><path fill="#FBBC05" d="M10.5 28.7c-.5-1.4-.8-3-.8-4.7s.3-3.3.8-4.7l-7.8-6.1C1 16.6 0 20.2 0 24s1 7.4 2.7 10.8l7.8-6.1z"/><path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.5-5.8c-2.1 1.4-4.9 2.3-8.4 2.3-6.3 0-11.6-4.1-13.5-9.8l-7.8 6.1C6.6 42.6 14.6 48 24 48z"/></svg>
    ${esc(txt)}</button>`;
  function ligarGoogle(raiz) { $$(".js-google", raiz).forEach((b) => (b.onclick = entrarGoogle)); }

  // =====================================================================
  // Roteador
  // =====================================================================
  let limpezas = [];
  let teclas = null;
  document.addEventListener("keydown", (e) => {
    if (!teclas) return;
    const alvo = e.target;
    if (alvo && (alvo.tagName === "INPUT" || alvo.tagName === "TEXTAREA" || alvo.closest?.(".CodeMirror"))) return;
    teclas(e);
  });
  function aoSair(fn) { limpezas.push(fn); }

  function rota() {
    const hash = location.hash || "#/";
    if (!hash.startsWith("#/")) return;
    limpezas.forEach((f) => { try { f(); } catch { /* */ } });
    limpezas = [];
    teclas = null;
    const p = hash.slice(2).split("/").filter(Boolean);
    const r = p[0] || "mapa";
    $$("#nav a").forEach((a) => a.classList.toggle("ativo",
      a.dataset.r === r || (a.dataset.r === "projetos" && r === "projeto") ||
      (["cap", "licao", "quiz", "desafio"].includes(r) && a.dataset.r === (+p[1] > ULTIMO_FUNDAMENTO ? "projetos" : "mapa"))));
    window.scrollTo(0, 0);
    const telas = {
      mapa: telaMapa, cap: () => telaCapitulo(+p[1]), licao: () => telaLicao(+p[1], +p[2]),
      quiz: () => telaQuiz(+p[1]), desafio: () => telaDesafio(+p[1], p[2]), relampago: telaRelampago,
      lab: telaLab, ranking: () => telaRanking(p[1] || "semana"), perfil: telaPerfil,
      projetos: telaProjetos, projeto: () => telaProjeto(p[1]),
    };
    try {
      (telas[r] || telaMapa)();
    } catch (e) {
      console.error(e);
      app.innerHTML = `<p>Página não encontrada. <a href="#/">Voltar ao início</a></p>`;
    }
  }

  // =====================================================================
  // Telas
  // =====================================================================
  function telaMapa() {
    const prox = proximoPasso();
    const nome = perfil?.apelido;
    let html = "";
    if (!usuario) {
      html += `<section class="hero">
        <h1>Aprenda <b>Python</b> jogando.</h1>
        <p>Lições curtas, desafios de código corrigidos na hora, chefões para derrotar e um ranking para disputar com gente do Brasil inteiro. Tudo grátis, direto no navegador.</p>
        <div class="feats"><span>${CAPS.length} capítulos</span><span>${CAPS.reduce((a, c) => a + c.licoes.length, 0)} lições</span><span>${CAPS.reduce((a, c) => a + c.desafios.length, 0)} desafios + ${CAPS.length} chefões</span><span>${CAPS.reduce((a, c) => a + c.quiz.length, 0)} perguntas de quiz</span><span>Ranking semanal</span><span>Python de verdade</span></div>
        <div class="linha">${prox ? `<a class="btn grande" href="${prox[1]}">Começar agora ▶</a>` : ""}
        ${sb ? botaoGoogle("Entrar para salvar e rankear") : ""}</div>
        ${sb ? `<p class="mudo" style="font-size:13px;margin-top:12px">Dá para jogar sem conta. Ao entrar, seu progresso vai junto.</p>` : ""}
      </section>`;
    } else {
      html += `<h1>Olá, ${esc(nome || "aventureiro(a)")}!</h1><p class="mudo">Continue de onde parou e suba no ranking da semana.</p>`;
    }
    html += prox
      ? `<div class="cartao proximo"><div class="espaco"><div class="mini verde">Próximo passo</div><h3>${esc(prox[0])}</h3></div><a class="btn" href="${prox[1]}">Continuar ▶</a></div>`
      : `<div class="cartao proximo"><h3 style="color:var(--verde)">Você completou a jornada! Treine no Relâmpago e no Laboratório.</h3></div>`;
    html += `<h2 style="margin:6px 0 12px">Mapa da Jornada</h2><div class="mini roxo" style="margin:18px 0 8px">Parte I · Fundamentos</div>`;
    html += CAPS.filter((c) => c.num <= ULTIMO_FUNDAMENTO).map(cartaoCap).join("");
    const projLib = feito(`c${ULTIMO_FUNDAMENTO}-chefe`);
    html += `<div class="mini roxo" style="margin:22px 0 8px">Parte II · Projetos</div>
      <a class="cartao projetos-chamada ${projLib ? "" : "trancado"}" href="#/projetos">
        <div class="espaco"><h3>${PROJETOS.map((p) => p.icone + " " + esc(p.titulo)).join(" &nbsp;·&nbsp; ")}</h3>
        <p class="mudo">${projLib ? "Projetos completos do livro, com mural para tirar dúvidas com outros alunos." : `🔒 Liberados ao derrotar o chefão do capítulo ${ULTIMO_FUNDAMENTO}. Dá para espiar o mural!`}</p></div>
        <span class="btn">Ver projetos →</span></a>`;
    app.innerHTML = html;
    ligarGoogle(app);
  }

  function cartaoCap(c) {
    let html = "";
    {
      const n = c.num, lib = capLiberado(n), ok = feito(`c${n}-chefe`), f = fracCap(n);
      html += `<div class="capcard ${ok ? "ok" : lib ? "" : "trancado"}"><div class="faixa"></div><div class="corpo">
        <div class="num">${n}</div>
        <div class="info"><h2>${esc(c.titulo)}</h2><div class="mudo">${esc(c.subtitulo)}</div>
          <div class="linha" style="gap:10px"><div class="barra espaco" style="max-width:300px"><i style="width:${f * 100}%"></i></div>
          <span class="mudo" style="font-size:13px">${ok ? "★ Concluído" : lib ? Math.round(f * 100) + "%" : projetoDoCap(n) && projetoDoCap(n).caps[0] === n ? `🔒 Derrote o chefão do cap. ${ULTIMO_FUNDAMENTO}` : "🔒 Derrote o chefão anterior"}</span></div></div>
        ${lib ? `<a class="btn ${ok ? "neutro" : ""}" href="#/cap/${n}">Entrar</a>` : ""}
      </div></div>`;
    }
    return html;
  }

  // =====================================================================
  // Projetos (Parte II do livro) e mural de discussão ao vivo
  // =====================================================================
  function telaProjetos() {
    let html = `<h1>Projetos</h1><p class="mudo" style="margin:4px 0 16px">Na Parte II do livro, você junta tudo o que aprendeu em projetos completos. Cada projeto tem um mural para trocar ideias e tirar dúvidas com outros alunos.</p>`;
    if (!feito(`c${ULTIMO_FUNDAMENTO}-chefe`))
      html += `<div class="cartao aviso-proj">🔒 Os capítulos dos projetos abrem quando você derrotar o chefão do capítulo ${ULTIMO_FUNDAMENTO}. Os murais já podem ser lidos.</div>`;
    for (const pj of PROJETOS) {
      const ids = pj.caps.flatMap(idsCap);
      const f = ids.filter(feito).length / ids.length;
      const ok = pj.caps.every((n) => feito(`c${n}-chefe`));
      html += `<a class="cartao projeto-card" href="#/projeto/${pj.id}"><div class="pj-ic">${pj.icone}</div>
        <div class="espaco"><h2>${esc(pj.titulo)}</h2><p class="mudo">${esc(pj.desc)}</p>
        <div class="linha" style="gap:10px"><div class="barra espaco" style="max-width:300px"><i style="width:${f * 100}%"></i></div>
        <span class="mudo" style="font-size:13px">${ok ? "★ Concluído" : Math.round(f * 100) + "%"} · capítulos ${pj.caps[0]} a ${pj.caps[pj.caps.length - 1]}</span></div></div>
        <span class="btn">Abrir</span></a>`;
    }
    app.innerHTML = html;
  }

  function telaProjeto(id) {
    const pj = PROJETOS.find((p) => p.id === id);
    if (!pj) { location.hash = "#/projetos"; return; }
    app.innerHTML = `<a class="voltar" href="#/projetos">← Projetos</a><div class="mini roxo">Projeto</div>
      <h1>${pj.icone} ${esc(pj.titulo)}</h1><p class="mudo" style="margin:4px 0 14px">${esc(pj.desc)}</p>
      <div class="projeto-grade"><div>${pj.caps.map((n) => cartaoCap(cap(n))).join("")}</div><section class="mural" id="mural"></section></div>`;
    montarMural(pj, $("#mural"));
  }

  function quando(iso) {
    const d = new Date(iso), seg = (Date.now() - d.getTime()) / 1000;
    if (seg < 60) return "agora";
    if (seg < 3600) return `há ${Math.floor(seg / 60)} min`;
    if (seg < 86400) return `há ${Math.floor(seg / 3600)} h`;
    return d.toLocaleDateString("pt-BR", { day: "2-digit", month: "2-digit" }) + " " + d.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
  }
  function formatarMsg(t) {
    return String(t).split("```").map((parte, i, arr) => {
      if (i % 2) return `<pre class="msg-cod">${esc(parte.replace(/^(python|py)?\n/, "").replace(/\n$/, ""))}</pre>`;
      let txt = parte;
      if (i > 0) txt = txt.replace(/^\n/, "");
      if (i < arr.length - 1) txt = txt.replace(/\n$/, "");
      return esc(txt).replace(/`([^`\n]+)`/g, "<code>$1</code>");
    }).join("");
  }

  async function montarMural(pj, el) {
    el.innerHTML = `<div class="mural-cab"><h2>💬 Mural do projeto</h2><span class="ao-vivo" id="mural-status"></span></div>
      <div class="mural-lista" id="mural-lista"><p class="mudo">Carregando mensagens…</p></div>
      <div id="mural-form"></div>
      <p class="mural-regras mudo">Seja gentil e não compartilhe dados pessoais. Para mostrar código, coloque entre três crases (\`\`\`). Mensagens com 3 denúncias somem. <a href="termos.html#mural">Regras do mural</a></p>`;
    const lista = $("#mural-lista", el), form = $("#mural-form", el), status = $("#mural-status", el);
    if (!sb) { lista.innerHTML = `<p class="mudo">O mural precisa de conexão com o servidor, e o site está em modo offline.</p>`; return; }
    if (usuario && souAdmin === null) {
      try { const { data } = await sb.rpc("sou_admin"); souAdmin = !!data; } catch { souAdmin = false; }
    }
    const msgs = new Map();
    let vivo = true;
    aoSair(() => { vivo = false; });

    function render() {
      if (!vivo) return;
      const perto = lista.scrollHeight - lista.scrollTop - lista.clientHeight < 80;
      const arr = [...msgs.values()].sort((a, b) => a.id - b.id);
      lista.innerHTML = arr.length ? arr.map((m) => {
        const meu = usuario && m.user_id === usuario.id;
        return `<div class="msg ${meu ? "minha" : ""}" data-id="${m.id}"><div class="msg-cab"><b>${esc(m.apelido)}</b>
          <span class="mudo">${quando(m.criado_em)}</span><span class="msg-acoes">
          ${meu || souAdmin ? `<button class="link" data-a="apagar">apagar</button>` : ""}
          ${usuario && !meu ? `<button class="link" data-a="denunciar">denunciar</button>` : ""}</span></div>
          <div class="msg-txt">${formatarMsg(m.texto)}</div></div>`;
      }).join("") : `<p class="mudo">Nenhuma mensagem ainda. Que tal começar a conversa?</p>`;
      if (perto) lista.scrollTop = lista.scrollHeight;
    }
    async function carregar() {
      const { data, error } = await sb.from("mensagens").select("id,user_id,apelido,texto,criado_em")
        .eq("projeto", pj.id).order("id", { ascending: false }).limit(80);
      if (!vivo) return;
      if (error) { lista.innerHTML = `<p class="mudo">Não consegui carregar o mural agora. Tente de novo mais tarde.</p>`; return; }
      msgs.clear();
      data.forEach((m) => msgs.set(m.id, m));
      render();
    }
    await carregar();
    lista.scrollTop = lista.scrollHeight;

    const canal = sb.channel("mural-" + pj.id)
      .on("postgres_changes", { event: "INSERT", schema: "public", table: "mensagens", filter: `projeto=eq.${pj.id}` },
        (p) => { msgs.set(p.new.id, p.new); render(); })
      .on("postgres_changes", { event: "DELETE", schema: "public", table: "mensagens" },
        (p) => { if (p.old && msgs.delete(p.old.id)) render(); })
      .subscribe((st) => { if (vivo) status.textContent = st === "SUBSCRIBED" ? "● ao vivo" : ""; });
    const timer = setInterval(carregar, 45000);
    aoSair(() => { clearInterval(timer); sb.removeChannel(canal); });

    lista.addEventListener("click", async (e) => {
      const a = e.target.dataset.a;
      if (!a) return;
      const id = +e.target.closest(".msg").dataset.id;
      if (a === "apagar") {
        const { error } = await sb.from("mensagens").delete().eq("id", id);
        if (error) return toast("Não consegui apagar: " + error.message, "vermelho");
        msgs.delete(id); render();
      } else if (a === "denunciar") {
        const { error } = await sb.rpc("denunciar", { mid: id });
        if (error) return toast("Não consegui registrar: " + error.message, "vermelho");
        e.target.remove();
        toast("Obrigado! A denúncia foi registrada.", "verde");
      }
    });

    if (!usuario) {
      form.innerHTML = `<div class="mural-entrar"><span class="mudo">Entre para participar da conversa.</span>${botaoGoogle("Entrar com Google")}</div>`;
      ligarGoogle(form);
      return;
    }
    form.innerHTML = `<div class="mural-form"><textarea id="mural-txt" maxlength="600" rows="3" placeholder="Escreva sua dúvida ou dica… (Ctrl+Enter envia)"></textarea>
      <div class="linha"><span class="mudo" id="mural-cont">0/600</span><button class="btn" id="mural-env">Enviar</button></div></div>`;
    const txt = $("#mural-txt", form), env = $("#mural-env", form), cont = $("#mural-cont", form);
    txt.addEventListener("input", () => { cont.textContent = `${txt.value.length}/600`; });
    async function enviar() {
      const texto = txt.value.trim();
      if (!texto) return;
      env.disabled = true;
      const { data, error } = await sb.from("mensagens").insert({ projeto: pj.id, texto })
        .select("id,user_id,apelido,texto,criado_em").single();
      env.disabled = false;
      if (error) return toast(error.message.includes("Calma") ? error.message : "Não consegui enviar: " + error.message, "vermelho");
      txt.value = ""; cont.textContent = "0/600";
      msgs.set(data.id, data); render();
      lista.scrollTop = lista.scrollHeight;
    }
    env.onclick = enviar;
    txt.addEventListener("keydown", (e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); enviar(); } });
  }

  function linhaItem(id, titulo, xpTxt, botao, href, { ativo = true, chefe = false, obs = "" } = {}) {
    const ok = feito(id);
    return `<div class="item ${ok ? "feito" : ""} ${chefe ? "chefe" : ""}">
      <span class="ic">${ok ? "✔" : ativo ? "○" : "🔒"}</span>
      <span class="tt">${esc(titulo)}${obs ? `<small>${esc(obs)}</small>` : ""}</span>
      <span class="xp">${esc(xpTxt)}</span>
      ${ativo ? `<a class="btn pq ${ok ? "neutro" : chefe ? "laranja" : ""}" href="${href}">${esc(botao)}</a>` : `<button class="btn pq" disabled>Bloqueado</button>`}
    </div>`;
  }

  function telaCapitulo(n) {
    const c = cap(n);
    if (!c || !capLiberado(n)) { location.hash = "#/"; return; }
    const f = fracCap(n);
    const pj = projetoDoCap(n);
    let html = `${pj ? `<a class="voltar" href="#/projeto/${pj.id}">← Projeto ${esc(pj.titulo)}</a>` : `<a class="voltar" href="#/">← Mapa</a>`}<div class="mini roxo">Capítulo ${n}</div><h1>${esc(c.titulo)}</h1>
      <p class="mudo" style="margin:4px 0 10px">${esc(c.subtitulo)}</p>
      <div class="linha"><div class="barra" style="width:min(360px,60vw)"><i style="width:${f * 100}%"></i></div><span class="mudo">${Math.round(f * 100)}% do capítulo</span></div>`;
    html += `<div class="mini secao">Lições</div>`;
    c.licoes.forEach((l, i) => { html += linhaItem(`c${n}-l${i}`, `Lição ${i + 1}: ${l.titulo}`, `+${XP.licao} XP`, feito(`c${n}-l${i}`) ? "Rever" : "Ler", `#/licao/${n}/${i}`); });
    const melhor = S.quiz_melhor[`c${n}-quiz`] || 0;
    html += `<div class="mini secao">Quiz</div>` + linhaItem(`c${n}-quiz`, `Quiz do capítulo (${c.quiz.length} perguntas)`, `+${XP.quiz} XP`, "Jogar", `#/quiz/${n}`,
      { obs: `Acerte ${Math.round(APROVACAO * 100)}% para passar · seu recorde: ${melhor}/${c.quiz.length}` });
    html += `<div class="mini secao">Desafios de código</div>`;
    c.desafios.forEach((d, i) => { html += linhaItem(`c${n}-d${i}`, d.titulo, `+${XP.desafio} XP`, feito(`c${n}-d${i}`) ? "Refazer" : "Resolver", `#/desafio/${n}/${i}`); });
    const lib = chefeLiberado(n);
    html += `<div class="mini secao">Chefão</div>` + linhaItem(`c${n}-chefe`, "♛ " + c.chefe.titulo, `+${XP.chefe} XP`, "Enfrentar", `#/desafio/${n}/chefe`,
      { ativo: lib, chefe: true, obs: lib ? "" : "Passe no quiz e resolva pelo menos 3 desafios para liberar." });
    app.innerHTML = html;
  }

  function telaLicao(n, i) {
    const c = cap(n);
    const l = c?.licoes[i];
    if (!l || !capLiberado(n)) { location.hash = "#/"; return; }
    const id = `c${n}-l${i}`;
    const ult = i + 1 >= c.licoes.length;
    app.innerHTML = `<div class="licao">
      <a class="voltar" href="#/cap/${n}">← Capítulo ${n}</a>
      <div class="mini roxo">Lição ${i + 1} de ${c.licoes.length} · ${esc(c.titulo)}</div>
      <h1 style="margin-bottom:16px">${esc(l.titulo)}</h1>
      <div class="rico">${rico(l.texto)}</div>
      <div class="mini" style="margin:18px 0 8px">Exemplo</div>
      ${blocoCodigo(l.exemplo)}
      <div class="barra-acoes"><button class="btn ciano" id="b-run">▶ Executar exemplo</button>
        <button class="btn neutro" id="b-lab">✎ Abrir no Laboratório</button></div>
      <div id="out" hidden></div>
      <div class="linha" style="margin-top:28px">
        ${i > 0 ? `<a class="btn neutro" href="#/licao/${n}/${i - 1}">← Anterior</a>` : ""}<span class="espaco"></span>
        <button class="btn" id="b-ok">${ult ? "Concluir e voltar ao capítulo" : "Concluir e ir para a próxima →"}${feito(id) ? "" : ` (+${XP.licao} XP)`}</button>
      </div></div>`;
    Py.aquecer();
    const outEl = $("#out");
    const saida = criarSaida(outEl);
    $("#b-run").onclick = () => { outEl.hidden = false; rodarCodigo(l.exemplo, l.ctx || {}, saida); };
    $("#b-lab").onclick = () => { S.codigo.lab = l.exemplo; salvar(); location.hash = "#/lab"; };
    $("#b-ok").onclick = () => {
      concluir(id, "nenhuma", "Lição concluída");
      location.hash = ult ? `#/cap/${n}` : `#/licao/${n}/${i + 1}`;
    };
  }

  function embaralhar(perguntas) {
    const mistura = (a) => { for (let k = a.length - 1; k > 0; k--) { const j = Math.floor(Math.random() * (k + 1)); [a[k], a[j]] = [a[j], a[k]]; } return a; };
    return mistura(perguntas.map((q) => {
      const ops = mistura(q.opcoes.map((o, k) => [k, o]));
      return { ...q, opcoes: ops.map((x) => x[1]), correta: ops.findIndex((x) => x[0] === q.correta) };
    }));
  }

  function telaQuiz(n) {
    const c = cap(n);
    if (!c || !capLiberado(n)) { location.hash = "#/"; return; }
    const est = { qs: embaralhar(c.quiz), i: 0, acertos: 0, combo: 0, max: 0, resp: false };
    app.innerHTML = `<div class="quiz"><a class="voltar" href="#/cap/${n}">← Capítulo ${n}</a><div id="qa"></div></div>`;
    const qa = $("#qa");

    function render() {
      if (est.i >= est.qs.length) return resultado();
      const q = est.qs[est.i];
      est.resp = false;
      qa.innerHTML = `<div class="linha"><span class="mini roxo">Quiz · Capítulo ${n} · Pergunta ${est.i + 1}/${est.qs.length}</span>
        <span class="espaco"></span>${est.combo >= 2 ? `<span class="combo">✹ Combo x${est.combo}</span>` : ""}</div>
        <div class="barra roxa" style="margin:10px 0 20px"><i style="width:${(est.i / est.qs.length) * 100}%"></i></div>
        <h2 style="margin-bottom:14px">${esc(q.pergunta)}</h2>${q.codigo ? blocoCodigo(q.codigo) : ""}
        <div style="margin-top:14px">${q.opcoes.map((o, k) => `<button class="opcao" data-k="${k}"><span class="k">${k + 1}</span><span>${esc(o)}</span></button>`).join("")}</div>
        <div id="fb"></div>`;
      $$(".opcao", qa).forEach((b) => (b.onclick = () => responder(+b.dataset.k)));
    }
    function responder(k) {
      if (est.resp) return;
      const q = est.qs[est.i];
      if (k >= q.opcoes.length) return;
      est.resp = true;
      const certo = k === q.correta;
      $$(".opcao", qa).forEach((b, j) => {
        b.disabled = true;
        if (j === q.correta) b.classList.add("certa"); else if (j === k) b.classList.add("errada");
      });
      if (certo) { est.acertos++; est.combo++; est.max = Math.max(est.max, est.combo); } else est.combo = 0;
      const ult = est.i + 1 >= est.qs.length;
      $("#fb", qa).innerHTML = `<h3 style="margin-top:16px;color:var(--${certo ? "verde" : "vermelho"})">${certo ? "Correto!" + (est.combo >= 2 ? ` Combo x${est.combo}!` : "") : "Não foi dessa vez."}</h3>
        <p class="mudo">${esc(q.explicacao)}</p><button class="btn" id="b-prox">${ult ? "Ver resultado" : "Próxima → (Enter)"}</button>`;
      $("#b-prox").onclick = avancar;
    }
    function avancar() { if (!est.resp) return; est.i++; render(); }
    function resultado() {
      teclas = null;
      const tot = est.qs.length, a = est.acertos, id = `c${n}-quiz`;
      const passou = a / tot >= APROVACAO;
      const recorde = a > (S.quiz_melhor[id] || 0);
      if (recorde) S.quiz_melhor[id] = a;
      salvar();
      const estrelas = a === tot ? 3 : a / tot >= 0.85 ? 2 : passou ? 1 : 0;
      qa.innerHTML = `<div class="cartao resultado"><div class="estrelas">${"★".repeat(estrelas)}${"☆".repeat(3 - estrelas)}</div>
        <h1>${a} / ${tot}</h1>
        <p style="color:var(--${passou ? "verde" : "laranja"})">${a === tot ? "Perfeito! Você dominou este capítulo." : passou ? "Aprovado! Agora encare os desafios de código." : `Você precisa de ${Math.round(APROVACAO * 100)}% para passar. Revise as lições e tente de novo!`}</p>
        <p class="mudo">Maior combo: ${est.max}${recorde ? " · novo recorde pessoal!" : ""}</p>
        <div class="linha" style="justify-content:center;margin-top:14px"><a class="btn neutro" href="#/quiz/${n}" id="b-again">Jogar de novo</a><a class="btn" href="#/cap/${n}">Voltar ao capítulo</a></div></div>`;
      $("#b-again").onclick = (e) => { e.preventDefault(); rota(); };
      if (a === tot) conquistar("quiz_perfeito");
      if (est.max >= 5) conquistar("combo5");
      if (passou) concluir(id, "nenhuma", "Quiz aprovado");
    }
    teclas = (e) => {
      if (/^[1-4]$/.test(e.key)) responder(+e.key - 1);
      else if (e.key === "Enter") avancar();
    };
    render();
  }

  function telaDesafio(n, i) {
    const c = cap(n);
    const chefe = i === "chefe";
    const d = c && (chefe ? c.chefe : c.desafios[+i]);
    if (!d || !capLiberado(n)) { location.hash = "#/"; return; }
    if (chefe && !chefeLiberado(n)) { location.hash = `#/cap/${n}`; return; }
    const idx = chefe ? "chefe" : +i;
    const id = chefe ? `c${n}-chefe` : `c${n}-d${i}`;
    const base = chefe ? XP.chefe : XP.desafio;
    const ctxTxt = descreverCtx(d.ctx);

    app.innerHTML = `<a class="voltar" href="#/cap/${n}">← Capítulo ${n}</a>
      <div class="linha"><div class="espaco"><div class="mini ${chefe ? "laranja" : "roxo"}">${chefe ? "Chefão" : `Desafio ${+i + 1} de ${c.desafios.length}`} · Capítulo ${n}</div>
      <h1>${chefe ? "♛ " : ""}${esc(d.titulo)}</h1></div>${feito(id) ? `<span style="color:var(--verde);font-weight:700">✔ Concluído</span>` : ""}</div>
      <div class="desafio" style="margin-top:16px">
        <div class="cartao"><div class="mini">Missão</div><div class="missao" style="margin-top:6px">${esc(d.enunciado)}</div>
          ${ctxTxt ? `<div class="mini" style="margin-top:14px">Dados do teste (usados no Executar)</div><pre class="codigo" style="margin-top:6px;white-space:pre-wrap">${esc(ctxTxt)}</pre>` : ""}
          ${d.ncasos > 1 ? `<p class="mudo" style="font-size:13px;margin:6px 0 0">O Verificar testa ${d.ncasos} situações diferentes.</p>` : ""}
          <p id="recompensa" style="font-weight:700;margin:14px 0 0"></p><div id="dica"></div></div>
        <div><div class="editor-wrap" id="ed"></div>
          <div class="barra-acoes"><button class="btn ciano" id="b-run">▶ Executar</button><button class="btn" id="b-ver">✔ Verificar</button>
            <button class="btn amarelo" id="b-dica">Dica</button><button class="btn laranja" id="b-sol">Ver solução</button>
            <span class="espaco"></span><span class="mudo" style="font-size:12px">Ctrl+Enter executa</span>
            <button class="btn neutro pq" id="b-reset" title="Recomeçar">↺</button></div>
          <div id="out"></div></div>
      </div>`;
    Py.aquecer();
    const saida = criarSaida($("#out"));
    saida.add("Escreva seu código, clique em Executar para testar e em Verificar para validar.\n", "s-info");
    const ed = criarEditor($("#ed"), S.codigo[id] ?? d.inicial, {
      aoMudar: (v) => { S.codigo[id] = v; salvar(); },
      aoExecutar: () => executar(),
    });
    const bSol = $("#b-sol");
    const tent = () => S.tentativas[id] || 0;
    function atualizar() {
      const r = $("#recompensa");
      if (feito(id)) { r.textContent = "Recompensa já recebida. Treine à vontade!"; r.style.color = "var(--mudo)"; }
      else if (S.solucoes.includes(id)) { r.textContent = `Recompensa: +${XP.solucao} XP (solução vista)`; r.style.color = "var(--laranja)"; }
      else if (S.dicas.includes(id)) { r.textContent = `Recompensa: +${Math.floor(base / 2)} XP (dica usada)`; r.style.color = "var(--amarelo)"; }
      else { r.textContent = `Recompensa: +${base} XP`; r.style.color = "var(--amarelo)"; }
      bSol.disabled = !(tent() >= 3 || feito(id) || S.solucoes.includes(id));
      bSol.title = bSol.disabled ? "Liberado após 3 tentativas" : "";
    }
    const mostrarDica = () => { $("#dica").innerHTML = `<div class="dica"><div class="mini" style="color:var(--amarelo)">Dica</div>${esc(d.dica)}</div>`; };
    if (S.dicas.includes(id)) mostrarDica();
    atualizar();

    const botoes = ["#b-run", "#b-ver"].map((s) => $(s));
    const ocupado = (v) => botoes.forEach((b) => (b.disabled = v));

    async function executar() {
      ocupado(true);
      await rodarCodigo(ed.get(), d.ctx, saida);
      ocupado(false);
    }
    async function verificar() {
      ocupado(true);
      saida.limpar();
      avisoCarregando(ed.get(), saida);
      let r;
      try { r = await Py.chamar("verificar", { cap: n, idx, codigo: ed.get() }); } catch (e) {
        saida.limpar(); saida.add(msgErroPy(e) + "\n", "s-erro"); ocupado(false); return;
      }
      ocupado(false);
      saida.limpar();
      if (!r.ok) {
        S.tentativas[id] = tent() + 1;
        salvar();
        saida.add("✘ Ainda não. " + r.msg + "\n", "s-erro");
        if (tent() >= 3 && !feito(id) && !S.solucoes.includes(id)) saida.add(`\n${tent()} tentativas. O botão "Ver solução" já está liberado.\n`, "s-info");
        atualizar();
        return;
      }
      saida.add("✔ " + r.msg + "\n", "s-ok");
      let ganho = 0;
      if (!feito(id)) {
        const ajuda = S.solucoes.includes(id) ? "solucao" : S.dicas.includes(id) ? "dica" : "nenhuma";
        if (ajuda === "nenhuma") S.sem_dica++;
        if (tent() >= 3) conquistar("persistente");
        ganho = concluir(id, ajuda, chefe ? "Chefão derrotado!" : "Desafio concluído");
        if (chefe && n === ULTIMO_FUNDAMENTO) toast("Projetos desbloqueados! Veja a aba Projetos.", "verde");
        else if (chefe && cap(n + 1) && capLiberado(n + 1) && projetoDoCap(n) === projetoDoCap(n + 1)) toast(`Capítulo ${n + 1} desbloqueado: ${cap(n + 1).titulo}`, "verde");
        atualizar();
      }
      vitoria(ganho);
    }
    function vitoria(ganho) {
      let prox = "";
      if (chefe) {
        const pj = projetoDoCap(n);
        if (n === ULTIMO_FUNDAMENTO) prox = `<a class="btn" href="#/projetos">Ver os projetos →</a>`;
        else if (pj && pj.caps.includes(n + 1)) prox = `<a class="btn" href="#/cap/${n + 1}">Ir para o Capítulo ${n + 1} →</a>`;
        else if (pj) prox = `<a class="btn" href="#/projeto/${pj.id}">Projeto concluído! →</a>`;
        else prox = `<a class="btn" href="#/cap/${n + 1}">Ir para o Capítulo ${n + 1} →</a>`;
      }
      else prox = +i + 1 < c.desafios.length ? `<a class="btn" href="#/desafio/${n}/${+i + 1}">Próximo desafio →</a>` : `<a class="btn" href="#/cap/${n}">Voltar ao capítulo →</a>`;
      const m = modal(`<h2>${chefe ? "♛ Chefão derrotado!" : "✔ Desafio concluído!"}</h2>
        ${ganho ? `<p style="color:var(--amarelo);font-weight:700;font-size:18px">+${ganho} XP</p>` : `<p class="mudo">Muito bem!</p>`}
        <div class="linha"><button class="btn neutro" data-a="fechar">Continuar aqui</button>${chefe ? `<button class="btn roxo" data-a="share">Compartilhar</button>` : ""}${prox}</div>`, { classe: "vitoria" });
      m.el.addEventListener("click", (e) => {
        const a = e.target.dataset.a;
        if (a === "fechar" || e.target.tagName === "A") m.fechar();
        if (a === "share") compartilhar(`Derrotei o chefão "${d.titulo}" no PyQuest e estou aprendendo Python jogando!`);
      });
      aoSair(m.fechar);
    }

    $("#b-run").onclick = executar;
    $("#b-ver").onclick = verificar;
    $("#b-dica").onclick = async () => {
      if (!S.dicas.includes(id)) {
        if (!feito(id) && !(await confirmar("Usar dica?", "A dica reduz a recompensa deste desafio pela metade."))) return;
        S.dicas.push(id); salvar();
      }
      mostrarDica(); atualizar();
    };
    bSol.onclick = async () => {
      if (!S.solucoes.includes(id) && !feito(id)) {
        if (!(await confirmar("Ver solução?", `A recompensa cai para ${XP.solucao} XP. Você ainda vai precisar verificar o código.`))) return;
        S.solucoes.push(id); salvar();
      }
      saida.limpar();
      saida.add("Uma solução possível:\n\n", "s-info");
      saida.add(d.solucao + "\n", "s-ok");
      saida.add("\nEntenda cada linha, digite (ou adapte) no editor e clique em Verificar.\n", "s-info");
      atualizar();
    };
    $("#b-reset").onclick = async () => {
      if (await confirmar("Recomeçar?", "Apagar seu código e voltar ao código inicial?", "Recomeçar")) {
        ed.set(d.inicial); S.codigo[id] = d.inicial; salvar();
      }
    };
  }

  function telaRelampago() {
    const pool = CAPS.filter((c) => capLiberado(c.num)).flatMap((c) => c.quiz);
    app.innerHTML = `<h1>⚡ Desafio Relâmpago</h1>
      <p class="mudo" style="max-width:720px">${TEMPO_RELAMPAGO} segundos para acertar o máximo de perguntas dos capítulos que você já liberou. Cada erro custa 3 segundos. Seu recorde entra no ranking Relâmpago${sb && !usuario ? " (entre com Google para participar)" : ""}.</p>
      <div id="area"><div class="cartao resultado"><div class="estrelas">⚡</div><h2>Recorde: ${S.recorde} acertos</h2>
        <p class="mudo">${pool.length} perguntas disponíveis</p><button class="btn grande" id="b-go">Começar!</button></div></div>`;
    $("#b-go").onclick = () => jogo(pool);
  }

  function jogo(pool) {
    const area = $("#area");
    const est = { fila: embaralhar(pool), q: null, acertos: 0, erros: 0, tempo: TEMPO_RELAMPAGO, fim: false };
    area.innerHTML = `<div class="cartao linha" id="placar"><span id="tempo" style="font-size:22px;font-weight:800"></span><span class="espaco"></span><span id="pts" style="font-weight:700"></span></div><div id="qa" style="margin-top:16px"></div>`;
    const qa = $("#qa"), placar = $("#placar");
    const timer = setInterval(() => { est.tempo--; desenhar(); if (est.tempo <= 0) terminar(); }, 1000);
    aoSair(() => clearInterval(timer));
    function desenhar() {
      const t = $("#tempo");
      if (!t) return;
      t.textContent = `⏱ ${Math.max(0, est.tempo)}s`;
      t.style.color = est.tempo <= 10 ? "var(--vermelho)" : "var(--amarelo)";
      $("#pts").textContent = `✔ ${est.acertos}   ✘ ${est.erros}`;
    }
    function proxima() {
      if (!est.fila.length) est.fila = embaralhar(pool);
      const q = (est.q = est.fila.pop());
      qa.innerHTML = `<h2 style="margin-bottom:12px">${esc(q.pergunta)}</h2>${q.codigo ? blocoCodigo(q.codigo) : ""}
        <div style="margin-top:12px">${q.opcoes.map((o, k) => `<button class="opcao" data-k="${k}"><span class="k">${k + 1}</span><span>${esc(o)}</span></button>`).join("")}</div>`;
      $$(".opcao", qa).forEach((b) => (b.onclick = () => responder(+b.dataset.k)));
    }
    function responder(k) {
      if (est.fim || k >= est.q.opcoes.length) return;
      const ok = k === est.q.correta;
      if (ok) est.acertos++; else { est.erros++; est.tempo -= 3; }
      placar.classList.remove("flash-ok", "flash-erro");
      void placar.offsetWidth;
      placar.classList.add(ok ? "flash-ok" : "flash-erro");
      desenhar();
      if (est.tempo <= 0) return terminar();
      proxima();
    }
    function terminar() {
      if (est.fim) return;
      est.fim = true;
      clearInterval(timer);
      teclas = null;
      const a = est.acertos;
      const novo = a > S.recorde;
      if (novo) S.recorde = a;
      salvar();
      if (sb && usuario && a > 0) {
        sb.from("relampago").insert({ user_id: usuario.id, acertos: Math.min(60, a) }).then(({ error }) => {
          if (error) { S.pend.relampago.push(a); salvar(); }
        });
      }
      if (a >= 8) conquistar("raio");
      area.innerHTML = `<div class="cartao resultado"><h2>Tempo esgotado!</h2><div class="estrelas" style="letter-spacing:0">${a}</div>
        <p class="mudo">acertos · ${est.erros} erros</p>${novo && a > 0 ? `<h3 style="color:var(--rosa)">★ Novo recorde! ★</h3>` : ""}
        ${sb && !usuario ? `<p class="mudo">Entre com Google para seu recorde aparecer no ranking.</p>${botaoGoogle()}` : ""}
        <div class="linha" style="justify-content:center;margin-top:14px"><button class="btn" id="b-de-novo">Jogar de novo</button>
        <a class="btn neutro" href="#/ranking/relampago">Ver ranking</a></div></div>`;
      ligarGoogle(area);
      $("#b-de-novo").onclick = () => telaRelampago();
    }
    teclas = (e) => { if (/^[1-4]$/.test(e.key)) responder(+e.key - 1); };
    desenhar();
    proxima();
  }

  function telaLab() {
    const padrao = "# Experimente à vontade!\nlinguagens = ['python', 'c', 'rust']\nfor l in linguagens:\n    print(l.title())\n";
    app.innerHTML = `<h1>✎ Laboratório</h1><p class="mudo">Espaço livre para experimentar. Nada aqui vale nota: teste ideias, quebre coisas e aprenda!</p>
      <div class="editor-wrap lab" id="ed"></div>
      <div class="barra-acoes"><button class="btn ciano" id="b-run">▶ Executar</button><button class="btn neutro" id="b-clr">Limpar saída</button>
      <span class="espaco"></span><span class="mudo" style="font-size:12px">Ctrl+Enter executa</span></div><div id="out"></div>`;
    Py.aquecer();
    const saida = criarSaida($("#out"));
    const ed = criarEditor($("#ed"), S.codigo.lab ?? padrao, {
      aoMudar: (v) => { S.codigo.lab = v; salvar(); }, aoExecutar: () => executar(),
    });
    async function executar() {
      $("#b-run").disabled = true;
      await rodarCodigo(ed.get(), {}, saida, { vars: true });
      $("#b-run").disabled = false;
      S.lab++; salvar();
      if (S.lab >= 15) conquistar("cientista");
    }
    $("#b-run").onclick = executar;
    $("#b-clr").onclick = () => saida.limpar();
  }

  async function telaRanking(aba) {
    const abas = [["semana", "Esta semana"], ["geral", "Geral"], ["relampago", "⚡ Relâmpago"]];
    app.innerHTML = `<h1>🏆 Ranking</h1><p class="mudo">O ranking semanal recomeça toda segunda-feira (horário de Brasília). Bônus diário, lições, quizzes, desafios e chefões contam pontos.</p>
      <div class="abas">${abas.map(([k, t]) => `<button data-a="${k}" class="${k === aba ? "ativo" : ""}">${t}</button>`).join("")}</div>
      ${sb && !usuario ? `<div class="cartao linha" style="margin-bottom:14px"><span class="espaco">Entre para aparecer no ranking. Seu progresso atual vai junto.</span>${botaoGoogle()}</div>` : ""}
      <div class="cartao" id="tab"><span class="carregando">Carregando ranking…</span></div>`;
    ligarGoogle(app);
    $$(".abas button").forEach((b) => (b.onclick = () => { location.hash = `#/ranking/${b.dataset.a}`; }));
    const tab = $("#tab");
    if (!sb) {
      tab.innerHTML = `<p>O ranking online ainda não está configurado neste site (modo offline).</p><p class="mudo">Seu progresso fica salvo neste navegador.</p>`;
      return;
    }
    const { data, error } = aba === "relampago"
      ? await sb.rpc("ranking_relampago", { limite: 50 })
      : await sb.rpc("ranking", { periodo: aba, limite: 50 });
    if (!tab.isConnected) return;
    if (error) { tab.innerHTML = `<p class="s-erro">Não consegui carregar o ranking. Tente de novo em instantes.</p>`; return; }
    if (!data.length) { tab.innerHTML = `<p>Ninguém pontuou ainda${aba === "semana" ? " nesta semana" : ""}. Que tal ser o primeiro?</p>`; return; }
    const medalha = (p) => (p === 1 ? "🥇" : p === 2 ? "🥈" : p === 3 ? "🥉" : p);
    const linhas = data.map((r) => {
      const eu = usuario && r.user_id === usuario.id;
      if (aba === "relampago") {
        return `<tr class="${eu ? "eu" : ""}"><td class="pos">${medalha(r.posicao)}</td><td>${esc(r.apelido)}${eu ? " <span class='mudo'>(você)</span>" : ""}</td><td class="num">${r.acertos}</td></tr>`;
      }
      const nv = nivelDe(aba === "geral" ? r.xp : 0);
      return `<tr class="${eu ? "eu" : ""}"><td class="pos">${medalha(r.posicao)}</td>
        <td>${esc(r.apelido)}${eu ? " <span class='mudo'>(você)</span>" : ""}${aba === "geral" ? `<div class="nivel-tag">Nv. ${nv.n} · ${esc(nv.titulo)}</div>` : ""}</td>
        <td class="num">${r.chefes}</td><td class="num">${r.xp}</td></tr>`;
    }).join("");
    tab.innerHTML = aba === "relampago"
      ? `<table class="rank"><thead><tr><th>#</th><th>Jogador</th><th class="num">Acertos</th></tr></thead><tbody>${linhas}</tbody></table>`
      : `<table class="rank"><thead><tr><th>#</th><th>Jogador</th><th class="num">♛</th><th class="num">XP</th></tr></thead><tbody>${linhas}</tbody></table>`;
  }

  function telaPerfil() {
    const xp = xpTotal(), nv = nivelDe(xp), ids = Object.keys(S.feitos);
    const cont = (t) => ids.filter((i) => tipoItem(i) === t).length;
    const frac = nv.prox ? (xp - nv.ini) / (nv.prox - nv.ini) : 1;
    let html = `<h1>${usuario ? esc(perfil?.apelido || "Seu perfil") : "Seu progresso"}</h1>
      <p class="mudo">Nível ${nv.n} · ${esc(nv.titulo)}${nv.prox ? ` · faltam ${nv.prox - xp} XP para o nível ${nv.n + 1}` : " · nível máximo!"}</p>
      <div class="barra" style="max-width:420px;margin-top:8px"><i style="width:${frac * 100}%"></i></div>
      <div class="stats">
        <div class="stat"><b style="color:var(--amarelo)">${xp}</b><span class="mudo">XP total</span></div>
        <div class="stat"><b style="color:var(--ciano)">${cont("licao")}</b><span class="mudo">Lições</span></div>
        <div class="stat"><b style="color:var(--verde)">${cont("desafio")}</b><span class="mudo">Desafios</span></div>
        <div class="stat"><b style="color:var(--laranja)">${cont("chefe")}/${CAPS.length}</b><span class="mudo">Chefões</span></div>
        <div class="stat"><b style="color:var(--rosa)">${S.recorde}</b><span class="mudo">Recorde ⚡</span></div>
        <div class="stat"><b style="color:var(--laranja)">${sequencia()} d</b><span class="mudo">Sequência</span></div>
      </div>`;
    if (usuario) {
      html += `<div class="cartao" style="margin-bottom:18px"><div class="mini">Seu apelido no ranking</div>
        <form id="f-apelido" class="linha" style="margin-top:8px"><input class="campo" id="apelido" maxlength="20" value="${esc(perfil?.apelido || "")}">
        <button class="btn">Salvar</button><span class="mudo" style="font-size:13px">3 a 20 caracteres: letras, números, espaço, _ . -</span></form></div>`;
    } else if (sb) {
      html += `<div class="cartao linha" style="margin-bottom:18px"><span class="espaco">Você está jogando sem conta: o progresso fica só neste navegador. Entre para salvar na nuvem e entrar no ranking.</span>${botaoGoogle()}</div>`;
    }
    html += `<div class="mini" style="margin-bottom:8px">Conquistas (${S.conquistas.length}/${CONQUISTAS.length})</div><div class="grade">` +
      CONQUISTAS.map(([cid, nome, desc]) => {
        const tem = S.conquistas.includes(cid);
        return `<div class="medalha ${tem ? "tem" : ""}"><span class="m">${tem ? "★" : "☆"}</span><span><b>${esc(nome)}</b><span class="mudo" style="font-size:13px">${esc(desc)}</span></span></div>`;
      }).join("") + `</div>
      <div class="linha" style="margin-top:28px">${usuario ? `<button class="btn neutro" id="b-sair">Sair da conta</button>` : ""}
      <span class="espaco"></span><button class="btn vermelho" id="b-zerar">Zerar progresso</button></div>`;
    app.innerHTML = html;
    ligarGoogle(app);
    const f = $("#f-apelido");
    if (f) f.onsubmit = async (e) => {
      e.preventDefault();
      const v = $("#apelido").value.trim();
      if (!/^[A-Za-zÀ-ÿ0-9_. -]{3,20}$/.test(v)) return toast("Apelido inválido: use 3 a 20 letras, números, espaço, _ . -", "vermelho");
      const { error } = await sb.from("perfis").update({ apelido: v }).eq("id", usuario.id);
      if (error) return toast(error.code === "23505" ? "Esse apelido já está em uso." : "Não deu para salvar: " + error.message, "vermelho");
      perfil = { ...perfil, apelido: v };
      toast("Apelido salvo!", "verde");
    };
    const bs = $("#b-sair");
    if (bs) bs.onclick = sair;
    $("#b-zerar").onclick = async () => {
      if (!(await confirmar("Zerar progresso?", usuario ? "Isso apaga TODO o seu XP, conquistas e posição no ranking, também na nuvem. Não dá para desfazer." : "Isso apaga todo o progresso salvo neste navegador.", "Zerar tudo"))) return;
      if (sb && usuario) {
        await Promise.all([
          sb.from("progresso").delete().eq("user_id", usuario.id),
          sb.from("bonus_diario").delete().eq("user_id", usuario.id),
          sb.from("relampago").delete().eq("user_id", usuario.id),
        ]);
      }
      S = PADRAO();
      try { localStorage.setItem(chaveLS, JSON.stringify(S)); } catch { /* */ }
      desenharConta();
      location.hash = "#/";
      rota();
    };
  }

  // =====================================================================
  // Início
  // =====================================================================
  async function iniciar() {
    carregar(CHAVE_CONVIDADO);
    try {
      const r = await fetch("conteudo.json?v=5");
      CAPS = await r.json();
    } catch {
      app.innerHTML = `<p>Não consegui carregar o conteúdo. Recarregue a página.</p>`;
      return;
    }
    window.addEventListener("hashchange", rota);
    if (sb) {
      const { data } = await sb.auth.getSession();
      await aoMudarSessao(data.session, true);
      sb.auth.onAuthStateChange((_ev, session) => { setTimeout(() => aoMudarSessao(session), 0); });
    } else {
      bonusDiario();
      desenharConta();
      rota();
    }
  }
  iniciar();
})();
