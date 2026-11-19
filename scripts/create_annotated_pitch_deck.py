import os, sys, time, threading
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.pdfgen import canvas

PORT = 8923
class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

server = HTTPServer(('127.0.0.1', PORT), QuietHandler)
t = threading.Thread(target=server.serve_forever, daemon=True)
t.start()
time.sleep(1)

out_dir = "pitch_assets"
os.makedirs(out_dir, exist_ok=True)
os.makedirs("docs", exist_ok=True)
URL = f"http://127.0.0.1:{PORT}/index.html"

print("Capturing screenshots with Playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    
    # 1. Desktop Night Hero
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.goto(URL, wait_until="networkidle")
    time.sleep(2)
    page.screenshot(path=f"{out_dir}/01_raw_hero_night.png")
    
    # 2. Toggle to Day Mode
    page.locator("#theme-toggle-btn").click()
    time.sleep(1.5)
    page.screenshot(path=f"{out_dir}/02_raw_hero_day.png")
    
    # Toggle back to Night
    page.locator("#theme-toggle-btn").click()
    time.sleep(1)
    
    # 3. Pizarra de Canillas
    page.locator("[data-menu-target='taps']").click()
    time.sleep(1)
    canillas_el = page.locator("#canillas")
    canillas_el.scroll_into_view_if_needed()
    time.sleep(1)
    page.screenshot(path=f"{out_dir}/03_raw_canillas.png")
    
    # 4. Festejos / Calculador de Cumpleaños (Mobile Viewport)
    page_mob = browser.new_page(viewport={"width": 412, "height": 915})
    page_mob.goto(URL, wait_until="networkidle")
    time.sleep(1.5)
    festejos_el = page_mob.locator("#festejos")
    festejos_el.scroll_into_view_if_needed()
    time.sleep(1)
    page_mob.screenshot(path=f"{out_dir}/04_raw_festejos_mobile.png")
    
    # 5. Modal Reserva Mesa (Desktop)
    page.locator("[data-open-modal='reserva']").first.click()
    time.sleep(1)
    page.screenshot(path=f"{out_dir}/05_raw_modal_reserva.png")
    
    browser.close()

print("Screenshots captured successfully.")

def get_font(size, bold=False):
    font_paths = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "arial.ttf"
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except:
                pass
    return ImageFont.load_default()

def draw_callout(draw, x, y, w, h, title, text, color="#FF1E27", font_title=None, font_text=None):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=(18, 20, 24, 240), outline=color, width=3)
    draw.text((x + 14, y + 10), title, fill=color, font=font_title)
    draw.text((x + 14, y + 36), text, fill=(240, 240, 245), font=font_text)

def draw_arrow(draw, start, end, color="#FF1E27", width=4):
    draw.line([start, end], fill=color, width=width)
    ex, ey = end
    sx, sy = start
    import math
    angle = math.atan2(ey - sy, ex - sx)
    arrow_len = 16
    arrow_angle = math.pi / 6
    x1 = ex - arrow_len * math.cos(angle - arrow_angle)
    y1 = ey - arrow_len * math.sin(angle - arrow_angle)
    x2 = ex - arrow_len * math.cos(angle + arrow_angle)
    y2 = ey - arrow_len * math.sin(angle + arrow_angle)
    draw.polygon([end, (x1, y1), (x2, y2)], fill=color)

print("Annotating screenshots with callouts...")
font_h1 = get_font(20, bold=True)
font_p = get_font(15, bold=False)

# 1. Annotate Hero Night
img1 = Image.open(f"{out_dir}/01_raw_hero_night.png").convert("RGBA")
d1 = ImageDraw.Draw(img1)
draw_callout(d1, 380, 210, 420, 85, "1. MOTOR DE HORARIO EN VIVO", "Detecta si el local esta abierto o cerrado en tiempo real.\nEvita que los clientes consulten '¿abren hoy?' por WhatsApp.", "#25D366", font_h1, font_p)
draw_arrow(d1, (590, 210), (720, 160), "#25D366", 4)

draw_callout(d1, 980, 90, 420, 85, "2. MODO DUAL DIA / NOCHE", "Switch interactivo: Cafeteria y brunch de dia,\nCerveceria, hamburguesas y bodegon de noche.", "#FFAA00", font_h1, font_p)
draw_arrow(d1, (1260, 90), (1330, 40), "#FFAA00", 4)

