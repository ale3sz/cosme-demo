"""
Genera la secuencia maestra de 28 fotogramas continuos y la empaqueta en un SPRITE SHEET de alta definición (4 columnas x 7 filas).
Esto garantiza 60 FPS nativos con 1 sola petición HTTP y 0 stuttering en móviles.
"""
import os
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

ROOT = os.path.abspath('.')
OUT_DIR = os.path.join(ROOT, 'assets', 'logo_morph')
os.makedirs(OUT_DIR, exist_ok=True)

FRAME_W, FRAME_H = 800, 240
TARGET_LETTER_W = 600.0

def align_by_letters(im, bbox):
    x_min, y_min, x_max, y_max = bbox
    letter_w = float(x_max - x_min)
    letter_cx = float(x_min + x_max) / 2.0
    letter_cy = float(y_min + y_max) / 2.0
    
    scale = TARGET_LETTER_W / letter_w
    new_w = round(im.width * scale)
    new_h = round(im.height * scale)
    resized = im.resize((new_w, new_h), Image.LANCZOS)
    
    scaled_cx = letter_cx * scale
    scaled_cy = letter_cy * scale
    
    pos_x = round((FRAME_W / 2.0) - scaled_cx)
    pos_y = round((FRAME_H / 2.0) - scaled_cy)
    
    canvas = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    canvas.alpha_composite(resized, (pos_x, pos_y))
    return canvas

# 1. Base Keyframes
day_raw = Image.open(os.path.join(ROOT, 'assets', 'logo_morph', 'frame_0_day.png')).convert('RGBA')
mid_raw = Image.open(os.path.join(ROOT, 'assets', 'brand', 'cosme_neon_intermediate.png')).convert('RGBA')
night_raw = Image.open(os.path.join(ROOT, 'assets', 'brand', 'cosme_neon_original.png')).convert('RGBA')

k0_day = align_by_letters(day_raw, (120, 53, 878, 245))
k3_mid = align_by_letters(mid_raw, (122, 22, 900, 287))
k7_night = align_by_letters(night_raw, (9, 21, 1014, 337))

# 2. Derive intermediate physical keyframes
# k1_glass: Cold glass outlines over day stamp
k1_glass = Image.blend(k0_day, k3_mid, 0.20)

# k2_preheat: Filaments warming up in deep crimson
k2_preheat = Image.blend(k0_day, k3_mid, 0.55)

# k4_surge: Intermediate neon with intense white-hot core
arr_surge = np.array(k3_mid, dtype=np.float32)
bright_tubes = (arr_surge[:,:,0] > 160) & (arr_surge[:,:,3] > 100)
arr_surge[bright_tubes, 1] += 120 # add yellow/white
arr_surge[bright_tubes, 2] += 110 # white
# Heat up the interior burgundy texture to glowing crimson
dark_fill = (arr_surge[:,:,3] > 60) & (arr_surge[:,:,0] < 160)
arr_surge[dark_fill, 0] = np.clip(arr_surge[dark_fill, 0] * 2.2 + 50, 0, 255)
arr_surge = np.clip(arr_surge, 0, 255).astype(np.uint8)
k4_surge = Image.fromarray(arr_surge, 'RGBA')

# k5_ignited: Complete solid neon .COSME.
arr_ignited = arr_surge.copy()
arr_ignited[dark_fill, 0] = 245
arr_ignited[dark_fill, 1] = 40
arr_ignited[dark_fill, 2] = 45
k5_ignited = Image.fromarray(arr_ignited, 'RGBA').filter(ImageFilter.GaussianBlur(0.6))

# k6_arc: High-voltage bridge discharge uniting both signs
k6_arc = Image.blend(k5_ignited, k7_night, 0.50)
enhancer = ImageEnhance.Brightness(k6_arc.convert('RGB'))
k6_arc_rgb = enhancer.enhance(1.35)
k6_arc_rgb.putalpha(k6_arc.getchannel('A'))
k6_arc = k6_arc_rgb.filter(ImageFilter.GaussianBlur(0.8))

def ease(t):
    return t * t * (3.0 - 2.0 * t)

# Segments to create 28 frames total (0 to 27):
# k0 -> k1: 3 steps (frames 1, 2, 3)
# k1 -> k2: 4 steps (frames 4, 5, 6, 7)
# k2 -> k3: 4 steps (frames 8, 9, 10, 11) -> hits user's exact intermediate state
# k3 -> k4: 4 steps (frames 12, 13, 14, 15)
# k4 -> k5: 4 steps (frames 16, 17, 18, 19)
# k5 -> k6: 4 steps (frames 20, 21, 22, 23)
# k6 -> k7: 4 steps (frames 24, 25, 26, 27)
segments = [
    (k0_day, k1_glass, 3),
    (k1_glass, k2_preheat, 4),
    (k2_preheat, k3_mid, 4),
    (k3_mid, k4_surge, 4),
    (k4_surge, k5_ignited, 4),
    (k5_ignited, k6_arc, 4),
    (k6_arc, k7_night, 4),
]

frames = [k0_day]
for start_im, end_im, steps in segments:
    for s in range(1, steps + 1):
        t = ease(s / steps)
        blended = Image.blend(start_im, end_im, t)
        frames.append(blended)

print(f"Total frames: {len(frames)} (Expected 28)")

# Save individual webp frames into assets/logo_morph/seq/ for fallback
seq_dir = os.path.join(OUT_DIR, 'seq')
os.makedirs(seq_dir, exist_ok=True)
for i, fr in enumerate(frames):
    fr.save(os.path.join(seq_dir, f'f{i:02d}.webp'), format='WEBP', quality=82, method=4)

# Create 4 cols x 7 rows Sprite Sheet
COLS = 4
ROWS = (len(frames) + COLS - 1) // COLS
sheet = Image.new('RGBA', (COLS * FRAME_W, ROWS * FRAME_H), (0, 0, 0, 0))

for idx, fr in enumerate(frames):
    col = idx % COLS
    row = idx // COLS
    sheet.alpha_composite(fr, (col * FRAME_W, row * FRAME_H))

sheet_path = os.path.join(OUT_DIR, 'morph_spritesheet.webp')
sheet.save(sheet_path, format='WEBP', quality=85, method=4)

sheet_kb = os.path.getsize(sheet_path) / 1024.0
print(f"Sprite Sheet saved: {sheet_path} ({sheet.width}x{sheet.height}) - Weight: {sheet_kb:.1f} KB")
