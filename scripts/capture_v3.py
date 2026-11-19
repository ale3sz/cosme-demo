import os
import time
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = os.path.join(os.getcwd(), "audit_screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
URL = "http://localhost:4321"

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Desktop captures (1440x900)
    context_desktop = browser.new_context(
        viewport={"width": 1440, "height": 900},
        device_scale_factor=1.5
    )
    page_d = context_desktop.new_page()
    page_d.goto(URL, wait_until="networkidle")
    page_d.wait_for_timeout(1000)

    # 1.1 Desktop Hero Night
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "v3_astro_desktop_hero.png"))
    print("Captured: v3 Desktop Hero")

    # 1.2 Desktop Bento
    bento = page_d.locator("#el-lugar")
    bento.scroll_into_view_if_needed()
    page_d.wait_for_timeout(500)
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "v3_astro_desktop_bento.png"))
    print("Captured: v3 Desktop Bento")

    # 1.3 Desktop Menu Tabs
    menu = page_d.locator("#menu-interactivo")
    menu.scroll_into_view_if_needed()
    page_d.wait_for_timeout(500)
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "v3_astro_desktop_menu_night.png"))
    print("Captured: v3 Desktop Menu Night")

    # Click day tab in menu
    day_tab = page_d.locator("#tab-day")
    if day_tab.is_visible():
        day_tab.click()
        page_d.wait_for_timeout(400)
        page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "v3_astro_desktop_menu_day.png"))
        print("Captured: v3 Desktop Menu Day")

    # 1.4 Desktop VHS & Birthday Calculator
    vhs = page_d.locator("#festejos-dj")
    vhs.scroll_into_view_if_needed()
    page_d.wait_for_timeout(500)
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "v3_astro_desktop_vhs_birthday.png"))
    print("Captured: v3 Desktop VHS & Birthday")

    # 1.5 Desktop Location & Footer
    loc = page_d.locator("#ubicacion")
    loc.scroll_into_view_if_needed()
    page_d.wait_for_timeout(500)
    page_d.screenshot(path=os.path.join(SCREENSHOT_DIR, "v3_astro_desktop_location.png"))
    print("Captured: v3 Desktop Location")

    # 2. Mobile captures (390x844 - iPhone 14 / modern smartphone)
    context_mobile = browser.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2,
        is_mobile=True
    )
    page_m = context_mobile.new_page()
    page_m.goto(URL, wait_until="networkidle")
    page_m.wait_for_timeout(800)

    # 2.1 Mobile Hero
    page_m.screenshot(path=os.path.join(SCREENSHOT_DIR, "v3_astro_mobile_hero.png"))
    print("Captured: v3 Mobile Hero")

    # 2.2 Mobile Birthday Calculator
    cumple_m = page_m.locator("#festejos-dj")
    cumple_m.scroll_into_view_if_needed()
    page_m.wait_for_timeout(500)
    page_m.screenshot(path=os.path.join(SCREENSHOT_DIR, "v3_astro_mobile_birthday.png"))
    print("Captured: v3 Mobile Birthday")

    browser.close()
    print("All captures completed successfully!")
