import os
import sys
import time
import subprocess

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_gates_of_hell.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

# 21 Shorts (15 Standard + 6 Special Compilations 35s-55s) - English SEO Metadata
SHORTS_METADATA = {
    # 15 Standard Dynamic Shorts
    "gates_of_hell_short_1": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_1_final.mp4"),
        "title": "5 INSANE TANK TURRET POPS 💥 #shorts",
        "desc": "Best tank explosions and turret pops in Call to Arms: Gates of Hell: Ostfront. #gatesofhell #tank #explosion #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_2": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_2_final.mp4"),
        "title": "EXTREME SNIPER KILLSHOTS IN DIRECT CONTROL 💀 #shorts",
        "desc": "Insane 3rd-person sniper headshots and officer eliminations in Gates of Hell. #gatesofhell #sniper #headshot #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_3": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_3_final.mp4"),
        "title": "ARTILLERY BARRAGE OBLITERATION 💣 #shorts",
        "desc": "Heavy mortar and howitzer strikes tearing down enemy bunkers in Gates of Hell. #gatesofhell #artillery #explosion #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_4": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_4_final.mp4"),
        "title": "SUOMI KP/-31 TRENCH WIPES 🗡️ #shorts",
        "desc": "Brutal close-quarters trench clearing with Suomi submachine guns and bayonets. #gatesofhell #ww2 #infantry #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_5": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_5_final.mp4"),
        "title": "PaK 36 AMBUSH VS SOVIET T-26 TANK 🚜 #shorts",
        "desc": "Anti-tank gun crossfire trap obliterating an advancing T-26 light tank. #gatesofhell #tank #ambush #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_6": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_6_final.mp4"),
        "title": "SAVAGE TANK TRACK DESTRUCTION ⛓️ #shorts",
        "desc": "Precise track-shots disabling enemy armor into sitting ducks. #gatesofhell #tank #tactic #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_7": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_7_final.mp4"),
        "title": "KV-1 MONSTER TANK VS MAGNETIC MINE 👹 #shorts",
        "desc": "Bouncing shells off heavy KV-1 armor and placing a side magnetic charge. #gatesofhell #kv1 #tank #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_8": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_8_final.mp4"),
        "title": "BA-10 ARMORED CAR SNOWFIELD SWEEP 🚘 #shorts",
        "desc": "High-speed armored vehicle sweep suppressing enemy infantry lines. #gatesofhell #ww2 #armoredcar #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_9": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_9_final.mp4"),
        "title": "BRIDGE BOTTLENECK CONVOY MASSACRE 🌉 #shorts",
        "desc": "Trapping a Soviet convoy on a wooden bridge and unleashing artillery. #gatesofhell #explosion #convoy #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_10": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_10_final.mp4"),
        "title": "0 AMMO TRENCH CLUTCH: SCAVENGING UNDER FIRE 🎒 #shorts",
        "desc": "Out of ammo clutch: crawling under machine gun fire to loot AT grenades. #gatesofhell #clutch #logistics #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_11": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_11_final.mp4"),
        "title": "COUNTER-BATTERY ARTILLERY DUEL 💣 #shorts",
        "desc": "Calculating enemy howitzer positions and launching counter-battery salvo. #gatesofhell #artillery #ww2 #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_12": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_12_final.mp4"),
        "title": "STEALTH AMBUSH AT 5 METERS 🌲 #shorts",
        "desc": "Prone stealth in birch forest, letting enemy pass 5 meters before opening fire. #gatesofhell #ambush #stealth #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_13": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_13_final.mp4"),
        "title": "CAPTURED TANK POINT BLANK BLAST 🎮 #shorts",
        "desc": "Boarding abandoned Soviet tank in Direct Control and blasting enemy armor point blank. #gatesofhell #tank #ww2 #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_14": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_14_final.mp4"),
        "title": "MOLOTOV VS T-34 ENGINE ENGINE FIRE 🛑 #shorts",
        "desc": "T-34 breaking fence and infantry charging with Molotovs to ignite engine. #gatesofhell #tank #molotov #rts #shorts #dominus",
        "is_short": True
    },
    "gates_of_hell_short_15": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_15_final.mp4"),
        "title": "THE FINAL VICTORY CHARGE 🏆 #shorts",
        "desc": "Combined arms final assault with all remaining forces securing victory. #gatesofhell #victory #ww2 #rts #shorts #dominus",
        "is_short": True
    },

    # 6 Special Extended Compilations (35s - 55s)
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
    print(f"\n[UPLOAD PRIVATE] Launching VAREGO uploader (PRIVATE/DRAFT) for: {title}...")
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
        print(f"[SUCCESS] Private Upload completed for: {title}")
        return True
    else:
        print(f"[ERROR] Upload failed for: {title}")
        print("Stdout:", res.stdout)
        print("Stderr:", res.stderr)
        return False

def main():
    print("====================================================")
    print("VAREGO AUTOMATED PRIVATE UPLOADER - 21 SHORTS (15 + 6 SPECIALS)")
    print("====================================================\n")
    
    queue = list(SHORTS_METADATA.items())
    
    while True:
        uploaded = load_uploaded()
        pending = [item for item in queue if item[1]["file"] not in uploaded]
        
        if not pending:
            print("\n✅ All 21 Dynamic Gates of Hell Shorts have been uploaded as PRIVATE to DOMINUSBABEL!")
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
                print(f"[STATUS] Progress: {len(load_uploaded())}/{len(queue)} uploaded as PRIVATE.")
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
