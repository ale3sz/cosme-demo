import re

def apply_fix():
    # 1. Update index.html
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    old_box = r'<div class="hero-logo-box" id="hero-logo-box"[\s\S]*?</div>'
    new_box = """<div class="hero-logo-box" id="hero-logo-box" title="Cosme Alberdi — Tocá para interactuar">
          <!-- Un solo logo dinámico que transmuta entre Tinta Vintage y Neón Tubos -->
          <img id="hero-logo-display" src="assets/logo_morph/frame_3_night.png" alt="Cosme Alberdi" class="hero-logo-img neon-breathing" width="480">
        </div>"""

    html = re.sub(old_box, new_box, html, count=1)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html with single dynamic hero-logo-display!")

    # 2. Update styles.css
    with open('styles.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Clean old hero-logo styles
    old_css_pattern = r'/\* ==========================================================================\s*HERO LOGO TRANSITION[\s\S]*?@keyframes neonIgniteSpark\s*\{[\s\S]*?\}\s*\}'
    if re.search(old_css_pattern, css):
        css = re.sub(old_css_pattern, '', css)

    new_styles = """/* ==========================================================================
   HERO LOGO: UN SOLO LOGO DINÁMICO (.COSME.)
   Transmuta limpiamente sin superposiciones ni duplicados
   ========================================================================== */
.hero-logo-box {
  margin: 0 auto 20px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 480px;
  width: 90%;
  aspect-ratio: 1000 / 300;
  cursor: pointer;
  user-select: none;
}

.hero-logo-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  transition: transform 0.25s ease, filter 0.25s ease;
}

/* Respiración de Neón Nocturno */
.hero-logo-img.neon-breathing {
  filter: drop-shadow(0 0 24px rgba(255, 30, 39, 0.65)) drop-shadow(0 0 6px rgba(255, 255, 255, 0.35));
  animation: neonGlowBreathing 5.5s ease-in-out infinite alternate;
}

html[data-theme="day"] .hero-logo-img {
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.08));
  animation: none !important;
}
"""
    css += "\n" + new_styles
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Updated styles.css with clean single logo styling!")

    # 3. Update app.js
    with open('app.js', 'r', encoding='utf-8') as f:
        app_js = f.read()

    # Add morphing logic
    morph_code = """
  // =========================================================================
  // SECUENCIA DE TRANSMUTACIÓN DE LOGO (.COSME. Tinta ⇄ Neón)
  // =========================================================================
  const MORPH_FRAMES = [
    'assets/logo_morph/frame_0_day.png',
    'assets/logo_morph/frame_1_heat.png',
    'assets/logo_morph/frame_2_spark.png',
    'assets/logo_morph/frame_3_night.png'
  ];
  // Pre-carga inmediata para animación instantánea sin parpadeos
  MORPH_FRAMES.forEach(src => { const img = new Image(); img.src = src; });

  const heroLogoDisplay = document.getElementById('hero-logo-display');
  const heroLogoBox = document.getElementById('hero-logo-box');

  function morphLogo(targetMode, animate = true) {
    if (!heroLogoDisplay) return;

    if (!animate) {
      if (targetMode === 'day') {
        heroLogoDisplay.src = MORPH_FRAMES[0];
        heroLogoDisplay.classList.remove('neon-breathing');
      } else {
        heroLogoDisplay.src = MORPH_FRAMES[3];
        heroLogoDisplay.classList.add('neon-breathing');
      }
      return;
    }

    if (targetMode === 'night') {
      // Día -> Noche: Tinta -> Calentamiento -> Chispa -> Neón encendido
      heroLogoDisplay.src = MORPH_FRAMES[1];
      setTimeout(() => {
        heroLogoDisplay.src = MORPH_FRAMES[2];
        setTimeout(() => {
          heroLogoDisplay.src = MORPH_FRAMES[3];
          heroLogoDisplay.classList.add('neon-breathing');
        }, 90);
      }, 70);
    } else {
      // Noche -> Día: Neón -> Desvanecido -> Enfriamiento -> Tinta negra
      heroLogoDisplay.classList.remove('neon-breathing');
      heroLogoDisplay.src = MORPH_FRAMES[2];
      setTimeout(() => {
        heroLogoDisplay.src = MORPH_FRAMES[1];
        setTimeout(() => {
          heroLogoDisplay.src = MORPH_FRAMES[0];
        }, 70);
      }, 70);
    }
  }

  if (heroLogoBox) {
    heroLogoBox.addEventListener('click', () => {
      const current = htmlRoot.getAttribute('data-theme') || 'night';
      if (current === 'night' && heroLogoDisplay) {
        // Chispa táctil al tocar
        heroLogoDisplay.src = MORPH_FRAMES[2];
        setTimeout(() => {
          heroLogoDisplay.src = MORPH_FRAMES[3];
        }, 120);
      }
    });
  }
"""

    # Inject into app.js inside DOMContentLoaded
    # In setTheme, call morphLogo(theme, updateMenu)
    old_set_theme_call = "if (updateMenu) setMenuMode('night');"
    app_js = re.sub(r'const box = document\.getElementById\(\'hero-logo-box\'\);[\s\S]*?\}, 400\);', '', app_js)
    
    # replace setTheme calls
    app_js = app_js.replace("setTheme(initialTheme, false);", "setTheme(initialTheme, false);\n  morphLogo(initialTheme, false);")
    
    # In setTheme function
    set_theme_regex = r'function setTheme\(theme, updateMenu\) \{([\s\S]*?)\}'
    def repl_set_theme(m):
        body = m.group(1)
        # append morphLogo call
        return f"function setTheme(theme, updateMenu) {{{body}\n    morphLogo(theme, updateMenu);\n  }}"
    
    app_js = re.sub(set_theme_regex, repl_set_theme, app_js, count=1)
    
    # Append morph_code at end of DOMContentLoaded
    app_js = app_js.rstrip()
    if app_js.endswith('});'):
        app_js = app_js[:-3] + morph_code + "\n});"
    else:
        app_js += morph_code

    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(app_js)
    print("Updated app.js with morphLogo function and frame sequence!")

if __name__ == '__main__':
    apply_fix()
