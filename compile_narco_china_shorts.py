# -*- coding: utf-8 -*-
"""
KINESIO & VAREGO COMPILER SUITE: CAMPAÑA "LA RUTA DE LA SEDA DEL CRIMEN" (CHINA & CÁRTELES MEXICANOS)
BASADO EN VISUALPOLITIK (https://www.youtube.com/watch?v=_W6l7b7qKkE)
ESTÁNDAR: KINESIO V5.5.0 / VAREGO FRAMEWORK
ENTREGABLE: 13 VERTICAL SHORTS (23s A 45s CADA UNO) CON 2 DÚOS DE PARTE 1 Y PARTE 2
"""

import os
import sys
import re
import json

SHORTS_DATA = [
    {
        "id": 1,
        "type": "Dúo 1 - Parte 1",
        "badge": "[DÚO 1: PARTE 1/2]",
        "title": "El Secreto de las Transacciones Espejo",
        "music": "Cipher2.mp3",
        "script": "¿Cómo hace un cártel mexicano para lavar miles de millones de dólares sin tocar un solo banco en Estados Unidos? La respuesta no está en Panamá ni en Suiza, sino en las llamadas transacciones espejo de la mafia china. Los cárteles entregan efectivo en efectivo en ciudades como Los Ángeles o Nueva York. A cambio, intermediarios chinos liberan al instante dinero equivalente en México a través de empresas de exportación, cobrando comisiones ridículas de apenas el tres por ciento. Un circuito subterráneo perfecto e indetectable por el que nadie paga impuestos porque la clave final siempre es..."
    },
    {
        "id": 2,
        "type": "Dúo 1 - Parte 2",
        "badge": "[DÚO 1: PARTE 2/2]",
        "title": "De Lavar Dinero Narco a Mar-a-Lago",
        "music": "Volatile Reaction.mp3",
        "script": "...la clave final siempre es mover el dinero lavado hacia los negocios más influyentes de Estados Unidos. El caso de Tao Liu, mentor del famoso lavador Xizhi Li, lo demuestra a la perfección. Liu blanqueó millones de dólares del cártel de Sinaloa invirtiéndolos en bienes raíces de lujo en Nueva York. Su influencia fue tan grande que en 2018 logró sentarse en la mesa del propio Donald Trump en su exclusivo club de golf de Nueva Jersey. Ni el Servicio Secreto pudo explicar cómo este magnate financiero estaba conectado directamente con el lavado narco que explica..."
    },
    {
        "id": 3,
        "type": "Dúo 2 - Parte 1",
        "badge": "[DÚO 2: PARTE 1/2]",
        "title": "El Negocio Secreto de los Precursores",
        "music": "Cipher2.mp3",
        "script": "El verdadero motor del fentanilo no nace en los laboratorios clandestinos de Sinaloa, sino en gigantescas fábricas químicas ubicadas en el corazón de China. Desde puertos como Wuhan o Shanghái, toneladas de precursores químicos no fiscalizados viajan camuflados como productos farmacéuticos o de limpieza hacia los puertos mexicanos de Manzanillo y Lázaro Cárdenas. Allí, los cárteles procesan la materia prima transformando unos pocos miles de dólares en un negocio multimillonario de potencia letal, donde el suministro químico chino es tan inagotable que demuestra por qué..."
    },
    {
        "id": 4,
        "type": "Dúo 2 - Parte 2",
        "badge": "[DÚO 2: PARTE 2/2]",
        "title": "La Guerra Asimétrica del Partido Comunista",
        "music": "Clash Defiant.mp3",
        "script": "...demuestra por qué Washington acusa a Pekín de ejecutar una auténtica guerra asimétrica. Mientras el fentanilo devasta las ciudades norteamericanas, el Partido Comunista Chino retira los incentivos fiscales a las químicas que exportan precursores ilegales solo bajo presión diplomática extrema. Para Pekín, este tráfico genera una triple ventaja: desestabiliza a su mayor rival geopolítico, genera dividendos millonarios y asegura que las divisas en dólares fluyan de vuelta a su economía. Es la venganza del opio al revés en pleno siglo veintiuno, una jugada perfecta de poder que revela..."
    },
    {
        "id": 5,
        "type": "Autónomo 05",
        "badge": "[AUTÓNOMO 05/13]",
        "title": "Por qué la DEA Falla Frente al Sistema Chino",
        "music": "Volatile Reaction.mp3",
        "script": "Durante décadas, la DEA persiguió maletas llenas de efectivo y transferencias hacia paraísos fiscales. Pero frente al sistema de lavado chino, los agentes federales están completamente a ciegas. La red china no utiliza bancos occidentales; utiliza una red informal de mensajería comercial conocida como Flying Money. El dinero contante se compensa internamente mediante la compra de contenedores de mercancías y electrónicos de consumo. Cuando los investigadores intentan rastrear una cuenta, la transacción ya se convirtió en un cargamento legal de ropa que demuestra..."
    },
    {
        "id": 6,
        "type": "Autónomo 06",
        "badge": "[AUTÓNOMO 06/13]",
        "title": "Las Granjas Ilegales de Marihuana en Maine",
        "music": "Sneaky Snitch.mp3",
        "script": "En los tranquilos bosques de Maine y Oklahoma, cientos de propiedades rurales han sido compradas en efectivo por redes asiáticas vinculadas a la mafia china. Bajo la fachada de cultivos legales de marihuana, estas organizaciones operan gigantescas granjas clandestinas con mano de obra sometida y electricidad robada. Los ingresos millonarios generados en el mercado negro norteamericano sirven para financiar directamente las operaciones de lavado de los cárteles de la droga mexicanos, un mecanismo tan refinado que explica..."
    },
    {
        "id": 7,
        "type": "Autónomo 07",
        "badge": "[AUTÓNOMO 07/13]",
        "title": "El Truco del 3%: Tarifas de Lavado Narco",
        "music": "Severe Tire Damage.mp3",
        "script": "Históricamente, los lavadores de dinero colombianos o italianos cobraban hasta un veinte por ciento de comisión por limpiar las ganancias del narcotráfico. Pero cuando la mafia china entró al mercado, ofreció tarifas insuperables de entre el dos y el cinco por ciento, garantizando además el pago inmediato en pesos mexicanos. Ningún otro grupo criminal en el planeta pudo competir contra semejante nivel de eficiencia financiera, logrando apoderarse en tiempo récord de todo el monopolio del blanqueo narco internacional, demostrando así..."
    },
    {
        "id": 8,
        "type": "Autónomo 08",
        "badge": "[AUTÓNOMO 08/13]",
        "title": "Cárteles sin Bancos Tradicionales",
        "music": "Cipher2.mp3",
        "script": "Las estrictas regulaciones contra el blanqueo introducidas tras el once de septiembre volvieron prohibitivo el uso de bancos tradicionales para el crimen organizado. Depositar millones en efectivo encendía alarmas automáticas en el Tesoro norteamericano. El sistema chino solucionó este problema eliminando los bancos de la ecuación: el efectivo físico entregado en Estados Unidos se utiliza localmente para pagar a importadores chinos que necesitan dólares para comprar mercancía, cerrando un círculo invisible que demuestra..."
    },
    {
        "id": 9,
        "type": "Autónomo 09",
        "badge": "[AUTÓNOMO 09/13]",
        "title": "Xizhi Li: El Limpiador Definitivo",
        "music": "Volatile Reaction.mp3",
        "script": "Xizhi Li no parecía un capo criminal; vestía trajes de diseñador y dirigía casinos y restaurantes en Centroamérica. Sin embargo, este empresario chino construyó la red de lavado más sofisticada de la historia para el Cártel de Sinaloa. Usando pasaportes falsos y empresas fantasma en más de veinte estados de Estados Unidos, Li movió más de trescientos millones de dólares antes de ser capturado por el FBI. Su arresto reveló que la mafia china se había convertido en la columna vertebral del narcotráfico global, demostrando que..."
    },
    {
        "id": 10,
        "type": "Autónomo 10",
        "badge": "[AUTÓNOMO 10/13]",
        "title": "Fuga de Capitales Inversa de la Élite China",
        "music": "Cipher2.mp3",
        "script": "¿Por qué los ciudadanos chinos adinerados están dispuestos a ayudar a los cárteles mexicanos? La respuesta es el férreo control de cambios impuesto por Pekín, que prohíbe sacar más de cincuenta mil dólares al año por persona. Para comprar propiedades de lujo en Miami o Vancouver, la élite china entrega yuanes en China a los lavadores y recibe a cambio los dólares en efectivo generados por la venta de droga en Estados Unidos. Una simbiosis perfecta entre fuga de capitales y narcotráfico que revela..."
    },
    {
        "id": 11,
        "type": "Autónomo 11",
        "badge": "[AUTÓNOMO 11/13]",
        "title": "Trade-Based Money Laundering (Fraude Comercial)",
        "music": "Clash Defiant.mp3",
        "script": "El lavado de dinero moderno ya no viaja en maletines, sino en contenedores marítimos llenos de teléfonos celulares, juguetes o telas. Mediante la sobrefacturación y subfacturación de mercancías entre China, Estados Unidos y México, las redes criminales transfieren valor de un país a otro de forma totalmente legal a ojos de las aduanas. Cuando la policía inspecciona un embarque, solo ve productos comerciales genuinos, tapando un flujo de miles de millones de dólares que demuestra..."
    },
    {
        "id": 12,
        "type": "Autónomo 12",
        "badge": "[AUTÓNOMO 12/13]",
        "title": "Fentanilo y Guerra Híbrida",
        "music": "Volatile Reaction.mp3",
        "script": "Analistas del Pentágono señalan que la crisis del fentanilo guarda paralelismos inquietantes con las Guerras del Opio del siglo diecinueve. En aquel entonces, potencias occidentales debilitaron a China inundándola de adicciones. Hoy, el suministro masivo de precursores desde laboratorios chinos sin una supervisión rigurosa de Pekín está desangrando la fuerza laboral y el tejido social de Estados Unidos. Sin disparar un solo misil, esta alianza narco-empresarial genera un impacto devastador en la seguridad nacional norteamericana, demostrando cómo..."
    },
    {
        "id": 13,
        "type": "Autónomo 13",
        "badge": "[AUTÓNOMO 13/13]",
        "title": "El Futuro Global del Narcotráfico",
        "music": "Future Gladiator.mp3",
        "script": "El narcotráfico ha dejado de ser un asunto regional entre México y Estados Unidos para convertirse en una corporación transnacional hiperconectada. La fusión entre la capacidad operativa de los cárteles mexicanos y la sofisticación financiera de las triadas chinas ha creado una estructura casi invulnerable a las fuerzas del orden tradicionales. Mientras las leyes de los países sigan fragmentadas, el dinero y los químicos seguirán fluyendo sin descanso a través de las fronteras globales, demostrando exactamente..."
    }
]

