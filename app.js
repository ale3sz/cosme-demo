/**
 * COSME ALBERDI — APP.JS (V2.5 LIVING EXPERIENCE)
 * Atmósfera viva en tiempo real:
 * - Detector automático de franja horaria (Pub/Cervecería de noche × Cafetería/Almuerzo de día)
 * - Pizarra interactiva de 12 Canillas Artesanales
 * - Sugeridor interactivo de Almuerzo Ejecutivo
 * - Efectos de scroll (Scroll-Reveal & Parallax sutil)
 * - Pulsaciones de neón y presets de WhatsApp
 */

document.addEventListener('DOMContentLoaded', () => {
  const WHATSAPP_PHONE = '5493416802275'; // Número oficial de Cosme Alberdi

  // =========================================================================
  // 1. MOTOR HORARIO EN VIVO (ROSARIO, ARGENTINA UTC-3)
  // =========================================================================
  const liveStatusText = document.getElementById('live-status-text');
  const liveStatusHero = document.getElementById('live-status-text-hero');

  function getRosarioTime() {
    // Rosario está en UTC-3 (maneja correctamente el cambio de día al restar 3 horas)
    const now = new Date();
    const rosarioMs = now.getTime() - 3 * 60 * 60 * 1000;
    const r = new Date(rosarioMs);
    return { hour: r.getUTCHours(), minute: r.getUTCMinutes(), day: r.getUTCDay() };
  }

  // Horarios oficiales de Google Maps (0: Dom, 1: Lun, ..., 6: Sáb)
  // closeAfterMidnight indica la hora de cierre de la madrugada siguiente (en decimal)
  const SCHEDULE = {
    0: { open: 8.5, openStr: '08:30 hs', closeAfterMidnight: 1.0 },  // Domingo: 08:30 – 01:00
    1: { open: 8.0, openStr: '08:00 hs', closeAfterMidnight: 1.0 },  // Lunes: 08:00 – 01:00
    2: { open: 8.0, openStr: '08:00 hs', closeAfterMidnight: 1.0 },  // Martes: 08:00 – 01:00
    3: { open: 8.0, openStr: '08:00 hs', closeAfterMidnight: 1.0 },  // Miércoles: 08:00 – 01:00
    4: { open: 8.0, openStr: '08:00 hs', closeAfterMidnight: 2.0 },  // Jueves: 08:00 – 02:00
    5: { open: 8.0, openStr: '08:00 hs', closeAfterMidnight: 2.5 },  // Viernes: 08:00 – 02:30
    6: { open: 8.5, openStr: '08:30 hs', closeAfterMidnight: 2.5 },  // Sábado: 08:30 – 02:30
  };

  function updateLiveScheduleStatus() {
    const { hour, minute, day } = getRosarioTime();
    const currentDecimal = hour + (minute / 60);
    const todaySched = SCHEDULE[day];
    const prevDaySched = SCHEDULE[(day + 6) % 7];

    let statusMsg = '';
    let isDaytime = false;
    let isOpen = false;

    // Abierto si ya pasó la apertura de hoy, O si estamos en la madrugada antes del cierre de ayer
    if (currentDecimal >= todaySched.open || currentDecimal < prevDaySched.closeAfterMidnight) {
      isOpen = true;
      if (hour >= 8 && hour < 12) {
        statusMsg = `Abierto ahora · Cafetería de Especialidad & Desayunos`;
        isDaytime = true;
      } else if (hour >= 12 && hour < 16) {
        statusMsg = `Abierto ahora · Almuerzos & Cocina de Bodegón`;
        isDaytime = true;
      } else if (hour >= 16 && hour < 19) {
        statusMsg = `Abierto ahora · Merienda & Cafetería`;
        isDaytime = true;
      } else {
        statusMsg = `Abierto ahora · Modo Pub, Cervecería & Cocina`;
        isDaytime = false;
      }
    } else {
      isOpen = false;
      statusMsg = `Cerrado por descanso · Abre hoy a las ${todaySched.openStr}`;
      isDaytime = false;
    }

    if (liveStatusText) liveStatusText.textContent = statusMsg;
    if (liveStatusHero) liveStatusHero.textContent = statusMsg;

    // Actualizar indicador visual de pulso
    const pulseDots = document.querySelectorAll('.pulse-dot');
    pulseDots.forEach(dot => {
      dot.style.background = isOpen ? '#25d366' : '#ff1e27';
      dot.style.boxShadow = isOpen ? '0 0 10px rgba(37, 211, 102, 0.65)' : '0 0 10px rgba(255, 30, 39, 0.65)';
    });

    return isDaytime;
  }

  const isCurrentTimeDay = updateLiveScheduleStatus();
  setInterval(updateLiveScheduleStatus, 30000);

  // =========================================================================
  // GESTOR DE TRANSMUTACIÓN DE LOGO (.COSME. Tinta ⇄ Neón)
  // RENDERIZADOR MAESTRO 60 FPS ULTRA-FLUIDO POR SPRITE SHEET (28 FRAMES)
  // 1 Sola imagen en memoria GPU = 0 descargas extra, 0 pérdida de frames
  // =========================================================================
  const SPRITE_URL = 'assets/logo_morph/morph_spritesheet.webp?v=3';
  const TOTAL_FRAMES = 28;
  const LAST = TOTAL_FRAMES - 1;
  const FRAME_W = 800;
  const FRAME_H = 240;
  const COLS = 4;
  const FRAME_MS = 16; // 60 FPS exacto -> encendido ≈ 0.43s, apagado ≈ 0.24s

  const heroLogoCanvas = document.getElementById('hero-logo-canvas');
  const heroLogoDisplay = document.getElementById('hero-logo-display');
  const heroLogoBox = document.getElementById('hero-logo-box');
  const ctx = heroLogoCanvas ? heroLogoCanvas.getContext('2d', { alpha: true }) : null;

  let spriteSheet = null;
  let isSpriteReady = false;
  let morphRaf = null;

  // Carga inmediata del Sprite Sheet en memoria GPU
  const initSpriteSheet = () => {
    const img = new Image();
    img.src = SPRITE_URL;
    img.onload = async () => {
      if (window.createImageBitmap) {
        try {
          spriteSheet = await createImageBitmap(img);
        } catch (e) {
          spriteSheet = img;
        }
      } else {
        spriteSheet = img;
      }
      isSpriteReady = true;
      // Dibujar el estado inicial inmediatamente
      const current = htmlRoot.getAttribute('data-theme') || 'night';
      drawFrame(current === 'day' ? 0 : LAST);
    };
  };
  initSpriteSheet();

  function drawFrame(idx) {
    const frameIndex = Math.max(0, Math.min(LAST, idx));
    if (!ctx) return;

    if (isSpriteReady && spriteSheet) {
      const col = frameIndex % COLS;
      const row = Math.floor(frameIndex / COLS);
      const sx = col * FRAME_W;
      const sy = row * FRAME_H;
      ctx.clearRect(0, 0, FRAME_W, FRAME_H);
      ctx.drawImage(spriteSheet, sx, sy, FRAME_W, FRAME_H, 0, 0, FRAME_W, FRAME_H);
    } else {
      // Fallback antes de que termine de decodificar el sprite sheet
      const fallback = new Image();
      fallback.src = `assets/logo_morph/seq/f${String(frameIndex).padStart(2, '0')}.webp`;
      fallback.onload = () => {
        ctx.clearRect(0, 0, FRAME_W, FRAME_H);
        ctx.drawImage(fallback, 0, 0, FRAME_W, FRAME_H);
      };
    }
  }

  function playFrames(seq, onEnd) {
    cancelAnimationFrame(morphRaf);
    const t0 = performance.now();
    let shown = -1;
    const tick = (now) => {
      const stepIdx = Math.min(seq.length - 1, Math.floor((now - t0) / FRAME_MS));
      if (stepIdx !== shown) {
        drawFrame(seq[stepIdx]);
        shown = stepIdx;
      }
      if (stepIdx < seq.length - 1) {
        morphRaf = requestAnimationFrame(tick);
      } else {
        morphRaf = null;
        if (onEnd) onEnd();
      }
    };
    morphRaf = requestAnimationFrame(tick);
  }

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function morphLogo(targetMode, animate = true) {
    const targetIdx = targetMode === 'day' ? 0 : LAST;
    const el = heroLogoCanvas || heroLogoDisplay;
    if (el) el.classList.remove('neon-breathing');

    if (!animate || reduceMotion) {
      cancelAnimationFrame(morphRaf);
      drawFrame(targetIdx);
      if (el) el.classList.toggle('neon-breathing', targetMode !== 'day');
      return;
    }

    if (targetMode === 'night') {
      // 0 -> 27: Sello -> Vidrio -> Precalor -> Neón contorno con borgoña (User stage) -> Sobretensión -> Ignición -> Arco eléctrico -> Neón Bar
      const seqNight = Array.from({ length: 28 }, (_, i) => i);
      playFrames(seqNight, () => {
        if (el) el.classList.add('neon-breathing');
      });
    } else {
      // 27 -> 0: Enfriamiento rápido y nítido (15 cuadros seleccionados)
      const seqDay = [27, 25, 23, 21, 19, 17, 15, 13, 11, 9, 7, 5, 3, 1, 0];
      playFrames(seqDay);
    }
  }
  // =========================================================================
  // 2. GESTOR DE TEMA DUAL (DÍA / NOCHE) CON SENSOR INTELIGENTE
  // =========================================================================
  const htmlRoot = document.documentElement;
  const themeToggleBtn = document.getElementById('theme-toggle-btn');
  const themeToggleText = document.getElementById('theme-toggle-text');
  const themeToggleIcon = document.getElementById('theme-toggle-icon');
  const metaThemeColor = document.getElementById('theme-color-meta');

  // Si el usuario guardó preferencia la respetamos, sino aplicamos según horario real
  const userSavedTheme = localStorage.getItem('cosme_theme');
  const initialTheme = userSavedTheme || 'night';

  function setTheme(theme, updateMenu) {
    htmlRoot.setAttribute('data-theme', theme);
    localStorage.setItem('cosme_theme', theme);

    if (theme === 'day') {
      if (themeToggleBtn) themeToggleBtn.setAttribute('aria-checked', 'true');
      if (metaThemeColor) metaThemeColor.setAttribute('content', '#F7F4EE');
      if (updateMenu) setMenuMode('day');
    } else {
      if (themeToggleBtn) themeToggleBtn.setAttribute('aria-checked', 'false');
      if (metaThemeColor) metaThemeColor.setAttribute('content', '#0C0D10');
      if (updateMenu) setMenuMode('night');
    }
    morphLogo(theme, updateMenu);
  }

  setTheme(initialTheme, false);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const current = htmlRoot.getAttribute('data-theme') || 'night';
      const next = current === 'night' ? 'day' : 'night';
      setTheme(next, true);
    });
  }

  // =========================================================================
  // 3. TABS Y FILTRADO DEL MENÚ UNIFICADO (DÍA / NOCHE / CANILLAS)
  // =========================================================================
  const menuTabs = document.querySelectorAll('.menu-mode-tab');
  const dishesNight = document.querySelectorAll('.dish-night');
  const dishesDay = document.querySelectorAll('.dish-day');
  const lunchSuggester = document.getElementById('lunch-suggester-box');
  const tapsBoard = document.getElementById('canillas');
  const menuGrid = document.querySelector('.menu-grid');
  const menuFooterBar = document.querySelector('.menu-footer-bar');

  menuTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.getAttribute('data-menu-target');
      setMenuMode(target);
    });
  });

  function setMenuMode(mode) {
    menuTabs.forEach(t => {
      if (t.getAttribute('data-menu-target') === mode) {
        t.classList.add('active');
      } else {
        t.classList.remove('active');
      }
    });

    const menuQuickFilters = document.getElementById('menu-quick-filters');
    const filterPills = document.querySelectorAll('.filter-pill');
    filterPills.forEach((p, idx) => {
      if (idx === 0) p.classList.add('active');
      else p.classList.remove('active');
    });

    if (mode === 'taps') {
      if (menuQuickFilters) menuQuickFilters.style.display = 'none';
      if (tapsBoard) tapsBoard.style.display = 'block';
      if (menuGrid) menuGrid.style.display = 'none';
      if (lunchSuggester) lunchSuggester.style.display = 'none';
      if (menuFooterBar) menuFooterBar.style.display = 'none';
      const diurnalBanner = document.getElementById('diurnal-header-banner');
      if (diurnalBanner) diurnalBanner.style.display = 'none';
    } else if (mode === 'day') {
      if (menuQuickFilters) menuQuickFilters.style.display = 'flex';
      if (tapsBoard) tapsBoard.style.display = 'none';
      if (menuGrid) menuGrid.style.display = 'grid';
      if (menuFooterBar) menuFooterBar.style.display = 'flex';
      dishesNight.forEach(el => el.style.display = 'none');
      dishesDay.forEach(el => el.style.display = 'flex');
      if (lunchSuggester) lunchSuggester.style.display = 'block';
      const diurnalBanner = document.getElementById('diurnal-header-banner');
      if (diurnalBanner) diurnalBanner.style.display = 'flex';
    } else {
      // mode === 'night'
      if (menuQuickFilters) menuQuickFilters.style.display = 'flex';
      if (tapsBoard) tapsBoard.style.display = 'none';
      if (menuGrid) menuGrid.style.display = 'grid';
      if (menuFooterBar) menuFooterBar.style.display = 'flex';
      dishesNight.forEach(el => el.style.display = 'flex');
      dishesDay.forEach(el => el.style.display = 'none');
      if (lunchSuggester) lunchSuggester.style.display = 'none';
      const diurnalBanner = document.getElementById('diurnal-header-banner');
      if (diurnalBanner) diurnalBanner.style.display = 'none';
    }
  }

  // Soporte directo para hash #canillas
  function checkHashTab() {
    if (window.location.hash === '#canillas') {
      setMenuMode('taps');
    }
  }
  window.addEventListener('hashchange', checkHashTab);
  checkHashTab();

  // Manejo de saltos directos desde las tarjetitas superiores
  document.querySelectorAll('[data-jump-menu]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      const targetMode = trigger.getAttribute('data-jump-menu');
      setMenuMode(targetMode);
    });
  });

  // Highlight suave en Ubicación si se hace click en su tarjetita
  const cardUbicacion = document.getElementById('card-nav-ubicacion');
  if (cardUbicacion) {
    cardUbicacion.addEventListener('click', () => {
      const ubicacionSection = document.getElementById('ubicacion');
      if (ubicacionSection) {
        ubicacionSection.classList.add('ubicacion-highlight');
        setTimeout(() => {
          ubicacionSection.classList.remove('ubicacion-highlight');
        }, 2200);
      }
    });
  }


  // Inicializar menú con el tema actual
  setMenuMode(initialTheme);

  // =========================================================================
  // 4. PIZARRA INTERACTIVA DE CANILLAS DE CERVEZA (TAPROOM + FILTROS PALADAR)
  // =========================================================================
  const tapPalateChips = document.querySelectorAll('.tap-filter-chip');
  const tapRows = document.querySelectorAll('.tap-row');

  if (tapPalateChips.length > 0) {
    tapPalateChips.forEach(chip => {
      chip.addEventListener('click', () => {
        tapPalateChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        const palate = chip.getAttribute('data-palate');

        tapRows.forEach(row => {
          const itemPalate = row.getAttribute('data-palate-item');
          row.style.display = (palate === 'all' || itemPalate === palate) ? '' : 'none';
        });
      });
    });
  }

  tapRows.forEach(row => {
    row.addEventListener('click', (e) => {
      const beerName = row.getAttribute('data-beer-name') || 'Cerveza Tirada';
      const beerStyle = row.getAttribute('data-beer-style') || 'Artesanal';

      tapRows.forEach(r => r.classList.remove('tap-selected'));
      row.classList.add('tap-selected');

      if (e.target.closest('.tap-row-btn') || e.target.closest('[data-order-beer]')) {
        e.stopPropagation();
        const orderMsg = `¡Hola Cosme Alberdi! 🍻 Quiero pedir una pinta de *${beerName}* (${beerStyle}) o consultar disponibilidad para recargar growler. ¿Tienen disponible hoy?`;
        window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(orderMsg)}`, '_blank');
      }
    });
  });

  // =========================================================================
  // 5. SUGERIDOR DE ALMUERZO EJECUTIVO (MEDIODÍA)
  // =========================================================================
  const lunchDishSelect = document.getElementById('lunch-dish-select');
  const lunchDrinkSelect = document.getElementById('lunch-drink-select');
  const lunchDessertSelect = document.getElementById('lunch-dessert-select');
  const lunchCtaBtn = document.getElementById('lunch-cta-btn');

  function getLunchSelections() {
    const dish = lunchDishSelect ? lunchDishSelect.value : 'Plato del Día';
    const drink = lunchDrinkSelect ? lunchDrinkSelect.value : 'Bebida sin alcohol';
    const dessert = lunchDessertSelect ? lunchDessertSelect.value : 'Café Espresso Barista';
    return { dish, drink, dessert };
  }

  if (lunchCtaBtn) {
    lunchCtaBtn.addEventListener('click', () => {
      const { dish, drink, dessert } = getLunchSelections();
      const msg = `¡Hola Cosme! â˜€ï¸ Quiero pedir / reservar para el Almuerzo Ejecutivo:\n- Principal: *${dish}*\n- Bebida: *${drink}*\n- Cierre: *${dessert}*\n¿A qué hora tienen mesa o para retirar?`;
      window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(msg)}`, '_blank');
    });
  }

  // =========================================================================
  // 6. GENERADOR DE ENLACES DE WHATSAPP CON MENSAJES PRECONFIGURADOS
  // =========================================================================
  window.openWhatsApp = function(presetType, customData = {}) {
    let message = '';

    switch (presetType) {
      case 'reservar_mesa':
        message = '¡Hola Cosme Alberdi! Quiero consultar disponibilidad para reservar una mesa. ¿Me indican horarios y opciones para hoy?';
        break;
      case 'cumpleanos':
        message = '¡Hola Cosme! Cumplo años y quiero consultar por promociones de grupo, sector exclusivo y el brindis de regalo.';
        break;
      case 'menu_ejecutivo':
        message = '¡Hola Cosme! ¿Me podrían pasar las opciones del Menú Ejecutivo del día de hoy con plato, bebida y postre?';
        break;
      case 'pasta_libre':
        message = '¡Hola Cosme! Quiero reservar para el Jueves de Pasta Libre. ¿Tienen mesa disponible para cenar?';
        break;
      case 'mesa_amigos':
        message = '¡Hola Cosme Alberdi! Quiero consultar disponibilidad para reservar una mesa. ¿Me indican horarios y opciones para hoy?';
        break;
      case 'take_away':
        message = '¡Hola Cosme! Quiero hacer un pedido para retirar por el local de Bv. Rondeau 1602. ¿Me pasan la carta para elegir?';
        break;
      case 'plato_especifico':
        const dish = customData.dishName || 'un plato de la carta';
        message = `¡Hola Cosme! Me tentó el plato *${dish}*. ¿Lo tienen disponible hoy en el salón?`;
        break;
      default:
        message = '¡Hola Cosme Alberdi! Quisiera hacerles una consulta.';
    }

    const waUrl = `https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(message)}`;
    window.open(waUrl, '_blank');
  };

  // Delegación de clicks para presets de WhatsApp
  document.querySelectorAll('[data-wa-preset]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const preset = btn.getAttribute('data-wa-preset');
      const dishName = btn.getAttribute('data-dish-name');
      window.openWhatsApp(preset, { dishName });
    });
  });

  // =========================================================================
  // 7. CALCULADOR INTERACTIVO DE FESTEJOS (REFACTOR CRO: TICKET ALTO)
  // =========================================================================
  const calcRange = document.getElementById('calc-guests-range');
  const calcCount = document.getElementById('calc-guests-count');
  const calcBenefit = document.getElementById('calc-benefit-text');
  const calcCta = document.getElementById('calc-wa-btn') || document.getElementById('calc-cta-btn');

  function getGroupPerks(val) {
    if (val < 10) {
      return {
        benefit: 'Propuesta para grupos chicos (hasta 9 personas)',
        details: '[Espacio para cargar beneficios, mesas unificadas o cortesías reales que el local ofrezca para este tamaño de grupo.]',
        package: 'Ej: Carta abierta, tablas para compartir o menú sugerido por el local'
      };
    } else if (val < 20) {
      return {
        benefit: 'Propuesta para grupos medianos (10 a 19 personas)',
        details: '[Espacio para detallar opciones reales de menú grupal, combos de comida/bebida o condiciones de reserva de sector.]',
        package: 'Ej: Menú fijo por persona o combo grupal definido por el local'
      };
    } else {
      return {
        benefit: 'Propuesta para grupos grandes (20 o más personas)',
        details: '[Espacio para detallar modalidad de eventos, reserva de sector exclusivo, seña o beneficios especiales vigentes.]',
        package: 'Ej: Propuesta de evento o festejo a medida definida por el local'
      };
    }
  }

  if (calcRange) {
    function updateCalculator(val) {
      if (calcCount) calcCount.textContent = `${val} personas`;
      const perks = getGroupPerks(parseInt(val, 10));

      if (calcBenefit) {
        calcBenefit.innerHTML = `<strong>${perks.benefit}</strong><br><span style="font-size:0.83rem; color:var(--text-muted); display:inline-block; margin-top:3px;">${perks.details}</span><br><span style="font-size:0.8rem; color:var(--neon-amber); font-weight:700;">★ Contexto sugerido: ${perks.package}</span>`;
      }
    }

    calcRange.addEventListener('input', (e) => {
      updateCalculator(e.target.value);
    });

    // Inicializar cálculo inicial
    updateCalculator(calcRange.value);

    if (calcCta) {
      calcCta.addEventListener('click', (e) => {
        e.preventDefault();
        const guests = calcRange.value;
        const msg = `¡Hola Cosme Alberdi! Queremos consultar para reservar en grupo:
• Cantidad estimada: *${guests} personas*

¿Nos cuentan qué opciones, disponibilidad de sector y condiciones manejan para esa cantidad? ¡Muchas gracias!`;
        window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(msg)}`, '_blank');
      });
    }
  }



  // =========================================================================
  // 9. ANIMACIONES EN SCROLL (SCROLL-REVEAL OBSERVER)
  // =========================================================================
  const revealElements = document.querySelectorAll('.scroll-reveal');
  if ('IntersectionObserver' in window && revealElements.length > 0) {
    const observer = new IntersectionObserver((entries, obs) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('revealed');
          obs.unobserve(entry.target);
        }
      });
    }, {
      root: null,
      threshold: 0.12,
      rootMargin: '0px 0px -40px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
  } else {
    // Fallback si no hay observer
    revealElements.forEach(el => el.classList.add('revealed'));
  }

  // =========================================================================
  // 10. GESTIÓN DE MODALES (RESERVA, CARTA PDF, KIT DE MARCA)
  // =========================================================================
  const modalReserva = document.getElementById('modal-reserva');
  const modalCarta = document.getElementById('modal-carta');
  
  function openModal(modal) {
    if (modal) {
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    }
  }

  function closeModal(modal) {
    if (modal) {
      modal.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

    // =========================================================================
  // 10B. GESTIÓN DEL VISOR DE CARTA DIGITAL IN-PAGE
  // =========================================================================
  const pdfFrame = document.getElementById('pdf-frame');
  const pdfBadge = document.getElementById('modal-pdf-badge');
  const pdfDownloadLink = document.getElementById('modal-pdf-download-link');
  const pdfSwitchTabs = document.querySelectorAll('.pdf-switch-tab');

  const PDF_DOC_DATA = {
    noche: {
      title: 'Carta Salón & Noche',
      badge: 'CARTA SALÓN & NOCHE',
      previewUrl: 'https://drive.google.com/file/d/1r6Pmaf6tBvK8j-wzST7jegs-poxu5HXt/preview',
      downloadUrl: 'assets/docs/carta-noche.pdf',
      downloadName: 'Carta_Cosme_Alberdi_Noche.pdf'
    },
    dia: {
      title: 'Desayunos & Meriendas',
      badge: 'DESAYUNOS & MERIENDAS',
      previewUrl: 'https://drive.google.com/file/d/1X0_n1wfn8lNFb6mAV4BZjV-Zevl-YU_N/preview',
      downloadUrl: 'assets/docs/carta-dia.pdf',
      downloadName: 'Carta_Cosme_Alberdi_Desayunos_Meriendas.pdf'
    }
  };

  function setPdfDoc(docKey) {
    const data = PDF_DOC_DATA[docKey] || PDF_DOC_DATA.noche;
    if (pdfFrame && pdfFrame.src !== data.previewUrl) {
      pdfFrame.src = data.previewUrl;
    }
    if (pdfBadge) pdfBadge.textContent = data.badge;
    if (pdfDownloadLink) {
      pdfDownloadLink.href = data.downloadUrl;
      pdfDownloadLink.setAttribute('download', data.downloadName);
    }
    pdfSwitchTabs.forEach(tab => {
      if (tab.getAttribute('data-pdf-doc') === docKey) {
        tab.classList.add('active');
      } else {
        tab.classList.remove('active');
      }
    });
  }

  // Clicks en pestañas del visor
  pdfSwitchTabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      const doc = tab.getAttribute('data-pdf-doc');
      setPdfDoc(doc);
    });
  });

  // Gatillos externos [data-open-pdf]
  document.querySelectorAll('[data-open-pdf]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const doc = trigger.getAttribute('data-open-pdf');
      setPdfDoc(doc);
      openModal(modalCarta);
    });
  });

  document.querySelectorAll('[data-open-modal]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const target = trigger.getAttribute('data-open-modal');
      if (target === 'reserva') openModal(modalReserva);
      if (target === 'carta') {
        const defaultDoc = (currentTheme === 'day') ? 'dia' : 'noche';
        setPdfDoc(defaultDoc);
        openModal(modalCarta);
      }
          });
  });

  document.querySelectorAll('.modal-close-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const modal = btn.closest('.modal-backdrop, .modal-container');
      closeModal(modal);
    });
  });

  document.querySelectorAll('.modal-backdrop').forEach(backdrop => {
    backdrop.addEventListener('click', (e) => {
      if (e.target === backdrop) {
        closeModal(backdrop);
      }
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal(modalReserva);
      closeModal(modalCarta);
          }
  });

  // Formulario rápido de Reserva dentro del modal
  const bookingForm = document.getElementById('form-modal-reserva') || document.getElementById('booking-quick-form');
  if (bookingForm) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const nombre = document.getElementById('res-nombre')?.value || 'Cliente';
      const personas = document.getElementById('res-personas')?.value || '2 personas';
      const fecha = document.getElementById('res-fecha')?.value || 'Hoy';
      const horario = document.getElementById('res-horario')?.value || document.getElementById('res-turno')?.value || '21:00 hs';

      const text = `¡Hola Cosme Alberdi! Quisiera hacer una reserva:
- Nombre: ${nombre}
- Personas: ${personas}
- Fecha: ${fecha}
- Horario deseado: ${horario}

¿Tienen disponibilidad? ¡Muchas gracias!`;

      closeModal(modalReserva);
      window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(text)}`, '_blank');
    });
  }

  // =========================================================================
  // 11. WIDGET FLOTANTE DE WHATSAPP (FIX SELECTOR CRO)
  // =========================================================================
  const floatingToggle = document.getElementById('floating-wa-btn') || document.getElementById('floating-wa-toggle');
  const floatingMenu = document.getElementById('floating-wa-menu');

  if (floatingToggle && floatingMenu) {
    floatingToggle.addEventListener('click', (e) => {
      e.stopPropagation();
      floatingMenu.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
      if (!floatingToggle.contains(e.target) && !floatingMenu.contains(e.target)) {
        floatingMenu.classList.remove('active');
      }
    });
  }

  // =========================================================================
  // 12. FILTROS RÁPIDOS DE EXPLORACIÓN DE CARTA (CRO)
  // =========================================================================
  const filterPills = document.querySelectorAll('.filter-pill');
  if (filterPills.length > 0) {
    filterPills.forEach(pill => {
      pill.addEventListener('click', () => {
        filterPills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        const filterVal = pill.getAttribute('data-filter');

        const activeMode = document.querySelector('.menu-mode-tab.active')?.getAttribute('data-menu-target') || 'night';
        const targetDishes = (activeMode === 'day') 
          ? document.querySelectorAll('.dish-day') 
          : document.querySelectorAll('.dish-night');

        targetDishes.forEach(dish => {
          if (filterVal === 'all') {
            dish.style.display = 'flex';
          } else {
            const categories = dish.getAttribute('data-category') || '';
            if (categories.split(' ').includes(filterVal)) {
              dish.style.display = 'flex';
            } else {
              dish.style.display = 'none';
            }
          }
        });
      });
    });
  }

  if (heroLogoBox) {
    heroLogoBox.addEventListener('click', () => {
      const current = htmlRoot.getAttribute('data-theme') || 'night';
      if (current === 'night') {
        // Chispa táctil reactiva al tocar el logo de noche
        playFrames([24, 20, 22, 25, LAST]);
      }
    });
  }

  // =========================================================================
  // 13. BOTTOM SHEET DE NAVEGACIÓN MÓVIL (SECCIONES)
  // =========================================================================
  const mobileSheetBtn = document.getElementById('mobile-nav-sheet-btn');
  const mobileSheet = document.getElementById('mobile-nav-sheet');

  if (mobileSheetBtn && mobileSheet) {
    const closeSheet = () => {
      mobileSheet.classList.remove('is-open');
      mobileSheet.setAttribute('aria-hidden', 'true');
      mobileSheetBtn.setAttribute('aria-expanded', 'false');
    };

    const toggleSheet = () => {
      const isOpen = mobileSheet.classList.toggle('is-open');
      mobileSheet.setAttribute('aria-hidden', String(!isOpen));
      mobileSheetBtn.setAttribute('aria-expanded', String(isOpen));
    };

    mobileSheetBtn.addEventListener('click', toggleSheet);
    mobileSheet.querySelectorAll('[data-close-sheet]').forEach(el => {
      el.addEventListener('click', closeSheet);
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && mobileSheet.classList.contains('is-open')) {
        closeSheet();
      }
    });
  }

});