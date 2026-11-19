import os, time, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8795
class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

server = HTTPServer(('127.0.0.1', PORT), H)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(1)

os.makedirs('audit_screenshots', exist_ok=True)
URL = f"http://127.0.0.1:{PORT}/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. 1920x1080 Full HD PC Monitor
    page_1080p = browser.new_page(viewport={"width": 1920, "height": 1080})
    page_1080p.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    page_1080p.screenshot(path="audit_screenshots/pc_1080p_hero.png")
    page_1080p.screenshot(path="audit_screenshots/pc_1080p_full.png", full_page=True)
    print("1920x1080 PC screenshots captured.")

    # 2. 1440x900 Laptop / Desktop
    page_1440 = browser.new_page(viewport={"width": 1440, "height": 900})
    page_1440.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    page_1440.screenshot(path="audit_screenshots/pc_1440p_hero.png")
    print("1440x900 PC screenshots captured.")

    browser.close()

print("All wide PC screenshots successfully taken!")
