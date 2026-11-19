from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://127.0.0.1:8080/index.html')
    
    taps = page.evaluate("""() => {
        const cards = Array.from(document.querySelectorAll('.beer-tap-card'));
        return cards.map(c => ({
            num: c.querySelector('.tap-num')?.innerText.trim(),
            name: c.querySelector('.tap-beer-name')?.innerText.trim(),
            style: c.querySelector('.tap-style-tag')?.innerText.trim(),
            specs: c.querySelector('.tap-specs')?.innerText.trim(),
            desc: c.querySelector('.tap-desc')?.innerText.trim(),
            hasBtn: !!c.querySelector('.btn-tap-order'),
            btnText: c.querySelector('.btn-tap-order')?.innerText.trim()
        }));
    }""")
    print(f"Total beer tap cards found: {len(taps)}")
    for t in taps:
        print(f"{t['num']}: {t['name']} ({t['style']}) - {t['specs']} | Button: {t['btnText']}")
    
    # Also test clicking a tap order button
    tap_btn = page.locator('.btn-tap-order').first
    href_or_click = tap_btn.get_attribute('href')
    onclick = tap_btn.get_attribute('onclick')
    print(f"Tap button 1 attributes: href={href_or_click}, onclick={onclick}")
    
    # Test modal carta open
    carta_btn = page.locator('[data-open-pdf="noche"]').first
    carta_btn.click()
    page.wait_for_timeout(500)
    
    modal_carta_state = page.evaluate("""() => {
        const m = document.getElementById('modal-carta');
        const iframe = document.getElementById('pdf-frame');
        return {
            hasActive: m.classList.contains('active'),
            display: window.getComputedStyle(m).display,
            visibility: window.getComputedStyle(m).visibility,
            opacity: window.getComputedStyle(m).opacity,
            iframeSrc: iframe ? iframe.src : null
        };
    }""")
    print("Modal carta state after click:", modal_carta_state)

    browser.close()
