import os
import shutil

BASE_DIR = r"C:\Users\jegom\shorts_project"
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
THUMBNAIL_STEAM_SRC = r"C:\Users\jegom\.gemini\antigravity-cli\brain\85ea5793-f40a-4d89-b19b-1234c4ea39cb\thumbnail_steam_essay_1784219779298.jpg"
THUMBNAIL_SONY_SRC = os.path.join(BASE_DIR, "screenshots", "thumbnail_sony_essay.jpg")

SEO_STEAM = """# SEO: ¿Por qué todos demandan a Steam... excepto los jugadores?
## Canal: DOMINUSBABEL (@dominus8735)

### 📌 Títulos A/B:
*   **Opción 1:** ¿Por qué todos odian a Steam... excepto los jugadores?
*   **Opción 2:** La Guerra Oculta Contra Steam: ¿Por qué nadie puede vencer a Gabe Newell?

### 📝 Descripción:
Steam domina el 74% del mercado de PC y factura más de 17.000 millones de dólares al año. Es el rey indiscutible de las computadoras. Sin embargo, detrás de esa fachada de estabilidad, se libra una guerra judicial antitrust sin precedentes.

### ⏱ Marcas de Tiempo:
*   `00:00` - Capítulo 1: El Coloso Silencioso
*   `01:10` - Capítulo 2: El Impuesto Digital (30%)
*   `02:25` - Capítulo 3: La Paridad de Precios
*   `03:45` - Capítulo 4: La Conspiración de Microsoft
*   `05:00` - Capítulo 5: La Amenaza a las Distribuidoras
*   `06:20` - Capítulo 6: El Azote de Epic Games
*   `07:35` - Capítulo 7: El Fracaso de los Gigantes
*   `08:55` - Capítulo 8: El Interés de las Corporaciones
*   `10:15` - Capítulo 9: La Edad de Oro de Valve
*   `11:35` - Capítulo 10: La Estructura de Propiedad Privada
*   `12:55` - Capítulo 11: Políticas Pro-Consumidor
*   `14:15` - Capítulo 12: Compartir en Familia
*   `15:35` - Capítulo 13: Precios Regionales
*   `16:55` - Capítulo 14: La Mística de Gabe Newell
*   `18:15` - Capítulo 15: Conclusión
"""

SEO_SONY = """# SEO: Matar el disco puede ser el peor error de Sony
## Canal: DOMINUSBABEL (@dominus8735)

### 📌 Títulos A/B:
*   **Opción 1:** Matar el disco puede ser el peor error de Sony.
*   **Opción 2:** La Conspiración de PlayStation Contra el Formato Físico.

### 📝 Descripción:
¿Vale la pena comprar una consola digital? Sony ha lanzado la PlayStation 5 Pro por setecientos dólares sin lectora de discos. Esto no es un accidente, es el inicio de la muerte del formato físico.

### ⏱ Marcas de Tiempo:
*   `00:00` - Capítulo 1: El Impuesto del Pro
*   `01:20` - Capítulo 2: El Espejismo de la Propiedad
*   `02:40` - Capítulo 3: La Muerte de la Preservación
*   `04:00` - Capítulo 4: El Monopolio de la Store
*   `05:25` - Capítulo 5: La Resistencia del Disco
"""

