import os
import sys
import time
import subprocess
from datetime import datetime

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_spain.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

# Metadata for Widescreen Video Essays
ESSAYS_METADATA = {
    "spain_essay_1": {
        "file": os.path.join(PROJECT_DIR, "spain_essay_1_final.mp4"),
        "title": "La Segunda Estrella: Cómo España conquistó el Mundial de 2026 🇪🇸🏆",
        "desc": "Análisis táctico y emotivo de la consagración de la selección española en Nueva Jersey. Las claves de Luis de la Fuente, Rodri, Pedri y el histórico gol de Ferran Torres. #futbol #mundial2026 #españa #campeones #táctica",
        "is_short": False
    },
    "spain_essay_2": {
        "file": os.path.join(PROJECT_DIR, "spain_essay_2_final.mp4"),
        "title": "El Último Baile de Messi y la Pizarra Táctica de la Final 👑🇦🇷",
        "desc": "El desglose táctico de la final del Mundial 2026 y el adiós de Lionel Messi a las Copas del Mundo a sus 39 años. Cómo España neutralizó el mediocampo y la batalla física del MetLife Stadium. #messi #argentina #mundial #futbol #deportes",
        "is_short": False
    }
}

# Metadata for 18 Vertical Shorts
SHORTS_METADATA = {
    "spain_short_1": {
        "file": os.path.join(PROJECT_DIR, "spain_short_1_final.mp4"),
        "title": "El gol de la gloria de Ferran Torres ⚽ #shorts",
        "desc": "El gol decisivo de Ferran Torres en el minuto 106 de la prórroga que le dio la Copa del Mundo a España. #futbol #españa #mundial",
        "is_short": True
    },
    "spain_short_2": {
        "file": os.path.join(PROJECT_DIR, "spain_short_2_final.mp4"),
        "title": "El adiós de Lionel Messi a los Mundiales 👑 #shorts",
        "desc": "El último partido mundialista del astro argentino Lionel Messi a sus 39 años en Nueva Jersey. #messi #argentina #leyenda",
        "is_short": True
    },
    "spain_short_3": {
        "file": os.path.join(PROJECT_DIR, "spain_short_3_final.mp4"),
        "title": "La roja que sentenció a la Albiceleste 🔴 #shorts",
        "desc": "La expulsión de Enzo Fernández que rompió el equilibrio defensivo de Argentina en el tiempo regular. #futbol #roja #mundial",
        "is_short": True
    },
    "spain_short_4": {
        "file": os.path.join(PROJECT_DIR, "spain_short_4_final.mp4"),
        "title": "Rodri: El cerebro indiscutible del campeón 🧠 #shorts",
        "desc": "El MVP táctico de la final que asfixió la creación ofensiva de Argentina. #rodri #futbol #españa",
        "is_short": True
    },
    "spain_short_5": {
        "file": os.path.join(PROJECT_DIR, "spain_short_5_final.mp4"),
        "title": "Pedri y la magia del mediocampo español 🔮 #shorts",
        "desc": "La exhibición de fútbol asociativo y la milimétrica asistencia de Pedri para el gol del campeonato. #pedri #españa #magia",
        "is_short": True
    },
    "spain_short_6": {
        "file": os.path.join(PROJECT_DIR, "spain_short_6_final.mp4"),
        "title": "España conquista su segunda estrella mundialista ⭐ #shorts",
        "desc": "Dieciséis años después de Sudáfrica 2010, España vuelve a ser campeona del mundo. #campeones #españa #mundial2026",
        "is_short": True
    },
    "spain_short_7": {
        "file": os.path.join(PROJECT_DIR, "spain_short_7_final.mp4"),
        "title": "El dolor de Messi tras la derrota en Nueva Jersey 😢 #shorts",
        "desc": "La tristeza de Lionel Messi contemplando el trofeo tras la final del Mundial 2026. #messi #argentina #futbol",
        "is_short": True
    },
    "spain_short_8": {
        "file": os.path.join(PROJECT_DIR, "spain_short_8_final.mp4"),
        "title": "La pizarra secreta de Luis de la Fuente 📋 #shorts",
        "desc": "El planteamiento táctico español que neutralizó la salida limpia de Argentina. #pizarra #táctica #futbol",
        "is_short": True
    },
    "spain_short_9": {
        "file": os.path.join(PROJECT_DIR, "spain_short_9_final.mp4"),
        "title": "Una prórroga de infarto en el MetLife Stadium 🕰️ #shorts",
        "desc": "La tensión límite y los calambres musculares en una prórroga de infarto. #mundial #futbol #prorroga",
        "is_short": True
    },
    "spain_short_10": {
        "file": os.path.join(PROJECT_DIR, "spain_short_10_final.mp4"),
        "title": "Lionel Scaloni y la heroica defensa argentina ⚔️ #shorts",
        "desc": "La resistencia defensiva de la albiceleste con un hombre menos en la gran final. #scaloni #argentina #defensa",
        "is_short": True
    },
    "spain_short_11": {
        "file": os.path.join(PROJECT_DIR, "spain_short_11_final.mp4"),
        "title": "Ferran Torres: El tiburón de los momentos clave 🦈 #shorts",
        "desc": "La consagración del delantero valenciano Ferran Torres marcando el gol de la victoria. #ferran #tiburón #españa",
        "is_short": True
    },
    "spain_short_12": {
        "file": os.path.join(PROJECT_DIR, "spain_short_12_final.mp4"),
        "title": "El MetLife Stadium: Epicentro del fútbol mundial 🏟️ #shorts",
        "desc": "El espectacular ambiente en el MetLife Stadium de Nueva Jersey durante la final de la Copa del Mundo. #estadio #futbol #mundial",
        "is_short": True
    },
    "spain_short_13": {
        "file": os.path.join(PROJECT_DIR, "spain_short_13_final.mp4"),
        "title": "España vs Argentina: Una final histórica 🌍 #shorts",
        "desc": "El choque de estilos contrapuestos entre España y Argentina en Nueva Jersey. #futbol #clasico #final",
        "is_short": True
    },
    "spain_short_14": {
        "file": os.path.join(PROJECT_DIR, "spain_short_14_final.mp4"),
        "title": "El colapso físico extremo de la final 🥵 #shorts",
        "desc": "El agotamiento extremo y el calor de verano que marcaron el desenlace físico de la prórroga. #futbol #fatiga #mundial",
        "is_short": True
    },
    "spain_short_15": {
        "file": os.path.join(PROJECT_DIR, "spain_short_15_final.mp4"),
        "title": "La segunda estrella: Comparación 2010 vs 2026 ⭐ #shorts",
        "desc": "Cómo se compara la hazaña histórica de Sudáfrica con la de Nueva Jersey. #iniesta #ferran #españa",
        "is_short": True
    },
    "spain_short_16": {
        "file": os.path.join(PROJECT_DIR, "spain_short_16_final.mp4"),
        "title": "Las estadísticas reales de la final del Mundial 📊 #shorts",
        "desc": "Posesión de balón, remates y claves numéricas del duelo táctico del siglo. #datos #estadísticas #futbol",
        "is_short": True
    },
    "spain_short_17": {
        "file": os.path.join(PROJECT_DIR, "spain_short_17_final.mp4"),
        "title": "La nueva generación de España domina el mundo 👶 #shorts",
        "desc": "La consagración del plantel joven que liderará el fútbol internacional la próxima década. #pedri #lamine #españa",
        "is_short": True
    },
    "spain_short_18": {
        "file": os.path.join(PROJECT_DIR, "spain_short_18_final.mp4"),
        "title": "El fin del ciclo triunfal de Argentina 👑 #shorts",
        "desc": "El adiós a una época gloriosa iniciada en Qatar 2022 para la selección albiceleste. #argentina #futbol #messi",
        "is_short": True
    }
}