draw_callout(d1, 70, 720, 430, 85, "3. ACCESOS RAPIDOS SIN FRICCION", "Botones directos para Reservar Mesa, ver Carta\ny calcular Festejos sin perderse navegando.", "#FF1E27", font_h1, font_p)
draw_arrow(d1, (500, 760), (600, 770), "#FF1E27", 4)
img1.convert("RGB").save(f"{out_dir}/01_annotated_hero_night.png")

# 2. Annotate Hero Day
img2 = Image.open(f"{out_dir}/02_raw_hero_day.png").convert("RGBA")
d2 = ImageDraw.Draw(img2)
draw_callout(d2, 50, 120, 450, 90, "TRANSICION A MODO DIA (CAFE & BRUNCH)", "Al cambiar a Modo Dia, la web adapta su estetica rústica\ny muestra cafes de especialidad, chipás y menú ejecutivo.", "#288062", font_h1, font_p)
draw_arrow(d2, (500, 150), (680, 150), "#288062", 4)
img2.convert("RGB").save(f"{out_dir}/02_annotated_hero_day.png")

# 3. Annotate Canillas
img3 = Image.open(f"{out_dir}/03_raw_canillas.png").convert("RGBA")
d3 = ImageDraw.Draw(img3)
draw_callout(d3, 40, 200, 460, 95, "PIZARRA VIVA DE 12 CANILLAS", "Muestra en tiempo real los estilos pinchados, graduacion e IBU.\nFiltros rapidos: Rubia, Roja, Negra o Lupulada.", "#FFAA00", font_h1, font_p)
draw_arrow(d3, (500, 240), (560, 240), "#FFAA00", 4)

draw_callout(d3, 930, 420, 470, 95, "PEDIDO DIRECTO A WHATSAPP", "Cada canilla tiene un boton que dispara un WhatsApp:\n'Hola Cosme! Quiero pedir una pinta de Golden...'", "#FF1E27", font_h1, font_p)
draw_arrow(d3, (930, 470), (840, 470), "#FF1E27", 4)
img3.convert("RGB").save(f"{out_dir}/03_annotated_canillas.png")

# 4. Annotate Festejos Mobile
img4 = Image.open(f"{out_dir}/04_raw_festejos_mobile.png").convert("RGBA")
d4 = ImageDraw.Draw(img4)
draw_callout(d4, 15, 80, 380, 100, "CALCULADOR DE CUMPLEAÑOS", "El cliente desliza la cantidad de invitados.\nCalcula en vivo beneficios (Champagne, DJ, Comida Libre)\ny manda la cotización lista a su WhatsApp.", "#FFAA00", get_font(17, bold=True), get_font(13, bold=False))
draw_arrow(d4, (200, 180), (200, 280), "#FFAA00", 4)
img4.convert("RGB").save(f"{out_dir}/04_annotated_festejos_mobile.png")

# 5. Annotate Modal Reserva
img5 = Image.open(f"{out_dir}/05_raw_modal_reserva.png").convert("RGBA")
d5 = ImageDraw.Draw(img5)
draw_callout(d5, 80, 260, 430, 100, "RESERVA AGIL (ZERO FRICTION)", "Formulario express de 4 campos simples.\nEl cliente no debe registrarse: envía nombre, comensales,\nfecha y turno directo al WhatsApp del bar.", "#FF1E27", font_h1, font_p)
draw_arrow(d5, (510, 310), (600, 310), "#FF1E27", 4)
img5.convert("RGB").save(f"{out_dir}/05_annotated_modal_reserva.png")

print("Annotated images saved.")

# PDF Generation
pdf_path = "docs/Presentacion_Cosme_Alberdi.pdf"
page_w, page_h = landscape(letter)
c = canvas.Canvas(pdf_path, pagesize=landscape(letter))

def draw_header_footer(c, title, category="PROPUESTA WEB INTERACTIVA"):
    c.setFillColor(colors.HexColor("#0B0C0E"))
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)
    
    c.setFillColor(colors.HexColor("#14161B"))
    c.rect(0, page_h - 60, page_w, 60, fill=1, stroke=0)
    
    c.setFillColor(colors.HexColor("#FF1E27"))
    c.rect(0, page_h - 63, page_w, 3, fill=1, stroke=0)
    
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.HexColor("#FF1E27"))
    c.drawString(36, page_h - 26, category)
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.white)
    c.drawString(36, page_h - 48, title)
    
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor("#FFAA00"))
    c.drawRightString(page_w - 36, page_h - 38, "COSME ALBERDI")
    
    c.setFillColor(colors.HexColor("#14161B"))
    c.rect(0, 0, page_w, 30, fill=1, stroke=0)
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#8C919D"))
    c.drawString(36, 10, "Bv. Rondeau 1602, Rosario · Desarrollo Web y Soluciones de Conversion Gastronomica")
    c.drawRightString(page_w - 36, 10, "Presentacion de Maqueta Funcional")