ROMAN_ESSAYS_SEO = {
    "augusto": {
        "title": "¿Por qué el primer emperador de Roma se negó a ser llamado rey?",
        "desc": "Octavio Augusto heredó un imperio en ruinas a los 18 años y fundó la Pax Romana sin ceñirse la corona de rey, construyendo una Roma de mármol.\n\n00:00 - El Sucesor Oculto\n01:45 - Las Luces de la Pax Romana\n03:20 - Las Sombras del Actor"
    },
    "trajano": {
        "title": "Trajano: El general hispano que llevó a Roma a su máxima extensión",
        "desc": "Coronado como el mejor emperador (Optimus Princeps), Trajano expandió las fronteras de Roma desde el Rin hasta los desiertos de Partia.\n\n00:00 - El Soldado del Rin\n01:50 - Las Luces del Imperio Máximo\n03:35 - Las Sombras de la Extensión"
    },
    "aureliano": {
        "title": "Aureliano: El soldado humilde que salvó al Imperio de la destrucción",
        "desc": "En solo 5 años de reinado en la Crisis del Siglo III, Aureliano reunificó un imperio fragmentado y levantó las murallas de Roma.\n\n00:00 - El Siglo del Caos\n02:00 - Las Luces del Restaurador\n03:40 - Las Sombras del Autócrata"
    },
    "constantino": {
        "title": "Constantino: El emperador que unió la espada y la cruz",
        "desc": "La visión mística del Puente Milvio, la refundación de Constantinopla y las intrigas palaciegas que cambiaron la religión de Europa.\n\n00:00 - El Puente de la Visión\n02:05 - Las Luces de la Tolerancia\n03:50 - Las Sombras del Palacio"
    },
    "mayoriano": {
        "title": "Mayoriano: El último héroe real del Imperio Romano de Occidente",
        "desc": "El general indomable que reconquistó Galia e Hispania y construyó una flota legendaria antes de ser traicionado por Ricimero.\n\n00:00 - El Crepúsculo de Occidente\n01:55 - Las Luces de la Reconquista\n03:40 - Las Sombras de la Traición"
    },
    "justiniano": {
        "title": "Justiniano: El adicto al trabajo que resucitó la gloria de Roma",
        "desc": "Las conquistas de Belisario, el Corpus Juris Civilis y las tragedias de las revueltas de Nika y la peste bubónica en Constantinopla.\n\n00:00 - El Campesino que no Dormía\n02:10 - Las Luces del Derecho\n03:55 - Las Sombras de Nika"
    }
}

STOIC_SHORTS_SEO = {
    1: ("El secreto de la paz mental que los estoicos y la cábala comparten 🛡", "La dicotomía del control estoica y el concepto de la vasija (Kli). #estoicismo #cabala #shorts"),
    2: ("Construye una mente indestructible con este secreto ancestral 🏛", "La 'ciudadela interior' estoica y la chispa divina (Shejiná). #sabiduria #shorts"),
    3: ("El poder oculto de callar cuando te insultan (Tzimtzum) 🤫", "Callar no es debilidad. Es contraer tu ego (Tzimtzum) para dar espacio a la templanza. #autocontrol #shorts"),
    4: ("Por qué deberías amar tu destino (Incluso cuando todo sale mal) 👑", "Aceptar tu destino (Amor Fati) te alinea con la voluntad superior (Keter). #amorfati #shorts"),
    5: ("Agradece tus problemas: el crisol que esculpe tu alma 💎", "Las dificultades no son obstáculos, son los golpes de cincel que crean belleza moral (Tiferet). #resiliencia #shorts")
}

ROMAN_SHORTS_SEO = {
    1: ("El hombre que rechazó el título de Rey para reinar sobre Roma 🏛", "Augusto fundó la Pax Romana y reconstruyó Roma sin corona de rey. #historia #roma #shorts"),
    2: ("El emperador más exitoso que Roma jamás conoció (Trajano) ⚔", "Trajano llevó al Imperio a su máxima extensión militar y fue coronado Optimus Princeps. #historia #shorts"),
    3: ("Aureliano: El soldado humilde que salvó a Roma del colapso 🛡", "Aureliano reunificó el imperio dividido en 5 años de reinado militar. #historia #aureliano #shorts"),
    4: ("Constantino y la visión mística que cambió la historia del mundo ✝", "La visión del Puente Milvio que llevó a Constantino a tolerar el cristianismo. #constantino #shorts"),
    5: ("Mayoriano: El último héroe real del Imperio Romano de Occidente 🕯", "Mayoriano luchó heroicamente en el frente y reformó leyes para salvar a Roma. #historia #shorts"),
    6: ("El emperador que resucitó la gloria de Roma desde las cenizas 📜", "Justiniano reconquistó las provincias occidentales perdidas y codificó las leyes. #justiniano #shorts")
}

