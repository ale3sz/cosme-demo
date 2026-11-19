import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Check espacio section match
espacio_match = re.search(r'<!-- =+[\r\n\s]+3\. BENTO GRID: EL ESPACIO[\s\S]*?<section id="espacio"[\s\S]*?</section>', html)
if espacio_match:
    print("Found espacio block, length:", len(espacio_match.group(0)))
else:
    print("WARNING: espacio block not matched with standard comment, checking without comment")
    espacio_match2 = re.search(r'<section id="espacio"[\s\S]*?</section>', html)
    if espacio_match2:
        print("Found espacio section tag, length:", len(espacio_match2.group(0)))

# 2. Check modal-carta match
modal_match = re.search(r'<div id="modal-carta"[\s\S]*?</div>\s*</div>\s*</div>', html)
if modal_match:
    print("Found modal-carta, length:", len(modal_match.group(0)))
else:
    print("modal-carta check with regex")
    idx = html.find('id="modal-carta"')
    print("idx:", idx)
