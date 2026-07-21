import os
import sys
import time
import subprocess
from datetime import datetime

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_siberia.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

# Metadata for Widescreen Video Essays
ESSAYS_METADATA = {
    "siberia_essay_1": {
        "file": os.path.join(PROJECT_DIR, "siberia_essay_1_final.mp4"),
        "title": "La Subasta de Siberia: ¿Cuánto vale un soldado en Rusia? 🇷🇺💸",
        "desc": "Introducción al sesgo geográfico en el reclutamiento militar ruso. Analizamos por qué las bajas se concentran en las repúblicas remotas y el funcionamiento descentralizado de la subasta de bonos. #historia #rusia #geopolitica #siberia #guerra",
        "is_short": False
    },
    "siberia_essay_2": {
        "file": os.path.join(PROJECT_DIR, "siberia_essay_2_final.mp4"),
        "title": "El Negocio de la Muerte: Los \"Grobovye\" en la Rusia Rural ⚰️",
        "desc": "Un análisis social y profundo sobre el fenómeno de los \"pagos de ataúd\" en las repúblicas de Siberia, y el impacto demográfico y económico de estas indemnizaciones. #historia #rusia #grobovye #economia #sociedad",
        "is_short": False
    }
}

# Metadata for 15 Vertical Shorts
SHORTS_METADATA = {
    "siberia_short_1": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_1_final.mp4"),
        "title": "¿Cuánto vale un soldado en Siberia? 🇷🇺💸 #shorts",
        "desc": "Contraste crudo entre el costo de la vida y el valor económico de un contrato de reclutamiento en Siberia. #rusia #geopolitica #guerra",
        "is_short": True
    },
    "siberia_short_2": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_2_final.mp4"),
        "title": "El macabro negocio de los \"Grobovye\" ⚰️ #shorts",
        "desc": "Explicación del término \"dinero de ataúd\" y su volumen en rublos en la Rusia profunda. #grobovye #rusia #siberia #historia",
        "is_short": True
    },
    "siberia_short_3": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_3_final.mp4"),
        "title": "La subasta militar: República contra República ⚔️ #shorts",
        "desc": "La competencia interna en las regiones de Rusia por ofrecer el bono de reclutamiento más alto. #militar #rusia #geopolitica",
        "is_short": True
    },
    "siberia_short_4": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_4_final.mp4"),
        "title": "Yakutia: Contratos militares a -40 grados ❄️ #shorts",
        "desc": "El factor climático y la extrema pobreza rural como motores de reclutamiento militar en Yakutia. #yakutia #sajha #historia",
        "is_short": True
    },
    "siberia_short_5": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_5_final.mp4"),
        "title": "El oscuro secreto de los entrenamientos rusos ☠️ #shorts",
        "desc": "Denuncia sobre abusos de la Dedovshchina y la falta de preparación de los nuevos reclutas rusos. #militar #guerra #dedovshchina",
        "is_short": True
    },
    "siberia_short_6": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_6_final.mp4"),
        "title": "Presos al frente: ¿Amnistía o sentencia? ⛓️ #shorts",
        "desc": "El papel de los convictos movilizados y su valor de mercado militar. #convictos #rusia #prisioneros #historia",
        "is_short": True
    },
    "siberia_short_7": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_7_final.mp4"),
        "title": "Moscú no va a la guerra: La gran mentira 🏙️ #shorts",
        "desc": "Disparidad de mortalidad y reclutamiento entre la capital rusa y las regiones de Siberia. #desigualdad #moscu #guerra",
        "is_short": True
    },
    "siberia_short_8": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_8_final.mp4"),
        "title": "¿De dónde saca Rusia billones para reclutas? 💳 #shorts",
        "desc": "Explicación del presupuesto militar de guerra de la economía de Moscú. #presupuesto #finanzas #rusia",
        "is_short": True
    },
    "siberia_short_9": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_9_final.mp4"),
        "title": "Del frío de Siberia directo a la trinchera 🌲 #shorts",
        "desc": "La veloz transición de civiles a combatientes en menos de 15 días. #militar #siberia #trinchera",
        "is_short": True
    },
    "siberia_short_10": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_10_final.mp4"),
        "title": "La deuda familiar: El gancho de la guerra 🏠 #shorts",
        "desc": "Cómo los prestamistas y las deudas empujan a los hombres jóvenes al frente en Siberia. #deudas #economia #guerra",
        "is_short": True
    },
    "siberia_short_11": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_11_final.mp4"),
        "title": "¿Qué pasa cuando el dinero de ataúd se acaba? 📉 #shorts",
        "desc": "El impacto social y psicológico de las viudas en la economía rural de Siberia. #sociedad #viudas #guerra",
        "is_short": True
    },
    "siberia_short_12": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_12_final.mp4"),
        "title": "La inflación del rublo y los bonos de verano 💵 #shorts",
        "desc": "Cómo el aumento de precios obliga al Kremlin a subir las ofertas de reclutamiento. #inflacion #rublo #economia",
        "is_short": True
    },
    "siberia_short_13": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_13_final.mp4"),
        "title": "Minorías étnicas: El costo demográfico invisible 👥 #shorts",
        "desc": "La reducción desproporcionada de las poblaciones buriatas y yakutas. #demografia #etnias #historia",
        "is_short": True
    },
    "siberia_short_14": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_14_final.mp4"),
        "title": "Bajas invisibles: Las cifras que oculta Moscú 📊 #shorts",
        "desc": "Las discrepancias de datos oficiales contra registros independientes de prensa. #censura #bajas #datos",
        "is_short": True
    },
    "siberia_short_15": {
        "file": os.path.join(PROJECT_DIR, "siberia_short_15_final.mp4"),
        "title": "El Sur Global y el decoupling financiero ruso 🪐 #shorts",
        "desc": "El impacto geopolítico del desvío económico ruso hacia el bloque euroasiático. #surglobal #finanzas #geopolitica",
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
    print("DOMINUSBABEL SIBERIA CAMPAIGN AUTOMATED UPLOADER")
    print("====================================================\n")
    
    # Ordered queue: 2 widescreen essays first, then 15 vertical shorts
    queue = []
    for key, info in ESSAYS_METADATA.items():
        queue.append((key, info))
    for key, info in SHORTS_METADATA.items():
        queue.append((key, info))
        
    while True:
        uploaded = load_uploaded()
        pending = [item for item in queue if item[1]["file"] not in uploaded]
        
        if not pending:
            print("\n✅ All Siberia campaign videos (2 essays & 15 shorts) are successfully uploaded to DOMINUSBABEL!")
            break
            
        # Find the first pending item whose video file is compiled and ready on disk
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
                # Pause between uploads to let YouTube process and avoid session throttle
                print("Waiting 15 seconds before next upload...")
                time.sleep(15)
            else:
                print("[WARNING] Upload encountered an error. Retrying in 60 seconds...")
                time.sleep(60)
        else:
            # No files are ready yet. Show the first pending one and wait
            key, info = pending[0]
            print(f"[WAIT] No ready files found. First pending: {key} -> not compiled yet. Waiting 30 seconds...")
            time.sleep(30)

if __name__ == "__main__":
    main()
