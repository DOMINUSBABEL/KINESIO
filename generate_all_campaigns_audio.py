# -*- coding: utf-8 -*-
"""
KINESIO TTS AUDIO GENERATOR: CAMPAÑAS NARCO CHINA & GUERRA ANTIGUA
Generates .mp3 audio tracks and .vtt subtitles for 23 Shorts using edge-tts.
"""

import os
import sys
import asyncio
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_assets")

if not os.path.exists(AUDIO_DIR):
    os.makedirs(AUDIO_DIR, exist_ok=True)

# 13 Shorts Narco China
NARCO_CHINA_SHORTS = [
    {
        "id": "narco_china_short_1",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "¿Cómo hace un cártel mexicano para lavar miles de millones de dólares sin tocar un solo banco en Estados Unidos? La respuesta no está en Panamá ni en Suiza, sino en las llamadas transacciones espejo de la mafia china. Los cárteles entregan efectivo en ciudades como Los Ángeles o Nueva York. A cambio, intermediarios chinos liberan al instante dinero equivalente en México a través de empresas de exportación, cobrando comisiones ridículas de apenas el tres por ciento. Un circuito subterráneo perfecto e indetectable por el que nadie paga impuestos porque la clave final siempre es..."
    },
    {
        "id": "narco_china_short_2",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "...la clave final siempre es mover el dinero lavado hacia los negocios más influyentes de Estados Unidos. El caso de Tao Liu, mentor del famoso lavador Xizhi Li, lo demuestra a la perfección. Liu blanqueó millones de dólares del cártel de Sinaloa invirtiéndolos en bienes raíces de lujo en Nueva York. Su influencia fue tan grande que en 2018 logró sentarse en la mesa del propio Donald Trump en su exclusivo club de golf de Nueva Jersey. Ni el Servicio Secreto pudo explicar cómo este magnate financiero estaba conectado directamente con el lavado narco que explica..."
    },
    {
        "id": "narco_china_short_3",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "El verdadero motor del fentanilo no nace en los laboratorios clandestinos de Sinaloa, sino en gigantescas fábricas químicas ubicadas en el corazón de China. Desde puertos como Wuhan o Shanghái, toneladas de precursores químicos no fiscalizados viajan camuflados como productos farmacéuticos o de limpieza hacia los puertos mexicanos de Manzanillo y Lázaro Cárdenas. Allí, los cárteles procesan la materia prima transformando unos pocos miles de dólares en un negocio multimillonario de potencia letal, donde el suministro químico chino es tan inagotable que demuestra por qué..."
    },
    {
        "id": "narco_china_short_4",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "...demuestra por qué Washington acusa a Pekín de ejecutar una auténtica guerra asimétrica. Mientras el fentanilo devasta las ciudades norteamericanas, el Partido Comunista Chino retira los incentivos fiscales a las químicas que exportan precursores ilegales solo bajo presión diplomática extrema. Para Pekín, este tráfico genera una triple ventaja: desestabiliza a su mayor rival geopolítico, genera dividendos millonarios y asegura que las divisas en dólares fluyan de vuelta a su economía. Es la venganza del opio al revés en pleno siglo veintiuno, una jugada perfecta de poder que revela..."
    },
    {
        "id": "narco_china_short_5",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "Durante décadas, la DEA persiguió maletas llenas de efectivo y transferencias hacia paraísos fiscales. Pero frente al sistema de lavado chino, los agentes federales están completamente a ciegas. La red china no utiliza bancos occidentales; utiliza una red informal de mensajería comercial conocida como Flying Money. El dinero contante se compensa internamente mediante la compra de contenedores de mercancías y electrónicos de consumo. Cuando los investigadores intentan rastrear una cuenta, la transacción ya se convirtió en un cargamento legal de ropa que demuestra..."
    },
    {
        "id": "narco_china_short_6",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "En los tranquilos bosques de Maine y Oklahoma, cientos de propiedades rurales han sido compradas en efectivo por redes asiáticas vinculadas a la mafia china. Bajo la fachada de cultivos legales de marihuana, estas organizaciones operan gigantescas granjas clandestinas con mano de obra sometida y electricidad robada. Los ingresos millonarios generados en el mercado negro norteamericano sirven para financiar directamente las operaciones de lavado de los cárteles de la droga mexicanos, un mecanismo tan refinado que explica..."
    },
    {
        "id": "narco_china_short_7",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "Históricamente, los lavadores de dinero colombianos o italianos cobraban hasta un veinte por ciento de comisión por limpiar las ganancias del narcotráfico. Pero cuando la mafia china entró al mercado, ofreció tarifas insuperables de entre el dos y el cinco por ciento, garantizando además el pago inmediato en pesos mexicanos. Ningún otro grupo criminal en el planeta pudo competir contra semejante nivel de eficiencia financiera, logrando apoderarse en tiempo récord de todo el monopolio del blanqueo narco internacional, demostrando así..."
    },
    {
        "id": "narco_china_short_8",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "Las estrictas regulaciones contra el blanqueo introducidas tras el once de septiembre volvieron prohibitivo el uso de bancos tradicionales para el crimen organizado. Depositar millones en efectivo encendía alarmas automáticas en el Tesoro norteamericano. El sistema chino solucionó este problema eliminando los bancos de la ecuación: el efectivo físico entregado en Estados Unidos se utiliza localmente para pagar a importadores chinos que necesitan dólares para comprar mercancía, cerrando un círculo invisible que demuestra..."
    },
    {
        "id": "narco_china_short_9",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "Xizhi Li no parecía un capo criminal; vestía trajes de diseñador y dirigía casinos y restaurantes en Centroamérica. Sin embargo, este empresario chino construyó la red de lavado más sofisticada de la historia para el Cártel de Sinaloa. Usando pasaportes falsos y empresas fantasma en más de veinte estados de Estados Unidos, Li movió más de trescientos millones de dólares antes de ser capturado por el FBI. Su arresto reveló que la mafia china se había convertido en la columna vertebral del narcotráfico global, demostrando que..."
    },
    {
        "id": "narco_china_short_10",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "¿Por qué los ciudadanos chinos adinerados están dispuestos a ayudar a los cárteles mexicanos? La respuesta es el férreo control de cambios impuesto por Pekín, que prohíbe sacar más de cincuenta mil dólares al año por persona. Para comprar propiedades de lujo en Miami o Vancouver, la élite china entrega yuanes en China a los lavadores y recibe a cambio los dólares en efectivo generados por la venta de droga en Estados Unidos. Una simbiosis perfecta entre fuga de capitales y narcotráfico que revela..."
    },
    {
        "id": "narco_china_short_11",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "El lavado de dinero moderno ya no viaja en maletines, sino en contenedores marítimos llenos de teléfonos celulares, juguetes o telas. Mediante la sobrefacturación y subfacturación de mercancías entre China, Estados Unidos y México, las redes criminales transfieren valor de un país a otro de forma totalmente legal a ojos de las aduanas. Cuando la policía inspecciona un embarque, solo ve productos comerciales genuinos, tapando un flujo de miles de millones de dólares que demuestra..."
    },
    {
        "id": "narco_china_short_12",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "Analistas del Pentágono señalan que la crisis del fentanilo guarda paralelismos inquietantes con las Guerras del Opio del siglo diecinueve. En aquel entonces, potencias occidentales debilitaron a China inundándola de adicciones. Hoy, el suministro masivo de precursores desde laboratorios chinos sin una supervisión rigurosa de Pekín está desangrando la fuerza laboral y el tejido social de Estados Unidos. Sin disparar un solo misil, esta alianza narco-empresarial genera un impacto devastador en la seguridad nacional norteamericana, demostrando cómo..."
    },
    {
        "id": "narco_china_short_13",
        "voice": "es-MX-JorgeNeural",
        "rate": "+0%",
        "text": "El narcotráfico ha dejado de ser un asunto regional entre México y Estados Unidos para convertirse en una corporación transnacional hiperconectada. La fusión entre la capacidad operativa de los cárteles mexicanos y la sofisticación financiera de las triadas chinas ha creado una estructura casi invulnerable a las fuerzas del orden tradicionales. Mientras las leyes de los países sigan fragmentadas, el dinero y los químicos seguirán fluyendo sin descanso a través de las fronteras globales, demostrando exactamente..."
    }
]

