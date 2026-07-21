import os
import sys
import time
import datetime
import subprocess

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
VAREGO_DIR = r"C:\Users\jegom\VAREGO"

# 49 Required Video Files
REQUIRED_FILES = [
    # Widescreen Essays (8)
    os.path.join(BASE_DIR, "steam_essay_final.mp4"),
    os.path.join(BASE_DIR, "sony_essay_final.mp4"),
    os.path.join(BASE_DIR, "augusto_essay_final.mp4"),
    os.path.join(BASE_DIR, "trajano_essay_final.mp4"),
    os.path.join(BASE_DIR, "aureliano_essay_final.mp4"),
    os.path.join(BASE_DIR, "constantino_essay_final.mp4"),
    os.path.join(BASE_DIR, "mayoriano_essay_final.mp4"),
    os.path.join(BASE_DIR, "justiniano_essay_final.mp4"),
    
    # General Shorts (23)
    os.path.join(BASE_DIR, "stoic_short_1_final.mp4"),
    os.path.join(BASE_DIR, "stoic_short_2_final.mp4"),
    os.path.join(BASE_DIR, "stoic_short_3_final.mp4"),
    os.path.join(BASE_DIR, "stoic_short_4_final.mp4"),
    os.path.join(BASE_DIR, "stoic_short_5_final.mp4"),
    os.path.join(BASE_DIR, "roman_short_1_final.mp4"),
    os.path.join(BASE_DIR, "roman_short_2_final.mp4"),
    os.path.join(BASE_DIR, "roman_short_3_final.mp4"),
    os.path.join(BASE_DIR, "roman_short_4_final.mp4"),
    os.path.join(BASE_DIR, "roman_short_5_final.mp4"),
    os.path.join(BASE_DIR, "roman_short_6_final.mp4"),
    os.path.join(BASE_DIR, "sony_short_1_final.mp4"),
    os.path.join(BASE_DIR, "sony_short_2_final.mp4"),
    os.path.join(BASE_DIR, "sony_short_3_final.mp4"),
    os.path.join(BASE_DIR, "sony_short_4_final.mp4"),
    os.path.join(BASE_DIR, "sony_short_5_final.mp4"),
    os.path.join(BASE_DIR, "sony_short_6_final.mp4"),
    os.path.join(BASE_DIR, "steam_short_1_final.mp4"),
    os.path.join(BASE_DIR, "steam_short_2_final.mp4"),
    os.path.join(BASE_DIR, "steam_short_3_final.mp4"),
    os.path.join(BASE_DIR, "steam_short_4_final.mp4"),
    os.path.join(BASE_DIR, "steam_short_5_final.mp4"),
    os.path.join(BASE_DIR, "steam_short_6_final.mp4")
]

# Add the 18 Roman Extra Shorts
for emp in ["augusto", "trajano", "aureliano", "constantino", "mayoriano", "justiniano"]:
    for i in range(1, 4):
        REQUIRED_FILES.append(os.path.join(BASE_DIR, f"roman_extra_{emp}_{i}_final.mp4"))

# SEO metadata for video essays
STEAM_ESSAY_SEO = {
    "title": "¿Por qué todos odian a Steam... excepto los jugadores?",
    "desc": "Steam domina el 74% del PC gaming. ¿Por qué es el monopolio más querido por sus usuarios? #steam #valve #pcgaming"
}

SONY_ESSAY_SEO = {
    "title": "Matar el disco puede ser el peor error de Sony",
    "desc": "La PS5 Pro sin lector de discos inicia el fin de la propiedad de tus videojuegos. ¿Por qué el formato físico es vital? #sony #playstation #formatofisico #gaming"
}

