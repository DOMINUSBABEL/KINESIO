# -*- coding: utf-8 -*-
"""
KINESIO HIGH-IMPACT VISUAL ARTWORK GENERATOR
Creates 69 high-resolution (1920x1080) thematic visual artworks (3 per short for 23 Shorts).
Ensures 100% full visual coverage in top half (1080x960) with Ken Burns multi-asset rotation.
"""

import os
import sys
import json
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
ARTWORK_DIR = os.path.join(BASE_DIR, "visual_artworks")
os.makedirs(ARTWORK_DIR, exist_ok=True)

def load_font(size, bold=True):
    path = "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
    if not os.path.exists(path):
        path = "C:\\Windows\\Fonts\\dejavusans-bold.ttf"
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

FONT_HEADER = load_font(42, bold=True)
FONT_SUB = load_font(28, bold=True)
FONT_BODY = load_font(24, bold=False)

def create_thematic_visual_artwork(title, subtitle, tag_badge, date_str, theme_colors, output_filename):
    """
    Renders a 1920x1080 high-contrast cinematic documentary visual artwork.
    theme_colors: (top_rgb, bot_rgb, accent_rgb)
    """
    w, h = 1920, 1080
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    draw = ImageDraw.Draw(img)
    
    c_top, c_bot, c_accent = theme_colors
    
    # 1. Background Gradient & Atmospheric Noise Texture
    for y in range(h):
        ratio = y / h
        r = int(c_top[0] * (1 - ratio) + c_bot[0] * ratio)
        g = int(c_top[1] * (1 - ratio) + c_bot[1] * ratio)
        b = int(c_top[2] * (1 - ratio) + c_bot[2] * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))
        
    # 2. Geometric Architectural Vignette / Frame Elements
    draw.rectangle([0, 0, w, 15], fill=c_accent)
    draw.rectangle([0, h - 15, w, h], fill=c_accent)
    
    # 3. Main Central Visual Document Card (1400x700)
    card_w, card_h = 1480, 740
    card_x = (w - card_w) // 2
    card_y = (h - card_h) // 2
    
    # Card Shadow
    shadow = Image.new("RGBA", (card_w + 30, card_h + 30), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.rounded_rectangle([15, 15, card_w + 15, card_h + 15], radius=24, fill=(0, 0, 0, 200))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    img.paste(shadow, (card_x - 15, card_y - 15), mask=shadow)
    
    # Card Main Body (Rich aged parchment / obsidian plate)
    draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill=(15, 23, 42, 235), outline=c_accent, width=4)
    
    # Header Banner inside Card
    draw.rectangle([card_x + 4, card_y + 4, card_x + card_w - 4, card_y + 110], fill=(24, 36, 64, 255))
    draw.line([card_x, card_y + 110, card_x + card_w, card_y + 110], fill=c_accent, width=3)
    
    # Tag Badge (Top Left of Card)
    badge_str = f"  {tag_badge.upper()}  "
    draw.rounded_rectangle([card_x + 40, card_y + 35, card_x + 420, card_y + 85], radius=8, fill=c_accent)
    draw.text((card_x + 50, card_y + 45), badge_str, font=FONT_SUB, fill=(10, 15, 26, 255))
    
    # Date Stamp (Top Right of Card)
    date_text = f"📅 ARCHIVO HISTÓRICO: {date_str}"
    draw.text((card_x + card_w - 460, card_y + 50), date_text, font=FONT_SUB, fill=(226, 232, 240, 255))
    
    # Headline Title inside Card
    draw.text((card_x + 60, card_y + 160), title.upper(), font=FONT_HEADER, fill=(255, 255, 255, 255))
    draw.line([card_x + 60, card_y + 225, card_x + card_w - 60, card_y + 225], fill=(71, 85, 105, 255), width=2)
    
    # Subtitle Paragraph wrapping
    words = subtitle.split()
    lines = []
    curr = ""
    for wd in words:
        test = f"{curr} {wd}".strip()
        if draw.textlength(test, font=FONT_BODY) < (card_w - 120):
            curr = test
        else:
            lines.append(curr)
            curr = wd
    if curr:
        lines.append(curr)
        
    line_y = card_y + 260
    for l in lines[:7]:
        draw.text((card_x + 60, line_y), l, font=FONT_BODY, fill=(203, 213, 225, 255))
        line_y += 45
        
    # High-impact stamp seal in bottom right of card
    seal_x = card_x + card_w - 220
    seal_y = card_y + card_h - 180
    draw.ellipse([seal_x, seal_y, seal_x + 150, seal_y + 150], outline=c_accent, width=4)
    draw.text((seal_x + 25, seal_y + 60), "CONFIDENCIAL", font=FONT_SUB, fill=c_accent)
    
    out_path = os.path.join(ARTWORK_DIR, output_filename)
    img.convert("RGB").save(out_path, quality=95)
    print(f"  [ARTWORK STUDIO] Created: {output_filename}")
    return out_path

