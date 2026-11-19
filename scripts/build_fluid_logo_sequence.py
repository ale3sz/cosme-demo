"""
Generador de secuencia fluida de alta definición para el logo de Cosme Alberdi:
Día (Sello negro) -> Calentamiento -> Neón sobre borgoña (Intermedio) -> Arco de Alta Tensión -> Neón Doble Tubo Bar (Noche).
"""
import os, glob
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np

ROOT = os.path.abspath('.')
OUT = os.path.join(ROOT, 'assets', 'logo_morph', 'seq')
os.makedirs(OUT, exist_ok=True)

SIZE = (800, 240)
W, H = SIZE
BOX_W, BOX_H = 740, 200

def fit_canvas(im):
    # Crop to alpha content and center into (W, H)
    arr = np.array(im)
    m = arr[:,:,3] > 10
    y, x = np.where(m)
    cropped = im.crop((x.min(), y.min(), x.max(), y.max()))
    scale = min(BOX_W / cropped.width, BOX_H / cropped.height)
    new_w = round(cropped.width * scale)
    new_h = round(cropped.height * scale)
    resized = cropped.resize((new_w, new_h), Image.LANCZOS)
    canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((W - new_w) // 2, (H - new_h) // 2))
    return canvas

# 1. Base Keyframes
day_raw = Image.open(os.path.join(ROOT, 'assets', 'logo_morph', 'frame_0_day.png')).convert('RGBA')
user_raw = Image.open(os.path.join(ROOT, 'assets', 'brand', 'cosme_neon_intermediate.png')).convert('RGBA')
neon_raw = Image.open(os.path.join(ROOT, 'assets', 'brand', 'cosme_neon_original.png')).convert('RGBA')

k_day = fit_canvas(day_raw)
k_intermediate = fit_canvas(user_raw)
k_night = fit_canvas(neon_raw)

# 2. Derive helper keyframes:
# k_preheat: Subtle glass tube reflection and warm dark red contour
k_preheat = Image.blend(k_day, k_intermediate, 0.35)

# k_surge: Intermediate with intense core highlight (high voltage arc)
arr_surge = np.array(k_intermediate, dtype=np.float32)
# Boost the bright red tube borders
bright_mask = (arr_surge[:,:,0] > 170) & (arr_surge[:,:,3] > 120)
arr_surge[bright_mask, 1] += 100  # white-pink core
arr_surge[bright_mask, 2] += 90
# Also make interior burgundy glow warmer
dark_fill = (arr_surge[:,:,3] > 80) & (arr_surge[:,:,0] < 160)
arr_surge[dark_fill, 0] = np.clip(arr_surge[dark_fill, 0] * 1.8 + 40, 0, 255)
arr_surge = np.clip(arr_surge, 0, 255).astype(np.uint8)
k_surge = Image.fromarray(arr_surge, 'RGBA')

# k_arc_flash: High-intensity electrical strike bridging the two signs
arr_flash = np.array(k_night, dtype=np.float32)
# Mix with surge at peak light
flash_blend = Image.blend(k_surge, k_night, 0.5)
enhancer = ImageEnhance.Brightness(flash_blend.convert('RGB'))
flash_rgb = enhancer.enhance(1.4)
flash_rgb.putalpha(flash_blend.getchannel('A'))
k_arc_flash = flash_rgb.filter(ImageFilter.GaussianBlur(0.8))

def ease(t):
    return t * t * (3.0 - 2.0 * t)

# Segments:
# 1. Day -> Preheat: 4 frames
# 2. Preheat -> Intermediate (User's stage): 5 frames
# 3. Intermediate -> Surge: 4 frames
# 4. Surge -> Arc Flash: 3 frames (fast electrical pulse)
# 5. Arc Flash -> Night: 5 frames (stabilizing double line neon)
segments = [
    (k_day, k_preheat, 4),
    (k_preheat, k_intermediate, 5),
    (k_intermediate, k_surge, 4),
    (k_surge, k_arc_flash, 3),
    (k_arc_flash, k_night, 5),
]

all_frames = [k_day]
for start_im, end_im, steps in segments:
    for s in range(1, steps + 1):
        t = ease(s / steps)
        blended = Image.blend(start_im, end_im, t)
        all_frames.append(blended)

# Save all frames
for f in glob.glob(os.path.join(OUT, '*.webp')):
    try: os.remove(f)
    except: pass

for idx, fr in enumerate(all_frames):
    out_file = os.path.join(OUT, f'f{idx:02d}.webp')
    fr.save(out_file, format='WEBP', quality=80, method=5)

total_kb = sum(os.path.getsize(os.path.join(OUT, f'f{i:02d}.webp')) for i in range(len(all_frames))) / 1024.0
print(f'Generated {len(all_frames)} frames successfully! Total weight: {total_kb:.1f} KB (Avg {total_kb/len(all_frames):.1f} KB/frame)')
