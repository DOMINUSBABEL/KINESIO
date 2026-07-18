import os
import sys
import time
import datetime
import subprocess
import re

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
VAREGO_DIR = r"C:\Users\jegom\VAREGO"

uploaded_file_log_1 = os.path.join(BASE_DIR, "uploaded_campaign_1.txt")
uploaded_file_log_2 = os.path.join(BASE_DIR, "uploaded_campaign_2.txt")
uploaded_file_log_3 = os.path.join(BASE_DIR, "uploaded_campaign_3.txt")
uploaded_file_log_4 = os.path.join(BASE_DIR, "uploaded_campaign_4.txt")
file_shorts_c2 = os.path.join(BASE_DIR, "scripts_expansion_shorts.md")
file_shorts_c3 = os.path.join(BASE_DIR, "scripts_war_myths.md")
file_shorts_c4 = os.path.join(BASE_DIR, "scripts_argentina_rivalries.md")

# ==========================================
# CAMPAIGN 1 UPGRADED SEO METADATA
# ==========================================
STEAM_ESSAY_SEO = {
    "title": "El Monopolio Más Querido del Mundo (Y Por Qué Nadie Puede Derrotarlo)",
    "desc": "Steam controla casi el 75% del mercado de PC. En cualquier otra industria, esto sería un monopolio odiado... pero los gamers lo defienden a muerte. ¿Cuál es el secreto de Valve y Gabe Newell para tener clientes tan leales? Descúbrelo en este análisis. \n\nSuscríbete para más secretos de la industria del gaming. #steam #valve #pcgaming #monopolio #epicgames"
}

SONY_ESSAY_SEO = {
    "title": "El Peligroso Plan de Sony para Quitarte la Propiedad de tus Juegos",
    "desc": "La PS5 Pro sin lectora de discos no es solo una consola cara, es el inicio de una era donde YA NO ERES DUEÑO de lo que compras. Si el formato físico muere, tu biblioteca digital puede desaparecer con un solo clic de Sony. ¿Estamos ante el fin de la propiedad privada en el gaming? \n\n¡Dale like y suscríbete para defender la preservación de los videojuegos! #playstation #ps5pro #sony #formatofisico #gaming"
}

ROMAN_ESSAYS_SEO = {
    "augusto": {
        "title": "El Político Más Astuto de la Historia: Cómo Augusto Engañó a Toda Roma",
        "desc": "Heredó un imperio destrozado a los 18 años. Estaba rodeado de enemigos que habían asesinado a Julio César por querer ser rey. ¿Cómo logró Octavio Augusto gobernar como emperador absoluto durante 40 años sin que nadie lo llamara tirano? La jugada maestra del primer emperador. #roma #historia #imperioromano #augusto #curiosidades"
    },
    "trajano": {
        "title": "El Emperador Perfecto de Roma (Y la Conquista que Nadie Pudo Repetir)",
        "desc": "Coronado como 'Optimus Princeps' (el mejor de los emperadores), Trajano desafió los límites del mundo conocido. Desde las indomables montañas de Dacia hasta los desiertos de Partia, esta es la historia del general hispano que llevó a las legiones romanas a su máxima gloria y extensión. #trajano #imperioromano #historia #roma #militares"
    },
    "aureliano": {
        "title": "El Humilde Soldado que Salvó a Roma del Apocalipsis en Solo 5 Años",
        "desc": "En el siglo III, el Imperio Romano estaba fragmentado, invadido y al borde de la desaparición total. Entonces apareció Aureliano, un general de origen humilde que en tiempo récord derrotó a usurpadores, aplastó a los bárbaros y reunificó el imperio. Esta es la epopeya del 'Restaurador del Mundo'. #aureliano #historia #roma #imperioromano #antiguedad"
    },
    "constantino": {
        "title": "La Cruz de Fuego que Cambió el Destino de Roma para Siempre",
        "desc": "Una visión mística antes de la batalla del Puente Milvio, una señal en el cielo y la decisión política y religiosa más trascental de la historia de Occidente. ¿Cómo Constantino el Grande usó la cruz cristiana para unificar y refundar un imperio al borde del colapso? #constantino #roma #historia #religion #puentemilvio"
    },
    "mayoriano": {
        "title": "El Héroe Olvidado que Casi Salva a Roma de la Caída Definitiva",
        "desc": "Cuando el Imperio de Occidente agonizaba, un hombre se negó a rendirse. Mayoriano reconquistó Hispania y la Galia, reconstruyó la armada romana y desafió a los bárbaros... hasta que la traición interna selló su trágico destino. La historia del último gran emperador de Occidente. #mayoriano #roma #historia #tragedia #imperioromano"
    },
    "justiniano": {
        "title": "El Emperador Bizantino que Intentó Reconstruir la Roma de los Césares",
        "desc": "Con el apoyo del legendario general Belisario y la implacable emperatriz Teodora, Justiniano desafió a la peste, reconstruyó Hagia Sophia, codificó el derecho romano y reconquistó Italia y África. Esta es la historia del último emperador que soñó con una Roma unida. #justiniano #imperiobizantino #historia #roma #belisario"
    }
}

STOIC_SHORTS_SEO = {
    1: {"title": "El Secreto Estoico de la Paz Mental (Kli vs Control) 🛡", "desc": "La dicotomía del control estoica y el concepto místico de la vasija (Kli). #estoicismo #cabala #sabiduria"},
    2: {"title": "Cómo Construir una Mente Indestructible 🏛", "desc": "La 'ciudadela interior' estoica de Marco Aurelio y la chispa divina (Shejiná) en tu interior. #estoicismo #crecimiento #mindset"},
    3: {"title": "El Poder Oculto de Callar ante un Insulto (Tzimtzum) 🤫", "desc": "Contraer tu ego es la mayor muestra de fortaleza. El secreto cabalístico del Tzimtzum y el autocontrol. #autocontrol #sabiduria #ego"},
    4: {"title": "Por qué Deberías Amar tu Destino (Amor Fati) 👑", "desc": "Aceptar el destino estoico te alinea con la voluntad superior (Keter) en el Árbol de la Vida. #amorfati #filosofia #destino"},
    5: {"title": "Agradece tus Problemas: El Crisol que Esculpe tu Alma 💎", "desc": "Las dificultades no son obstáculos, son los golpes de cincel que crean belleza moral (Tiferet). #resiliencia #estoicismo #reflexion"}
}