# Specifications for 23 Shorts (3 distinct visual assets per Short = 69 Artworks)
VISUAL_ARTWORK_SPECS = [
    # Narco China (13 Shorts)
    {
        "sid": "narco_china_short_1",
        "colors": ((15, 23, 42), (2, 6, 23), (250, 200, 21)),
        "a1": ("TRANSACCIONES ESPEJO EN NUEVA YORK", "Registros de la red Flying Money entre cárteles mexicanos y comercios chinos en Los Ángeles y Nueva York.", "DOCUMENTO DE INTELIGENCIA", "2024-03-15", "nc1_1.jpg"),
        "a2": ("CIRCUITO SUBTERRÁNEO DE EFECTIVO", "Intermediarios chinos liberan pesos en México mediante exportaciones comerciales con comisiones del 3%.", "REPORTE FINANCIERO", "2024-05-10", "nc1_2.jpg"),
        "a3": ("EVALUACIÓN DE AMENAZA FINANCIERA", "El sistema de blanqueo chino evita depósitos bancarios occidentales y alerta del Tesoro.", "INFORME DEA & FBI", "2024-06-01", "nc1_3.jpg")
    },
    {
        "sid": "narco_china_short_2",
        "colors": ((30, 10, 20), (10, 2, 8), (255, 77, 77)),
        "a1": ("INVERSIONES EN BIENES RAÍCES DE MANHATTAN", "Caso Tao Liu: millones del Cartel de Sinaloa lavados en rascacielos y desarrollo inmobiliario de lujo.", "EXPEDIENTE POLICIAL", "2018-09-20", "nc2_1.jpg"),
        "a2": ("REUNIONES EXCLUSIVAS EN NUEVA JERSEY", "Investigación tras encuentros con figuras políticas clave en club de golf privado en 2018.", "REGISTRO DE SEGURIDAD", "2018-11-04", "nc2_2.jpg"),
        "a3": ("CAÍDA DEL IMPERIO DE TAO LIU", "Incautación de bienes raíces y cuentas fantasma conectadas a la red de Xizhi Li.", "CORTE FEDERAL NY", "2019-02-15", "nc2_3.jpg")
    },
    {
        "sid": "narco_china_short_3",
        "colors": ((6, 30, 20), (2, 12, 8), (0, 229, 255)),
        "a1": ("FÁBRICAS QUÍMICAS DE WUHAN Y SHANGHÁI", "Exportación de precursores de fentanilo no fiscalizados camuflados como productos industriales.", "REPORTE DE ADUANAS", "2023-11-12", "nc3_1.jpg"),
        "a2": ("INCAUTACIÓN EN EL PUERTO DE MANZANILLO", "La Marina Armada de México intercepta cargamentos químicos provenientes del Pacífico.", "BOLETÍN MARÍTIMO", "2024-01-22", "nc3_2.jpg"),
        "a3": ("LABORATORIOS CLANDESTINOS DE SINALOA", "Transformación de insumos chinos en millones de dosis de alta potencia mortífera.", "DOCUMENTO INTERPOL", "2024-03-08", "nc3_3.jpg")
    },
    {
        "sid": "narco_china_short_4",
        "colors": ((40, 10, 10), (15, 2, 2), (255, 77, 77)),
        "a1": ("ALERTA DE GUERRA ASIMÉTRICA EN EL PENTÁGONO", "Analistas alertan sobre la estrategia de Pekín y la paralela con las Guerras del Opio del siglo XIX.", "ESTUDIO DE DEFENSA", "2024-02-18", "nc4_1.jpg"),
        "a2": ("INCENTIVOS FISCALES A QUÍMICAS EN CHINA", "Pekín mantiene reembolsos impositivos a exportadoras salvo bajo presión diplomática extrema.", "INFORME GEOPOLÍTICO", "2024-04-05", "nc4_2.jpg"),
        "a3": ("IMPACTO SOCIAL Y DEMOGRÁFICO EN EE.UU.", "Desagüe de divisas en dólares y devastación en el cinturón industrial norteamericano.", "MONITOR GLOBAL", "2024-05-20", "nc4_3.jpg")
    },
    {
        "sid": "narco_china_short_5",
        "colors": ((15, 23, 42), (2, 6, 23), (250, 200, 21)),
        "a1": ("OBSOLESCENCIA DE LOS MÉTODOS DE LA DEA", "Agentes buscan maletines y cuentas bancarias mientras el dinero fluye por valor comercial.", "AUDITORÍA FEDERAL", "2023-08-14", "nc5_1.jpg"),
        "a2": ("RED INFORMAL DE MENSAJERÍA FLYING MONEY", "Compensación de saldos mediante electrónica y ropa sin pasar por cámaras bancarias.", "ANÁLISIS FINANCIERO", "2023-10-30", "nc5_2.jpg"),
        "a3": ("INVISIBILIDAD EN LAS TRANSACCIONES", "Las cuentas investigadas se convierten en mercancía legal vendida antes del rastreo.", "REPORTE TÁCTICO", "2024-01-15", "nc5_3.jpg")
    },
    {
        "sid": "narco_china_short_6",
        "colors": ((10, 25, 15), (2, 10, 5), (0, 229, 255)),
        "a1": ("GRANJAS CLANDESTINAS EN BOSQUES DE MAINE", "Cientos de hectáreas rurales compradas en efectivo por organizaciones vinculadas a la mafia china.", "PERIÓDICO LOCAL MAINE", "2023-09-08", "nc6_1.jpg"),
        "a2": ("CULTIVOSS ILEGALES Y EXPLOTACIÓN LABORAL", "Fachada de cáñamo legal ocultando megaplantaciones clandestinas con electricidad robada.", "INFORME DE POLICÍA", "2023-12-01", "nc6_2.jpg"),
        "a3": ("FINANCIAMIENTO AL CARTEL DE SINALOA", "Ganancias millonarias del mercado negro estadounidense inyectadas al blanqueo de droga.", "EXPEDIENTE JUDICIAL", "2024-02-10", "nc6_3.jpg")
    },
    {
        "sid": "narco_china_short_7",
        "colors": ((25, 20, 10), (10, 8, 2), (250, 200, 21)),
        "a1": ("DESTRUCCIÓN DEL MONOPOLIO COLOMBIANO", "Las triadas chinas desploman las tarifas de lavado del 20% al 3% con pago inmediato en pesos.", "HISTORIA DEL CRIMEN", "2022-06-14", "nc7_1.jpg"),
        "a2": ("EFICIENCIA FINANCIERA EN TIEMPO RÉCORD", "Ningún grupo criminal logró competir contra la velocidad de liquidez del sistema chino.", "ESTUDIO ECONÓMICO", "2022-09-28", "nc7_2.jpg"),
        "a3": ("MONOPOLIO MUNDIAL DEL BLANQUEO NARCO", "Pekín se convierte en la capital indiscutible de la limpieza de activos internacionales.", "REPORTE INTERPOL", "2023-01-18", "nc7_3.jpg")
    },
    {
        "sid": "narco_china_short_8",
        "colors": ((15, 23, 42), (2, 6, 23), (250, 200, 21)),
        "a1": ("REGULACIONES POST 11 DE SEPTIEMBRE", "Leyes bancarias stricts activan alarmas del Tesoro ante depósitos en efectivo masivos.", "REGISTRO BANCARIO", "2006-04-12", "nc8_1.jpg"),
        "a2": ("ELIMINACIÓN TOTAL DE LOS BANCOS", "Efectivo recibido en EE.UU. paga compras a importadores que necesitan dólares en China.", "DOCUMENTO FINANCIERO", "2023-07-19", "nc8_2.jpg"),
        "a3": ("EL CÍRCULO INVISIBLE DEL COMERCIO", "Transferencia de valor pura sin firma electrónica ni intervención de la reserva federal.", "REGISTRO DE COMERCIO", "2023-11-05", "nc8_3.jpg")
    },
    {
        "sid": "narco_china_short_9",
        "colors": ((30, 10, 20), (10, 2, 8), (255, 77, 77)),
        "a1": ("PERFIL DE XIZHI LI: EL LIMPIADOR DEFINITIVO", "Empresario de trajes italianos y casinos unmitigated como el cerebro financiero de Sinaloa.", "CAPTURAS FBI", "2021-10-15", "nc9_1.jpg"),
        "a2": ("RED DE EMPRESAS FANTASMA EN 20 ESTADOS", "Movimiento de más de $300 millones usando identidades falsas y contabilidad oculta.", "CORTE DISTRITAL", "2022-01-20", "nc9_2.jpg"),
        "a3": ("LA COLUMNA VERTEBRAL DEL NARCO GLOBAL", "Arresto histórico que desnudó la fusión entre carteles latinos y triadas asiáticas.", "REPORTE DE PRENSA", "2022-04-12", "nc9_3.jpg")
    },
    {
        "sid": "narco_china_short_10",
        "colors": ((15, 23, 42), (2, 6, 23), (250, 200, 21)),
        "a1": ("CEPO CAMBIARIO DE PEKÍN ($50,000 ANUALES)", "Restricciones a la fuga de capitales empujan a la élite china a buscar dólares narco.", "ANÁLISIS ECONÓMICO", "2023-03-22", "nc10_1.jpg"),
        "a2": ("MANSIONES EN MIAMI Y VANCOUVER", "Entrega de yuanes en Asia a cambio de dólares en efectivo generados por venta de droga.", "REGISTRO INMOBILIARIO", "2023-06-30", "nc10_2.jpg"),
        "a3": ("SIMBIOSIS PERFECTA NARCO-EMPRESARIAL", "Integración de la fuga de divisas de millonarios chinos con la liquidez de los carteles.", "INVESTIGACIÓN GLOBAL", "2023-10-14", "nc10_3.jpg")
    },
    {
        "sid": "narco_china_short_11",
        "colors": ((10, 25, 20), (2, 10, 8), (0, 229, 255)),
        "a1": ("TRADE-BASED MONEY LAUNDERING EN ADUANAS", "Sobrefacturación de contenedores con ropa y teléfonos celulares para mover riqueza legal.", "MANUAL ADUANERO", "2023-02-14", "nc11_1.jpg"),
        "a2": ("INSPECCIONES MARÍTIMAS SIN HALLAZGOS", "Policía encuentra mercancía comercial genuina tapando transferencias de miles de millones.", "REPORTE DE PUERTOS", "2023-05-19", "nc11_2.jpg"),
        "a3": ("TRANSFERENCIA DE VALOR LEGAL A SIMPLE VISTA", "Operación logística limpia que invalida el control fronterizo tradicional.", "REVISTA DE LOGÍSTICA", "2023-09-02", "nc11_3.jpg")
    },
    {
        "sid": "narco_china_short_12",
        "colors": ((40, 10, 10), (15, 2, 2), (255, 77, 77)),
        "a1": ("PARALELISMO CON LAS GUERRAS DEL OPIO (S. XIX)", "Occidente debilitó a China con adicciones; hoy precursores químicos desangran a EE.UU.", "PARALELO HISTÓRICO", "2024-01-10", "nc12_1.jpg"),
        "a2": ("DEVASTACIÓN DE LA FUERZA LABORAL", "Impacto social severo sobre la juventud y la productividad del cinturón industrial.", "REPORTE DE SALUD", "2024-03-29", "nc12_2.jpg"),
        "a3": ("IMPACTO EN LA SEGURIDAD NACIONAL", "Guerra sin misiles que socava la estabilidad interna del gigante norteamericano.", "ANÁLISIS ESTRATÉGICO", "2024-05-15", "nc12_3.jpg")
    },
    {
        "sid": "narco_china_short_13",
        "colors": ((15, 23, 42), (2, 6, 23), (250, 200, 21)),
        "a1": ("EL NUEVO IMPERIO NARCO TRANSNACIONAL", "Fusión de la violencia de los carteles mexicanos y la tecnología financiera china.", "INFORME FINAL DE SEGURIDAD", "2024-04-18", "nc13_1.jpg"),
        "a2": ("INEXPUGNABILIDAD ANTE LEYES LOCALES", "Estructura criminal hiperconectada invulnerable a patrullas policiales fragmentadas.", "ESTUDIO DIPLOMÁTICO", "2024-06-02", "nc13_2.jpg"),
        "a3": ("EL DESAFÍO DEL LIBRE COMERCIO GLOBAL", "El dinero y los químicos seguirán fluyendo mientras exista la globalización de mercados.", "CONCLUSIÓN GEOPOLÍTICA", "2024-07-01", "nc13_3.jpg")
    },

    # Guerra Antigua (10 Shorts)
    {
        "sid": "guerra_antigua_short_1",
        "colors": ((25, 15, 10), (10, 5, 2), (250, 200, 21)),
        "a1": ("EL GRAN MITO DE HOLLYWOOD EN EL CINE", "Esprintar a toda velocidad rompe la falange y conduce a una masacre inmediata.", "ESTUDIO HISTÓRICO", "490 A.C.", "ga1_1.jpg"),
        "a2": ("DESINTEGRACIÓN DE LA LÍNEA DE LANZAS", "Soldados aislados sin cobertura de escudos ejecutados en segundos por el bloque.", "CRÓNICA BÉLICA", "338 A.C.", "ga1_2.jpg"),
        "a3": ("LA REALIDAD TÁCTICA DEL PASO MARCADO", "Avanzar a paso firme mantenía la cohesión de la pared de bronce espartana.", "MANUSCRITO GRIEGO", "431 A.C.", "ga1_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_2",
        "colors": ((10, 25, 20), (2, 10, 8), (0, 229, 255)),
        "a1": ("EL MURO DE ESCUDOS COMO MÁQUINA BIOMECÁNICA", "Cada soldado cubre el costado izquierdo de su compañero con su propio escudo.", "CÓDIGO VIKINGO", "1066 A.D.", "ga2_1.jpg"),
        "a2": ("EL PELIGRO DE LA HEROICIDAD INDIVIDUAL", "Adelantarse corriendo abrías brechas mortales por donde penetraban las lanzas.", "CRÓNICA ANGLOSAJONA", "911 A.D.", "ga2_2.jpg"),
        "a3": ("IMPENETRABILIDAD DE LA MASA APRETADA", "El bloque avanza cadencioso aplastando la resistencia por pura masa física.", "HISTORIA MILITAR", "1014 A.D.", "ga2_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_3",
        "colors": ((30, 10, 10), (10, 2, 2), (255, 77, 77)),
        "a1": ("BIOME CÁNICA DEL CANSANCIO EXTREMO", "Cargar 30kg de Lorica Segmentata, casco y Scutum drena la resistencia en 200m.", "ANALES ROMANOS", "100 A.C.", "ga3_1.jpg"),
        "a2": ("COLLAPSE ANTE DEFENTORES DESCANSA DOS", "Infantería exhausta cae al suelo ante el primer empujón de la línea enemiga.", "HISTORIAS DE HERÓDOTO", "480 A.C.", "ga3_2.jpg"),
        "a3": ("GESTIÓN DEL ESFUERZO COMO REGLA DE ORO", "Conservar el aliento era la diferencia clave entre vivir o ser ejecutado en el barro.", "MANUAL LEGIONARIO", "50 A.C.", "ga3_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_4",
        "colors": ((25, 15, 10), (10, 5, 2), (250, 200, 21)),
        "a1": ("EL SANGRIENTO EMPUJE DEL OTHIS MOS", "Las batallas eran choques masivos de masa corporal y hombros, no duelos de esgrima.", "TUCÍDIDES HISTORIAS", "431 A.C.", "ga4_1.jpg"),
        "a2": ("LA ESTABILIDAD DEL BLOQUE DE BRONCE", "Filas traseras empujan la espalda de los delanteros para volcar la pared rival.", "BATALLA DE LEUCTRA", "371 A.C.", "ga4_2.jpg"),
        "a3": ("CHOQUE DIRECTO CONTRA LA PARED HUMANA", "Correr hacia la falange era como estrellarse contra un muro de ladrillos macizo.", "TÁCTICA HOPLITA", "362 A.C.", "ga4_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_5",
        "colors": ((15, 23, 42), (2, 6, 23), (250, 200, 21)),
        "a1": ("LA EXCEPCIÓN DE MARATÓN (490 A.C.)", "Atenienses avanzaron a paso firme y esprintaron únicamente los últimos 100 metros.", "GACETA ATENIENSE", "490 A.C.", "ga5_1.jpg"),
        "a2": ("ESCAPANDO DE LA LLUVIA DE FLECHAS PER SAS", "Cruzar en segundos la zona de muerte de los arqueros para evitar ser masacrados.", "REGISTRO PER SA", "490 A.C.", "ga5_2.jpg"),
        "a3": ("MANTENIENDO LA LÍNEA HASTA EL CHOQUE", "Aceleración calculada que conservó la pared de escudos intacta al impactar.", "HISTORIA DE GRECIA", "490 A.C.", "ga5_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_6",
        "colors": ((10, 25, 20), (2, 10, 8), (0, 229, 255)),
        "a1": ("GRADUS MILITARIS: EL PASO ROMANO A 4 KM/H", "Marcha disciplinada a ritmo exacto para conquistar todo el Mediterráneo.", "MANUAL DE LA LEGION", "146 A.C.", "ga6_1.jpg"),
        "a2": ("LANZAMIENTO DE PILUM A 15 METROS", "Jabalines pesados inutilizan los escudos enemigos antes del contacto con Gladius.", "GUERRAS GALAS", "50 A.C.", "ga6_2.jpg"),
        "a3": ("PASO CORTO Y ESPADA COR TANTE", "Legionarios avanzaban calmados tras el Scutum destruyendo al enemigo sin correr.", "ANALES IMPERIALES", "100 A.D.", "ga6_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_7",
        "colors": ((40, 10, 10), (15, 2, 2), (255, 77, 77)),
        "a1": ("EL 80% DE MUERTES OCURRÍAN EN LA HUIDA", "En el choque frontal morían muy pocos; la masacre comenzaba al romper la línea.", "ANÁLISIS CANNAS", "216 A.C.", "ga7_1.jpg"),
        "a2": ("PERSECUCIÓN DE CABALLERÍA POR LA ESPALDA", "Soldados aterrados en huida desarmados ejecutados por jinetes perseguidores.", "GAUGAMELA REPORT", "331 A.C.", "ga7_2.jpg"),
        "a3": ("EL DESTINO FATAL DEL SOL DADO DESORDERADO", "Dar la espalda convertía al guerrero en blanco indefenso ante la lanza enemiga.", "HISTORIA ANTIGUA", "100 A.C.", "ga7_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_8",
        "colors": ((25, 15, 10), (10, 5, 2), (250, 200, 21)),
        "a1": ("LA FLAUTA AULOS Y LA FALANGE ESPARTANA", "Flautistas al frente marcaban el metrónomo militar para evitar prisas o retrasos.", "CÓDIGO ESPARTANO", "418 A.C.", "ga8_1.jpg"),
        "a2": ("CADENCIA PERFECTA DE LOS MAN TOS ROJOS", "El ritmo musical mantenía la muralla de bronce sin fisuras ni tropezones.", "ANÁBASIS DE JENOFONTE", "400 A.C.", "ga8_2.jpg"),
        "a3": ("EL TERROR DE LA MARCHA SILENCIOSA Y RÍTMICA", "Enemigos aterrorizados ante la calma y sincronía de los guerreros de Esparta.", "HISTORIA DE PELOPONESO", "431 A.C.", "ga8_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_9",
        "colors": ((15, 23, 42), (2, 6, 23), (250, 200, 21)),
        "a1": ("EL MURO ANGLOSAJÓN EN SENLAC HILL 1066", "Resistencia de horas contra las cargas de caballería normanda en lluvia y barro.", "TAPIZ DE BAYEUX", "1066 A.D.", "ga9_1.jpg"),
        "a2": ("LA FALSA RETIRADA DE GUILLERMO EL CONQUISTADOR", "Normandos simularon huir loma abajo engañando a parte de los defensores saxones.", "MANUSCRITO NORMANDO", "1066 A.D.", "ga9_2.jpg"),
        "a3": ("ANIKILACIÓN AL ABANDONAR LA FORMACIÓN", "Los saxones que corrieron para perseguir fueron rodeados y masacrados en el campo.", "REGISTRO DE HASTINGS", "1066 A.D.", "ga9_3.jpg")
    },
    {
        "sid": "guerra_antigua_short_10",
        "colors": ((10, 25, 20), (2, 10, 8), (0, 229, 255)),
        "a1": ("LA REGLA DE ORO DEL VETERANO ANTIGUO", "Caminar con calma era la tecnología militar de supervivencia más avanzada.", "MEMORIAS VETERANAS", "100 A.D.", "ga10_1.jpg"),
        "a2": ("ROTACIÓN DE LÍNEAS FATIGADAS A RETAGUARDIA", "Reemplazo continuo de combatientes exhaustos por tropas frescas y descansadas.", "ESTRATEGIA ROMANA", "200 A.D.", "ga10_2.jpg"),
        "a3": ("LA VICTORIA DE LA DISCIPLINA SOBRE LA FURIA", "Mantener el hombro pegado al compañero separaba la gloria de la ejecución.", "SÍNTESIS DE GUERRA", "300 A.D.", "ga10_3.jpg")
    }
]

def generate_all_visual_artworks():
    print("=" * 80)
    print("  KINESIO ARTWORK STUDIO: GENERATING 69 HIGH-IMPACT VISUAL ARTWORKS")
    print("=" * 80)
    
    asset_map = {}
    
    for item in VISUAL_ARTWORK_SPECS:
        sid = item["sid"]
        colors = item["colors"]
        
        a1_title, a1_sub, a1_badge, a1_date, fn1 = item["a1"]
        a2_title, a2_sub, a2_badge, a2_date, fn2 = item["a2"]
        a3_title, a3_sub, a3_badge, a3_date, fn3 = item["a3"]
        
        p1 = create_thematic_visual_artwork(a1_title, a1_sub, a1_badge, a1_date, colors, fn1)
        p2 = create_thematic_visual_artwork(a2_title, a2_sub, a2_badge, a2_date, colors, fn2)
        p3 = create_thematic_visual_artwork(a3_title, a3_sub, a3_badge, a3_date, colors, fn3)
        
        asset_map[sid] = [p1, p2, p3]
        print(f"  [SUCCESS] Created 3 Visual Assets for Short '{sid}'")

    map_json_path = os.path.join(BASE_DIR, "campaign_assets_map.json")
    with open(map_json_path, "w", encoding="utf-8") as f:
        json.dump(asset_map, f, indent=2, ensure_ascii=False)
        
    print("\n" + "=" * 80)
    print(f"  SUCCESS: 69 High-Contrast Visual Artworks Generated and Mapped!")
    print(f"  Mapping File: {map_json_path}")
    print("=" * 80)

if __name__ == "__main__":
    generate_all_visual_artworks()
