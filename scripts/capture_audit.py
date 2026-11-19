import os
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8780
SCREENSHOT_DIR = os.path.join(os.getcwd(), "audit_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

def run_server():
    server = HTTPServer(("127.0.0.1", PORT), QuietHandler)
    server.serve_forever()

server_thread = threading.Thread(target=run_server, daemon=True)
server_thread.start()
time.sleep(0.5)

URL = f"http://127.0.0.1:{PORT}/index.html"

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Desktop (1440x900)
    context_desktop = browser.new_context(
        viewport={"width": 1440, "height": 900},
        device_scale_factor=1.5
    )
    page_d = context_desktop.new_page()
    page_d.goto(URL, wait_until="networkidle")
    page_d.wait_for_timeout(1000)

    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "reference_fidelity_desktop.png"))
    print("Captured Reference Fidelity Desktop")

    context_desktop.close()

    # 2. Mobile (390x844)
    context_mobile = browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
        is_mobile=True,
        has_touch=True,
        device_scale_factor=2
    )
    page_m = context_mobile.new_page()
    page_m.goto(URL, wait_until="networkidle")
    page_m.wait_for_timeout(1000)

    page_m.screenshot(path=os.path.join(SCREENSHOT_DIR, "reference_fidelity_mobile.png"))
    print("Captured Reference Fidelity Mobile")

    context_mobile.close()
    browser.close()

print("Capturas completadas con éxito.")
