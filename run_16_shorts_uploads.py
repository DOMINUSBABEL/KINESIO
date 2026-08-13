import os
import sys
import time
import subprocess

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
uploaded_log_path = os.path.join(PROJECT_DIR, "uploaded_16_shorts_gates_of_hell.txt")
uploader_script = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

SHORTS_16_METADATA_EN = {
    "gates_of_hell_short_1": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_1_final.mp4"),
        "title": "When a 150mm Artillery Shell Hits a Bunker Point-Blank... 💣 #shorts",
        "desc": "What happens when heavy howitzer shells drop directly onto fortified defensive positions? Pure battlefield destruction in Call to Arms: Gates of Hell: Ostfront. #gatesofhell #artillery #ww2 #gaming #shorts",
        "is_short": True
    },
    "gates_of_hell_short_2": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_2_final.mp4"),
        "title": "This Tank Shell Hit the Ammo Rack & Sent the Turret into Orbit 💥 #shorts",
        "desc": "One precise armor-piercing round hit the internal ammunition magazine, causing an instant turret pop explosion. #gatesofhell #tank #explosion #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_3": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_3_final.mp4"),
        "title": "Hidden in the Bush at 10 Meters: The Ultimate Anti-Tank Trap 🚜 #shorts",
        "desc": "The Soviet T-26 tank didn't see the concealed PaK 36 anti-tank gun until it was too late. Absolute point-blank ambush. #gatesofhell #tank #ambush #gaming #shorts",
        "is_short": True
    },
    "gates_of_hell_short_4": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_4_final.mp4"),
        "title": "They Ran at a 30-Ton T-34 Tank with Molotov Cocktails... 🔥 #shorts",
        "desc": "Desperate infantry charge: throwing glass bottles filled with fuel directly onto the hot engine deck of a Soviet T-34 tank. #gatesofhell #ww2 #tank #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_5": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_5_final.mp4"),
        "title": "Can a $5 Magnetic Charge Stop a 45-Ton Soviet KV-1 Monster? 👺 #shorts",
        "desc": "Bouncing heavy tank shells off impenetrable front armor, one soldier crawls underneath to attach a magnetic mine. #gatesofhell #kv1 #tank #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_6": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_6_final.mp4"),
        "title": "Finding the Enemy Howitzer by Sound... Then Wiping It Out 💥 #shorts",
        "desc": "High-stakes counter-battery artillery duel: pinpointing the exact coordinates of enemy heavy guns and detonating their ammo crates. #gatesofhell #artillery #ww2 #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_7": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_7_final.mp4"),
        "title": "This Solo Finnish Sniper Took Out an Entire Officer Squad... 🎯 #shorts",
        "desc": "Third-person direct control manual sniping deep in snow-covered woods. Every single bullet counts. #gatesofhell #sniper #headshot #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_8": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_8_final.mp4"),
        "title": "The Brutal Submachine Gun Soviet Troops Feared the Most... 🗡️ #shorts",
        "desc": "Clearing an entire enemy trench line single-handedly using the legendary 900 RPM Suomi KP/-31 submachine gun in Direct Control. #gatesofhell #ww2 #infantry #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_9": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_9_final.mp4"),
        "title": "Driving a 6-Wheeled Armored Car Straight Through Enemy Lines 🚘 #shorts",
        "desc": "Flanking behind enemy lines at high speed, spraying 45mm autocannon rounds and machine gun fire in third-person direct control. #gatesofhell #armoredcar #ww2 #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_10": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_10_final.mp4"),
        "title": "He Lay Prone for 3 Minutes & Let the Enemy Walk Past Him... 🌲 #shorts",
        "desc": "Ultimate patience and stealth: holding fire until enemy infantry are literally stepping 5 meters away before pulling the trigger. #gatesofhell #stealth #ambush #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_11": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_11_final.mp4"),
        "title": "He Stole the Enemy's Abandoned Tank & Turned the Turret 🎮 #shorts",
        "desc": "Crawling under fire, jumping inside a disabled Soviet tank, and blasting the enemy from behind their own line in direct control. #gatesofhell #tank #clutch #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_12": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_12_final.mp4"),
        "title": "They Trapped an Entire Armored Convoy on a Single Bridge... 🌉 #shorts",
        "desc": "Blowing up the lead truck on a narrow wooden bridge, trapping the entire reinforcement column under heavy crossfire. #gatesofhell #convoy #bridge #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_13": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_13_final.mp4"),
        "title": "0 Ammo Left & MG Fire Everywhere: He Crawled Out to Loot 🎒 #shorts",
        "desc": "Out of ammunition in a pinned-down trench, a soldier crawls between bullet impacts to retrieve anti-tank grenades from fallen soldiers. #gatesofhell #clutch #survival #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_14": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_14_final.mp4"),
        "title": "First 60 Seconds of a Winter War Ambush... Absolute Chaos 🌲 #shorts",
        "desc": "Intense tactical opening clash in dense pine woods: muzzle flashes lighting up snow and smoke under heavy fire. #gatesofhell #combat #ww2 #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_15": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_15_final.mp4"),
        "title": "10 Soldiers vs 500 Enemy Troops... Can They Hold the Line? 🛡️ #shorts",
        "desc": "Holding the Mannerheim defensive trench system against wave after wave of enemy infantry and light armor. #gatesofhell #epic #defense #shorts #gaming",
        "is_short": True
    },
    "gates_of_hell_short_16": {
        "file": os.path.join(PROJECT_DIR, "gates_of_hell_short_16_final.mp4"),
        "title": "The Moment the Entire Army Charged the Last Stronghold 🏆 #shorts",
        "desc": "Combined arms final assault: infantry, armor, and artillery storming the main enemy stronghold to achieve complete victory. #gatesofhell #victory #epic #shorts #gaming",
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
    if not os.path.exists(uploader_script):
        print(f"[SKIP UPLOAD] Script {uploader_script} not found.")
        return False
    print(f"\n[UPLOAD PRIVATE] Uploading to DOMINUSBABEL: {title}...")
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
        print(f"[SUCCESS] Uploaded: {title}")
        return True
    else:
        print(f"[ERROR] Upload failed for: {title}")
        print("Output:", res.stdout[:500] if res.stdout else "No stdout")
        print("Error:", res.stderr[:500] if res.stderr else "No stderr")
        return False

def main():
    print("====================================================")
    print("SEO & UPLOAD MANAGER: 16 CALL TO ARMS SHORTS (DOMINUSBABEL)")
    print("====================================================\n")
    
    uploaded = load_uploaded()
    queue = list(SHORTS_16_METADATA_EN.items())
    
    pending = [item for item in queue if item[1]["file"] not in uploaded]
    
    if not pending:
        print("✅ All 16 Shorts have already been uploaded to DOMINUSBABEL!")
        return
        
    print(f"Found {len(pending)} pending Shorts to upload to DOMINUSBABEL.\n")
    
    for key, info in pending:
        vpath = info["file"]
        if os.path.exists(vpath) and os.path.getsize(vpath) > 100000:
            success = run_upload(vpath, info["title"], info["desc"], info["is_short"])
            if success:
                register_upload(vpath)
                print(f"[STATUS] Progress: {len(load_uploaded())}/{len(queue)} uploaded.")
                print("Waiting 15 seconds before next upload...")
                time.sleep(15)
            else:
                print(f"[WARN] Skipping {key} due to upload error.")
        else:
            print(f"[WARN] File {vpath} not ready or missing. Skipping.")

if __name__ == "__main__":
    main()
