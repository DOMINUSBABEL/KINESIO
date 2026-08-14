import os
import sys
import time
import subprocess

# Ensure UTF-8 output for Windows console
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_gates_of_hell_specials.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

# 6 Special Extended Compilations (Shorts #16 to #21) - English SEO Metadata
SPECIALS_METADATA = {
    "gates_of_hell_short_16": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_16_final.mp4"),
        "title": "SPECIAL #1: ULTIMATE TANK WARFARE COMPILATION 🚜💥 #shorts",
        "desc": "The most destructive tank engagements, turret pops, and armor breaches in Call to Arms: Gates of Hell: Ostfront. #gatesofhell #tanks #ww2 #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_17": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_17_final.mp4"),
        "title": "SPECIAL #2: DIRECT CONTROL SNIPER MASTERCLASS 💀 #shorts",
        "desc": "Insane manual third-person sniping and long-range headshots in Gates of Hell gameplay. #gatesofhell #sniper #headshot #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_18": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_18_final.mp4"),
        "title": "SPECIAL #3: HEAVY ARTILLERY & MORTAR OBLITERATION 💣 #shorts",
        "desc": "Brutal artillery shell drops and total destruction of enemy defensive emplacements. #gatesofhell #artillery #explosion #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_19": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_19_final.mp4"),
        "title": "SPECIAL #4: BRUTAL INFANTRY TRENCH WARFARE 🗡️ #shorts",
        "desc": "Point-blank trench clearings, SMG sweeps, and grenade assaults in Gates of Hell skirmish. #gatesofhell #ww2 #infantry #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_20": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_20_final.mp4"),
        "title": "SPECIAL #5: EPIC CONVOY AMBUSHES & BOTTLENECK DESTRUCTION 🌉 #shorts",
        "desc": "Trapping enemy convoys on narrow bridges and destroying reinforcement columns. #gatesofhell #ambush #convoy #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_21": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_21_final.mp4"),
        "title": "SPECIAL #6: 0 AMMO SCAVENGING & IMPOSSIBLE DEFENSES 🏆 #shorts",
        "desc": "High-stress gameplay clutches, body scavenging under fire, and desperate defensive wins. #gatesofhell #clutch #victory #rts #shorts #dominus",
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
    print(f"\n[UPLOAD SPECIAL PRIVATE] Launching VAREGO uploader (PRIVATE/DRAFT) for: {title}...")
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
        print(f"[SUCCESS] Upload completed for Special: {title}")
        return True
    else:
        print(f"[ERROR] Upload failed for Special: {title}")
        print("Stdout:", res.stdout)
        print("Stderr:", res.stderr)
        return False

def main():
    print("====================================================")
    print("VAREGO AUTOMATED UPLOADER - SPECIAL SHORTS #16 TO #21 (ENGLISH SEO - PRIVATE)")
    print("====================================================\n")
    
    queue = list(SPECIALS_METADATA.items())
    
    while True:
        uploaded = load_uploaded()
        pending = [item for item in queue if item[1]["file"] not in uploaded]
        
        if not pending:
            print("\n✅ All 6 Special Shorts (#16 to #21) have been uploaded as PRIVATE to DOMINUSBABEL!")
            break
            
        ready_item = None
        for item in pending:
            video_path = item[1]["file"]
            if os.path.exists(video_path) and os.path.getsize(video_path) > 1000000:
                ready_item = item
                break
                
        if ready_item:
            key, info = ready_item
            video_path = info["file"]
            success = run_upload(video_path, info["title"], info["desc"], info["is_short"])
            if success:
                register_upload(video_path)
                print(f"[STATUS] Progress: {len(load_uploaded())}/{len(queue)} Specials uploaded as PRIVATE.")
                print("Waiting 15 seconds before next upload...")
                time.sleep(15)
            else:
                print("[WARNING] Upload encountered an error. Retrying in 45 seconds...")
                time.sleep(45)
        else:
            key, info = pending[0]
            print(f"[WAIT] File {key} not ready. Waiting 20 seconds...")
            time.sleep(20)

if __name__ == "__main__":
    main()
