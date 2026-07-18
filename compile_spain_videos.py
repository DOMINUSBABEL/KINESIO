import os
import sys
import re
import time
import shutil
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

# Widescreen Essays configuration (Spain campaign - 5 Essays)
ESSAYS_DATA = {
    "spain_essay_1": {
        "title": "ESPAÑA Y EL SUEÑO MUNDIALISTA",
        "badge": "LA ROJA ⚽",
        "music": "Volatile Reaction.mp3",
        "bg_name": "spain_team.jpg",
        "chapters": {
            1: {"subtitle": "El Regreso de un Gigante a la Elite", "bullets": ["✔ Superando la transición generacional", "✔ Humildad, esfuerzo y convicción", "✔ El respeto ganado de todo el planeta"], "badge": "EL REGRESO 👑"},
            2: {"subtitle": "La Filosofía de Luis de la Fuente", "bullets": ["✔ El conocimiento de las inferiores", "✔ Cercanía humana y sencillez táctica", "✔ El catalizador del cambio colectivo"], "badge": "EL MÍSTER 📋"},
            3: {"subtitle": "El Cambio del Tiki-Taka al Ritmo Vertical", "bullets": ["✔ Posesión con ataque directo y veloz", "✔ Desequilibrio letal por las bandas", "✔ Capacidad de contragolpe fulminante"], "badge": "TÁCTICA ⚡"},
            4: {"subtitle": "La Madurez del Bloque de Veteranos", "bullets": ["✔ Guías emocionales en momentos de tensión", "✔ Control de los tiempos del partido", "✔ Equilibrio absoluto en el vestuario"], "badge": "LIDERAZGO 🛡"},
            5: {"subtitle": "La Ilusión Desbordada de un País", "bullets": ["✔ Calles teñidas de rojo y amarillo", "✔ Multitudes unidas por la pasión", "✔ El sueño de conquistar el mundo otra vez"], "badge": "HINCHADA 🇪🇸"},
            6: {"subtitle": "El Umbral del Destino y de la Gloria", "bullets": ["✔ A solo noventa minutos de la eternidad", "✔ Preparación física y fuerza mental", "✔ La cita con la historia del fútbol"], "badge": "EL DESTINO 🏆"}
        }
    },
    "spain_essay_2": {
        "title": "LA DUPLA MARAVILLA Y LA REVOLUCIÓN",
        "badge": "EXTREMOS ⚡",
        "music": "Volatile Reaction.mp3",
        "bg_name": "spain_stars.jpg",
        "chapters": {
            1: {"subtitle": "El Fenómeno Irrepetible de Lamine Yamal", "bullets": ["✔ Apenas diecisiete años y ya es leyenda", "✔ Regate endiablado en espacios reducidos", "✔ Comparaciones inevitables con Messi"], "badge": "LAMINE 🌟"},
            2: {"subtitle": "La Explosividad y Potencia de Nico Williams", "bullets": ["✔ Velocidad endiablada y fuerza física", "✔ Desborde constante en el uno contra uno", "✔ Sello del fútbol alegre y directo"], "badge": "NICO ⚔"},
            3: {"subtitle": "La Conexión y Amistad de Dos Hermanos", "bullets": ["✔ Bailes virales y risas en entrenamientos", "✔ Química que contagia al vestuario", "✔ Entendimiento táctico de memoria"], "badge": "AMISTAD 🤜🤛"},
            4: {"subtitle": "Diversidad e Identidad de la España Moderna", "bullets": ["✔ Hijos de inmigrantes alcanzando la gloria", "✔ Esfuerzo, integración y multiculturalidad", "✔ Inspiración para miles en los barrios"], "badge": "IDENTIDAD 🇪🇸"},
            5: {"subtitle": "El Impacto en el Mercado Internacional", "bullets": ["✔ Cláusulas millonarias listas para pagarse", "✔ Interés de los clubes más grandes de Europa", "✔ Cotización comercial en niveles récords"], "badge": "MERCADO 💸"},
            6: {"subtitle": "El Desafío de la Gran Final del Mundial", "bullets": ["✔ Marcajes dobles y defensas agresivas", "✔ La lucidez para romper el cerrojo rival", "✔ Rompiendo el partido en el momento cumbre"], "badge": "LA FINAL 🏆"}
        }
    },
    "spain_essay_3": {
        "title": "ESCÁNDALOS EN LA FEDERACIÓN",
        "badge": "CORRUPCIÓN ⚖",
        "music": "Volatile Reaction.mp3",
        "bg_name": "spain_team.jpg",
        "chapters": {
            1: {"subtitle": "La Crisis de la Real Federación Española", "bullets": ["✔ Polvorín administrativo tras bambalinas", "✔ Acusaciones de corrupción e intereses", "✔ La peor crisis de reputación histórica"], "badge": "CRISIS RFEF 🏛"},
            2: {"subtitle": "El Caso de Luis Rubiales", "bullets": ["✔ El beso polémico en la final femenina", "✔ Ola mundial de indignación social y política", "✔ Destitución y auditoría profunda de cuentas"], "badge": "RUBIALES ⚖"},
            3: {"subtitle": "La Intervención del Gobierno Español", "bullets": ["✔ Creada una comisión especial de supervisión", "✔ Asegurar la candidatura del Mundial 2030", "✔ Tensión política que encendió las alarmas"], "badge": "GOBIERNO 🇪🇸"},
            4: {"subtitle": "La Amenaza de Sanciones de la FIFA", "bullets": ["✔ Prohibición estricta de injerencia política", "✔ Riesgo de exclusión de clubes y selección", "✔ Pánico entre la afición por una descalificación"], "badge": "SANCIONES 🚫"},
            5: {"subtitle": "El Blindaje Absoluto del Vestuario", "bullets": ["✔ Aislamiento de debates y rumores mediáticos", "✔ Concentración exclusiva en la táctica de juego", "✔ La fortaleza mental y la unión del grupo"], "badge": "EL BÚNKER 🛡"},
            6: {"subtitle": "El Triunfo de la Pelota y el Deporte", "bullets": ["✔ Goles y victorias callan la tormenta", "✔ Protagonismo devuelto a los futbolistas", "✔ Refundación ética necesaria en el futuro"], "badge": "LA PELOTA ⚽"}
        }
    },
    "spain_essay_4": {
        "title": "ESPAÑA EN VÍSPERAS DE LA FINAL",
        "badge": "ANÁLISIS TÁCTICO 📋",
        "music": "Volatile Reaction.mp3",
        "bg_name": "spain_trophy.jpg",
        "chapters": {
            1: {"subtitle": "La Pizarra de Luis de la Fuente", "bullets": ["✔ El esquema base de cuatro tres tres", "✔ Solidez defensiva y presión tras pérdida", "✔ Transiciones letales a máxima velocidad"], "badge": "LA PIZARRA 📋"},
            2: {"subtitle": "La Batalla por el Medio Campo", "bullets": ["✔ Rodri Hernández: El metrónomo y ancla", "✔ Distribución inteligente y coberturas", "✔ Monopolio del ritmo frente al rival"], "badge": "VOLANTES ⚙"},
            3: {"subtitle": "El Desequilibrio de las Bandas", "bullets": ["✔ Aclarados para Nico Williams y Lamine", "✔ Diagonales letales hacia el área central", "✔ Llegadas de segunda línea para finalizar"], "badge": "BANDAS ⚡"},
            4: {"subtitle": "La Solidez Defensiva y Unai Simón", "bullets": ["✔ Concentración ante contragolpes rivales", "✔ Seguridad en el juego aéreo y salidas", "✔ Intervenciones del arquero en momentos límite"], "badge": "PORTEO 🧤"},
            5: {"subtitle": "El Banquillo como Factor Diferencial", "bullets": ["✔ Recambios de garantías en la segunda mitad", "✔ Velocidad y desborde de los revulsivos", "✔ Ajustes tácticos clave para la prórroga"], "badge": "BANCO 🔋"},
            6: {"subtitle": "La Búsqueda de la Segunda Estrella", "bullets": ["✔ El sueño de repetir Sudáfrica dos mil diez", "✔ Hambre de gloria e irreverencia juvenil", "✔ La coronación de una época inolvidable"], "badge": "LA ESTRELLA ⭐️"}
        }
    },
    "spain_essay_5": {
        "title": "LA SEGUNDA ESTRELLA DORADA",
        "badge": "CONSAGRACIÓN 🇪🇸",
        "music": "Volatile Reaction.mp3",
        "bg_name": "spain_team.jpg",
        "chapters": {
            1: {"subtitle": "El Recuerdo Histórico de Sudáfrica 2010", "bullets": ["✔ Catorce años después del gol de Iniesta", "✔ El faro espiritual de este nuevo plantel", "✔ La historia como motivación, no como presión"], "badge": "EL LEGADO ⭐️"},
            2: {"subtitle": "El Orgullo y Responsabilidad de la Roja", "bullets": ["✔ El honor supremo de representar al país", "✔ Millones de latidos en una misma sintonía", "✔ Jugar por la felicidad y unión de España"], "badge": "LA CAMISETA 🛡"},
            3: {"subtitle": "Inteligencia Emocional y Táctica en la Cita", "bullets": ["✔ Evitar fallos defensivos bajo máxima tensión", "✔ Control de los nervios e ímpetu rival", "✔ Saber sufrir para coronarse campeones"], "badge": "MADUREZ 🧠"},
            4: {"subtitle": "Unai Simón: El Seguro de Vida en Penales", "bullets": ["✔ Confianza plena en el guardameta español", "✔ Historial legendario en tandas decisivas", "✔ La batalla psicológica contra el lanzador"], "badge": "PORTERÍA 🧤"},
            5: {"subtitle": "El Festejo Soñado en las Fuentes", "bullets": ["✔ Levantar la Copa del Mundo en el podio", "✔ El reencuentro multitudinario con los hinchas", "✔ La recompensa al esfuerzo y a la hermandad"], "badge": "LA GLORIA 🏆"},
            6: {"subtitle": "El Futuro Brillante de la Generación", "bullets": ["✔ Las bases firmes de un equipo indestructible", "✔ El nacimiento de una nueva época dorada", "✔ Inspiración total para los niños de España"], "badge": "EL FUTURO 🚀"}
        }
    }
}

