import re
from lucide_icons import get_icon

def update_all():
    # =========================================================================
    # 1. UPDATE STYLES.CSS
    # =========================================================================
    with open('styles.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Add Oswald to font imports if needed
    font_import = """@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Oswald:wght@500;600;700&display=swap');\n"""
    if 'Bebas+Neue' not in css:
        css = font_import + css

    # Update font variables
    css = css.replace("--font-heading: 'Anton', sans-serif;", "--font-heading: 'Oswald', 'Bebas Neue', 'Anton', sans-serif;")

    # Replace old .theme-toggle-btn with modern minimal switch
    old_switch_css = """/* Toggle Día / Noche (Flat & Minimalista) */
.theme-toggle-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid var(--border-color);
  color: var(--text-main);
  font-size: 0.8rem;
  font-weight: 700;
  transition: all 0.2s ease;
}
.theme-toggle-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.25);
}"""

    new_switch_css = """/* Toggle Día / Noche Minimalista (Switch Shadcn UI / iOS Pure Icon) */
.theme-switch {
  position: relative;
  width: 52px;
  height: 28px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.18);
  padding: 2px;
  cursor: pointer;
  transition: all 0.28s cubic-bezier(0.16, 1, 0.3, 1);
  display: inline-flex;
  align-items: center;
  outline: none;
}

.theme-switch:hover {
  background: rgba(255, 255, 255, 0.18);
  border-color: rgba(255, 255, 255, 0.3);
}

.switch-thumb {
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: #181920;
  border: 1px solid rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffaa00;
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), background 0.25s ease, color 0.25s ease, border-color 0.25s ease;
  transform: translateX(0);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
}

.switch-thumb .icon-sun { display: none; }
.switch-thumb .icon-moon { display: block; }

html[data-theme="day"] .theme-switch {
  background: rgba(0, 0, 0, 0.08);
  border-color: rgba(0, 0, 0, 0.16);
}

html[data-theme="day"] .switch-thumb {
  transform: translateX(24px);
  background: #ffffff;
  color: #d97706;
  border-color: rgba(0, 0, 0, 0.12);
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
}

html[data-theme="day"] .switch-thumb .icon-moon { display: none; }
html[data-theme="day"] .switch-thumb .icon-sun { display: block; }"""

    if old_switch_css in css:
        css = css.replace(old_switch_css, new_switch_css)
    else:
        # append new switch css
        css += "\n" + new_switch_css

    # Upgrade Beer Cards & Shadcn Card Styling
    card_upgrade_css = """
/* Shadcn / Premium Gastrobar Cards con Profundidad y Personalidad */
.beer-tap-card {
  background: rgba(20, 22, 28, 0.88) !important;
  border: 1px solid rgba(255, 255, 255, 0.10) !important;
  border-radius: 14px !important;
  padding: 26px 22px !important;
  box-shadow: 0 10px 28px -5px rgba(0, 0, 0, 0.5) !important;
  backdrop-filter: blur(12px) !important;
  -webkit-backdrop-filter: blur(12px) !important;
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s ease, box-shadow 0.25s ease !important;
}

.beer-tap-card:hover, .beer-tap-card.tap-selected {
  transform: translateY(-5px) !important;
  border-color: rgba(245, 158, 11, 0.5) !important;
  box-shadow: 0 20px 40px -10px rgba(0, 0, 0, 0.7), 0 0 24px rgba(245, 158, 11, 0.15) !important;
}

html[data-theme="day"] .beer-tap-card {
  background: #ffffff !important;
  border-color: rgba(0, 0, 0, 0.09) !important;
  box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.06) !important;
}

html[data-theme="day"] .beer-tap-card:hover, html[data-theme="day"] .beer-tap-card.tap-selected {
  border-color: var(--terracotta) !important;
  box-shadow: 0 16px 32px -6px rgba(200, 109, 81, 0.18) !important;
}

.tap-beer-name {
  font-family: var(--font-heading) !important;
  font-size: 1.45rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.04em !important;
  text-transform: uppercase !important;
  line-height: 1.15 !important;
  margin: 0 0 6px !important;
}

.tap-specs {
  display: flex !important;
  gap: 8px !important;
  margin: 10px 0 14px !important;
}

.tap-spec-pill {
  font-family: var(--font-mono) !important;
  font-size: 0.72rem !important;
  font-weight: 700 !important;
  background: rgba(255, 255, 255, 0.06) !important;
  border: 1px solid rgba(255, 255, 255, 0.12) !important;
  padding: 4px 10px !important;
  border-radius: 6px !important;
  color: var(--text-main) !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 5px !important;
}

html[data-theme="day"] .tap-spec-pill {
  background: rgba(0, 0, 0, 0.04) !important;
  border-color: rgba(0, 0, 0, 0.1) !important;
  color: #1f2937 !important;
}

/* Unificación de Botones CTAs en Canillas */
.btn-tap-order {
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  gap: 8px !important;
  width: 100% !important;
  padding: 11px 16px !important;
  border-radius: 8px !important;
  background: rgba(245, 158, 11, 0.10) !important;
  border: 1px solid rgba(245, 158, 11, 0.32) !important;
  color: #f59e0b !important;
  font-weight: 700 !important;
  font-size: 0.82rem !important;
  letter-spacing: 0.02em !important;
  text-transform: uppercase !important;
  transition: all 0.22s ease !important;
}

.btn-tap-order:hover {
  background: #f59e0b !important;
  color: #0c0d10 !important;
  box-shadow: 0 0 18px rgba(245, 158, 11, 0.4) !important;
}

html[data-theme="day"] .btn-tap-order {
  background: rgba(200, 109, 81, 0.08) !important;
  border-color: rgba(200, 109, 81, 0.35) !important;
  color: #c86d51 !important;
}

html[data-theme="day"] .btn-tap-order:hover {
  background: #c86d51 !important;
  color: #ffffff !important;
  box-shadow: 0 4px 16px rgba(200, 109, 81, 0.3) !important;
}

/* Rediseño del Widget Flotante de WhatsApp: No más verde chillón que compite */
.floating-whatsapp {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 99;
}

.floating-wa-btn {
  width: auto !important;
  height: 48px !important;
  padding: 0 18px !important;
  border-radius: 999px !important;
  background: rgba(18, 20, 26, 0.94) !important;
  border: 1px solid rgba(255, 255, 255, 0.16) !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 15px rgba(255, 30, 39, 0.15) !important;
  color: #ffffff !important;
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  font-weight: 700 !important;
  font-size: 0.85rem !important;
  backdrop-filter: blur(12px) !important;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.floating-wa-btn:hover {
  background: #181922 !important;
  border-color: rgba(255, 255, 255, 0.3) !important;
  transform: translateY(-2px) scale(1.02) !important;
  box-shadow: 0 14px 36px rgba(0, 0, 0, 0.6), 0 0 20px rgba(255, 30, 39, 0.25) !important;
}

html[data-theme="day"] .floating-wa-btn {
  background: rgba(255, 255, 255, 0.96) !important;
  border-color: rgba(0, 0, 0, 0.15) !important;
  color: #111827 !important;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}

.lucide-icon {
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
}
"""
    css += "\n" + card_upgrade_css

    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("styles.css updated with modern switch, typography & Shadcn card styling!")

    # =========================================================================
    # 2. UPDATE INDEX.HTML (REPLACE ALL EMOJIS WITH LUCIDE ICONS)
    # =========================================================================
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Add Google Fonts Bebas Neue and Oswald link in head
    old_fonts = 'family=Alfa+Slab+One&family=Anton&family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@600;700&display=swap'
    new_fonts = 'family=Alfa+Slab+One&family=Anton&family=Bebas+Neue&family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@600;700&family=Oswald:wght@500;600;700&display=swap'
    html = html.replace(old_fonts, new_fonts)

    # 1. Redesign Toggle Button in Navbar (Minimalist Switch)
    old_toggle_markup = """        <!-- Selector Dual Día / Noche -->
        <button id="theme-toggle-btn" class="theme-toggle-btn" title="Cambiar entre estilo Día y Noche">
          <span id="theme-toggle-icon">🌙</span>
          <span id="theme-toggle-text">Noche 🌙</span>
        </button>"""

    new_toggle_markup = f"""        <!-- Switch Minimalista Día / Noche (Shadcn UI Style) -->
        <button id="theme-toggle-btn" class="theme-switch" role="switch" aria-label="Cambiar entre Modo Noche y Día" title="Modo Día / Noche">
          <span class="switch-thumb">
            {get_icon('moon', 13, 2.2, 'icon-moon')}
            {get_icon('sun', 13, 2.2, 'icon-sun')}
          </span>
        </button>"""

    html = html.replace(old_toggle_markup, new_toggle_markup)

    # 2. Location badge emoji -> Lucide MapPin
    html = html.replace('<span>📍 </span> BV. RONDEAU', f'{get_icon("map-pin", 15, 2.2)} BV. RONDEAU')
    html = html.replace('<span>📍</span> BV. RONDEAU', f'{get_icon("map-pin", 15, 2.2)} BV. RONDEAU')

    # 3. Hero CTAs: Replace emojis with Lucide Icons
    html = html.replace('Explorar las Cartas ➔', f'Explorar las Cartas {get_icon("arrow-right", 16, 2.2)}')
    html = html.replace('Explorar las Cartas âž”', f'Explorar las Cartas {get_icon("arrow-right", 16, 2.2)}')

    # 4. WhatsApp Presets Section: Replace emojis with Lucide Icons
    html = html.replace('<span>📅</span>\n                <span>Reservar Mesa</span>', f'{get_icon("calendar", 18, 2.2)}\n                <span>Reservar Mesa</span>')
    html = html.replace('<span>🎉</span>\n                <span>Festejos &amp; Cumpleaños</span>', f'{get_icon("party-popper", 18, 2.2)}\n                <span>Festejos &amp; Cumpleaños</span>')
    html = html.replace('<span>🍽️</span>\n                <span>Menú Ejecutivo del Día</span>', f'{get_icon("utensils", 18, 2.2)}\n                <span>Menú Ejecutivo del Día</span>')
    html = html.replace('<span>🍝</span>\n                <span>Jueves de Pasta Libre</span>', f'{get_icon("utensils", 18, 2.2)}\n                <span>Jueves de Pasta Libre</span>')
    html = html.replace('<span>🍻</span>\n                <span>Mesa Grande / Amigos</span>', f'{get_icon("beer", 18, 2.2)}\n                <span>Mesa Grande / Amigos</span>')
    html = html.replace('<span>🛵</span>\n                <span>Take Away / Retiro</span>', f'{get_icon("shopping-bag", 18, 2.2)}\n                <span>Take Away / Retiro</span>')
    html = html.replace('Enviar solicitud ➔', f'Enviar solicitud {get_icon("arrow-right", 14, 2)}')
    html = html.replace('Consultar opciones ➔', f'Consultar opciones {get_icon("arrow-right", 14, 2)}')
    html = html.replace('Ver menú de hoy ➔', f'Ver menú de hoy {get_icon("arrow-right", 14, 2)}')
    html = html.replace('Reservar jueves ➔', f'Reservar jueves {get_icon("arrow-right", 14, 2)}')
    html = html.replace('Coordinar mesa ➔', f'Coordinar mesa {get_icon("arrow-right", 14, 2)}')
    html = html.replace('Pedir para llevar ➔', f'Pedir para llevar {get_icon("arrow-right", 14, 2)}')

    # 5. Pizarra de Canillas Section: Remove 🍻 and 🍺 emojis
    html = html.replace('<div class="taps-icon-badge">🍻</div>', f'<div class="taps-icon-badge">{get_icon("beer", 24, 2.2)}</div>')
    html = html.replace('<span>🍺</span> Pedir Pinta por WhatsApp', f'{get_icon("beer", 15, 2.2)} Pedir Pinta')
    html = html.replace('<span>🍺</span> Consultar Pizarrón de Hoy', f'{get_icon("beer", 15, 2.2)} Consultar Pizarrón')

    # Add gauge and flame to specs in Beer Cards
    html = html.replace('<span class="tap-spec-pill">ABV ', f'<span class="tap-spec-pill">{get_icon("gauge", 13, 2)} ABV ')
    html = html.replace('<span class="tap-spec-pill">IBU ', f'<span class="tap-spec-pill">{get_icon("flame", 13, 2)} IBU ')

    # 6. Menu Tabs: Remove 🌙 and ☀️ emojis
    html = html.replace('<span>🌙</span> Carta Nocturna (Bodegón &amp; Pub)', f'{get_icon("moon", 16, 2.2)} Carta Nocturna (Bodegón &amp; Pub)')
    html = html.replace('<span>☀️</span> Carta Diurna (Cafetería &amp; Almuerzos)', f'{get_icon("sun", 16, 2.2)} Carta Diurna (Cafetería &amp; Almuerzos)')

    # 7. Lunch Suggester: Remove 🍽️ and 🚀 emojis
    html = html.replace('<span>🍽️</span>\n              <span>Armá tu Menú Ejecutivo del Mediodía</span>', f'{get_icon("utensils", 20, 2.2)}\n              <span>Armá tu Menú Ejecutivo del Mediodía</span>')
    html = html.replace('<span>🚀</span> Pedir Menú Ejecutivo por WhatsApp', f'{get_icon("utensils", 16, 2.2)} Pedir Menú Ejecutivo por WhatsApp')

    # 8. Menu items buttons: replace ➔ with Lucide ArrowRight
    html = re.sub(r'Pedir por WhatsApp ➔', f'Pedir por WhatsApp {get_icon("arrow-right", 14, 2)}', html)
    html = re.sub(r'Reservar Pasta Libre ➔', f'Reservar Pasta Libre {get_icon("arrow-right", 14, 2)}', html)
    html = re.sub(r'Consultar Canillas ➔', f'Consultar Canillas {get_icon("arrow-right", 14, 2)}', html)
    html = re.sub(r'Consultar Barra ➔', f'Consultar Barra {get_icon("arrow-right", 14, 2)}', html)
    html = re.sub(r'Pedir Desayuno ➔', f'Pedir Desayuno {get_icon("arrow-right", 14, 2)}', html)
    html = re.sub(r'Pedir Merienda ➔', f'Pedir Merienda {get_icon("arrow-right", 14, 2)}', html)
    html = re.sub(r'Consultar Menú de Hoy ➔', f'Consultar Menú de Hoy {get_icon("arrow-right", 14, 2)}', html)
    html = html.replace('📄 Ver Carta Completa (PDF)', f'{get_icon("file-text", 16, 2.2)} Ver Carta Completa (PDF)')
    html = html.replace('Abrir en Google Drive ↗', f'Abrir en Google Drive {get_icon("external-link", 14, 2)}')
    html = html.replace('🎟️ Comprar Entradas para Eventos ↗', f'{get_icon("sparkles", 16, 2.2)} Comprar Entradas para Eventos {get_icon("external-link", 14, 2)}')

    # 9. Festejos perks emojis: remove 🥂, 🪑, 🎂, etc. inside app.js too
    # 10. Footer brand trigger: remove 🎨
    html = html.replace('🎨 Ver Identidad Visual &amp; Descargar Logos', f'{get_icon("palette", 16, 2.2)} Ver Identidad Visual &amp; Descargar Logos')
    html = html.replace('🎨 Identidad Visual &amp; Suite de Logos', f'{get_icon("palette", 20, 2.2)} Identidad Visual &amp; Suite de Logos')

    # 11. Floating WhatsApp Button: Replace with elegant dark pill
    old_floating_wa = """  <div class="floating-whatsapp">
    <div id="floating-wa-menu" class="floating-wa-menu">
      <div class="wa-menu-title">¿Qué necesitás consultar?</div>
      <a href="#" class="wa-quick-item" data-wa-preset="reservar_mesa">
        <span>📅</span> <span>Reservar mesa</span>
      </a>
      <a href="#" class="wa-quick-item" data-wa-preset="cumpleanos">
        <span>🎉</span> <span>Festejar cumpleaños</span>
      </a>
      <a href="#" class="wa-quick-item" data-wa-preset="menu_ejecutivo">
        <span>🍽️</span> <span>Menú del día</span>
      </a>
      <a href="#" class="wa-quick-item" data-wa-preset="take_away">
        <span>🛵</span> <span>Take Away</span>
      </a>
    </div>

    <button id="floating-wa-toggle" class="floating-wa-btn" aria-label="Abrir opciones de WhatsApp">
      <svg width="32" height="32" viewBox="0 0 24 24" fill="currentColor">
        <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981z"/>
      </svg>
    </button>
  </div>"""

    new_floating_wa = f"""  <div class="floating-whatsapp">
    <div id="floating-wa-menu" class="floating-wa-menu">
      <div class="wa-menu-title">Atención Directa Cosme Alberdi</div>
      <a href="#" class="wa-quick-item" data-wa-preset="reservar_mesa">
        {get_icon("calendar", 16, 2)} <span>Reservar mesa</span>
      </a>
      <a href="#" class="wa-quick-item" data-wa-preset="cumpleanos">
        {get_icon("party-popper", 16, 2)} <span>Festejar cumpleaños</span>
      </a>
      <a href="#" class="wa-quick-item" data-wa-preset="menu_ejecutivo">
        {get_icon("utensils", 16, 2)} <span>Menú del día</span>
      </a>
      <a href="#" class="wa-quick-item" data-wa-preset="take_away">
        {get_icon("shopping-bag", 16, 2)} <span>Take Away / Retiro</span>
      </a>
    </div>

    <button id="floating-wa-toggle" class="floating-wa-btn" aria-label="Atención por WhatsApp">
      <span class="pulse-dot" style="background:#22c55e; width:8px; height:8px;"></span>
      {get_icon("whatsapp", 20, 0, "wa-svg-icon")}
      <span>WhatsApp</span>
    </button>
  </div>"""

    html = html.replace(old_floating_wa, new_floating_wa)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html completely cleansed of emojis and equipped with Lucide SVGs!")

    # =========================================================================
    # 3. UPDATE APP.JS (NO EMOJIS IN STATUS TEXTS OR TOGGLE LOGIC)
    # =========================================================================
    with open('app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()

    # Clean schedule strings
    app_js = app_js.replace("`☀️ ${timeStr} h · Abierto · Cafetería de Especialidad & Desayunos`", "`Abierto · Cafetería de Especialidad & Desayunos`")
    app_js = app_js.replace("`☀️ ${timeStr} h · Abierto · Modo Almuerzo Ejecutivo & Menú del Día`", "`Abierto · Almuerzo Ejecutivo & Menú del Día`")
    app_js = app_js.replace("`☕ ${timeStr} h · Abierto · Merienda Alberdi & Tostados`", "`Abierto · Merienda Alberdi & Tostados`")
    app_js = app_js.replace("`🌙 ${timeStr} h · En vivo · Modo Pub & 12 Canillas de Cerveza Artesanal`", "`En vivo · Modo Pub & 12 Canillas de Cerveza`")
    app_js = app_js.replace("`😴 ${timeStr} h · Cerrado por descanso · Abrimos a las 08:00 h con café fresco`", "`Cerrado por descanso · Abrimos a las 08:00 h`")

    # Update theme toggle logic in app.js for switch without text
    old_theme_func = """    if (theme === 'day') {
      if (themeToggleText) themeToggleText.textContent = 'Día ☀️';
      if (themeToggleIcon) themeToggleIcon.textContent = '☀️';
      if (metaThemeColor) metaThemeColor.setAttribute('content', '#F5F0E6');
      if (updateMenu) setMenuMode('day');
    } else {
      if (themeToggleText) themeToggleText.textContent = 'Noche 🌙';
      if (themeToggleIcon) themeToggleIcon.textContent = '🌙';
      if (metaThemeColor) metaThemeColor.setAttribute('content', '#0C0D10');
      if (updateMenu) setMenuMode('night');
    }"""

    new_theme_func = """    if (theme === 'day') {
      if (themeToggleBtn) themeToggleBtn.setAttribute('aria-checked', 'true');
      if (metaThemeColor) metaThemeColor.setAttribute('content', '#F7F4EE');
      if (updateMenu) setMenuMode('day');
    } else {
      if (themeToggleBtn) themeToggleBtn.setAttribute('aria-checked', 'false');
      if (metaThemeColor) metaThemeColor.setAttribute('content', '#0C0D10');
      if (updateMenu) setMenuMode('night');
    }"""

    app_js = app_js.replace(old_theme_func, new_theme_func)

    # Clean calculator strings in app.js (remove 🥂, 🪑, 🎂, etc.)
    app_js = app_js.replace("'🥂 <strong>1 Botella de espumante</strong> de cortesía para el brindis.'", "'<strong>1 Botella de espumante</strong> de cortesía para el brindis.'")
    app_js = app_js.replace("'🪑 <strong>Mesa unificada</strong> en sector salón o vereda templada.'", "'<strong>Mesa unificada</strong> en sector salón o vereda templada.'")
    app_js = app_js.replace("'🎂 Podés traer tu torta (servicio de vajilla sin costo).'", "'Podés traer tu torta (servicio de vajilla sin costo).'")
    app_js = app_js.replace("'🥂 <strong>2 Botellas de espumante</strong> de cortesía para el brindis.'", "'<strong>2 Botellas de espumante</strong> de cortesía para el brindis.'")
    app_js = app_js.replace("'🎯 <strong>Sector semi-exclusivo</strong> reservado especialmente.'", "'<strong>Sector semi-exclusivo</strong> reservado especialmente.'")
    app_js = app_js.replace("'🍻 <strong>Ronda de pintas de bienvenida</strong> a precio promocional.'", "'<strong>Ronda de pintas de bienvenida</strong> a precio promocional.'")
    app_js = app_js.replace("'🥂 <strong>3 Botellas de espumante</strong> de regalo para celebrar a lo grande.'", "'<strong>3 Botellas de espumante</strong> de regalo para celebrar a lo grande.'")
    app_js = app_js.replace("'👑 <strong>Espacio exclusivo</strong> con atención de camarero dedicada.'", "'<strong>Espacio exclusivo</strong> con atención de camarero dedicada.'")
    app_js = app_js.replace("'🎧 Opción de solicitar temas a la cabina de DJ en vivo.'", "'Opción de solicitar temas a la cabina de DJ en vivo.'")

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)
    print("app.js updated successfully with clean switch logic!")

if __name__ == '__main__':
    update_all()
