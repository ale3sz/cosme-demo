import os
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8899
SCREENSHOT_DIR = os.path.join(os.getcwd(), "audit_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

server = HTTPServer(("127.0.0.1", PORT), QuietHandler)
server_thread = threading.Thread(target=server.serve_forever, daemon=True)
server_thread.start()
time.sleep(0.5)

URL = f"http://127.0.0.1:{PORT}/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Mobile viewport (390x844)
    context_m = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, device_scale_factor=2)
    page_m = context_m.new_page()
    page_m.goto(URL, wait_until="networkidle")
    page_m.wait_for_timeout(500)

    # Screenshot Hub in local index.html
    hub = page_m.locator("#accesos-rapidos")
    hub.scroll_into_view_if_needed()
    page_m.wait_for_timeout(400)
    page_m.screenshot(path=os.path.join(SCREENSHOT_DIR, "local_index_bio_hub_mobile.png"))
    print("Captured: Local index.html Bio Hub Mobile")

    # Click "Ver Carta PDF" on noche
    pdf_btn = page_m.locator("[data-open-pdf='noche']").first
    if pdf_btn.is_visible():
        pdf_btn.click()
        page_m.wait_for_timeout(1000)
        page_m.screenshot(path=os.path.join(SCREENSHOT_DIR, "local_index_pdf_modal_opened.png"))
        print("Captured: Local index.html PDF Modal Opened")

    # 2. Desktop viewport (1440x900)
    context_d = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    page_d = context_d.new_page()
    page_d.goto(URL, wait_until="networkidle")
    page_d.wait_for_timeout(500)

    hub_d = page_d.locator("#accesos-rapidos")
    hub_d.scroll_into_view_if_needed()
    page_d.wait_for_timeout(400)
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "local_index_bio_hub_desktop.png"))
    print("Captured: Local index.html Bio Hub Desktop")

    browser.close()
    server.shutdown()
    print("Test local index completed successfully!")
