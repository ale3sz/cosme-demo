import re

with open('app.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "case 'reservar_mesa':" in line:
        new_lines.append(line)
    elif "case 'cumpleanos':" in line:
        new_lines.append(line)
    elif "case 'menu_ejecutivo':" in line:
        new_lines.append(line)
    elif "case 'pasta_libre':" in line:
        new_lines.append(line)
    elif "case 'mesa_amigos':" in line:
        new_lines.append(line)
    elif "case 'take_away':" in line:
        new_lines.append(line)
    elif "¡Hola Cosme Alberdi! ð" in line or "¡Hola Cosme Alberdi! Quiero consultar" in line:
        new_lines.append("        message = '¡Hola Cosme Alberdi! Quiero consultar disponibilidad para reservar una mesa. ¿Me indican horarios y opciones para hoy?';\n")
    elif "¡Hola Cosme! 🎉 Cumplo" in line or "¡Hola Cosme! Cumplo" in line:
        new_lines.append("        message = '¡Hola Cosme! Cumplo años y quiero consultar por promociones de grupo, sector exclusivo y el brindis de regalo.';\n")
    elif "¡Hola Cosme! ð" in line and "Menú Ejecutivo" in line:
        new_lines.append("        message = '¡Hola Cosme! ¿Me podrían pasar las opciones del Menú Ejecutivo del día de hoy con plato, bebida y postre?';\n")
    elif "¡Hola Cosme! ð" in line and "Pasta Libre" in line:
        new_lines.append("        message = '¡Hola Cosme! Quiero reservar para el Jueves de Pasta Libre. ¿Tienen mesa disponible para cenar?';\n")
    elif "¡Hola Cosme Alberdi! ð" in line and "amigos" in line:
        new_lines.append("        message = '¡Hola Cosme Alberdi! Somos un grupo de amigos y queremos coordinar una mesa grande para tomar cerveza tirada y picar.';\n")
    elif "¡Hola Cosme! ð" in line and "retirar por el local" in line:
        new_lines.append("        message = '¡Hola Cosme! Quiero hacer un pedido para retirar por el local de Bv. Rondeau 1602. ¿Me pasan la carta para elegir?';\n")
    elif "const msg = `¡Hola Cosme! 🎉 Somos" in line:
        new_lines.append("        const msg = `¡Hola Cosme! Somos unas *${guests} personas* y queremos festejar en el bar. ¿Me confirman disponibilidad y promos para grupos?`;\n")
    else:
        new_lines.append(line)

with open('app.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("app.js successfully sanitized of emojis and corrupted unicode.")
