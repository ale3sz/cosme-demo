import json
import os
import time
from playwright.sync_api import sync_playwright

URL = "http://127.0.0.1:8080/index.html"
OUT_DIR = "audit_results"
os.makedirs(OUT_DIR, exist_ok=True)

results = {
    "console_logs": [],
    "page_errors": [],
    "failed_requests": [],
    "network_404s": [],
    "logo_transition": {},
    "hero_audit": {},
    "menu_audit": {},
    "taps_audit": {},
    "modal_audit": {},
    "day_vs_night": {}
}

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # -------------------------------------------------------------
    # 1. DESKTOP RUN & LOGO TRANSITION BENCHMARK
    # -------------------------------------------------------------
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    page = context.new_page()

    # Listeners
    page.on("console", lambda msg: results["console_logs"].append({"type": msg.type, "text": msg.text}))
    page.on("pageerror", lambda err: results["page_errors"].append(str(err)))
    page.on("requestfailed", lambda req: results["failed_requests"].append({"url": req.url, "failure": req.failure}))
    page.on("response", lambda res: results["network_404s"].append(res.url) if res.status >= 400 else None)

    print("Navigating to", URL)
    page.goto(URL, wait_until="networkidle")
    time.sleep(1.0) # wait for bitmap preloads

    # Check canvas and ImageBitmap preload status in JS
    canvas_info = page.evaluate("""() => {
        const canvas = document.getElementById('hero-logo-canvas');
        const img = document.getElementById('hero-logo-display');
        const box = document.getElementById('hero-logo-box');
        
        return {
            canvasExists: !!canvas,
            canvasWidth: canvas ? canvas.width : null,
            canvasHeight: canvas ? canvas.height : null,
            canvasClientWidth: canvas ? canvas.clientWidth : null,
            canvasClientHeight: canvas ? canvas.clientHeight : null,
            imgExists: !!img,
            imgSrc: img ? img.src : null,
            boxExists: !!box,
            createImageBitmapSupported: typeof window.createImageBitmap === 'function'
        };
    }""")
    results["logo_transition"]["canvas_info"] = canvas_info

    # Capture initial Night mode
    page.locator("#hero-logo-box").screenshot(path=f"{OUT_DIR}/logo_01_initial_night.png")

    # Install FPS & frame timeline hook into window for the transition
    page.evaluate("""() => {
        window.__frameLog = [];
        const origDrawFrame = window.drawFrame;
        // Intercept playFrames / drawFrame if possible or listen to rAF
        let lastTime = performance.now();
        window.__rafStats = [];
        
        const monitorRaf = (t) => {
            if (window.__recordingRaf) {
                const delta = t - lastTime;
                window.__rafStats.push({ time: t, delta: delta });
            }
            lastTime = t;
            requestAnimationFrame(monitorRaf);
        };
        requestAnimationFrame(monitorRaf);
    }""")

    # TEST: Night to Day Transition
    print("Testing Night -> Day transition...")
    page.evaluate("() => { window.__recordingRaf = true; window.__rafStats = []; }")
    t0 = time.time()
    page.locator("#theme-toggle-btn").click()
    # Let animation play (~250-400ms)
    time.sleep(0.4)
    page.evaluate("() => { window.__recordingRaf = false; }")
    t_night_to_day = (time.time() - t0) * 1000

    night_to_day_stats = page.evaluate("() => window.__rafStats")
    page.locator("#hero-logo-box").screenshot(path=f"{OUT_DIR}/logo_02_settled_day.png")

    # TEST: Day to Night Transition (21 frames forward)
    print("Testing Day -> Night transition with high-speed sampling...")
    # We will sample mid frames
    # Let's see frame details
    page.evaluate("() => { window.__recordingRaf = true; window.__rafStats = []; }")
    t0 = time.time()
    page.locator("#theme-toggle-btn").click()
    
    # Capture intermediate state: 100ms in (approx frame 6-9)
    time.sleep(0.12)
    page.locator("#hero-logo-box").screenshot(path=f"{OUT_DIR}/logo_03_mid_transition_burgundy_tubes.png")
    
    # Capture arc flash / neon flare: ~200ms in (approx frame 12-15)
    time.sleep(0.10)
    page.locator("#hero-logo-box").screenshot(path=f"{OUT_DIR}/logo_04_neon_arc_flash.png")

    # Settle
    time.sleep(0.4)
    page.evaluate("() => { window.__recordingRaf = false; }")
    t_day_to_night = (time.time() - t0) * 1000

    day_to_night_stats = page.evaluate("() => window.__rafStats")
    page.locator("#hero-logo-box").screenshot(path=f"{OUT_DIR}/logo_05_settled_night_double_neon.png")

    # Calculate FPS and deltas
    def analyze_raf(stats):
        if not stats or len(stats) < 2:
            return {"count": len(stats), "avg_fps": 0, "max_delta_ms": 0, "dropped_frames": 0}
        deltas = [s["delta"] for s in stats[1:]] # skip first
        avg_delta = sum(deltas) / len(deltas)
        avg_fps = 1000.0 / avg_delta if avg_delta > 0 else 0
        max_delta = max(deltas)
        # dropped frame: delta > 30ms (for 60Hz)
        dropped = sum(1 for d in deltas if d > 32)
        return {
            "frames_recorded": len(stats),
            "avg_delta_ms": round(avg_delta, 2),
            "avg_fps": round(avg_fps, 1),
            "max_delta_ms": round(max_delta, 2),
            "dropped_frames": dropped
        }

    results["logo_transition"]["night_to_day"] = {
        "duration_ms": round(t_night_to_day, 1),
        "raf_analysis": analyze_raf(night_to_day_stats)
    }
    results["logo_transition"]["day_to_night"] = {
        "duration_ms": round(t_day_to_night, 1),
        "raf_analysis": analyze_raf(day_to_night_stats)
    }

    # -------------------------------------------------------------
    # FASE 2: AUDITORÍA INTEGRAL DE LA PÁGINA
    # -------------------------------------------------------------

    # Full page screenshots Desktop
    page.screenshot(path=f"{OUT_DIR}/page_desktop_night.png", full_page=True)
    page.locator("#theme-toggle-btn").click()
    time.sleep(0.4)
    page.screenshot(path=f"{OUT_DIR}/page_desktop_day.png", full_page=True)
    # Return to night mode
    page.locator("#theme-toggle-btn").click()
    time.sleep(0.4)

    # 1. Hero Audit
    hero_data = page.evaluate("""() => {
        const hero = document.getElementById('hero') || document.querySelector('.hero');
        const badges = Array.from(document.querySelectorAll('.hero-badge, .badge, [class*=\"badge\"]')).map(b => ({
            text: b.innerText.trim(),
            rect: b.getBoundingClientRect()
        }));
        const btnWp = document.querySelector('a[href*=\"whatsapp\"], a[href*=\"wa.me\"], .btn-whatsapp');
        const btnRes = document.querySelector('[data-modal=\"reserva\"], [href*=\"reserva\"], .btn-reserve, #btn-reserva, #btn-open-reserva');
        const liveStatus = document.querySelector('#live-status-pill, .live-status, [class*=\"live-status\"]');

        return {
            heroExists: !!hero,
            badges: badges,
            btnWhatsApp: btnWp ? { text: btnWp.innerText.trim(), href: btnWp.getAttribute('href'), rect: btnWp.getBoundingClientRect() } : null,
            btnReserva: btnRes ? { text: btnRes.innerText.trim(), id: btnRes.id, rect: btnRes.getBoundingClientRect() } : null,
            liveStatus: liveStatus ? { text: liveStatus.innerText.trim(), rect: liveStatus.getBoundingClientRect() } : null
        };
    }""")
    results["hero_audit"] = hero_data

    # 2. Menu & Tabs Audit
    menu_data = page.evaluate("""() => {
        const tabs = Array.from(document.querySelectorAll('.menu-mode-tab')).map(t => ({
            text: t.innerText.trim(),
            target: t.getAttribute('data-menu-target'),
            active: t.classList.contains('active')
        }));
        const dishesDay = Array.from(document.querySelectorAll('.dish-day')).map(d => ({
            title: d.querySelector('h3, .dish-title, font, strong')?.innerText.trim() || d.innerText.split('\\n')[0],
            visible: d.offsetParent !== null
        }));
        const dishesNight = Array.from(document.querySelectorAll('.dish-night')).map(d => ({
            title: d.querySelector('h3, .dish-title, font, strong')?.innerText.trim() || d.innerText.split('\\n')[0],
            visible: d.offsetParent !== null
        }));
        return {
            tabs: tabs,
            totalDishesDay: dishesDay.length,
            visibleDishesDay: dishesDay.filter(d => d.visible).length,
            totalDishesNight: dishesNight.length,
            visibleDishesNight: dishesNight.filter(d => d.visible).length
        };
    }""")
    results["menu_audit"]["initial_night"] = menu_data

    # Click Almuerzo / Day tab
    tab_day = page.locator('.menu-mode-tab[data-menu-target="day"]')
    if tab_day.count() > 0:
        tab_day.click()
        time.sleep(0.3)
        menu_day_data = page.evaluate("""() => {
            const dishesDay = Array.from(document.querySelectorAll('.dish-day')).map(d => ({ visible: d.offsetParent !== null }));
            const dishesNight = Array.from(document.querySelectorAll('.dish-night')).map(d => ({ visible: d.offsetParent !== null }));
            return {
                visibleDishesDay: dishesDay.filter(d => d.visible).length,
                visibleDishesNight: dishesNight.filter(d => d.visible).length
            };
        }""")
        results["menu_audit"]["after_click_day_tab"] = menu_day_data

    # Return to night tab
    tab_night = page.locator('.menu-mode-tab[data-menu-target="night"]')
    if tab_night.count() > 0:
        tab_night.click()
        time.sleep(0.3)

    # 3. 12 Canillas Board Audit
    taps_data = page.evaluate("""() => {
        const board = document.getElementById('canillas');
        const tapCards = Array.from(document.querySelectorAll('.tap-card, [data-tap]')).map(c => {
            const name = c.querySelector('.tap-name, h4, h3')?.innerText.trim();
            const style = c.querySelector('.tap-style, .style-tag')?.innerText.trim();
            const price = c.querySelector('.tap-price, .price')?.innerText.trim();
            const btn = c.querySelector('button, a');
            return {
                name: name,
                style: style,
                price: price,
                hasActionBtn: !!btn,
                btnText: btn ? btn.innerText.trim() : null
            };
        });
        return {
            boardExists: !!board,
            totalTaps: tapCards.length,
            taps: tapCards
        };
    }""")
    results["taps_audit"] = taps_data

    # 4. Modales Audit
    modal_data = page.evaluate("""() => {
        const modals = Array.from(document.querySelectorAll('.modal, [id*=\"modal\"], [role=\"dialog\"]')).map(m => ({
            id: m.id,
            className: m.className,
            isVisible: m.offsetParent !== null || window.getComputedStyle(m).display !== 'none' && window.getComputedStyle(m).visibility !== 'hidden'
        }));
        return modals;
    }""")
    results["modal_audit"]["initial_modals"] = modal_data

    # Test open reservation modal
    res_btn = page.locator('[data-open-modal="reserva"], #btn-reserva, a[href="#modal-reserva"], button:has-text("Reservar")').first
    if res_btn.count() > 0:
        print("Testing Reservation modal trigger...")
        res_btn.click()
        time.sleep(0.4)
        page.screenshot(path=f"{OUT_DIR}/modal_reserva_open.png")
        modal_open_state = page.evaluate("""() => {
            const m = document.getElementById('modal-reserva') || document.querySelector('.modal-reserva, [role=\"dialog\"]');
            const closeBtn = m ? m.querySelector('.modal-close, button[aria-label*=\"Cerrar\"], [data-close-modal]') : null;
            return {
                isOpen: m ? (window.getComputedStyle(m).display !== 'none' && window.getComputedStyle(m).opacity !== '0') : false,
                hasCloseBtn: !!closeBtn
            };
        }""")
        results["modal_audit"]["reserva_open_test"] = modal_open_state

        # Close modal
        close_btn = page.locator('#modal-reserva .modal-close, #modal-reserva button[aria-label*="Cerrar"], [data-close-modal]').first
        if close_btn.count() > 0:
            close_btn.click()
            time.sleep(0.3)
        else:
            page.keyboard.press("Escape")
            time.sleep(0.3)

    # Test open carta digital modal
    carta_btn = page.locator('button:has-text("Ver Carta"), a:has-text("Ver Carta"), [data-open-modal="carta"]').first
    if carta_btn.count() > 0:
        print("Testing Carta Digital modal trigger...")
        carta_btn.click()
        time.sleep(0.4)
        page.screenshot(path=f"{OUT_DIR}/modal_carta_open.png")
        carta_open_state = page.evaluate("""() => {
            const m = document.getElementById('modal-carta') || document.querySelector('.modal-carta');
            return {
                isOpen: m ? (window.getComputedStyle(m).display !== 'none') : false
            };
        }""")
        results["modal_audit"]["carta_open_test"] = carta_open_state
        page.keyboard.press("Escape")
        time.sleep(0.3)

    # 5. Mobile Run (390x844 - iPhone 14 / modern standard)
    context_mobile = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    page_mobile = context_mobile.new_page()
    page_mobile.goto(URL, wait_until="networkidle")
    time.sleep(0.5)

    # Screenshots Mobile
    page_mobile.screenshot(path=f"{OUT_DIR}/page_mobile_night.png", full_page=True)
    page_mobile.locator("#theme-toggle-btn").click()
    time.sleep(0.4)
    page_mobile.screenshot(path=f"{OUT_DIR}/page_mobile_day.png", full_page=True)

    browser.close()

with open(f"{OUT_DIR}/audit_summary.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Comprehensive QA completed! Report saved to audit_results/audit_summary.json")