SONY_SHORTS_SEO = {
    1: ("El impuesto oculto de la PS5 Pro de Sony 🎮", "$700 por una consola sin lectora de discos. La trampa para obligarte al formato digital. #playstation #shorts"),
    2: ("Por qué no eres dueño de tus juegos digitales ⚖", "Sony borró de las bibliotecas contenidos de Discovery comprados por usuarios. Comprar digital es rentar. #derechos #shorts"),
    3: ("La demo legendaria de Silent Hills que desapareció para siempre 🏛", "P.T. de Hideo Kojima fue borrado de PlayStation Network. Sin disco, el arte puede eliminarse. #silenthills #shorts"),
    4: ("La trampa detrás de la eliminación del lector de discos 💸", "Sin lector físico, la PlayStation Store tiene el monopolio. Adiós al mercado de juegos usados. #monopolio #shorts"),
    5: ("Pagaron $70 por un juego que ya no existe (The Crew) 💥", "Ubisoft cerró los servidores de The Crew, convirtiendo un juego de carreras en inservible. #estafa #shorts"),
    6: ("Por qué comprar juegos en formato físico es defender tus derechos 👑", "El disco físico es tu única garantía de propiedad privada offline y de preservación histórica. #formatofisico #shorts")
}

STEAM_SHORTS_SEO = {
    1: ("El monopolio más querido y defendido de la historia 🌐", "Valve domina el 74% de las ventas en PC, pero la comunidad defiende al gigante de los juicios. #steam #shorts"),
    2: ("El impuesto del 30% que cobran Valve y Apple en sus tiendas 💸", "La comisión del 30% de Steam y Apple comparada con el 12% de Epic Store. El núcleo de las demandas. #comisiones #shorts"),
    3: ("La cláusula secreta de Valve para mantener sus precios altos ⚖", "Las demandas antitrust acusan a Valve de obligar a no vender más barato en otras tiendas de PC. #precios #shorts"),
    4: ("Los correos secretos de Microsoft que delatan a Steam 💼", "Correos confidenciales revelados en juicio muestran cómo Valve exige la paridad de precios verbalmente. #filtraciones #shorts"),
    5: ("El soporte al usuario que convirtió a Valve en un gigante intocable 🔄", "Reembolsos en menos de dos horas y garantías completas de hardware. Buen servicio al consumidor. #reembolsos #shorts"),
    6: ("El superpoder de Gabe Newell para proteger a los videojugadores 👑", "Al no cotizar en bolsa, Valve no tiene que rendir cuentas a accionistas avariciosos. Libertad total. #gabenewell #shorts")
}

ROMAN_EXTRA_SHORTS_SEO = {
    # Augusto
    "roman_extra_augusto_1": ("EL FIN DE CLEOPATRA ⚔", "La batalla de Actio y el trágico desenlace de Cleopatra y Marco Antonio. #augusto #historia #shorts"),
    "roman_extra_augusto_2": ("LA HIJA EXILIADA 🏛", "Julia la Mayor, desterrada de por vida por desafiar las leyes morales de Augusto. #historia #shorts"),
    "roman_extra_augusto_3": ("LEGIONES PERDIDAS 🌲", "La emboscada mortal en el bosque de Teutoburgo y la locura de Augusto. #tragedia #shorts"),
    # Trajano
    "roman_extra_trajano_1": ("EL FIN DE DECÉBALO ⚔", "El cruce del Danubio y el suicidio del rey bábaro para no ser capturado. #trajano #guerra #shorts"),
    "roman_extra_trajano_2": ("LA CAÍDA DE TRAJANO 💀", "El derrame cerebral del mejor emperador de Roma en medio de revueltas en Oriente. #historia #shorts"),
    "roman_extra_trajano_3": ("EL BOTÍN DE ORO 🏆", "El tesoro oculto de Dacia de 165 toneladas de oro que financió a Roma. #riqueza #shorts"),
    # Aureliano
    "roman_extra_aureliano_1": ("LA REINA CAPTURADA 👑", "El asedio de Palmira y la captura de Zenobia con cadenas de oro puro. #aureliano #historia #shorts"),
    "roman_extra_aureliano_2": ("ASESINATO A TRAICIÓN ☠", "La conspiración de la lista falsa que acabó con la vida de Aureliano. #complot #shorts"),
    "roman_extra_aureliano_3": ("LA MASACRE DE LA CECA 💥", "La rebelión violenta de los trabajadores de la ceca aplastada sin piedad. #historia #shorts"),
    # Constantino
    "roman_extra_constantino_1": ("EL MONOGRAMA CELESTE ✝", "La cruz de fuego en el cielo y la victoria de Constantino en Puente Milvio. #constantino #shorts"),
    "roman_extra_constantino_2": ("EL HIJO EJECUTADO 💔", "El misterio detrás de la ejecución secreta de Crispo por orden de Constantino. #tragedia #shorts"),
    "roman_extra_constantino_3": ("LA EMERATRIZ AHOGADA 🏛", "La muerte de Fausta en los baños calientes y su damnatio memoriae. #constantino #shorts"),
    # Mayoriano
    "roman_extra_mayoriano_1": ("LA ÚLTIMA RECONQUISTA 🛡", "La campaña invernal relámpago de Mayoriano sobre Galia e Hispania. #historia #shorts"),
    "roman_extra_mayoriano_2": ("LA FLOTA TRAICIONADA ⚓", "La armada romana de 300 barcos quemada por traición en Alicante. #tragedia #shorts"),
    "roman_extra_mayoriano_3": ("EL FIN DEL HÉROE ☠", "Tortura y decapitación del último héroe militar de Occidente por Ricimero. #historia #shorts"),
    # Justiniano
    "roman_extra_justiniano_1": ("LA VENGANZA DE ROMA ⚔", "La reconquista de Cartago en semanas por el brillante general Belisario. #historia #shorts"),
    "roman_extra_justiniano_2": ("MASACRE DE NIKA 💀", "La matanza de 30,000 ciudadanos en el Hipódromo para salvar el trono. #tragedia #shorts"),
    "roman_extra_justiniano_3": ("LA EMPERATRIZ DE HIERRO 👑", "Teodora: la actriz de los bajos fondos que gobernó el Imperio Bizantino. #teodora #shorts")
}

