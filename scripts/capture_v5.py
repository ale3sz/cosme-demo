import os, time, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

PORT = 8786
class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
threading.Thread(target=lambda: HTTPServer(('127.0.0.1', PORT), H).serve_forever(), daemon=True).start()
time.sleep(0.8)
os.makedirs('audit_screenshots', exist_ok=True)
URL = f"http://127.0.0.1:{PORT}/index.html"

def reveal_all(page):
    page.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible'))")

with sync_playwright() as p:
    b = p.chromium.launch()
    errors = []
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.on("pageerror", lambda e: errors.append(str(e)))
    pg.on("console", lambda m: m.type == "error" and errors.append(m.text))
    pg.goto(URL, wait_until="networkidle"); time.sleep(2)
    pg.screenshot(path="audit_screenshots/v5_desktop_hero.png")
    reveal_all(pg); time.sleep(0.8)
    pg.click("#tab-btn-night"); time.sleep(0.5)
    pg.screenshot(path="audit_screenshots/v5_desktop_full.png", full_page=True)
    pg.evaluate("document.getElementById('menu').scrollIntoView()"); time.sleep(0.6)
    pg.screenshot(path="audit_screenshots/v5_desktop_menu_scrolled.png")
    pg.evaluate("window.scrollTo(0,0)"); time.sleep(0.3)
    pg.click("#theme-toggle"); time.sleep(1)
    pg.screenshot(path="audit_screenshots/v5_desktop_hero_day.png")
    pg.evaluate("document.getElementById('menu').scrollIntoView()"); time.sleep(0.6)
    pg.screenshot(path="audit_screenshots/v5_desktop_menu_day.png")
    pg.evaluate("localStorage.clear()")

    m = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=2)
    m.on("pageerror", lambda e: errors.append(str(e)))
    m.goto(URL, wait_until="networkidle"); time.sleep(2)
    m.screenshot(path="audit_screenshots/v5_mobile_hero.png")
    m.click("#mobile-menu-toggle"); time.sleep(0.6)
    m.screenshot(path="audit_screenshots/v5_mobile_menu.png")
    m.keyboard.press("Escape"); time.sleep(0.4)
    reveal_all(m)
    m.evaluate("document.getElementById('el-lugar').scrollIntoView()"); time.sleep(0.6)
    m.screenshot(path="audit_screenshots/v5_mobile_bento.png")
    m.evaluate("document.getElementById('ubicacion').scrollIntoView()"); time.sleep(0.6)
    m.screenshot(path="audit_screenshots/v5_mobile_ubicacion.png")
    b.close()
    print("ERRORS:", errors)
print("done")
