import time
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # Test on Mobile (390x844) exactly as user's phone
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto('http://127.0.0.1:8080/index.html', wait_until='networkidle')
    time.sleep(1)

    # 1. Night Mode Mobile Hero
    page.screenshot(path='audit_screenshots/fixed_mobile_night.png')
    print("Captured fixed mobile night.")

    # 2. Toggle to Day Mode
    page.locator('#theme-toggle-btn').click()
    time.sleep(0.6) # Wait for transition to complete
    page.screenshot(path='audit_screenshots/fixed_mobile_day.png')
    print("Captured fixed mobile day.")

    # 3. Toggle back to Night Mode
    page.locator('#theme-toggle-btn').click()
    time.sleep(0.6)
    page.screenshot(path='audit_screenshots/fixed_mobile_night_after.png')
    print("Captured fixed mobile night after toggle.")

    browser.close()

print("Verification complete!")