ROMAN_SHORTS_SEO = {
    1: {"title": "El Hombre que Rechazó ser Rey para Salvar a Roma 🏛", "desc": "Octavio Augusto fundó la Pax Romana y reconstruyó el imperio sin ceñirse jamás la corona de rey. #historia #roma #curiosidades"},
    2: {"title": "El Emperador Más Exitoso que Roma Jamás Conoció ⚔", "desc": "Trajano llevó al Imperio Romano a su máxima extensión militar y fue aclamado como el mejor (Optimus Princeps). #trajano #guerra #historia"},
    3: {"title": "Aureliano: El Humilde Soldado que Salvó al Imperio de la Muerte 🛡", "desc": "Aureliano reunificó un imperio fragmentado en solo 5 años de reinado militar heroico. #aureliano #roma #imperioromano"},
    4: {"title": "Constantino y la Visión Mística que Cambió el Mundo ✝", "desc": "La visión de la cruz de fuego en el cielo que llevó a Constantino a tolerar y abrazar el cristianismo. #constantino #historia #misterio"},
    5: {"title": "Mayoriano: El Último Héroe Real del Imperio de Occidente 🕯", "desc": "Mayoriano luchó en el frente y reformó leyes para revivir el moribundo imperio antes de ser traicionado. #historia #roma #tragedia"},
    6: {"title": "El Emperador que Resucitó la Gloria de Roma desde las Cenizas 📜", "desc": "Justiniano reconquistó las provincias occidentales perdidas y codificó las bases del derecho civil. #justiniano #imperiobizantino #leyes"}
}

SONY_SHORTS_SEO = {
    1: {"title": "El Impuesto Oculto de la PS5 Pro de Sony 🎮", "desc": "$700 por una consola sin lectora de discos. La trampa corporativa para obligarte al mercado digital. #playstation #ps5pro #gaming"},
    2: {"title": "Por qué Comprar Juegos Digitales es una Trampa ⚖", "desc": "Sony borró películas y contenidos comprados por los usuarios de sus bibliotecas. Comprar digital es solo rentar. #derechos #playstation #sony"},
    3: {"title": "La Demo Legendaria de Silent Hills que Desapareció 🏛", "desc": "P.T. de Hideo Kojima fue borrado por completo de la tienda digital. Sin disco físico, el arte se pierde. #silenthills #pt #preservacion"},
    4: {"title": "La Trampa Detrás de Eliminar el Lector de Discos 💸", "desc": "Sin formato físico, las tiendas oficiales tienen el monopolio absoluto. Adiós al mercado de juegos usados. #monopolio #ps5 #gaming"},
    5: {"title": "Pagaron $70 por un Juego que Ya No Existe 💥", "desc": "Ubisoft apagó los servidores de The Crew, convirtiendo un disco digital en un archivo inservible. #estafa #gaming #thecrew"},
    6: {"title": "Por qué el Formato Físico es Defender tus Derechos 👑", "desc": "El disco físico es tu única garantía de propiedad real, juego offline y preservación histórica. #formatofisico #preservacion #gaming"}
}

STEAM_SHORTS_SEO = {
    1: {"title": "El Monopolio Más Querido y Defendido del Mundo 🌐", "desc": "Valve controla casi el 75% de las ventas en PC, pero la comunidad de gamers defiende a Gabe Newell a muerte. #steam #valve #gaming"},
    2: {"title": "El Impuesto del 30% que Cobran Valve y Apple 💸", "desc": "La controvertida comisión del 30% de Steam y Apple comparada con el 12% de Epic Store. El núcleo de las demandas. #comisiones #steam"},
    3: {"title": "La Cláusula Secreta de Valve para Mantener Precios Altos ⚖", "desc": "Demandas antitrust acusan a Valve de obligar a los desarrolladores a no vender más barato en otras tiendas de PC. #steam #precios #monopolio"},
    4: {"title": "Los Correos Secretos de Microsoft que Delatan a Steam 💼", "desc": "Correos internos revelados en juicio muestran cómo Valve exige paridad de precios de forma verbal. #filtraciones #gaming #steam"},
    5: {"title": "El Soporte al Usuario que Convirtió a Valve en un Gigante Intocable 🔄", "desc": "Reembolsos en menos de dos horas y garantía total. El impecable servicio que mantiene leales a los gamers. #steam #reembolsos #hardware"},
    6: {"title": "El Superpoder de Gabe Newell para Proteger a los Jugadores 👑", "desc": "Al no cotizar en bolsa, Valve no tiene que rendir cuentas a accionistas codiciosos. Libertad absoluta. #gabenewell #valve #pcgaming"}
}

