# -*- coding: utf-8 -*-
"""
EDGE-TTS AUDIO GENERATOR FOR CAMPAIGN 5: CIBERSEGURIDAD & IA (11 SHORTS)
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

CIBERSEGURIDAD_SHORTS = [
    ("ciberseguridad_short_1", "es-ES-AlvaroNeural", "Escucha con atención esto antes de volver a usar una Inteligencia Artificial. En junio de 2026, el Departamento de Comercio de Estados Unidos envió una orden de emergencia a Anthropic para apagar de inmediato Claude Mythos, su modelo de IA más potente hasta la fecha. El gobierno citó riesgos severos para la seguridad nacional, argumentando que Mythos era tan avanzado encontrando vulnerabilidades que podía convertirse en el hacker autónomo perfecto. Ante la orden de restringirlo solo para uso militar estadounidense, Anthropic decidió apagar el modelo para todo el planeta. ¿Estamos presenciando el momento en que una IA fue declarada la primera arma digital prohibida de la historia?"),
    ("ciberseguridad_short_2", "es-ES-AlvaroNeural", "Si escuchaste la parte uno, sabrás por qué la Casa Blanca entró en pánico. Tradicionalmente, descubrir un fallo de seguridad de día cero requería semanas de trabajo de un equipo de hackers de élite. Hoy, agentes autónomos de IA escanean millones de líneas de código en segundos, escribiendo exploits sin intervención humana. Esto reduce la barrera de entrada a niveles aterradores: pequeños grupos criminales ahora poseen la capacidad ofensiva de ejércitos cibernéticos enteros. La ciberseguridad dejó de ser un departamento de informática para convertirse en una cuestión de supervivencia nacional. ¿Quién nos defenderá de la IA?"),
    ("ciberseguridad_short_3", "es-ES-AlvaroNeural", "Presta mucha atención a la única industria que no teme a las crisis económicas. En el mundo de los negocios, la ciberseguridad no es una inversión opcional; es literalmente el impuesto digital obligatorio que toda empresa debe pagar para existir. Una corporación puede recortar presupuesto en publicidad, contratación o suministros de oficina, pero jamás puede recortar en ciberseguridad. Sufrir un ataque de ransomware significa la paralización total de operaciones, demandas millonarias y la bancarrota inmediata. Por eso, pase lo que pase en los mercados, el gasto en ciberseguridad no para de crecer."),
    ("ciberseguridad_short_4", "es-ES-AlvaroNeural", "Si escuchaste la parte uno, entenderás por qué este sector es inelástico. A diferencia del software tradicional, donde las empresas cancelan suscripciones durante una recesión, las licencias de ciberseguridad son intocables. Los ciberdelincuentes no descansan cuando la economía cae; de hecho, los ataques se triplican en épocas de inestabilidad. Mientras los presupuestos de tecnología convencional sufren recortes masivos, el presupuesto de protección digital se incrementa año tras año por mandato de las aseguradoras y gobiernos. ¿Es este el negocio más seguro de la década?"),
    ("ciberseguridad_short_5", "es-ES-AlvaroNeural", "Abre bien los oídos porque la guerra moderna ya no se combate en campos de batalla. Ciberataques patrocinados por estados-nación como Rusia, China, Irán y Corea del Norte no buscan robar tarjetas de crédito, sino apagar redes eléctricas, bloquear plantas de tratamiento de agua y paralizar hospitales enteros. Un solo virus introducido en un sistema industrial puede dejar a millones de ciudadanos sin luz ni agua en cuestión de minutos. La ciberseguridad ha pasado de proteger archivos corporativos a ser la última línea de defensa de la infraestructura nacional. ¿Está preparado el mundo occidental?"),
    ("ciberseguridad_short_6", "es-ES-AlvaroNeural", "No te pierdas este mapa definitivo del dinero en tecnología. Muchos inversores cometen el error de meter a todas las empresas de ciberseguridad en el mismo saco, pero el mercado funciona en tres bloques según el Modelo OSI. En la capa baja está el hardware de cables y routers como Cisco. En la capa media están los firewalls de red y conectividad como Palo Alto Networks y Fortinet. Y en la capa alta están la identidad y los dispositivos finales como CrowdStrike. Entender en qué capa opera cada gigante es la clave para no perder dinero en bolsa."),
    ("ciberseguridad_short_7", "es-ES-AlvaroNeural", "Escucha con cuidado cómo funciona el cimiento de la red global. En la parte más profunda del Modelo OSI están los cables físicos, la fibra óptica y los conmutadores por donde viajan los pulsos de luz. Empresas como Cisco y Arista Networks protegen los componentes físicos de los centros de datos y redes corporativas. Aunque es un mercado de hardware más lento y competitivo, sin estos guardianes físicos ninguna plataforma cloud o Inteligencia Artificial podría transmitir un solo dato de forma segura."),
    ("ciberseguridad_short_8", "es-ES-AlvaroNeural", "Presta atención a la capa donde se detienen las invasiones de datos. En el nivel medio del Modelo OSI, empresas como Palo Alto Networks, Fortinet y Cloudflare actúan como los aduaneros digitales del tráfico de internet. Analizan trillones de paquetes de información en tiempo real, bloqueando ataques de denegación de servicio e infiltraciones de red antes de que toquen los servidores de las empresas. Es una muralla de fuego gigante que procesa el tráfico global con algoritmos de inspección profunda."),
    ("ciberseguridad_short_9", "es-ES-AlvaroNeural", "Pon mucha atención a la cúspide de la pirámide de la ciberseguridad. En la capa alta del Modelo OSI se protegen las aplicaciones, los teléfonos, las ordenadores portátiles y las identidades de los empleados. Gigantes como CrowdStrike, Microsoft y Okta monitorean cada dispositivo conectado a la red corporativa. Si un portátil en cualquier lugar del mundo muestra un comportamiento anómalo, sus agentes de IA lo aíslan al instante antes de que el malware infecte a toda la compañía."),
    ("ciberseguridad_short_10", "es-ES-AlvaroNeural", "Escucha esta aterradora evolución de la ingeniería social. Los ciberdelincuentes ya no envían correos electrónicos con faltas de ortografía. Ahora utilizan IA para clonar la voz y el rostro de directores ejecutivos en videollamadas en tiempo real. En Hong Kong, un empleado transfirió 25 millones de dólares tras una reunión virtual donde todos sus superiores eran réplicas generadas por IA. La ciberseguridad ya no solo protege servidores; ahora debe verificar si el humano al otro lado de la pantalla es real."),
    ("ciberseguridad_short_11", "es-ES-AlvaroNeural", "Escucha bien esta conclusión sobre el futuro de la tecnología. La Inteligencia Artificial se ha convertido en la espada más afilada para los atacantes y en el único escudo capaz de reaccionar a la velocidad de la luz para los defensores. En una era donde los ciberataques ocurren en microsegundos, la mente humana es demasiado lenta para responder. La carrera armamentista del siglo 21 no se librará con misiles, sino con algoritmos de IA enfrentándose en las sombras de la red mundial. Adaptarse o ser destruido.")
]

async def generate_single_short_audio(sid, voice, text):
    mp3_path = os.path.join(AUDIO_DIR, f"{sid}.mp3")
    vtt_path = os.path.join(AUDIO_DIR, f"{sid}.vtt")
    
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
    print(f"  [SUCCESS] Audio & VTT created for '{sid}' (Size: {os.path.getsize(mp3_path)} bytes)")

async def main():
    print("=" * 80)
    print("  EDGE-TTS AUDIO GENERATOR FOR CAMPAIGN 5: CIBERSEGURIDAD & IA")
    print("=" * 80)
    for sid, voice, text in CIBERSEGURIDAD_SHORTS:
        await generate_single_short_audio(sid, voice, text)
    print("\n[ALL SUCCESS] 11 Audio Tracks and VTT Files Generated for Campaign 5!")

if __name__ == "__main__":
    asyncio.run(main())
