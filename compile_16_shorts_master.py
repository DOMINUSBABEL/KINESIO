import os
import sys
import shutil
import subprocess

# Fix Windows console UTF-8 printing
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
MUSIC_DIR = os.path.join(PROJECT_DIR, "music")
VIDEO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_720p.mp4")
AUDIO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_audio.webm")

# 16 VIRAL PSYCHOLOGICAL HOOK SHORTS SPECIFICATIONS
SHORTS_16_SPEC = [
    # --- CATEGORY 1: EXPLOSIONS & TANK/ARTILLERY DESTRUCTION ---
    {
        "id": 1,
        "category": "Explosions & Tanks",
        "title_en": "When a 150mm Artillery Shell Hits a Bunker Point-Blank... 💣 #shorts",
        "banner": "150mm ARTILLERY vs ENEMY BUNKER",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:03:48", "00:03:57"), ("00:35:05", "00:35:14"), ("00:35:25", "00:35:35"), ("00:43:25", "00:43:35")]
    },
    {
        "id": 2,
        "category": "Explosions & Tanks",
        "title_en": "This Tank Shell Hit the Ammo Rack & Sent the Turret into Orbit 💥 #shorts",
        "banner": "AMMO RACK BLAST: TURRET FLIES 100m",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:06:42", "00:06:51"), ("00:13:02", "00:13:12"), ("00:27:38", "00:27:48"), ("00:47:30", "00:47:40")]
    },
    {
        "id": 3,
        "category": "Explosions & Tanks",
        "title_en": "Hidden in the Bush at 10 Meters: The Ultimate Anti-Tank Trap 🚜 #shorts",
        "banner": "10m ANTI-TANK AMBUSH TRAP",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:06:22", "00:06:31"), ("00:06:33", "00:06:41"), ("00:06:42", "00:06:50")]
    },
    {
        "id": 4,
        "category": "Explosions & Tanks",
        "title_en": "They Ran at a 30-Ton T-34 Tank with Molotov Cocktails... 🔥 #shorts",
        "banner": "MOLOTOV CHARGE VS T-34 ENGINE",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:12:32", "00:12:41"), ("00:12:48", "00:12:57"), ("00:13:03", "00:13:14")]
    },
    {
        "id": 5,
        "category": "Explosions & Tanks",
        "title_en": "Can a $5 Magnetic Charge Stop a 45-Ton Soviet KV-1 Monster? 👺 #shorts",
        "banner": "MAGNETIC CHARGE VS 45-TON KV-1",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:27:12", "00:27:22"), ("00:27:28", "00:27:37"), ("00:27:40", "00:27:50")]
    },
    {
        "id": 6,
        "category": "Explosions & Tanks",
        "title_en": "Finding the Enemy Howitzer by Sound... Then Wiping It Out 💥 #shorts",
        "banner": "COUNTER-BATTERY: SOUND TRACKING",
        "music": "Clash Defiant.mp3",
        "clips": [("00:35:02", "00:35:12"), ("00:35:16", "00:35:25"), ("00:35:28", "00:35:38")]
    },

    # --- CATEGORY 2: 3RD PERSON DIRECT CONTROL COMPILATIONS ---
    {
        "id": 7,
        "category": "3rd Person Control",
        "title_en": "This Solo Finnish Sniper Took Out an Entire Officer Squad... 🎯 #shorts",
        "banner": "SOLO SNIPER vs ENEMY OFFICERS",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:09:12", "00:09:22"), ("00:09:24", "00:09:33"), ("00:09:35", "00:09:44"), ("00:39:35", "00:39:44")]
    },
    {
        "id": 8,
        "category": "3rd Person Control",
        "title_en": "The Brutal Submachine Gun Soviet Troops Feared the Most... 🗡️ #shorts",
        "banner": "THE MOST FEARED TRENCH WEAPON",
        "music": "Clash Defiant.mp3",
        "clips": [("00:19:15", "00:19:24"), ("00:19:26", "00:19:35"), ("00:19:37", "00:19:46")]
    },
    {
        "id": 9,
        "category": "3rd Person Control",
        "title_en": "Driving a 6-Wheeled Armored Car Straight Through Enemy Lines 🚘 #shorts",
        "banner": "HIGH-SPEED ARMORED CAR RAID",
        "music": "Clash Defiant.mp3",
        "clips": [("00:23:03", "00:23:13"), ("00:23:16", "00:23:25"), ("00:23:28", "00:23:38")]
    },
    {
        "id": 10,
        "category": "3rd Person Control",
        "title_en": "He Lay Prone for 3 Minutes & Let the Enemy Walk Past Him... 🌲 #shorts",
        "banner": "PRONE FOR 3 MINS: 5m AMBUSH",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:39:20", "00:39:28"), ("00:39:30", "00:39:38"), ("00:39:40", "00:39:48")]
    },
    {
        "id": 11,
        "category": "3rd Person Control",
        "title_en": "He Stole the Enemy's Abandoned Tank & Turned the Turret 🎮 #shorts",
        "banner": "STEALING THE ENEMY'S TANK",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:47:12", "00:47:21"), ("00:47:24", "00:47:33"), ("00:47:36", "00:47:46")]
    },

    # --- CATEGORY 3: EPIC BATTLE MOMENTS ---
    {
        "id": 12,
        "category": "Epic Battle Moments",
        "title_en": "They Trapped an Entire Armored Convoy on a Single Bridge... 🌉 #shorts",
        "banner": "CONVOY TRAPPED ON A BRIDGE",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:43:03", "00:43:13"), ("00:43:16", "00:43:26"), ("00:43:28", "00:43:38")]
    },
    {
        "id": 13,
        "category": "Epic Battle Moments",
        "title_en": "0 Ammo Left & MG Fire Everywhere: He Crawled Out to Loot 🎒 #shorts",
        "banner": "0 AMMO: DESPERATE TRENCH LOOT",
        "music": "Clash Defiant.mp3",
        "clips": [("00:31:32", "00:31:42"), ("00:31:45", "00:31:54"), ("00:31:57", "00:32:07")]
    },
    {
        "id": 14,
        "category": "Epic Battle Moments",
        "title_en": "First 60 Seconds of a Winter War Ambush... Absolute Chaos 🌲 #shorts",
        "banner": "FIRST 60 SECONDS OF AMBUSH",
        "music": "Clash Defiant.mp3",
        "clips": [("00:01:15", "00:01:25"), ("00:01:28", "00:01:38"), ("00:01:40", "00:01:50")]
    },
    {
        "id": 15,
        "category": "Epic Battle Moments",
        "title_en": "10 Soldiers vs 500 Enemy Troops... Can They Hold the Line? 🛡️ #shorts",
        "banner": "CAN 10 MEN HOLD THE LINE?",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:16:02", "00:16:11"), ("00:16:14", "00:16:23"), ("00:16:25", "00:16:34")]
    },
    {
        "id": 16,
        "category": "Epic Battle Moments",
        "title_en": "The Moment the Entire Army Charged the Last Stronghold 🏆 #shorts",
        "banner": "THE FINAL ALL-OUT CHARGE",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:51:02", "00:51:12"), ("00:51:15", "00:51:25"), ("00:51:30", "00:51:42")]
    }
]

