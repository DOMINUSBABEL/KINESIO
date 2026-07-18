import os
import sys
import asyncio
import edge_tts

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
VOICE = "es-MX-JorgeNeural"
RATE = "+22%"

# Define scripts for Campaign 3
ESSAYS = {
    "war_myths_essay_1": {
        "title": "MITOS DE GUERRA: 10 MENTIRAS DEL COMBATE REAL (PARTE 1)",
        "chapters": [
            {
                "num": 1,
                "title": "El Mito de la Música de Fondo",
                "text": "En el cine, los combates están acompañados por bandas sonoras heroicas que elevan la tensión. En la vida real, la guerra no tiene música. Los momentos de combate se caracterizan por silencios aterradores rotos por ráfagas repentinas, los gritos distantes de heridos y un constante pitido ensordecedor en tus oídos debido al ruido de las detonaciones. El silencio de la batalla real es mucho más traumático que cualquier escena de Hollywood."
            },
            {
                "num": 2,
                "title": "Siempre Ves a Tu Enemigo",
                "text": "La cultura popular nos enseña duelos cara a cara en el campo de batalla. La realidad de la infantería moderna es que rara vez ves a quien te está disparando. Los soldados disparan hacia destellos de cañón a la distancia, nubes de polvo levantadas por los disparos, o ventanas sospechosas en entornos urbanos. El combate real es una lucha constante contra un enemigo invisible que se esconde tras parapetos y trincheras a cientos de metros."
            },
            {
                "num": 3,
                "title": "El Rango Militar Equivale a Competencia",
                "text": "Asumimos que un rango superior garantiza mayor conocimiento y habilidad táctica. Sin embargo, en el frente, los rangos a menudo son administrativos. Oficiales recién graduados de la academia pueden cometer errores trágicos por falta de experiencia real, mientras que sargentos y cabos curtidos en batalla terminan tomando las decisiones operativas reales. En combate, la competencia se demuestra con sangre, no con insignias."
            },
            {
                "num": 4,
                "title": "Disparas Tu Fusil Todo el Tiempo",
                "text": "El cine retrata a los soldados disparando ráfagas continuas en cada combate. En realidad, un soldado de infantería pasa el noventa y nueve por ciento de su tiempo transportando equipo pesado, excavando trincheras y esperando bajo la lluvia. Firar el fusil es solo una pequeña fracción del tiempo en guerra. Además, la munición es un recurso limitado que debe cuidarse celosamente, priorizando el fuego selectivo y la puntería."
            },
            {
                "num": 5,
                "title": "La Guerra es Puro Ruido Ensordecedor",
                "text": "Aunque las armas son ruidosas, el estrés extremo altera la percepción humana. Debido a la adrenalina, muchos soldados experimentan exclusión auditiva, un fenómeno donde el cerebro bloquea el sonido de las explosiones y disparos para concentrarse en la supervivencia. El combate puede sentirse extrañamente silencioso, con sonidos amortiguados como si estuvieras bajo el agua, haciendo que la experiencia de la batalla sea psicológicamente surrealista."
            },
            {
                "num": 6,
                "title": "Siempre Sabes lo que Está Pasando",
                "text": "Las películas muestran mapas tácticos digitales y comandantes que controlan cada movimiento. En el terreno, la niebla de guerra es total y absoluta. El soldado promedio solo conoce su esquina, su trinchera y a los compañeros a su lado. La información fluye tarde, las órdenes se contradicen y el caos de las comunicaciones hace que saber el estado real de la batalla sea una tarea casi imposible."
            },
            {
                "num": 7,
                "title": "Sabes de Inmediato Cuando te Disparan",
                "text": "Creemos que recibir un disparo causa un dolor insoportable inmediato. En combate, la adrenalina inunda el cuerpo, bloqueando temporalmente los receptores de dolor. Muchos soldados continúan corriendo o disparando sin darse cuenta de que han sido heridos. A menudo descubren el impacto al sentir la humedad de su propia sangre, notar debilidad repentina al intentar apoyar una extremidad, o cuando un compañero los revisa."
            },
            {
                "num": 8,
                "title": "Recuerdas Cada Detalle con Claridad",
                "text": "El trauma extremo daña el almacenamiento de la memoria. Bajo el pánico del combate, el cerebro archiva recuerdos de manera fragmentada. Un soldado puede recordar con absoluta nitidez un detalle absurdo, como el color de una alfombra o un insecto en el suelo, pero olvidar por completo cuántas horas duró el tiroteo o el orden cronológico de los sucesos. La memoria de guerra es un rompecabezas incompleto."
            },
            {
                "num": 9,
                "title": "Las Milicias No Sirven en Combate",
                "text": "Se cree que las fuerzas irregulares son inferiores a los ejércitos profesionales. La historia demuestra lo contrario en la guerra asimétrica. Milicias locales motivadas, con un profundo conocimiento del terreno y usando tácticas de guerrilla, pueden desgastar y derrotar a las superpotencias militares mejor equipadas del mundo. La motivación, el sigilo y la defensa del propio hogar superan la tecnología militar pura."
            },
            {
                "num": 10,
                "title": "El Soldado Occidental es Superior",
                "text": "El mito de la superioridad táctica occidental cae ante la cruda realidad del terreno. En las selvas densas, pantanos o desiertos extremos, el entrenamiento tecnológico sofisticado sirve de poco si no te adaptas al entorno. El soldado local, acostumbrado al clima y sin la necesidad de una cadena logística gigante, suele ser mucho más letal y resistente. La supervivencia en guerra pertenece al que mejor se adapta."
            }
        ]
    },
    "war_myths_essay_2": {
        "title": "MITOS DE GUERRA: 10 MENTIRAS DEL COMBATE REAL (PARTE 2)",
        "chapters": [
            {
                "num": 1,
                "title": "Siempre Sabes Quién es el Enemigo",
                "text": "Los videojuegos dividen a los bandos por uniformes de colores claros. En los conflictos modernos, la identificación del enemigo es una pesadilla constante. En combates urbanos, los combatientes suelen vestir ropas civiles y mezclarse con la población local. Distinguir a un insurgente de un civil inocente o incluso evitar el fuego amigo en la confusión del combate es uno de los mayores desafíos éticos y tácticos en la actualidad."
            },
            {
                "num": 2,
                "title": "Los Drones Son Armas Indestructibles",
                "text": "Aunque los drones han revolucionado el campo de batalla, distan de ser invulnerables. Los drones comerciales de bajo costo son derribados diariamente por miles. La guerra electrónica avanzada bloquea sus señales GPS y de control, haciéndolos caer. Además, la infantería ha recurrido al uso de escopetas de caza, redes físicas y jammers portátiles para derribarlos antes de que puedan acercarse a sus posiciones."
            },
            {
                "num": 3,
                "title": "Los Pilotos de Drones Están a Salvo",
                "text": "Existe la idea de que operar drones de forma remota elimina todo el riesgo físico para el piloto. En realidad, los operadores en el frente son los objetivos prioritarios de la artillería enemiga. Los sistemas de guerra electrónica triangulan las ondas de radio emitidas por el control del piloto en cuestión de minutos. Los pilotos deben moverse constantemente para evitar ser alcanzados por ataques de artillería devastadores."
            },
            {
                "num": 4,
                "title": "Los Drones FPV Reemplazarán Todo",
                "text": "Los drones suicidas FPV son letales y económicos, pero no son el arma definitiva. Tienen serias limitaciones: sus baterías duran pocos minutos, el mal tiempo o el viento fuerte los inutilizan y la interferencia electrónica bloquea su señal tras colinas. No pueden reemplazar el volumen sostenido de fuego de la artillería pesada ni la capacidad de ocupar terreno que solo tiene la infantería tradicional."
            },
            {
                "num": 5,
                "title": "Todos Reaccionan Igual Ante el Trauma",
                "text": "El mito del estrés postraumático asume que todos los soldados experimentan el trauma de la misma manera. El dolor psicológico se manifiesta de formas infinitas. Algunos soldados experimentan bloqueos mudos durante la batalla, otros desarrollan ansiedad años después de retirarse y algunos muestran resiliencia inicial pero colapsan ante detonantes cotidianos. No existe una respuesta psicológica estándar ante el horror de la guerra."
            },
            {
                "num": 6,
                "title": "Reconoces al Veterano a Simple Vista",
                "text": "Las películas nos muestran a los veteranos como tipos rudos y agresivos que intimidan a los demás. En la práctica militar, los soldados más ruidosos y arrogantes suelen ser los primeros en entrar en pánico bajo fuego real. El verdadero veterano de combate suele ser el más callado, el que mantiene una calma aparente bajo el caos y realiza sus tareas de forma metódica. La verdadera madurez militar es silenciosa."
            },
            {
                "num": 7,
                "title": "La Guerra Sigue Una Lógica Coherente",
                "text": "El espectador externo cree que cada movimiento militar obedece a una estrategia brillante. En el terreno de combate, la realidad está marcada por la confusión. Órdenes contradictorias de generales lejanos, misiones que parecen no tener sentido, fuego amigo trágico y errores de logística absurdos son la norma. La guerra es intrínsecamente caótica, desorganizada y absurda para quienes la viven de cerca."
            },
            {
                "num": 8,
                "title": "Las Granadas Explotan en Bolas de Fuego",
                "text": "Hollywood nos ha acostumbrado a explosiones con gigantescas bolas de fuego naranja producidas por granadas. Una granada real explota con un estallido seco y agudo, levantando una nube de polvo gris y metralla casi invisible a simple vista. Lo peligroso no es el fuego, sino los miles de fragmentos de metal que vuelan a velocidad supersónica en todas direcciones. Una explosión real es discreta pero letal."
            },
            {
                "num": 9,
                "title": "El Chaleco Antibalas Te Hace Inmune",
                "text": "El equipo de protección corporal moderno salva vidas, pero no te hace invencible. Las placas de cerámica o acero solo protegen el torso superior. Un impacto directo de fusil, aunque sea detenido por la placa, transfiere una energía brutal que puede fracturar costillas, colapsar pulmones o causar hemorragias internas graves. Además, las extremidades y el cuello siguen expuestos a la metralla mortal."
            },
            {
                "num": 10,
                "title": "Los Silenciadores Hacen las Armas Inaudibles",
                "text": "El cine nos muestra que un silenciador reduce el disparo a un susurro casi inaudible. En realidad, un supresor solo reduce el ruido de salida de los gases para evitar la sordera del tirador y ocultar el destello de luz. El proyectil en sí sigue viajando a velocidad supersónica, rompiendo la barrera del sonido con un estallido ruidoso y agudo que se escucha a cientos de metros del lugar de disparo."
            }
        ]
    }
}

