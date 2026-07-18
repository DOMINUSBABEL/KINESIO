import os
import sys
import asyncio
import edge_tts

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
VOICE = "es-MX-JorgeNeural"
RATE = "+22%"

# Define scripts for Campaign 4
ESSAYS = {
    "argentina_essay_1": {
        "title": "POR QUÉ TODOS ODIAN A ARGENTINA (PARTE 1): LA SOBERBIA Y EL ÉXITO DEPORTIVO",
        "chapters": [
            {
                "num": 1,
                "title": "El Estigma del Agrandado",
                "text": "El término 'agrandado' es la etiqueta más común que el mundo le asigna al hincha argentino. Desde el exterior, se percibe una supuesta superioridad moral y una soberbia innata al hablar de fútbol. Esta actitud es vista a menudo como un rasgo irritante por aficionados de otros países. Sin embargo, lo que para muchos es prepotencia, dentro de la cultura rioplatense se vive como 'chicana' o una simple forma de comunicación lúdica y competitiva. La línea entre la autoconfianza y la soberbia es extremadamente delgada y suele malinterpretarse fácilmente."
            },
            {
                "num": 2,
                "title": "El Folclore Hiriente de las Canciones",
                "text": "Las hinchadas argentinas son reconocidas mundialmente por su creatividad y pasión para alentar en los estadios. Sin embargo, esa misma pasión a menudo cruza la línea hacia la humillación del rival. Letras que hacen referencia a crisis económicas, derrotas históricas, o temas sociales sensibles son cantadas con orgullo por miles. Para el aficionado extranjero, estas canciones no son folklore sano, sino una provocación hiriente y una falta absoluta de respeto deportivo. El debate sobre los límites del folklore del fútbol sigue más abierto que nunca."
            },
            {
                "num": 3,
                "title": "El Protagonista de la Historia",
                "text": "A la afición argentina le encanta sentirse el centro del universo futbolístico. Esta necesidad de protagonismo mediático y digital genera un rechazo automático en el resto de los países. Cuando Argentina gana, la cobertura es masiva, ruidosa y monopoliza las redes sociales. Aquellos que no comparten ese sentimiento patrio terminan saturados de la omnipresencia albiceleste en sus pantallas, lo que alimenta una corriente contraria de rechazo y el deseo generalizado de verlos caer en la siguiente oportunidad."
            },
            {
                "num": 4,
                "title": "El Peso del Éxito Deportivo Histórico",
                "text": "El odio deportivo suele ser proporcional al éxito. Con tres Copas del Mundo y múltiples Copas América, Argentina es un gigante del fútbol mundial. Su historia está llena de leyendas inalcanzables como Diego Maradona y Lionel Messi. Ser un ganador constante genera envidia y antipatía natural en rivales menos laureados. En el deporte de élite, el público neutral tiende a alinearse con el más débil, convirtiendo a Argentina en el villano perfecto a vencer en cada torneo."
            },
            {
                "num": 5,
                "title": "La Pasión que Asusta al Extranjero",
                "text": "Para un argentino, el fútbol no es un simple entretenimiento; es una religión, una parte fundamental de su identidad nacional. Esta intensidad extrema puede resultar incomprensible y hasta aterradora para culturas donde el deporte se vive con mayor distancia y tranquilidad. Lo que para un local es una demostración genuina de amor y lealtad a los colores, para un espectador externo es visto como fanatismo desmedido, obsesión insana y una preocupante falta de deportividad."
            },
            {
                "num": 6,
                "title": "El Contraste Cultural Rioplatense",
                "text": "La forma de hablar, el acento marcado y el uso del lenguaje coloquial de los argentinos suelen ser interpretados en otros países de habla hispana como prepotentes o altaneros. Existe una barrera cultural donde el humor ácido, la ironía constante y el tono de voz firme chocan con la cortesía y la timidez comunicativa de otras regiones de América Latina. Este choque idiomático y expresivo genera una antipatía automática antes de que ruede el balón."
            }
        ]
    },
    "argentina_essay_2": {
        "title": "POR QUÉ TODOS ODIAN A ARGENTINA (PARTE 2): LA SOSPECHA ARBITRAL Y LAS GRANDES POLÉMICAS",
        "chapters": [
            {
                "num": 1,
                "title": "La Sombra de Qatar Dos Mil Veintidós",
                "text": "La Copa del Mundo de Qatar dos mil veintidós fue el punto de inflexión definitivo para la 'argentinofobia' global. La gran cantidad de penales cobrados a favor de la albiceleste durante el torneo despertó sospechas inmediatas en todo el mundo. Aficionados y prensa internacional crearon la narrativa de un 'Mundial comprado' o diseñado para que Lionel Messi levantara la copa. A pesar de la calidad futbolística demostrada, la sombra de la duda y el favoritismo de la FIFA se convirtió en un dogma para sus detractores."
            },
            {
                "num": 2,
                "title": "Las Provocaciones del Dibu Martínez",
                "text": "Emiliano 'El Dibu' Martínez es quizás el jugador más polarizante del fútbol moderno. Sus bailes en los penales, sus gestos con los trofeos y sus comentarios desafiantes lo convirtieron en un héroe nacional en Argentina y en el enemigo público número uno en el exterior. Para sus críticos, el arquero encarna la falta de respeto y la mala educación deportiva. Para sus defensores, es un estratega psicológico brillante que juega al límite para ganar."
            },
            {
                "num": 3,
                "title": "El Juego Físico y Rudo del Plantel",
                "text": "El estilo de la selección argentina no solo es talento técnico, también es agresividad y roce físico constante. Jugadores como Rodrigo De Paul o Cristian Romero son conocidos por su vehemencia y su temperamento provocador en la cancha. Esta intensidad defensiva, al borde del reglamento, es catalogada por sus rivales como juego sucio e indisciplina consentida por los árbitros, sumando más argumentos a quienes los tachan de tramposos."
            },
            {
                "num": 4,
                "title": "El Mito de las Ayudas Arbitrales",
                "text": "Existe una creencia generalizada de que los árbitros protegen a las grandes figuras como Lionel Messi para mantener el espectáculo y el negocio del fútbol. Cada falta dudosa no cobrada o cada tarjeta perdonada a un jugador argentino es analizada bajo lupa por miles de usuarios en redes. Las repeticiones en cámara lenta y los debates virales perpetúan la idea de una impunidad sistemática que beneficia siempre a la albiceleste."
            },
            {
                "num": 5,
                "title": "Declaraciones de los Referentes",
                "text": "Las conferencias de prensa y entrevistas de los futbolistas y técnicos argentinos a menudo añaden leña al fuego. Frases que demuestran una confianza absoluta o que minimizan al rival son amplificadas por los medios de comunicación sedientos de polémica. La honestidad brutal o el tono descontracturado de los protagonistas suele traducirse fuera de sus fronteras como una flagrante falta de humildad y respeto hacia los rivales."
            },
            {
                "num": 6,
                "title": "El Antagonista Perfecto",
                "text": "El fútbol necesita narrativas y personajes claros para capturar la atención del público. Argentina, con su mezcla de talento extraordinario, temperamento fuerte y afición ruidosa, llena de forma natural el rol del antagonista perfecto. El mundo del fútbol disfruta odiando a Argentina porque hace que cada partido sea dramático, cargado de emociones extremas y con una tensión narrativa digna de una película de Hollywood."
            }
        ]
    },
    "argentina_essay_3": {
        "title": "POR QUÉ TODOS ODIAN A ARGENTINA (PARTE 3): GEOPOLÍTICA, XENOFOBIA Y REDES SOCIALES",
        "chapters": [
            {
                "num": 1,
                "title": "La Rivalidad Eterna con Inglaterra",
                "text": "El choque futbolístico entre Argentina e Inglaterra está profundamente marcado por la historia política y el conflicto bélico de las Islas Malvinas de mil novecientos ochenta y dos. El partido del Mundial de mil novecientos ochenta y seis, con los dos goles históricos de Diego Maradona, elevó este enfrentamiento a una dimensión mística y patriótica. La tensión entre ambos países demuestra cómo el fútbol puede canalizar heridas geopolíticas y mantener vivas rivalidades que van mucho más allá de un partido de noventa minutos."
            },
            {
                "num": 2,
                "title": "El Clásico Sudamericano Contra Brasil",
                "text": "La rivalidad con Brasil es el clásico más pasional y disputado de selecciones a nivel mundial. Es una guerra cultural y deportiva por el trono del fútbol sudamericano. Los comentarios provocadores de periodistas de ambos países, los incidentes violentos en las tribunas del Maracaná y la constante comparación entre Pelé y Maradona alimentan un fuego que nunca se apaga y que divide a todo el continente."
            },
            {
                "num": 3,
                "title": "El Tenso Choque con México",
                "text": "En los últimos años, la rivalidad entre México y Argentina ha crecido de forma exponencial, principalmente en el ámbito de las redes sociales. Lo que comenzó como una disparidad deportiva histórica se ha convertido en una batalla campal digital llena de insultos clasistas, burlas sobre la economía y descalificaciones culturales. Es un claro ejemplo de cómo el anonimato de internet puede radicalizar y afear una sana rivalidad futbolística."
            },
            {
                "num": 4,
                "title": "El Cántico Contra Francia",
                "text": "El reciente incidente del cántico polémico entonado por los jugadores argentinos tras ganar la Copa América desató un escándalo diplomático y deportivo con Francia. El cántico, que cuestionaba los orígenes de los jugadores franceses, fue calificado en Europa de racista y xenófobo. Este suceso evidenció las profundas diferencias culturales sobre lo que se considera humor aceptable en los festejos y deterioró la imagen internacional del equipo."
            },
            {
                "num": 5,
                "title": "La Toxicidad Viral de las Redes",
                "text": "Las plataformas digitales multiplican el odio de manera alarmante. Creadores de contenido y cuentas de memes explotan el sentimiento antiargentino para generar millones de vistas e interacciones rápidas. La polarización web obliga a los usuarios a elegir un bando, transformando los comentarios de los videos en vertederos de insultos nacionalistas y xenofobia mutua que dañan la convivencia de la comunidad futbolera."
            },
            {
                "num": 6,
                "title": "¿Odio Real o Solo Folklore?",
                "text": "Al final del día, cabe preguntarse si este rechazo generalizado es un odio real y profundo o simplemente parte del folklore teatral del fútbol. Para la gran mayoría, la rivalidad termina cuando se apaga la pantalla o se sale del estadio. La pasión desmedida, las provocaciones y los enojos son solo el precio a pagar por vivir el fútbol con una intensidad única que hace que este deporte sea el más hermoso del mundo."
            }
        ]
    }
}

