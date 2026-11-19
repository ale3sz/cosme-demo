/* ==========================================================================
   MODULE: THEME CONTROLLER (NIGHT NEON <-> DAY CAFÉ)
   ========================================================================== */

export function initTheme() {
  const html = document.documentElement;
  const themeToggle = document.getElementById('theme-toggle');
  const themeColorMeta = document.getElementById('theme-color-meta');
  const leverKnob = themeToggle ? themeToggle.querySelector('.lever-knob') : null;

  const MOON_ICON =
    '<svg width="11" height="11" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  const SUN_ICON =
    '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';

  function setTheme(mode) {
    const isNight = mode === 'night';
    html.setAttribute('data-theme', mode);

    if (themeToggle) {
      themeToggle.setAttribute('aria-checked', String(isNight));
    }
    if (themeColorMeta) {
      themeColorMeta.setAttribute('content', isNight ? '#090A0D' : '#F8F6F1');
    }
    if (leverKnob) {
      leverKnob.innerHTML = isNight ? MOON_ICON : SUN_ICON;
    }

    try {
      localStorage.setItem('cosme-theme', mode);
    } catch (_) {}
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', () => {
      const current = html.getAttribute('data-theme') === 'day' ? 'day' : 'night';
      setTheme(current === 'night' ? 'day' : 'night');
    });
  }

  // Cargar preferencia guardada si existe
  try {
    const saved = localStorage.getItem('cosme-theme');
    if (saved === 'day' || saved === 'night') {
      setTheme(saved);
    }
  } catch (_) {}
}
