import os
import sys
import json
import time
import subprocess
from datetime import datetime, timedelta

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\reddit_shorts_project"
manifest_path = os.path.join(PROJECT_DIR, "manifest.json")
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_reddit.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_reddit.js"

VIRAL_TITLES = {
    1: "Descubrí el PEOR secreto de mi abuelo en su sótano... 🤫🚪",
    2: "Arruiné la boda de mi cuñada revelando su secreto en el altar 👰🔥",
    3: "¡El tiempo se detuvo por 10 segundos y vi algo aterrador! 🕰️😱",
    4: "Destruí la carrera de mi jefe abusivo tras 20 años 💼💥",
    5: "Subí las extrañas escaleras del bosque y no debí hacerlo... 🌲👣",
    6: "La prueba de ADN de mi bebé pelirrojo reveló esta locura 👶🧪",
    7: "Este juego de realidad virtual sabía DEMASIADO sobre mí... 🎮👁️",
    8: "Humillé a un cliente prepotente con una pintura de $50,000 🎨💸",
    9: "Escuché un golpe rítmico bajo tierra y descubrí esto... 🚪🔨",
    10: "Mi llave abre el apartamento 404... pero ese piso NO EXISTE 🔑🏢",
    11: "Cancelé el viaje de mi familia por culpa del ex de mi esposa ✈️😡",
    12: "Mi tío millonario me dejó su herencia con esta condición 💰📜",
    13: "Un becario destruyó a un fondo de inversión corrupto de esta forma 📉🔥",
    14: "Nadie más podía ver al pasajero del asiento 14B... ✈️👻",
    15: "Entré a una tienda que vendía fotos de mi propio futuro... 📸🔮"
}

def load_manifest():
    if not os.path.exists(manifest_path):
        return []
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

LAUNCH_TIME = datetime.now()

def get_schedule_time(index):
    # The first video is scheduled to publish in 15 minutes, with subsequent videos spaced by exactly 30 minutes
    target_time = LAUNCH_TIME + timedelta(minutes=15 + index * 30)
    return target_time

def main():
    print("====================================================")
    print("REDDIT SHORTS AUTOMATED UPLOAD PIPELINE")
    print("====================================================\n")
    
    while True:
        manifest = load_manifest()
        uploaded = load_uploaded()
        
        if not manifest:
            print("[INFO] No items found in manifest.json. Waiting 30 seconds...")
            time.sleep(30)
            continue
            
        pending_items = []
        for idx, item in enumerate(manifest):
            key = item["key"]
            video_path = os.path.join(PROJECT_DIR, f"{key}_final.mp4")
            
            if video_path in uploaded:
                continue
                
            pending_items.append((idx, item, video_path))
            
        if not pending_items:
            print("\n✅ All 45 Reddit shorts are successfully uploaded and scheduled!")
            break
            
        # Process the first pending item
        idx, item, video_path = pending_items[0]
        key = item["key"]
        story_title = item["story_title"]
        part_title = item["part_title"]
        part_num = item["part_num"]
        total_parts = item["total_parts"]
        voiceover_text = item["voiceover"]
        
        # Check if the video file exists on disk
        if not os.path.exists(video_path) or os.path.getsize(video_path) == 0:
            print(f"[STATUS] Next pending: {key} (Part {part_num} of {total_parts})")
            print(f"  -> File not compiled yet: {video_path}")
            print("  -> Waiting 60 seconds for rendering to catch up...")
            time.sleep(60)
            continue
            
        # Video is compiled! Let's schedule it
        target_time = get_schedule_time(idx)
        now = datetime.now()
        
        # Calculate offset in minutes
        delta = target_time - now
        schedule_offset = int(delta.total_seconds() / 60)
        
        if schedule_offset <= 0:
            # Fallback to immediate public release or small offset if we fell behind
            schedule_offset = 15
            
        print(f"\n[QUEUE] Processing: {part_title}")
        print(f"  Video: {video_path}")
        print(f"  Schedule target: {target_time.strftime('%Y-%m-%d %H:%M')} (In {schedule_offset} minutes)")
        
        # Extract story number from the key (e.g. reddit_story_1_part_1 -> 1)
        story_num = int(key.split("_")[2])
        viral_title = VIRAL_TITLES.get(story_num, story_title)
        
        # Title of the short on YouTube (include hashtags for viral reach)
        yt_title = f"{viral_title} (Parte {part_num}/{total_parts}) #reddit #historias #shorts"
        if len(yt_title) > 100:
            yt_title = yt_title[:95] + "..."
            
        # Description
        desc_text = (
            f"Historia: {viral_title}\n"
            f"Parte {part_num} de {total_parts}.\n\n"
            f"Narra las mejores historias virales, relatos paranormales, dramas familiares y anécdotas curiosas de los foros de Reddit.\n\n"
            f"#reddit #historias #shorts #relatos #drama #terror #misterio #redditstories"
        )
        
        # Write JSON data to temporary file to bypass Windows command line encoding issues
        temp_json_path = os.path.join(PROJECT_DIR, "temp_upload_data.json")
        upload_data = {
            "file": video_path,
            "title": yt_title,
            "desc": desc_text,
            "is_short": True,
            "schedule": schedule_offset
        }
        with open(temp_json_path, "w", encoding="utf-8") as json_f:
            json.dump(upload_data, json_f, ensure_ascii=False, indent=4)

        # Run node uploader script
        cmd = [
            "node", uploader_script,
            "--json", temp_json_path
        ]
        
        print(f"[UPLOAD] Launching uploader for: {yt_title}...")
        res = subprocess.run(cmd, cwd=r"C:\Users\jegom\VAREGO", capture_output=True, text=True, encoding="utf-8")
        
        print("Stdout:")
        print(res.stdout)
        
        if res.returncode == 0 and "Video published successfully" in res.stdout:
            print(f"[SUCCESS] Upload completed successfully for: {yt_title}")
            register_upload(video_path)
            print("Waiting 20 seconds before processing next video...")
            time.sleep(20)
        else:
            print(f"[ERROR] Failed to upload: {yt_title}")
            print("Stderr:")
            print(res.stderr)
            print("Retrying in 60 seconds...")
            time.sleep(60)

if __name__ == "__main__":
    main()
