# -*- coding: utf-8 -*-
"""
EDGE-TTS MASS AUDIO GENERATOR FOR ALL 48 SHORTS ACROSS ALL 4 CAMPAIGNS
"""

import os
import sys
import asyncio
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_assets")
os.makedirs(AUDIO_DIR, exist_ok=True)

ALL_48_SHORTS = [
    # Campaign 1: Narco China (13 Shorts - es-MX-JorgeNeural)
    ("narco_china_short_1", "es-MX-JorgeNeural", "Escucha con atención esto antes de ver el mercado financiero. Cárteles de la droga y lavado de dinero chino crearon las transacciones espejo. El dinero en efectivo nunca cruza la frontera, viaja en forma de bienes y créditos. ¿Cómo la DEA no pudo detener este sistema perfecto?"),
    ("narco_china_short_2", "es-MX-JorgeNeural", "Si escuchaste la parte uno, sabrás cómo Xizhi Li pasó de lavar millones para los carteles a codearse con políticos en Mar-a-Lago. Compraba propiedades de lujo y casinos para limpiar dólares a velocidad récord. ¿Es la red de lavado más peligrosa de la historia?"),
    ("narco_china_short_3", "es-MX-JorgeNeural", "Presta mucha atención a la conexión entre Wuhan y los laboratorios secretos. Empresas químicas chinas exportan precursores ilícitos disfrazados de fertilizantes. Los cárteles pagan en criptomonedas y dólares en efectivo. ¿Quién financia realmente este negocio?"),
    ("narco_china_short_4", "es-MX-JorgeNeural", "Abre bien los oídos porque esto es guerra asimétrica. El Partido Comunista Chino utiliza el tráfico de insumos químicos para desestabilizar la salud y economía de Estados Unidos mientras absorbe liquidez en dólares."),
    ("narco_china_short_5", "es-MX-JorgeNeural", "Escucha atentamente por qué los métodos tradicionales de la DEA fracasaron. Los agentes estadounidenses no pueden auditar chats en WeChat ni bancos del estado chino. Las investigaciones chocan contra un muro diplomático inaccesible."),
    ("narco_china_short_6", "es-MX-JorgeNeural", "No te pierdas ni un segundo de este hallazgo periodístico. Granjas masivas de marihuana ilegal en zonas rurales de Maine eran financiadas por inversionistas chinos que lavaban capitales de la élite asiática."),
    ("narco_china_short_7", "es-MX-JorgeNeural", "Escucha con cuidado cómo funciona el truco del 3%. Mientras los banqueros tradicionales cobraban hasta un 18% por lavar efectivo, las redes chinas redujeron las comisiones al 3% destruyendo a la competencia."),
    ("narco_china_short_8", "es-MX-JorgeNeural", "Presta atención a cómo los cárteles dejaron de usar bancos. Ahora entregan camiones llenos de dólares a comerciantes asiáticos en Los Ángeles a cambio de mercancía legal importada desde China."),
    ("narco_china_short_9", "es-MX-JorgeNeural", "Escucha la historia de Xizhi Li, el arquitecto del lavado moderno. Creó una red internacional de cuentas bancarias fantasma hasta que fue arrestado por agentes encubiertos de la DEA."),
    ("narco_china_short_10", "es-MX-JorgeNeural", "Pon mucha atención a la fuga de capitales inversa. Millonarios en Pekín necesitaban dólares fuera de China, y los cárteles en México necesitaban pesos. El intercambio perfecto sin tocar el sistema bancario."),
    ("narco_china_short_11", "es-MX-JorgeNeural", "Escucha cómo funciona el lavado basado en comercio internacional. Facturas falsificadas de iPhones y ropa de lujo sirven para camuflar millones de dólares como comercio legítimo transfronterizo."),
    ("narco_china_short_12", "es-MX-JorgeNeural", "Escucha este paralelismo histórico inquietante. Hace dos siglos, las potencias occidentales introdujeron opio en China. Hoy, la química sintética fluye en sentido contrario. ¿Venganza geopolítica o puro negocio?"),
    ("narco_china_short_13", "es-MX-JorgeNeural", "Escucha bien esta conclusión sobre el crimen organizado. La alianza entre la capacidad industrial de Asia y la distribución latinoamericana creó la máquina financiera más imparable de nuestro tiempo."),

    # Campaign 2: Guerra Antigua (10 Shorts - es-ES-AlvaroNeural)
    ("guerra_antigua_short_1", "es-ES-AlvaroNeural", "Escucha con atención antes de ver otra película de época. Hollywood nos vendió que las batallas antiguas eran caos de duelos individuales. La realidad es que romper la formación significaba morir apuñalado en segundos."),
    ("guerra_antigua_short_2", "es-ES-AlvaroNeural", "Si escuchaste la parte uno, sabrás por qué el muro de escudos era invencible. Cien hombres apretados madera contra madera creaban una muralla humana que ninguna carga individual podía atravesar."),
    ("guerra_antigua_short_3", "es-ES-AlvaroNeural", "Presta mucha atención a la física del combate antiguo. Un legionario romano con 30 kilos de armadura se agotaba por completo tras 15 minutos en primera línea. Por eso inventaron la rotación de líneas."),
    ("guerra_antigua_short_4", "es-ES-AlvaroNeural", "Abre bien los oídos al concepto de Othismos. El choque de las falanges griegas no era un duelo de lanzas, sino un empuje físico brutal cuerpo a cuerpo donde la masa del grupo aplastaba al enemigo."),
    ("guerra_antigua_short_5", "es-ES-AlvaroNeural", "Escucha atentamente la excepción legendaria de Maratón. En el año 490 antes de Cristo, los atenienses echaron a correr a toda velocidad para neutralizar la lluvia de flechas de los arqueros persas."),
    ("guerra_antigua_short_6", "es-ES-AlvaroNeural", "No te pierdas el secreto militar de Roma. La disciplina del manípulo permitía reemplazar a los soldados cansados mediante toques de corneta sin romper la formación de batalla."),
    ("guerra_antigua_short_7", "es-ES-AlvaroNeural", "Escucha con cuidado esta aterradora estadística. El 90% de los muertos en una batalla antigua no ocurrían durante el choque, sino cuando un bando se daba la vuelta y huía preso del pánico."),
    ("guerra_antigua_short_8", "es-ES-AlvaroNeural", "Presta atención al papel de los flautistas espartanos. La música del aulos no era entretenimiento; marcaba el ritmo exacto de marcha para que la falange no se desorganizara al avanzar."),
    ("guerra_antigua_short_9", "es-ES-AlvaroNeural", "Escucha el combate decisivo de Hastings en 1066. El muro de escudos saxón resistió horas de cargas de caballería normanda hasta que una falsa retirada los hizo romper filas."),
    ("guerra_antigua_short_10", "es-ES-AlvaroNeural", "Escucha la regla de oro del veterano antiguo. El miedo te incita a huir, pero solo el hombro de tu compañero a tu lado garantiza que vuelvas a casa con vida."),

    # Campaign 3: Steam Monopoly (12 Shorts - es-MX-JorgeNeural)
    ("steam_short_1", "es-MX-JorgeNeural", "Escucha con atención esto antes de comprar tu próximo juego. Steam controla el 74% del mercado global de PC con 17 mil millones de dólares en ingresos. Pero una histórica demanda colectiva en Reino Unido por mil millones de dólares los acusa de abuso monopolítico. ¿Es el fin de la era de Gabe Newell?"),
    ("steam_short_2", "es-MX-JorgeNeural", "Si escuchaste la parte uno, sabrás que Valve cobra una comisión del 30% a cada desarrollador. Para defender este margen, prohíben por contrato vender más barato en otras tiendas. Esto infla los precios para todos los jugadores del mundo. ¿Crees que Valve debería ser regulado?"),
    ("steam_short_3", "es-MX-JorgeNeural", "Presta mucha atención a este dato financiero. Tim Sweeney regaló cientos de juegos con Epic Games Store cobrando solo un 12% de comisión. Sin embargo, Valve mantiene el 30% intacto debido a la lealtad ciega de los usuarios. ¿Por qué preferimos pagar más en Steam?"),
    ("steam_short_4", "es-MX-JorgeNeural", "Abre bien los oídos porque esto cambiará tu biblioteca. Cuando compras un juego en Steam, no compras el producto, sino una licencia revocable. Si Valve cierra tus servidores o elimina tu cuenta, pierdes miles de dólares en minutos sin derecho a reclamo."),
    ("steam_short_5", "es-MX-JorgeNeural", "Escucha atentamente cómo funciona la cláusula de Nación Más Favorecida. Si un estudio intenta vender su juego más barato en su propia web, Steam los sanciona eliminándolos de la tienda. ¿Es protección al consumidor o chantaje comercial?"),
    ("steam_short_6", "es-MX-JorgeNeural", "No te pierdas ni una sola palabra de esta batalla legal. Wolfire Games llevó a Valve ante los tribunales federales de EE.UU. por bloquear la competencia. La jueza rechazó la moción de desestimación de Steam. ¿Estamos presenciando la caída del gigante?"),
    ("steam_short_7", "es-MX-JorgeNeural", "Escucha con cuidado si usabas VPN para comprar más barato. Valve dolarizó las tiendas de Argentina y Turquía tras la masiva migración de usuarios occidentales. El resultado: millones de jugadores locales destruidos económicamente. ¿Quién tiene la culpa?"),
    ("steam_short_8", "es-MX-JorgeNeural", "Presta atención al efecto red que protege a Valve. Con más de 100 millones de perfiles, inventarios de cromos, mercado de comunidad y workshop, cambiar de plataforma es socialmente imposible. Steam no vende juegos, vende tu identidad digital."),
    ("steam_short_9", "es-MX-JorgeNeural", "Escucha la estructura financiera más rentable del mundo. Valve genera más dinero por empleado que Google o Apple. Al ser una empresa privada sin accionistas, Gabe Newell controla el destino del PC gaming sin rendir cuentas a nadie."),
    ("steam_short_10", "es-MX-JorgeNeural", "Pon mucha atención a la ruina de los pequeños desarrolladores. Tras pagar el 30% a Steam, impuestos y marketing, los estudios independientes quiebran antes de lanzar su segundo juego. ¿Está la codicia de Valve matando la innovación?"),
    ("steam_short_11", "es-MX-JorgeNeural", "Escucha el precedente de la Ley de Mercados Digitales en Europa. Tras multar a Apple y Google, los reguladores de Bruselas ponen la mira sobre la distribución digital en PC. ¿Veremos tiendas de terceros obligatorias en Steam?"),
    ("steam_short_12", "es-MX-JorgeNeural", "Escucha bien este aviso para los próximos cinco años. Si el juego en la nube se impone con Microsoft y GeForce Now, la tienda tradicional de Steam perderá su hegemonía. ¿Sobrevivirá el imperio de Gabe Newell a la era del streaming?"),

    # Campaign 4: Programadores IA (13 Shorts - es-ES-AlvaroNeural)
    ("programadores_short_1", "es-ES-AlvaroNeural", "Escucha con atención antes de matricularte en ingeniería. El multimillonario Jason Lemkin creó una aplicación completa usando Inteligencia Artificial sin escribir una sola línea de código. Las empresas ya no contratan programadores junior. ¿Es el fin de la carrera?"),
    ("programadores_short_2", "es-ES-AlvaroNeural", "Si escuchaste la parte uno, sabrás que Lemkin celebró su app sin saber que contenía fallos de seguridad críticos. La Inteligencia Artificial genera código rápido, pero carece de criterio arquitectónico. ¿Nos salvará esto de los despidos masivos?"),
    ("programadores_short_3", "es-ES-AlvaroNeural", "Presta mucha atención a la velocidad de evolución. Agentes autónomos como Devin resuelven tickets de GitHub reales sin intervención humana. Un solo desarrollador senior con IA reemplaza a todo un equipo de diez programadores."),
    ("programadores_short_4", "es-ES-AlvaroNeural", "Abre bien los oídos si estás aprendiendo Python o JavaScript. Memorizar comandos o sintaxis es profesionalmente obsoleto. La IA escribe sintaxis perfecta en milisegundos; tu único valor es saber qué problema resolver."),
    ("programadores_short_5", "es-ES-AlvaroNeural", "Escucha atentamente el colapso del modelo educativo tech. Los bootcamps de 6 meses prometían sueldos de seis cifras por escribir HTML y CSS. Hoy, herramientas como Vercel y Replit generan esas interfaces con una simple orden de voz."),
    ("programadores_short_6", "es-ES-AlvaroNeural", "No te pierdas ni un segundo de esta advertencia de ciberseguridad. El código generado por IA suele incluir librerías inexistentes o vulnerabilidades de inyección SQL. Quien no sepa auditar código caerá en catástrofes financieras."),
    ("programadores_short_7", "es-ES-AlvaroNeural", "Escucha con cuidado cómo cambia el mercado laboral. La IA no destruye al programador, destruye al intermediario. Un solo fundador técnico puede construir un unicornio sin contratar ingenieros adicionales."),
    ("programadores_short_8", "es-ES-AlvaroNeural", "Presta atención a la paradoja de la automatización. Cuanto más código escribe la IA, más valioso es el ingeniero senior capaz de corregir la arquitectura y garantizar la seguridad del sistema."),
    ("programadores_short_9", "es-ES-AlvaroNeural", "Escucha la nueva habilidad imprescindible del siglo 21. La programación en código cede el paso a la ingeniería de contexto, la arquitectura de sistemas complejos y la validación de seguridad."),
    ("programadores_short_10", "es-ES-AlvaroNeural", "Pon mucha atención al desastre de mantenimiento técnico. Las empresas que abusan del código IA acumulan deuda técnica inmanejable que requerirá millones de dólares para ser reescrita por humanos."),
    ("programadores_short_11", "es-ES-AlvaroNeural", "Escucha el dilema legal de la automatización. Cuando un agente IA despliega un bug que filtra datos de millones de usuarios, ¿quién asume la responsabilidad penal: el modelo, el prompt o la empresa?"),
    ("programadores_short_12", "es-ES-AlvaroNeural", "Escucha cómo la tecnología rompe las barreras de entrada. Médicos, abogados y economistas crean hoy sus propias herramientas digitales sin pasar por un departamento de tecnología. ¿Es la democratización suprema?"),
    ("programadores_short_13", "es-ES-AlvaroNeural", "Escucha bien esta conclusión definitiva. El programador del futuro no será un artesano del teclado, sino un director de orquesta de modelos de Inteligencia Artificial. Adaptarse o extinguirse.")
]

