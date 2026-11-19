from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://127.0.0.1:8080/index.html')
    page.wait_for_timeout(1000) # wait for preload
    
    status = page.evaluate("""() => {
        // We can inspect decodedBitmaps if exposed or via canvas
        const canvas = document.getElementById('hero-logo-canvas');
        const ctx = canvas.getContext('2d');
        const pxl = ctx.getImageData(400, 120, 1, 1).data;
        return {
            canvasWidth: canvas.width,
            canvasHeight: canvas.height,
            centerPixel: Array.from(pxl),
            hasNonZeroPixels: pxl.some(x => x > 0)
        };
    }""")
    print("Canvas drawn state:", status)
    browser.close()
