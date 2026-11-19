import re

def fix_all():
    # 1. Update index.html to use the identical glyph pair
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    old_box = """        <div class="hero-logo-box" id="hero-logo-box" title="Cosme Alberdi — Tocá para interactuar con el neón">
          <!-- Capa 1: Logo Cafetería Diurna (Tinta negra estampada con micro-transición) -->
          <img src="assets/hero_logo_day_aligned.png" alt="Cosme Alberdi Cafetería" class="hero-logo-day" width="480">
          <!-- Capa 2: Logo Neón Nocturno (Tubos incandescentes con encendido) -->
          <img src="assets/hero_logo_night_aligned.png" alt="Cartel de Neón Rojo Cosme" class="hero-logo-night" width="480">
        </div>"""

    new_box = """        <div class="hero-logo-box" id="hero-logo-box" title="Cosme Alberdi — Tocá para interactuar con el neón">
          <!-- Logo Día: Tinta negra vintage estampada (.COSME.®) -->
          <img src="assets/cosme_wordmark_day.png" alt="Cosme Alberdi Cafetería" class="hero-logo-day" width="480">
          <!-- Logo Noche: Los mismos caracteres .COSME. transformados en tubos de neón rojo incandescente -->
          <img src="assets/cosme_wordmark_night_neon.png" alt="Cosme Alberdi Neón" class="hero-logo-night" width="480">
        </div>"""

    if old_box in html:
        html = html.replace(old_box, new_box)
        print("Replaced hero-logo-box in index.html")
    else:
        # regex replace
        pattern = r'<div class="hero-logo-box"[\s\S]*?</div>'
        html = re.sub(pattern, new_box, html, count=1)
        print("Replaced hero-logo-box via regex in index.html")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # 2. Update styles.css
    with open('styles.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Clean any old animation on .hero-logo-night around line 1250
    css = re.sub(r'\.hero-logo-night\s*\{[^}]*animation:[^}]*\}', '', css)
    css = re.sub(r'\.hero-logo-night\.neon-ignite-active\s*\{[^}]*\}', '', css)

    # Replace hero-logo block
    old_css_pattern = r'/\* Hero Logo Seamless Transition[\s\S]*?@keyframes neonQuickFlicker\s*\{[\s\S]*?\}\s*\}'
    
    new_css = """/* ==========================================================================
   HERO LOGO TRANSITION: MISMO LOGO .COSME. (CAFETERÍA TINTA ⇄ PUB NEÓN)
   ========================================================================== */
.hero-logo-box {
  margin: 0 auto 20px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 480px;
  width: 90%;
  aspect-ratio: 1200 / 380;
  cursor: pointer;
  user-select: none;
}

.hero-logo-day,
.hero-logo-night {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  will-change: opacity, transform, filter;
  transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.35s cubic-bezier(0.16, 1, 0.3, 1),
              filter 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

/* 1. ESTADO NOCHE: El neón brilla con sus tubos rojos y respira. El logo de día está COMPLETAMENTE OCULTO */
html[data-theme="night"] .hero-logo-night {
  opacity: 1 !important;
  visibility: visible !important;
  transform: scale(1);
  filter: drop-shadow(0 0 20px rgba(255, 30, 39, 0.65)) drop-shadow(0 0 6px rgba(255, 255, 255, 0.35));
  pointer-events: auto;
  animation: neonGlowBreathing 5.5s ease-in-out infinite alternate;
}

html[data-theme="night"] .hero-logo-day {
  opacity: 0 !important;
  visibility: hidden !important;
  pointer-events: none !important;
  transform: scale(0.98);
}

/* 2. ESTADO DÍA: El logo de cafetería está nítido en tinta negra. El neón está 100% APAGADO Y OCULTO */
html[data-theme="day"] .hero-logo-day {
  opacity: 1 !important;
  visibility: visible !important;
  transform: scale(1);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.08));
  pointer-events: auto;
}

html[data-theme="day"] .hero-logo-night {
  opacity: 0 !important;
  visibility: hidden !important;
  animation: none !important;
  pointer-events: none !important;
  transform: scale(1.02);
  filter: drop-shadow(0 0 0px transparent);
}

/* 3. DURANTE LA TRANSICIÓN: Se vuelven ambos visibles temporalmente para el crossfade suave */
.hero-logo-box.is-transitioning .hero-logo-day,
.hero-logo-box.is-transitioning .hero-logo-night {
  visibility: visible !important;
}

/* Ignición de Neón al pasar a Noche */
.hero-logo-box.is-igniting .hero-logo-night {
  visibility: visible !important;
  animation: neonIgniteSpark 0.40s cubic-bezier(0.2, 0.8, 0.2, 1) forwards !important;
}

@keyframes neonIgniteSpark {
  0% {
    opacity: 0.1;
    filter: drop-shadow(0 0 4px rgba(255, 30, 39, 0.2));
    transform: scale(0.98);
  }
  25% {
    opacity: 0.95;
    filter: drop-shadow(0 0 35px rgba(255, 30, 39, 0.9)) drop-shadow(0 0 10px rgba(255, 255, 255, 0.7));
    transform: scale(1.01);
  }
  45% {
    opacity: 0.45;
    filter: drop-shadow(0 0 8px rgba(255, 30, 39, 0.3));
    transform: scale(0.99);
  }
  70% {
    opacity: 1;
    filter: drop-shadow(0 0 30px rgba(255, 30, 39, 0.75));
    transform: scale(1.005);
  }
  100% {
    opacity: 1;
    filter: drop-shadow(0 0 20px rgba(255, 30, 39, 0.65)) drop-shadow(0 0 6px rgba(255, 255, 255, 0.35));
    transform: scale(1);
  }
}"""

    # Replace old section if found
    if re.search(old_css_pattern, css):
        css = re.sub(old_css_pattern, new_css, css)
        print("Replaced old hero-logo CSS with robust transition CSS!")
    else:
        # replace simple block
        simple_pattern = r'/\* Hero Logo Seamless Transition[\s\S]*?@keyframes neonQuickFlicker\s*\{[\s\S]*?\}'
        if re.search(simple_pattern, css):
            css = re.sub(simple_pattern, new_css, css)
            print("Replaced simple hero-logo pattern with robust transition CSS!")
        else:
            css += "\n" + new_css
            print("Appended robust hero-logo transition CSS!")

    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)

    # 3. Update app.js for transition classes
    with open('app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()

    # In setTheme, handle .is-transitioning and .is-igniting
    old_box_handling = """      const box = document.getElementById('hero-logo-box');
      if (box) {
        box.classList.remove('is-igniting');
        void box.offsetWidth;
        box.classList.add('is-igniting');
        setTimeout(() => box.classList.remove('is-igniting'), 450);
      }"""

    new_box_handling = """      const box = document.getElementById('hero-logo-box');
      if (box && updateMenu) {
        box.classList.add('is-transitioning');
        if (theme === 'night') {
          box.classList.add('is-igniting');
        }
        setTimeout(() => {
          box.classList.remove('is-transitioning');
          box.classList.remove('is-igniting');
        }, 400);
      }"""

    if old_box_handling in app_js:
        app_js = app_js.replace(old_box_handling, new_box_handling)
        print("Updated app.js transition logic!")

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)

if __name__ == '__main__':
    fix_all()
