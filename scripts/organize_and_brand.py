import os
import shutil
import cv2
import numpy as np

def organize():
    os.makedirs('scripts', exist_ok=True)
    os.makedirs('media/raw', exist_ok=True)
    os.makedirs('docs', exist_ok=True)
    os.makedirs('brand/mascot', exist_ok=True)
    os.makedirs('brand/wordmark', exist_ok=True)
    os.makedirs('brand/lockup', exist_ok=True)

    # 1. Move python utility scripts to scripts/
    py_files = [f for f in os.listdir('.') if f.endswith('.py') and f != 'organize_and_brand.py']
    for pf in py_files:
        dest = os.path.join('scripts', pf)
        print(f"Moving {pf} -> {dest}")
        shutil.move(pf, dest)

    # 2. Move raw media to media/raw/ and ensure copies in assets/ if needed
    raw_media = [
        'barra.jpg',
        'cartel cosme neon.jpg',
        'noche cosme.jpg',
        'moodboard_completo_cosme.jpg',
        'logo neon cosme.jpg',
        'cosmo logo neon png.png',
        'qr_celular.png',
        'logo cosme.jfif'
    ]
    for rm in raw_media:
        if os.path.exists(rm):
            # If assets/noche cosme.jpg was referenced, copy it to assets/noche-cosme.jpg or assets/noche cosme.jpg
            if rm == 'noche cosme.jpg':
                shutil.copy2(rm, os.path.join('assets', rm))
            dest = os.path.join('media/raw', rm)
            print(f"Moving {rm} -> {dest}")
            shutil.move(rm, dest)

    # 3. Move large dossier to docs/
    if os.path.exists('dossier_cosme_alberdi.html'):
        shutil.move('dossier_cosme_alberdi.html', os.path.join('docs', 'dossier_cosme_alberdi.html'))
        print("Moved dossier_cosme_alberdi.html -> docs/")

def generate_svg_and_brand_assets():
    # 4. Generate SVGs for wordmark and mascot
    # Wordmark SVG
    wm_path = 'brand/wordmark/cosme-wordmark-black.png'
    if os.path.exists(wm_path):
        wm = cv2.imread(wm_path, cv2.IMREAD_UNCHANGED)
        h, w = wm.shape[:2]
        ret, thresh_wm = cv2.threshold(wm[:, :, 3], 127, 255, 0)
        contours_wm, hier_wm = cv2.findContours(thresh_wm, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        paths = []
        for c in contours_wm:
            if cv2.contourArea(c) < 2:
                continue
            approx = cv2.approxPolyDP(c, 0.7, True)
            if len(approx) < 3:
                continue
            pts = approx.reshape(-1, 2)
            d = f"M {pts[0][0]} {pts[0][1]} " + " ".join(f"L {p[0]} {p[1]}" for p in pts[1:]) + " Z"
            paths.append(d)
        
        d_combined = " ".join(paths)
        svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <path fill="currentColor" fill-rule="evenodd" d="{d_combined}" />
</svg>'''
        with open('brand/wordmark/cosme-wordmark.svg', 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print("Generated brand/wordmark/cosme-wordmark.svg")

    # Mascot SVG
    mascot_path = 'brand/mascot/cosme-mascot-black.png'
    if os.path.exists(mascot_path):
        mascot = cv2.imread(mascot_path, cv2.IMREAD_UNCHANGED)
        mh, mw = mascot.shape[:2]
        ret, thresh_m = cv2.threshold(mascot[:, :, 3], 127, 255, 0)
        contours_m, hier_m = cv2.findContours(thresh_m, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        paths_m = []
        for c in contours_m:
            if cv2.contourArea(c) < 4:
                continue
            approx = cv2.approxPolyDP(c, 0.9, True)
            if len(approx) < 3:
                continue
            pts = approx.reshape(-1, 2)
            d = f"M {pts[0][0]} {pts[0][1]} " + " ".join(f"L {p[0]} {p[1]}" for p in pts[1:]) + " Z"
            paths_m.append(d)
        
        d_m_combined = " ".join(paths_m)
        svg_m_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {mw} {mh}" width="100%" height="100%">
  <path fill="currentColor" fill-rule="evenodd" d="{d_m_combined}" />
</svg>'''
        with open('brand/mascot/cosme-mascot.svg', 'w', encoding='utf-8') as f:
            f.write(svg_m_content)
        print("Generated brand/mascot/cosme-mascot.svg")

if __name__ == '__main__':
    organize()
    generate_svg_and_brand_assets()
