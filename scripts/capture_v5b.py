import time, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright
PORT = 8787
class H(SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
threading.Thread(target=lambda: HTTPServer(('127.0.0.1', PORT), H).serve_forever(), daemon=True).start()
time.sleep(0.8)
with sync_playwright() as p:
    b = p.chromium.launch()
    for vw, vh, name in [(1440, 900, 'desk'), (390, 844, 'mob')]:
        pg = b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=2 if name=='mob' else 1)
        pg.goto(f"http://127.0.0.1:{PORT}/index.html", wait_until="networkidle"); time.sleep(1)
        pg.evaluate("document.documentElement.style.scrollBehavior='auto'; document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-visible'))")
        pg.evaluate("window.scrollTo(0, document.getElementById('ubicacion').offsetTop - 80)"); time.sleep(1.2)
        print(name, 'header top:', pg.evaluate("document.querySelector('.site-header').getBoundingClientRect().top"),
              'height:', pg.evaluate("document.querySelector('.site-header').offsetHeight"))
        pg.screenshot(path=f"audit_screenshots/v5_{name}_ubicacion_fixed.png")
        pg.evaluate("window.scrollTo(0, document.getElementById('el-lugar').offsetTop + 300)"); time.sleep(1)
        pg.screenshot(path=f"audit_screenshots/v5_{name}_bento_fixed.png")
    b.close()
