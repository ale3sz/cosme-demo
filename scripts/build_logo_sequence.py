"""Genera la secuencia fluida sello -> neón original (frames intermedios interpolados).
Salida: assets/logo_morph/seq/f00.webp ... (día = f00, noche = último)."""
from PIL import Image, ImageEnhance, ImageFilter
import os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(ROOT, 'assets', 'logo_morph')
OUT = os.path.join(M, 'seq')
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, '*')):
    os.remove(f)
SIZE = (800, 240)

def load(n):
    return Image.open(os.path.join(M, n)).convert('RGBA').resize(SIZE, Image.LANCZOS)

A, H, S, B, N = [load(n) for n in ['frame_0_day.png', 'frame_1_heat.png', 'frame_2_spark.png',
                                   'frame_3_bridge.png', 'frame_6_neon.png']]

def ease(t):
    return t * t * (3 - 2 * t)

def bright(im, k):
    rgb = ImageEnhance.Brightness(im.convert('RGB')).enhance(k)
    rgb.putalpha(im.getchannel('A'))
    return rgb

# (desde, hasta, pasos, brillo extra opcional por paso)
segments = [
    (A, H, 3, None),
    (H, S, 2, [1.0, 1.25]),          # chispazo
    (S, B, 3, [1.15, 0.85, 1.05]),   # parpadeo de encendido
    (B, N, 5, None),                  # las letras-sello se acomodan en los tubos originales
]
frames = [A]
for a, b, n, flick in segments:
    for i in range(1, n + 1):
        t = ease(i / n)
        f = Image.blend(a, b, t)
        if b is N and 0 < t < 1:
            # leve desenfoque en el cruce para que no se lea doble
            f = f.filter(ImageFilter.GaussianBlur(1.6 * (1 - abs(2 * t - 1))))
        if flick:
            f = bright(f, flick[i - 1])
        frames.append(f)

for i, f in enumerate(frames):
    f.save(os.path.join(OUT, f'f{i:02d}.webp'), quality=82, method=6)
print(len(frames), 'frames')
