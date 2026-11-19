import os
from playwright.sync_api import sync_playwright

SCREENSHOT_DIR = os.path.join(os.getcwd(), "audit_screenshots")

with sync_playwright() as p:
    browser = p.chromium.launch()
    context_mobile = browser.new_context(
        viewport={"width": 390, "height": 844},
        device_scale_factor=2,
        is_mobile=True
    )
    page = context_mobile.new_page()
    page.goto("http://localhost:4321", wait_until="networkidle")
    page.wait_for_timeout(800)

    # Scroll to #bio-hub
    hub = page.locator("#bio-hub")
    hub.scroll_into_view_if_needed()
    page.wait_for_timeout(400)
    page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v5_final_bio_hub_in_landing.png"))
    print("Captured: v5 Final Bio Hub in Landing")

    # Click "Ver Carta PDF" on noche to test modal opening
    pdf_btn = page.locator("button:has-text('Ver Carta PDF')").first
    if pdf_btn.is_visible():
        pdf_btn.click()
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, "v5_pdf_modal_opened.png"))
        print("Captured: v5 PDF Modal Opened")

    browser.close()
    print("Final capture complete!")
