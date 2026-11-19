import os, time, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8790
class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

threading.Thread(target=lambda: HTTPServer(('127.0.0.1', PORT), H).serve_forever(), daemon=True).start()
time.sleep(1)

os.makedirs('audit_screenshots', exist_ok=True)
URL = f"http://127.0.0.1:{PORT}/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Desktop 1440x900 (Hero viewport)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    page.screenshot(path="audit_screenshots/ref_desktop_hero.png")
    print("Desktop hero captured.")
    
    # Full page
    page.screenshot(path="audit_screenshots/ref_desktop_full.png", full_page=True)
    print("Desktop full page captured.")
    
    # 2. Mobile 390x844
    mobile = browser.new_page(viewport={"width": 390, "height": 844})
    mobile.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    mobile.screenshot(path="audit_screenshots/ref_mobile_hero.png")
    mobile.screenshot(path="audit_screenshots/ref_mobile_full.png", full_page=True)
    print("Mobile screenshots captured.")
    
    browser.close()
print("All screenshots successfully captured!")
