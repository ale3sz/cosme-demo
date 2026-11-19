import cv2
import numpy as np

def generate_photorealistic_neon():
    # Load exact source logo (.COSME.®)
    src = cv2.imread('C:/Users/aleja/.gemini/antigravity/brain/f8f257e2-6a56-4fc7-aea8-60c71038f382/.user_uploaded/media_1794983813737_dd9eae17.png', cv2.IMREAD_UNCHANGED)
    h, w = src.shape[:2]
    alpha = src[:, :, 3]

    # Target high-res canvas: 1200 x 380
    canvas_w, canvas_h = 1200, 380
    
    # 1. Clean the day logo
    # Find bounding box of letters (excluding or keeping dots)
    mask = (alpha > 30).astype(np.uint8) * 255
    y_idx, x_idx = np.where(mask > 0)
    crop_day = src[y_idx.min():y_idx.max()+1, x_idx.min():x_idx.max()+1]
    
    ch, cw = crop_day.shape[:2]
    scale = min((canvas_w - 120) / cw, (canvas_h - 80) / ch)
    nw, nh = int(cw * scale), int(ch * scale)
    
    resized_day = cv2.resize(crop_day, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    
    # Create Day Logo Canvas
    day_canvas = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)
    ox = (canvas_w - nw) // 2
    oy = (canvas_h - nh) // 2
    day_canvas[oy:oy+nh, ox:ox+nw] = resized_day
    
    # Save clean high-res Day Logo
    cv2.imwrite('assets/cosme_wordmark_day.png', day_canvas)
    print("Saved assets/cosme_wordmark_day.png")

    # 2. Build the exact matching Night Neon Sign from the SAME letters
    day_mask = day_canvas[:, :, 3]
    # Smooth glyphs slightly to simulate bent glass neon tubes
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    tube_solid = cv2.morphologyEx(day_mask, cv2.MORPH_CLOSE, kernel_close, iterations=2)
    
    # Distance transform gives the inner centerline of each letter
    dist = cv2.distanceTransform(tube_solid, cv2.DIST_L2, 5)
    max_d = np.max(dist)
    print("Max thickness:", max_d)
    
    # Neon Tube Contour (Double glass wall effect):
    # Outer glass tube wall
    glass_outer = cv2.Canny(tube_solid, 50, 150)
    glass_outer = cv2.dilate(glass_outer, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    
    # Plasma core: distance ridge (centerline of tubes)
    plasma_core = (dist > 4.5).astype(np.float32)
    plasma_core_blur = cv2.GaussianBlur(plasma_core, (5, 5), 1.2)
    
    # Inner gas body (saturated red)
    gas_body = (dist > 1.5).astype(np.float32)
    gas_body_blur = cv2.GaussianBlur(gas_body, (9, 9), 2.8)
    
    # Ambient Glow layers (Photorealistic crimson gas aura)
    glow_close = cv2.GaussianBlur(gas_body, (19, 19), 5.5)
    glow_mid   = cv2.GaussianBlur(gas_body, (45, 45), 14.0)
    glow_wide  = cv2.GaussianBlur(gas_body, (95, 95), 32.0)
    
    # Compose Neon RGB
    neon_rgb = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
    
    # Wide ambient glow (deep pure crimson #D60020)
    neon_rgb[:, :, 0] += glow_wide * 25.0   # Blue
    neon_rgb[:, :, 1] += glow_wide * 8.0    # Green
    neon_rgb[:, :, 2] += glow_wide * 230.0  # Red
    
    # Mid glow (#FF1E27)
    neon_rgb[:, :, 0] += glow_mid * 40.0
    neon_rgb[:, :, 1] += glow_mid * 20.0
    neon_rgb[:, :, 2] += glow_mid * 255.0
    
    # Close intense glow (#FF3B44)
    neon_rgb[:, :, 0] += glow_close * 65.0
    neon_rgb[:, :, 1] += glow_close * 45.0
    neon_rgb[:, :, 2] += glow_close * 255.0
    
    # Dense gas body inside tube
    neon_rgb[:, :, 0] += gas_body_blur * 110.0
    neon_rgb[:, :, 1] += gas_body_blur * 70.0
    neon_rgb[:, :, 2] += gas_body_blur * 255.0
    
    # Glass tube specular outline (reflection on glass)
    specular = (glass_outer.astype(np.float32) / 255.0)
    specular_blur = cv2.GaussianBlur(specular, (3, 3), 0.8)
    neon_rgb[:, :, 0] += specular_blur * 160.0
    neon_rgb[:, :, 1] += specular_blur * 140.0
    neon_rgb[:, :, 2] += specular_blur * 255.0
    
    # White-hot incandescent plasma core (#FFFFFF to #FFE4E6)
    neon_rgb[:, :, 0] += plasma_core_blur * 255.0
    neon_rgb[:, :, 1] += plasma_core_blur * 240.0
    neon_rgb[:, :, 2] += plasma_core_blur * 255.0
    
    neon_rgb = np.clip(neon_rgb, 0, 255).astype(np.uint8)
    
    # Alpha channel: carefully mapped so glow doesn't create hard edges
    neon_alpha = np.clip((glow_wide * 0.45 + glow_mid * 0.65 + glow_close * 0.85 + gas_body * 0.98 + plasma_core * 0.99) * 255.0, 0, 255).astype(np.uint8)
    
    neon_canvas = np.dstack([neon_rgb, neon_alpha])
    cv2.imwrite('assets/cosme_wordmark_night_neon.png', neon_canvas)
    print("Saved assets/cosme_wordmark_night_neon.png")

if __name__ == '__main__':
    generate_photorealistic_neon()
