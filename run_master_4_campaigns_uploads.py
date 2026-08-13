# -*- coding: utf-8 -*-
"""
VAREGO MASTER AUTOMATED UPLOADER: 48 SHORTS ACROSS 4 CAMPAIGNS FOR DOMINUSBABEL
"""

import os
import sys
import time
import subprocess
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
RENDERED_DIR = os.path.join(PROJECT_DIR, "final_rendered_mp4s")
UPLOAD_LOG = os.path.join(PROJECT_DIR, "uploaded_48_shorts_log.txt")
VAREGO_UPLOADER = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

# 48 Shorts Metadata Dictionary
UPLOADS_QUEUE = [
    # Campaign 1: Narco China (13 Shorts)
    ("narco_china_short_1", "Las Transacciones Espejo que Desafían a la DEA 🇨🇳💵 #shorts", "Análisis del sistema Flying Money y el lavado del narcotráfico entre China y México. #narco #china #dea #dinero"),
    ("narco_china_short_2", "De Lavar Dinero Narco a Mar-a-Lago 🏰 #shorts", "El ascenso de los banquetes chinos de lavado de dinero y la élite política. #maralago #eeuu #investigacion"),
    ("narco_china_short_3", "El Negocio Secreto de los Precursores Químicos 🧪 #shorts", "Cómo Wuhan se convirtió en la capital mundial de los precursores químicos. #wuhan #quimica #fentanilo"),
    ("narco_china_short_4", "La Guerra Asimétrica del Partido Comunista Chino ⚔️ #shorts", "Estrategia híbrida y desestabilización económica a través de redes de contrabando. #geopolitica #china #eeuu"),
    ("narco_china_short_5", "Por qué la DEA Falla Ante el Sistema Chino 🚔 #shorts", "Las limitaciones de la inteligencia estadounidense frente al sistema bancario paralelo chino. #dea #policia #seguridad"),
    ("narco_china_short_6", "Las Granjas Ilegales de Marihuana en Maine 🌿 #shorts", "Redes chinas operando granjas masivas en territorio rural norteamericano. #maine #noticias #cripto"),
    ("narco_china_short_7", "El Truco del 3%: Tarifas Imposibles de Competir 💸 #shorts", "Cómo los banqueros chinos redujeron las comisiones de lavado del 18% al 3%. #finanzas #economia #banca"),
    ("narco_china_short_8", "Cárteles sin Bancos Tradicionales 🏦 #shorts", "La sustitución del dólar bancario por compras masivas de bienes de lujo. #carteles #lujo #comercio"),
    ("narco_china_short_9", "Xizhi Li: El Limpiador Definitivo 💼 #shorts", "La historia del hombre que revolucionó el movimiento de capitales clandestinos. #historia #personajes #crimen"),
    ("narco_china_short_10", "Fuga de Capitales Inversa de la Élite China 🛫 #shorts", "Cómo la prohibición de sacar dólares de China impulsó el mercado narco. #dolares #china #inversion"),
    ("narco_china_short_11", "Trade-Based Money Laundering: Fraude Aduanero 📦 #shorts", "El intercambio de iPhones y ropa por efectivo del narcotráfico. #comercio #aduanas #negocios"),
    ("narco_china_short_12", "Fentanilo y Guerra Híbrida: La Opio al Revés 💊 #shorts", "La inversión de la Guerra del Opio del siglo XIX en el siglo XXI. #historia #guerra #salud"),
    ("narco_china_short_13", "El Futuro Global del Narcotráfico 🌐 #shorts", "La alianza silenciosa entre redes chinas y carteles latinoamericanos. #futuro #latam #internacional"),

    # Campaign 2: Guerra Antigua (10 Shorts)
    ("guerra_antigua_short_1", "El Gran Mito de Hollywood sobre las Batallas Antiguas 🛡️ #shorts", "Por qué las cargas de duelo individual de Hollywood eran suicidas en la antigüedad. #historia #cine #mitos"),
    ("guerra_antigua_short_2", "La Fuerza Imparable del Muro de Escudos 🛡️⚔️ #shorts", "Física y biomecánica del muro de escudos espartano y vikingo. #esparta #vikingos #historia"),
    ("guerra_antigua_short_3", "La Biomecánica del Cansancio Extremo en Combate 🏃‍♂️ #shorts", "El colapso físico de los legionarios tras 15 minutos en primera línea. #roma #legion #ejercito"),
    ("guerra_antigua_short_4", "El Empuje del Othismos: Choque de Masas 💥 #shorts", "Cómo la presión física del grupo ganaba batallas sin usar las espadas. #grecia #falange #guerra"),
    ("guerra_antigua_short_5", "La Excepción de Maratón (490 a.C.) 🏛️ #shorts", "La carga a la carrera ateniense que sorprendió a los arqueros persas. #maraton #persia #grecia"),
    ("guerra_antigua_short_6", "La Disciplina Táctica de la Legión Romana 🏛️ #shorts", "El relevo rotativo de líneas de combate que mantuvo a Roma victoriosa. #roma #legionarios #tactica"),
    ("guerra_antigua_short_7", "La Masacre de la Huida: Muerte por la Espalda ⚔️ #shorts", "El 90% de las bajas en combate ocurrian cuando un bando rompía filas y huía. #batalla #historia #estrategia"),
    ("guerra_antigua_short_8", "La Flauta y la Falange Espartana 🎶 #shorts", "El uso de la música de aulos para coordinar la marcha impecable espartana. #esparta #musica #tactica"),
    ("guerra_antigua_short_9", "El Muro Saxón en Hastings (1066) 🏰 #shorts", "La batalla decisiva de Inglaterra y el impacto del muro de escudos. #inglaterra #1066 #vikingos"),
    ("guerra_antigua_short_10", "La Regla de Oro del Veterano Antiguo 🥇 #shorts", "Mantener la formación era la única diferencia entre sobrevivir o morir. #historia #veteranos #guerra"),

    # Campaign 3: Steam Monopoly (12 Shorts)
    ("steam_short_1", "¿Por qué Steam Podría Quebrar por una Demanda? 🎮 #shorts", "La demanda multimillonaria en Reino Unido por abuso de posición dominante. #steam #gaming #noticias"),
    ("steam_short_2", "El Impuesto Secreto del 30% que Pagas sin Saberlo 💳 #shorts", "Cómo la tasa del 30% de Valve infla los precios de los videojuegos en PC. #valve #precios #pcgaming"),
    ("steam_short_3", "Epic Games vs Steam: La Guerra por el 12% ⚔️ #shorts", "Tim Sweeney regala juegos mientras Valve mantiene el 30% intacto. #epicgames #steam #guerra"),
    ("steam_short_4", "¿Tus Juegos en Steam son Realmente Tuyos? 🔒 #shorts", "La cruda realidad de las licencias digitales revocables sin propiedad real. #steam #licencias #derechos"),
    ("steam_short_5", "La Cláusula MFN: La Trampa de Precios de Valve 📜 #shorts", "El contrato que impide a los desarrolladores vender más barato en otras tiendas. #monopolio #negocios #pc"),
    ("steam_short_6", "El Caso Wolfire Games que Amenaza a Gabe Newell ⚖️ #shorts", "El juicio federal en EE.UU. que avanzó contra las prácticas de Valve. #gabenewell #justicia #tribunales"),
    ("steam_short_7", "El Fin de los Precios Regionales Baratos 🌎 #shorts", "La dolarización de tiendas en Argentina y Turquía tras la migración por VPN. #argentina #turquia #economia"),
    ("steam_short_8", "¿Por qué Ningún Competidor Puede Vencer a Steam? 🌐 #shorts", "El efecto red social, perfiles e inventarios que amarran a 100M de usuarios. #comunidad #steam #redes"),
    ("steam_short_9", "La Fortuna de Gabe Newell y el Imperio sin Accionistas 👑 #shorts", "La empresa más rentable por empleado del mundo sin rendir cuentas a Wall Street. #gabenewell #finanzas #empresa"),
    ("steam_short_10", "La Tasa Valve y la Crisis de los Estudios Indie 🏚️ #shorts", "La quiebra de pequeños desarrolladores tras los costes de distribución. #indie #gaming #estudios"),
    ("steam_short_11", "¿Debería la U.E. Obligar a Dividir Steam? 🇪🇺 #shorts", "La Ley de Mercados Digitales de Bruselas apuntando a la distribución digital en PC. #unioneuropea #leyes #tech"),
    ("steam_short_12", "El Futuro del Gaming: ¿Nube o Monopolio? ☁️ #shorts", "La batalla entre la tienda de Steam y el streaming de Microsoft y GeForce. #cloudgaming #microsoft #futuro"),

    # Campaign 4: Programadores IA (13 Shorts)
    ("programadores_short_1", "¿Por qué Ningún Junior Conseguirá Trabajo en 2026? 💻 #shorts", "Jason Lemkin creando apps completas con IA sin saber escribir código. #programacion #ia #empleo"),
    ("programadores_short_2", "El Ridículo que Reveló la Verdad de la IA ⚠️ #shorts", "Aplicaciones generadas por IA que fallan en seguridad básica sin supervisión. #seguridad #codigo #dev"),
    ("programadores_short_3", "Devin y Claude 3.5: ¿El Fin de los Ingenieros? 🤖 #shorts", "Agentes autónomos resolviendo tickets de GitHub reales sin intervención humana. #devin #claude #tecnologia"),
    ("programadores_short_4", "El Error Fatal de Aprender Sintaxis en 2026 🛑 #shorts", "Por qué memorizar comandos de Python o JS es profesionalmente obsoleto. #python #javascript #aprender"),
    ("programadores_short_5", "La Extinción de los Bootcamps de Programación 🎓 #shorts", "El colapso de las academias de 6 meses frente a herramientas de voz e IA. #bootcamp #educacion #tech"),
    ("programadores_short_6", "Alucinaciones y Bugs: El Peligro del Código IA 🚨 #shorts", "Vulnerabilidades de inyección SQL e importación de librerías inexistentes. #ciberseguridad #bugs #alerta"),
    ("programadores_short_7", "El Nace del Programador 10x Autónomo 🦄 #shorts", "Fundadores técnicos construyendo unicornios sin contratar ingenieros adicionales. #startup #unicornio #10x"),
    ("programadores_short_8", "¿Por qué los Seniors son Ahora Más Caros que Nunca? 💎 #shorts", "La paradoja: a más código generado por IA, más valioso el arquitecto senior. #senior #arquitectura #sueldos"),
    ("programadores_short_9", "¿Qué Debes Estudiar si la IA ya Programa? 🧠 #shorts", "La transición crucial hacia la ingeniería de contexto y validación de seguridad. #futuro #estudios #habilidades"),
    ("programadores_short_10", "La Trampa del Código Basura Generado por IA 🗑️ #shorts", "La deuda técnica inmanejable que acumulan las empresas que abusan de la IA. #deudatecnica #software #empresa"),
    ("programadores_short_11", "¿Deberían Regularse los Agentes de Código IA? ⚖️ #shorts", "La responsabilidad legal tras un fallo de seguridad provocado por un prompt. #leyes #responsabilidad #ia"),
    ("programadores_short_12", "Replit y la Democracia Total de Crear Software 🌐 #shorts", "Médicos y abogados creando sus propias herramientas sin intermediarios tech. #replit #no-code #creadores"),
    ("programadores_short_13", "El Futuro del Software: De Escribir Código a Dirigir IA 🎼 #shorts", "El programador del futuro como director de orquesta de modelos de IA. #futuro #ia #innovacion"),

    # Campaign 5: Ciberseguridad & IA (11 Shorts)
    ("ciberseguridad_short_1", "El Día que EE.UU. Prohibió la IA Más Avanzada por Pánico 🚨 #shorts", "El veto gubernamental a Claude Mythos (Anthropic) por riesgos de ciberataques. #ciberseguridad #ia #anthropic #geopolitica"),
    ("ciberseguridad_short_2", "La IA Hacker de 0 Días que Aterroriza al Pentágono 💻 #shorts", "Agentes de IA descubriendo fallos de seguridad y creando exploits autónomos. #hacking #seguridad #ia #pentagono"),
    ("ciberseguridad_short_3", "El Impuesto Obligatorio que Toda Empresa Debe Pagar 💸 #shorts", "Por qué el gasto en ciberseguridad es inelástico y obligatorio para no quebrar. #empresas #negocios #inversion #tech"),
    ("ciberseguridad_short_4", "Por qué la Ciberseguridad NUNCA Caerá en Recesión 🏦 #shorts", "La inmunidad de la seguridad digital frente a las crisis y recesiones globales. #finanzas #recesion #inversiones #wallstreet"),
    ("ciberseguridad_short_5", "La Ciberguerra Silenciosa contra la Infraestructura Crítica ⚡ #shorts", "Ataques de estados-nación contra redes eléctricas, agua y hospitales. #ciberguerra #geopolitica #defensa #tecnologia"),
    ("ciberseguridad_short_6", "El Modelo OSI Explicado para Inversores en Tech 🌐 #shorts", "Las 7 capas de Internet y cómo se divide el capital en ciberseguridad. #modeloosi #inversiones #bolsa #tecnologia"),
    ("ciberseguridad_short_7", "Capa Baja: El Imperio Hardware de Cisco y Arista 🔌 #shorts", "La protección de fibra óptica, cables y conmutadores físicos en data centers. #hardware #cisco #arista #redes"),
    ("ciberseguridad_short_8", "Capa Media: La Muralla de Fuego de Palo Alto y Fortinet 🛡️ #shorts", "Firewalls de red, inspección de paquetes en tiempo real y Cloudflare. #firewall #paloalto #fortinet #cloud"),
    ("ciberseguridad_short_9", "Capa Alta: CrowdStrike y el Negocio de la Identidad 🔑 #shorts", "Protección de endpoints, ordenadores portátiles e identidades corporativas. #crowdstrike #microsoft #endpoint #seguridad"),
    ("ciberseguridad_short_10", "Deepfakes de Voz y la Estafa del CEO por IA 👤 #shorts", "Phishing ultrarrealista clonando voz y video de directores en tiempo real. #deepfake #phishing #ia #estafas"),
    ("ciberseguridad_short_11", "El Futuro de la IA: ¿Espada de Hackers o Escudo Global? 🛡️ #shorts", "La carrera armamentista digital entre IA ofensiva y IA defensiva. #futuro #ia #ciberseguridad #innovacion"),

    # Campaign 6: La Gran Estafa de la Propiedad Digital (13 Shorts)
    ("propiedad_short_1", "¿Sabías que Tu PS5 NO es Realmente Tuya? 🎮 #shorts", "Términos de licencia revocables que te prohíben modificar tu consola pagada. #ps5 #nintendo #propiedad #gaming"),
    ("propiedad_short_2", "El Baneo a Distancia que Invalida tu Consola de $500 🚫 #shorts", "El control corporativo que inhabilita tu dispositivo si violas los términos de servicio. #baneo #sony #hardware #derechos"),
    ("propiedad_short_3", "El Día que Ubisoft Borró un Juego que Pagaste 🛑 #shorts", "El caso The Crew: eliminación del juego y revocación de licencias compradas. #ubisoft #thecrew #gaming #polemica"),
    ("propiedad_short_4", "Por qué las Tiendas Digitales Pueden Quitarte Todo 📲 #shorts", "La trampa legal de alquilar licencias digitales temporales en lugar de comprar. #steam #playstation #licencias #leyes"),
    ("propiedad_short_5", "Sony Borrando Películas Compradas en PlayStation Network 🎬 #shorts", "La pérdida de contenido de Discovery en PSN por vencimiento de licencias. #sony #discovery #cine #streaming"),
    ("propiedad_short_6", "La Trampa de las Consolas Sin Lector de Disco 💿 #shorts", "La eliminación del mercado de segunda mano y el monopolio de tiendas oficiales. #consolas #digital #precios #mercadolibre"),
    ("propiedad_short_7", "Game Pass y la Ilusión de la Biblioteca Infinita 🟢 #shorts", "La rotación constante de títulos en suscripciones que destruye la colección personal. #gamepass #psplus #suscripciones #gaming"),
    ("propiedad_short_8", "Asientos Calefactables por Suscripción: El Futuro del Software 🚗 #shorts", "BMW cobrando mensualidad por activar características físicas instaladas en coches. #bmw #autos #micropagos #suscripciones"),
    ("propiedad_short_9", "¿Qué Pasará con tu Cuenta de Steam cuando Gabe Newell Falte? 👑 #shorts", "Las cuentas de Steam no son hereditarias ni se pueden transferir por testamento. #steam #gabenewell #herencia #legal"),
    ("propiedad_short_10", "El Derecho a Reparar: Las Marcas Contra tus Herramientas 🛠️ #shorts", "Piezas emparejadas por software para evitar reparaciones independientes. #righttorepair #reparacion #apple #tecnologia"),
    ("propiedad_short_11", "La Destrucción de la Historia Gaming: Preservación vs DRM 🏛️ #shorts", "El 87% de los videojuegos clásicos perdidos por cierre de tiendas y leyes DRM. #preservacion #emulacion #retro #historia"),
    ("propiedad_short_12", "\"No Poseerás Nada y Serás Feliz\": La Distopía Digital 🌐 #shorts", "La transición global del capitalismo de propiedad al modelo de arrendamiento perpetuo. #distopia #economia #futuro #arriendo"),
    ("propiedad_short_13", "El Movimiento de Resistencia: Cómo Proteger tu Propiedad Real 🛡️ #shorts", "Plataformas DRM-Free como GOG, formato físico y respaldo personal. #gog #drmfree #resistencia #propiedad"),

    # Campaign 7: La Estafa de la Chica Anime (Pig Butchering Scams) (8 Shorts)
    ("estafa_anime_short_1", "La Solicitud de Amistad de la Chica Anime que Te Quere Estafar 🎣 #shorts", "La trampa inicial tras hacer una gran partida en LoL, CS2 o Valorant. #estafas #gaming #anime #discord"),
    ("estafa_anime_short_2", "¿Qué es el \"Pig Butchering\"? La Anatomía de la Matadero Digital 🐖 #shorts", "La técnica Sha Zhu Pan de engordar emocionalmente a la víctima antes del fraude. #pigbutchering #shazhupan #fraude #psicologia"),
    ("estafa_anime_short_3", "De Discord a WhatsApp: La Trampa del Aislamiento Emocional 📱 #shorts", "Cómo mueven a la víctima a mensajes privados para evitar advertencias de amigos. #whatsapp #telegram #ingenieriasocial #seguridad"),
    ("estafa_anime_short_4", "La Falsa Plataforma de Criptomonedas donde Siempre Ganas 📈 #shorts", "Sitios web manipulados que muestran ganancias falsas para enganchar depósitos. #cripto #trading #estafas #inversiones"),
    ("estafa_anime_short_5", "La Falsa Retirada de $50: El Anzuelo Definitivo de la Estafa 🎣 #shorts", "Dejar retirar $50 reales para destruir el escepticismo y pedir todos tus ahorros. #anzuelo #manipulacion #finanzas #banco"),
    ("estafa_anime_short_6", "El \"Impuesto de Desbloqueo\": La Trampa de la que Nadie Escapa 💸 #shorts", "Exigir un 20% adicional de supuestos impuestos antes de desaparecer con todo. #impuestos #bloqueo #perdidatotal #alerta"),
    ("estafa_anime_short_7", "El Lado Oscuro: Granjas de Estafadores Secuestrados en Asia ⛓️ #shorts", "Víctimas de trata humana secuestradas en Myanmar y Camboya obligadas a estafar. #myanmar #camboya #tratadepersonas #noticias"),
    ("estafa_anime_short_8", "La Regla de Oro para NUNCA Caer en una Estafa de Romance 🛡️ #shorts", "El escepticismo digital y las reglas de oro para proteger tu dinero y salud mental. #prevencion #seguridad #consejos #educacion")
]

