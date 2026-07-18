import os
import sys
import json
import time
import subprocess
from datetime import datetime, timedelta

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\reddit_deep_project"
manifest_path = os.path.join(PROJECT_DIR, "manifest.json")
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_deep.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_reddit.js"

# Title mappings for horizontal documentals
LONG_TITLES = {
    1: "McMurdo: Sobrevivir a la Aterradora Noche Polar en la Antártida ❄️💀",
    2: "Buceo de Saturación: El Agónico Trabajo a 300 Metros Bajo el Mar 🌊⚓",
    3: "La Torre del Silencio: 90 Días de Aislamiento Extremo en Oregón 🌲⚡",
    4: "Svalbard: El Extraño Pueblo donde la Muerte está Prohibida 🐻❄️",
    5: "Punto Nemo: Qué hay Realmente en el Lugar más Aislado de la Tierra 🚀🌌",
    6: "Chernóbil: El Peligroso Día a Día del Vigilante de la Zona Prohibida ☣️☢️"
}

# Clickbait title mappings for the 18 Shorts
SHORT_TITLES = {
    1: "La Regla de los Tres Metros en el Polo Sur ❄️",
    2: "El Síndrome de T3: Locura en el Hielo 🧠",
    3: "La Base de la Antártida que no Puede Apagarse 🔌",
    4: "La Sangre que Hierve Bajo el Mar 🩸",
    5: "El Peligroso Cordón de Vida de un Buzo ⚓",
    6: "Cinco Días de Retorno a la Tierra 🚀",
    7: "El Pararrayos Humano de la Torre de Oregón ⚡",
    8: "La Soledad Ruidosa en Medio de la Nada 🌲",
    9: "Cinco Minutos para Evitar el Infierno 🔥",
    10: "El Pueblo donde Morir está Prohibido 💀",
    11: "La Regla del Rifle Obligatorio en Svalbard 🐻",
    12: "La Bóveda del Fin del Mundo en el Ártico ❄️",
    13: "Los Seres Humanos más Cercanos están en el Espacio 🌌",
    14: "El Cementerio de Titanio Espacial Bajo el Mar 🚀",
    15: "El Misterio de la Señal 'The Bloop' 🌊",
    16: "El Abrazo Invisible de la Radiación de Chernóbil ☣️",
    17: "Trabajar en el Corazón del Monstruo de Acero ☢️",
    18: "El Bosque Rojo de la Zona de Exclusión 🌲"
}

