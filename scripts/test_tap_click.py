from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    
    errors = []
    page.on('pageerror', lambda e: errors.append(str(e)))
    
    page.goto('http://127.0.0.1:8080/index.html')
    
    # Mock window.open to intercept
    page.evaluate("""() => {
        window.__openedUrls = [];
        window.open = (url) => {
            window.__openedUrls.push(url);
            return null;
        };
    }""")
    
    # Switch to taps tab
    page.locator('.menu-mode-tab[data-menu-target="taps"]').click()
    page.wait_for_timeout(300)
    
    # Check visible taps count
    visible_taps = page.evaluate("() => Array.from(document.querySelectorAll('.beer-tap-card')).filter(c => c.offsetParent !== null).length")
    print(f"Visible tap cards after clicking tab: {visible_taps}")
    
    btn = page.locator('.btn-tap-order').first
    btn.click()
    page.wait_for_timeout(300)
    
    opened = page.evaluate("() => window.__openedUrls")
    print("Page errors on tap order click:", errors)
    print("Opened URLs:", opened)
    
    browser.close()
