import cv2
import numpy as np
import os

def create_neon_morph_sequence():
    os.makedirs('assets/logo_morph', exist_ok=True)
    
    # 1. Load exact source logo (.COSME.®)
    src = cv2.imread('C:/Users/aleja/.gemini/antigravity/brain/f8f257e2-6a56-4fc7-aea8-60c71038f382/.user_uploaded/media_1794983813737_dd9eae17.png', cv2.IMREAD_UNCHANGED)
    alpha = src[:, :, 3]
    mask = (alpha > 30).astype(np.uint8) * 255
    y_idx, x_idx = np.where(mask > 0)
    crop_day = src[y_idx.min():y_idx.max()+1, x_idx.min():x_idx.max()+1]

    canvas_w, canvas_h = 1000, 300
    ch, cw = crop_day.shape[:2]
    scale = min((canvas_w - 100) / cw, (canvas_h - 60) / ch)
    nw, nh = int(cw * scale), int(ch * scale)
    
    resized_day = cv2.resize(crop_day, (nw, nh), interpolation=cv2.INTER_LANCZOS4)
    
    # Frame 0: Clean Day Logo (stamped black ink)
    f0 = np.zeros((canvas_h, canvas_w, 4), dtype=np.uint8)
    ox = (canvas_w - nw) // 2
    oy = (canvas_h - nh) // 2
    f0[oy:oy+nh, ox:ox+nw] = resized_day
    cv2.imwrite('assets/logo_morph/frame_0_day.png', f0)

    # Prepare masks for tube generation
    f0_mask = f0[:, :, 3]
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    tube_solid = cv2.morphologyEx(f0_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    dist = cv2.distanceTransform(tube_solid, cv2.DIST_L2, 5)

    # Outer glass tube contour
    glass_outer = cv2.Canny(tube_solid, 50, 150)
    glass_outer = cv2.dilate(glass_outer, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)))
    specular = (glass_outer.astype(np.float32) / 255.0)
    specular_blur = cv2.GaussianBlur(specular, (3, 3), 0.8)

    # Centerline plasma core
    plasma_core = (dist > 3.8).astype(np.float32)
    plasma_core_blur = cv2.GaussianBlur(plasma_core, (5, 5), 1.2)

    # Gas tube body
    gas_body = (dist > 1.2).astype(np.float32)
    gas_body_blur = cv2.GaussianBlur(gas_body, (9, 9), 2.5)

    # Ambient glows
    glow_close = cv2.GaussianBlur(gas_body, (17, 17), 5.0)
    glow_mid   = cv2.GaussianBlur(gas_body, (39, 39), 12.0)
    glow_wide  = cv2.GaussianBlur(gas_body, (85, 85), 28.0)

    # Frame 1: Unlit glass tube outlines appearing over the letters with faint red pre-heat
    f1 = f0.copy().astype(np.float32)
    # Tint ink slightly reddish
    f1[:, :, 0] = f1[:, :, 0] * 0.7  # B
    f1[:, :, 1] = f1[:, :, 1] * 0.7  # G
    f1[:, :, 2] = np.clip(f1[:, :, 2] + glow_close * 90.0, 0, 255) # R
    # Add glass outline reflection
    f1[:, :, 0] = np.clip(f1[:, :, 0] + specular_blur * 80.0, 0, 255)
    f1[:, :, 1] = np.clip(f1[:, :, 1] + specular_blur * 80.0, 0, 255)
    f1[:, :, 2] = np.clip(f1[:, :, 2] + specular_blur * 140.0, 0, 255)
    cv2.imwrite('assets/logo_morph/frame_1_heat.png', f1.astype(np.uint8))

    # Frame 2: Electrical spark / ignition pulse (high voltage white flash)
    f2_rgb = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
    f2_rgb[:, :, 0] = glow_mid * 60.0 + plasma_core_blur * 255.0 + specular_blur * 180.0
    f2_rgb[:, :, 1] = glow_mid * 40.0 + plasma_core_blur * 240.0 + specular_blur * 180.0
    f2_rgb[:, :, 2] = glow_mid * 255.0 + plasma_core_blur * 255.0 + specular_blur * 255.0
    f2_alpha = np.clip((glow_mid * 0.7 + gas_body * 0.95 + plasma_core) * 255.0, 0, 255).astype(np.uint8)
    f2 = np.dstack([np.clip(f2_rgb, 0, 255).astype(np.uint8), f2_alpha])
    cv2.imwrite('assets/logo_morph/frame_2_spark.png', f2)

    # Frame 3: Full glowing crimson red neon sign (photorealistic night state)
    f3_rgb = np.zeros((canvas_h, canvas_w, 3), dtype=np.float32)
    f3_rgb[:, :, 0] = glow_wide * 25.0 + glow_mid * 40.0 + glow_close * 65.0 + gas_body_blur * 100.0 + plasma_core_blur * 255.0 + specular_blur * 150.0
    f3_rgb[:, :, 1] = glow_wide * 8.0  + glow_mid * 20.0 + glow_close * 45.0 + gas_body_blur * 70.0  + plasma_core_blur * 230.0 + specular_blur * 130.0
    f3_rgb[:, :, 2] = glow_wide * 230.0 + glow_mid * 255.0 + glow_close * 255.0 + gas_body_blur * 255.0 + plasma_core_blur * 255.0 + specular_blur * 255.0
    f3_alpha = np.clip((glow_wide * 0.45 + glow_mid * 0.65 + glow_close * 0.85 + gas_body * 0.98 + plasma_core * 0.99) * 255.0, 0, 255).astype(np.uint8)
    f3 = np.dstack([np.clip(f3_rgb, 0, 255).astype(np.uint8), f3_alpha])
    cv2.imwrite('assets/logo_morph/frame_3_night.png', f3)

    print("Created morph frames: frame_0_day.png, frame_1_heat.png, frame_2_spark.png, frame_3_night.png!")

if __name__ == '__main__':
    create_neon_morph_sequence()
