// Main-thread proxy to a Web Worker that hosts Pyodide. Doing the work
// off-thread keeps the page interactive while wasm compiles (multi-second
// blocking operation otherwise) and while user code runs.

export interface RunResult {
  output: string;
  errored: boolean;
}

interface WorkerMessage {
  id: number;
  type: 'ready' | 'error' | 'result';
  output?: string;
  errored?: boolean;
  error?: string;
}

let worker: Worker | null = null;
let readyPromise: Promise<void> | null = null;
let msgId = 0;
const pending = new Map<number, (msg: WorkerMessage) => void>();

function getWorker(): Worker {
  if (worker) return worker;
  const base = (import.meta.env.BASE_URL || '/').replace(/\/?$/, '/');
  worker = new Worker(base + 'pyodide.worker.js');
  worker.onmessage = (e: MessageEvent<WorkerMessage>) => {
    const cb = pending.get(e.data.id);
    if (cb) {
      pending.delete(e.data.id);
      cb(e.data);
    }
  };
  return worker;
}

function send<T = WorkerMessage>(type: 'init' | 'run', payload: unknown): Promise<T> {
  const w = getWorker();
  return new Promise((resolve, reject) => {
    const id = ++msgId;
    pending.set(id, (msg) => {
      if (msg.type === 'error') reject(new Error(msg.error || 'pyodide error'));
      else resolve(msg as T);
    });
    w.postMessage({ id, type, payload });
  });
}

export function ensurePyodide(): Promise<void> {
  if (readyPromise) return readyPromise;
  const base = (import.meta.env.BASE_URL || '/').replace(/\/?$/, '/');
  readyPromise = send('init', { base }).then(() => undefined);
  // If init fails, allow a retry on the next call.
  readyPromise.catch(() => { readyPromise = null; });
  return readyPromise;
}

export async function runProblem(args: {
  kind: 'function' | 'class' | 'multi';
  payload: unknown;
  userCode: string;
}): Promise<RunResult> {
  await ensurePyodide();
  const msg = await send('run', args);
  return { output: msg.output || '', errored: !!msg.errored };
}
