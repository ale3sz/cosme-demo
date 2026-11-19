from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Check mobile overflow
    page_m = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
    page_m.goto('http://127.0.0.1:8080/index.html')
    page_m.wait_for_timeout(500)
    
    overflow_m_night = page_m.evaluate("""() => {
        const docEl = document.documentElement;
        const body = document.body;
        const scrollW = Math.max(docEl.scrollWidth, body.scrollWidth);
        const clientW = window.innerWidth;
        
        // Find any element causing overflow
        const overflowingEls = [];
        document.querySelectorAll('*').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > clientW + 1) {
                overflowingEls.push({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className,
                    right: rect.right,
                    clientW: clientW
                });
            }
        });
        return {
            scrollW: scrollW,
            clientW: clientW,
            hasHorizontalScroll: scrollW > clientW,
            overflowingEls: overflowingEls.slice(0, 10)
        };
    }""")

    # Day mode mobile overflow
    page_m.locator('#theme-toggle-btn').click()
    page_m.wait_for_timeout(300)
    overflow_m_day = page_m.evaluate("""() => {
        const docEl = document.documentElement;
        const body = document.body;
        const scrollW = Math.max(docEl.scrollWidth, body.scrollWidth);
        const clientW = window.innerWidth;
        return {
            scrollW: scrollW,
            clientW: clientW,
            hasHorizontalScroll: scrollW > clientW
        };
    }""")

    # Check desktop overflow
    page_d = browser.new_page(viewport={"width": 1440, "height": 900})
    page_d.goto('http://127.0.0.1:8080/index.html')
    page_d.wait_for_timeout(500)
    overflow_d = page_d.evaluate("""() => {
        const docEl = document.documentElement;
        const scrollW = docEl.scrollWidth;
        const clientW = window.innerWidth;
        return {
            scrollW: scrollW,
            clientW: clientW,
            hasHorizontalScroll: scrollW > clientW
        };
    }""")

    # Check contrast and color styles in Night vs Day
    styles_audit = page_d.evaluate("""() => {
        const getStyles = (sel) => {
            const el = document.querySelector(sel);
            if (!el) return null;
            const cs = window.getComputedStyle(el);
            return {
                color: cs.color,
                bgColor: cs.backgroundColor,
                fontSize: cs.fontSize,
                fontWeight: cs.fontWeight,
                border: cs.border,
                boxShadow: cs.boxShadow
            };
        };

        const nightElements = {
            body: getStyles('body'),
            heroBadge: getStyles('.hero-top-badge, .hero-badge'),
            heroTitle: getStyles('.hero-title'),
            heroSubtitle: getStyles('.hero-subtitle'),
            quickNavCard: getStyles('.quick-nav-card'),
            menuTabActive: getStyles('.menu-mode-tab.active'),
            dishCard: getStyles('.dish-card'),
            dishTitle: getStyles('.dish-title'),
            dishPrice: getStyles('.dish-price')
        };

        return nightElements;
    }""")

    # Switch to Day and sample again
    page_d.locator('#theme-toggle-btn').click()
    page_d.wait_for_timeout(400)

    styles_audit_day = page_d.evaluate("""() => {
        const getStyles = (sel) => {
            const el = document.querySelector(sel);
            if (!el) return null;
            const cs = window.getComputedStyle(el);
            return {
                color: cs.color,
                bgColor: cs.backgroundColor,
                fontSize: cs.fontSize,
                fontWeight: cs.fontWeight,
                border: cs.border,
                boxShadow: cs.boxShadow
            };
        };

        return {
            body: getStyles('body'),
            heroBadge: getStyles('.hero-top-badge, .hero-badge'),
            heroTitle: getStyles('.hero-title'),
            heroSubtitle: getStyles('.hero-subtitle'),
            quickNavCard: getStyles('.quick-nav-card'),
            menuTabActive: getStyles('.menu-mode-tab.active'),
            dishCard: getStyles('.dish-card'),
            dishTitle: getStyles('.dish-title'),
            dishPrice: getStyles('.dish-price')
        };
    }""")

    # Check background images and brick texture
    bg_textures = page_d.evaluate("""() => {
        const hero = document.getElementById('hero') || document.querySelector('.hero');
        const root = document.documentElement;
        return {
            rootTheme: root.getAttribute('data-theme'),
            rootBgColor: window.getComputedStyle(root).backgroundColor,
            bodyBgColor: window.getComputedStyle(document.body).backgroundColor,
            bodyBgImage: window.getComputedStyle(document.body).backgroundImage
        };
    }""")

    res = {
        "overflow_mobile_night": overflow_m_night,
        "overflow_mobile_day": overflow_m_day,
        "overflow_desktop": overflow_d,
        "styles_night": styles_audit,
        "styles_day": styles_audit_day,
        "bg_textures": bg_textures
    }

    with open("audit_results/layout_and_styles_audit.json", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2)

    print("Layout & styles audit complete.")
    browser.close()
