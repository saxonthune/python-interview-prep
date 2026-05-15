const SOL_PREFIX = 'solution:';
const HASH_PREFIX = 'skeleton_hash:';

async function sha1(s: string): Promise<string> {
  const buf = new TextEncoder().encode(s);
  const digest = await crypto.subtle.digest('SHA-1', buf);
  return [...new Uint8Array(digest)]
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
}

export async function loadSolution(
  id: string,
  skeleton: string,
): Promise<{ code: string; skeletonChanged: boolean }> {
  const saved = localStorage.getItem(SOL_PREFIX + id);
  if (saved == null) {
    return { code: skeleton, skeletonChanged: false };
  }
  // If the saved code is byte-identical to the current skeleton, there's
  // nothing for the user to lose — treat as unchanged regardless of hash.
  if (saved === skeleton) {
    return { code: saved, skeletonChanged: false };
  }
  const savedHash = localStorage.getItem(HASH_PREFIX + id);
  if (savedHash == null) {
    return { code: saved, skeletonChanged: false };
  }
  const currentHash = await sha1(skeleton);
  return { code: saved, skeletonChanged: savedHash !== currentHash };
}

export async function saveSolution(id: string, code: string, skeleton: string): Promise<void> {
  // Don't persist an untouched skeleton — keeps localStorage clean and
  // prevents stale skeleton_hash entries from raising false "changed" alarms.
  if (code === skeleton) {
    clearSolution(id);
    return;
  }
  localStorage.setItem(SOL_PREFIX + id, code);
  localStorage.setItem(HASH_PREFIX + id, await sha1(skeleton));
}

export function clearSolution(id: string): void {
  localStorage.removeItem(SOL_PREFIX + id);
  localStorage.removeItem(HASH_PREFIX + id);
}

export function clearAllSolutions(): number {
  const keys: string[] = [];
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (k && (k.startsWith(SOL_PREFIX) || k.startsWith(HASH_PREFIX))) {
      keys.push(k);
    }
  }
  keys.forEach((k) => localStorage.removeItem(k));
  return keys.length;
}

export function debounce<A extends unknown[]>(
  fn: (...args: A) => void,
  ms: number,
): (...args: A) => void {
  let t: ReturnType<typeof setTimeout> | null = null;
  return (...args: A) => {
    if (t) clearTimeout(t);
    t = setTimeout(() => fn(...args), ms);
  };
}
