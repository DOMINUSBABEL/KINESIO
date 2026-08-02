# -*- coding: utf-8 -*-
"""
EDGE-TTS AUDIO GENERATOR FOR CAMPAIGN 6 (13 SHORTS) AND CAMPAIGN 7 (8 SHORTS)
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

# Campaign 6: Propiedad Digital (13 Shorts)
CAMPAIGN_6_SHORTS = [
    ("propiedad_short_1", "es-ES-AlvaroNeural", "Escucha con mucha atención esto antes de volver a encender tu consola. Cuando compraste tu PlayStation 5 o Nintendo Switch con tu dinero, asumiste que el hardware era 100% tuyo. Sin embargo, al aceptar esos términos y condiciones larguísimos que nadie lee, firmaste un acuerdo donde las compañías especifican que solo te otorgan una licencia revocable de uso de su software interno. Si intentas modificar el sistema operativo o hacer jailbreak para instalar tus propios programas, Sony o Nintendo pueden banear tu consola a distancia de forma permanente, convirtiendo un dispositivo de 500 euros en un pisa papales inservible. ¿Es justo que no seas dueño de lo que pagaste?"),
    ("propiedad_short_2", "es-ES-AlvaroNeural", "Si escuchaste la parte uno, entenderás el alcance de este control corporativo. Imagine comprar un coche y que el fabricante te prohíba cambiar las llantas o reparar el motor por tu cuenta. Eso es exactamente lo que ocurre en el mundo gaming. Al bloquear el hardware mediante firmware propietario, los fabricantes obligan a los usuarios a depender exclusivamente de sus tiendas digitales y servicios técnicos oficiales. Si vulneras su contrato digital, pierdes el acceso a tu cuenta, tus juegos comprados y las funciones en línea de inmediato. ¿Hasta dónde llega el derecho de propiedad en la era digital?"),
    ("propiedad_short_3", "es-ES-AlvaroNeural", "Presta atención a este precedente histórico sobre las compras digitales. En 2024, Ubisoft cerró definitivamente los servidores del juego The Crew. Pero no se limitaron a apagar el modo multijugador; eliminaron el juego por completo de las bibliotecas de los usuarios y revocaron las licencias digitales. Miles de jugadores que habían pagado precio completo vieron cómo el título desaparecía de sus cuentas sin posibilidad de descargarlo o jugarlo en modo offline. Fue la prueba definitiva de que cuando compras un juego digital, en realidad solo estás alquilando un acceso temporal."),
    ("propiedad_short_4", "es-ES-AlvaroNeural", "Si escuchaste la parte uno sobre el caso Ubisoft, debes conocer el truco legal de las plataformas. El botón que dice Comprar en tiendas como PlayStation Store, Xbox Marketplace o Steam es jurídicamente engañoso. En los términos de servicio se aclara que no adquieres la propiedad del producto informático, sino una licencia personal e intransferible que puede extinguirse en cualquier momento si la editora pierde los derechos de distribución o decide cerrar los servidores. Si una empresa quiebra o retira una licencia, tu biblioteca completa de miles de euros puede evaporarse de la noche a la mañana."),
    ("propiedad_short_5", "es-ES-AlvaroNeural", "Pon mucha atención porque esto no solo afecta a los videojuegos, sino también al cine. Sony anunció la eliminación de cientos de programas y películas de Discovery de las bibliotecas de usuarios de PlayStation que las habían comprado legítimamente. Debido al vencimiento de licencias de contenido con la productora, los clientes perdieron el acceso a títulos por los que habían pagado años atrás. Este escándalo demostró que el formato digital no garantiza la permanencia de ningún bien audiovisual y que los servidores centralizados controlan qué puedes ver y cuándo."),
    ("propiedad_short_6", "es-ES-AlvaroNeural", "Escucha esta jugada maestra de la industria del videojuego. El impulso hacia consolas digitales sin lector de discos no se trata de comodidad para el jugador, sino de eliminar el mercado de segunda mano. Sin discos físicos, pierdes el derecho de prestar, vender, intercambiar o regalar tus juegos a tus amigos. Estás atrapado al 100% en la tienda oficial del fabricante, donde ellos fijan los precios sin competencia y controlan el catálogo a su antojo. El formato digital elimina la propiedad privada para imponer un monopolio absoluto de distribución."),
    ("propiedad_short_7", "es-ES-AlvaroNeural", "Presta atención a cómo el modelo de suscripción cambia tu psicología de consumo. Servicios como Xbox Game Pass o PlayStation Plus te ofrecen acceso a cientos de títulos por una tarifa mensual. Sin embargo, este modelo destruye el concepto de colección. Los juegos entran y salen del catálogo constantemente sin tu consentimiento; si estás a mitad de una partida y el título abandona el servicio, debes comprarlo a precio completo o abandonar tu progreso. Pagas indefinidamente por un buffet donde la comida puede ser retirada en cualquier instante."),
    ("propiedad_short_8", "es-ES-AlvaroNeural", "Abre bien los ojos porque la pérdida de propiedad ya llegó al mundo del automóvil. Marcas como BMW probaron cobrar una suscripción mensual de 18 dólares para activar los asientos calefactables que el coche ya traía instalados de fábrica. El hardware está físicamente en el vehículo que pagaste, pero el software bloquea su funcionamiento hasta que pases por caja cada mes. Este modelo de micropagos por características físicas amenaza con extenderse a electrodomésticos, herramientas y dispositivos tecnológicos de uso diario."),
    ("propiedad_short_9", "es-ES-AlvaroNeural", "Escucha este dilema legal sobre la tienda digital más grande de PC. Valve y Steam han sido el refugio de millones de jugadores durante dos décadas gracias a sus excelentes ofertas. Pero según los términos del acuerdo de suscriptor de Steam, las cuentas son estrictamente personales y no se pueden heredar ni transferir por testamento. Si falleces, legalmente tus herederos no pueden reclamar la propiedad de tu biblioteca digital de miles de juegos. Tu patrimonio digital acumulado durante toda una vida se extingue contigo."),
    ("propiedad_short_10", "es-ES-AlvaroNeural", "Pon atención a la batalla legal por el Right to Repair. Gigantes tecnológicos diseñan deliberadamente sus productos con piezas emparejadas por software para evitar que reparadores independientes o tú mismo arregléis un componente roto. Si cambias una pantalla o una batería sin la herramienta de calibración oficial de la marca, el sistema operativo desactiva funciones clave o muestra advertencias constantes. Esta obsolescencia programada software te obliga a acudir a sus servicios técnicos oficiales a precios astronómicos o a desechar el producto."),
    ("propiedad_short_11", "es-ES-AlvaroNeural", "Escucha por qué la preservación cultural de los videojuegos está en peligro crítico. Más del 87% de los videojuegos clásicos lanzados antes de 2010 son inalcanzables de forma legal en la actualidad debido al cierre de tiendas digitales y el vencimiento de derechos. Las leyes de DRM criminalizan la conservación por parte de archivistas y museos digitales, mientras las grandes distribuidoras dejan morir catálogos enteros en el olvido. La emulación y la preservación comunitaria se han convertido en los únicos bastiones de resistencia cultural."),
    ("propiedad_short_12", "es-ES-AlvaroNeural", "Presta atención al cambio de paradigma económico global. La célebre frase del Foro Económico Mundial refleja la transición del capitalismo de propiedad al capitalismo de acceso o arrendamiento. Todo en nuestra vida digital está Virando hacia pagos recurrentes: música en Spotify, películas en Netflix, software en Adobe y juegos en consolas. Dejas de ser propietario de bienes tangibles para convertirte en un inquilino perpetuo del software corporativo, pagando mensualidades de por vida para conservar el derecho a usar lo que antes era tuyo."),
    ("propiedad_short_13", "es-ES-AlvaroNeural", "Escucha esta guía de supervivencia para mantener el control sobre tu tecnología. Frente al avance del monopolio digital, la resistencia pasa por apoyar plataformas DRM-Free como GOG, donde descargas los instaladores offline reales de tus juegos sin dependencia de servidores. Prioriza la compra de formatos físicos siempre que sea posible, respalda tus contenidos personalmente y exige legislaciones de derecho a reparar a tus representantes políticos. Tu independencia digital depende de que defiendas activamente el derecho a poseer lo que pagas.")
]

# Campaign 7: Pig Butchering Estafas (8 Shorts)
CAMPAIGN_7_SHORTS = [
    ("estafa_anime_short_1", "es-ES-AlvaroNeural", "Escucha esto con mucha atención si juegas online. Acabas de hacer una partida increíble en League of Legends, Counter-Strike o Valorant. De repente, recibes una solicitud de amistad inesperada de una cuenta con avatar de chica anime o foto de perfil de una joven asiática atractiva. Te envía un mensaje diciendo: Jugaste increíble, deberíamos hacer dúo alguna vez. Tu ego te dice que es real y aceptas de inmediato. Lo que no sabes es que estás entrando voluntariamente en el embudo de una red internacional de estafas cibernéticas conocida como Pig Butchering."),
    ("estafa_anime_short_2", "es-ES-AlvaroNeural", "Si escuchaste la parte uno, entenderás el origen siniestro de esta técnica. El término Pig Butchering o Sha Zhu Pan proviene del mandarín y significa literalmente engordar al cerdo antes del matadero. Los ciberdelincuentes dedican semanas o incluso meses a construir una relación de confianza y afecto fingido con la víctima. Chatean a diario sobre la vida cotidiana, comparten aficiones y brindan apoyo emocional. Una vez que la víctima está completamente enganchada emocionalmente, el estafador introduce sutilmente la trampa financiera."),
    ("estafa_anime_short_3", "es-ES-AlvaroNeural", "Presta atención al primer movimiento estratégico del estafador. Tras romper el hielo en el chat del juego o Discord, la supuesta chica te pide rápidamente migrar la conversación a WhatsApp o Telegram con la excusa de estar más conectados. Este cambio de plataforma busca sacarte de entornos donde otros jugadores o moderadores podrían advertirte sobre el perfil falso. Una vez en un canal privado de mensajería, comienzan a enviar fotos casuales sacadas de bancos de imágenes o cuentas robadas de redes sociales para reforzar la ilusión."),
    ("estafa_anime_short_4", "es-ES-AlvaroNeural", "Si escuchaste la parte uno, conoce cómo ejecutan el golpe financiero. Casualmente, en medio de las charlas afectivas, el personaje menciona que su tío o ella misma gana miles de dólares comerciando criptomonedas o divisas mediante una plataforma exclusiva. Te invitan a probar con una modesta inversión de 100 dólares. Te envían un enlace a una app o sitio web falso controlado por ellos. Milagrosamente, en pocas horas tu pantalla muestra que tus 100 dólares se convirtieron en 300. Es el señuelo perfecto para hacerte morder el anzuelo."),
    ("estafa_anime_short_5", "es-ES-AlvaroNeural", "Pon mucha atención a la maniobra psicológica más brillante del fraude. Para eliminar cualquier sospecha de estafa, el delincuente te incita activamente a retirar tus primeros 50 o 100 dólares de ganancia a tu cuenta bancaria real. Al ver que el dinero efectivamente llega a tu banco, tu cerebro invalida cualquier alarma de peligro. Convencido de que has descubierto una mina de oro guiado por tu pareja virtual, decides invertir todos tus ahorros de vida, solicitar préstamos bancarios o vender propiedades para depositarlos en la plataforma."),
    ("estafa_anime_short_6", "es-ES-AlvaroNeural", "Escucha el trágico desenlace de esta estafa cibernética. Cuando la víctima intenta retirar sus decenas de miles de dólares acumulados en la pantalla, la plataforma bloquea la transacción y exige pagar un supuesto impuesto de verificación del 20% o tasa de desbloqueo previa en dinero real. Desesperada por recuperar su dinero, la víctima paga miles adicionales. Al hacerlo, la web desaparece, el perfil del juego bloquea al usuario y la persona descubre que lo ha perdido absolutamente todo sin posibilidad de rastreo."),
    ("estafa_anime_short_7", "es-ES-AlvaroNeural", "Abre bien los ojos porque la realidad detrás de estos perfiles es aún más aterradora. Las personas que te escriben al otro lado de la pantalla a menudo no son criminales voluntarios, sino víctimas de trata de personas secuestradas en recintos fortificados en Myanmar y Camboya. Engañados con falsas ofertas de empleo tecnológico, son privados de sus pasaportes y obligados bajo tortura física y amenazas a operar docenas de perfiles falsos a diario para extorsionar a víctimas occidentales. Una industria millonaria manchada de sangre y esclavitud moderna."),
    ("estafa_anime_short_8", "es-ES-AlvaroNeural", "Escucha esta regla de oro definitiva para proteger tu dinero y tu salud mental. Ninguna persona atractiva desconocida que te agregue en un juego online o red social se enamorará de ti de forma repentina ni te ofrecerá oportunidades de inversión secretas. Si alguien que jamás has visto en persona menciona plataformas de trading, criptomonedas o transferencias de dinero, bloquea inmediatamente el contacto. La prevención y el escepticismo digital son tus únicos escudos reales en internet.")
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
    print("  EDGE-TTS AUDIO GENERATOR FOR CAMPAIGNS 6 & 7 (21 SHORTS)")
    print("=" * 80)
    print("\n--- CAMPAIGN 6: PROPIEDAD DIGITAL (13 SHORTS) ---")
    for sid, voice, text in CAMPAIGN_6_SHORTS:
        await generate_single_short_audio(sid, voice, text)
    print("\n--- CAMPAIGN 7: PIG BUTCHERING ESTAFAS (8 SHORTS) ---")
    for sid, voice, text in CAMPAIGN_7_SHORTS:
        await generate_single_short_audio(sid, voice, text)
    print("\n[ALL SUCCESS] 21 Audio Tracks and VTT Files Generated for Campaigns 6 & 7!")

if __name__ == "__main__":
    asyncio.run(main())