# 20 Shorts Configuration (4 shorts per essay)
shorts_config_c5 = [
    # Essay 1 Shorts
    ("spain_essay_1_short_1", "Lamine Yamal: ¿Heredero de Messi? 🌟", "spain_stars.jpg"),
    ("spain_essay_1_short_2", "El Estilo Vertical: Adiós al Tiki-Taka ⚡", "spain_team.jpg"),
    ("spain_essay_1_short_3", "La Pizarra de De la Fuente 📋", "spain_team.jpg"),
    ("spain_essay_1_short_4", "El Regreso de un Gigante 👑", "spain_team.jpg"),
    # Essay 2 Shorts
    ("spain_essay_2_short_1", "La Hermandad Nico-Lamine 🤜🤛", "spain_stars.jpg"),
    ("spain_essay_2_short_2", "Nico Williams: Velocidad Extrema ⚡", "spain_stars.jpg"),
    ("spain_essay_2_short_3", "Lamine Yamal: Joven Récord 🌟", "spain_stars.jpg"),
    ("spain_essay_2_short_4", "Diversidad e Identidad en la Roja 🇪🇸", "spain_stars.jpg"),
    # Essay 3 Shorts
    ("spain_essay_3_short_1", "El Escándalo de la Federación ⚖", "spain_team.jpg"),
    ("spain_essay_3_short_2", "La Intervención del Gobierno Español ⚖", "spain_team.jpg"),
    ("spain_essay_3_short_3", "¿Sanciones FIFA para España? 🚫", "spain_team.jpg"),
    ("spain_essay_3_short_4", "El Búnker: Blindaje de Vestuario 🛡", "spain_team.jpg"),
    # Essay 4 Shorts
    ("spain_essay_4_short_1", "Rodri Hernández: El Cerebro de Oro 🧠", "spain_trophy.jpg"),
    ("spain_essay_4_short_2", "La Batalla en el Medio Campo ⚙", "spain_trophy.jpg"),
    ("spain_essay_4_short_3", "Unai Simón: Guardián de la Final 🧤", "spain_trophy.jpg"),
    ("spain_essay_4_short_4", "El Banquillo de España: Revulsivos 🔋", "spain_trophy.jpg"),
    # Essay 5 Shorts
    ("spain_essay_5_short_1", "¿Segunda Estrella para España? ⭐️", "spain_trophy.jpg"),
    ("spain_essay_5_short_2", "El Legado de Sudáfrica 2010 🏆", "spain_team.jpg"),
    ("spain_essay_5_short_3", "El Peso de una Final Mundialista 🛡", "spain_team.jpg"),
    ("spain_essay_5_short_4", "La Nueva Edad de Oro del Fútbol 🚀", "spain_team.jpg")
]