ROMAN_EXTRA_SHORTS_SEO = {
    "roman_extra_augusto_1": ("El Trágico y Secreto Fin de Cleopatra y Marco Antonio ⚔", "La legendaria batalla de Actio y la desesperada decisión de la última reina de Egipto para evitar ser exhibida como trofeo en Roma. #cleopatra #historia #curiosidades #roma"),
    "roman_extra_augusto_2": ("El Destierro de la Hija de Augusto: Sexo y Escándalo en Roma 🏛", "Julia la Mayor desafió las estrictas leyes morales de su propio padre, el emperador Augusto, terminando exiliada en una isla desierta de por vida. #augusto #historia #escandalo"),
    "roman_extra_augusto_3": ("¡Devuélveme mis legiones! El peor desastre militar de Augusto 🌲", "Tres legiones romanas masacradas en el bosque de Teutoburgo y la desesperación que llevó a Augusto a golpearse la cabeza contra las paredes. #teutoburgo #guerra #historia"),
    "roman_extra_trajano_1": ("El Orgullo de un Rey: El trágico suicidio de Decébalo ⚔", "El rey de Dacia prefirió cortarse la garganta bajo un árbol antes que desfilar encadenado en el triunfo militar de Trajano. #trajano #guerra #historia"),
    "roman_extra_trajano_2": ("La repentina muerte de Trajano en plena gloria imperial 💀", "El emperador que llevó a Roma a su máxima extensión encontró su fin no en batalla, sino por un derrame cerebral volviendo de Oriente. #historia #trajano #roma"),
    "roman_extra_trajano_3": ("Las 165 Toneladas de Oro que Financieron el Imperio Romano 🏆", "La increíble riqueza oculta en los ríos de Dacia que Trajano saqueó para construir su monumental Foro e inaugurar espectáculos gigantescos. #oro #roma #historia"),
    "roman_extra_aureliano_1": ("Zenobia de Palmira: La reina rebelde que desafió a Roma 👑", "Aureliano sitió Palmira y capturó a su bella emperatriz, obligándola a desfilar en Roma atada con cadenas de oro puro. #aureliano #zenobia #historia"),
    "roman_extra_aureliano_2": ("La lista de la muerte que costó la vida a un gran emperador ☠", "Un secretario corrupto falsificó una lista de ejecuciones para asustar a los generales, quienes asesinaron a Aureliano por pánico. #complot #tragedia #historia"),
    "roman_extra_aureliano_3": ("La Sangrienta Rebelión de los Monederos de Roma 💥", "Los trabajadores de la ceca de Roma se rebelaron por corrupción y Aureliano aplastó la revuelta dejando 7,000 cadáveres en las calles. #historia #aureliano #roma"),
    "roman_extra_constantino_1": ("La Señal en el Cielo que Convirtió al Imperio Romano ✝", "La famosa visión de Constantino antes de la batalla del Puente Milvio: 'Con este signo vencerás'. #constantino #historia #misterio"),
    "roman_extra_constantino_2": ("El Oscuro Secreto de Constantino: ¿Por qué ejecutó a su hijo? 💔", "El brillante heredero Crispo fue ejecutado por orden de su padre bajo cargos de una supuesta intriga con su madrastra Fausta. #tragedia #misterio #historia"),
    "roman_extra_constantino_3": ("La Emperatriz Ahogada: Fausta borrada de la historia 🏛", "La esposa de Constantino murió ahogada en un baño hirviendo y su nombre fue borrado de todos los registros del imperio. #constantino #historia #misterio"),
    "roman_extra_mayoriano_1": ("La Última Reconquista: Campaña invernal de Mayoriano 🛡", "En pleno invierno, Mayoriano cruzó los Alpes con un ejército germánico y reconquistó las provincias de Galia e Hispania. #historia #militar #roma"),
    "roman_extra_mayoriano_2": ("La Gran Armada que Roma Perdió por Traición ⚓", "El plan de Mayoriano para invadir Cartago quedó destrozado cuando los vándalos quemaron sus 300 barcos en el puerto de Alicante mediante espías. #tragedia #historia"),
    "roman_extra_mayoriano_3": ("El Cruel Asesinato del Último Héroe Romano ☠", "El general bárbaro Ricimero arrestó a Mayoriano, lo torturó durante cinco días y lo decapitó, sellando el fin de Occidente. #tragedia #historia #roma"),
    "roman_extra_justiniano_1": ("La Increíble Reconquista de Cartago en solo 15 días ⚔", "El general Belisario desembarcó en África con 15,000 hombres y aniquiló el reino de los vándalos para devolver la tierra al imperio. #belisario #historia #guerra"),
    "roman_extra_justiniano_2": ("30,000 Muertos: La revuelta que casi destruye Constantinopla 💀", "Los ciudadanos de Constantinopla gritaron 'Nika' (victoria) contra Justiniano, quien ordenó a sus generales masacrar a la multitud atrapada en el Hipódromo. #justiniano #tragedia #historia"),
    "roman_extra_justiniano_3": ("Teodora: De bailarina exótica a emperatriz romana 👑", "La fascinante historia de la mujer más poderosa de Bizancio, cuya valentía salvó el trono de Justiniano durante las revueltas. #teodora #historia #mujerespoderosas")
}

