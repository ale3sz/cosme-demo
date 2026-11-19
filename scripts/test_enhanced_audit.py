import os, time, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8793
class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

server = HTTPServer(('127.0.0.1', PORT), H)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(1)

os.makedirs('audit_screenshots', exist_ok=True)
URL = f"http://127.0.0.1:{PORT}/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Desktop Night Mode
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(URL, wait_until="networkidle")
    time.sleep(2)
    page.screenshot(path="audit_screenshots/enhanced_desktop_night_hero.png")
    
    # Scroll to Pizarra de Canillas
    canillas = page.locator('#canillas')
    if canillas.count() > 0:
        canillas.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path="audit_screenshots/enhanced_desktop_canillas.png")

    # Scroll to Menu
    menu = page.locator('#menu')
    if menu.count() > 0:
        menu.scroll_into_view_if_needed()
        time.sleep(1)
        page.screenshot(path="audit_screenshots/enhanced_desktop_menu_night.png")

    # Full page Night
    page.screenshot(path="audit_screenshots/enhanced_desktop_night_full.png", full_page=True)
    print("Desktop Night captured.")

    # 2. Desktop Day Mode Toggle
    page.locator('#theme-toggle-btn').click()
    time.sleep(1.5)
    page.screenshot(path="audit_screenshots/enhanced_desktop_day_hero.png")

    # Scroll to Day Menu with Lunch Suggester
    menu.scroll_into_view_if_needed()
    time.sleep(1)
    page.screenshot(path="audit_screenshots/enhanced_desktop_day_menu_suggester.png")
    page.screenshot(path="audit_screenshots/enhanced_desktop_day_full.png", full_page=True)
    print("Desktop Day captured.")

    # 3. Test Brand Modal
    page.locator('[data-open-modal="brand"]').click()
    time.sleep(1)
    page.screenshot(path="audit_screenshots/enhanced_brand_modal.png")
    page.locator('#modal-brand .modal-close-btn').click()
    time.sleep(0.5)

    # 4. Mobile Viewport (390x844)
    mobile = browser.new_page(viewport={"width": 390, "height": 844})
    mobile.goto(URL, wait_until="networkidle")
    time.sleep(2)
    mobile.screenshot(path="audit_screenshots/enhanced_mobile_hero.png")
    mobile.screenshot(path="audit_screenshots/enhanced_mobile_full.png", full_page=True)
    print("Mobile captured.")

    browser.close()

print("All enhanced audit screenshots successfully generated!")
