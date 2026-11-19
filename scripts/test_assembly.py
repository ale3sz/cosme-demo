import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Navbar Links
old_nav = re.search(r'<nav class="nav-links">[\s\S]*?</nav>', html).group(0)
new_nav = """<nav class="nav-links">
        <a href="#inicio" class="active">Inicio</a>
        <a href="#espacio">El Espacio</a>
        <a href="#menu">Cartas &amp; Canillas</a>
        <a href="#festejos">Reservas &amp; Festejos</a>
        <a href="#ubicacion">Ubicación</a>
      </nav>"""
html = html.replace(old_nav, new_nav, 1)

# 2. Extract sections
hero_match = re.search(r'(<!-- =+[\r\n\s]+2\. HERO SECTION[\s\S]*?<section class="hero">[\s\S]*?</section>)', html)
hero_block = hero_match.group(1)

whatsapp_match = re.search(r'(<!-- =+[\r\n\s]+3\. WHATSAPP PRESETS COMPONENT[\s\S]*?<section id="whatsapp-rapido"[\s\S]*?</section>)', html)
whatsapp_block = whatsapp_match.group(1)

canillas_match = re.search(r'(<!-- =+[\r\n\s]+3B\. PIZARRA DE CANILLAS[\s\S]*?<section id="canillas"[\s\S]*?</section>)', html)
canillas_block = canillas_match.group(1)

menu_match = re.search(r'(<!-- =+[\r\n\s]+4\. SECCI[ÓO]N MEN[ÚU][\s\S]*?<section id="menu"[\s\S]*?</section>)', html)
menu_block = menu_match.group(1)

espacio_match = re.search(r'(<!-- =+[\r\n\s]+5\. BENTO GRID: EL ESPACIO[\s\S]*?<section id="espacio"[\s\S]*?</section>)', html)
espacio_block = espacio_match.group(1)

festejos_match = re.search(r'(<!-- =+[\r\n\s]+6\. FESTEJOS[\s\S]*?<section id="festejos"[\s\S]*?</section>)', html)
festejos_block = festejos_match.group(1)

ubicacion_match = re.search(r'(<!-- =+[\r\n\s]+7\. UBICACI[ÓO]N[\s\S]*?<section id="ubicacion"[\s\S]*?</section>)', html)
ubicacion_block = ubicacion_match.group(1)

print("All 7 blocks extracted successfully!")