SHORTS = {
    "argentina_essay_1_short_1": "El mito del agrandado argentino. ¿Por qué se les acusa de soberbios? En el exterior, su forma de hablar de fútbol se interpreta como egocentrismo. Pero para ellos, es solo 'chicana' y competitividad sana. ¿Tú qué opinas? #argentina #futbol #messi #polemica #shorts",
    "argentina_essay_1_short_2": "¿Fútbol o falta de respeto? Las hinchadas argentinas son muy creativas, pero a veces sus cantos cruzan la línea y humillan al rival con temas sensibles. Lo que llaman folklore, fuera se ve como provocación. #hinchada #copaamerica #argentina #shorts",
    "argentina_essay_1_short_3": "El precio de ganar. Argentina tiene tres Mundiales y leyendas como Maradona y Messi. El éxito genera envidia natural, y en el deporte, todos quieren ver caer al gigante. Son el villano perfecto. #maradona #campeon #mundial #datos #shorts",
    "argentina_essay_1_short_4": "La pasión que asusta. En Argentina, el fútbol es una religión absoluta. Esa intensidad extrema es incomprendida en otras culturas, donde se ve como fanatismo desmedido y falta de deportividad. #pasion #hinchas #cultura #shorts",
    "argentina_essay_1_short_5": "El choque cultural rioplatense. El acento y la ironía constante de los argentinos suelen ser interpretados en Latinoamérica como prepotencia. Un simple malentendido cultural antes de jugar. #latinoamerica #humor #rivalidad #shorts",
    "argentina_essay_2_short_1": "¿Un Mundial comprado? La sombra de Qatar dos mil veintidós. Los cinco penales cobrados a favor de Argentina crearon la teoría de que la FIFA quería coronar a Messi. ¿Ayuda real o calidad de campeón? #qatar2022 #messi #fifa #polemica #shorts",
    "argentina_essay_2_short_2": "El Dibu Martínez: ¿genio o provocador? Sus bailes y gestos desafiantes lo hacen héroe en su país y el más odiado fuera. ¿Falta de respeto o una estrategia psicológica brillante para ganar? #dibumartinez #penales #arquero #tactica #shorts",
    "argentina_essay_2_short_3": "El juego rudo albiceleste. El equipo no solo tiene talento, también agresividad física al límite del reglamento. Rodrigo De Paul y Cuti Romero imponen miedo, algo que los rivales tachan de juego sucio. #cutiromero #depaul #defensa #futbol #shorts",
    "argentina_essay_2_short_4": "¿Impunidad para las estrellas? Existe la teoría de que los árbitros protegen a figuras como Messi para cuidar el negocio. Cada falta no cobrada desata debates eternos en las redes sociales. #messi #arbitraje #negocios #deporte #shorts",
    "argentina_essay_2_short_5": "La honestidad brutal en la prensa. Las declaraciones sin filtro de los jugadores y técnicos argentinos suelen sonar soberbias fuera de sus fronteras. La prensa explota esto para generar clics. #declaraciones #prensa #humildad #shorts",
    "argentina_essay_3_short_1": "Inglaterra vs Argentina: más que fútbol. Una rivalidad nacida de la guerra de las Malvinas de mil novecientos ochenta y dos. El partido del ochenta y seis con Maradona convirtió el juego en una revancha patria. #malvinas #maradona #inglaterra #historia #shorts",
    "argentina_essay_3_short_2": "Brasil vs Argentina: la batalla por el trono. El clásico más caliente del mundo. Una guerra deportiva y cultural por el dominio de Sudamérica, llena de provocaciones y duelos de tribuna. #brasil #clasico #sudamerica #pele #shorts",
    "argentina_essay_3_short_3": "El tenso choque con México. En redes sociales, esta rivalidad ha explotado con insultos clasistas y burlas económicas. El anonimato de internet transformó una sana competencia en toxicidad pura. #mexico #seleccionmexicana #redessociales #shorts",
    "argentina_essay_3_short_4": "El cántico de la polémica. El festejo de los jugadores argentinos tras ganar la Copa América desató acusaciones de racismo desde Francia. Un escándalo que dañó su imagen internacional. #francia #polemica #copaamerica #racismo #shorts",
    "argentina_essay_3_short_5": "El negocio del odio digital. Creadores de contenido explotan el sentimiento antiargentino para ganar vistas fáciles. La polarización web transforma la sección de comentarios en un campo de batalla. #algoritmo #hater #toxicidad #redes #shorts",
    "argentina_essay_3_short_6": "¿Es odio real o solo folklore? Al final, la rivalidad futbolística suele terminar cuando se apaga la pantalla. Las peleas y provocaciones son parte del teatro que hace al fútbol tan apasionante. #debate #reflexion #folklore #deportes #shorts"
}

