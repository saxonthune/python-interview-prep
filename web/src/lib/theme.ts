// Tiny theme helper. The pre-paint setter lives inline in each page's <head>
// (see THEME_INIT below) so the saved preference is applied before first paint
// and there's no flash. This module handles the runtime toggle.

export const THEME_INIT = `
(function () {
  try {
    var saved = localStorage.getItem('theme');
    var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    var theme = saved || (prefersDark ? 'dark' : 'light');
    document.documentElement.setAttribute('data-theme', theme);
  } catch (e) {}
})();
`;

export function attachThemeToggle(buttonId: string): void {
  const btn = document.getElementById(buttonId);
  if (!btn) return;
  const sync = () => {
    const t = document.documentElement.getAttribute('data-theme') || 'light';
    btn.textContent = t === 'dark' ? '☀' : '☾';
    btn.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  };
  sync();
  btn.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    localStorage.setItem('theme', next);
    sync();
  });
}
