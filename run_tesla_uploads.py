import os
import sys
import time
import subprocess
from datetime import datetime

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_tesla.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

ESSAYS_METADATA = {
    "tesla_essay_1": {
        "file": os.path.join(PROJECT_DIR, "tesla_essay_1_final.mp4"),
        "title": "Warp Drive: La Apuesta Imposible de Tesla que Humilló a la Industria del Software ⚡🚗",
        "desc": "Documental periodístico sobre cómo Elon Musk y Tesla desmantelaron el sistema alemán SAP para programar su propio ERP nativo en solo 4 meses. La historia de Jay Vijayan y la revolución del software de manufactura. #tesla #warpdrive #sap #elonmusk #tecnologia #software",
        "is_short": False
    }
}

SHORTS_METADATA = {
    "tesla_short_1": {
        "file": os.path.join(PROJECT_DIR, "tesla_short_1_final.mp4"),
        "title": "El día que Tesla estuvo a 48 horas de la quiebra 💸 #shorts",
        "desc": "La dramática crisis de la Nochebuena de 2008 donde Elon Musk no tenía dinero para pagar nóminas. #tesla #elonmusk #historia",
        "is_short": True
    },
    "tesla_short_2": {
        "file": os.path.join(PROJECT_DIR, "tesla_short_2_final.mp4"),
        "title": "¿Por qué Tesla despidió al gigante alemán SAP? 🚗 #shorts",
        "desc": "La incompatibilidad de SAP con el ritmo de cambios diarios en las fábricas de Tesla. #tesla #sap #software",
        "is_short": True
    },
    "tesla_short_3": {
        "file": os.path.join(PROJECT_DIR, "tesla_short_3_final.mp4"),
        "title": "El ingeniero que rechazó trabajar para Elon Musk 👤 #shorts",
        "desc": "Cómo Jay Vijayan dijo no inicialmente a Elon Musk antes de crear Warp Drive. #liderazgo #tecnologia #negocios",
        "is_short": True
    },
    "tesla_short_4": {
        "file": os.path.join(PROJECT_DIR, "tesla_short_4_final.mp4"),
        "title": "Un sistema de 2 años construido en 4 meses ⚡ #shorts",
        "desc": "La proeza de programación de 25 ingenieros de Tesla para sustituir el software corporativo tradicional. #warpdrive #programacion #produtividad",
        "is_short": True
    },
    "tesla_short_5": {
        "file": os.path.join(PROJECT_DIR, "tesla_short_5_final.mp4"),
        "title": "El secreto con el que Tesla redujo costes de fábrica 📉 #shorts",
        "desc": "La integración en milisegundos entre la tienda web y los robots de las Gigafábricas. #gigafactory #eficiencia #automatizacion",
        "is_short": True
    },
    "tesla_short_6": {
        "file": os.path.join(PROJECT_DIR, "tesla_short_6_final.mp4"),
        "title": "Por qué BMW y Mercedes no pueden copiar a Tesla ⚔️ #shorts",
        "desc": "La trampa del software heredado y los concesionarios que atan a la industria automotriz tradicional. #autos #bmw #mercedes #tesla",
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
    print("DOMINUSBABEL TESLA SAP CAMPAIGN AUTOMATED UPLOADER")
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
            print("\n✅ All Tesla SAP campaign videos (1 essay & 6 shorts) are successfully uploaded to DOMINUSBABEL!")
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
