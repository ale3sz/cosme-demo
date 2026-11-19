import re

def update_transition():
    # 1. Update index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    old_logo_box = """        <div class="hero-logo-box">
          <!-- Logo Noche: Neón Rojo puro aislado con encendido y respiración -->
          <img src="assets/neon_cosme_isolated.png" alt="Cartel de Neón Rojo Cosme" class="hero-logo-night" width="480" title="Tocá el cartel para encender el neón">
          <!-- Logo Día: Wordmark Cosme de alta resolución -->
          <img src="assets/cosme-wordmark-black.png" alt="Logo Cosme Alberdi" class="hero-logo-day" width="380">
        </div>"""

    new_logo_box = """        <div class="hero-logo-box" id="hero-logo-box" title="Cosme Alberdi — Tocá para interactuar con el neón">
          <!-- Capa 1: Logo Cafetería Diurna (Tinta negra estampada con micro-transición) -->
          <img src="assets/hero_logo_day_aligned.png" alt="Cosme Alberdi Cafetería" class="hero-logo-day" width="480">
          <!-- Capa 2: Logo Neón Nocturno (Tubos incandescentes con encendido) -->
          <img src="assets/hero_logo_night_aligned.png" alt="Cartel de Neón Rojo Cosme" class="hero-logo-night" width="480">
        </div>"""

    if old_logo_box in html:
        html = html.replace(old_logo_box, new_logo_box)
        print("Updated hero-logo-box in index.html!")
    else:
        # regex replace
        pattern = r'<div class="hero-logo-box">[\s\S]*?</div>'
        html = re.sub(pattern, new_logo_box, html, count=1)
        print("Replaced hero-logo-box via regex in index.html!")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

    # 2. Update styles.css
    with open('styles.css', 'r', encoding='utf-8') as f:
        css = f.read()

    old_hero_logo_css = """/* Hero Logo Switching (Neón en Noche / Stamped .COSME.® en Día) */
.hero-logo-box {
  margin: 0 auto 24px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 140px;
}
.hero-logo-night {
  max-width: 480px;
  width: 90%;
  height: auto;
  filter: drop-shadow(0 0 35px var(--neon-red-glow));
  transition: filter 0.3s ease;
}
.hero-logo-day {
  max-width: 380px;
  width: 85%;
  height: auto;
  transition: transform 0.3s ease;
}

html[data-theme="night"] .hero-logo-night { display: block; }
html[data-theme="night"] .hero-logo-day { display: none; }

html[data-theme="day"] .hero-logo-night { display: none; }
html[data-theme="day"] .hero-logo-day { display: block; }"""

    new_hero_logo_css = """/* Hero Logo Seamless Transition (Cafetería Stamped ⇄ Neón Tubes) */
.hero-logo-box {
  margin: 0 auto 20px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 480px;
  width: 90%;
  aspect-ratio: 1100 / 360;
  cursor: pointer;
  user-select: none;
}

.hero-logo-night,
.hero-logo-day {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: contain;
  will-change: opacity, transform, filter;
  transition: opacity 0.38s cubic-bezier(0.16, 1, 0.3, 1),
              transform 0.38s cubic-bezier(0.16, 1, 0.3, 1),
              filter 0.38s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Modo Noche: Neón encendido y respirando, logo día se desvanece con aura cálida */
html[data-theme="night"] .hero-logo-night {
  opacity: 1;
  transform: scale(1);
  filter: drop-shadow(0 0 28px rgba(255, 30, 39, 0.65)) drop-shadow(0 0 8px rgba(255, 255, 255, 0.35));
  pointer-events: auto;
}

html[data-theme="night"] .hero-logo-day {
  opacity: 0;
  transform: scale(0.97);
  filter: drop-shadow(0 0 14px rgba(255, 30, 39, 0.85)) blur(1px);
  pointer-events: none;
}

/* Modo Día: Logo Cafetería nítido y sólido, Neón apagado sin voltaje */
html[data-theme="day"] .hero-logo-day {
  opacity: 1;
  transform: scale(1);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.08));
  pointer-events: auto;
}