# ==========================================
# CAMPAIGN 2 UPGRADED SEO METADATA
# ==========================================
WIDESCREEN_METADATA_C2 = {
    "stoic_essay_1": {
        "title": "El Arte Estoico de Ser Indestructible (Dicotomía del Control)",
        "desc": "¿Te preocupas por cosas que no puedes cambiar? Los filósofos estoicos descubrieron el secreto absoluto de la ataraxia mental: dividir el mundo entre lo que controlas y lo que no. Domina tu mente y elimina la ansiedad para siempre. #estoicismo #filosofia #ansiedad #autocontrol",
        "thumb": "stoic_screenshot_0.jpg",
        "day": 1
    },
    "stoic_essay_2": {
        "title": "La Ciudadela Interior: Cómo Construir una Mente Inmune a las Ofensas",
        "desc": "Marco Aurelio gobernó el imperio más poderoso de la Tierra mientras lidiaba con pestes, guerras y traiciones. ¿Su secreto? La ciudadela interior. Aprende a proteger tu paz mental frente a insultos, críticas y el caos del día a día. #marcoaurelio #estoicismo #crecimientopersonal #mente",
        "thumb": "stoic_screenshot_1.jpg",
        "day": 3
    },
    "stoic_essay_3": {
        "title": "El Poder de la Templanza: Sabiduría de Séneca y Epicteto",
        "desc": "Séneca fue el hombre más rico de Roma y Epicteto un esclavo cojo. Ambos compartían la misma filosofía de vida: la libertad interior no depende de tus riquezas o estatus, sino de tu autocontrol. Descubre sus enseñanzas clave. #seneca #epicteto #estoicismo #sabiduria #filosofia",
        "thumb": "stoic_screenshot_2.jpg",
        "day": 5
    },
    "kabbalah_essay_1": {
        "title": "El Árbol de la Vida Revelado: Los Secretos Místicos de la Cábala",
        "desc": "¿Qué es el Árbol de la Vida y cómo explica la estructura del universo y de tu propia alma? Descodificamos las 10 Sefirot cósmicas y la luz infinita del Ein Sof en este viaje a través del misticismo ancestral. #cabala #mistica #espiritualidad #universo #zohar",
        "thumb": "kabbalah_screenshot_0.jpg",
        "day": 7
    },
    "kabbalah_essay_2": {
        "title": "El Propósito de tu Alma en la Tierra: El Misterio del Tikún",
        "desc": "Según la cábala, no estás aquí por accidente. Tu alma tiene una misión de corrección llamada Tikún. Descubre cómo identificar tus desafíos kármicos y canalizar la misericordia divina para transformar tu destino. #tikun #karma #espiritualidad #alma #conciencia",
        "thumb": "kabbalah_screenshot_1.jpg",
        "day": 9
    },
    "kabbalah_essay_3": {
        "title": "Los Secretos del Zohar: Rasgando el Velo de la Realidad Oculta",
        "desc": "El Libro del Esplendor (Zohar) guarda las llaves del misticismo hebreo. Exploramos la elevación de la Shejiná (presencia divina), la transmutación del egoísmo y los misterios que escapan a la percepción física. #zohar #mistica #sabiduria #espiritualidad #filosofia",
        "thumb": "kabbalah_screenshot_2.jpg",
        "day": 11
    },
    "humanitas_essay_1": {
        "title": "¿Tiene la IA Alma? El Vaticano y el Futuro de la Humanidad",
        "desc": "Analizamos 'Magnifica Humanitas', la encíclica papal sobre el desarrollo de la Inteligencia Artificial. ¿Qué pasa cuando la tecnología imita la conciencia humana? La advertencia de la Iglesia contra el transhumanismo sin límites éticos. #vaticano #inteligenciaartificial #etica #papa #tecnologia",
        "thumb": "humanitas_screenshot_0.jpg",
        "day": 13
    },
    "humanitas_essay_2": {
        "title": "La Nueva Torre de Babel: El Peligro de la Soberbia Tecnocrática",
        "desc": "La IA avanza a pasos agigantados, pero ¿estamos construyendo una nueva utopía o una celda digital? Usamos la metáfora bíblica de la Torre de Babel para reflexionar sobre la necesidad de edificar una tecnología orientada a la fraternidad. #tecnologia #etica #filosofia #sociedad #ia",
        "thumb": "humanitas_screenshot_1.jpg",
        "day": 15
    },
    "humanitas_essay_3": {
        "title": "Armas Autónomas y Ética Algorítmica: El Límite de la IA",
        "desc": "¿Deben los algoritmos decidir quién vive y quién muere en el campo de batalla? Analizamos el debate global sobre las armas autónomas de la IA, el derecho al trabajo humano digno y la resistencia contra la propaganda algorítmica. #guerra #automatizacion #derechos #paz #inteligenciaartificial",
        "thumb": "humanitas_screenshot_2.jpg",
        "day": 17
    }
}

SHORT_TITLES_C2 = {
    "stoic": [
        "El Secreto Estoico para Eliminar la Ansiedad 🛡",
        "El Arte de Callar para Conservar tu Energía 🤫",
        "Prepárate para lo Peor y serás Invencible ⏳",
        "Ama tu Destino: La Clave para No Sufrir Jamás 👑",
        "Tu Mente es una Vasija: ¿De qué la llenas? 🏺",
        "La Balanza de la Justicia en tu Propia Alma ⚖",
        "La Ciudadela Interior: Tu Refugio Mental 🏰",
        "La Chispa Divina que Habita en tu Interior ✨",
        "El Silencio de Oro: La Sabiduría de No Opinar 🤫",
        "El Obstáculo es el Camino: Crece en la Tempestad ⚔",
        "El Secreto del Tikún: Corrige tu Destino 💎",
        "La Fortaleza Mental de Marco Aurelio 🏛",
        "La Brevedad de la Vida: No Malgastes tu Tiempo ⏳",
        "La Templanza Estoica: Controla tus Deseos ⚖",
        "Tu Libertad Interior Nadie te la Puede Quitar 🔓",
        "El Verdadero Valor del Tiempo en la Tierra ⏳",
        "Tiferet: El Equilibrio del Amor y la Belleza ❤️",
        "La Soberanía de Epicteto: Sé Dueño de Ti Mismo 👑"
    ],
    "kabbalah": [
        "Las 10 Emanaciones de la Energía Divina 🌟",
        "Contracción del Ego: El Vacío Creador 🤫",
        "La Vasija del Dar: El Propósito de Compartir 🏺",
        "La Fuerza de Restricción: Domina tus Impulsos 🛡",
        "Las 10 Sefirot: El Mapa del Universo 🌌",
        "El Reino de Maljut: El Espejo de tus Acciones ☯",
        "El Tikún: Descubre la Misión de tu Alma 💎",
        "Rigor vs Misericordia: El Equilibrio Cósmico ☯",
        "Tiferet: El Corazón del Árbol de la Vida ❤️",
        "Cómo Transmutar tu Destino con la Cábala 🌌",
        "La Fuerza de Gevurá: Disciplina y Límites 🛡",
        "El Poder de la Luz Divina en tu Día a Día ✨",
        "Los Secretos del Zohar Revelados 📖",
        "La Elevación de la Shejiná: Luz en la Oscuridad ✨",
        "Retorno al Infinito: El Ein Sof Revelado 🌌",
        "La Conciencia es un Espejo del Cosmos 🌌",
        "El Arte de Transmutar el Egoísmo Humano 🏺",
        "El Despertar Divino de la Conciencia Interior 🔓"
    ],
    "humanitas": [
        "Dignidad Humana frente a la Inteligencia Artificial 🏛",
        "El Peligro de una IA sin Límites Éticos ⚖",
        "La Trampa del Transhumanismo Tecnológico 🛡",
        "La Chispa Humana que la IA Jamás Podrá Replicar ✨",
        "Bien Común vs El Monopolio del Lucro de la IA 💼",
        "No Adores a la Máquina: El Límite Humano 🔓",
        "La Nueva Torre de Babel: Soberbia de la IA 🗼",
        "Tecnología para la Fraternidad y la Paz Global 🕊",
        "Protección Digital: El Cuidado en la Era Algorítmica 👵",
        "La Soberbia Tecnológica frente al Cosmos 🗼",
        "Edificar con Justicia el Futuro Digital 🕊",
        "IA y el Cuidado de los Sectores Más Débiles 👵",
        "Hacia un Marco Ético Internacional para la IA 🌐",
        "La Prohibición Absoluta de las Armas Autónomas ⚔",
        "El Derecho al Trabajo frente a la Automatización 💼",
        "La Amenaza de la Propaganda Algorítmica Masiva 📰",
        "Defender la Dignidad del Trabajo Humano frente a la IA 💼",
        "Resistencia Digital: Mantén la Antorcha Encendida 🕯"
    ]
}