def write_seo_file(folder, title, desc, tags=None):
    seo_file = os.path.join(folder, "seo.md")
    with open(seo_file, "w", encoding="utf-8") as f:
        f.write(f"# Título Propuesto:\n{title}\n\n")
        f.write(f"# Descripción:\n{desc}\n")
        if tags:
            f.write(f"\n# Etiquetas:\n{tags}\n")

def main():
    print("====================================================")
    print("ORGANIZING EXPORTS DIRECTORY STRUCTURE")
    print("====================================================")
    
    os.makedirs(EXPORTS_DIR, exist_ok=True)
    
    # 1. Widescreen Steam video essay
    steam_folder = os.path.join(EXPORTS_DIR, "video_essay_steam")
    os.makedirs(steam_folder, exist_ok=True)
    video_steam_src = os.path.join(BASE_DIR, "steam_essay_final.mp4")
    if os.path.exists(video_steam_src):
        shutil.copy(video_steam_src, os.path.join(steam_folder, "steam_essay_final.mp4"))
        print("Copied Steam video essay to exports/video_essay_steam/")
    with open(os.path.join(steam_folder, "seo.md"), "w", encoding="utf-8") as f:
        f.write(SEO_STEAM)
    if os.path.exists(THUMBNAIL_STEAM_SRC):
        shutil.copy(THUMBNAIL_STEAM_SRC, os.path.join(steam_folder, "thumbnail.jpg"))
        print("Copied Steam thumbnail to exports/video_essay_steam/")

    # 2. Widescreen Sony video essay
    sony_folder = os.path.join(EXPORTS_DIR, "video_essay_sony")
    os.makedirs(sony_folder, exist_ok=True)
    video_sony_src = os.path.join(BASE_DIR, "sony_essay_final.mp4")
    if os.path.exists(video_sony_src):
        shutil.copy(video_sony_src, os.path.join(sony_folder, "sony_essay_final.mp4"))
        print("Copied Sony video essay to exports/video_essay_sony/")
    with open(os.path.join(sony_folder, "seo.md"), "w", encoding="utf-8") as f:
        f.write(SEO_SONY)
    if os.path.exists(THUMBNAIL_SONY_SRC):
        shutil.copy(THUMBNAIL_SONY_SRC, os.path.join(sony_folder, "thumbnail.jpg"))
        print("Copied Sony thumbnail to exports/video_essay_sony/")

    # 3. Widescreen Roman video essays (Augusto to Justiniano)
    for emp_key, seo_data in ROMAN_ESSAYS_SEO.items():
        folder_name = f"video_essay_{emp_key}"
        emp_folder = os.path.join(EXPORTS_DIR, folder_name)
        os.makedirs(emp_folder, exist_ok=True)
        
        video_src = os.path.join(BASE_DIR, f"{emp_key}_essay_final.mp4")
        if os.path.exists(video_src):
            shutil.copy(video_src, os.path.join(emp_folder, f"{emp_key}_essay_final.mp4"))
            print(f"Copied Roman video essay to exports/{folder_name}/")
            
        write_seo_file(emp_folder, seo_data["title"], seo_data["desc"], "historia, roma, emperadores, imperioromano, videoensayo")
        
        thumb_src = os.path.join(BASE_DIR, "screenshots", f"thumbnail_{emp_key}_essay.jpg")
        if os.path.exists(thumb_src):
            shutil.copy(thumb_src, os.path.join(emp_folder, "thumbnail.jpg"))
            print(f"Copied thumbnail to exports/{folder_name}/")
        
    # 4. Stoic Shorts
    for i in range(1, 6):
        folder = os.path.join(EXPORTS_DIR, f"stoic_short_{i}")
        os.makedirs(folder, exist_ok=True)
        short_video_src = os.path.join(BASE_DIR, f"stoic_short_{i}_final.mp4")
        if os.path.exists(short_video_src):
            shutil.copy(short_video_src, os.path.join(folder, f"stoic_short_{i}_final.mp4"))
            print(f"Copied stoic_short_{i}_final.mp4 to exports/stoic_short_{i}/")
        title, desc = STOIC_SHORTS_SEO[i]
        write_seo_file(folder, title, desc, "estoicismo, cabala, mente, sabiduria, shorts")
        
    # 5. Roman Shorts
    for i in range(1, 7):
        folder = os.path.join(EXPORTS_DIR, f"roman_short_{i}")
        os.makedirs(folder, exist_ok=True)
        short_video_src = os.path.join(BASE_DIR, f"roman_short_{i}_final.mp4")
        if os.path.exists(short_video_src):
            shutil.copy(short_video_src, os.path.join(folder, f"roman_short_{i}_final.mp4"))
            print(f"Copied roman_short_{i}_final.mp4 to exports/roman_short_{i}/")
        title, desc = ROMAN_SHORTS_SEO[i]
        write_seo_file(folder, title, desc, "historia, roma, emperadores, imperioromano, shorts")

    # 6. Sony Shorts
    for i in range(1, 7):
        folder = os.path.join(EXPORTS_DIR, f"sony_short_{i}")
        os.makedirs(folder, exist_ok=True)
        short_video_src = os.path.join(BASE_DIR, f"sony_short_{i}_final.mp4")
        if os.path.exists(short_video_src):
            shutil.copy(short_video_src, os.path.join(folder, f"sony_short_{i}_final.mp4"))
            print(f"Copied sony_short_{i}_final.mp4 to exports/sony_short_{i}/")
        title, desc = SONY_SHORTS_SEO[i]
        write_seo_file(folder, title, desc, "playstation, sony, formatofisico, reventa, coleccionismo, shorts")

    # 7. Steam Shorts
    for i in range(1, 7):
        folder = os.path.join(EXPORTS_DIR, f"steam_short_{i}")
        os.makedirs(folder, exist_ok=True)
        short_video_src = os.path.join(BASE_DIR, f"steam_short_{i}_final.mp4")
        if os.path.exists(short_video_src):
            shutil.copy(short_video_src, os.path.join(folder, f"steam_short_{i}_final.mp4"))
            print(f"Copied steam_short_{i}_final.mp4 to exports/steam_short_{i}/")
        title, desc = STEAM_SHORTS_SEO[i]
        write_seo_file(folder, title, desc, "steam, valve, gabenewell, monopolio, pcgaming, shorts")

    # 8. Extra Roman Shorts (18 files)
    for key, seo_data in ROMAN_EXTRA_SHORTS_SEO.items():
        folder = os.path.join(EXPORTS_DIR, key)
        os.makedirs(folder, exist_ok=True)
        short_video_src = os.path.join(BASE_DIR, f"{key}_final.mp4")
        if os.path.exists(short_video_src):
            shutil.copy(short_video_src, os.path.join(folder, f"{key}_final.mp4"))
            print(f"Copied extra Short to exports/{key}/")
        title, desc = seo_data
        write_seo_file(folder, title, desc, "historia, roma, emperadores, imperioromano, leyendas, shorts")
        
    print("\n====================================================")
    print("EXPORTS ORGANIZATION COMPLETE")
    print("====================================================")

if __name__ == "__main__":
    main()