def verify_and_report():
    print("=" * 80)
    print("  KINESIO & VAREGO CAMPAIGN AUDIT: CHINA Y CÁRTELES MEXICANOS")
    print("  FUENTE: VisualPolitik (https://www.youtube.com/watch?v=_W6l7b7qKkE&t=691s)")
    print("=" * 80)
    
    total_shorts = len(SHORTS_DATA)
    print(f"\n[+] Total Shorts configurados: {total_shorts} (Requeridos: 13)")
    
    duos = [s for s in SHORTS_DATA if "Dúo" in s["type"]]
    print(f"[+] Dúos configurados: {len(duos)} vídeos ({len(duos)//2} Dúos completos: Dúo 1 P1/P2 y Dúo 2 P1/P2)")
    
    all_valid = True
    print("\n" + "-" * 80)
    print(f"{'ID':<4} | {'Tipo':<16} | {'Palabras':<8} | {'Est. Dur.':<10} | {'Rango Ok?':<10} | {'Título'}")
    print("-" * 80)
    
    for item in SHORTS_DATA:
        words = len(item["script"].split())
        est_sec = words / 2.5  # ~2.5 palabras por segundo para voz de alta tensión
        is_ok = 23 <= est_sec <= 45
        if not is_ok:
            all_valid = False
            
        status_str = "VALIDO (23s-45s)" if is_ok else "FUERA DE RANGO"
        print(f"#{item['id']:02d}  | {item['type']:<16} | {words:<8} | {est_sec:4.1f}s     | {status_str:<10} | {item['title']}")
        
    print("-" * 80)
    if all_valid and total_shorts == 13:
        print("\nSUCCESS: Todos los 13 Shorts cumplen estrictamente los parámetros de KINESIO & VAREGO.")
    else:
        print("\nWARNING: Se detectaron inconsistencias en la validación.")
        
if __name__ == "__main__":
    verify_and_report()