SHORTS_DATA = {}
for key, title, bg_name in shorts_config_c5:
    SHORTS_DATA[key] = {
        "title": title,
        "badge": "ESPAÑA MUNDIALISTA ⚽",
        "music": "Volatile Reaction.mp3",
        "bg_name": bg_name
    }

from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_progress_bar

def extract_short_text(file_path, key):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split(f"### {key}")
    if len(parts) < 2:
        return ""
    block = parts[1].strip()
    subparts = block.split("---")
    text = subparts[0].strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    return text

def get_chapter_timestamps(script_path, total_duration, key):
    if not os.path.exists(script_path):
        return []
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split(f"## 📌 {key}")
    if len(parts) < 2:
        return []
    block = parts[1].strip()
    subparts = block.split("\n## 📌 ")
    target_block = subparts[0].strip()
    
    chapters = target_block.split("### 📌 Capítulo ")
    sections = []
    total_words = 0
    for ch in chapters[1:]:
        lines = ch.split('\n')
        title_line = lines[0].strip()
        title = title_line.split(":")[-1].strip() if ":" in title_line else title_line
        
        voc_text = ""
        for i, line in enumerate(lines):
            if "Audio (Voz en off)" in line:
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line.startswith('"') and next_line.endswith('"'):
                        voc_text = next_line[1:-1].strip()
                        break
        words_count = len(voc_text.split())
        total_words += words_count
        sections.append({"title": title, "words": words_count})
        
    boundaries = []
    current_time = 0.0
    for idx, sec in enumerate(sections):
        pct = sec["words"] / total_words if total_words > 0 else (1.0 / len(sections))
        duration = pct * total_duration
        boundaries.append((current_time, current_time + duration, sec["title"]))
        current_time += duration
    return boundaries