ROMAN_ESSAYS_SEO = {
    "augusto": {
        "title": "¿Por qué el primer emperador de Roma se negó a ser llamado rey?",
        "desc": "Octavio Augusto heredó un imperio en ruinas a los 18 años y fundó la Pax Romana sin ceñirse la corona de rey. #historia #roma #imperioromano"
    },
    "trajano": {
        "title": "Trajano: El general hispano que llevó a Roma a su máxima extensión",
        "desc": "Coronado como el mejor emperador (Optimus Princeps), Trajano expandió las fronteras de Roma desde el Rin hasta Partia. #trajano #roma #militar"
    },
    "aureliano": {
        "title": "Aureliano: El soldado humilde que salvó al Imperio de la destrucción",
        "desc": "En solo 5 años de reinado en la Crisis del Siglo III, Aureliano reunificó un imperio fragmentado. #aureliano #roma #imperioromano"
    },
    "constantino": {
        "title": "Constantino: El emperador que unió la espada y la cruz",
        "desc": "La visión mística del Puente Milvio, la refundación de Constantinopla y las intrigas palaciegas que cambiaron la religión de Europa. #constantino #fe #historia"
    },
    "mayoriano": {
        "title": "Mayoriano: El último héroe real del Imperio Romano de Occidente",
        "desc": "El general indomable que reconquistó Galia e Hispania y construyó una flota legendaria antes de ser traicionado por Ricimero. #mayoriano #roma #historia"
    },
    "justiniano": {
        "title": "Justiniano: El adicto al trabajo que resucitó la gloria de Roma",
        "desc": "Las conquistas de Belisario, el Corpus Juris Civilis y las tragedias de las revueltas de Nika y la peste bubónica en Constantinopla. #justiniano #leyes #imperiobizantino"
    }
}

# SEO metadata for general Shorts
STOIC_SHORTS_SEO = {
    1: {"title": "El secreto de la paz mental que los estoicos y la cábala comparten 🛡", "desc": "La dicotomía del control estoica y el concepto de la vasija (Kli). #estoicismo #cabala #shorts"},
    2: {"title": "Construye una mente indestructible con este secreto ancestral 🏛", "desc": "La 'ciudadela interior' estoica y la chispa divina (Shejiná). #sabiduria #shorts"},
    3: {"title": "El poder oculto de callar cuando te insultan (Tzimtzum) 🤫", "desc": "Callar no es debilidad. Es contraer tu ego (Tzimtzum) para dar espacio a la templanza. #autocontrol #shorts"},
    4: {"title": "Por qué deberías amar tu destino (Incluso cuando todo sale mal) 👑", "desc": "Aceptar tu destino (Amor Fati) te alinea con la voluntad superior (Keter). #amorfati #shorts"},
    5: {"title": "Agradece tus problemas: el crisol que esculpe tu alma 💎", "desc": "Las dificultades no son obstáculos, son los golpes de cincel que crean belleza moral (Tiferet). #resiliencia #shorts"}
}

ROMAN_SHORTS_SEO = {
    1: {"title": "El hombre que rechazó el título de Rey para reinar sobre Roma 🏛", "desc": "Augusto fundó la Pax Romana y reconstruyó Roma sin corona de rey. #historia #roma #shorts"},
    2: {"title": "El emperador más exitoso que Roma jamás conoció (Trajano) ⚔", "desc": "Trajano llevó al Imperio a su máxima extensión militar y fue coronado Optimus Princeps. #historia #shorts"},
    3: {"title": "Aureliano: El soldado humilde que salvó a Roma del colapso 🛡", "desc": "Aureliano reunificó el imperio dividido en 5 años de reinado militar. #historia #aureliano #shorts"},
    4: {"title": "Constantino y la visión mística que cambió la historia del mundo ✝", "desc": "La visión del Puente Milvio que llevó a Constantino a tolerar el cristianismo. #constantino #shorts"},
    5: {"title": "Mayoriano: El último héroe real del Imperio Romano de Occidente 🕯", "desc": "Mayoriano luchó heroicamente en el frente y reformó leyes para salvar a Roma. #historia #shorts"},
    6: {"title": "El emperador que resucitó la gloria de Roma desde las cenizas 📜", "desc": "Justiniano reconquistó las provincias occidentales perdidas y codificó las leyes. #justiniano #shorts"}
}

SONY_SHORTS_SEO = {
    1: {"title": "El impuesto oculto de la PS5 Pro de Sony 🎮", "desc": "$700 por una consola sin lectora de discos. La trampa para obligarte al formato digital. #playstation #shorts"},
    2: {"title": "Por qué no eres dueño de tus juegos digitales ⚖", "desc": "Sony borró de las bibliotecas contenidos de Discovery comprados por usuarios. Comprar digital es rentar. #derechos #shorts"},
    3: {"title": "La demo legendaria de Silent Hills que desapareció para siempre 🏛", "desc": "P.T. de Hideo Kojima fue borrado de PlayStation Network. Sin disco, el arte puede eliminarse. #silenthills #shorts"},
    4: {"title": "La trampa detrás de la eliminación del lector de discos 💸", "desc": "Sin lector físico, la PlayStation Store tiene el monopolio. Adiós al mercado de juegos usados. #monopolio #shorts"},
    5: {"title": "Pagaron $70 por un juego que ya no existe (The Crew) 💥", "desc": "Ubisoft cerró los servidores de The Crew, convirtiendo un juego de carreras en inservible. #estafa #shorts"},
    6: {"title": "Por qué comprar juegos en formato físico es defender tus derechos 👑", "desc": "El disco físico es tu única garantía de propiedad privada offline y de preservación histórica. #formatofisico #shorts"}
}