# ==========================================
# CAMPAIGN 3 UPGRADED SEO METADATA
# ==========================================
WIDESCREEN_METADATA_C3 = {
    "war_myths_essay_1": {
        "title": "Mitos de Guerra: 10 Mentiras del Combate Real que Todos Creen (Parte 1) ⚔",
        "desc": "Desde la música heroica que nunca suena hasta el mito de que siempre ves a quien te dispara. En esta primera parte, analizamos los 10 mitos más de combate real explicados por tácticas e historias militares. \n\n¡Suscríbete para más realismo histórico y militar! #guerra #combate #historia #mitos #militar",
        "thumb": "gates_of_hell_screenshot_0.jpg",
        "day": 1
    },
    "war_myths_essay_2": {
        "title": "Mitos de Guerra: 10 Mentiras del Combate Real que Todos Creen (Parte 2) ⚔",
        "desc": "En esta segunda parte, desmontamos las creencias sobre los drones modernos, la supuesta invulnerabilidad de los blindajes corporales y cómo explotan realmente las granadas. La guerra real no es como en Hollywood. \n\n¡Dale like y suscríbete para más análisis tácticos! #tecnologia #drones #guerra #ejercito #armas",
        "thumb": "gates_of_hell_screenshot_1.jpg",
        "day": 6
    }
}

SHORT_TITLES_C3 = [
    "El Mito de la Música en Combate 🔇",
    "¿Siempre Ves a Tu Enemigo? 👁",
    "El Rango No Equivale a Competencia 🎖",
    "¿Disparan Todo el Tiempo? 🎒",
    "La Guerra No Siempre es Ruidosa 🔇",
    "La Mentira del Control Absoluto 🗺",
    "¿Sientes Cuando te Disparan? 💉",
    "La Memoria Bajo Fuego se Rompe 🧠",
    "Las Milicias Locales No Servirían 🛡",
    "El Soldado Occidental es Superior 🌴",
    "Distinguiendo al Enemigo Real 👥",
    "Los Drones No Son Indestructibles 🛸",
    "Los Pilotos de Drones Están a Salvo 🎯",
    "Los Drones FPV No Reemplazan Todo 🔋",
    "El Trauma No es Igual para Todos 🧠",
    "El Mito del Soldado Rudo 🎖",
    "La Guerra No Tiene Lógica ⚖",
    "Las Granadas No Causan Bolas de Fuego 💥",
    "El Chaleco Antibalas No Te Hace Inmune 🛡",
    "Los Silenciadores No Hacen el Arma Muda 🤫"
]

# ==========================================
# CAMPAIGN 4 UPGRADED SEO METADATA
# ==========================================
WIDESCREEN_METADATA_C4 = {
    "argentina_essay_1": {
        "title": "Por Qué TODOS Odian a ARGENTINA? (Parte 1): La Soberbia y el Éxito Deportivo ⚽",
        "desc": "Desde la etiqueta del 'agrandado' rioplatense hasta el costo mediático de ser el protagonista de la historia. En esta primera parte, analizamos los factores psicológicos y deportivos que alimentan el rechazo hacia la selección argentina. \n\n¡Suscríbete para más debates e historias del fútbol! #argentina #messi #maradona #seleccionargentina #polemica",
        "thumb": "argentina_stadium.jpg",
        "day": 1
    },
    "argentina_essay_2": {
        "title": "Por Qué TODOS Odian a ARGENTINA? (Parte 2): La Sospecha Arbitral y las Polémicas ⚽",
        "desc": "Desmontamos las teorías conspirativas sobre el Mundial de Qatar 2022, las agresivas tácticas psicológicas del Dibu Martínez y la supuesta protección arbitral a Lionel Messi. ¿Favoritismo real o calidad de campeones? \n\n¡Dale like y suscríbete para más análisis futbolísticos! #dibumartinez #qatar2022 #polemica #arbitro #deportes",
        "thumb": "referee_red_card.jpg",
        "day": 6
    },
    "argentina_essay_3": {
        "title": "Por Qué TODOS Odian a ARGENTINA? (Parte 3): Geopolítica, Xenofobia y Redes ⚽",
        "desc": "En esta tercera y última parte, exploramos cómo el fútbol canaliza tensiones geopolíticas reales: desde las Islas Malvinas contra Inglaterra hasta la rivalidad digital tóxica con México y los cánticos polémicos contra Francia. \n\n¡Comenta tu opinión con respeto! #futbol #geopolitica #mexico #francia #polemica #redessociales",
        "thumb": "messi_celebration.jpg",
        "day": 11
    }
}

