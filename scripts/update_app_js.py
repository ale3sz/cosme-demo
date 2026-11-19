import os

def update_files():
    # 1. Update app.js
    app_js_content = '''/**
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
    // Rosario está en UTC-3
    const now = new Date();
    const utcHours = now.getUTCHours();
    const utcMinutes = now.getUTCMinutes();
    let rosarioHour = (utcHours - 3 + 24) % 24;
    return { hour: rosarioHour, minute: utcMinutes };
  }

  function updateLiveScheduleStatus() {
    const { hour, minute } = getRosarioTime();
    const timeStr = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`;
    let statusMsg = '';
    let isDaytime = false;

    if (hour >= 8 && hour < 12) {
      statusMsg = `☀️ ${timeStr} h · Abierto · Cafetería de Especialidad & Desayunos`;
      isDaytime = true;
    } else if (hour >= 12 && hour < 16) {
      statusMsg = `☀️ ${timeStr} h · Abierto · Modo Almuerzo Ejecutivo & Menú del Día`;
      isDaytime = true;
    } else if (hour >= 16 && hour < 18) {
      statusMsg = `☕ ${timeStr} h · Abierto · Merienda Alberdi & Tostados`;
      isDaytime = true;
    } else if (hour >= 18 || hour < 3) {
      statusMsg = `🌙 ${timeStr} h · En vivo · Modo Pub & 12 Canillas de Cerveza Artesanal`;
      isDaytime = false;
    } else {
      statusMsg = `😴 ${timeStr} h · Cerrado por descanso · Abrimos a las 08:00 h con café fresco`;
      isDaytime = false;
    }

    if (liveStatusText) liveStatusText.textContent = statusMsg;
    if (liveStatusHero) liveStatusHero.textContent = statusMsg;

    return isDaytime;
  }

  const isCurrentTimeDay = updateLiveScheduleStatus();
  setInterval(updateLiveScheduleStatus, 30000);

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
  const initialTheme = userSavedTheme || (isCurrentTimeDay ? 'day' : 'night');
  setTheme(initialTheme, false);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const current = htmlRoot.getAttribute('data-theme') || 'night';
      const next = current === 'night' ? 'day' : 'night';
      setTheme(next, true);
    });
  }

  function setTheme(theme, updateMenu) {
    htmlRoot.setAttribute('data-theme', theme);
    localStorage.setItem('cosme_theme', theme);

    if (theme === 'day') {
      if (themeToggleText) themeToggleText.textContent = 'Día ☀️';
      if (themeToggleIcon) themeToggleIcon.textContent = '☀️';
      if (metaThemeColor) metaThemeColor.setAttribute('content', '#F5F0E6');
      if (updateMenu) setMenuMode('day');
    } else {
      if (themeToggleText) themeToggleText.textContent = 'Noche 🌙';
      if (themeToggleIcon) themeToggleIcon.textContent = '🌙';
      if (metaThemeColor) metaThemeColor.setAttribute('content', '#0C0D10');
      if (updateMenu) setMenuMode('night');
    }
  }

  // =========================================================================
  // 3. TABS Y FILTRADO DEL MENÚ (DÍA / NOCHE)
  // =========================================================================
  const menuTabs = document.querySelectorAll('.menu-mode-tab');
  const dishesNight = document.querySelectorAll('.dish-night');
  const dishesDay = document.querySelectorAll('.dish-day');
  const lunchSuggester = document.getElementById('lunch-suggester-box');

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

    if (mode === 'day') {
      dishesNight.forEach(el => el.style.display = 'none');
      dishesDay.forEach(el => el.style.display = 'flex');
      if (lunchSuggester) lunchSuggester.style.display = 'block';
    } else {
      dishesNight.forEach(el => el.style.display = 'flex');
      dishesDay.forEach(el => el.style.display = 'none');
      if (lunchSuggester) lunchSuggester.style.display = 'none';
    }
  }

  // Inicializar menú con el tema actual
  setMenuMode(initialTheme);

  // =========================================================================
  // 4. PIZARRA INTERACTIVA DE CANILLAS DE CERVEZA
  // =========================================================================
  const beerTaps = document.querySelectorAll('.beer-tap-card');
  beerTaps.forEach(tap => {
    tap.addEventListener('click', (e) => {
      // Si hizo click en el botón de whatsapp o en la tarjeta
      const beerName = tap.getAttribute('data-beer-name') || 'Cerveza Tirada';
      const beerStyle = tap.getAttribute('data-beer-style') || 'Artesanal';
      
      // Remover highlight previo y marcar activo
      beerTaps.forEach(b => b.classList.remove('tap-selected'));
      tap.classList.add('tap-selected');

      if (e.target.closest('.btn-tap-order')) {
        const msg = `¡Hola Cosme Alberdi! 🍻 Quiero consultar para tomar una pinta de *${beerName}* (${beerStyle}) o cargar mi growler. ¿Tienen disponible hoy?`;
        window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(msg)}`, '_blank');
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
      const msg = `¡Hola Cosme! ☀️ Quiero pedir / reservar para el Almuerzo Ejecutivo:\\n- Principal: *${dish}*\\n- Bebida: *${drink}*\\n- Cierre: *${dessert}*\\n¿A qué hora tienen mesa o para retirar?`;
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
        message = '¡Hola Cosme Alberdi! 📅 Quiero consultar disponibilidad para reservar una mesa. ¿Me indican horarios y opciones para hoy?';
        break;
      case 'cumpleanos':
        message = '¡Hola Cosme! 🎉 Cumplo años y quiero consultar por promociones de grupo, sector exclusivo y el brindis de regalo.';
        break;
      case 'menu_ejecutivo':
        message = '¡Hola Cosme! 🍽️ ¿Me podrían pasar las opciones del Menú Ejecutivo del día de hoy con plato, bebida y postre?';
        break;
      case 'pasta_libre':
        message = '¡Hola Cosme! 🍝 Quiero reservar para el Jueves de Pasta Libre. ¿Tienen mesa disponible para cenar?';
        break;
      case 'mesa_amigos':
        message = '¡Hola Cosme Alberdi! 🍻 Somos un grupo de amigos y queremos coordinar una mesa grande para tomar cerveza tirada y picar.';
        break;
      case 'take_away':
        message = '¡Hola Cosme! 🛵 Quiero hacer un pedido para retirar por el local de Bv. Rondeau 1602. ¿Me pasan la carta para elegir?';
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
  // 7. CALCULADOR INTERACTIVO DE FESTEJOS
  // =========================================================================
  const calcRange = document.getElementById('calc-guests-range');
  const calcCount = document.getElementById('calc-guests-count');
  const calcPerk1 = document.getElementById('calc-perk-1');
  const calcPerk2 = document.getElementById('calc-perk-2');
  const calcPerk3 = document.getElementById('calc-perk-3');
  const calcCta = document.getElementById('calc-cta-btn');

  if (calcRange) {
    function updateCalculator(val) {
      if (calcCount) calcCount.textContent = `${val} personas`;

      if (val < 15) {
        if (calcPerk1) calcPerk1.innerHTML = '🥂 <strong>1 Botella de espumante</strong> de cortesía para el brindis.';
        if (calcPerk2) calcPerk2.innerHTML = '🪑 <strong>Mesa unificada</strong> en sector salón o vereda templada.';
        if (calcPerk3) calcPerk3.innerHTML = '🎂 Podés traer tu torta (servicio de vajilla sin costo).';
      } else if (val < 25) {
        if (calcPerk1) calcPerk1.innerHTML = '🥂 <strong>2 Botellas de espumante</strong> de cortesía para el brindis.';
        if (calcPerk2) calcPerk2.innerHTML = '🎯 <strong>Sector semi-exclusivo</strong> reservado especialmente.';
        if (calcPerk3) calcPerk3.innerHTML = '🍻 <strong>Ronda de pintas de bienvenida</strong> a precio promocional.';
      } else {
        if (calcPerk1) calcPerk1.innerHTML = '🥂 <strong>3 Botellas de espumante</strong> de regalo para celebrar a lo grande.';
        if (calcPerk2) calcPerk2.innerHTML = '👑 <strong>Espacio exclusivo</strong> con atención de camarero dedicada.';
        if (calcPerk3) calcPerk3.innerHTML = '🎧 Opción de solicitar temas a la cabina de DJ en vivo.';
      }
    }

    calcRange.addEventListener('input', (e) => {
      updateCalculator(e.target.value);
    });

    if (calcCta) {
      calcCta.addEventListener('click', () => {
        const guests = calcRange.value;
        const msg = `¡Hola Cosme! 🎉 Somos unas *${guests} personas* y queremos festejar en el bar. ¿Me confirman disponibilidad y promos para grupos?`;
        window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(msg)}`, '_blank');
      });
    }
  }

  // =========================================================================
  // 8. EFECTO DE RESPLANDOR Y ENCENDIDO DEL NEÓN AL CLICK
  // =========================================================================
  const heroNeonSign = document.querySelector('.hero-logo-night');
  if (heroNeonSign) {
    heroNeonSign.addEventListener('click', () => {
      heroNeonSign.classList.remove('neon-ignite-active');
      void heroNeonSign.offsetWidth; // Forzar reflow
      heroNeonSign.classList.add('neon-ignite-active');
    });
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
  const modalBrand = document.getElementById('modal-brand');

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

  document.querySelectorAll('[data-open-modal]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const target = trigger.getAttribute('data-open-modal');
      if (target === 'reserva') openModal(modalReserva);
      if (target === 'carta') openModal(modalCarta);
      if (target === 'brand') openModal(modalBrand);
    });
  });

  document.querySelectorAll('.modal-backdrop, .modal-close-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const modal = e.target.closest('.modal-container');
      closeModal(modal);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      closeModal(modalReserva);
      closeModal(modalCarta);
      closeModal(modalBrand);
    }
  });

  // Formulario rápido de Reserva dentro del modal
  const bookingForm = document.getElementById('booking-quick-form');
  if (bookingForm) {
    bookingForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const date = document.getElementById('book-date')?.value || 'Hoy';
      const time = document.getElementById('book-time')?.value || '21:30';
      const guests = document.getElementById('book-guests')?.value || '2';
      const sector = document.getElementById('book-sector')?.value || 'Salón';
      const notes = document.getElementById('book-notes')?.value || '';

      let text = `¡Hola Cosme Alberdi! 📅 Quiero confirmar una reserva:\\n- Fecha: *${date}*\\n- Horario: *${time} h*\\n- Personas: *${guests}*\\n- Preferencia: *${sector}*`;
      if (notes) text += `\\n- Aclaración: ${notes}`;

      closeModal(modalReserva);
      window.open(`https://wa.me/${WHATSAPP_PHONE}?text=${encodeURIComponent(text)}`, '_blank');
    });
  }

  // =========================================================================
  // 11. WIDGET FLOTANTE DE WHATSAPP
  // =========================================================================
  const floatingToggle = document.getElementById('floating-wa-toggle');
  const floatingMenu = document.getElementById('floating-wa-menu');

  if (floatingToggle && floatingMenu) {
    floatingToggle.addEventListener('click', () => {
      floatingMenu.classList.toggle('active');
    });

    document.addEventListener('click', (e) => {
      if (!floatingToggle.contains(e.target) && !floatingMenu.contains(e.target)) {
        floatingMenu.classList.remove('active');
      }
    });
  }
});
'''
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js_content)
    print("Updated app.js successfully!")

if __name__ == '__main__':
    update_files()
