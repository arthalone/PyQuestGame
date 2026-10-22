// Web Worker: roda o Python (Pyodide) fora da tela principal.
const PYODIDE = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
const VERSAO = "5";
let ponte = null;
let iniciando = null;
let pyodide = null;
let mpl = null;

// Carrega o matplotlib (e o numpy) só quando o código do aluno usa gráficos.
async function prepararPacotes(codigo) {
  if (!/\bmatplotlib\b/.test(codigo || "")) return;
  if (!mpl) mpl = pyodide.loadPackage("matplotlib").catch((e) => { mpl = null; throw e; });
  await mpl;
}

async function iniciar() {
  if (ponte) return;
  if (!iniciando) {
    iniciando = (async () => {
      importScripts(PYODIDE + "pyodide.js");
      const py = await loadPyodide({ indexURL: PYODIDE });
      pyodide = py;
      for (const nome of ["django_treino", "conteudo", "motor", "ponte"]) {
        const r = await fetch(`py/${nome}.py?v=${VERSAO}`);
        if (!r.ok) throw new Error(`Não consegui carregar py/${nome}.py`);
        py.FS.writeFile(`/home/pyodide/${nome}.py`, await r.text());
      }
      py.runPython("import sys\nif '/home/pyodide' not in sys.path: sys.path.insert(0, '/home/pyodide')");
      ponte = py.pyimport("ponte");
    })();
  }
  await iniciando;
}

self.onmessage = async (e) => {
  const { id, tipo, args } = e.data;
  try {
    await iniciar();
    if (args && args.codigo) await prepararPacotes(args.codigo);
    let r = null;
    if (tipo === "executar") r = ponte.executar(args.codigo, JSON.stringify(args.ctx || {}));
    else if (tipo === "verificar") r = ponte.verificar(args.cap, String(args.idx), args.codigo);
    self.postMessage({ id, ok: true, r: r ? JSON.parse(r) : null });
  } catch (err) {
    self.postMessage({ id, ok: false, erro: String(err && err.message || err) });
  }
};
