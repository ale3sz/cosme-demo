from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto('http://127.0.0.1:8080/index.html')
    page.wait_for_timeout(1000)

    # Instrument drawFrame to record exactly which frames are drawn and when
    page.evaluate("""() => {
        window.__frameEvents = [];
        const canvas = document.getElementById('hero-logo-canvas');
        const ctx = canvas.getContext('2d');
        const origDrawImage = ctx.drawImage.bind(ctx);
        
        ctx.drawImage = function(...args) {
            window.__frameEvents.push({
                time: performance.now(),
                type: 'canvas_drawImage'
            });
            return origDrawImage(...args);
        };
    }""")

    # First switch to Day to start from Day
    page.locator('#theme-toggle-btn').click()
    page.wait_for_timeout(600)

    # Now instrument and trigger Day -> Night
    page.evaluate("() => { window.__frameEvents = []; window.__t0 = performance.now(); }")
    page.locator('#theme-toggle-btn').click()
    page.wait_for_timeout(600)
    
    events_day_to_night = page.evaluate("() => window.__frameEvents")

    # Now instrument and trigger Night -> Day
    page.evaluate("() => { window.__frameEvents = []; window.__t0 = performance.now(); }")
    page.locator('#theme-toggle-btn').click()
    page.wait_for_timeout(600)
    
    events_night_to_day = page.evaluate("() => window.__frameEvents")

    def analyze_events(events, name):
        times = [e['time'] for e in events]
        deltas = [times[i] - times[i-1] for i in range(1, len(times))]
        total_time = times[-1] - times[0] if times else 0
        avg_delta = sum(deltas) / len(deltas) if deltas else 0
        effective_fps = 1000.0 / avg_delta if avg_delta > 0 else 0
        print(f"=== {name} ===")
        print(f"Total draws: {len(events)}")
        print(f"Total duration: {total_time:.2f} ms")
        print(f"Average delta: {avg_delta:.2f} ms (~{effective_fps:.1f} FPS)")
        print(f"Max delta: {max(deltas) if deltas else 0:.2f} ms")
        print(f"Min delta: {min(deltas) if deltas else 0:.2f} ms")
        return {
            "total_draws": len(events),
            "total_duration_ms": round(total_time, 2),
            "avg_delta_ms": round(avg_delta, 2),
            "effective_fps": round(effective_fps, 1),
            "max_delta_ms": round(max(deltas) if deltas else 0, 2),
            "min_delta_ms": round(min(deltas) if deltas else 0, 2)
        }

    res_d2n = analyze_events(events_day_to_night, "DAY -> NIGHT (21 frames)")
    res_n2d = analyze_events(events_night_to_day, "NIGHT -> DAY (13 frames cooling)")

    with open("audit_results/frame_timing_analysis.json", "w", encoding="utf-8") as f:
        json.dump({"day_to_night": res_d2n, "night_to_day": res_n2d}, f, indent=2)

    browser.close()
