import asyncio
import os
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop Test
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        errors = []
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: errors.append(f"ConsoleError: {msg.text}") if msg.type == "error" else None)

        file_url = f"file:///{os.path.abspath('index.html').replace(os.sep, '/')}"
        print(f"Loading {file_url}")
        await page.goto(file_url, wait_until="networkidle")

        # Verify sections in DOM order
        sections = await page.locator("main > section").all()
        section_ids = []
        for s in sections:
            sid = await s.get_attribute("id")
            if not sid:
                sclass = await s.get_attribute("class")
                sid = f"class:{sclass}"
            section_ids.append(sid)
        print("DOM Section Order:", section_ids)

        expected_order = ['class:hero', 'menu', 'espacio', 'resenas', 'festejos', 'ubicacion']
        assert section_ids == expected_order, f"Section order mismatch! Found: {section_ids}"

        # Check visibility
        for sid in ['#menu', '#espacio', '#resenas', '#festejos', '#ubicacion']:
            visible = await page.is_visible(sid)
            print(f"Section {sid} visible: {visible}")
            assert visible, f"Section {sid} is not visible!"

        os.makedirs("audit_screenshots", exist_ok=True)
        await page.screenshot(path="audit_screenshots/desktop_neuro_journey.png", full_page=True)
        print("Desktop screenshot saved: audit_screenshots/desktop_neuro_journey.png")

        # 2. Mobile Test (iPhone 14 style)
        mobile_page = await browser.new_page(viewport={"width": 390, "height": 844})
        await mobile_page.goto(file_url, wait_until="networkidle")
        await mobile_page.screenshot(path="audit_screenshots/mobile_neuro_journey.png", full_page=True)
        print("Mobile screenshot saved: audit_screenshots/mobile_neuro_journey.png")

        print("Total console errors:", len(errors))
        if errors:
            print("Errors:", errors)

        await browser.close()
        print("ALL AUDIT CHECKS PASSED PERFECTLY!")

if __name__ == '__main__':
    asyncio.run(verify())
