/* ==========================================================================
   MODULE: VHS CAMCORDER OSD & COTIZADOR FESTEJOS
   ========================================================================== */

export function initVhsAndQuote() {
  // 1. VHS Camcorder OSD
  const vhsImg = document.getElementById('vhs-preview-img');
  const vhsStatus = document.getElementById('vhs-osd-status');
  const vhsDate = document.getElementById('vhs-osd-date');
  const vhsTimecode = document.getElementById('vhs-osd-tc');
  const vhsPauseBtn = document.getElementById('vhs-pause-btn');
  const vhsTapeButtons = document.querySelectorAll('[data-vhs-tape]');

  const VHS_TAPES = {
    dj: {
      src: 'assets/dj-pioneer-vhs.jpg',
      alt: 'DJ tocando en vivo con consola Pioneer CDJ durante la Fiesta Retro de Cosme Alberdi',
      date: 'AUG 28 2026',
      status: 'PLAY \u25B6 · SP',
    },
    pista: {
      src: 'assets/noche-fiesta-caja.jpg',
      alt: 'Salón repleto de fiesta nocturna con carteles CAJA y COSME en neón rojo',
      date: 'ALBERDI LIVE',
      status: 'CLUB \u25B6 · SLP',
    },
  };

  vhsTapeButtons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const key = btn.getAttribute('data-vhs-tape');
      const tape = VHS_TAPES[key];
      if (!tape || !vhsImg) return;

      vhsImg.src = tape.src;
      vhsImg.alt = tape.alt;
      if (vhsDate) vhsDate.textContent = tape.date;
      if (vhsStatus) vhsStatus.textContent = tape.status;

      vhsTapeButtons.forEach((b) =>
        b.setAttribute('aria-pressed', String(b === btn))
      );
    });
  });

  let vhsSeconds = 5049;
  let vhsPaused = false;

  function formatTimecode(totalSec) {
    const h = String(Math.floor(totalSec / 3600) % 24).padStart(2, '0');
    const m = String(Math.floor((totalSec % 3600) / 60)).padStart(2, '0');
    const s = String(totalSec % 60).padStart(2, '0');
    return `${h}:${m}:${s}`;
  }

  if (vhsTimecode) {
    setInterval(() => {
      if (!vhsPaused) {
        vhsSeconds += 1;
        vhsTimecode.textContent = formatTimecode(vhsSeconds);
      }
    }, 1000);
  }

  if (vhsPauseBtn) {
    vhsPauseBtn.addEventListener('click', () => {
      vhsPaused = !vhsPaused;
      vhsPauseBtn.setAttribute('aria-pressed', String(vhsPaused));
      vhsPauseBtn.textContent = vhsPaused ? 'REANUDAR OSD' : 'PAUSAR OSD';
      if (vhsStatus) {
        vhsStatus.textContent = vhsPaused ? 'PAUSE \u23F8 · SP' : 'PLAY \u25B6 · SP';
      }
    });
  }

  // 2. Cotizador de Cumpleaños & Festejos
  const promoOptions = document.querySelectorAll('.promo-option');
  const guestPills = document.querySelectorAll('.guest-pill');
  const quoteSummaryLabel = document.getElementById('quote-summary-label');
  const quoteTotalPrice = document.getElementById('quote-total-price');
  const cumpleWaCta = document.getElementById('cumple-wa-cta');

  let selectedPromo = {
    id: '2',
    price: 21000,
    label: 'Promo 2 Full (Papas + Pizzas + Sándwiches de Carne + DJ y Cotillón LED)',
  };
  let selectedGuests = 12;

  function formatARS(num) {
    return '$' + num.toLocaleString('es-AR');
  }

  function updateQuote() {
    const total = selectedPromo.price * selectedGuests;
    const guestText = selectedGuests === 30 ? '30+ personas' : `${selectedGuests} personas`;

    if (quoteSummaryLabel) {
      quoteSummaryLabel.textContent = `${guestText} · Promo ${selectedPromo.id}`;
    }
    if (quoteTotalPrice) {
      quoteTotalPrice.textContent = formatARS(total);
    }
    if (cumpleWaCta) {
      const msg = `Hola Cosme Alberdi! Quiero cotizar mi cumpleaños para ${guestText} con la ${selectedPromo.label} (${formatARS(selectedPromo.price)} c/u — estimado total ${formatARS(total)}).`;
      cumpleWaCta.href = `https://wa.me/5493416802275?text=${encodeURIComponent(msg)}`;
    }
  }

  promoOptions.forEach((opt) => {
    opt.addEventListener('click', () => {
      selectedPromo = {
        id: opt.getAttribute('data-promo-id') || '2',
        price: Number(opt.getAttribute('data-promo-price')) || 21000,
        label: opt.getAttribute('data-promo-label') || 'Promo Cosme',
      };
      promoOptions.forEach((o) => o.classList.toggle('is-selected', o === opt));
      updateQuote();
    });
  });

  guestPills.forEach((pill) => {
    pill.addEventListener('click', () => {
      selectedGuests = Number(pill.getAttribute('data-guests')) || 12;
      guestPills.forEach((p) => p.classList.toggle('is-selected', p === pill));
      updateQuote();
    });
  });

  updateQuote();
}