# 10 Shorts Guerra Antigua
GUERRA_ANTIGUA_SHORTS = [
    {
        "id": "guerra_antigua_short_1",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "¿Por qué las películas de Hollywood nos han mentido durante décadas sobre las batallas antiguas? En el cine ves a miles de soldados rompiendo filas y esprintando a toda velocidad antes de chocar. En la vida real, si una unidad de infantería hubiera hecho eso, habrían sido masacrados antes de asestar el primer golpe. Romper la carrera destruía la cohesión de la línea, dejando a cada guerrero aislado contra un muro compacto de lanzas porque en el combate antiguo..."
    },
    {
        "id": "guerra_antigua_short_2",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "Un muro de escudos o una falange griega no era un grupo de soldados luchando juntos; era una sola máquina biomecánica de varias toneladas. Cada soldado protegía el costado izquierdo de su compañero con su propio escudo. Si un solo hombre corría más rápido para atacar por su cuenta, abría una brecha mortal en la formación. Un muro apretado avanzaba a paso firme y cadencioso, porque aplastar al enemigo requería mantener la línea unida, demostrando que..."
    },
    {
        "id": "guerra_antigua_short_3",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "Intenta correr doscientos metros llevando encima treinta kilos de armadura de hierro, casco, lanza y un escudo gigante de madera. Si esprintabas hacia la línea enemiga, llegabas al choque completamente agotado, sin aire en los pulmones y con las piernas temblando. Tus enemigos, que te esperaban descansados y bien plantados, solo tenían que empujarte para hacerte caer. La gestión del esfuerzo físico era la regla número uno de supervivencia porque en la guerra..."
    },
    {
        "id": "guerra_antigua_short_4",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "El combate de infantería antigua no consistía en duelos acrobáticos con espadas. Era un sangriento juego de empujones conocido como Othismos. Filas de hombres apretando sus hombros contra la espalda de sus compañeros para aplastar literalmente a la masa enemiga. Correr hacia ese muro era como estrellarse de cabeza contra una pared de ladrillo. El objetivo de la marcha ordenada no era golpear más fuerte, sino mantener la estabilidad física del bloque para evitar que..."
    },
    {
        "id": "guerra_antigua_short_5",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "¿Existió alguna excepción donde una infantería corrió al combate? Sí, en la famosa Batalla de Maratón. Los atenienses avanzaron a paso firme hasta estar a cien metros del ejército persa. En ese punto exacto, apretaron el paso y esprintaron la última distancia. ¿Por qué lo hicieron? Para cruzar en segundos la zona de muerte de los arqueros persas antes de que las flechas los despedazaran. Pero corrieron solo los últimos metros manteniendo la línea, demostrando que..."
    },
    {
        "id": "guerra_antigua_short_6",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "Las legiones romanas conquistaron el mundo gracias a una disciplina marcha llamada Gradus Militaris. Avanzaban a exactamente cuatro kilómetros por hora en perfecta formación. Al llegar a quince metros del enemigo, se detenían un segundo, lanzaban sus pesados jabalines Pilum para inutilizar los escudos contrarios, y avanzaban calmados a paso corto con sus espadas Gladius. Ningún legionario corría jamás por su cuenta porque romper filas significaba..."
    },
    {
        "id": "guerra_antigua_short_7",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "¿Sabías que el ochenta por ciento de las bajas en las batallas antiguas no ocurrían durante el choque frontal? Ocurrían cuando uno de los dos bandos entraba en pánico y salía corriendo. En el choque de escudos morían muy pocos hombres. Pero cuando la línea se rompe y los soldados dan la espalda para esprintar, se convierten en presas fáciles para la caballería y los perseguidores. Quien corría hacia atrás moría atravesado por la espalda, demostrando que..."
    },
    {
        "id": "guerra_antigua_short_8",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "Los espartanos avanzaban hacia la batalla acompañados por flautistas que tocaban el Aulos. Esto no era por entretenimiento militar; era una herramienta táctica vital para mantener la cadencia del paso. El ritmo de la música impedía que los soldados se apresuraran o se retrasaran, asegurando que la falange se mantuviera como una muralla de bronce ininterrumpida. Si alguien corría, tropezaba y pisoteaba a sus propios compañeros porque..."
    },
    {
        "id": "guerra_antigua_short_9",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "En la Batalla de Hastings en 1066, el muro de escudos anglosajón aguantó durante horas en lo alto de la colina los embates de la caballería normanda de Guillermo el Conquistador. La tragedia ocurrió cuando los normandos simularon una retirada. Engañados por la falsa huida, parte de los anglosajones rompió el muro y corrió colina abajo para perseguirlos. Al abandonar su formación, fueron rodeados y aniquilados al instante, una lección histórica que demuestra..."
    },
    {
        "id": "guerra_antigua_short_10",
        "voice": "es-ES-AlvaroNeural",
        "rate": "+0%",
        "text": "Caminar con calma hacia el enemigo no era cobardía ni lentitud; era la tecnología militar más avanzada de la antigüedad. Conservar la energía, rotar a los soldados fatigados de la primera línea hacia la retaguardia y mantener el hombro pegado al compañero era lo único que separaba la victoria de una ejecución masiva. La próxima vez que veas una película con cargas desordenadas, recuerda que los verdaderos veteranos nunca corrían porque sabían que..."
    }
]