def safe_replace(src, dst):
    if not os.path.exists(src):
        return
    if os.path.exists(dst):
        try:
            os.remove(dst)
        except Exception:
            pass
    try:
        os.replace(src, dst)
    except Exception:
        try:
            shutil.copy(src, dst)
            os.remove(src)
        except Exception as e:
            print(f"    [WARN] Could not move {src} to {dst}: {e}")

def render_single_short(spec):
    output_filename = f"gates_of_hell_short_{spec['id']}_final.mp4"
    output_path = os.path.join(PROJECT_DIR, output_filename)
    music_file = os.path.join(MUSIC_DIR, spec['music'])
    
    print(f"\n==========================================================")
    print(f"[+] Rendering Short #{spec['id']} [{spec['category']}]")
    print(f"    Title: {spec['title_en']}")
    print(f"    Banner: {spec['banner']}")
    print(f"    Music: {spec['music']}")
    print(f"==========================================================")
    
    banner_clean = spec['banner'].replace(":", "\\:").replace("'", "")
    temp_clips = []
    
    for idx, (start_t, end_t) in enumerate(spec["clips"]):
        clip_path = os.path.join(PROJECT_DIR, f"subclip_m_{spec['id']}_{idx}.mp4")
        
        video_filter = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920,"
            "eq=contrast=1.12:brightness=0.02:saturation=1.2,"
            "unsharp=5:5:0.8:5:5:0.0,"
            f"drawtext=text='{banner_clean}':fontcolor=yellow:fontsize=40:x=(w-text_w)/2:y=180:box=1:boxcolor=black@0.7:boxborderw=12"
        )
        
        cmd_sub = [
            "ffmpeg", "-y",
            "-ss", start_t, "-to", end_t, "-i", VIDEO_SOURCE,
            "-ss", start_t, "-to", end_t, "-i", AUDIO_SOURCE,
            "-vf", video_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "60",
            "-c:a", "aac", "-b:a", "192000",
            clip_path
        ]
        
        res = subprocess.run(cmd_sub, capture_output=True, text=True)
        if res.returncode == 0 and os.path.exists(clip_path) and os.path.getsize(clip_path) > 0:
            temp_clips.append(clip_path)
        else:
            print(f"    [WARN] Subclip {idx} failed: {res.stderr[:200] if res.stderr else 'Error'}")

    if not temp_clips:
        print(f"[ERROR] Could not generate subclips for Short #{spec['id']}")
        return False
        
    concat_list_file = os.path.join(PROJECT_DIR, f"concat_{spec['id']}.txt")
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for c in temp_clips:
            f.write(f"file '{c.replace(os.sep, '/')}'\n")
            
    merged_raw = os.path.join(PROJECT_DIR, f"merged_raw_{spec['id']}.mp4")
    cmd_concat = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list_file,
        "-c", "copy", merged_raw
    ]
    subprocess.run(cmd_concat, capture_output=True)
    
    # Audio mixing: gameplay original audio (vol 1.0) + background music (vol 0.07 / -23dB)
    if os.path.exists(music_file) and os.path.exists(merged_raw):
        audio_filter = "[0:a]volume=1.0[a1];[1:a]volume=0.07[a2];[a1][a2]amix=inputs=2:duration=first[a]"
        cmd_final = [
            "ffmpeg", "-y",
            "-i", merged_raw, "-i", music_file,
            "-filter_complex", audio_filter,
            "-map", "0:v", "-map", "[a]",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192000",
            "-shortest", output_path
        ]
        res_f = subprocess.run(cmd_final, capture_output=True, text=True)
        if res_f.returncode != 0 or not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
            safe_replace(merged_raw, output_path)
    else:
        if os.path.exists(merged_raw):
            safe_replace(merged_raw, output_path)
            
    # Cleanup temporary files
    for c in temp_clips:
        try: os.remove(c)
        except: pass
    try: os.remove(concat_list_file)
    except: pass
    try: os.remove(merged_raw)
    except: pass

    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"    [SUCCESS] Short #{spec['id']} Exported: {output_filename} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"    [ERROR] Final render failed for Short #{spec['id']}")
        return False

def main():
    print("=================================================================")
    print("VIRAL PSYCHOLOGICAL HOOK SHORTS PROCESSOR (16 SHORTS)")
    print("=================================================================")
    
    if not os.path.exists(VIDEO_SOURCE) or not os.path.exists(AUDIO_SOURCE):
        print("ERROR: Video or audio source file missing!")
        return
        
    success = 0
    for spec in SHORTS_16_SPEC:
        if render_single_short(spec):
            success += 1
            
    print(f"\n=================================================================")
    print(f"FINAL SUMMARY: {success} of {len(SHORTS_16_SPEC)} Shorts successfully rendered.")
    print(f"Output folder: {PROJECT_DIR}")
    print("=================================================================")

if __name__ == "__main__":
    main()
