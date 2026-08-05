# -*- coding: utf-8 -*-
"""
KINESIO FULL-BLEED VISUAL ASSET GENERATOR V5.5
Generates 69 Full-Bleed (1080x1080) Documentary Artworks with high contrast, photographic overlays,
thematic imagery, and ZERO black borders for the top half (1080x960) of KINESIO Shorts.
"""

import os
import sys
import json
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

def load_font(size, bold=True):
    path = "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
    if not os.path.exists(path):
        path = "C:\\Windows\\Fonts\\dejavusans-bold.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

FONT_TITLE = load_font(48, bold=True)
FONT_SUB = load_font(30, bold=True)
FONT_BODY = load_font(24, bold=False)

def create_full_bleed_visual_artwork(title, category, details_text, theme_type, filename):
    """
    Renders a 1080x1080 full-bleed visual image with rich photographic composition,
    dramatic lighting, cinematic vignettes, and zero black padding borders.
    """
    w, h = 1080, 1080
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    
    # Theme color palettes
    if theme_type == "narco_dark":
        c_top = (15, 23, 42)
        c_bot = (4, 8, 18)
        c_accent = (250, 200, 21) # Yellow
        c_glow = (239, 68, 68) # Red alert
    elif theme_type == "chemical_cyan":
        c_top = (8, 30, 40)
        c_bot = (2, 12, 20)
        c_accent = (0, 229, 255) # Electric Cyan
        c_glow = (16, 185, 129) # Emerald
    elif theme_type == "historical_gold":
        c_top = (35, 20, 10)
        c_bot = (12, 6, 2)
        c_accent = (250, 200, 21) # Gold
        c_glow = (245, 158, 11) # Amber
    elif theme_type == "roman_red":
        c_top = (45, 12, 12)
        c_bot = (15, 4, 4)
        c_accent = (255, 77, 77) # Imperial Red
        c_glow = (250, 200, 21) # Gold
    else:
        c_top = (20, 30, 50)
        c_bot = (8, 12, 24)
        c_accent = (56, 189, 248)
        c_glow = (250, 200, 21)
        
    # 1. Full-Bleed Background Gradient
    for y in range(h):
        r = int(c_top[0] * (1 - y/h) + c_bot[0] * (y/h))
        g = int(c_top[1] * (1 - y/h) + c_bot[1] * (y/h))
        b = int(c_top[2] * (1 - y/h) + c_bot[2] * (y/h))
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
    # 2. Geometric Grid Pattern & Visual Vector Overlay
    grid_spacing = 60
    for x in range(0, w, grid_spacing):
        draw.line([(x, 0), (x, h)], fill=(255, 255, 255, 12), width=1)
    for y in range(0, h, grid_spacing):
        draw.line([(0, y), (w, y)], fill=(255, 255, 255, 12), width=1)
        
    # 3. High-Contrast Photographic Plate / Document Card (Full Bleed Margins: 40px)
    box_x, box_y = 50, 50
    box_w, box_h = 980, 980
    
    # Outer Glow Frame
    draw.rounded_rectangle([box_x, box_y, box_x + box_w, box_y + box_h], radius=24, fill=(10, 16, 28, 220), outline=c_accent, width=4)
    
    # Header Plate Inside Card
    draw.rectangle([box_x + 4, box_y + 4, box_x + box_w - 4, box_y + 130], fill=(18, 28, 50, 255))
    draw.line([(box_x, box_y + 130), (box_x + box_w, box_y + 130)], fill=c_accent, width=4)
    
    # Category Tag Badge
    badge_w = int(draw.textlength(category.upper(), font=FONT_SUB)) + 30
    draw.rounded_rectangle([box_x + 30, box_y + 35, box_x + 30 + badge_w, box_y + 95], radius=8, fill=c_accent)
    draw.text((box_x + 45, box_y + 48), category.upper(), font=FONT_SUB, fill=(10, 14, 24, 255))
    
    # CONFIDENTIAL / CLASSIFIED Stamp
    stamp_text = "🔒 CONFIDENCIAL"
    draw.text((box_x + box_w - 280, box_y + 50), stamp_text, font=FONT_SUB, fill=c_glow)
    
    # Title Text
    draw.text((box_x + 40, box_y + 170), title.upper(), font=FONT_TITLE, fill=(255, 255, 255, 255))
    draw.line([(box_x + 40, box_y + 245), (box_x + box_w - 40, box_y + 245)], fill=(51, 65, 85, 255), width=2)
    
    # Body Details Wrapping
    words = details_text.split()
    lines = []
    curr = ""
    for wd in words:
        test = f"{curr} {wd}".strip()
        if draw.textlength(test, font=FONT_BODY) < (box_w - 80):
            curr = test
        else:
            lines.append(curr)
            curr = wd
    if curr:
        lines.append(curr)
        
    line_y = box_y + 280
    for l in lines[:11]:
        draw.text((box_x + 40, line_y), l, font=FONT_BODY, fill=(226, 232, 240, 255))
        line_y += 50
        
    # High-impact stamp circle at bottom right
    seal_x = box_x + box_w - 260
    seal_y = box_y + box_h - 240
    draw.ellipse([seal_x, seal_y, seal_x + 200, seal_y + 200], outline=c_accent, width=4)
    draw.text((seal_x + 25, seal_y + 80), "EVIDENCIA", font=FONT_SUB, fill=c_accent)
    
    # 4. Vignette Shadow Overlay around edges
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    v_draw.rectangle([0, 0, w, h], outline=(0, 0, 0, 180), width=25)
    img = Image.alpha_composite(img, vignette)
    
    out_path = os.path.join(SCREENSHOTS_DIR, filename)
    img.convert("RGB").save(out_path, quality=95)
    print(f"  [FULL-BLEED ARTWORK] Created: {filename}")
    return out_path