def load_manifest():
    if not os.path.exists(manifest_path):
        return None
    with open(manifest_path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_uploaded():
    if not os.path.exists(uploaded_log_path):
        return set()
    with open(uploaded_log_path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def register_upload(video_path):
    with open(uploaded_log_path, "a", encoding="utf-8") as f:
        f.write(video_path + "\n")

def main():
    print("====================================================")
    print("CAMPAIGN 2 (TRABAJOS EXTREMOS) AUTOMATED UPLOAD RUNNER")
    print("====================================================\n")
    
    # Establish campaign start time
    launch_time = datetime.now()
    
    while True:
        manifest = load_manifest()
        uploaded = load_uploaded()
        
        if not manifest:
            print("[INFO] Manifest file missing. Waiting 30 seconds...")
            time.sleep(30)
            continue
            
        # Compile Queue: Interleave Widescreen and Shorts
        # We want Story 1 Long -> Story 1 Short 1 -> Story 1 Short 2 -> Story 1 Short 3 -> Story 2 Long...
        queue = []
        
        # Parse manifest data
        longs = {item["story_num"]: item for item in manifest.get("long_form", [])}
        shorts = {}
        for s_item in manifest.get("shorts", []):
            story_num = int(s_item["key"].split("_")[2])
            part_num = s_item["part_num"]
            if story_num not in shorts:
                shorts[story_num] = {}
            shorts[story_num][part_num] = s_item

        # Assemble queue elements in correct order
        for s_idx in range(1, 7):
            # 1. Long form widescreen video
            if s_idx in longs:
                queue.append({
                    "type": "long",
                    "story_num": s_idx,
                    "item": longs[s_idx]
                })
            # 2. 3 Shorts parts
            if s_idx in shorts:
                for p_idx in range(1, 4):
                    if p_idx in shorts[s_idx]:
                        queue.append({
                            "type": "short",
                            "story_num": s_idx,
                            "part_num": p_idx,
                            "item": shorts[s_idx][p_idx]
                        })

        # Process pending items
        for q_idx, q_item in enumerate(queue):
            item = q_item["item"]
            key = item["key"]
            video_path = os.path.join(PROJECT_DIR, f"{key}_final.mp4")
            
            if video_path in uploaded:
                continue
                
            # Check if file exists and has non-zero size (waiting for compiler if needed)
            if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
                print(f"[INFO] Video file {key}_final.mp4 is not compiled yet. Waiting for compiler...")
                time.sleep(30)
                break # Break out to reload manifest/check again
                
            # Calculate schedule target:
            # First item at launch_time + 15 minutes, subsequent items scheduled with exactly 30 minutes interval
            target_time = launch_time + timedelta(minutes=15 + q_idx * 30)
            schedule_offset = int((target_time - datetime.now()).total_seconds() / 60)
            
            if schedule_offset <= 0:
                schedule_offset = 15 # Minimum fallback schedule offset to allow upload processing buffer
                
            # Prepare metadata based on format type
            thumbnail_path = ""
            is_short = False
            
            if q_item["type"] == "long":
                # Long form widescreen metadata
                viral_title = LONG_TITLES.get(q_item["story_num"], item["title"])
                yt_title = f"{viral_title} | Historias de Reddit"
                if len(yt_title) > 100:
                    yt_title = yt_title[:95] + "..."
                    
                desc_text = (
                    f"Documental completo: {viral_title}\n\n"
                    f"Recopilamos las mejores crónicas de supervivencia, misterio y trabajo extremo narradas por testimonios reales de Reddit.\n\n"
                    f"#reddit #documental #historias #misterio #supervivencia #trabajos #redditstories"
                )
                # Use widescreen illustration as custom thumbnail!
                thumbnail_path = os.path.join(PROJECT_DIR, "capsules", f"story_{q_item['story_num']}.jpg")
            else:
                # Shorts metadata
                is_short = True
                short_index = item["short_index"]
                part_num = q_item["part_num"]
                viral_title = SHORT_TITLES.get(short_index, item["title"])
                
                # Title format: [Clickbait Title] (Parte X/3) #reddit #historias #shorts
                yt_title = f"{viral_title} (Parte {part_num}/3) #reddit #historias #shorts"
                if len(yt_title) > 100:
                    yt_title = yt_title[:95] + "..."
                    
                desc_text = (
                    f"Historia: {viral_title}\n"
                    f"Parte {part_num} de 3.\n\n"
                    f"Relatos reales e intrigantes de personas que trabajaron en los sitios más raros y peligrosos de la Tierra.\n\n"
                    f"#reddit #historias #shorts #relatos #misterio #trabajosextremos"
                )
                
            print(f"\n[QUEUE] Processing Campaign 2: {key}")
            print(f"  Format: {'Short' if is_short else 'Widescreen Documental'}")
            print(f"  Video Path: {video_path}")
            print(f"  Schedule Target: {target_time.strftime('%Y-%m-%d %H:%M')} (In {schedule_offset} minutes)")
            if thumbnail_path:
                print(f"  Thumbnail Path: {thumbnail_path}")
                
            # Write JSON config for Node uploader
            temp_json_path = os.path.join(PROJECT_DIR, "temp_deep_upload_data.json")
            upload_data = {
                "file": video_path,
                "title": yt_title,
                "desc": desc_text,
                "is_short": is_short,
                "thumbnail": thumbnail_path,
                "schedule": schedule_offset
            }
            
            with open(temp_json_path, "w", encoding="utf-8") as f:
                json.dump(upload_data, f, ensure_ascii=False, indent=4)
                
            # Invoke Node Puppeteer uploader
            cmd = ["node", uploader_script, "--json", temp_json_path]
            print(f"[UPLOAD] Launching uploader for {key}...")
            
            res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
            
            # Clean up config file
            try:
                os.remove(temp_json_path)
            except:
                pass
                
            print("Stdout:")
            print(res.stdout)
            
            if res.returncode == 0 and "Video published successfully!" in res.stdout:
                print(f"[SUCCESS] Upload completed successfully for {key}!\n")
                register_upload(video_path)
                # Small cool-down wait before proceeding to the next video
                time.sleep(20)
            else:
                print(f"[ERROR] Upload process failed for {key}. Details:")
                print(res.stderr)
                print("Retrying in 60 seconds...")
                time.sleep(60)
                break # Break out to retry the same video
                
        # If all items in queue are processed, wait 60 seconds and check manifest again
        time.sleep(60)

if __name__ == "__main__":
    main()