ALL_SHORTS = NARCO_CHINA_SHORTS + GUERRA_ANTIGUA_SHORTS

async def generate_single_tts(item):
    item_id = item["id"]
    mp3_path = os.path.join(AUDIO_DIR, f"{item_id}.mp3")
    vtt_path = os.path.join(AUDIO_DIR, f"{item_id}.vtt")
    
    cmd = [
        "edge-tts",
        "--voice", item["voice"],
        "--rate", item["rate"],
        "--text", item["text"],
        "--write-media", mp3_path,
        "--write-subtitles", vtt_path
    ]
    
    try:
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = await proc.communicate()
        if proc.returncode == 0 and os.path.exists(mp3_path):
            print(f"  [SUCCESS] Generated audio & VTT for '{item_id}'")
            return True
        else:
            print(f"  [FAILED] '{item_id}': {stderr.decode('utf-8').strip()}")
            return False
    except Exception as e:
        print(f"  [ERROR] '{item_id}': {e}")
        return False

async def main():
    print("=" * 80)
    print("  KINESIO TTS GENERATOR: 23 SHORTS (NARCO CHINA & GUERRA ANTIGUA)")
    print("=" * 80)
    
    tasks = [generate_single_tts(item) for item in ALL_SHORTS]
    results = await asyncio.gather(*tasks)
    
    successes = sum(1 for r in results if r)
    print("\n" + "=" * 80)
    print(f"  RESULT: {successes} / {len(ALL_SHORTS)} audio tracks generated successfully.")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(main())
