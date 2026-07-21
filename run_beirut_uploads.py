import os
import sys
import time
import subprocess
from datetime import datetime

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_beirut.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

# Metadata for Widescreen Video Essay
ESSAYS_METADATA = {
    "beirut_essay_1": {
        "file": os.path.join(PROJECT_DIR, "beirut_essay_1_final.mp4"),
        "title": "La Explosión de Beirut: El Día que la Negligencia Destruyó una Ciudad 🇱🇧💥",
        "desc": "Análisis forense y social de la catástrofe del 4 de agosto de 2020 en el puerto de Beirut. La historia del Rhosus, la negligencia en el Hangar 12 y la onda expansiva que marcó a Líbano. #beirut #explosion #documental #historia #negligencia",
        "is_short": False
    }
}

# Metadata for 14 Vertical Shorts
SHORTS_METADATA = {
    "beirut_short_1": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_1_final.mp4"),
        "title": "El barco maldito que selló el destino de Beirut 🚢 #shorts",
        "desc": "La llegada del buque Rhosus en 2013 y cómo abandonó una bomba de tiempo química en el puerto. #beirut #historia #barco",
        "is_short": True
    },
    "beirut_short_2": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_2_final.mp4"),
        "title": "Hangar 12: La bomba de tiempo ignorada por años 💣 #shorts",
        "desc": "El almacenamiento inseguro de 2,750 toneladas de nitrato de amonio en el corazón de Beirut. #beirut #negligencia #química",
        "is_short": True
    },
    "beirut_short_3": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_3_final.mp4"),
        "title": "Las alertas rojas que la burocracia archivó 📁 #shorts",
        "desc": "Las seis cartas de advertencia sobre el peligro en el puerto que los jueces y el gobierno ignoraron. #corrupción #burocracia #libano",
        "is_short": True
    },
    "beirut_short_4": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_4_final.mp4"),
        "title": "Pirotecnia y nitrato: La mezcla letal de la tragedia 🔥 #shorts",
        "desc": "Cómo unos trabajos de soldadura iniciaron el fuego fatal en el hangar de almacenamiento. #incendio #tragedia #desastre",
        "is_short": True
    },
    "beirut_short_5": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_5_final.mp4"),
        "title": "El milagro de la novia de Beirut 👰 #shorts",
        "desc": "El estremecedor video viral de una boda interrumpida por la masiva onda expansiva de la explosión. #viral #novia #milagro",
        "is_short": True
    },
    "beirut_short_6": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_6_final.mp4"),
        "title": "La física detrás de la nube blanca de la explosión ☁️ #shorts",
        "desc": "Explicación científica de la nube de condensación Wilson generada por la onda de choque. #ciencia #física #curiosidades",
        "is_short": True
    },
    "beirut_short_7": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_7_final.mp4"),
        "title": "El colapso de los silos de trigo de Beirut 🌾 #shorts",
        "desc": "Cómo la colosal estructura de hormigón protegió a media ciudad de la onda destructiva. #silos #hormigón #resistencia",
        "is_short": True
    },
    "beirut_short_8": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_8_final.mp4"),
        "title": "La explosión no nuclear más potente de la historia 💥 #shorts",
        "desc": "La escala energética equivalente a un kilotón que arrasó el puerto de Beirut. #desastre #energía #historia",
        "is_short": True
    },
    "beirut_short_9": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_9_final.mp4"),
        "title": "Hospitales en ruinas: La segunda catástrofe de Beirut 🏥 #shorts",
        "desc": "El colapso médico inmediato tras la destrucción de los centros de salud por el estallido. #humanitario #hospital #emergencia",
        "is_short": True
    },
    "beirut_short_10": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_10_final.mp4"),
        "title": "El desastre económico tras perder el principal puerto 📉 #shorts",
        "desc": "El impacto demoledor sobre el abastecimiento de alimentos en un Líbano ya quebrado. #economía #crisis #libano",
        "is_short": True
    },
    "beirut_short_11": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_11_final.mp4"),
        "title": "La dimisión del gobierno libanés tras la ira popular 🏛️ #shorts",
        "desc": "Las intensas manifestaciones y la caída del gabinete político tras la tragedia. #protestas #gobierno #justicia",
        "is_short": True
    },
    "beirut_short_12": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_12_final.mp4"),
        "title": "El cargamento fantasma de nitrato de amonio 👻 #shorts",
        "desc": "Las empresas británicas y de Mozambique ligadas al envío fantasma del Rhosus. #corrupción #investigación #crimen",
        "is_short": True
    },
    "beirut_short_13": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_13_final.mp4"),
        "title": "Héroes sin capa: Los bomberos de Beirut 🚒 #shorts",
        "desc": "El primer equipo de bomberos que acudió a apagar las llamas y falleció en la gran detonación. #héroes #bomberos #tributo",
        "is_short": True
    },
    "beirut_short_14": {
        "file": os.path.join(PROJECT_DIR, "beirut_short_14_final.mp4"),
        "title": "Beirut a cuatro años: Las heridas siguen abiertas 🇱🇧 #shorts",
        "desc": "La lucha contra la impunidad estatal y la falta de sanciones a altos mandos responsables. #justicia #libano #aniversario",
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
    print("DOMINUSBABEL BEIRUT CAMPAIGN AUTOMATED UPLOADER")
    print("====================================================\n")
    
    queue = []
    for key, info in ESSAYS_METADATA.items():
        queue.append((key, info))
    for key, info in SHORTS_METADATA.items():
        queue.append((key, info))
        
    while True:
        uploaded = load_uploaded()
        pending = [item for item in queue if item[1]["file"] not in uploaded]
        
        if not pending:
            print("\n✅ All Beirut campaign videos (1 essay & 14 shorts) are successfully uploaded to DOMINUSBABEL!")
            break
            
        # Non-blocking check for ready compiled files
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
