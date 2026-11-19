import re

def update_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Navbar logos & add #canillas link
    old_navbar_logos = """      <a href="#inicio" class="brand-logo" aria-label="Volver al inicio">
        <!-- Logo Noche: Mascota Cosme -->
        <img src="assets/cosme-logo-amber.png" alt="Mascota Cosme Alberdi" class="nav-logo-night" width="44" height="44">
        <!-- Logo Día: .COSME.® Nuevo Logo -->
        <img src="assets/logo_day_dark_transparent.png" alt="Logo Cosme Alberdi" class="nav-logo-day" height="34">
        <div class="brand-title nav-brand-text">
          <span>COSME</span>
          <span class="brand-sub">ALBERDI · ROSARIO</span>
        </div>
      </a>

      <nav class="nav-links">
        <a href="#inicio" class="active">Inicio</a>
        <a href="#whatsapp-rapido">WhatsApp</a>
        <a href="#menu">Menú &amp; Cartas</a>
        <a href="#espacio">El Espacio</a>
        <a href="#festejos">Festejos</a>
        <a href="#ubicacion">Ubicación</a>
      </nav>"""

    new_navbar_logos = """      <a href="#inicio" class="brand-logo" aria-label="Volver al inicio">
        <!-- Logo Noche: Mascota Cosme en Ámbar Dorado -->
        <img src="assets/cosme-mascot-amber.png" alt="Mascota Cosme Alberdi" class="nav-logo-night" width="44" height="44">
        <!-- Logo Día: Wordmark Cosme en Negro Vintage -->
        <img src="assets/cosme-wordmark-black.png" alt="Logo Cosme Alberdi" class="nav-logo-day" height="32">
        <div class="brand-title nav-brand-text">
          <span>COSME</span>
          <span class="brand-sub">ALBERDI · ROSARIO</span>
        </div>
      </a>

      <nav class="nav-links">
        <a href="#inicio" class="active">Inicio</a>
        <a href="#canillas">Canillas &amp; Birras</a>
        <a href="#whatsapp-rapido">WhatsApp</a>
        <a href="#menu">Menú &amp; Cartas</a>
        <a href="#espacio">El Espacio</a>
        <a href="#festejos">Festejos</a>
        <a href="#ubicacion">Ubicación</a>
      </nav>"""

    if old_navbar_logos in html:
        html = html.replace(old_navbar_logos, new_navbar_logos)
        print("Updated Navbar logos & links.")
    else:
        print("Navbar logos not matched exactly, checking regex...")

    # 2. Update Hero logo assets and live status id
    old_hero_box = """        <div class="hero-logo-box">
          <!-- Logo Noche: Neón Rojo puro sin nada más -->
          <img src="assets/logo_neon_pure.png" alt="Cartel de Neón Rojo Cosme" class="hero-logo-night" width="480">
          <!-- Logo Día: .COSME.® Nuevo Logo para la versión diurna -->
          <img src="assets/logo_day_dark_transparent.png" alt="Logo Cosme Alberdi" class="hero-logo-day" width="380">
        </div>"""

    new_hero_box = """        <div class="hero-logo-box">
          <!-- Logo Noche: Neón Rojo puro aislado con encendido y respiración -->
          <img src="assets/neon_cosme_isolated.png" alt="Cartel de Neón Rojo Cosme" class="hero-logo-night" width="480" title="Tocá el cartel para encender el neón">
          <!-- Logo Día: Wordmark Cosme de alta resolución -->
          <img src="assets/cosme-wordmark-black.png" alt="Logo Cosme Alberdi" class="hero-logo-day" width="380">
        </div>"""

    if old_hero_box in html:
        html = html.replace(old_hero_box, new_hero_box)
        print("Updated Hero logo box.")

    old_live_status = """        <div class="live-status">
          <span class="pulse-dot"></span>
          <span id="live-status-text">Abierto Ahora · Cierra a las 03:00 h</span>
        </div>"""

    new_live_status = """        <div class="live-status">
          <span class="pulse-dot"></span>
          <span id="live-status-text-hero">Detectando estado en vivo en Rosario...</span>
        </div>"""

    if old_live_status in html:
        html = html.replace(old_live_status, new_live_status)
        print("Updated Live Status badge in Hero.")

    # 3. Add Pizarra de Canillas Section right after WhatsApp presets section
    taps_section_html = """
    <!-- =====================================================================
         3B. PIZARRA DE CANILLAS ARTESANALES (12 TAPS EN VIVO)
         ===================================================================== -->
    <section id="canillas" class="taps-section scroll-reveal">
      <div class="container">
        <div class="taps-board">
          <div class="taps-header">
            <div class="taps-title-box">
              <div class="taps-icon-badge">🍻</div>
              <div>
                <h3>PIZARRA DE CANILLAS EN VIVO</h3>
                <span style="font-size:0.85rem; color:var(--text-muted);">Cerveza artesanal tirada a 2°C en copón enfriado</span>
              </div>
            </div>
            <div class="taps-live-badge">
              <span class="pulse-dot" style="background:#59bd95; width:8px; height:8px;"></span>
              <span>12 CANILLAS ACTIVAS HOY</span>
            </div>
          </div>

          <div class="taps-grid">
            
            <!-- Canilla 1: IPA -->
            <div class="beer-tap-card" data-beer-name="IPA Alberdi" data-beer-style="India Pale Ale">
              <span class="tap-num">TAP #01</span>
              <div>
                <h4 class="tap-beer-name">IPA Alberdi</h4>
                <span class="tap-style-tag" style="color:var(--neon-amber);">Lupulada &amp; Aromática</span>
                <div class="tap-specs">
                  <span class="tap-spec-pill">ABV 6.2%</span>
                  <span class="tap-spec-pill">IBU 55</span>
                </div>
                <p class="tap-desc">Explosión de lúpulos patagónicos con notas a pomelo rosado, pino y resina. Amargor marcado y persistente.</p>
              </div>
              <button class="btn-tap-order">
                <span>🍺</span> Pedir Pinta por WhatsApp
              </button>
            </div>

            <!-- Canilla 2: Honey -->
            <div class="beer-tap-card" data-beer-name="Honey de la Isla" data-beer-style="Honey Ale">
              <span class="tap-num">TAP #02</span>
              <div>
                <h4 class="tap-beer-name">Honey de la Isla</h4>
                <span class="tap-style-tag" style="color:#f5c042;">Suave &amp; Dulce Natural</span>
                <div class="tap-specs">
                  <span class="tap-spec-pill">ABV 5.0%</span>
                  <span class="tap-spec-pill">IBU 18</span>
                </div>
                <p class="tap-desc">Miel pura de monte de las islas del Paraná. Suavidad maltosa con final dulce y refrescante.</p>
              </div>
              <button class="btn-tap-order">
                <span>🍺</span> Pedir Pinta por WhatsApp
              </button>
            </div>

            <!-- Canilla 3: Scottish -->
            <div class="beer-tap-card" data-beer-name="Scottish Heavy" data-beer-style="Scottish Export">
              <span class="tap-num">TAP #03</span>
              <div>
                <h4 class="tap-beer-name">Scottish Heavy</h4>
                <span class="tap-style-tag" style="color:var(--terracotta);">Caramelo &amp; Malta Roja</span>
                <div class="tap-specs">
                  <span class="tap-spec-pill">ABV 5.5%</span>
                  <span class="tap-spec-pill">IBU 22</span>
                </div>
                <p class="tap-desc">Notas profundas a toffee, frutos secos y corteza de pan horneado. Cuerpo sedoso y calidez en boca.</p>
              </div>
              <button class="btn-tap-order">
                <span>🍺</span> Pedir Pinta por WhatsApp
              </button>
            </div>

            <!-- Canilla 4: Golden -->
            <div class="beer-tap-card" data-beer-name="Golden Ale Pampeana" data-beer-style="Golden Ale">
              <span class="tap-num">TAP #04</span>
              <div>
                <h4 class="tap-beer-name">Golden Pampeana</h4>
                <span class="tap-style-tag" style="color:#d4af37;">Dorada &amp; Refrescante</span>
                <div class="tap-specs">
                  <span class="tap-spec-pill">ABV 4.8%</span>
                  <span class="tap-spec-pill">IBU 15</span>
                </div>
                <p class="tap-desc">Cerveza rubia de trago ágil, espuma blanca cremosa y final limpio. La compañera perfecta para arrancar.</p>
              </div>
              <button class="btn-tap-order">
                <span>🍺</span> Pedir Pinta por WhatsApp
              </button>
            </div>

            <!-- Canilla 5: APA -->
            <div class="beer-tap-card" data-beer-name="American Pale Ale" data-beer-style="APA">
              <span class="tap-num">TAP #05</span>
              <div>
                <h4 class="tap-beer-name">APA del Bulevar</h4>
                <span class="tap-style-tag" style="color:var(--neon-amber);">Cítricos &amp; Amargor Medio</span>
                <div class="tap-specs">
                  <span class="tap-spec-pill">ABV 5.2%</span>
                  <span class="tap-spec-pill">IBU 38</span>
                </div>
                <p class="tap-desc">Equilibrio redondo entre malta cristal y lúpulos americanos. Aromas a mango, maracuyá y cáscara de naranja.</p>
              </div>
              <button class="btn-tap-order">
                <span>🍺</span> Pedir Pinta por WhatsApp
              </button>
            </div>

            <!-- Canilla 6: Stout -->
            <div class="beer-tap-card" data-beer-name="Imperial Stout Café" data-beer-style="Stout Imperial">
              <span class="tap-num">TAP #06</span>
              <div>
                <h4 class="tap-beer-name">Stout Café Cosme</h4>
                <span class="tap-style-tag" style="color:#a0725a;">Tostada &amp; Cacao Puro</span>
                <div class="tap-specs">
                  <span class="tap-spec-pill">ABV 7.0%</span>
                  <span class="tap-spec-pill">IBU 32</span>
                </div>
                <p class="tap-desc">Infusionada en frío con café de especialidad de nuestro salón. Notas a chocolate amargo y crema moka.</p>
              </div>
              <button class="btn-tap-order">
                <span>🍺</span> Pedir Pinta por WhatsApp
              </button>
            </div>

            <!-- Canilla 7: Session IPA -->
            <div class="beer-tap-card" data-beer-name="Session IPA Ligera" data-beer-style="Session IPA">
              <span class="tap-num">TAP #07</span>
              <div>
                <h4 class="tap-beer-name">Session IPA Verano</h4>
                <span class="tap-style-tag" style="color:#7ef5c8;">Ultra Tomable &amp; Aromas</span>
                <div class="tap-specs">
                  <span class="tap-spec-pill">ABV 4.2%</span>
                  <span class="tap-spec-pill">IBU 40</span>
                </div>
                <p class="tap-desc">Bajo alcohol, máxima frescura. Aromas intensos a frutas tropicales sin saturar el paladar.</p>
              </div>
              <button class="btn-tap-order">
                <span>🍺</span> Pedir Pinta por WhatsApp
              </button>
            </div>

            <!-- Canilla 8: Rotativa Invitada -->
            <div class="beer-tap-card" data-beer-name="Canilla Invitada Rotativa" data-beer-style="Especial Microcervecería">
              <span class="tap-num">TAP #08</span>
              <div>
                <h4 class="tap-beer-name">Canilla Rotativa</h4>
                <span class="tap-style-tag" style="color:var(--neon-red);">Edición Limitada</span>
                <div class="tap-specs">
                  <span class="tap-spec-pill">ABV 6.5%</span>
                  <span class="tap-spec-pill">IBU Especial</span>
                </div>
                <p class="tap-desc">Barril especial de productores invitados de Rosario y la región. Consultá qué estilo pinchamos hoy.</p>
              </div>
              <button class="btn-tap-order">
                <span>🍺</span> Consultar Pizarrón de Hoy
              </button>
            </div>

          </div>
        </div>
      </div>
    </section>
"""

    if '</section>\n\n    <!-- =====================================================================\n         4. SECCIÓN MENÚ' in html:
        html = html.replace('</section>\n\n    <!-- =====================================================================\n         4. SECCIÓN MENÚ', '</section>' + taps_section_html + '\n    <!-- =====================================================================\n         4. SECCIÓN MENÚ')
        print("Inserted Pizarra de Canillas section.")
    else:
        # try alternative anchor
        anchor = '<!-- =====================================================================\n         4. SECCIÓN MENÚ'
        if anchor in html:
            html = html.replace(anchor, taps_section_html + '\n    ' + anchor)
            print("Inserted Pizarra de Canillas before Menu section.")

    # 4. Insert Lunch Suggester into Menu Section
    lunch_suggester_html = """
        <!-- Sugeridor Interactivo de Almuerzo Ejecutivo (Visible en Modo Día) -->
        <div id="lunch-suggester-box" class="lunch-suggester scroll-reveal" style="display:none;">
          <div class="lunch-suggester-head">
            <div class="lunch-suggester-title">
              <span>🍽️</span>
              <span>Armá tu Menú Ejecutivo del Mediodía</span>
            </div>
            <div class="lunch-badge-price">Precio Fijo $9.800</div>
          </div>
          <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px;">
            Disponible de Lunes a Viernes de 12:00 a 16:00 h. Incluye plato principal abundante, bebida fresca y café espresso o postre.
          </p>
          <div class="lunch-selectors-grid">
            <div class="lunch-select-wrap">
              <label for="lunch-dish-select">1. Plato Principal</label>
              <select id="lunch-dish-select" class="lunch-select-control">
                <option value="Sorrentinos caseros con salsa rosa">Sorrentinos caseros con salsa rosa</option>
                <option value="Milanesa de ternera al plato con papas">Milanesa de ternera al plato con papas</option>
                <option value="Pechuga grillée con mix verde y tomates">Pechuga grillée con mix verde y tomates</option>
                <option value="Tarta rústica de calabaza asada y queso brie">Tarta rústica de calabaza y brie</option>
              </select>
            </div>
            <div class="lunch-select-wrap">
              <label for="lunch-drink-select">2. Bebida</label>
              <select id="lunch-drink-select" class="lunch-select-control">
                <option value="Limonada casera con menta y jengibre">Limonada con menta y jengibre</option>
                <option value="Copa de vino tinto o blanco de la casa">Copa de vino de la casa</option>
                <option value="Agua mineral con o sin gas">Agua mineral con o sin gas</option>
                <option value="Gaseosa línea clásica">Gaseosa línea clásica</option>
              </select>
            </div>
            <div class="lunch-select-wrap">
              <label for="lunch-dessert-select">3. Cierre Dulce o Café</label>
              <select id="lunch-dessert-select" class="lunch-select-control">
                <option value="Café Espresso de especialidad barista">Café Espresso Barista</option>
                <option value="Bocha de helado artesanal con praliné">Bocha de helado artesanal</option>
                <option value="Flan casero con dulce de leche">Flan casero con dulce de leche</option>
              </select>
            </div>
          </div>
          <div class="lunch-actions">
            <button id="lunch-cta-btn" class="btn-lunch-cta">
              <span>🚀</span> Pedir Menú Ejecutivo por WhatsApp
            </button>
          </div>
        </div>
"""

    if '<!-- Grid de Platos -->' in html:
        html = html.replace('<!-- Grid de Platos -->', lunch_suggester_html + '\n        <!-- Grid de Platos -->')
        print("Inserted Lunch Suggester.")

    # 5. Update Footer Brand with official Lockup and Brand Kit modal button
    old_footer_brand = """        <div class="footer-brand">
          <a href="#inicio" class="brand-logo">
            <img src="assets/cosme-logo-amber.png" alt="Cosme" width="38" height="38">
            <span class="brand-title" style="font-size:1.25rem;">COSME</span>
          </a>
          <p>
            Pub, restaurante y cervecería artesanal sobre Boulevard Rondeau. El clásico de barrio que reúne a toda la Zona Norte de Rosario.
          </p>
        </div>"""

    new_footer_brand = """        <div class="footer-brand">
          <a href="#inicio" class="footer-lockup-box" aria-label="Cosme Alberdi Inicio">
            <img src="assets/cosme-lockup-horizontal-amber.png" alt="Cosme Alberdi Gastrobar" class="footer-lockup-night" height="54">
            <img src="assets/cosme-lockup-horizontal-black.png" alt="Cosme Alberdi Gastrobar" class="footer-lockup-day" height="54">
          </a>
          <p>
            Pub, restaurante y cervecería artesanal sobre Boulevard Rondeau. El clásico de barrio que reúne a toda la Zona Norte de Rosario.
          </p>
          <button class="btn-brand-modal-trigger" data-open-modal="brand">
            🎨 Ver Identidad Visual &amp; Descargar Logos
          </button>
        </div>"""

    if old_footer_brand in html:
        html = html.replace(old_footer_brand, new_footer_brand)
        print("Updated Footer Brand with official lockup.")

    # 6. Add Brand Kit Modal at the end of the modals section
    brand_modal_html = """
  <!-- =====================================================================
       MODAL: KIT DE IDENTIDAD VISUAL Y LOGOS OFICIALES
       ===================================================================== -->
  <div id="modal-brand" class="modal-container">
    <div class="modal-backdrop"></div>
    <div class="modal-window" style="max-width:850px;">
      <div class="modal-header">
        <h3 class="modal-title">🎨 Identidad Visual &amp; Suite de Logos</h3>
        <button class="modal-close-btn" aria-label="Cerrar modal">&times;</button>
      </div>
      <p style="font-size:0.85rem; color:var(--text-muted); margin-bottom:16px;">
        Descargá los recursos oficiales de Cosme Alberdi en PNG transparente de alta definición y vectores SVG:
      </p>

      <div class="brand-gallery-grid">
        <!-- 1. Mascota Ámbar -->
        <div class="brand-card-preview">
          <img src="assets/cosme-mascot-amber.png" alt="Mascota Ámbar" loading="lazy">
          <div style="font-size:0.85rem; font-weight:700; margin-bottom:8px;">Mascota Ámbar / Birra</div>
          <div class="brand-download-links">
            <a href="brand/mascot/cosme-mascot-amber.png" download class="brand-dl-pill">PNG HD</a>
            <a href="brand/mascot/cosme-mascot.svg" download class="brand-dl-pill">SVG</a>
          </div>
        </div>

        <!-- 2. Mascota Negro -->
        <div class="brand-card-preview" style="background:#f4eee2;">
          <img src="assets/cosme-mascot-black.png" alt="Mascota Negra" loading="lazy">
          <div style="font-size:0.85rem; font-weight:700; margin-bottom:8px; color:#121212;">Mascota Tinta Negra</div>
          <div class="brand-download-links">
            <a href="brand/mascot/cosme-mascot-black.png" download class="brand-dl-pill" style="background:#121212; color:#fff;">PNG HD</a>
            <a href="brand/mascot/cosme-mascot.svg" download class="brand-dl-pill" style="background:#121212; color:#fff;">SVG</a>
          </div>
        </div>

        <!-- 3. Wordmark Ámbar -->
        <div class="brand-card-preview">
          <img src="assets/cosme-wordmark-amber.png" alt="Wordmark Ámbar" loading="lazy">
          <div style="font-size:0.85rem; font-weight:700; margin-bottom:8px;">Wordmark "COSME" Ámbar</div>
          <div class="brand-download-links">
            <a href="brand/wordmark/cosme-wordmark-amber.png" download class="brand-dl-pill">PNG 4K</a>
            <a href="brand/wordmark/cosme-wordmark.svg" download class="brand-dl-pill">SVG</a>
          </div>
        </div>

        <!-- 4. Wordmark Negro -->
        <div class="brand-card-preview" style="background:#f4eee2;">
          <img src="assets/cosme-wordmark-black.png" alt="Wordmark Negro" loading="lazy">
          <div style="font-size:0.85rem; font-weight:700; margin-bottom:8px; color:#121212;">Wordmark "COSME" Negro</div>
          <div class="brand-download-links">
            <a href="brand/wordmark/cosme-wordmark-black.png" download class="brand-dl-pill" style="background:#121212; color:#fff;">PNG 4K</a>
            <a href="brand/wordmark/cosme-wordmark.svg" download class="brand-dl-pill" style="background:#121212; color:#fff;">SVG</a>
          </div>
        </div>

        <!-- 5. Lockup Horizontal Ámbar -->
        <div class="brand-card-preview" style="grid-column: 1 / -1;">
          <img src="assets/cosme-lockup-horizontal-amber.png" alt="Lockup Completo" loading="lazy">
          <div style="font-size:0.85rem; font-weight:700; margin-bottom:8px;">Lockup Oficial Completo (Mascota + Marca)</div>
          <div class="brand-download-links">
            <a href="brand/lockup/cosme-lockup-horizontal-amber.png" download class="brand-dl-pill">PNG Ámbar</a>
            <a href="brand/lockup/cosme-lockup-horizontal-black.png" download class="brand-dl-pill">PNG Negro</a>
            <a href="brand/lockup/cosme-lockup-horizontal-white.png" download class="brand-dl-pill">PNG Blanco</a>
          </div>
        </div>
      </div>
    </div>
  </div>
"""

    if '</body>' in html:
        html = html.replace('</body>', brand_modal_html + '\n</body>')
        print("Added Brand Modal before </body>.")

    # 7. Add scroll-reveal class to main sections
    html = re.sub(r'class="whatsapp-presets-section"', r'class="whatsapp-presets-section scroll-reveal"', html)
    html = re.sub(r'class="menu-section"', r'class="menu-section scroll-reveal"', html)
    html = re.sub(r'class="bento-section"', r'class="bento-section scroll-reveal"', html)
    html = re.sub(r'class="festejos-section"', r'class="festejos-section scroll-reveal"', html)
    html = re.sub(r'class="location-section"', r'class="location-section scroll-reveal"', html)

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html successfully!")

if __name__ == '__main__':
    update_index()
