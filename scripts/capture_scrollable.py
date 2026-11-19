import os
import sys
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8785

class Handler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # silent

def run_server():
    server = HTTPServer(('127.0.0.1', PORT), Handler)
    server.serve_forever()

# Start background server
t = threading.Thread(target=run_server, daemon=True)
t.start()
time.sleep(1)

os.makedirs('audit_screenshots', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Desktop full page & Hero
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle")
    time.sleep(1)
    
    # Viewport Hero
    page.screenshot(path="audit_screenshots/desktop_hero_scrollable.png")
    print("Desktop hero captured.")
    
    # Full Page
    page.screenshot(path="audit_screenshots/desktop_full_page.png", full_page=True)
    print("Desktop full page captured.")
    
    # Click Day Tab and capture Menu
    day_tab = page.locator("#tab-btn-day")
    if day_tab.is_visible():
        day_tab.click()
        time.sleep(0.5)
        page.locator("#menu").screenshot(path="audit_screenshots/desktop_menu_day.png")
        print("Desktop day menu captured.")
        
    # Switch back to Night Tab and capture Menu
    night_tab = page.locator("#tab-btn-night")
    if night_tab.is_visible():
        night_tab.click()
        time.sleep(0.5)
        page.locator("#menu").screenshot(path="audit_screenshots/desktop_menu_night.png")
        print("Desktop night menu captured.")
        
    # Capture Bento Grid
    page.locator("#el-lugar").screenshot(path="audit_screenshots/desktop_bento.png")
    print("Desktop bento captured.")
    
    # Capture Ubicación & Footer
    page.locator("#ubicacion").screenshot(path="audit_screenshots/desktop_ubicacion.png")
    page.locator("footer").screenshot(path="audit_screenshots/desktop_footer.png")
    print("Desktop ubicacion & footer captured.")

    # 2. Mobile (390x844)
    mobile_page = browser.new_page(viewport={"width": 390, "height": 844})
    mobile_page.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle")
    time.sleep(1)
    
    mobile_page.screenshot(path="audit_screenshots/mobile_hero.png")
    mobile_page.screenshot(path="audit_screenshots/mobile_full_page.png", full_page=True)
    print("Mobile screenshots captured.")
    
    browser.close()
print("All screenshots successfully captured!")