# Slide 1: Cover
c.setFillColor(colors.HexColor("#0B0C0E"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

c.setFillColor(colors.HexColor("#1A1215"))
c.roundRect(page_w/2 - 200, page_h/2 + 110, 400, 35, 10, fill=1, stroke=1)
c.setFont("Helvetica-Bold", 12)
c.setFillColor(colors.HexColor("#FF1E27"))
c.drawCentredString(page_w/2, page_h/2 + 122, "CANAL DIRECTO DE RESERVAS & VENTAS")

c.setFont("Helvetica-Bold", 38)
c.setFillColor(colors.white)
c.drawCentredString(page_w/2, page_h/2 + 50, "COSME ALBERDI")

c.setFont("Helvetica-Bold", 18)
c.setFillColor(colors.HexColor("#FFAA00"))
c.drawCentredString(page_w/2, page_h/2 + 20, "PLATAFORMA WEB INTERACTIVA & MOTOR DE CONVERSION")

c.setFont("Helvetica", 12)
c.setFillColor(colors.HexColor("#D1D5DB"))
c.drawCentredString(page_w/2, page_h/2 - 30, "Una web disenada especificamente para llenar mesas los dias de baja demanda,")
c.drawCentredString(page_w/2, page_h/2 - 48, "cerrar mesas grandes de cumpleanos y modernizar las cartas sin costos de imprenta.")

p_y = page_h/2 - 120
box_w = 210
box_h = 70
c.setFillColor(colors.HexColor("#16181E"))

c.roundRect(70, p_y, box_w, box_h, 8, fill=1, stroke=0)
c.setFont("Helvetica-Bold", 11)
c.setFillColor(colors.HexColor("#FF1E27"))
c.drawString(85, p_y + 46, "1. GRUPOS & CUMPLES")
c.setFont("Helvetica", 9)
c.setFillColor(colors.HexColor("#9CA3AF"))
c.drawString(85, p_y + 28, "Calculador de invitados y")
c.drawString(85, p_y + 14, "cierre rapido por WhatsApp.")

c.roundRect(290, p_y, box_w, box_h, 8, fill=1, stroke=0)
c.setFont("Helvetica-Bold", 11)
c.setFillColor(colors.HexColor("#25D366"))
c.drawString(305, p_y + 46, "2. AHORRO DE TIEMPO")
c.setFont("Helvetica", 9)
c.setFillColor(colors.HexColor("#9CA3AF"))
c.drawString(305, p_y + 28, "Horarios en vivo y reservas")
c.drawString(305, p_y + 14, "automaticas sin llamadas.")

c.roundRect(510, p_y, box_w, box_h, 8, fill=1, stroke=0)
c.setFont("Helvetica-Bold", 11)
c.setFillColor(colors.HexColor("#FFAA00"))
c.drawString(525, p_y + 46, "3. CARTA & 12 CANILLAS")
c.setFont("Helvetica", 9)
c.setFillColor(colors.HexColor("#9CA3AF"))
c.drawString(525, p_y + 28, "Carta viva y canillas al dia")
c.drawString(525, p_y + 14, "sin reimpresion por inflacion.")

c.showPage()

# Slide 2: Hero & Dual Mode
draw_header_footer(c, "Experiencia Dual: Dia (Cafe) y Noche (Pub & Birreria)", "MODO DUAL & HORARIO VIVO")
c.drawImage(f"{out_dir}/01_annotated_hero_night.png", 36, 60, width=470, height=450, preserveAspectRatio=True)

tx = 530
ty = 460
c.setFont("Helvetica-Bold", 15)
c.setFillColor(colors.HexColor("#FFAA00"))
c.drawString(tx, ty, "Puntos Clave del Inicio:")

bullets = [
    ("Estado en Tiempo Real (UTC-3):", "Indica si el local esta abierto con punto verde pulsante. Avisa si es turno desayuno, almuerzo o noche."),
    ("Switch Dia / Noche Inmediato:", "El cliente puede alternar en un clic entre la propuesta cafetera y la cerveceria nocturna."),
    ("Botones de Conversion Directa:", "Sin rodeos: reservas de mesa, cartas completas y festejos al alcance del pulgar.")
]
for title, desc in bullets:
    ty -= 35
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.white)
    c.drawString(tx, ty, f"• {title}")
    ty -= 18
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#9CA3AF"))
    words = desc.split()
    line = ""
    for w in words:
        if len(line + " " + w) < 40:
            line += " " + w
        else:
            c.drawString(tx + 12, ty, line.strip())
            ty -= 14
            line = w
    if line:
        c.drawString(tx + 12, ty, line.strip())
    ty -= 10

c.drawImage(f"{out_dir}/02_annotated_hero_day.png", tx, 60, width=225, height=140, preserveAspectRatio=True)
c.showPage()

# Slide 3: Pizarra de Canillas
draw_header_footer(c, "Pizarra Interactiva de 12 Canillas con Pedido Directo", "CERVECERIA ARTESANAL")
c.drawImage(f"{out_dir}/03_annotated_canillas.png", 36, 60, width=480, height=450, preserveAspectRatio=True)

tx = 540
ty = 460
c.setFont("Helvetica-Bold", 15)
c.setFillColor(colors.HexColor("#FFAA00"))
c.drawString(tx, ty, "Ventajas de la Pizarra Viva:")

b_canillas = [
    ("12 Estilos al Momento:", "Muestra estilo, IBU, graduacion alcoholica y notas de cata para el publico cervecero."),
    ("Filtros por Paladar:", "El cliente filtra en 1 toque por Rubia, Roja, Negra o Lupulada (IPA, APA)."),
    ("Pedido / Recarga a WhatsApp:", "Cada canilla incluye un boton que abre WhatsApp con el estilo exacto listo para pedir o recargar growler.")
]
for title, desc in b_canillas:
    ty -= 35
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.white)
    c.drawString(tx, ty, f"• {title}")
    ty -= 18
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#9CA3AF"))
    words = desc.split()
    line = ""
    for w in words:
        if len(line + " " + w) < 40:
            line += " " + w
        else:
            c.drawString(tx + 12, ty, line.strip())
            ty -= 14
            line = w
    if line:
        c.drawString(tx + 12, ty, line.strip())
    ty -= 10

