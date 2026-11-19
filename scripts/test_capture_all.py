import os
import time
import threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8901
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

    # =========================================================================
    # 1. DESKTOP VIEWPORT (1440x900) - NIGHT MODE
    # =========================================================================
    context_d = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1.5)
    page_d = context_d.new_page()
    page_d.goto(URL, wait_until="networkidle")
    page_d.wait_for_timeout(600)

    # Full page Night
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_desktop_night_full.png"), full_page=True)
    print("✓ Captured: final_desktop_night_full.png")

    # Hero Night
    hero = page_d.locator(".hero")
    hero.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_desktop_night_hero.png"))
    print("✓ Captured: final_desktop_night_hero.png")

    # WhatsApp Presets
    wa_sec = page_d.locator("#whatsapp-rapido")
    wa_sec.scroll_into_view_if_needed()
    page_d.wait_for_timeout(300)
    wa_sec.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_desktop_whatsapp_presets.png"))
    print("✓ Captured: final_desktop_whatsapp_presets.png")

    # Menú Night
    menu_sec = page_d.locator("#menu")
    menu_sec.scroll_into_view_if_needed()
    page_d.wait_for_timeout(300)
    menu_sec.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_desktop_menu_night.png"))
    print("✓ Captured: final_desktop_menu_night.png")

    # Modal Reserva Open
    page_d.click("[data-open-modal='reserva']")
    page_d.wait_for_timeout(400)
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_desktop_modal_reserva.png"))
    print("✓ Captured: final_desktop_modal_reserva.png")
    page_d.click(".modal-close-btn")
    page_d.wait_for_timeout(300)

    # =========================================================================
    # 2. DESKTOP VIEWPORT - TOGGLE TO DAY MODE
    # =========================================================================
    page_d.click("#theme-toggle-btn")
    page_d.wait_for_timeout(500)

    # Full page Day
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_desktop_day_full.png"), full_page=True)
    print("✓ Captured: final_desktop_day_full.png")

    # Hero Day
    hero.scroll_into_view_if_needed()
    page_d.wait_for_timeout(300)
    hero.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_desktop_day_hero.png"))
    print("✓ Captured: final_desktop_day_hero.png")

    # Menú Day
    menu_sec.scroll_into_view_if_needed()
    page_d.wait_for_timeout(300)
    menu_sec.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_desktop_menu_day.png"))
    print("✓ Captured: final_desktop_menu_day.png")

    # =========================================================================
    # 3. MOBILE VIEWPORT (390x844)
    # =========================================================================
    context_m = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, device_scale_factor=2)
    page_m = context_m.new_page()
    page_m.goto(URL, wait_until="networkidle")
    page_m.wait_for_timeout(600)

    # Mobile Full Page Night
    page_m.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_mobile_night_full.png"), full_page=True)
    print("✓ Captured: final_mobile_night_full.png")

    # Mobile WhatsApp Presets
    wa_m = page_m.locator("#whatsapp-rapido")
    wa_m.scroll_into_view_if_needed()
    page_m.wait_for_timeout(300)
    wa_m.screenshot(path=os.path.join(SCREENSHOT_DIR, "final_mobile_whatsapp.png"))
    print("✓ Captured: final_mobile_whatsapp.png")

    browser.close()
    server.shutdown()
    print("All captures completed successfully!")
