"""Secuencia v2: sello negro -> neón con letras del sello (puente) -> neón original.
Todos los frames comparten lienzo 1000x300 y centro óptico para evitar saltos."""
from PIL import Image, ImageFilter
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = os.path.join(ROOT, 'assets', 'logo_morph')
ORIG_NEON = os.path.join(ROOT, 'assets', 'brand', 'cosme_neon_original.png')
W, H = 1000, 300

def fit(im, box_w, box_h):
    im = im.crop(im.getchannel('A').getbbox())
    s = min(box_w / im.width, box_h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    c.alpha_composite(im, ((W - im.width) // 2, (H - im.height) // 2))
    return c

bridge = fit(Image.open(os.path.join(M, 'frame_3_night.png')).convert('RGBA'), 960, 270)
neon = fit(Image.open(ORIG_NEON).convert('RGBA'), 960, 270)

bridge.save(os.path.join(M, 'frame_3_bridge.png'))
# Mezclas: el neón de letras-sello "parpadea" y se reacomoda en los tubos originales
Image.blend(bridge, neon, 0.35).filter(ImageFilter.GaussianBlur(1.2)).save(os.path.join(M, 'frame_4_mix.png'))
Image.blend(bridge, neon, 0.75).save(os.path.join(M, 'frame_5_mix.png'))
neon.save(os.path.join(M, 'frame_6_neon.png'))
print('ok')