SHORT_TITLES_C4 = [
    "El Mito del 'Agrandado' Argentino 😤",
    "¿Por Qué Hinchas Cantan Así? 🗣",
    "El Precio de la Gloria Deportiva 🏆",
    "La Pasión que Asusta al Mundo 🔥",
    "El Choque Rioplatense de Voces 🗣",
    "¿Un Mundial Comprado en Qatar? 🇶🇦",
    "El Dibu Martínez: ¿Genio o Loco? 🧤",
    "El Juego Rudo de la Albiceleste ⚔",
    "¿Protege FIFA a Lionel Messi? 🐐",
    "La Honestidad Brutal en Prensa 🎙",
    "Inglaterra vs Argentina: Malvinas 🇬🇧",
    "Brasil vs Argentina: Guerra por Trono 🇧🇷",
    "El Tenso Choque con México 🇲🇽",
    "El Escándalo del Canto a Francia 🇫🇷",
    "El Gran Negocio del Odio Digital 📱",
    "¿Es Odio Real o Solo Folklore? 🎭"
]

def extract_short_text(file_path, key):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split(f"### {key}")
    if len(parts) < 2:
        return ""
    block = parts[1].strip()
    subparts = block.split("---")
    text = subparts[0].strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    return text

def get_schedule_offset(day, hour, minute):
    now = datetime.datetime.now()
    start_date = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    target_time = start_date + datetime.timedelta(days=(day - 1), hours=hour, minutes=minute)
    diff_seconds = (target_time - now).total_seconds()
    return max(0, int(diff_seconds / 60))

def run_youtube_upload(file_path, title, desc, is_short=False, thumbnail_path=None, schedule_offset=0):
    print(f"\n[UPLOAD] Uploading: {title}")
    cmd = [
        "node",
        os.path.join(VAREGO_DIR, "upload_youtube.js"),
        "--file", file_path,
        "--title", title,
        "--desc", desc
    ]
    if is_short:
        cmd.append("--is_short")
    if thumbnail_path:
        cmd.extend(["--thumbnail", thumbnail_path])
    if schedule_offset > 0:
        cmd.extend(["--schedule", str(schedule_offset)])
        
    res = subprocess.run(cmd, cwd=VAREGO_DIR, capture_output=True, text=True, encoding="utf-8")
    
    if res.returncode == 0:
        print(f"[SUCCESS] Upload completed successfully for: {title}")
        return True
    else:
        print(f"[ERROR] Upload failed for: {title}")
        print("Stdout:", res.stdout)
        print("Stderr:", res.stderr)
        return False