c.showPage()

# Slide 4: Calculador Festejos
draw_header_footer(c, "Calculador de Festejos y Cumpleanos (Ticket Alto)", "EMBUDO DE EVENTOS")
c.drawImage(f"{out_dir}/04_annotated_festejos_mobile.png", 50, 45, width=280, height=480, preserveAspectRatio=True)

tx = 360
ty = 460
c.setFont("Helvetica-Bold", 16)
c.setFillColor(colors.HexColor("#FF1E27"))
c.drawString(tx, ty, "El Generador de Mayor Rentabilidad del Bar:")

b_fest = [
    ("Los cumpleanos salvan noches:", "Una sola mesa de 15 a 30 personas genera una facturacion enorme. La gente suele reservar donde le facilitan todo rapido."),
    ("Beneficios Claros por Escala:", "Segun los invitados seleccionados con el slider, la web ofrece automaticamente:"),
    (" - Menos de 10 personas:", "1 Espumante de regalo + Mesa preferencial."),
    (" - De 10 a 20 personas:", "2 Espumantes + Menu Comida Libre de pizzas/papas."),
    (" - Mas de 20 personas:", "3 Espumantes + Sector exclusivo + DJ y Cotillon LED."),
    ("Mensaje masticado:", "El boton de WhatsApp ya envia fecha, cantidad de invitados y paquete consultado para senar en el acto.")
]

for title, desc in b_fest:
    ty -= 24
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.white)
    c.drawString(tx, ty, title)
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.HexColor("#9CA3AF"))
    c.drawString(tx + 15, ty - 12, desc)
    ty -= 12

c.showPage()

# Slide 5: Reserva de Mesa Agil
draw_header_footer(c, "Reserva de Mesas sin Friccion (Cero Burocracia)", "RESERVAS RAPIDAS")
c.drawImage(f"{out_dir}/05_annotated_modal_reserva.png", 36, 60, width=470, height=450, preserveAspectRatio=True)

tx = 530
ty = 460
c.setFont("Helvetica-Bold", 15)
c.setFillColor(colors.HexColor("#25D366"))
c.drawString(tx, ty, "Reserva en 15 Segundos:")

