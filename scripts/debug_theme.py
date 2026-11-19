from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:8080/index.html', wait_until='networkidle')
    theme1 = page.locator('html').get_attribute('data-theme')
    print('Theme on load:', theme1)
    
    page.locator('#theme-toggle-btn').click()
    theme2 = page.locator('html').get_attribute('data-theme')
    print('Theme after click:', theme2)
    
    night_style = page.evaluate("() => { const s = window.getComputedStyle(document.querySelector('.hero-logo-night')); return { opacity: s.opacity, visibility: s.visibility, display: s.display, anim: s.animationName }; }")
    day_style = page.evaluate("() => { const s = window.getComputedStyle(document.querySelector('.hero-logo-day')); return { opacity: s.opacity, visibility: s.visibility, display: s.display }; }")
    print('Computed night:', night_style)
    print('Computed day:', day_style)
    browser.close()