def build_queues():
    # --------------------------------------
    # BUILD QUEUE FOR CAMPAIGN 1
    # --------------------------------------
    c1_queue = []
    
    # 1. Widescreen Essays
    essay_days = {"steam": 1, "augusto": 2, "sony": 3, "trajano": 4, "aureliano": 5, "constantino": 6, "mayoriano": 7, "justiniano": 8}
    widescreen_uploads_c1 = [
        {"key": "steam", "file": os.path.join(EXPORTS_DIR, "video_essay_steam", "steam_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_steam", "thumbnail.jpg"), "seo": STEAM_ESSAY_SEO, "day": 1},
        {"key": "augusto", "file": os.path.join(EXPORTS_DIR, "video_essay_augusto", "augusto_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_augusto", "thumbnail.jpg"), "seo": ROMAN_ESSAYS_SEO["augusto"], "day": 2},
        {"key": "sony", "file": os.path.join(EXPORTS_DIR, "video_essay_sony", "sony_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_sony", "thumbnail.jpg"), "seo": SONY_ESSAY_SEO, "day": 3},
        {"key": "trajano", "file": os.path.join(EXPORTS_DIR, "video_essay_trajano", "trajano_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_trajano", "thumbnail.jpg"), "seo": ROMAN_ESSAYS_SEO["trajano"], "day": 4},
        {"key": "aureliano", "file": os.path.join(EXPORTS_DIR, "video_essay_aureliano", "aureliano_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_aureliano", "thumbnail.jpg"), "seo": ROMAN_ESSAYS_SEO["aureliano"], "day": 5},
        {"key": "constantino", "file": os.path.join(EXPORTS_DIR, "video_essay_constantino", "constantino_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_constantino", "thumbnail.jpg"), "seo": ROMAN_ESSAYS_SEO["constantino"], "day": 6},
        {"key": "mayoriano", "file": os.path.join(EXPORTS_DIR, "video_essay_mayoriano", "mayoriano_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_mayoriano", "thumbnail.jpg"), "seo": ROMAN_ESSAYS_SEO["mayoriano"], "day": 7},
        {"key": "justiniano", "file": os.path.join(EXPORTS_DIR, "video_essay_justiniano", "justiniano_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_justiniano", "thumbnail.jpg"), "seo": ROMAN_ESSAYS_SEO["justiniano"], "day": 8}
    ]
    for w in widescreen_uploads_c1:
        c1_queue.append({
            "campaign": 1,
            "file": w["file"],
            "title": w["seo"]["title"],
            "desc": w["seo"]["desc"],
            "is_short": False,
            "thumb": w["thumb"],
            "schedule": (w["day"], 12, 0)
        })
        
    # 2. Extra Roman Shorts
    for emp_key, day_num in essay_days.items():
        if emp_key in ["steam", "sony"]: continue
        for i in range(1, 4):
            short_key = f"roman_extra_{emp_key}_{i}"
            file_path = os.path.join(EXPORTS_DIR, short_key, f"{short_key}_final.mp4")
            seo_data = ROMAN_EXTRA_SHORTS_SEO[short_key]
            c1_queue.append({
                "campaign": 1,
                "file": file_path,
                "title": seo_data[0],
                "desc": seo_data[1],
                "is_short": True,
                "thumb": None,
                "schedule": (day_num, 12 + i, 0)
            })
            
    # 3. General Shorts
    stoic_q = [{"file": os.path.join(EXPORTS_DIR, f"stoic_short_{i}", f"stoic_short_{i}_final.mp4"), "seo": STOIC_SHORTS_SEO[i]} for i in range(1, 6)]
    roman_q = [{"file": os.path.join(EXPORTS_DIR, f"roman_short_{i}", f"roman_short_{i}_final.mp4"), "seo": ROMAN_SHORTS_SEO[i]} for i in range(1, 7)]
    sony_q = [{"file": os.path.join(EXPORTS_DIR, f"sony_short_{i}", f"sony_short_{i}_final.mp4"), "seo": SONY_SHORTS_SEO[i]} for i in range(1, 7)]
    steam_q = [{"file": os.path.join(EXPORTS_DIR, f"steam_short_{i}", f"steam_short_{i}_final.mp4"), "seo": STEAM_SHORTS_SEO[i]} for i in range(1, 7)]
    
    general_shorts = []
    max_len = max(len(stoic_q), len(roman_q), len(sony_q), len(steam_q))
    for step in range(max_len):
        if step < len(stoic_q): general_shorts.append(stoic_q[step])
        if step < len(roman_q): general_shorts.append(roman_q[step])
        if step < len(sony_q): general_shorts.append(sony_q[step])
        if step < len(steam_q): general_shorts.append(steam_q[step])
        
    slots_c1 = []
    for day in range(1, 7):
        slots_c1.append((day, 8, 0))
        slots_c1.append((day, 11, 0))
        slots_c1.append((day, 16, 0))
        slots_c1.append((day, 20, 0))
        
    for idx, short in enumerate(general_shorts):
        if idx >= len(slots_c1): break
        day_num, hr, mins = slots_c1[idx]
        c1_queue.append({
            "campaign": 1,
            "file": short["file"],
            "title": short["seo"]["title"],
            "desc": short["seo"]["desc"],
            "is_short": True,
            "thumb": None,
            "schedule": (day_num, hr, mins)
        })

    # --------------------------------------
    # BUILD QUEUE FOR CAMPAIGN 2 (EXPANSION)
    # --------------------------------------
    c2_queue = []
    slots_c2 = [
        (8, 0),   # 8:00 AM
        (10, 0),  # 10:00 AM
        (14, 0),  # 2:00 PM
        (16, 0),  # 4:00 PM
        (18, 0),  # 6:00 PM
        (20, 0)   # 8:00 PM
    ]
    
    for key, info in WIDESCREEN_METADATA_C2.items():
        file_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        thumb_path = os.path.join(BASE_DIR, "screenshots", info["thumb"])
        
        # Add Essay
        c2_queue.append({
            "campaign": 2,
            "file": file_path,
            "title": info["title"],
            "desc": info["desc"],
            "is_short": False,
            "thumb": thumb_path,
            "schedule": (info["day"], 12, 0) # 12:00 PM
        })
        
        # Add its 6 Complemental Shorts
        match = re.match(r"([a-z]+)_essay_(\d+)", key)
        if match:
            cat = match.group(1)
            e_idx = int(match.group(2))
            for s_idx in range(1, 7):
                short_key = f"{cat}_essay_{e_idx}_short_{s_idx}"
                short_file = os.path.join(BASE_DIR, f"{short_key}_final.mp4")
                desc_text = extract_short_text(file_shorts_c2, short_key)
                t_idx = ((e_idx - 1) * 6 + (s_idx - 1)) % 18
                title_text = SHORT_TITLES_C2[cat][t_idx]
                hr, mins = slots_c2[s_idx - 1]
                
                c2_queue.append({
                    "campaign": 2,
                    "file": short_file,
                    "title": title_text,
                    "desc": desc_text,
                    "is_short": True,
                    "thumb": None,
                    "schedule": (info["day"], hr, mins)
                })
                
    # --------------------------------------
    # BUILD QUEUE FOR CAMPAIGN 3 (MITOS DE GUERRA)
    # --------------------------------------
    c3_queue = []
    
    # Add Widescreen Essays
    for key, info in WIDESCREEN_METADATA_C3.items():
        file_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        thumb_path = os.path.join(BASE_DIR, "screenshots", info["thumb"])
        c3_queue.append({
            "campaign": 3,
            "file": file_path,
            "title": info["title"],
            "desc": info["desc"],
            "is_short": False,
            "thumb": thumb_path,
            "schedule": (info["day"], 12, 0) # 12:00 PM
        })
        
    # Add 20 Shorts (2 per day at 8:00 AM and 4:00 PM)
    for idx in range(20):
        essay_num = 1 if idx < 10 else 2
        short_num = (idx % 10) + 1
        short_key = f"war_myths_essay_{essay_num}_short_{short_num}"
        short_file = os.path.join(BASE_DIR, f"{short_key}_final.mp4")
        desc_text = extract_short_text(file_shorts_c3, short_key)
        title_text = SHORT_TITLES_C3[idx]
        
        # Scheduling
        day_offset = idx // 2
        day_num = day_offset + 1
        hr = 8 if (idx % 2 == 0) else 16
        mins = 0
        
        c3_queue.append({
            "campaign": 3,
            "file": short_file,
            "title": title_text,
            "desc": desc_text,
            "is_short": True,
            "thumb": None,
            "schedule": (day_num, hr, mins)
        })
        
    # --------------------------------------
    # BUILD QUEUE FOR CAMPAIGN 4 (ARGENTINA RIVALRIES)
    # --------------------------------------
    c4_queue = []
    
    # Add Widescreen Essays
    for key, info in WIDESCREEN_METADATA_C4.items():
        file_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        thumb_path = os.path.join(BASE_DIR, "screenshots", info["thumb"])
        c4_queue.append({
            "campaign": 4,
            "file": file_path,
            "title": info["title"],
            "desc": info["desc"],
            "is_short": False,
            "thumb": thumb_path,
            "schedule": (info["day"], 12, 0)
        })
        
    # Add 16 Shorts (2 per day at 8:00 AM and 4:00 PM)
    for idx, title_text in enumerate(SHORT_TITLES_C4):
        essay_num = 1 if idx < 5 else (2 if idx < 10 else 3)
        short_num = (idx % 5) + 1 if idx < 5 else ((idx - 5) % 5 + 1 if idx < 10 else (idx - 10) % 6 + 1)
        short_key = f"argentina_essay_{essay_num}_short_{short_num}"
        short_file = os.path.join(BASE_DIR, f"{short_key}_final.mp4")
        short_desc = extract_short_text(file_shorts_c4, short_key)
        desc_text = f"{short_desc}\n\n#futbol #argentina #shorts #polemica #messi"
        
        # Scheduling
        day_offset = idx // 2
        day_num = day_offset + 1
        hr = 8 if (idx % 2 == 0) else 16
        mins = 0
        
        c4_queue.append({
            "campaign": 4,
            "file": short_file,
            "title": title_text,
            "desc": desc_text,
            "is_short": True,
            "thumb": None,
            "schedule": (day_num, hr, mins)
        })
                
    return c1_queue, c2_queue, c3_queue, c4_queue

