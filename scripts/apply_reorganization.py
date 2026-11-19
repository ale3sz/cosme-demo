import re

def run_reorganization():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Navbar Links
    old_nav_match = re.search(r'<nav class="nav-links">[\s\S]*?</nav>', html)
    new_nav = """<nav class="nav-links">
        <a href="#inicio" class="active">Inicio</a>
        <a href="#espacio">El Espacio</a>
        <a href="#menu">Cartas &amp; Canillas</a>
        <a href="#festejos">Reservas &amp; Festejos</a>
        <a href="#ubicacion">Ubicación</a>
      </nav>"""
    html = html[:old_nav_match.start()] + new_nav + html[old_nav_match.end():]

    # 2. Extract sections
    hero_pattern = r'<!-- =+[\r\n\s]+2\. HERO SECTION[\s\S]*?<section class="hero">[\s\S]*?</section>'
    hero_match = re.search(hero_pattern, html)
    hero_block = hero_match.group(0)

    # In hero_block, update the CTAs
    # Change "Explorar las Cartas" to "Ver Cartas &amp; Canillas"
    hero_block = hero_block.replace('Explorar las Cartas', 'Ver Cartas &amp; Canillas')
    # Change "Reservar por WhatsApp" to "Reservar Mesa"
    hero_block = hero_block.replace('Reservar por WhatsApp', 'Reservar Mesa')

    # Extract canillas taps-board
    canillas_pattern = r'<!-- =+[\r\n\s]+3B\. PIZARRA DE CANILLAS[\s\S]*?<section id="canillas"[\s\S]*?</section>'
    canillas_match = re.search(canillas_pattern, html)
    canillas_block = canillas_match.group(0)

    taps_inner = re.search(r'(<div class="taps-board">[\s\S]*?</div>\s*</div>)\s*</div>\s*</section>', canillas_block)
    taps_board_html = taps_inner.group(1).strip()
    # Add id="canillas" and initial display:none to taps-board
    taps_board_html = taps_board_html.replace('<div class="taps-board">', '<div id="canillas" class="taps-board" style="display:none; margin-top:28px;">', 1)

    # Extract menu block
    menu_pattern = r'<!-- =+[\r\n\s]+4\. SECCI[ÓO]N MEN[ÚU][\s\S]*?<section id="menu"[\s\S]*?</section>'
    menu_match = re.search(menu_pattern, html)
    menu_block = menu_match.group(0)

    # In menu_block, update section head and tabs:
    # 1) Section title:
    old_menu_head = re.search(r'<div class="section-head">[\s\S]*?</div>', menu_block).group(0)
    new_menu_head = """<div class="section-head">
          <span class="section-tag">Gastronomía &amp; Cervecería</span>
          <h2 class="section-heading">CARTAS &amp; CANILLAS</h2>
          <p class="hero-subtitle">
            Cocina de bodegón con porciones para compartir y 12 canillas de cerveza artesanal tiradas en copón enfriado.
          </p>
        </div>"""
    menu_block = menu_block.replace(old_menu_head, new_menu_head, 1)

    # 2) Tabs: Add Canillas Tiradas tab between night and day
    old_menu_tabs = re.search(r'<div class="menu-mode-tabs">[\s\S]*?</div>', menu_block).group(0)
    new_menu_tabs = """<div class="menu-mode-tabs">
          <button class="menu-mode-tab active" data-menu-target="night">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg> Carta Nocturna (Bodegón &amp; Pub)
          </button>
          <button class="menu-mode-tab" data-menu-target="taps">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><path d="M17 11h1a3 3 0 0 1 0 6h-1"/><path d="M9 12v6"/><path d="M13 12v6"/><path d="M14 7.5c-1 0-1.44.5-3 .5s-2-.5-3-.5-1.72.5-2.5.5a2.5 2.5 0 0 1 0-5c.78 0 1.57.5 2.5.5S9.44 3 11 3s2 .5 3 .5 1.72-.5 2.5-.5a2.5 2.5 0 0 1 0 5c-.78 0-1.5-.5-2.5-.5Z"/><path d="M5 8v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2V8"/></svg> Canillas Tiradas (12 Taps en Vivo)
          </button>
          <button class="menu-mode-tab" data-menu-target="day">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg> Carta Diurna (Cafetería &amp; Almuerzos)
          </button>
        </div>"""
    menu_block = menu_block.replace(old_menu_tabs, new_menu_tabs, 1)

    # 3) Insert taps_board_html right after new_menu_tabs
    menu_block = menu_block.replace(new_menu_tabs, new_menu_tabs + "\n\n        <!-- 12 Canillas Tiradas (Tab 'taps') -->\n        " + taps_board_html, 1)

    # Update section comment
    menu_block = re.sub(r'<!-- =+[\r\n\s]+4\. SECCI[ÓO]N MEN[ÚU][\s\S]*?-->',
"""<!-- =====================================================================
         4. SECCIÓN CARTAS & CANILLAS (PROPUESTA GASTRONÓMICA UNIFICADA)
         ===================================================================== -->""", menu_block, count=1)

    # Extract espacio block
    espacio_pattern = r'<!-- =+[\r\n\s]+5\. BENTO GRID: EL ESPACIO[\s\S]*?<section id="espacio"[\s\S]*?</section>'
    espacio_match = re.search(espacio_pattern, html)
    espacio_block = espacio_match.group(0)
    # Update section number comment
    espacio_block = re.sub(r'5\. BENTO GRID: EL ESPACIO', '3. BENTO GRID: EL ESPACIO', espacio_block, count=1)

    # Extract festejos block
    festejos_pattern = r'<!-- =+[\r\n\s]+6\. FESTEJOS[\s\S]*?<section id="festejos"[\s\S]*?</section>'
    festejos_match = re.search(festejos_pattern, html)
    festejos_block = festejos_match.group(0)

    # Update festejos block to be RESERVAS & FESTEJOS
    festejos_block = re.sub(r'6\. FESTEJOS Y CUMPLEA[ÑN]OS', '5. RESERVAS & FESTEJOS', festejos_block, count=1)

    # Update the left side of festejos-content
    old_festejos_left = re.search(r'<div>\s*<span class="section-tag">Momentos Especiales</span>[\s\S]*?</div>\s*<!-- Calculador', festejos_block).group(0)
    new_festejos_left = """<div>
              <span class="section-tag">Asegurá tu Lugar</span>
              <h2 class="section-heading">RESERVAS &amp; FESTEJOS</h2>
              <p class="hero-subtitle" style="text-align: left; margin: 0 0 16px;">
                Almuerzos de trabajo, meriendas, cenas con amigos y celebraciones de cumpleaños en salón o vereda.
              </p>

              <ul class="festejos-perks">
                <li>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                  <span><strong>Reserva online inmediata</strong> sin costo para grupos chicos o grandes.</span>
                </li>
                <li>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                  <span><strong>Brindis con espumante de regalo</strong> en mesas de cumpleaños y festejos.</span>
                </li>
                <li>
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
                  <span>Música, DJs invitados los fines de semana y sector preferencial unificado.</span>
                </li>
              </ul>

              <div style="margin-top: 24px; display: flex; flex-wrap: wrap; gap: 12px; align-items: center;">
                <button class="btn-kraft-torn" data-open-modal="reserva" style="cursor: pointer;">
                  Reservar Mesa Ahora <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><path d="M5 12h14"/><path d="m12 5 7 7-7 7"/></svg>
                </button>
                <a href="https://compras.evento-simple.com/cosme" target="_blank" rel="noopener noreferrer" class="btn-gmaps" style="display:inline-flex; align-items:center; gap:8px;">
                  Entradas para Eventos <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
                </a>
              </div>
            </div>

            <!-- Calculador"""
    festejos_block = festejos_block.replace(old_festejos_left, new_festejos_left, 1)

    # Extract ubicacion block
    ubicacion_pattern = r'<!-- =+[\r\n\s]+7\. UBICACI[ÓO]N[\s\S]*?<section id="ubicacion"[\s\S]*?</section>'
    ubicacion_match = re.search(ubicacion_pattern, html)
    ubicacion_block = ubicacion_match.group(0)
    ubicacion_block = re.sub(r'7\. UBICACI[ÓO]N', '6. UBICACIÓN', ubicacion_block, count=1)

    # Reassemble main content
    # Order:
    # 1. hero_block
    # 2. espacio_block
    # 3. menu_block (with canillas inside)
    # 4. festejos_block
    # 5. ubicacion_block
    main_start = html.find('<main id="inicio">') + len('<main id="inicio">')
    main_end = html.find('</main>')

    new_main_content = f"""

    {hero_block}

    {espacio_block}

    {menu_block}

    {festejos_block}

    {ubicacion_block}

  """

    html = html[:main_start] + new_main_content + html[main_end:]

    # 4. Update Footer Links & Remove Brand trigger
    footer_pattern = r'<footer class="site-footer">[\s\S]*?</footer>'
    footer_match = re.search(footer_pattern, html)
    footer_block = footer_match.group(0)

    # Remove the brand button from footer
    footer_block = re.sub(r'<button class="btn-brand-modal-trigger"[\s\S]*?</button>', '', footer_block)

    # Update navigation column links
    old_footer_nav = re.search(r'<h5>Navegaci[óo]n</h5>\s*<ul>[\s\S]*?</ul>', footer_block).group(0)
    new_footer_nav = """<h5>Navegación</h5>
          <ul>
            <li><a href="#inicio">Inicio</a></li>
            <li><a href="#espacio">El Espacio</a></li>
            <li><a href="#menu">Cartas &amp; Canillas</a></li>
            <li><a href="#festejos">Reservas &amp; Festejos</a></li>
            <li><a href="#ubicacion">Ubicación</a></li>
          </ul>"""
    footer_block = footer_block.replace(old_footer_nav, new_footer_nav, 1)

    html = html[:footer_match.start()] + footer_block + html[footer_match.end():]

    # Save reorganized index.html
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("index.html reorganization completed successfully!")

if __name__ == '__main__':
    run_reorganization()
