import re

def update_styles():
    with open('styles.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # 1. Update body and background to feel like the camera descending a continuous brick wall
    old_body_block = """body {
  font-family: var(--font-body);
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.6;
  transition: var(--transition-theme);
  overflow-x: hidden;
  position: relative;
  min-height: 100vh;
}

/* Textura sutil de fondo de ladrillo - sin decoraciones a los costados */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background-image: url('assets/seamless_brick_tile.jpg');
  background-size: 800px auto;
  opacity: 0.15;
  pointer-events: none;
  z-index: -2;
  transition: opacity 0.35s ease;
}

html[data-theme="day"] body::before {
  opacity: 0.04;
}"""

    new_body_block = """body {
  font-family: var(--font-body);
  background-color: var(--bg-main);
  color: var(--text-main);
  line-height: 1.6;
  transition: var(--transition-theme);
  overflow-x: hidden;
  position: relative;
  min-height: 100vh;
  /* Cámara recorriendo la pared de ladrillos continuos de arriba a abajo */
  background-image: 
    radial-gradient(ellipse 950px 520px at 50% 280px, rgba(255, 30, 39, 0.18), transparent 72%),
    radial-gradient(ellipse 850px 600px at 50% 1250px, rgba(255, 170, 0, 0.09), transparent 75%),
    radial-gradient(ellipse 950px 650px at 50% 2600px, rgba(255, 30, 39, 0.07), transparent 75%),
    linear-gradient(180deg, rgba(12, 13, 16, 0.74) 0%, rgba(12, 13, 16, 0.85) 15%, rgba(12, 13, 16, 0.82) 65%, rgba(12, 13, 16, 0.94) 100%),
    url('assets/seamless_brick_tile.jpg');
  background-repeat: no-repeat, no-repeat, no-repeat, no-repeat, repeat-y;
  background-size: 100% auto, 100% auto, 100% auto, 100% 100%, 1050px auto;
  background-position: top center, top center, top center, top center, top center;
  background-attachment: scroll;
}

/* Fondo continuo en Modo Día: iluminación cálida de café boutique */
html[data-theme="day"] body {
  background-color: #f7f4ee;
  background-image: 
    radial-gradient(ellipse 950px 500px at 50% 260px, rgba(212, 140, 70, 0.12), transparent 70%),
    radial-gradient(ellipse 850px 600px at 50% 1200px, rgba(40, 128, 98, 0.06), transparent 75%),
    linear-gradient(180deg, rgba(247, 244, 238, 0.88) 0%, rgba(247, 244, 238, 0.92) 20%, rgba(247, 244, 238, 0.90) 70%, rgba(247, 244, 238, 0.96) 100%),
    url('assets/seamless_brick_tile.jpg');
  background-repeat: no-repeat, no-repeat, no-repeat, repeat-y;
  background-size: 100% auto, 100% auto, 100% 100%, 1050px auto;
  background-position: top center, top center, top center, top center;
  background-attachment: scroll;
}"""

    if old_body_block in css:
        css = css.replace(old_body_block, new_body_block)
        print("Replaced body background successfully.")
    else:
        print("Warning: old_body_block not found exactly, will check regex.")

    # 2. Add Neon Ignition and Breathing Animation Keyframes and Enhancements
    extra_styles = """
/* ==========================================================================
   ANIMACIONES VIVAS: NEÓN REALISTA, CANILLAS Y SCROLL REVEAL
   ========================================================================== */

/* 1. Encendido con chispa y parpadeo de tubo fluorescente */
@keyframes neonIgnition {
  0% {
    opacity: 0.1;
    filter: drop-shadow(0 0 2px rgba(255, 30, 39, 0.1));
  }
  8% {
    opacity: 0.85;
    filter: drop-shadow(0 0 25px rgba(255, 30, 39, 0.6));
  }
  14% {
    opacity: 0.2;
    filter: drop-shadow(0 0 4px rgba(255, 30, 39, 0.15));
  }
  22% {
    opacity: 0.95;
    filter: drop-shadow(0 0 35px rgba(255, 30, 39, 0.7));
  }
  30% {
    opacity: 0.55;
    filter: drop-shadow(0 0 15px rgba(255, 30, 39, 0.35));
  }
  42% {
    opacity: 1;
    filter: drop-shadow(0 0 42px rgba(255, 30, 39, 0.75));
  }
  100% {
    opacity: 1;
    filter: drop-shadow(0 0 38px rgba(255, 30, 39, 0.65));
  }
}

/* Respiración continua y cálida del cartel de neón */
@keyframes neonGlowBreathing {
  0% {
    filter: drop-shadow(0 0 32px rgba(255, 30, 39, 0.55)) drop-shadow(0 0 8px rgba(255, 255, 255, 0.3));
  }
  50% {
    filter: drop-shadow(0 0 44px rgba(255, 30, 39, 0.72)) drop-shadow(0 0 12px rgba(255, 255, 255, 0.45));
  }
  100% {
    filter: drop-shadow(0 0 32px rgba(255, 30, 39, 0.55)) drop-shadow(0 0 8px rgba(255, 255, 255, 0.3));
  }
}

.hero-logo-night {
  animation: neonIgnition 1.6s cubic-bezier(0.2, 0.8, 0.2, 1) forwards, neonGlowBreathing 5.5s ease-in-out 1.6s infinite alternate;
  cursor: pointer;
  user-select: none;
}

.hero-logo-night.neon-ignite-active {
  animation: neonIgnition 1.2s cubic-bezier(0.2, 0.8, 0.2, 1) forwards, neonGlowBreathing 5.5s ease-in-out 1.2s infinite alternate !important;
}

/* 2. Micro-animaciones en Scroll (Scroll-Reveal) */
.scroll-reveal {
  opacity: 0;
  transform: translateY(28px);
  transition: opacity 0.7s cubic-bezier(0.16, 1, 0.3, 1), transform 0.7s cubic-bezier(0.16, 1, 0.3, 1);
  will-change: opacity, transform;
}

.scroll-reveal.revealed {
  opacity: 1;
  transform: translateY(0);
}

.delay-1 { transition-delay: 0.1s; }
.delay-2 { transition-delay: 0.2s; }
.delay-3 { transition-delay: 0.3s; }
.delay-4 { transition-delay: 0.4s; }

/* 3. SECCIÓN PIZARRA DE CANILLAS ARTESANALES (#canillas) */
.taps-section {
  padding: 80px 0;
  position: relative;
}

.taps-board {
  background: rgba(18, 20, 26, 0.88);
  border: 1px solid rgba(255, 170, 0, 0.25);
  border-radius: 16px;
  padding: 36px 32px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px rgba(255, 170, 0, 0.05);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  transition: var(--transition-theme);
}

html[data-theme="day"] .taps-board {
  background: rgba(255, 255, 255, 0.92);
  border-color: rgba(200, 109, 81, 0.25);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.08);
}

.taps-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 28px;
  padding-bottom: 20px;
  border-bottom: 1px dashed rgba(255, 255, 255, 0.12);
}

html[data-theme="day"] .taps-header {
  border-bottom-color: rgba(0, 0, 0, 0.1);
}

.taps-title-box {
  display: flex;
  align-items: center;
  gap: 14px;
}

.taps-icon-badge {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 170, 0, 0.15);
  border: 1px solid rgba(255, 170, 0, 0.35);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.taps-title-box h3 {
  font-family: var(--font-heading);
  font-size: 1.6rem;
  letter-spacing: 0.03em;
  margin: 0;
  color: var(--text-main);
}

.taps-live-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: rgba(40, 128, 98, 0.2);
  border: 1px solid var(--hop-mint);
  color: #7ef5c8;
  padding: 6px 14px;
  border-radius: 20px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 700;
}

html[data-theme="day"] .taps-live-badge {
  background: rgba(40, 128, 98, 0.1);
  color: #1e6b50;
  border-color: #288062;
}

.taps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 18px;
}

.beer-tap-card {
  background: rgba(28, 30, 38, 0.9);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all 0.25s ease;
  cursor: pointer;
}

.beer-tap-card:hover, .beer-tap-card.tap-selected {
  transform: translateY(-4px);
  border-color: rgba(255, 170, 0, 0.5);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.4), 0 0 18px rgba(255, 170, 0, 0.15);
}

html[data-theme="day"] .beer-tap-card {
  background: #fdfbf7;
  border-color: rgba(0, 0, 0, 0.08);
}

html[data-theme="day"] .beer-tap-card:hover, html[data-theme="day"] .beer-tap-card.tap-selected {
  border-color: var(--terracotta);
  box-shadow: 0 8px 20px rgba(200, 109, 81, 0.15);
}

.tap-num {
  position: absolute;
  top: 14px;
  right: 16px;
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 800;
  color: var(--neon-amber);
  background: rgba(255, 170, 0, 0.12);
  padding: 3px 8px;
  border-radius: 6px;
}

.tap-beer-name {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  color: var(--text-main);
  margin: 0 0 4px;
}

.tap-style-tag {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  letter-spacing: 0.04em;
  margin-bottom: 10px;
}

.tap-specs {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.tap-spec-pill {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.05);
  padding: 3px 8px;
  border-radius: 4px;
  color: var(--text-muted);
}

html[data-theme="day"] .tap-spec-pill {
  background: rgba(0, 0, 0, 0.05);
}

.tap-desc {
  font-size: 0.85rem;
  color: var(--text-muted);
  line-height: 1.45;
  margin-bottom: 16px;
  flex-grow: 1;
}

.btn-tap-order {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  width: 100%;
  padding: 10px;
  border-radius: 8px;
  background: rgba(255, 170, 0, 0.12);
  border: 1px solid rgba(255, 170, 0, 0.3);
  color: var(--neon-amber);
  font-weight: 700;
  font-size: 0.82rem;
  transition: all 0.2s ease;
}

.btn-tap-order:hover {
  background: var(--neon-amber);
  color: #0c0d10;
  box-shadow: 0 0 12px rgba(255, 170, 0, 0.4);
}

/* 4. SUGERIDOR DE ALMUERZO EJECUTIVO (#lunch-suggester-box) */
.lunch-suggester {
  margin: 36px 0;
  background: rgba(28, 30, 38, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-left: 4px solid var(--hop-mint);
  border-radius: 12px;
  padding: 28px;
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
}

html[data-theme="day"] .lunch-suggester {
  background: #ffffff;
  border-color: rgba(0, 0, 0, 0.08);
  border-left: 4px solid var(--terracotta);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
}

.lunch-suggester-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 20px;
}

.lunch-suggester-title {
  font-family: var(--font-heading);
  font-size: 1.35rem;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 10px;
}

.lunch-badge-price {
  font-family: var(--font-mono);
  font-size: 1.15rem;
  font-weight: 800;
  color: #fff;
  background: var(--terracotta);
  padding: 4px 12px;
  border-radius: 6px;
}

.lunch-selectors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.lunch-select-wrap label {
  display: block;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 6px;
  letter-spacing: 0.03em;
}

.lunch-select-control {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: var(--text-main);
  font-family: inherit;
  font-size: 0.9rem;
}

html[data-theme="day"] .lunch-select-control {
  background: #f7f4ee;
  border-color: rgba(0, 0, 0, 0.15);
}

.lunch-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-lunch-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #1b7a43;
  color: #fff;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
  transition: all 0.2s ease;
}

.btn-lunch-cta:hover {
  background: #208e4e;
  box-shadow: 0 4px 14px rgba(27, 122, 67, 0.35);
}

/* 5. FOOTER LOCKUP & BRAND SHOWCASE */
.footer-lockup-box {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;
}

.footer-lockup-night { display: block; }
.footer-lockup-day { display: none; }

html[data-theme="day"] .footer-lockup-night { display: none; }
html[data-theme="day"] .footer-lockup-day { display: block; }

.btn-brand-modal-trigger {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--neon-amber);
  margin-top: 8px;
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid rgba(255, 170, 0, 0.25);
  background: rgba(255, 170, 0, 0.06);
  transition: all 0.2s ease;
}

.btn-brand-modal-trigger:hover {
  background: rgba(255, 170, 0, 0.15);
  border-color: var(--neon-amber);
}

/* Modal Brand Gallery */
.brand-gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 20px;
}

.brand-card-preview {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  padding: 16px;
  text-align: center;
}

.brand-card-preview img {
  max-height: 120px;
  margin: 0 auto 12px;
  object-fit: contain;
}

.brand-download-links {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.brand-dl-pill {
  font-size: 0.75rem;
  padding: 4px 8px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-main);
  text-decoration: none;
  font-weight: 600;
}

.brand-dl-pill:hover {
  background: var(--neon-amber);
  color: #0c0d10;
}
"""

    css = css + "\n" + extra_styles
    with open('styles.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Enhanced styles.css successfully!")

if __name__ == '__main__':
    update_styles()