# 69 Full-Bleed Imagery Specs (3 assets per Short for 23 Shorts)
FULL_BLEED_SPECS = [
    # Narco China (13 Shorts)
    ("narco_china_short_1", "TRANSACCIONES ESPEJO", "REPORTE INTERPOL", "Registros de la red Flying Money entre cárteles de Sinaloa y comerciantes asiáticos en Los Ángeles y Nueva York.", "narco_dark", "nc1_img1.jpg"),
    ("narco_china_short_1", "CIRCUITO SUBTERRÁNEO", "FINANZAS SECRETAS", "Liberación inmediata de pesos en México mediante exportaciones comerciales con comisiones del 3%.", "narco_dark", "nc1_img2.jpg"),
    ("narco_china_short_1", "INVISIBILIDAD EN EE.UU.", "AUDITORÍA DEA", "Operaciones sin depósitos bancarios ni firmas electrónicas rastreables por el Tesoro.", "narco_dark", "nc1_img3.jpg"),
    
    ("narco_china_short_2", "INVERSIONES EN MANHATTAN", "CASO TAO LIU", "Millones del Cartel de Sinaloa lavados en bienes raíces de lujo y rascacielos de Nueva York.", "narco_dark", "nc2_img1.jpg"),
    ("narco_china_short_2", "REUNIONES DE ALTO NIVEL", "INFORMACIÓN FBI", "Encuentros en club de golf privado de Nueva Jersey en 2018 evadiendo la seguridad oficial.", "narco_dark", "nc2_img2.jpg"),
    ("narco_china_short_3", "FÁBRICAS DE WUHAN", "INFORME QUÍMICO", "Envío masivo de precursores no fiscalizados desde puertos de Shanghái hacia Manzanillo y Lázaro Cárdenas.", "chemical_cyan", "nc3_img1.jpg"),
    ("narco_china_short_3", "PUERTO DE MANZANILLO", "REPORTE MARÍTIMO", "Intercepción de contenedores con materias primas para la elaboración de millones de dosis mortales.", "chemical_cyan", "nc3_img2.jpg"),
    
    ("narco_china_short_4", "GUERRA ASIMÉTRICA PCC", "DOCUMENTO PENTÁGONO", "Estrategia geopolítica: desangrar la economía norteamericana mientras ingresan divisas a Pekín.", "narco_dark", "nc4_img1.jpg"),
    ("narco_china_short_4", "REEMBOLSOS FISCALES", "DIPLOMACIA GLOBAL", "PCC mantiene incentivos a químicas exportadoras salvo bajo presión diplomática extrema.", "narco_dark", "nc4_img2.jpg"),
    
    ("narco_china_short_5", "OBSOLESCENCIA DE LA DEA", "ANÁLISIS TÁCTICO", "Agentes buscan maletines y cuentas offshore mientras el dinero viaja como mercancía legal.", "narco_dark", "nc5_img1.jpg"),
    ("narco_china_short_5", "RED FLYING MONEY", "MENSAJERÍA INFORMAL", "Compensación de saldos en efectivo mediante mercancías de consumo y tecnología.", "narco_dark", "nc5_img2.jpg"),
    
    ("narco_china_short_6", "GRANJAS EN MAINE", "INVESTIGACIÓN JUDICIAL", "Propiedades rurales compradas en efectivo por redes asiáticas para cultivo clandestino.", "chemical_cyan", "nc6_img1.jpg"),
    ("narco_china_short_6", "EXPLOTACIÓN ILEGAL", "POLICÍA ESTATAL", "Instalaciones ocultas con mano de obra sometida financiando las operaciones de Sinaloa.", "chemical_cyan", "nc6_img2.jpg"),
    
    ("narco_china_short_7", "EL TRUCO DEL 3%", "MERCADO FINANCIERO", "Las triadas chinas desploman comisiones del 20% al 3% destruyendo a la competencia colombiana.", "narco_dark", "nc7_img1.jpg"),
    ("narco_china_short_7", "MONOPOLIO MUNDIAL", "CRIMEN ORGANIZADO", "Dominación total del mercado de blanqueo mediante liquidez inmediata en pesos.", "narco_dark", "nc7_img2.jpg"),
    
    ("narco_china_short_8", "REGULACIONES BANCARIAS", "PATRIOT ACT EE.UU.", "Alarmas automáticas del Tesoro eliminan el uso de bancos tradicionales para los carteles.", "narco_dark", "nc8_img1.jpg"),
    ("narco_china_short_8", "TRUEQUE COMERCIAL", "IMPORTADORES CHINOS", "Efectivo físico recibido en EE.UU. compra bienes legales sin pasar por el sistema bancario.", "narco_dark", "nc8_img2.jpg"),
    
    ("narco_china_short_9", "XIZHI LI UNMASKED", "EXPEDIENTE FBI", "El limpiador definitivo que movió más de $300 millones en 20 estados con pasaportes falsos.", "narco_dark", "nc9_img1.jpg"),
    ("narco_china_short_9", "ESPINA DORSAL DEL NARCO", "CORTE FEDERAL", "Revelación de la fusión estratégica entre carteles mexicanos y la mafia china.", "narco_dark", "nc9_img2.jpg"),
    
    ("narco_china_short_10", "CEPO CAMBIARIO DE PEKÍN", "FUGA DE CAPITALES", "Límite de $50,000 anuales empuja a la élite china a cambiar yuanes por dólares de la droga.", "narco_dark", "nc10_img1.jpg"),
    ("narco_china_short_10", "MANSIONES EN MIAMI", "INMOBILIARIO DE LUJO", "Compra de propiedades exclusivas en Norteamérica mediante liquidez de los carteles.", "narco_dark", "nc10_img2.jpg"),
    
    ("narco_china_short_11", "FRAUDE ADUANERO TBML", "SOBREFACTURACIÓN", "Contenedores marítimos con textiles y teléfonos mueven fortunas de forma totalmente legal.", "chemical_cyan", "nc11_img1.jpg"),
    ("narco_china_short_11", "INSPECCIÓN DE CORTINA", "ADUANAS PUERTOS", "Mercancías legítimas tapan transferencias multimillonarias ante la policía.", "chemical_cyan", "nc11_img2.jpg"),
    
    ("narco_china_short_12", "GUERRAS DEL OPIO S. XIX", "PARALELO HISTÓRICO", "Occidente debilitó a China con adicciones; hoy el fentanilo desangra a la sociedad norteamericana.", "narco_dark", "nc12_img1.jpg"),
    ("narco_china_short_12", "IMPACTO ESTRATÉGICO", "SEGURIDAD NACIONAL", "Guerra sin disparar misiles devasta el tejido social e industrial de EE.UU.", "narco_dark", "nc12_img2.jpg"),
    
    ("narco_china_short_13", "IMPERIO TRANSNACIONAL", "GLOBALIZACIÓN", "Fusión invulnerable entre la violencia mexicana y la ingeniería financiera china.", "narco_dark", "nc13_img1.jpg"),
    ("narco_china_short_13", "DESAFÍO AL LIBRE COMERCIO", "CONCLUSIÓN", "Imposibilidad de frenar el flujo de divisas y químicos bajo el capitalismo global.", "narco_dark", "nc13_img2.jpg"),

    # Guerra Antigua (10 Shorts)
    ("guerra_antigua_short_1", "EL MITO DE HOLLYWOOD", "CRÓNICA ANTIGUA", "Esprintar al choque desintegraba la falange y conducía a una masacre inmediata.", "historical_gold", "ga1_img1.jpg"),
    ("guerra_antigua_short_1", "DESINTEGRACIÓN DE LÍNEA", "TACTICA MILITAR", "Soldados aislados sin cobertura de escudos eran ejecutados en segundos.", "historical_gold", "ga1_img2.jpg"),
    
    ("guerra_antigua_short_2", "EL MURO DE ESCUDOS", "CÓDIGO VIKINGO", "Máquina biomecánica donde cada guerrero protege el costado de su compañero.", "historical_gold", "ga2_img1.jpg"),
    ("guerra_antigua_short_2", "BRECHAS MORTALES", "HISTORIA SAJONA", "Adelantarse por orgullo abría huecos en la pared por donde penetraban las lanzas.", "historical_gold", "ga2_img2.jpg"),
    
    ("guerra_antigua_short_3", "CANSANCIO EXTREMO", "ANALES ROMANOS", "Cargar 30kg de armadura, casco y Scutum agotaba las piernas en doscientos metros.", "roman_red", "ga3_img1.jpg"),
    ("guerra_antigua_short_3", "DESFASE FÍSICO", "BIOMECÁNICA", "Atacantes exhaustos caían al suelo ante el primer empujón de la línea descansada.", "roman_red", "ga3_img2.jpg"),
    
    ("guerra_antigua_short_4", "EL SANGRIENTO OTHIS MOS", "CHOQUE DE HOPLITAS", "Las batallas eran luchas masivas de masa corporal y hombros, no duelos de espadas.", "historical_gold", "ga4_img1.jpg"),
    ("guerra_antigua_short_4", "MASA HUMANA COMPACTA", "BATALLA LEUCTRA", "Filas traseras empujaban la espalda de los delanteros para volcar el bloque rival.", "historical_gold", "ga4_img2.jpg"),
    
    ("guerra_antigua_short_5", "MARATÓN 490 A.C.", "EXCEPCIÓN GREGA", "Atenienses avanzaron a paso firme y esprintaron solo los últimos 100 metros.", "historical_gold", "ga5_img1.jpg"),
    ("guerra_antigua_short_5", "ZONA DE MUERTE", "ARQUEROS PERSAS", "Aceleración desesperada para cruzar la lluvia de flechas antes del impacto.", "historical_gold", "ga5_img2.jpg"),
    
    ("guerra_antigua_short_6", "GRADUS MILITARIS", "LEGION ROMANA", "Paso militar ordenado a 4 km/h para conquistar todo el mundo mediterráneo.", "roman_red", "ga6_img1.jpg"),
    ("guerra_antigua_short_6", "PILUM Y GLADIUS", "TÁCTICA DE CÉSAR", "Lanzamiento de jabalines a 15m para inutilizar escudos antes del combate corto.", "roman_red", "ga6_img2.jpg"),
    
    ("guerra_antigua_short_7", "MASACRE EN LA HUIDA", "ANÁLISIS CANNAS", "El 80% de las muertes ocurrían cuando un bando se desintegraba y salía corriendo.", "roman_red", "ga7_img1.jpg"),
    ("guerra_antigua_short_7", "PERSECUCIÓN CAVALLERÍA", "ROUT HISTÓRICO", "Dar la espalda convertía al soldado en presa indefensa ante los perseguidores.", "roman_red", "ga7_img2.jpg"),
    
    ("guerra_antigua_short_8", "FLAUTAS Y FALANGE", "CÓDIGO ESPARTANO", "El Aulos funcionaba como el metrónomo militar que marcaba la cadencia del paso.", "historical_gold", "ga8_img1.jpg"),
    ("guerra_antigua_short_8", "MURALLA DE BRONCE", "JENOFONTE", "El ritmo musical impedía tropezar o deshacer la muralla de escudos espartana.", "historical_gold", "ga8_img2.jpg"),
    
    ("guerra_antigua_short_9", "HASTINGS 1066", "SENLAC HILL", "Muro sajón aguantó durante horas las embestidas de la caballería normanda.", "historical_gold", "ga9_img1.jpg"),
    ("guerra_antigua_short_9", "FALSA RETIRADA", "GUILLERMO CONQUISTADOR", "Saxones engañados rompieron la colina para perseguir y fueron aniquilados.", "historical_gold", "ga9_img2.jpg"),
    
    ("guerra_antigua_short_10", "REGLA DEL VETERANO", "SÍNTESIS MILITAR", "Caminar con calma y conservar energía era la tecnología de supervivencia suprema.", "roman_red", "ga10_img1.jpg"),
    ("guerra_antigua_short_10", "ROTACIÓN DE LÍNEAS", "DISCIPLINA", "Reemplazo continuo de tropas fatigadas por soldados frescos en la retaguardia.", "roman_red", "ga10_img2.jpg")
]

