// Pyodide host that runs in a Web Worker so wasm compile + execution don't
// block the page's main thread. The main thread talks to this worker via
// structured-cloned messages: init -> ready, run -> result.

const PYODIDE_VERSION = '0.26.2';
const CDN = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

importScripts(CDN + 'pyodide.js');

let pyodideReadyPromise = null;
let baseUrl = '/';

async function bootstrap() {
  // eslint-disable-next-line no-undef
  const pyodide = await loadPyodide({ indexURL: CDN });
  const [utilsSrc, harnessSrc] = await Promise.all([
    fetch(baseUrl + 'utils.py').then((r) => r.text()),
    fetch(baseUrl + 'web_harness.py').then((r) => r.text()),
  ]);
  pyodide.FS.writeFile('utils.py', utilsSrc);
  pyodide.FS.writeFile('web_harness.py', harnessSrc);
  return pyodide;
}

self.onmessage = async (e) => {
  const { id, type, payload } = e.data;

  if (type === 'init') {
    baseUrl = payload && payload.base ? payload.base : '/';
    if (!pyodideReadyPromise) pyodideReadyPromise = bootstrap();
    try {
      await pyodideReadyPromise;
      self.postMessage({ id, type: 'ready' });
    } catch (err) {
      self.postMessage({ id, type: 'error', error: String(err) });
    }
    return;
  }

  if (type === 'run') {
    try {
      const pyodide = await pyodideReadyPromise;
      let buf = '';
      pyodide.setStdout({ batched: (s) => (buf += s + '\n') });
      pyodide.setStderr({ batched: (s) => (buf += s + '\n') });
      pyodide.globals.set('__user_code__', payload.userCode);
      pyodide.globals.set('__kind__', payload.kind);
      pyodide.globals.set('__payload__', payload.payload);
      pyodide.runPython(`
import traceback
import web_harness

payload = __payload__.to_py() if hasattr(__payload__, "to_py") else __payload__

user_ns = {}
try:
    exec(compile(__user_code__, "<solution>", "exec"), user_ns)
except Exception:
    traceback.print_exc()
else:
    try:
        web_harness.run_problem(__kind__, payload, user_ns)
    except Exception:
        traceback.print_exc()
`);
      self.postMessage({ id, type: 'result', output: buf, errored: false });
    } catch (err) {
      self.postMessage({ id, type: 'result', output: `[worker] ${err}\n`, errored: true });
    }
  }
};
