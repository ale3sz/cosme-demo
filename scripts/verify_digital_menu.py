import asyncio
import os
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        errors = []
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: errors.append(f"ConsoleError: {msg.text}") if msg.type == "error" else None)

        file_url = f"file:///{os.path.abspath('index.html').replace(os.sep, '/')}"
        print(f"Loading {file_url}")
        await page.goto(file_url, wait_until="networkidle")

        # 1. Verify #espacio is gone
        espacio_count = await page.locator("#espacio").count()
        print(f"Count of #espacio elements: {espacio_count} (expected 0)")
        assert espacio_count == 0, "Error: #espacio still exists!"

        # 2. Verify sections: Hero -> Menu -> Festejos -> Ubicacion
        menu_visible = await page.is_visible("#menu")
        festejos_visible = await page.is_visible("#festejos")
        ubicacion_visible = await page.is_visible("#ubicacion")
        print(f"Sections visible - Menu: {menu_visible}, Festejos: {festejos_visible}, Ubicacion: {ubicacion_visible}")

        # 3. Test opening Carta Noche modal
        open_noche_btn = page.locator('button[data-open-pdf="noche"]')
        await open_noche_btn.scroll_into_view_if_needed()
        await open_noche_btn.click()
        await page.wait_for_timeout(400)

        modal_visible = await page.is_visible("#modal-carta.active")
        badge_text = await page.inner_text("#modal-pdf-badge")
        download_href = await page.get_attribute("#modal-pdf-download-link", "href")
        print(f"Modal Carta active: {modal_visible}, Badge: '{badge_text}', Download: '{download_href}'")

        # 4. Switch tab to Dia inside modal
        dia_tab = page.locator('.pdf-switch-tab[data-pdf-doc="dia"]')
        await dia_tab.click()
        await page.wait_for_timeout(300)
        badge_dia = await page.inner_text("#modal-pdf-badge")
        download_dia = await page.get_attribute("#modal-pdf-download-link", "href")
        print(f"Switched to Dia - Badge: '{badge_dia}', Download: '{download_dia}'")

        # 5. Close modal
        close_btn = page.locator("#modal-carta .modal-close-btn")
        await close_btn.click()
        await page.wait_for_timeout(300)
        modal_closed = not await page.is_visible("#modal-carta.active")
        print(f"Modal closed cleanly: {modal_closed}")

        # 6. Take screenshot of desktop
        await page.screenshot(path="audit_screenshots/desktop_digital_menu.png", full_page=False)

        await browser.close()

        if errors:
            print("Errors detected:", errors)
        else:
            print("VERIFICATION COMPLETE: Zero errors detected!")

if __name__ == "__main__":
    asyncio.run(verify())