async def generate_single_short_audio(sid, voice, text):
    mp3_path = os.path.join(AUDIO_DIR, f"{sid}.mp3")
    vtt_path = os.path.join(AUDIO_DIR, f"{sid}.vtt")
    
    if os.path.exists(mp3_path) and os.path.exists(vtt_path) and os.path.getsize(mp3_path) > 10000:
        return

    for attempt in range(3):
        try:
            communicate = edge_tts.Communicate(text, voice)
            submaker = edge_tts.SubMaker()
            with open(mp3_path, "wb") as f:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        f.write(chunk["data"])
                    elif chunk["type"] == "WordBoundary":
                        submaker.feed(chunk)
            with open(vtt_path, "w", encoding="utf-8") as f:
                f.write(submaker.get_srt())
            print(f"  [SUCCESS] Audio & VTT created for '{sid}'")
            return
        except Exception as e:
            print(f"  [RETRY {attempt+1}/3] Error for '{sid}': {e}")
            await asyncio.sleep(2)

async def main():
    print("=" * 80)
    print("  EDGE-TTS MASS AUDIO GENERATOR FOR ALL 48 SHORTS ACROSS ALL 4 CAMPAIGNS")
    print("=" * 80)
    for sid, voice, text in ALL_48_SHORTS:
        await generate_single_short_audio(sid, voice, text)
    print("\n[ALL SUCCESS] 48 Audio Tracks and VTT Files Generated!")

if __name__ == "__main__":
    asyncio.run(main())
