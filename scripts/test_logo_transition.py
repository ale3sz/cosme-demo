import os, time, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8798
class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

server = HTTPServer(('127.0.0.1', PORT), H)
threading.Thread(target=server.serve_forever, daemon=True).start()
time.sleep(1)

os.makedirs('audit_screenshots', exist_ok=True)
URL = f"http://127.0.0.1:{PORT}/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(URL, wait_until="networkidle")
    time.sleep(1.5)

    # 1. Capture initial Night Mode
    logo_box = page.locator('#hero-logo-box')
    logo_box.screenshot(path="audit_screenshots/logo_trans_01_night.png")
    print("Captured logo in Night Mode.")

    # 2. Click Day Switch & capture during / after transition
    page.locator('#theme-toggle-btn').click()
    time.sleep(0.5) # Transition finished
    logo_box.screenshot(path="audit_screenshots/logo_trans_02_day.png")
    print("Captured logo in Day Mode.")

    # 3. Click back to Night Mode & capture ignition
    page.locator('#theme-toggle-btn').click()
    time.sleep(0.15) # Mid-ignition flicker
    logo_box.screenshot(path="audit_screenshots/logo_trans_03_mid_ignition.png")
    time.sleep(0.5) # Settled night
    logo_box.screenshot(path="audit_screenshots/logo_trans_04_settled_night.png")
    print("Captured logo ignition back to Night.")

    # Full hero capture in Day and Night
    page.screenshot(path="audit_screenshots/logo_hero_full_night.png")
    page.locator('#theme-toggle-btn').click()
    time.sleep(0.5)
    page.screenshot(path="audit_screenshots/logo_hero_full_day.png")

    browser.close()

print("All transition test captures complete!")