def write_scripts_file():
    filepath = os.path.join(BASE_DIR, "scripts_argentina_rivalries.md")
    print(f"Escribiendo guiones en: {filepath}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Guiones de Video Ensayos e Hilos de la Campaña 4 (Por Qué Odian a Argentina)\n")
        f.write("## Canal: DOMINUSBABEL (@dominus8735)\n\n---\n\n")
        
        # Write Widescreen Essays
        for key, val in ESSAYS.items():
            f.write(f"## 📌 {key}\n")
            for ch in val["chapters"]:
                f.write(f"### 📌 Capítulo {ch['num']}: {ch['title']}\n")
                f.write("*   **Audio (Voz en off):**\n")
                f.write(f'    "{ch["text"]}"\n')
                f.write(f'*   **Visual:** Escena dramática de fútbol en estadio o gráficos de rivalidad.\n\n')
            f.write("---\n\n")
            
        # Write Shorts Scripts Header
        f.write("# Guiones de Shorts: Campaña 4 (16 Shorts de 25-45 segundos)\n\n---\n\n")
        for key, val in SHORTS.items():
            f.write(f"### {key}\n")
            f.write(f'"{val}"\n\n')
            f.write("---\n\n")
            
    print("¡Guiones escritos exitosamente!")

async def generate_audio_file(text: str, output_path: str):
    print(f"Generando audio: {output_path}...")
    communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
    await communicate.save(output_path)

async def main():
    write_scripts_file()
    
    tasks = []
    # 1. Essays Audios
    for key, val in ESSAYS.items():
        essay_full_text = " ".join(ch["text"] for ch in val["chapters"])
        out_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        tasks.append(generate_audio_file(essay_full_text, out_path))
        
    # 2. Shorts Audios
    for key, val in SHORTS.items():
        out_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        tasks.append(generate_audio_file(val, out_path))
        
    print(f"\nIniciando generación paralela de {len(tasks)} audios con Edge TTS...")
    await asyncio.gather(*tasks)
    print("\n¡Todos los audios de la Campaña 4 han sido generados exitosamente!")

if __name__ == "__main__":
    asyncio.run(main())
