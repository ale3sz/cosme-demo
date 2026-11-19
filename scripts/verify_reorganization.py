import asyncio
import os
from playwright.async_api import async_playwright

async def verify_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        errors = []
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: errors.append(f"ConsoleError: {msg.text}") if msg.type == "error" else None)

        file_url = f"file:///{os.path.abspath('index.html').replace(os.sep, '/')}"
        print(f"Loading {file_url}")
        await page.goto(file_url, wait_until="networkidle")

        # Check section visibility
        espacio_visible = await page.is_visible("#espacio")
        menu_visible = await page.is_visible("#menu")
        festejos_visible = await page.is_visible("#festejos")
        ubicacion_visible = await page.is_visible("#ubicacion")
        
        print(f"Sections visible - Espacio: {espacio_visible}, Menu: {menu_visible}, Festejos: {festejos_visible}, Ubicacion: {ubicacion_visible}")

        # Check Tab switching in Menu:
        # 1. Click Canillas tab
        taps_btn = page.locator('button[data-menu-target="taps"]')
        await taps_btn.click()
        await page.wait_for_timeout(300)
        taps_board_visible = await page.is_visible("#canillas")
        print(f"Canillas tab clicked - Board visible: {taps_board_visible}")

        # 2. Click Day tab
        day_btn = page.locator('button[data-menu-target="day"]')
        await day_btn.click()
        await page.wait_for_timeout(300)
        lunch_suggester_visible = await page.is_visible("#lunch-suggester-box")
        print(f"Day tab clicked - Lunch Suggester visible: {lunch_suggester_visible}")

        # 3. Click Night tab
        night_btn = page.locator('button[data-menu-target="night"]')
        await night_btn.click()
        await page.wait_for_timeout(300)
        night_dishes_visible = await page.is_visible(".dish-night")
        print(f"Night tab clicked - Night dishes visible: {night_dishes_visible}")

        # Test mobile viewport (390x844)
        mobile_page = await browser.new_page(viewport={"width": 390, "height": 844})
        await mobile_page.goto(file_url, wait_until="networkidle")
        await mobile_page.screenshot(path="audit_screenshots/mobile_reorganized.png", full_page=False)
        print("Mobile screenshot captured")

        await browser.close()
        
        if errors:
            print("Detected errors:", errors)
        else:
            print("ZERO JavaScript errors detected!")

if __name__ == "__main__":
    asyncio.run(verify_page())
