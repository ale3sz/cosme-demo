import re

def apply_changes():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove #espacio section
    espacio_pattern = r'<!-- =+[\r\n\s]+3\. BENTO GRID: EL ESPACIO[\s\S]*?<section id="espacio"[\s\S]*?</section>'
    if re.search(espacio_pattern, html):
        html = re.sub(espacio_pattern, '', html, count=1)
        print("Removed #espacio with comment header")
    else:
        # Fallback search
        espacio_pattern2 = r'<section id="espacio"[\s\S]*?</section>'
        html = re.sub(espacio_pattern2, '', html, count=1)
        print("Removed #espacio section tag")

    # 2. Update Navbar: Remove #espacio link
    old_nav = re.search(r'<nav class="nav-links">[\s\S]*?</nav>', html).group(0)
    new_nav = """<nav class="nav-links">
        <a href="#inicio" class="active">Inicio</a>
        <a href="#menu">Cartas &amp; Canillas</a>
        <a href="#festejos">Reservas &amp; Festejos</a>
        <a href="#ubicacion">Ubicación</a>
      </nav>"""
    html = html.replace(old_nav, new_nav, 1)

    # 3. Update Footer: Remove #espacio link
    old_footer_nav = re.search(r'<h5>Navegaci[óo]n</h5>\s*<ul>[\s\S]*?</ul>', html).group(0)
    new_footer_nav = """<h5>Navegación</h5>
          <ul>
            <li><a href="#inicio">Inicio</a></li>
            <li><a href="#menu">Cartas &amp; Canillas</a></li>
            <li><a href="#festejos">Reservas &amp; Festejos</a></li>
            <li><a href="#ubicacion">Ubicación</a></li>
          </ul>"""
    html = html.replace(old_footer_nav, new_footer_nav, 1)

    # 4. Update menu-footer-bar in #menu
    old_menu_footer = re.search(r'<div class="menu-footer-bar">[\s\S]*?</div>\s*</div>\s*</section>', html).group(0)
    new_menu_footer = """<div class="menu-footer-bar">
          <p>¿Buscás la lista completa con precios detallados, opciones sin TACC, coctelería y pastelería?</p>
          <div class="menu-actions">
            <button class="btn-carta-pdf" data-open-pdf="noche">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/></svg> Ver Carta Noche &amp; Salón (PDF)
            </button>
            <button class="btn-carta-pdf" data-open-pdf="dia" style="border-color: rgba(255, 170, 0, 0.4); background: rgba(255, 170, 0, 0.08);">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/></svg> Ver Desayunos &amp; Meriendas (PDF)
            </button>
          </div>
        </div>

      </div>
    </section>"""
    html = html.replace(old_menu_footer, new_menu_footer, 1)

    # 5. Replace #modal-carta with rich in-page viewer
    old_modal_carta = re.search(r'<!-- =+[\r\n\s]+11\. MODAL: VISOR DE CARTA COMPLETA[\s\S]*?<div id="modal-carta"[\s\S]*?</div>\s*</div>\s*</div>', html).group(0)
    new_modal_carta = """<!-- =====================================================================
       11. MODAL: VISOR DE CARTA DIGITAL IN-PAGE
       ===================================================================== -->
  <div id="modal-carta" class="modal-backdrop" role="dialog" aria-modal="true" aria-labelledby="modal-carta-title">
    <div class="modal-window modal-window-pdf">
      <!-- Modal Header -->
      <div class="modal-pdf-header">
        <div class="modal-pdf-titles">
          <div class="modal-pdf-badge" id="modal-pdf-badge">CARTA SALÓN &amp; NOCHE</div>
          <h3 id="modal-carta-title" class="modal-title" style="margin:0; font-size:1.15rem;">CARTA DIGITAL COSME</h3>
        </div>

        <!-- Selector de Carta (Noche vs Día) -->
        <div class="pdf-switch-tabs">
          <button type="button" class="pdf-switch-tab active" data-pdf-doc="noche">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg> Carta Salón &amp; Noche
          </button>
          <button type="button" class="pdf-switch-tab" data-pdf-doc="dia">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg> Desayunos &amp; Meriendas
          </button>
        </div>

        <div class="modal-pdf-actions">
          <a id="modal-pdf-download-link" href="assets/docs/carta-noche.pdf" download="Carta_Cosme_Alberdi_Noche.pdf" class="btn-pdf-action" title="Descargar archivo PDF oficial">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>
            <span class="btn-pdf-action-text">Descargar PDF</span>
          </a>
          <button class="modal-close-btn" aria-label="Cerrar visor de carta">&times;</button>
        </div>
      </div>

      <!-- Iframe Contenedor del PDF sin salir de la web -->
      <div class="modal-pdf-body">
        <iframe 
          id="pdf-frame" 
          src="https://drive.google.com/file/d/1r6Pmaf6tBvK8j-wzST7jegs-poxu5HXt/preview" 
          title="Visor de Carta Digital Cosme Alberdi" 
          class="pdf-embed-frame"
          allow="autoplay">
        </iframe>
      </div>

      <!-- Footer rápido del visor -->
      <div class="modal-pdf-footer">
        <span class="pdf-footer-note">Visualización directa in-page · Documento oficial actualizado</span>
        <button class="btn-nav-reserve" data-open-modal="reserva" style="padding: 7px 16px; font-size: 0.82rem;">
          Reservar Mesa
        </button>
      </div>
    </div>
  </div>"""
    html = html.replace(old_modal_carta, new_modal_carta, 1)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("index.html updated successfully!")

if __name__ == '__main__':
    apply_changes()
