import os
import sys
import time
import subprocess
from datetime import datetime

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_onedrive.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

ESSAYS_METADATA = {
    "onedrive_essay_1": {
        "file": os.path.join(PROJECT_DIR, "onedrive_essay_1_final.mp4"),
        "title": "La Paradoja de OneDrive: Cómo Microsoft Arruinó su Mejor Producto ☁️💻",
        "desc": "Análisis tecnológico y estratégico de por qué OneDrive pierde usuarios frente a Google Drive a pesar de estar integrado en Windows. La historia de las notificaciones intrusivas y el ecosistema educativo de Google. #onedrive #googledrive #windows #tecnologia #microsoft",
        "is_short": False
    }
}

SHORTS_METADATA = {
    "onedrive_short_1": {
        "file": os.path.join(PROJECT_DIR, "onedrive_short_1_final.mp4"),
        "title": "¿Por qué todos odian OneDrive aunque sea mejor? ☁️ #shorts",
        "desc": "La paradoja del almacenamiento en la nube de Microsoft y el rechazo de sus propios usuarios. #onedrive #googledrive #tecnologia",
        "is_short": True
    },
    "onedrive_short_2": {
        "file": os.path.join(PROJECT_DIR, "onedrive_short_2_final.mp4"),
        "title": "El truco con el que Google conquistó a una generación 🎓 #shorts",
        "desc": "Cómo Google dominó las escuelas con Chromebooks y Google Classroom desplazando a Microsoft. #google #escuela #estudiantes",
        "is_short": True
    },
    "onedrive_short_3": {
        "file": os.path.join(PROJECT_DIR, "onedrive_short_3_final.mp4"),
        "title": "El día que Microsoft traicionó a sus usuarios 💔 #shorts",
        "desc": "El recorte drástico de la oferta ilimitada y la reducción del espacio gratuito en 2015. #microsoft #nube #almacenamiento",
        "is_short": True
    },
    "onedrive_short_4": {
        "file": os.path.join(PROJECT_DIR, "onedrive_short_4_final.mp4"),
        "title": "El molesto aviso que te obliga a usar OneDrive 🔔 #shorts",
        "desc": "La intrusividad de las notificaciones de respaldo en Windows que irritan a los usuarios. #windows11 #onedrive #molesto",
        "is_short": True
    },
    "onedrive_short_5": {
        "file": os.path.join(PROJECT_DIR, "onedrive_short_5_final.mp4"),
        "title": "¿Google Drive o OneDrive? La verdad técnica 💻 #shorts",
        "desc": "Comparativa técnica directa entre las funciones de sincronización de Microsoft y Google. #comparativa #software #nube",
        "is_short": True
    },
    "onedrive_short_6": {
        "file": os.path.join(PROJECT_DIR, "onedrive_short_6_final.mp4"),
        "title": "El desastre de la sincronización de archivos 📁 #shorts",
        "desc": "Los duplicados de archivos y errores de sincronización que frustran el uso de OneDrive. #archivos #errores #windows",
        "is_short": True
    },
    "onedrive_short_7": {
        "file": os.path.join(PROJECT_DIR, "onedrive_short_7_final.mp4"),
        "title": "Por qué Microsoft no logra vencer a Google en la nube ⚔️ #shorts",
        "desc": "El hábito de uso sobre la tecnología: por qué lo sencillo siempre le gana a lo preinstalado. #estrategia #google #microsoft",
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
    print("DOMINUSBABEL ONEDRIVE CAMPAIGN AUTOMATED UPLOADER")
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
            print("\n✅ All OneDrive campaign videos (1 essay & 7 shorts) are successfully uploaded to DOMINUSBABEL!")
            break
            
        ready_item = None
        for item in pending:
            video_path = item[1]["file"]
            if os.path.exists(video_path) and os.path.getsize(video_path) > 500000:
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
            print(f"[WAIT] No ready files found. First pending: {key} -> waiting 20 seconds...")
            time.sleep(20)

if __name__ == "__main__":
    main()
