import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find sections with comments
sections = [
    ('hero', r'<!-- =+[\r\n\s]+2\. HERO SECTION[\r\n\s]+=+\s*-->[\s\S]*?<section class="hero">[\s\S]*?</section>'),
    ('whatsapp', r'<!-- =+[\r\n\s]+3\. WHATSAPP PRESETS COMPONENT[\s\S]*?<section id="whatsapp-rapido"[\s\S]*?</section>'),
    ('canillas', r'<!-- =+[\r\n\s]+3B\. PIZARRA DE CANILLAS[\s\S]*?<section id="canillas"[\s\S]*?</section>'),
    ('menu', r'<!-- =+[\r\n\s]+4\. SECCI[ÓO]N MEN[ÚU][\s\S]*?<section id="menu"[\s\S]*?</section>'),
    ('espacio', r'<!-- =+[\r\n\s]+5\. BENTO GRID: EL ESPACIO[\s\S]*?<section id="espacio"[\s\S]*?</section>'),
    ('festejos', r'<!-- =+[\r\n\s]+6\. FESTEJOS[\s\S]*?<section id="festejos"[\s\S]*?</section>'),
    ('ubicacion', r'<!-- =+[\r\n\s]+7\. UBICACI[ÓO]N[\s\S]*?<section id="ubicacion"[\s\S]*?</section>')
]

for name, pattern in sections:
    match = re.search(pattern, html)
    if match:
        print(f"Match found for {name}: {len(match.group(0))} chars")
    else:
        print(f"FAILED to match {name}")
