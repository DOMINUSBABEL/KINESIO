# -*- coding: utf-8 -*-
"""
Prepares and maps rich visual image assets for all RTS and Saturation campaign scenes.
Guarantees 100% asset availability for Ken Burns rendering in KINESIO.
"""

import os
from PIL import Image, ImageDraw, ImageFont

PROJECT_DIR = r"C:\Users\jegom\shorts_project"

def create_themed_artwork(filename, main_title, subtitle, bg_color, accent_color):
    filepath = os.path.join(PROJECT_DIR, filename)
    img = Image.new("RGB", (1920, 1080), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw geometric background grid & accents
    for x in range(0, 1920, 80):
        draw.line([(x, 0), (x, 1080)], fill=(bg_color[0]+15, bg_color[1]+15, bg_color[2]+20), width=1)
    for y in range(0, 1080, 80):
        draw.line([(0, y), (1920, y)], fill=(bg_color[0]+15, bg_color[1]+15, bg_color[2]+20), width=1)
        
    # Draw glowing accent lines
    draw.line([(100, 150), (1820, 150)], fill=accent_color, width=4)
    draw.line([(100, 930), (1820, 930)], fill=accent_color, width=4)
    
    # Text
    try:
        font_main = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 72)
        font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 36)
    except:
        font_main = ImageFont.load_default()
        font_sub = ImageFont.load_default()
        
    draw.text((960, 480), main_title.upper(), font=font_main, fill=(255, 255, 255), anchor="mm")
    draw.text((960, 580), subtitle, font=font_sub, fill=accent_color, anchor="mm")
    
    img.save(filepath, quality=95)
    print(f"[ASSET CREATED] {filename}")

def prepare_all_assets():
    assets_to_create = [
        # RTS Campaign Assets
        ("starcraft_art.jpg", "STARCRAFT BROOD WAR", "La Paradoja de los 300 APM y la Era Esport en Seúl", (15, 23, 42), (250, 200, 21)),
        ("cnc_art.jpg", "COMMAND & CONQUER", "El Colapso de C&C 4 y la Eliminación de las Bases", (30, 10, 15), (239, 68, 68)),
        ("warcraft_dota_art.jpg", "WARCRAFT III & DOTA", "El Nacimiento del género MOBA y League of Legends", (10, 30, 25), (16, 185, 129)),
        ("macro_micro_art.jpg", "MACRO VS MICRO", "La Sobrecarga Cognitiva y el Dilema Estratégico", (25, 20, 40), (168, 85, 247)),
        ("manor_lords_art.jpg", "MANOR LORDS & REGRESO RTS", "El Renacimiento Neotérico y la Era Dorada Indie", (20, 30, 15), (34, 197, 94)),
        ("ensemble_art.jpg", "ENSEMBLE STUDIOS", "El Cierre de Age of Empires y Halo Wars (2009)", (35, 25, 15), (249, 115, 22)),
        
        # Saturation Campaign Assets
        ("steam_backlog_art.jpg", "PARÁLISIS DE SELECCIÓN", "14,000+ Juegos Anuales en Steam y la Biblioteca Infinita", (15, 25, 35), (59, 130, 246)),
        ("comfort_games_art.jpg", "COMFORT GAMES & GAAS", "El Refugio de LoL y la Trampa de los Pases de Batalla", (25, 15, 30), (236, 72, 153)),
        ("discovery_art.jpg", "LA MUERTE DEL DESCUBRIMIENTO", "Tier Lists, Min-Maxing y la Pérdida del Misterio", (35, 30, 15), (234, 179, 8)),
        ("rule20_art.jpg", "REGLA DE LOS 20 MINUTOS", "El Retorno a la Alegría Pura de Jugar sin Culpa", (15, 35, 30), (16, 185, 129))
    ]
    
    for fname, main_t, sub_t, bg_c, acc_c in assets_to_create:
        create_themed_artwork(fname, main_t, sub_t, bg_c, acc_c)

if __name__ == "__main__":
    prepare_all_assets()