def draw_horizontal_frame(draw, width, height, title, subtitle, bullets, badge, font_title, font_sub, font_badge, blurred_bg_img, progress, effect_type="zoom_in"):
    if blurred_bg_img:
        img_bg = get_ken_burns_crop(blurred_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (35, 10, 10, 255))
    draw_img = ImageDraw.Draw(img_bg)
    
    # 1. Vignette (Deep dark red/black borders)
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for r in range(0, int(width * 0.85), 15):
        alpha = int((r / (width * 0.85)) ** 2.2 * 190)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(30, 5, 5, alpha), width=16)
    img_bg = Image.alpha_composite(img_bg, vignette)
    draw_img = ImageDraw.Draw(img_bg)
    
    # 2. Card Float
    float_offset = int(math.sin(progress * math.pi * 2.0) * 8.0)
    
    # Card Coordinates
    panel_w = 1200
    panel_h = 600
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + 10 + float_offset
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    # Spain Theme Colors: Neon Gold/Yellow and Vibrant Red
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(24, 8, 8, 175), outline=(253, 200, 47, 50), width=2)
    draw_img.rounded_rectangle([panel_left - 3, panel_top - 3, panel_right + 3, panel_bottom + 3], radius=27, fill=(0, 0, 0, 0), outline=(232, 27, 35, 20), width=2)
    
    # Title and Subtitle in Gold/White
    draw_img.text((width // 2, panel_top + 80), title.upper(), font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, panel_top + 210), subtitle, font=font_sub, fill=(253, 200, 47, 255), anchor="mm")
    
    # Active bullet highlight
    num_bullets = len(bullets)
    active_b_idx = int(progress * num_bullets)
    active_b_idx = min(active_b_idx, num_bullets - 1)
    
    bullet_y = panel_top + 295
    for idx_b, b in enumerate(bullets):
        if idx_b == active_b_idx:
            glow_alpha = int(140 + math.sin(time.time() * 8) * 40)
            draw_img.text((width // 2, bullet_y), b, font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
            t_w = draw_img.textlength(b, font=font_sub)
            draw_img.line([width//2 - t_w//2, bullet_y + 26, width//2 + t_w//2, bullet_y + 26], fill=(232, 27, 35, glow_alpha), width=2)
        else:
            draw_img.text((width // 2, bullet_y), b, font=font_sub, fill=(190, 160, 160, 220), anchor="mm")
        bullet_y += 70
        
    # Badge
    if badge:
        badge_w = 280
        badge_h = 60
        badge_x = panel_right - badge_w - 40
        badge_y = panel_top + 40
        draw_img.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(232, 27, 35, 40), outline=(253, 200, 47, 200), width=2)
        draw_img.text((badge_x + badge_w // 2, badge_y + badge_h // 2), badge, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
    # Progress Bar at the bottom of the card
    bar_w = panel_w
    bar_x = panel_left
    bar_y = panel_bottom + 15
    draw_progress_bar(draw_img, bar_x, bar_y, bar_w, 8, progress)
    
    return img_bg

def draw_vertical_short_frame(draw, width, height, title, badge, active_words, font_title, font_sub, font_badge, font_act, font_side, sharp_bg_img, progress, effect_type="zoom_in"):
    if sharp_bg_img:
        img_bg = get_ken_burns_crop(sharp_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (35, 10, 10, 255))
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Vignette
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for r in range(0, int(height * 0.75), 20):
        alpha = int((r / (height * 0.75)) ** 1.8 * 210)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(30, 5, 5, alpha), width=22)
    img_bg = Image.alpha_composite(img_bg, vignette)
    draw_img = ImageDraw.Draw(img_bg)
    
    # Float animation
    float_offset = int(math.sin(progress * math.pi * 2.0) * 6.0)
    
    # Top Card
    card_w = 900
    card_h = 240
    card_left = (width - card_w) // 2
    card_top = 120 + float_offset
    card_right = card_left + card_w
    card_bottom = card_top + card_h
    
    # Double Neon Border Card (Gold and Red)
    draw_img.rounded_rectangle([card_left, card_top, card_right, card_bottom], radius=24, fill=(24, 8, 8, 175), outline=(253, 200, 47, 60), width=2)
    draw_img.rounded_rectangle([card_left - 3, card_top - 3, card_right + 3, card_bottom + 3], radius=27, fill=(0, 0, 0, 0), outline=(232, 27, 35, 20), width=2)
    
    # Card Text
    draw_img.text((width // 2, card_top + 60), badge, font=font_badge, fill=(253, 200, 47, 255), anchor="mm")
    draw_img.text((width // 2, card_top + 140), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    # Caption Box
    prev_w, active_w, next_w = active_words
    cap_y = height // 2 + 100
    
    active_clean = re.sub(r'[^\wáéíóúÁÉÍÓÚñÑ]', '', active_w).upper()
    prev_clean = prev_w.lower()
    next_clean = next_w.lower()
    
    if len(prev_clean) > 10: prev_clean = prev_clean[:9] + "..."
    if len(next_clean) > 10: next_clean = next_clean[:9] + "..."
    
    # Active Word pill background
    act_w = draw_img.textlength(active_clean, font=font_act)
    pill_padding_x = 40
    pill_padding_y = 25
    pill_left = width // 2 - act_w // 2 - pill_padding_x
    pill_top = cap_y - pill_padding_y
    pill_right = width // 2 + act_w // 2 + pill_padding_x
    pill_bottom = cap_y + font_act.size + pill_padding_y
    
    # Gold capsule outline
    draw_img.rounded_rectangle([pill_left, pill_top, pill_right, pill_bottom], radius=16, fill=(24, 8, 8, 195), outline=(253, 200, 47, 130), width=3)
    
    draw_img.text((width // 2, cap_y), active_clean, font=font_act, fill=(255, 255, 255, 255), anchor="mt")
    
    if prev_clean:
        draw_img.text((width // 2 - act_w // 2 - 120, cap_y + 15), prev_clean, font=font_side, fill=(200, 160, 160, 140), anchor="rm")
    if next_clean:
        draw_img.text((width // 2 + act_w // 2 + 120, cap_y + 15), next_clean, font=font_side, fill=(200, 160, 160, 140), anchor="lm")
        
    # Progress Bar at the bottom
    bar_padding = 80
    bar_w = width - bar_padding * 2
    bar_y = height - 140
    draw_img.line([bar_padding, bar_y, width - bar_padding, bar_y], fill=(255, 255, 255, 20), width=6)
    draw_img.line([bar_padding, bar_y, bar_padding + int(bar_w * progress), bar_y], fill=(253, 200, 47, 220), width=6)
    
    return img_bg

def compile_videos():
    script_path = os.path.join(BASE_DIR, "scripts_spain_final.md")
    
    print("\n====================================================")
    print("CAMPAIGN 5 VIDEOS COMPILER (SPAIN WORLD CUP)")
    print("====================================================\n")
    
    width_h, height_h = 1920, 1080
    width_v, height_v = 1080, 1920
    
    font_title_h = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub_h = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 34)
    font_badge_h = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    
    font_title_v = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 46)
    font_sub_v = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 32)
    font_badge_v = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 30)
    
    font_caption_active = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 64)
    font_caption_side = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 36)
    
    # Load custom backgrounds
    bgs = {}
    for name in ["spain_team.jpg", "spain_stars.jpg", "spain_trophy.jpg"]:
        bg_path = os.path.join(SCREENSHOTS_DIR, name)
        if os.path.exists(bg_path):
            try:
                bgs[name] = Image.open(bg_path)
                print(f"Loaded Spain visual asset background: {name}")
            except Exception as e:
                print(f"Error loading background {name}: {e}")
                
    # --------------------------------------
    # 1. COMPILE WIDESCREEN VIDEO ESSAYS
    # --------------------------------------
    for key, info in ESSAYS_DATA.items():
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Video essay '{key}' already exists on disk. Skipping.")
            continue
            
        print(f"\nCompiling Widescreen Video Essay: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio track missing for {key}. Skipping.")
            continue
            
        boundaries = get_chapter_timestamps(script_path, audio_dur, key)
        if not boundaries:
            print(f"  [ERROR] Failed to parse boundaries for {key}. Skipping.")
            continue
            
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        segment_files = []
        
        base_img = bgs.get(info["bg_name"])
        blurred_bg_img = None
        if base_img:
            blurred_bg_img = base_img.convert("RGBA").filter(ImageFilter.GaussianBlur(12))
            overlay = Image.new("RGBA", base_img.size, (20, 5, 5, 160)) # Deep dark red overlay
            blurred_bg_img = Image.alpha_composite(blurred_bg_img, overlay)
            
        for idx_ch, (start, end, ch_title) in enumerate(boundaries):
            ch_num = idx_ch + 1
            dur = end - start
            seg_video = os.path.join(temp_dir, f"seg_{idx_ch:02d}.mp4")
            
            if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
                print(f"  [CACHE] Chapter {ch_num}: '{ch_title}' exists. Skipping.")
                segment_files.append(seg_video)
                continue
                
            print(f"  [RENDER] Chapter {ch_num} ({dur:.2f}s): '{ch_title}'")
            
            ch_info = info["chapters"].get(ch_num, {})
            frame_dir = os.path.join(temp_dir, f"frames_{idx_ch}")
            os.makedirs(frame_dir, exist_ok=True)
            total_frames = int(dur * 30)
            
            kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
            effect_type = kb_effects[idx_ch % len(kb_effects)]
            
            t0 = time.time()
            for f_idx in range(total_frames):
                progress = f_idx / total_frames
                frame_img = draw_horizontal_frame(
                    None, width_h, height_h, ch_title,
                    f"Capítulo {ch_num}: {ch_info.get('subtitle','')}",
                    ch_info.get("bullets", []), ch_info.get("badge",""),
                    font_title_h, font_sub_h, font_badge_h,
                    blurred_bg_img, progress, effect_type=effect_type
                )
                frame_img.convert("RGB").save(os.path.join(frame_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
                
            fps_render = total_frames / (time.time() - t0)
            print(f"    Rendered {total_frames} frames in {time.time()-t0:.1f}s ({fps_render:.1f} FPS)")
            
            cmd_frames = [
                "ffmpeg", "-y",
                "-framerate", "30",
                "-i", os.path.join(frame_dir, "frame_%05d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-t", f"{dur:.2f}",
                seg_video
            ]
            subprocess.run(cmd_frames, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                shutil.rmtree(frame_dir)
            except:
                pass
                
            if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
                segment_files.append(seg_video)
                
        print("\nConcatenating all chapter segments...")
        raw_video = os.path.join(temp_dir, "raw_video.mp4")
        concat_inputs = []
        filter_concat_parts = []
        for i_seg, sf in enumerate(segment_files):
            concat_inputs.extend(["-i", sf])
            filter_concat_parts.append(f"[{i_seg}:v]")
        filter_concat_str = "".join(filter_concat_parts) + f"concat=n={len(segment_files)}:v=1:a=0[v]"
        
        cmd_concat = ["ffmpeg", "-y"]
        cmd_concat.extend(concat_inputs)
        cmd_concat.extend([
            "-filter_complex", filter_concat_str,
            "-map", "[v]",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            raw_video
        ])
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print("Assembling audio tracks with Volatile Reaction.mp3 background...")
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.0[speech];"
        
        bg_music_path = os.path.join(MUSIC_DIR, info["music"])
        use_bg = os.path.exists(bg_music_path)
        if use_bg:
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            audio_mix_filter += "[2:a]volume=-24dB[bg_music];"
            
        sfx_available = os.path.exists(WHOOSH_SFX)
        if sfx_available:
            w_idx = 3 if use_bg else 2
            audio_inputs.extend(["-i", WHOOSH_SFX])
            
            sfx_filter = f"[{w_idx}:a]asplit={len(boundaries)-1}"
            for i in range(len(boundaries)-1):
                sfx_filter += f"[w{i}]"
            sfx_filter += ";"
            
            sfx_mixes = []
            for i in range(len(boundaries)-1):
                boundary_time = boundaries[i][1]
                delay_ms = int(boundary_time * 1000)
                sfx_filter += f"[w{i}]adelay={delay_ms}|{delay_ms}[wd{i}];"
                sfx_mixes.append(f"[wd{i}]")
                
            sfx_filter += f"{''.join(sfx_mixes)}amix=inputs={len(boundaries)-1}:normalize=0[sfx_raw];[sfx_raw]volume=-6dB[sfx_final];"
            audio_mix_filter += sfx_filter
            
            if use_bg:
                audio_mix_filter += "[speech][bg_music][sfx_final]amix=inputs=3:normalize=0[a]"
            else:
                audio_mix_filter += "[speech][sfx_final]amix=inputs=2:normalize=0[a]"
        else:
            if use_bg:
                audio_mix_filter += "[speech][bg_music]amix=inputs=2:normalize=0[a]"
            else:
                audio_mix_filter += "[speech]anull[a]"
                
        cmd_final = ["ffmpeg", "-y"]
        cmd_final.extend(audio_inputs)
        cmd_final.extend([
            "-filter_complex", audio_mix_filter,
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ])
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
            
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Widescreen essay compiled: {output_path}")
        else:
            print(f"  [FAILED] Compile failed for {key}")

    # --------------------------------------
    # 2. COMPILE VERTICAL SHORTS
    # --------------------------------------
    print("\nStarting compilation of the 20 Spain Shorts...")
    for idx, (key, info) in enumerate(SHORTS_DATA.items()):
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Short '{key}' already exists on disk. Skipping.")
            continue
            
        print(f"Compiling Spain Short: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio missing for {key}. Skipping.")
            continue
            
        script_text = extract_short_text(script_path, key)
        words = script_text.split()
        total_words = len(words)
        
        base_img = bgs.get(info["bg_name"])
        sharp_bg_img = None
        if base_img:
            bg_scale = 1.4
            bg_w = int(width_v * bg_scale)
            bg_h = int(height_v * bg_scale)
            sharp_bg_img = base_img.resize((bg_w, bg_h)).convert("RGBA")
            
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        total_frames = int(audio_dur * 30)
        
        kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
        effect_type = kb_effects[idx % len(kb_effects)]
        
        t0 = time.time()
        for f_idx in range(total_frames):
            progress = f_idx / total_frames
            curr_time = f_idx / 30.0
            word_idx = int(curr_time * (total_words / audio_dur))
            word_idx = min(word_idx, total_words - 1)
            
            prev_w = words[word_idx - 1] if word_idx > 0 else ""
            active_w = words[word_idx]
            next_w = words[word_idx + 1] if word_idx < total_words - 1 else ""
            
            frame_img = draw_vertical_short_frame(
                None, width_v, height_v,
                info["title"], info["badge"],
                (prev_w, active_w, next_w),
                font_title_v, font_sub_v, font_badge_v,
                font_caption_active, font_caption_side,
                sharp_bg_img, progress, effect_type=effect_type
            )
            frame_img.convert("RGB").save(os.path.join(temp_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
            
        raw_video = os.path.join(temp_dir, "raw_video.mp4")
        cmd_frames = [
            "ffmpeg", "-y",
            "-framerate", "30",
            "-i", os.path.join(temp_dir, "frame_%05d.jpg"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-t", f"{audio_dur:.2f}",
            raw_video
        ]
        subprocess.run(cmd_frames, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Clause pop pause SFX
        pause_times = [0.0]
        for w_idx in range(1, len(words)):
            w = words[w_idx - 1]
            if w.endswith('.') or w.endswith(',') or w.endswith('?') or w.endswith('!'):
                p_time = w_idx * (audio_dur / total_words)
                pause_times.append(p_time)
        pop_times = [t for t in pause_times if t > 0.1][:12]
        
        bg_music_path = os.path.join(MUSIC_DIR, info["music"])
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.2[speech];"
        
        use_bg = os.path.exists(bg_music_path)
        if use_bg:
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            audio_mix_filter += "[2:a]volume=-24dB[bg_music];"
            
        use_sfx = os.path.exists(WHOOSH_SFX) and os.path.exists(POP_SFX)
        if use_sfx:
            w_idx = 3 if use_bg else 2
            p_idx = 4 if use_bg else 3
            audio_inputs.extend(["-i", WHOOSH_SFX, "-i", POP_SFX])
            audio_mix_filter += f"[{w_idx}:a]volume=-8dB,adelay=0|0[whoosh_delayed];"
            
            num_pops = len(pop_times)
            if num_pops > 0:
                audio_mix_filter += f"[{p_idx}:a]asplit={num_pops}" + "".join(f"[p{i}]" for i in range(num_pops)) + ";"
                for i, t in enumerate(pop_times):
                    delay_ms = int(t * 1000)
                    audio_mix_filter += f"[p{i}]volume=-10dB,adelay={delay_ms}|{delay_ms}[pd{i}];"
                    
            mix_inputs = ["[speech]"]
            if use_bg:
                mix_inputs.append("[bg_music]")
            mix_inputs.append("[whoosh_delayed]")
            for i in range(num_pops):
                mix_inputs.append(f"[pd{i}]")
            audio_mix_filter += "".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:normalize=0[a]"
        else:
            if use_bg:
                audio_mix_filter += "[speech][bg_music]amix=inputs=2:normalize=0[a]"
            else:
                audio_mix_filter += "[speech]anull[a]"
                
        cmd_final = ["ffmpeg", "-y"]
        cmd_final.extend(audio_inputs)
        cmd_final.extend([
            "-filter_complex", audio_mix_filter,
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ])
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
            
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Short generated: {output_path}")
        else:
            print(f"  [FAILED] Compile failed for {key}")

if __name__ == "__main__":
    compile_videos()
