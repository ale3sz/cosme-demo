/* ==========================================================================
   COSME ALBERDI — UI SCRIPT (vanilla, sin dependencias)
   Tema día/noche · Tabs con indicador · Scrollspy · Header compacto ·
   Menú móvil · Barra CTA móvil · Reveal · Spotlight · Estado en vivo · Toast
   ========================================================================== */
(function () {
  'use strict';

  var html = document.documentElement;
  html.classList.add('js');
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  /* ---------- Toast ---------- */
  var toastEl = $('#toast');
  var toastTimer;
  function toast(msg) {
    if (!toastEl) return;
    $('.toast-msg', toastEl).textContent = msg;
    toastEl.classList.add('is-visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toastEl.classList.remove('is-visible'); }, 2400);
  }

  /* ---------- Tabs del menú con indicador deslizante ---------- */
  var tabList = $('.menu-tabs-header');
  var indicator = $('.menu-tab-indicator');
  var tabs = $$('.menu-tab-btn');

  function moveIndicator() {
    var active = $('.menu-tab-btn.is-active');
    if (!active || !indicator) return;
    indicator.style.setProperty('--w', active.offsetWidth + 'px');
    indicator.style.setProperty('--x', active.offsetLeft + 'px');
  }

  function setMenuMode(mode, focus) {
    tabs.forEach(function (t) {
      var on = t.dataset.mode === mode;
      t.classList.toggle('is-active', on);
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      if (on && focus) t.focus();
      var panel = document.getElementById(t.getAttribute('aria-controls'));
      if (panel) panel.hidden = !on;
    });
    if (tabList) tabList.dataset.active = mode;
    moveIndicator();
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () { setMenuMode(t.dataset.mode); });
    // Flechas izquierda/derecha (patrón ARIA tabs)
    t.addEventListener('keydown', function (e) {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      e.preventDefault();
      setMenuMode(t.dataset.mode === 'day' ? 'night' : 'day', true);
    });
  });
  window.addEventListener('resize', moveIndicator);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(moveIndicator);

  $$('[data-target-tab]').forEach(function (link) {
    link.addEventListener('click', function () { setMenuMode(link.dataset.targetTab); });
  });

  /* ---------- Tema día / noche ---------- */
  var themeToggle = $('#theme-toggle');
  var themeLabel = $('#toggle-label-text') || $('#toggle-label-text-value');
  var themeMeta = $('#theme-color-meta');

  function setTheme(next, syncMenu) {
    html.setAttribute('data-theme', next);
    if (themeToggle) themeToggle.setAttribute('aria-checked', String(next === 'night'));
    if (themeLabel) themeLabel.textContent = next === 'night' ? '🌙 NOCHE' : '☀️ DÍA';
    if (themeMeta) themeMeta.setAttribute('content', next === 'night' ? '#0D0E11' : '#16110E');
    if (syncMenu) setMenuMode(next);
    try { localStorage.setItem('cosme-theme', next); } catch (e) {}
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', function () {
      setTheme(html.getAttribute('data-theme') === 'day' ? 'night' : 'day', true);
    });
  }

  /* ---------- Estado en vivo + horarios (datos reales del local) ----------
     L–V abre 08:00 · Sáb/Dom 08:30 · cierre variable ("al cierre").
     Se asume cierre de madrugada (hasta las 02:00) para no prometer de más. */
  var now = new Date();
  var day = now.getDay();            // 0 dom … 6 sáb
  var mins = now.getHours() * 60 + now.getMinutes();
  var isWeekend = day === 0 || day === 6;
  var openMin = isWeekend ? 8 * 60 + 30 : 8 * 60;
  var openLabel = isWeekend ? '08:30' : '08:00';
  var CLOSE_GUESS = 2 * 60;          // 02:00
  var isOpen = mins >= openMin || mins < CLOSE_GUESS;

  var live = $('#live-status');
  if (live) {
    live.dataset.state = isOpen ? 'open' : 'closed';
    $('.live-text', live).textContent = isOpen
      ? (mins >= 19 * 60 || mins < CLOSE_GUESS ? 'Abierto ahora · Noche de birra' : 'Abierto ahora · Café y brunch')
      : 'Hoy abrimos a las ' + openLabel;
  }
  var todayRow = $(isWeekend ? '[data-hours="weekend"]' : '[data-hours="weekday"]');
  if (todayRow) todayRow.classList.add('is-today');

  // Estado inicial: tema guardado; si no, la carta sigue la hora del día.
  var saved = null;
  try { saved = localStorage.getItem('cosme-theme'); } catch (e) {}
  if (saved === 'day' || saved === 'night') {
    setTheme(saved, true);
  } else {
    setMenuMode(mins >= 8 * 60 && mins < 19 * 60 ? 'day' : 'night');
  }

  /* ---------- Header compacto + barra de progreso + CTA móvil ---------- */
  var header = $('.site-header');
  var progress = $('.scroll-progress');
  var ctaBar = $('.mobile-cta-bar');
  var hero = $('#hero');
  var ticking = false;

  function onScroll() {
    var y = window.scrollY;
    var max = document.documentElement.scrollHeight - window.innerHeight;
    if (header) header.classList.toggle('is-scrolled', y > 24);
    if (progress) progress.style.setProperty('--progress', max > 0 ? (y / max).toFixed(4) : 0);
    if (ctaBar && hero) ctaBar.classList.toggle('is-visible', y > hero.offsetHeight * 0.6);
    ticking = false;
  }
  window.addEventListener('scroll', function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Scrollspy ---------- */
  var navLinks = $$('.primary-nav a[data-spy]');
  if ('IntersectionObserver' in window && navLinks.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        navLinks.forEach(function (a) { a.classList.toggle('is-active', a.dataset.spy === en.target.id); });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    ['hero', 'el-lugar', 'menu', 'ubicacion'].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) spy.observe(el);
    });
  }

  /* ---------- Reveal on scroll (una vez) ---------- */
  var reveals = $$('.reveal');
  if ('IntersectionObserver' in window && !reduceMotion) {
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add('is-visible'); ro.unobserve(en.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    reveals.forEach(function (el) { ro.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
  }

  /* ---------- Spotlight en bento (solo puntero fino) ---------- */
  if (window.matchMedia('(hover: hover) and (pointer: fine)').matches) {
    $$('.bento-card-space').forEach(function (card) {
      card.addEventListener('pointermove', function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty('--mx', (e.clientX - r.left) + 'px');
        card.style.setProperty('--my', (e.clientY - r.top) + 'px');
      });
    });
  }

  /* ---------- Menú móvil ---------- */
  var menuBtn = $('#mobile-menu-toggle');
  var sheet = $('#mobile-sheet');
  function setSheet(open) {
    if (!sheet || !menuBtn) return;
    sheet.classList.toggle('is-open', open);
    sheet.setAttribute('aria-hidden', String(!open));
    menuBtn.setAttribute('aria-expanded', String(open));
    menuBtn.setAttribute('aria-label', open ? 'Cerrar menú' : 'Abrir menú');
    document.body.classList.toggle('is-locked', open);
    if (open) { var first = $('a', sheet); if (first) first.focus(); }
  }
  if (menuBtn) menuBtn.addEventListener('click', function () { setSheet(!sheet.classList.contains('is-open')); });
  $$('#mobile-sheet a').forEach(function (a) { a.addEventListener('click', function () { setSheet(false); }); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && sheet && sheet.classList.contains('is-open')) { setSheet(false); menuBtn.focus(); }
  });

  /* ---------- Copiar dirección ---------- */
  $$('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.dataset.copy;
      var done = function () { toast('Dirección copiada'); };
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(done, function () { toast(text); });
      } else {
        toast(text);
      }
    });
  });

  /* ---------- Año del footer ---------- */
  var yearEl = $('#year');
  if (yearEl) yearEl.textContent = String((new Date()).getFullYear());

  /* ---------- Visor Interactivo de PDFs (Google Drive Oficial) ---------- */
  var PDF_REGISTRY = {
    noche: {
      title: 'Carta General, Noche & Salón',
      badge: 'CARTA SALÓN 2026',
      icon: '🍺',
      preview: 'https://drive.google.com/file/d/1r6Pmaf6tBvK8j-wzST7jegs-poxu5HXt/preview',
      drive: 'https://drive.google.com/file/d/1r6Pmaf6tBvK8j-wzST7jegs-poxu5HXt/view?usp=sharing'
    },
    dia: {
      title: 'Desayunos, Cafetería & Meriendas',
      badge: 'DESAYUNOS & MERIENDAS',
      icon: '☕',
      preview: 'https://drive.google.com/file/d/1X0_n1wfn8lNFb6mAV4BZjV-Zevl-YU_N/preview',
      drive: 'https://drive.google.com/file/d/1X0_n1wfn8lNFb6mAV4BZjV-Zevl-YU_N/view?usp=sharing'
    }
  };

  var pdfModal = $('#pdf-modal');
  var pdfIframe = $('#pdf-modal-iframe');
  var pdfTitle = $('#pdf-modal-title');
  var pdfBadge = $('#pdf-modal-badge');
  var pdfIcon = $('#pdf-modal-icon');
  var pdfDriveLink = $('#pdf-modal-drive-link');
  var pdfDownloadLink = $('#pdf-modal-download-link');
  var pdfCloseBtn = $('#pdf-modal-close');

  function openPdfModal(key) {
    var doc = PDF_REGISTRY[key] || PDF_REGISTRY.noche;
    if (!pdfModal || !pdfIframe) return;

    if (pdfTitle) pdfTitle.textContent = doc.title;
    if (pdfBadge) pdfBadge.textContent = doc.badge;
    if (pdfIcon) pdfIcon.textContent = doc.icon;
    if (pdfDriveLink) pdfDriveLink.href = doc.drive;
    if (pdfDownloadLink) pdfDownloadLink.href = doc.drive;

    // Cargar URL de preview en iframe
    pdfIframe.src = doc.preview;

    pdfModal.classList.add('is-open');
    pdfModal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('is-locked');
    if (pdfCloseBtn) pdfCloseBtn.focus();
  }

  function closePdfModal() {
    if (!pdfModal) return;
    pdfModal.classList.remove('is-open');
    pdfModal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('is-locked');
    if (pdfIframe) pdfIframe.src = '';
  }

  $$('[data-open-pdf]').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      openPdfModal(btn.dataset.openPdf);
    });
  });

  if (pdfCloseBtn) pdfCloseBtn.addEventListener('click', closePdfModal);
  if (pdfModal) {
    pdfModal.addEventListener('click', function (e) {
      if (e.target === pdfModal) closePdfModal();
    });
  }

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && pdfModal && pdfModal.classList.contains('is-open')) {
      closePdfModal();
    }
  });

  var openCartasBtn = $('#open-cartas-btn');
  if (openCartasBtn) {
    openCartasBtn.addEventListener('click', function (e) {
      var target = $('#accesos-rapidos');
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  }
})();