def load_uploaded():
    if not os.path.exists(uploaded_log_path):
        return set()
    with open(uploaded_log_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def register_upload(video_path):
    with open(uploaded_log_path, "a", encoding="utf-8") as f:
        f.write(video_path + "\n")

def run_upload(file_path, title, desc, is_short):
    print(f"\n[UPLOAD] Launching uploader for: {title}...")
    cmd = [
        "node", uploader_script,
        "--file", file_path,
        "--title", title,
        "--desc", desc,
        "--draft"
    ]
    if is_short:
        cmd.append("--is_short")
        
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    
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
    print("DOMINUSBABEL SPAIN CAMPAIGN AUTOMATED UPLOADER")
    print("====================================================\n")
    
    # Non-blocking queue setup
    queue = []
    for key, info in ESSAYS_METADATA.items():
        queue.append((key, info))
    for key, info in SHORTS_METADATA.items():
        queue.append((key, info))
        
    while True:
        uploaded = load_uploaded()
        pending = [item for item in queue if item[1]["file"] not in uploaded]
        
        if not pending:
            print("\n✅ All Spain campaign videos (2 essays & 18 shorts) are successfully uploaded to DOMINUSBABEL!")
            break
            
        # Find any pending video file that is already compiled on disk
        ready_item = None
        for item in pending:
            video_path = item[1]["file"]
            if os.path.exists(video_path) and os.path.getsize(video_path) > 1000000: # at least 1MB
                ready_item = item
                break
                
        if ready_item:
            key, info = ready_item
            video_path = info["file"]
            success = run_upload(video_path, info["title"], info["desc"], info["is_short"])
            if success:
                register_upload(video_path)
                print(f"[STATUS] Progress: {len(load_uploaded())}/{len(queue)} completed.")
                print("Waiting 15 seconds before next upload...")
                time.sleep(15)
            else:
                print("[WARNING] Upload encountered an error. Retrying in 60 seconds...")
                time.sleep(60)
        else:
            key, info = pending[0]
            print(f"[WAIT] No ready files found. First pending: {key} -> not compiled yet. Waiting 30 seconds...")
            time.sleep(30)

if __name__ == "__main__":
    main()