def load_uploaded_log():
    if not os.path.exists(UPLOAD_LOG):
        return set()
    with open(UPLOAD_LOG, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def register_upload(sid):
    with open(UPLOAD_LOG, "a", encoding="utf-8") as f:
        f.write(sid + "\n")

def upload_single_short(sid, title, desc):
    video_path = os.path.join(RENDERED_DIR, f"{sid}_final.mp4")
    if not os.path.exists(video_path):
        print(f"  [WAITING] Video '{sid}_final.mp4' is still compiling...")
        return False
        
    print(f"\n" + "=" * 80)
    print(f"  [VAREGO UPLOADING] '{sid}' -> DOMINUSBABEL")
    print(f"  Title: {title}")
    print(f"  File: {video_path}")
    print("=" * 80)
    
    # Kill orphan chrome instances and remove SingletonLock before launch
    try:
        subprocess.run(["powershell", "-Command", "Stop-Process -Name 'chrome','chromedriver' -Force -ErrorAction SilentlyContinue; Remove-Item -Path C:\\Users\\jegom\\VAREGO\\browser_profile\\youtube_shorts_profile\\Singleton* -Force -ErrorAction SilentlyContinue"], capture_output=True)
        time.sleep(2)
    except:
        pass
    
    cmd = [
        "node", VAREGO_UPLOADER,
        "--file", video_path,
        "--title", title,
        "--desc", desc,
        "--is_short",
        "--draft"
    ]
    
    res = subprocess.run(cmd, cwd=r"C:\Users\jegom\VAREGO", capture_output=True, text=True, encoding="utf-8")
    
    if res.returncode == 0:
        print(f"  [SUCCESS] '{sid}' uploaded to DOMINUSBABEL YouTube Studio!")
        register_upload(sid)
        return True
    else:
        print(f"  [ERROR] Failed uploading '{sid}'")
        print("  Stdout:", res.stdout[:500] if res.stdout else "None")
        print("  Stderr:", res.stderr[:500] if res.stderr else "None")
        return False

def main():
    print("================================================================================")
    print("  VAREGO MASTER AUTOMATED UPLOADER: 48 SHORTS FOR DOMINUSBABEL")
    print("================================================================================\n")
    
    uploaded_set = load_uploaded_log()
    print(f"Currently uploaded: {len(uploaded_set)} / {len(UPLOADS_QUEUE)}")
    
    for sid, title, desc in UPLOADS_QUEUE:
        if sid in uploaded_set:
            print(f"  [SKIP] '{sid}' already uploaded.")
            continue
            
        success = upload_single_short(sid, title, desc)
        if success:
            uploaded_set.add(sid)
            print("  Waiting 20 seconds before next upload...")
            time.sleep(20)
        else:
            print("  Retrying or waiting for compile in 30 seconds...")
            time.sleep(30)

if __name__ == "__main__":
    main()
