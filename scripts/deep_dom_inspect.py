import json
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:8080/index.html')
    
    hero_links = page.evaluate("""() => {
        const hero = document.getElementById('hero') || document.querySelector('.hero');
        if (!hero) return [];
        return Array.from(hero.querySelectorAll('a, button')).map(el => ({
            tag: el.tagName,
            text: el.innerText.replace(/\\s+/g, ' ').trim(),
            href: el.getAttribute('href'),
            class: el.className,
            id: el.id
        }));
    }""")
    print("--- HERO LINKS ---")
    print(json.dumps(hero_links, indent=2, ensure_ascii=False))

    canillas_info = page.evaluate("""() => {
        const can = document.getElementById('canillas');
        if (!can) return 'No #canillas';
        const cards = Array.from(can.querySelectorAll('[class*=\"canilla\"], [class*=\"tap\"], [class*=\"item\"], tr, article, li'));
        return {
            id: can.id,
            className: can.className,
            sampleCards: cards.slice(0, 15).map(c => ({ tag: c.tagName, class: c.className, text: c.innerText.slice(0, 60).replace(/\\s+/g, ' ') })),
            rawTextPreview: can.innerText.slice(0, 400).replace(/\\s+/g, ' ')
        };
    }""")
    print("--- CANILLAS INFO ---")
    print(json.dumps(canillas_info, indent=2, ensure_ascii=False))

    carta_triggers = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('a, button')).filter(el => 
            (el.innerText && el.innerText.toLowerCase().includes('carta')) ||
            (el.getAttribute('onclick') && el.getAttribute('onclick').includes('carta')) ||
            (el.getAttribute('data-open-modal') === 'carta')
        );
        return btns.map(b => ({ tag: b.tagName, text: b.innerText.replace(/\\s+/g, ' ').trim(), onclick: b.getAttribute('onclick'), href: b.getAttribute('href'), id: b.id, class: b.className }));
    }""")
    print("--- CARTA TRIGGERS ---")
    print(json.dumps(carta_triggers, indent=2, ensure_ascii=False))

    # Also check modal carta implementation in JS / HTML
    modal_carta_html = page.evaluate("""() => {
        const m = document.getElementById('modal-carta');
        return m ? m.outerHTML.slice(0, 1000) : 'Not found';
    }""")
    print("--- MODAL CARTA OUTER HTML ---")
    print(modal_carta_html[:500])

    # Check modal-reserva implementation in JS / HTML
    modal_res_html = page.evaluate("""() => {
        const m = document.getElementById('modal-reserva');
        return m ? m.outerHTML.slice(0, 1000) : 'Not found';
    }""")
    print("--- MODAL RESERVA OUTER HTML ---")
    print(modal_res_html[:500])

    browser.close()
