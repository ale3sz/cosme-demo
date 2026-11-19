from lucide_icons import get_icon
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Clean remaining emojis
html = html.replace('<span>💬</span> Reservar Festejo por WhatsApp', f'{get_icon("whatsapp", 16, 0)} Reservar Festejo por WhatsApp')
html = html.replace('<div class="info-icon">📍</div>', f'<div class="info-icon">{get_icon("map-pin", 22, 2.2)}</div>')
html = html.replace('<div class="info-icon">🚗</div>', f'<div class="info-icon">{get_icon("map-pin", 22, 2.2)}</div>')
html = html.replace('<span>🗺️</span> Abrir en Google Maps / Cómo llegar ↗', f'{get_icon("external-link", 15, 2)} Abrir en Google Maps / Cómo llegar')
html = html.replace('<span>📅</span> <span>Reservar mesa</span>', f'{get_icon("calendar", 16, 2)} <span>Reservar mesa</span>')
html = html.replace('<span>🎉</span> <span>Festejar cumpleaños</span>', f'{get_icon("party-popper", 16, 2)} <span>Festejar cumpleaños</span>')
html = html.replace('<span>🍽️</span> <span>Menú del día</span>', f'{get_icon("utensils", 16, 2)} <span>Menú del día</span>')
html = html.replace('<span>🛵</span> <span>Pedir Take Away</span>', f'{get_icon("shopping-bag", 16, 2)} <span>Pedir Take Away</span>')
html = html.replace('<span>💬</span> Confirmar Reserva por WhatsApp', f'{get_icon("whatsapp", 16, 0)} Confirmar Reserva por WhatsApp')
html = html.replace('📂 Abrir Carpeta de Cartas en Google Drive ↗', f'{get_icon("external-link", 16, 2)} Abrir Carpeta de Cartas en Google Drive')
html = html.replace('<span>💬</span> Pedir Carta en PDF por WhatsApp ➔', f'{get_icon("whatsapp", 16, 0)} Pedir Carta en PDF por WhatsApp')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("All remaining emojis purged from index.html!")