def main():
    print("====================================================")
    print("VAREGO UNIFIED INTERLEAVED PIPELINE (CAMPAIGNS 1, 2, 3 & 4)")
    print("====================================================\n")
    
    c1_queue, c2_queue, c3_queue, c4_queue = build_queues()
    last_campaign = None
    
    while True:
        # Load currently uploaded items from logs
        uploaded_c1 = set()
        if os.path.exists(uploaded_file_log_1):
            with open(uploaded_file_log_1, "r", encoding="utf-8") as f:
                uploaded_c1 = set(line.strip() for line in f if line.strip())
                
        uploaded_c2 = set()
        if os.path.exists(uploaded_file_log_2):
            with open(uploaded_file_log_2, "r", encoding="utf-8") as f:
                uploaded_c2 = set(line.strip() for line in f if line.strip())
                
        uploaded_c3 = set()
        if os.path.exists(uploaded_file_log_3):
            with open(uploaded_file_log_3, "r", encoding="utf-8") as f:
                uploaded_c3 = set(line.strip() for line in f if line.strip())
                
        uploaded_c4 = set()
        if os.path.exists(uploaded_file_log_4):
            with open(uploaded_file_log_4, "r", encoding="utf-8") as f:
                uploaded_c4 = set(line.strip() for line in f if line.strip())
                
        # Organize campaign 1 exports
        subprocess.run(["python", os.path.join(BASE_DIR, "organize_exports.py")], cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Filter pending items
        pending = {
            1: [item for item in c1_queue if item["file"] not in uploaded_c1],
            2: [item for item in c2_queue if item["file"] not in uploaded_c2],
            3: [item for item in c3_queue if item["file"] not in uploaded_c3],
            4: [item for item in c4_queue if item["file"] not in uploaded_c4]
        }
        
        print(f"[STATUS] Campaign 1: {len(pending[1])} pending | Campaign 2: {len(pending[2])} pending | Campaign 3: {len(pending[3])} pending | Campaign 4: {len(pending[4])} pending.")
        
        # Select next item based on round-robin ordering & file existence on disk
        next_item = None
        order = [1, 2, 3, 4]
        start_idx = order.index(last_campaign) if last_campaign in order else -1
        
        for offset in range(1, 5):
            candidate = order[(start_idx + offset) % 4]
            if len(pending[candidate]) > 0:
                candidate_item = pending[candidate][0]
                if os.path.exists(candidate_item["file"]):
                    next_item = candidate_item
                    break
                    
        if next_item is None:
            total_pending = sum(len(p) for p in pending.values())
            if total_pending > 0:
                print(f"[INFO] Pending items exist ({total_pending} total), but their video files are not compiled yet. Waiting 60 seconds...")
                time.sleep(60)
                continue
            else:
                print("\n✅ All campaign uploads are successfully completed!")
                break
                
        file_path = next_item["file"]
            
        # Calculate schedule:
        # Campaign 1 -> target_day = day_num (Days 1-10)
        # Campaign 2 -> target_day = day_num + 10 (Days 11-30)
        # Campaign 3 -> target_day = day_num + 30 (Days 31-40) (5-day cycle per essay + shorts)
        # Campaign 4 -> target_day = day_num + 40 (Days 41-50)
        day_num, hr, mins = next_item["schedule"]
        if next_item["campaign"] == 1:
            target_day = day_num
        elif next_item["campaign"] == 2:
            target_day = day_num + 10
        elif next_item["campaign"] == 3:
            target_day = day_num + 30
        else:
            target_day = day_num + 40
            
        schedule_offset = get_schedule_offset(target_day, hr, mins)
        
        print(f"\n[QUEUE] Processing Campaign {next_item['campaign']} (Day {target_day} @ {hr:02d}:{mins:02d})")
        print(f"  File: {file_path}")
        print(f"  Title: {next_item['title']}")
        
        success = run_youtube_upload(
            file_path=file_path,
            title=next_item["title"],
            desc=next_item["desc"],
            is_short=next_item["is_short"],
            thumbnail_path=next_item["thumb"],
            schedule_offset=schedule_offset
        )
        
        if success:
            last_campaign = next_item["campaign"]
            # Register in respective log
            if next_item["campaign"] == 1:
                log_file = uploaded_file_log_1
            elif next_item["campaign"] == 2:
                log_file = uploaded_file_log_2
            elif next_item["campaign"] == 3:
                log_file = uploaded_file_log_3
            else:
                log_file = uploaded_file_log_4
                
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(file_path + "\n")
            print(f"[SUCCESS] Registered upload in Campaign {next_item['campaign']} log.")
        else:
            print(f"[ERROR] Failed to upload: {next_item['title']}. Will retry in next iteration.")
            
        print("[INFO] Waiting 20 seconds before next action...")
        time.sleep(20)

if __name__ == "__main__":
    main()