SHORTS = {
    "war_myths_essay_1_short_1": "El mito de la música en combate. En el cine, las batallas tienen bandas sonoras épicas. En la realidad, la guerra se vive en un silencio tenso, interrumpido por ráfagas repentinas, gritos lejanos y un pitido ensordecedor en tus oídos por las detonaciones. El combate real no tiene música, solo caos. #guerra #historia #combate #mitos #shorts",
    "war_myths_essay_1_short_2": "¿Siempre ves a tu enemigo? En las películas, los soldados luchan cara a cara. En el combate moderno, rara vez ves a quien te dispara. Disparas a destellos lejanos, nubes de polvo o ventanas sospechosas. Es una lucha constante contra un enemigo invisible a cientos de metros. #militar #datos #soldados #shorts",
    "war_myths_essay_1_short_3": "El rango no equivale a competencia. Creemos que una estrella en el hombro garantiza sabiduría táctica. Pero en el frente, los oficiales novatos cometen errores graves por falta de experiencia, mientras los sargentos veteranos toman las decisiones reales para salvar vidas. #ejercito #liderazgo #realidad #shorts",
    "war_myths_essay_1_short_4": "¿Disparan todo el tiempo? El cine muestra tiroteos interminables. En la realidad, la infantería pasa el noventa y nueve por ciento del tiempo cargando equipo, cavando trincheras y esperando bajo la lluvia. Firar el arma es solo una mínima fracción, y la munición se cuida con celo. #infanteria #tactica #guerra #shorts",
    "war_myths_essay_1_short_5": "La guerra no siempre es ruidosa. Aunque las armas aturden, el estrés extremo activa la exclusión auditiva. Tu cerebro bloquea el sonido de las explosiones para sobrevivir. El combate puede sentirse extrañamente silencioso, como si estuvieras bajo el agua. Un silencio surrealista. #psicologia #sobrevivir #datos #shorts",
    "war_myths_essay_1_short_6": "La mentira del control absoluto. Las películas muestran mapas digitales donde todo se entiende. En el terreno, la niebla de guerra domina. El soldado solo sabe lo que pasa en su trinchera. Las órdenes se contradicen, la radio falla y el caos táctico es la regla general. #estrategia #caos #historia #shorts",
    "war_myths_essay_1_short_7": "¿Sientes cuando te disparan? La adrenalina extrema bloquea el dolor de inmediato. Muchos soldados siguen corriendo o disparando heridos sin notarlo. Descubren el impacto minutos después al sentir la sangre caliente, notar debilidad o al ser revisados por un compañero. #medicina #adrenalina #combate #shorts",
    "war_myths_essay_1_short_8": "La memoria bajo fuego se rompe. El trauma fragmenta los recuerdos. Un soldado puede recordar con total nitidez un detalle absurdo, como un insecto en el suelo, pero olvidar por completo el orden de la batalla o las horas transcurridas. La memoria de guerra es confusa. #cerebro #memoria #guerra #shorts",
    "war_myths_essay_1_short_9": "Las milicias locales no sirven. Falso. En combate asimétrico, milicias motivadas con conocimiento del terreno y tácticas de guerrilla pueden desgastar y derrotar a las superpotencias militares mejor equipadas. La defensa del hogar supera la tecnología pura. #guerrilla #milicia #historia #shorts",
    "war_myths_essay_1_short_10": "El soldado occidental es superior. La tecnología y el entrenamiento sirven de poco en selvas densas o desiertos extremos si no te adaptas. El soldado local, acostumbrado al clima y sin depender de una gran cadena logística, suele ser mucho más resistente y letal. #supervivencia #tactica #entrenamiento #shorts",
    "war_myths_essay_2_short_1": "Identificar al enemigo es una pesadilla. En las guerras modernas no hay uniformes de colores claros. En el combate urbano, los insurgentes visten ropa civil y se mezclan con los inocentes. Evitar el fuego amigo y las bajas civiles es un desafío trágico y diario. #combate #ciudades #ejercito #shorts",
    "war_myths_essay_2_short_2": "Los drones no son indestructibles. Aunque dominan el cielo, los drones comerciales son vulnerables. La guerra electrónica bloquea su señal GPS diariamente. Además, la infantería usa escopetas de caza y jammers portátiles para derribarlos antes de que ataquen. #tecnologia #drones #defensa #shorts",
    "war_myths_essay_2_short_3": "Los pilotos de drones están a salvo. Falso. Los operadores en el frente son los objetivos más buscados. La guerra electrónica triangula la señal de radio de sus controles en minutos. Por eso, los pilotos deben moverse constantemente para evitar fuego de artillería inmediato. #drones #artilleria #guerra #shorts",
    "war_myths_essay_2_short_4": "Los drones FPV no reemplazarán todo. Son letales, pero sus baterías duran minutos, el viento o la lluvia los inutilizan y la interferencia los bloquea. No pueden sustituir la artillería pesada ni la necesidad de infantería para ocupar y defender el terreno. #tecnologia #drones #combate #shorts",
    "war_myths_essay_2_short_5": "El trauma no es igual para todos. El estrés postraumático se manifiesta de formas infinitas. Algunos se bloquean en el frente, otros sufren pesadillas años después, y algunos colapsan con ruidos cotidianos. No existe una respuesta mental estándar al horror. #psicologia #ptsd #saludmental #shorts",
    "war_myths_essay_2_short_6": "El mito del soldado rudo. En las películas el veterano es agresivo y amenazante. En la realidad, los más ruidosos suelen entrar en pánico bajo fuego real. El verdadero veterano es silencioso, metódico y mantiene la calma fría en medio del caos. La templanza es invisible. #liderazgo #veterano #realidad #shorts",
    "war_myths_essay_2_short_7": "La guerra no tiene lógica. Creemos que cada misión obedece a un plan brillante. En la realidad, los soldados lidian con órdenes absurdas, misiones inútiles, errores de logística ridículos y fuego amigo. La guerra real es desorganizada, confusa y frustrante. #ejercito #absurdo #caos #shorts",
    "war_myths_essay_2_short_8": "Las granadas no causan bolas de fuego. El cine usa gasolina para crear explosiones espectaculares. Una granada real estalla de forma seca y gris, levantando polvo y lanzando miles de fragmentos de metal invisibles pero letales. Lo peligroso es la metralla, no el fuego. #armas #granadas #datos #shorts",
    "war_myths_essay_2_short_9": "El chaleco antibalas no te hace inmune. Protege tus órganos vitales, pero un impacto directo de fusil transfiere tanta energía que puede fracturar costillas, colapsar pulmones o causar graves sangrados internos. Además, tus brazos y piernas quedan expuestos. #chaleco #proteccion #infanteria #shorts",
    "war_myths_essay_2_short_10": "Los silenciadores no hacen el arma muda. En las películas son un susurro. En la realidad, solo reducen el ruido de los gases de salida para no ensordecer al tirador. La bala sigue viajando a velocidad supersónica, creando un estallido ruidoso audible a cientos de metros. #silenciador #armas #mitos #shorts"
}

