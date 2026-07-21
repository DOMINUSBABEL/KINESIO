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
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
VAREGO_DIR = r"C:\Users\jegom\VAREGO"

# Define the 63 required video files for the expansion
REQUIRED_FILES = []

# Widescreen Essays (9)
essay_keys = [
    "stoic_essay_1", "stoic_essay_2", "stoic_essay_3",
    "kabbalah_essay_1", "kabbalah_essay_2", "kabbalah_essay_3",
    "humanitas_essay_1", "humanitas_essay_2", "humanitas_essay_3"
]
for k in essay_keys:
    REQUIRED_FILES.append(os.path.join(BASE_DIR, f"{k}_final.mp4"))

# Shorts (54)
for cat in ["stoic", "kabbalah", "humanitas"]:
    for e_idx in range(1, 4):
        for s_idx in range(1, 7):
            key = f"{cat}_essay_{e_idx}_short_{s_idx}"
            REQUIRED_FILES.append(os.path.join(BASE_DIR, f"{key}_final.mp4"))

# Metadata mapping for widescreen essays
WIDESCREEN_METADATA = {
    "stoic_essay_1": {
        "title": "El Secreto estoico de la paz mental: La dicotomía del control",
        "desc": "Descubre el camino estoico hacia la paz mental y la ataraxia absoluta regulando tus juicios. #estoicismo #autocontrol #filosofia",
        "thumb": "stoic_screenshot_0.jpg",
        "day": 1
    },
    "stoic_essay_2": {
        "title": "La Ciudadela Interior: El arte de no dejarse afectar por nada",
        "desc": "Cómo construir una mente indestructible según las enseñanzas estoicas de Marco Aurelio. #marcoaurelio #reflexion #fortaleza",
        "thumb": "stoic_screenshot_1.jpg",
        "day": 3
    },
    "stoic_essay_3": {
        "title": "La Razón frente al Caos: La sabiduría de Séneca y Epicteto",
        "desc": "Un análisis de la brevedad de la vida, la templanza y la verdadera libertad interior. #séneca #epicteto #libertad",
        "thumb": "stoic_screenshot_2.jpg",
        "day": 5
    },
    "kabbalah_essay_1": {
        "title": "El Árbol de la Vida descodificado: Las 10 Sefirot cósmicas",
        "desc": "Un viaje a través de los misterios místicos del Árbol de la Vida y la luz del Ein Sof. #cábala #mística #espiritualidad",
        "thumb": "kabbalah_screenshot_0.jpg",
        "day": 7
    },
    "kabbalah_essay_2": {
        "title": "El Secreto del Tikún: El propósito de tu alma en la Tierra",
        "desc": "Aprende el misterio de la corrección de tu alma (Tikún) y las dos columnas del cosmos. #tikún #conciencia #alma",
        "thumb": "kabbalah_screenshot_1.jpg",
        "day": 9
    },
    "kabbalah_essay_3": {
        "title": "Los Misterios del Zohar: Rasgando el velo de la realidad física",
        "desc": "La revelación de la Shejiná, los secretos ocultos de la creación y el retorno al infinito. #zohar #mística #sabiduria",
        "thumb": "kabbalah_screenshot_2.jpg",
        "day": 11
    },
    "humanitas_essay_1": {
        "title": "Magnifica Humanitas: La encíclica del Papa sobre la Inteligencia Artificial",
        "desc": "Un análisis teológico sobre la custodia del ser humano y los peligros de la IA y el transhumanismo. #vaticano #inteligenciaartificial #ética",
        "thumb": "humanitas_screenshot_0.jpg",
        "day": 13
    },
    "humanitas_essay_2": {
        "title": "Babel contra Jerusalén: La soberbia tecnocrática en la era de la IA",
        "desc": "La metáfora bíblica de la Torre de Babel y la reconstrucción de la Jerusalén digital fraterna. #papa #tecnologia #fraternidad",
        "thumb": "humanitas_screenshot_1.jpg",
        "day": 15
    },
    "humanitas_essay_3": {
        "title": "La Ética Algorítmica: Armas autónomas y el futuro del trabajo digno",
        "desc": "Gobernanza global de la IA, el derecho al trabajo humano y la epidemia de la desinformación. #verdad #automatizacion #paz",
        "thumb": "humanitas_screenshot_2.jpg",
        "day": 17
    }
}