STEAM_SHORTS_SEO = {
    1: {"title": "El monopolio más querido y defendido de la historia 🌐", "desc": "Valve domina el 74% de las ventas en PC, pero la comunidad defiende al gigante de los juicios. #steam #shorts"},
    2: {"title": "El impuesto del 30% que cobran Valve y Apple en sus tiendas 💸", "desc": "La comisión del 30% de Steam y Apple comparada con el 12% de Epic Store. El núcleo de las demandas. #comisiones #shorts"},
    3: {"title": "La cláusula secreta de Valve para mantener sus precios altos ⚖", "desc": "Las demandas antitrust acusan a Valve de obligar a no vender más barato en otras tiendas de PC. #precios #shorts"},
    4: {"title": "Los correos secretos de Microsoft que delatan a Steam 💼", "desc": "Correos confidenciales revelados en juicio muestran cómo Valve exige la paridad de precios verbalmente. #filtraciones #shorts"},
    5: {"title": "El soporte al usuario que convirtió a Valve en un gigante intocable 🔄", "desc": "Reembolsos en menos de dos horas y garantías completas de hardware. Buen servicio al consumidor. #reembolsos #shorts"},
    6: {"title": "El superpoder de Gabe Newell para proteger a los videojugadores 👑", "desc": "Al no cotizar en bolsa, Valve no tiene que rendir cuentas a accionistas avariciosos. Libertad total. #gabenewell #shorts"}
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

def get_schedule_offset(day, hour, minute):
    # Base baseline: Tomorrow morning at 00:00
    now = datetime.datetime.now()
    start_date = (now + datetime.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    target_time = start_date + datetime.timedelta(days=(day - 1), hours=hour, minutes=minute)
    diff_seconds = (target_time - now).total_seconds()
    return max(0, int(diff_seconds / 60))

def check_compilation_ready():
    sizes_before = {}
    for f in REQUIRED_FILES:
        if not os.path.exists(f):
            return False
        sizes_before[f] = os.path.getsize(f)
        if sizes_before[f] < 1000000: # Files must be at least 1MB
            return False
            
    time.sleep(3)
    for f in REQUIRED_FILES:
        if os.path.getsize(f) != sizes_before[f]:
            return False
    return True

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

def main():
    print("====================================================")
    print("VAREGO HIGH-VELOCITY DYNAMIC PIPELINE (10 DAYS)")
    print("====================================================")
    
    uploaded_file_log = os.path.join(BASE_DIR, "uploaded_campaign_1.txt")
    
    essay_days = {
        "steam": 1,
        "augusto": 2,
        "sony": 3,
        "trajano": 4,
        "aureliano": 5,
        "constantino": 6,
        "mayoriano": 7,
        "justiniano": 8
    }
    
    widescreen_uploads = [
        {"key": "steam", "file": os.path.join(EXPORTS_DIR, "video_essay_steam", "steam_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_steam", "thumbnail.jpg"), "title": STEAM_ESSAY_SEO["title"], "desc": STEAM_ESSAY_SEO["desc"], "day": 1},
        {"key": "augusto", "file": os.path.join(EXPORTS_DIR, "video_essay_augusto", "augusto_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_augusto", "thumbnail.jpg"), "title": ROMAN_ESSAYS_SEO["augusto"]["title"], "desc": ROMAN_ESSAYS_SEO["augusto"]["desc"], "day": 2},
        {"key": "sony", "file": os.path.join(EXPORTS_DIR, "video_essay_sony", "sony_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_sony", "thumbnail.jpg"), "title": SONY_ESSAY_SEO["title"], "desc": SONY_ESSAY_SEO["desc"], "day": 3},
        {"key": "trajano", "file": os.path.join(EXPORTS_DIR, "video_essay_trajano", "trajano_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_trajano", "thumbnail.jpg"), "title": ROMAN_ESSAYS_SEO["trajano"]["title"], "desc": ROMAN_ESSAYS_SEO["trajano"]["desc"], "day": 4},
        {"key": "aureliano", "file": os.path.join(EXPORTS_DIR, "video_essay_aureliano", "aureliano_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_aureliano", "thumbnail.jpg"), "title": ROMAN_ESSAYS_SEO["aureliano"]["title"], "desc": ROMAN_ESSAYS_SEO["aureliano"]["desc"], "day": 5},
        {"key": "constantino", "file": os.path.join(EXPORTS_DIR, "video_essay_constantino", "constantino_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_constantino", "thumbnail.jpg"), "title": ROMAN_ESSAYS_SEO["constantino"]["title"], "desc": ROMAN_ESSAYS_SEO["constantino"]["desc"], "day": 6},
        {"key": "mayoriano", "file": os.path.join(EXPORTS_DIR, "video_essay_mayoriano", "mayoriano_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_mayoriano", "thumbnail.jpg"), "title": ROMAN_ESSAYS_SEO["mayoriano"]["title"], "desc": ROMAN_ESSAYS_SEO["mayoriano"]["desc"], "day": 7},
        {"key": "justiniano", "file": os.path.join(EXPORTS_DIR, "video_essay_justiniano", "justiniano_essay_final.mp4"), "thumb": os.path.join(EXPORTS_DIR, "video_essay_justiniano", "thumbnail.jpg"), "title": ROMAN_ESSAYS_SEO["justiniano"]["title"], "desc": ROMAN_ESSAYS_SEO["justiniano"]["desc"], "day": 8}
    ]
    
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
            
    slots = []
    for day in range(1, 7):
        slots.append((day, 8, 0))
        slots.append((day, 11, 0))
        slots.append((day, 16, 0))
        slots.append((day, 20, 0))
        
    while True:
        uploaded_set = set()
        if os.path.exists(uploaded_file_log):
            with open(uploaded_file_log, "r", encoding="utf-8") as f:
                uploaded_set = set(line.strip() for line in f if line.strip())
                
        subprocess.run(["python", os.path.join(BASE_DIR, "organize_exports.py")], cwd=BASE_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        pending_uploads = 0
        
        for essay in widescreen_uploads:
            if essay["file"] in uploaded_set: continue
            if not os.path.exists(essay["file"]):
                pending_uploads += 1
                continue
            schedule_offset = get_schedule_offset(essay["day"], 12, 0)
            print(f"Uploading Widescreen: '{essay['title']}'...")
            success = run_youtube_upload(essay["file"], essay["title"], essay["desc"], is_short=False, thumbnail_path=essay["thumb"], schedule_offset=schedule_offset)
            if success:
                uploaded_set.add(essay["file"])
                with open(uploaded_file_log, "a", encoding="utf-8") as f: f.write(essay["file"] + "\n")
            else: pending_uploads += 1
            time.sleep(10)
            
        for emp_key, day_num in essay_days.items():
            if emp_key in ["steam", "sony"]: continue
            for i in range(1, 4):
                short_key = f"roman_extra_{emp_key}_{i}"
                file_path = os.path.join(EXPORTS_DIR, short_key, f"{short_key}_final.mp4")
                if file_path in uploaded_set: continue
                if not os.path.exists(file_path):
                    pending_uploads += 1
                    continue
                seo_data = ROMAN_EXTRA_SHORTS_SEO[short_key]
                schedule_offset = get_schedule_offset(day_num, 12 + i, 0)
                print(f"Uploading Extra Short: '{seo_data[0]}'...")
                success = run_youtube_upload(file_path, seo_data[0], seo_data[1], is_short=True, schedule_offset=schedule_offset)
                if success:
                    uploaded_set.add(file_path)
                    with open(uploaded_file_log, "a", encoding="utf-8") as f: f.write(file_path + "\n")
                else: pending_uploads += 1
                time.sleep(10)
                
        for idx, short in enumerate(general_shorts):
            if idx >= len(slots): break
            file_path = short["file"]
            if file_path in uploaded_set: continue
            if not os.path.exists(file_path):
                pending_uploads += 1
                continue
            day_num, hr, mins = slots[idx]
            schedule_offset = get_schedule_offset(day_num, hr, mins)
            print(f"Uploading General Short: '{short['seo']['title']}'...")
            success = run_youtube_upload(file_path, short['seo']['title'], short['seo']['desc'], is_short=True, schedule_offset=schedule_offset)
            if success:
                uploaded_set.add(file_path)
                with open(uploaded_file_log, "a", encoding="utf-8") as f: f.write(file_path + "\n")
            else: pending_uploads += 1
            time.sleep(10)
            
        if pending_uploads == 0:
            print("\nAll 49 files for Campaign 1 uploaded successfully!")
            break
            
        print(f"\n[INFO] Campaign 1 loop finished. {pending_uploads} files still pending. Sleeping for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    main()
