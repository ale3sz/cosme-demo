import os
import time
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = os.path.join(os.getcwd(), "audit_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch()

    # 1. Mobile Bio-Links View (/links) — iPhone 14
    context_mobile = browser.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2,
        is_mobile=True
    )
    page_m = context_mobile.new_page()
    page_m.goto("http://localhost:4321/links", wait_until="networkidle")
    page_m.wait_for_timeout(800)
    page_m.screenshot(path=os.path.join(SCREENSHOT_DIR, "v4_bio_links_mobile.png"), full_page=True)
    print("Captured: v4 Bio Links Mobile (/links)")

    # 2. Main Page Quick Links Hub (#accesos-rapidos)
    page_home = context_mobile.new_page()
    page_home.goto("http://localhost:4321/#accesos-rapidos", wait_until="networkidle")
    page_home.wait_for_timeout(800)
    hub = page_home.locator("#accesos-rapidos")
    hub.scroll_into_view_if_needed()
    page_home.wait_for_timeout(400)
    page_home.screenshot(path=os.path.join(SCREENSHOT_DIR, "v4_home_hub_mobile.png"))
    print("Captured: v4 Home Hub Mobile")

    # 3. Main Page Event Banner in VHS section
    vhs_event = page_home.locator("#festejos-dj")
    vhs_event.scroll_into_view_if_needed()
    page_home.wait_for_timeout(400)
    page_home.screenshot(path=os.path.join(SCREENSHOT_DIR, "v4_event_banner_mobile.png"))
    print("Captured: v4 Event Banner Mobile")

    browser.close()
    print("All Linktree captures complete!")