def write_scripts_file():
    filepath = os.path.join(BASE_DIR, "scripts_war_myths.md")
    print(f"Escribiendo guiones en: {filepath}...")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# Guiones de Video Ensayos e Hilos de la Campaña 3 (Mitos de Guerra)\n")
        f.write("## Canal: DOMINUSBABEL (@dominus8735)\n\n---\n\n")
        
        # Write Widescreen Essays
        for key, val in ESSAYS.items():
            f.write(f"## 📌 {key}\n")
            for ch in val["chapters"]:
                f.write(f"### 📌 Capítulo {ch['num']}: {ch['title']}\n")
                f.write("*   **Audio (Voz en off):**\n")
                f.write(f'    "{ch["text"]}"\n')
                f.write(f'*   **Visual:** Escena dramática de combate militar en Gates of Hell.\n\n')
            f.write("---\n\n")
            
        # Write Shorts Scripts Header
        f.write("# Guiones de Shorts: Campaña 3 (20 Shorts Complementarios)\n\n---\n\n")
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
    
    # Generate audio files directory setup
    tasks = []
    
    # 1. Essays Audios (Concatenate chapters)
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
    print("\n¡Todos los audios de la Campaña 3 han sido generados exitosamente!")

if __name__ == "__main__":
    asyncio.run(main())
