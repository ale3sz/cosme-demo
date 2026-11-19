"""
v3.1: Alineación exacta C-O-S-M-E (excluyendo puntos laterales y ® en TODOS los frames)
y extracción de brillo neón con núcleo blanco-rosa grueso y radiante idéntico al neón final.
"""
import os
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.abspath('.')
BRAIN = r'C:\Users\aleja\.gemini\antigravity\brain\f8f257e2-6a56-4fc7-aea8-60c71038f382'
OUT_DIR = os.path.join(ROOT, 'assets', 'logo_morph')
KEY_DIR = os.path.join(OUT_DIR, 'keyframes_v3')
os.makedirs(KEY_DIR, exist_ok=True)

FRAME_W, FRAME_H = 800, 240
TARGET_LETTER_W = 620.0


def extract_neon_from_white(path, glow_boost=1.0, close_k=11):
    """Extrae neón rojo + núcleo blanco-rosa incandescente radiante desde fondo blanco puro."""
    im = Image.open(path).convert('RGB')
    arr = np.array(im, dtype=np.float32) / 255.0
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]

    # 1. De-white para halo rojo y tinta borgoña
    min_c = np.minimum(np.minimum(r, g), b)
    alpha_glow = np.clip(1.0 - min_c, 0.0, 1.0)

    fg = np.zeros_like(arr)
    mask = alpha_glow > 0.005
    denom = np.maximum(alpha_glow, 0.035)
    for c in range(3):
        fg[:, :, c] = np.where(mask, np.clip(1.0 - (1.0 - arr[:, :, c]) / denom, 0.0, 1.0), 0.0)

    # 2. Detectar SOLO el núcleo blanco-rosa incandescente atrapado dentro de paredes rojas fuertes del tubo
    redness = r - np.minimum(g, b)
    red_wall = (redness > 0.42).astype(np.uint8) * 255
    wall_im = Image.fromarray(red_wall, 'L')
    closed = wall_im.filter(ImageFilter.MaxFilter(close_k)).filter(ImageFilter.MinFilter(close_k))
    closed_f = np.array(closed, dtype=np.float32) / 255.0

    # El núcleo luminoso dentro del tubo cerrado es blanco-rosa brillante (min_c > 0.52)
    core_raw = closed_f * np.clip((min_c - 0.50) / 0.35, 0.0, 1.0)
    core_im = Image.fromarray(np.clip(core_raw * 255, 0, 255).astype(np.uint8), 'L')
    core_soft = np.array(core_im.filter(ImageFilter.GaussianBlur(1.2)), dtype=np.float32) / 255.0

    # Combinar alpha: halo rojo limpio + núcleo opaco
    final_alpha = np.clip(np.maximum(alpha_glow * glow_boost, core_soft * 0.96), 0.0, 1.0)

    # Color: donde hay núcleo blanco-rosa, mezclar hacia blanco-rosa neón (1.0, 0.90, 0.92)
    core_rgb = np.stack([np.ones_like(r), np.full_like(r, 0.88), np.full_like(r, 0.91)], axis=2)
    w_core = np.clip(core_soft * 1.1, 0.0, 1.0)[:, :, None]
    final_rgb = fg * (1.0 - w_core) + core_rgb * w_core

    # Limpiar ruido JPEG muy débil en el fondo exterior
    final_alpha = np.where(final_alpha < 0.025, 0.0, final_alpha)

    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[:, :, :3] = np.clip(final_rgb * 255.0, 0, 255).astype(np.uint8)
    rgba[:, :, 3] = np.clip(final_alpha * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(rgba, 'RGBA')


def get_cosme_letters_bbox(im, x_margin_pct=0.0, alpha_thresh=75):
    """Encuentra el bbox exacto de C-O-S-M-E recortando opcionalmente el margen de los puntos laterales."""
    arr = np.array(im)
    alpha = arr[:, :, 3]
    h, w = alpha.shape
    x0_lim = int(w * x_margin_pct)
    x1_lim = int(w * (1.0 - x_margin_pct))
    sub = alpha[:, x0_lim:x1_lim] > alpha_thresh

    col_has = np.any(sub, axis=0)
    xs = np.where(col_has)[0]
    x_min = int(xs.min()) + x0_lim
    x_max = int(xs.max()) + x0_lim

    ys = np.where(np.any(sub[:, xs.min():xs.max()+1], axis=1))[0]
    y_min, y_max = int(ys.min()), int(ys.max())
    return (x_min, y_min, x_max, y_max)


def align_by_letters(im, x_margin_pct=0.0, alpha_thresh=75):
    bbox = get_cosme_letters_bbox(im, x_margin_pct=x_margin_pct, alpha_thresh=alpha_thresh)
    x_min, y_min, x_max, y_max = bbox
    letter_w = float(x_max - x_min)
    letter_cx = float(x_min + x_max) / 2.0
    letter_cy = float(y_min + y_max) / 2.0

    scale = TARGET_LETTER_W / letter_w
    new_w = round(im.width * scale)
    new_h = round(im.height * scale)
    resized = im.resize((new_w, new_h), Image.LANCZOS)

    pos_x = round((FRAME_W / 2.0) - letter_cx * scale)
    pos_y = round((FRAME_H / 2.0) - letter_cy * scale)

    canvas = Image.new('RGBA', (FRAME_W, FRAME_H), (0, 0, 0, 0))
    canvas.alpha_composite(resized, (pos_x, pos_y))
    return canvas, bbox


# 1. Cargar y procesar los 7 keyframes reales
k0_raw = Image.open(os.path.join(OUT_DIR, 'frame_0_day.png')).convert('RGBA')
k1_raw = Image.open(os.path.join(ROOT, 'assets', 'brand', 'cosme_neon_intermediate.png')).convert('RGBA')
k2_raw = extract_neon_from_white(os.path.join(BRAIN, 'cosme_morph_stage1_30pct_v2_1795066435275.jpg'), glow_boost=1.05)
k3_raw = extract_neon_from_white(os.path.join(BRAIN, 'cosme_morph_stage1_5_42pct_1795066590635.jpg'), glow_boost=1.10)
k4_raw = extract_neon_from_white(os.path.join(BRAIN, 'cosme_morph_stage2_55pct_v2_1795066444000.jpg'), glow_boost=1.12)
k5_raw = extract_neon_from_white(os.path.join(BRAIN, 'cosme_morph_stage3_80pct_v2_1795066444757.jpg'), glow_boost=1.18, close_k=17)
k6_raw = Image.open(os.path.join(ROOT, 'assets', 'brand', 'cosme_neon_original.png')).convert('RGBA')

# x_margin_pct recorta los puntos laterales y ® al medir el ancho de "COSME" (el dibujo completo igual se conserva!)
specs = [
    ('k0_day',      k0_raw, 0.11, 50),
    ('k1_user_mid', k1_raw, 0.09, 75),
    ('k2_30pct',    k2_raw, 0.09, 85),
    ('k3_42pct',    k3_raw, 0.07, 85),
    ('k4_55pct',    k4_raw, 0.04, 85),
    ('k5_80pct',    k5_raw, 0.04, 85),
    ('k6_night',    k6_raw, 0.02, 75),
]

aligned_keys = []
for name, im, xm, thresh in specs:
    al, bbox = align_by_letters(im, x_margin_pct=xm, alpha_thresh=thresh)
    al.save(os.path.join(KEY_DIR, f'{name}.png'))
    aligned_keys.append(al)
    print(f'{name}: bbox={bbox}, w={bbox[2]-bbox[0]}, h={bbox[3]-bbox[1]}')

# 2. Vista previa de los 7 keyframes reales sobre ladrillo oscuro
brick = Image.open(os.path.join(ROOT, 'assets', 'brick_flattened.jpg')).resize((400, 120))
montage = Image.new('RGB', (800, 480), (15, 15, 18))
for idx, im in enumerate(aligned_keys):
    cell = brick.copy()
    sm = im.resize((400, 120), Image.LANCZOS)
    cell.paste(sm, (0, 0), sm)
    montage.paste(cell, ((idx % 2) * 400, (idx // 2) * 120))
montage.save(os.path.join(ROOT, 'preview_7_real_keyframes.jpg'), quality=92)
print('Saved preview_7_real_keyframes.jpg')

# 3. Interpolar suavemente entre los 7 keyframes reales -> 28 frames totales (0..27)
def ease(t):
    return t * t * (3.0 - 2.0 * t)

steps_per_seg = [5, 4, 4, 5, 5, 4]
frames = [aligned_keys[0]]
for seg_idx, n_steps in enumerate(steps_per_seg):
    a = aligned_keys[seg_idx]
    b = aligned_keys[seg_idx + 1]
    for s in range(1, n_steps + 1):
        t = ease(s / n_steps)
        frames.append(Image.blend(a, b, t))

assert len(frames) == 28

seq_dir = os.path.join(OUT_DIR, 'seq')
os.makedirs(seq_dir, exist_ok=True)
for i, fr in enumerate(frames):
    fr.save(os.path.join(seq_dir, f'f{i:02d}.webp'), format='WEBP', quality=80, method=4)

COLS, ROWS = 4, 7
sheet = Image.new('RGBA', (COLS * FRAME_W, ROWS * FRAME_H), (0, 0, 0, 0))
for idx, fr in enumerate(frames):
    sheet.alpha_composite(fr, ((idx % COLS) * FRAME_W, (idx // COLS) * FRAME_H))

sheet_path = os.path.join(OUT_DIR, 'morph_spritesheet.webp')
sheet.save(sheet_path, format='WEBP', quality=80, method=4)
print(f'Master Sprite Sheet v3.1 saved: {sheet_path} ({os.path.getsize(sheet_path)/1024:.1f} KB)')