# Metadata mapping for shorts titles
SHORT_TITLES = {
    "stoic": [
        "Dicotomía del Control 🛡", "El Arte del Tzimtzum 🤫", "Premeditación del Mal ⏳", 
        "Ama tu Destino (Amor Fati) 👑", "Construye tu Vasija 🏺", "El Juicio del Alma ⚖",
        "Ciudadela Interior 🏰", "La Chispa Divina ✨", "El Silencio de Oro 🤫",
        "El Obstáculo en el Camino ⚔", "El Secreto del Tikún 💎", "La Fortaleza de Marco Aurelio 🏛",
        "Brevedad de la Existencia ⏳", "La Balanza de la Templanza ⚖", "Libertad Interior Real 🔓",
        "Valor del Tiempo Real ⏳", "La Belleza de Tiferet ❤️", "Soberanía de Epicteto 👑"
    ],
    "kabbalah": [
        "Las Emanaciones del Ein Sof 🌟", "Contracción del Ego 🤫", "La Vasija del Dar 🏺",
        "Fuerza de Restricción 🛡", "Las 10 Sefirot Cósmicas 🌌", "Reino de los Efectos ☯",
        "Misión de tu Alma (Tikún) 💎", "Rigor y Misericordia ☯", "El Corazón del Árbol ❤️",
        "Transmutación del Destino 🌌", "Disciplina de Gevurá 🛡", "Luz del Dar Incondicional ✨",
        "Revelación del Zohar 📖", "Elevación de la Shejiná ✨", "Retorno al Infinito 🌌",
        "Espejo de la Conciencia 🌌", "Transmutar el Egoísmo 🏺", "Despertar Divino Interno 🔓"
    ],
    "humanitas": [
        "Dignidad Humana e IA 🏛", "La IA sin Límites Éticos ⚖", "La Trampa Transhumanista 🛡",
        "La Chispa No Replicable ✨", "Bien Común vs Lucro IA 💼", "Adoración de la Herramienta 🔓",
        "Babel y la Soberbia IA 🗼", "IA para la Fraternidad 🕊", "Protección Digital Social 👵",
        "Soberbia Tecnológica Cósmica 🗼", "Edificar con Justicia Digital 🕊", "El Cuidado de los Débiles 👵",
        "Marcos Éticos Internacionales 🌐", "Prohibición de Armas Autónomas ⚔", "El Derecho al Trabajo Real 💼",
        "Propaganda Algorítmica Masiva 📰", "Dignidad del Trabajo Humano 💼", "Resistencia Digital Activa 🕯"
    ]
}

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
    # Same baseline: Tomorrow morning at 00:00 is Day 1
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
    print("EXPANSION CAMPAIGN PIPELINE (DAYS 11-30, ODD DAYS)")
    print("====================================================")
    
    uploaded_file_log = os.path.join(BASE_DIR, "uploaded_campaign_2.txt")
    file_shorts = os.path.join(BASE_DIR, "scripts_expansion_shorts.md")
    
    # Daily slots for the 6 shorts
    slots = [
        (8, 0),   # 8:00 AM
        (10, 0),  # 10:00 AM
        (14, 0),  # 2:00 PM
        (16, 0),  # 4:00 PM
        (18, 0),  # 6:00 PM
        (20, 0)   # 8:00 PM
    ]
    
    while True:
        uploaded_set = set()
        if os.path.exists(uploaded_file_log):
            with open(uploaded_file_log, "r", encoding="utf-8") as f:
                uploaded_set = set(line.strip() for line in f if line.strip())
                
        pending_uploads = 0
        
        # 1. Widescreen Video Essays
        for key, info in WIDESCREEN_METADATA.items():
            file_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
            if file_path in uploaded_set: continue
            if not os.path.exists(file_path):
                pending_uploads += 1
                continue
            thumb_path = os.path.join(SCREENSHOTS_DIR, info["thumb"])
            schedule_offset = get_schedule_offset(info["day"], 12, 0) # 12:00 PM
            print(f"Uploading Widescreen: '{info['title']}'...")
            success = run_youtube_upload(file_path, info["title"], info["desc"], is_short=False, thumbnail_path=thumb_path, schedule_offset=schedule_offset)
            if success:
                uploaded_set.add(file_path)
                with open(uploaded_file_log, "a", encoding="utf-8") as f: f.write(file_path + "\n")
            else: pending_uploads += 1
            time.sleep(10)
            
        # 2. Complemental Shorts
        for key, info in WIDESCREEN_METADATA.items():
            day_num = info["day"]
            match = re.match(r"([a-z]+)_essay_(\d+)", key)
            if not match: continue
            cat = match.group(1)
            e_idx = int(match.group(2))
            
            for s_idx in range(1, 7):
                short_key = f"{cat}_essay_{e_idx}_short_{s_idx}"
                file_path = os.path.join(BASE_DIR, f"{short_key}_final.mp4")
                if file_path in uploaded_set: continue
                if not os.path.exists(file_path):
                    pending_uploads += 1
                    continue
                desc_text = extract_short_text(file_shorts, short_key)
                t_idx = ((e_idx - 1) * 6 + (s_idx - 1)) % 18
                title_text = SHORT_TITLES[cat][t_idx]
                
                hr, mins = slots[s_idx - 1]
                schedule_offset = get_schedule_offset(day_num, hr, mins)
                print(f"Uploading Short: '{title_text}'...")
                success = run_youtube_upload(file_path, title_text, desc_text, is_short=True, schedule_offset=schedule_offset)
                if success:
                    uploaded_set.add(file_path)
                    with open(uploaded_file_log, "a", encoding="utf-8") as f: f.write(file_path + "\n")
                else: pending_uploads += 1
                time.sleep(10)
                
        if pending_uploads == 0:
            print("\nAll 63 files for Campaign 2 uploaded successfully!")
            break
            
        print(f"\n[INFO] Campaign 2 loop finished. {pending_uploads} files still pending. Sleeping for 60 seconds...")
        time.sleep(60)

if __name__ == "__main__":
    main()