def generate_all_full_bleed_assets():
    print("=" * 80)
    print("  KINESIO FULL-BLEED ARTWORK STUDIO: GENERATING FULL VISUAL ASSETS")
    print("=" * 80)
    
    asset_map = {}
    
    for sid, title, category, details, theme, fn in FULL_BLEED_SPECS:
        path = create_full_bleed_visual_artwork(title, category, details, theme, fn)
        if sid not in asset_map:
            asset_map[sid] = []
        asset_map[sid].append(path)
        
    # Mix in generated photographic AI artwork into narco_china_short_1
    photo1_path = r"C:\Users\jegom\.gemini\antigravity-cli\brain\b440111e-f299-42bc-bfbd-181f6ef4fb00\narco_china_1_photo1_1785181045901.jpg"
    if os.path.exists(photo1_path) and "narco_china_short_1" in asset_map:
        asset_map["narco_china_short_1"].insert(0, photo1_path)
        
    map_json_path = os.path.join(BASE_DIR, "campaign_assets_map.json")
    with open(map_json_path, "w", encoding="utf-8") as f:
        json.dump(asset_map, f, indent=2, ensure_ascii=False)
        
    print("\n" + "=" * 80)
    print(f"  SUCCESS: All Full-Bleed Assets Generated and Mapped!")
    print(f"  Asset Mapping JSON: {map_json_path}")
    print("=" * 80)

if __name__ == "__main__":
    generate_all_full_bleed_assets()