html[data-theme="day"] .hero-logo-night {
  opacity: 0;
  transform: scale(1.03);
  filter: drop-shadow(0 0 0px transparent);
  pointer-events: none;
}

/* Animación de Ignición Rápida al cambiar a Noche */
.hero-logo-box.is-igniting .hero-logo-night {
  animation: neonQuickFlicker 0.42s cubic-bezier(0.2, 0.8, 0.2, 1) forwards !important;
}

@keyframes neonQuickFlicker {
  0% {
    opacity: 0.15;
    filter: drop-shadow(0 0 4px rgba(255, 30, 39, 0.2));
    transform: scale(0.97);
  }
  20% {
    opacity: 0.95;
    filter: drop-shadow(0 0 35px rgba(255, 30, 39, 0.85)) drop-shadow(0 0 10px rgba(255, 255, 255, 0.6));
    transform: scale(1.02);
  }
  35% {
    opacity: 0.4;
    filter: drop-shadow(0 0 8px rgba(255, 30, 39, 0.3));
    transform: scale(0.99);
  }
  60% {
    opacity: 1;
    filter: drop-shadow(0 0 32px rgba(255, 30, 39, 0.75));
    transform: scale(1.01);
  }
  100% {
    opacity: 1;
    filter: drop-shadow(0 0 28px rgba(255, 30, 39, 0.65)) drop-shadow(0 0 8px rgba(255, 255, 255, 0.35));
    transform: scale(1);
  }
}"""

    if old_hero_logo_css in css:
        css = css.replace(old_hero_logo_css, new_hero_logo_css)
        print("Updated hero-logo styles in styles.css!")
    else:
        # replace any remaining display: none/block for hero logo
        css = re.sub(r'html\[data-theme="night"\] \.hero-logo-night \{ display: [^;]+; \}', '', css)
        css = re.sub(r'html\[data-theme="night"\] \.hero-logo-day \{ display: [^;]+; \}', '', css)
        css = re.sub(r'html\[data-theme="day"\] \.hero-logo-night \{ display: [^;]+; \}', '', css)
        css = re.sub(r'html\[data-theme="day"\] \.hero-logo-day \{ display: [^;]+; \}', '', css)
        css += "\n" + new_hero_logo_css
        print("Appended new hero-logo styles to styles.css!")

    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)

    # 3. Update app.js for seamless ignition triggering
    with open('app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()

    # In setTheme, trigger is-igniting class on logo box
    set_theme_target = "if (updateMenu) setMenuMode('night');"
    set_theme_replacement = """if (updateMenu) setMenuMode('night');
      const box = document.getElementById('hero-logo-box');
      if (box) {
        box.classList.remove('is-igniting');
        void box.offsetWidth;
        box.classList.add('is-igniting');
        setTimeout(() => box.classList.remove('is-igniting'), 450);
      }"""

    if set_theme_target in app_js:
        app_js = app_js.replace(set_theme_target, set_theme_replacement)
        print("Updated app.js setTheme logic for logo ignition!")

    # Update click on logo box
    old_neon_click = """  const heroNeonSign = document.querySelector('.hero-logo-night');
  if (heroNeonSign) {
    heroNeonSign.addEventListener('click', () => {
      heroNeonSign.classList.remove('neon-ignite-active');
      void heroNeonSign.offsetWidth; // Forzar reflow
      heroNeonSign.classList.add('neon-ignite-active');
    });
  }"""

    new_neon_click = """  const heroLogoBox = document.getElementById('hero-logo-box');
  if (heroLogoBox) {
    heroLogoBox.addEventListener('click', () => {
      const current = htmlRoot.getAttribute('data-theme') || 'night';
      if (current === 'night') {
        heroLogoBox.classList.remove('is-igniting');
        void heroLogoBox.offsetWidth;
        heroLogoBox.classList.add('is-igniting');
        setTimeout(() => heroLogoBox.classList.remove('is-igniting'), 450);
      }
    });
  }"""

    if old_neon_click in app_js:
        app_js = app_js.replace(old_neon_click, new_neon_click)
        print("Updated app.js hero logo click listener!")

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)

if __name__ == '__main__':
    update_transition()