b_res = [
    ("Cero barreras de entrada:", "El comensal no tiene que crearse cuentas ni recordar contrasenas."),
    ("4 Datos Clave:", "Nombre, cantidad de personas, fecha y turno deseado."),
    ("Llega al WhatsApp del Encargado:", "El mensaje llega con el formato exacto para que el personal solo responda: 'Confirmado! Los esperamos'."),
    ("Ahorro de 1 hora diaria:", "Elimina las llamadas telefonicas en pleno servicio y el cruce interminable de mensajes.")
]
for title, desc in b_res:
    ty -= 35
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(colors.white)
    c.drawString(tx, ty, f"• {title}")
    ty -= 18
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.HexColor("#9CA3AF"))
    words = desc.split()
    line = ""
    for w in words:
        if len(line + " " + w) < 38:
            line += " " + w
        else:
            c.drawString(tx + 12, ty, line.strip())
            ty -= 14
            line = w
    if line:
        c.drawString(tx + 12, ty, line.strip())
    ty -= 10

c.showPage()

# Slide 6: Next steps
c.setFillColor(colors.HexColor("#0B0C0E"))
c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

c.setFont("Helvetica-Bold", 26)
c.setFillColor(colors.HexColor("#FFAA00"))
c.drawCentredString(page_w/2, page_h - 100, "LISTO PARA IMPLEMENTAR EN COSME ALBERDI")

c.setFont("Helvetica", 12)
c.setFillColor(colors.HexColor("#D1D5DB"))
c.drawCentredString(page_w/2, page_h - 130, "La plataforma ya cuenta con todo el diseno, identidad y logica operativa resuelta.")

sy = page_h - 320
card_w = 210
card_h = 150

# Card 1
c.setFillColor(colors.HexColor("#16181E"))
c.roundRect(65, sy, card_w, card_h, 10, fill=1, stroke=1)
c.setFont("Helvetica-Bold", 18)
c.setFillColor(colors.HexColor("#FF1E27"))
c.drawString(85, sy + card_h - 30, "PASO 1")
c.setFont("Helvetica-Bold", 12)
c.setFillColor(colors.white)
c.drawString(85, sy + card_h - 55, "Ajuste de Precios")
c.setFont("Helvetica", 9)
c.setFillColor(colors.HexColor("#9CA3AF"))
c.drawString(85, sy + 70, "Nos pasan la lista de precios")
c.drawString(85, sy + 55, "actualizada de cocina y")
c.drawString(85, sy + 40, "las canillas activas.")

# Card 2
c.setFillColor(colors.HexColor("#16181E"))
c.roundRect(290, sy, card_w, card_h, 10, fill=1, stroke=1)
c.setFont("Helvetica-Bold", 18)
c.setFillColor(colors.HexColor("#25D366"))
c.drawString(310, sy + card_h - 30, "PASO 2")
c.setFont("Helvetica-Bold", 12)
c.setFillColor(colors.white)
c.drawString(310, sy + card_h - 55, "Dominio Oficial")
c.setFont("Helvetica", 9)
c.setFillColor(colors.HexColor("#9CA3AF"))
c.drawString(310, sy + 70, "Habilitamos el dominio propio")
c.drawString(310, sy + 55, "(ej. cosmealberdi.com.ar)")
c.drawString(310, sy + 40, "con conexion segura SSL.")

# Card 3
c.setFillColor(colors.HexColor("#16181E"))
c.roundRect(515, sy, card_w, card_h, 10, fill=1, stroke=1)
c.setFont("Helvetica-Bold", 18)
c.setFillColor(colors.HexColor("#FFAA00"))
c.drawString(535, sy + card_h - 30, "PASO 3")
c.setFont("Helvetica-Bold", 12)
c.setFillColor(colors.white)
c.drawString(535, sy + card_h - 55, "Lanzamiento & QR")
c.setFont("Helvetica", 9)
c.setFillColor(colors.HexColor("#9CA3AF"))
c.drawString(535, sy + 70, "Entregamos el codigo QR en")
c.drawString(535, sy + 55, "alta resolucion para mesas y")
c.drawString(535, sy + 40, "el link para bio de Instagram.")

c.setFont("Helvetica-Bold", 14)
c.setFillColor(colors.white)
c.drawCentredString(page_w/2, 100, "¿Coordinamos 5 minutos para verlo en vivo desde el celular?")

c.setFont("Helvetica-Bold", 12)
c.setFillColor(colors.HexColor("#25D366"))
c.drawCentredString(page_w/2, 75, "Alejandro · Desarrollo Web & Soluciones Digitales · Rosario")

c.showPage()
c.save()

print(f"Presentation successfully generated at: {pdf_path}")
sys.exit(0)
