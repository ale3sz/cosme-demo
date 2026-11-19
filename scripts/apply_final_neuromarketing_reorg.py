import re

def apply_full_reorg():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Navbar
    nav_pattern = r'<nav class="nav-links">[\s\S]*?</nav>'
    new_nav = """<nav class="nav-links">
        <a href="#inicio" class="active">Inicio</a>
        <a href="#menu">Cartas &amp; Canillas</a>
        <a href="#espacio">El Espacio</a>
        <a href="#resenas">Opiniones</a>
        <a href="#festejos">Reservas &amp; Festejos</a>
        <a href="#ubicacion">Ubicación</a>
      </nav>"""
    html = re.sub(nav_pattern, new_nav, html, count=1)

    # 2. Update Footer Nav
    footer_nav_pattern = r'<h5>Navegaci[óo]n</h5>\s*<ul>[\s\S]*?</ul>'
    new_footer_nav = """<h5>Navegación</h5>
          <ul>
            <li><a href="#inicio">Inicio</a></li>
            <li><a href="#menu">Cartas &amp; Canillas</a></li>
            <li><a href="#espacio">El Espacio</a></li>
            <li><a href="#resenas">Opiniones</a></li>
            <li><a href="#festejos">Reservas &amp; Festejos</a></li>
            <li><a href="#ubicacion">Ubicación</a></li>
          </ul>"""
    html = re.sub(footer_nav_pattern, new_footer_nav, html, count=1)

    # 3. Create #espacio block
    espacio_block = """    <!-- =====================================================================
         5. BENTO GRID: EL ESPACIO (ARQUITECTURA & CONFORT)
         ===================================================================== -->
    <section id="espacio" class="bento-section scroll-reveal">
      <div class="container">
        <div class="section-head">
          <span class="section-tag">Ambiente y Mística</span>
          <h2 class="section-heading">EL ESPACIO</h2>
          <p class="hero-subtitle">
            Ladrillo original de Barrio Alberdi, hierro forjado, lámparas Edison y el clima perfecto tanto para una cita como para mesas de amigos.
          </p>
        </div>

        <div class="bento-grid">
          <div class="bento-card bento-card-1">
            <img src="assets/cartel-neon-ladrillo.jpg" alt="Pared de ladrillo visto con cartel de neón Cosme" class="bento-bg-img" loading="lazy">
            <div class="bento-overlay">
              <h3 class="bento-title">Neón &amp; Ladrillo Visto</h3>
              <p class="bento-desc">La calidez de la mampostería original enmarcada con el halo carmesí del emblemático cartel de neón.</p>
            </div>
          </div>

          <div class="bento-card bento-card-2">
            <img src="assets/barra-edison.jpg" alt="Barra rústica con banquetas y canillas de cerveza" class="bento-bg-img" loading="lazy">
            <div class="bento-overlay">
              <h3 class="bento-title">Barra &amp; Canillas</h3>
              <p class="bento-desc">Madera noble maciza, lámparas jaula Edison y 12 canillas artesanales a 2°C en rotación permanente.</p>
            </div>
          </div>

          <div class="bento-card bento-card-3">
            <img src="assets/salon-dia-tolix.jpg" alt="Salón con sillas Tolix y luz natural" class="bento-bg-img" loading="lazy">
            <div class="bento-overlay">
              <h3 class="bento-title">Salón &amp; Madera Noble</h3>
              <p class="bento-desc">Mesas amplias, sillas Tolix y climatización serena para disfrutar de brunch, meriendas o almuerzo de trabajo.</p>
            </div>
          </div>

          <div class="bento-card bento-card-4">
            <img src="assets/noche cosme.jpg" alt="Noches de bulevar y vereda en Cosme Alberdi" class="bento-bg-img" loading="lazy">
            <div class="bento-overlay">
              <h3 class="bento-title">Vereda &amp; Noches de Bulevar</h3>
              <p class="bento-desc">Deck al aire libre sobre Bv. Rondeau para las noches templadas con vista al ritmo urbano de Zona Norte.</p>
            </div>
          </div>
        </div>
      </div>
    </section>"""

    # 4. Create #resenas block (Social Proof)
    star_svg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" class="lucide-icon"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>'
    mini_star_svg = '<svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" class="lucide-icon"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>'

    resenas_block = f"""    <!-- =====================================================================
         6. SECCIÓN PRUEBA SOCIAL & COMUNIDAD (RESEÑAS VERIFICADAS)
         ===================================================================== -->
    <section id="resenas" class="resenas-section scroll-reveal">
      <div class="container">
        <div class="section-head">
          <span class="section-tag">Validación en Vivo</span>
          <h2 class="section-heading">LO QUE DICEN EN RONDEAU</h2>
          <p class="hero-subtitle">
            Más de 1.800 opiniones reales en Google Maps respaldan nuestras porciones de bodegón, la temperatura de las canillas y la calidez del equipo.
          </p>
        </div>

        <!-- Caja resumen de puntuación Google -->
        <div class="resenas-summary-box">
          <div class="resenas-score-group">
            <div class="resenas-score-big">4.7</div>
            <div class="resenas-score-meta">
              <div class="stars-row">
                {star_svg} {star_svg} {star_svg} {star_svg} {star_svg}
              </div>
              <h4>Excelente en Google Maps</h4>
              <p>Basado en más de 1.850 reseñas de clientes reales en Rosario</p>
            </div>
          </div>

          <div class="resenas-metrics-strip">
            <div class="resena-metric-item">
              <span class="resena-metric-val">12</span>
              <span class="resena-metric-lbl">Canillas Tiradas</span>
            </div>
            <div class="resena-metric-item">
              <span class="resena-metric-val">08-03 h</span>
              <span class="resena-metric-lbl">Cocina Corrida</span>
            </div>
            <div class="resena-metric-item">
              <span class="resena-metric-val">100%</span>
              <span class="resena-metric-lbl">Sin Costo de Reserva</span>
            </div>
          </div>

          <a href="https://maps.google.com/?q=Pub+y+Restaurante+Cosme+Alberdi" target="_blank" rel="noopener noreferrer" class="btn-gmaps" style="white-space:nowrap;">
            Ver Todas las Reseñas <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide-icon"><path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/></svg>
          </a>
        </div>

        <!-- Grid de 3 Testimonios Clave por Arquetipo -->
        <div class="resenas-cards-grid">
          <!-- Tarjeta 1: Festejos y Grupos -->
          <div class="resena-card">
            <div>
              <span class="resena-badge">Festejo de Cumpleaños</span>
              <div class="stars-row">
                {mini_star_svg} {mini_star_svg} {mini_star_svg} {mini_star_svg} {mini_star_svg}
              </div>
              <p class="resena-quote">
                &ldquo;Festejamos un cumple de 18 personas en el sector preferencial. La atención fue impecable, las smash burgers y las torres de papas salieron al toque y nos trajeron el espumante para el brindis de regalo. Cero complicaciones para reservar.&rdquo;
              </p>
            </div>
            <div class="resena-author-box">
              <div class="resena-avatar">MV</div>
              <div class="resena-author-info">
                <h5>Mariana V.</h5>
                <span>Local Guide en Google Maps · Festejo Grupal</span>
              </div>
            </div>
          </div>

          <!-- Tarjeta 2: Cerveceros & After -->
          <div class="resena-card">
            <div>
              <span class="resena-badge">Cervecería &amp; Amigos</span>
              <div class="stars-row">
                {mini_star_svg} {mini_star_svg} {mini_star_svg} {mini_star_svg} {mini_star_svg}
              </div>
              <p class="resena-quote">
                &ldquo;La mejor pizarra de canillas de Zona Norte. La IPA Alberdi y la Honey servidas en copón helado con la espuma perfecta. La cascada de cheddar caliente sobre las papas es una bomba. El ambiente con los neones y la música está a otro nivel.&rdquo;
              </p>
            </div>
            <div class="resena-author-box">
              <div class="resena-avatar">GR</div>
              <div class="resena-author-info">
                <h5>Gonzalo R.</h5>
                <span>Cliente Verificado · Noches de Bulevar</span>
              </div>
            </div>
          </div>

          <!-- Tarjeta 3: Bodegón y Almuerzos -->
          <div class="resena-card">
            <div>
              <span class="resena-badge">Bodegón Abundante</span>
              <div class="stars-row">
                {mini_star_svg} {mini_star_svg} {mini_star_svg} {mini_star_svg} {mini_star_svg}
              </div>
              <p class="resena-quote">
                &ldquo;Comida casera, abundante de verdad y con precios súper razonables. Fuimos a almorzar el fin de semana y con un solo plato comen dos tranquilamente. El café de especialidad post almuerzo cierra la experiencia de diez.&rdquo;
              </p>
            </div>
            <div class="resena-author-box">
              <div class="resena-avatar">LM</div>
              <div class="resena-author-info">
                <h5>Luciana M.</h5>
                <span>Reseña de Google Maps · Almuerzo en Familia</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>"""

    # Check if #espacio already exists
    if '<section id="espacio"' in html:
        print("espacio already exists, removing first")
        html = re.sub(r'<!-- =+[\r\n\s]+.*?BENTO GRID: EL ESPACIO[\s\S]*?<section id="espacio"[\s\S]*?</section>', '', html)

    # Check if #resenas already exists
    if '<section id="resenas"' in html:
        print("resenas already exists, removing first")
        html = re.sub(r'<!-- =+[\r\n\s]+.*?SECCI[ÓO]N PRUEBA SOCIAL[\s\S]*?<section id="resenas"[\s\S]*?</section>', '', html)

    # Insert #espacio and #resenas right after #menu section closing tag
    menu_end_tag = '</section>'
    menu_pos = html.find('id="menu"')
    if menu_pos == -1:
        print("Error: #menu not found!")
        return

    menu_close_pos = html.find('</section>', menu_pos) + len('</section>')

    middle_block = f"\n\n{espacio_block}\n\n{resenas_block}"
    html = html[:menu_close_pos] + middle_block + html[menu_close_pos:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    print("index.html updated successfully with complete neuromarketing flow!")

if __name__ == '__main__':
    apply_full_reorg()
