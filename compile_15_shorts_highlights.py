import os
import sys
import subprocess

# Fix Windows console UTF-8 printing
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
MUSIC_DIR = os.path.join(PROJECT_DIR, "music")
VIDEO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_720p.mp4")
AUDIO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_audio.webm")

# 21 Total Dynamic Shorts Specifications (15 Standard + 6 Special 35s-55s Compilations)
COMPILED_SHORTS_SPEC = [
    # --- 15 STANDARD DYNAMIC SHORTS ---
    {
        "id": 1,
        "title_en": "5 INSANE TANK TURRET POPS 💥 #shorts",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:06:45", "00:06:50"), ("00:13:05", "00:13:10"), ("00:27:42", "00:27:48"), ("00:43:25", "00:43:30"), ("00:47:32", "00:47:38")]
    },
    {
        "id": 2,
        "title_en": "EXTREME SNIPER KILLSHOTS IN DIRECT CONTROL 💀 #shorts",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:09:20", "00:09:26"), ("00:09:35", "00:09:42"), ("00:19:25", "00:19:32"), ("00:39:35", "00:39:42")]
    },
    {
        "id": 3,
        "title_en": "ARTILLERY BARRAGE OBLITERATION 💣 #shorts",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:03:52", "00:03:58"), ("00:35:15", "00:35:22"), ("00:35:30", "00:35:37"), ("00:43:30", "00:43:36")]
    },
    {
        "id": 4,
        "title_en": "SUOMI KP/-31 TRENCH WIPES 🗡️ #shorts",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:19:18", "00:19:24"), ("00:19:28", "00:19:34"), ("00:19:38", "00:19:44")]
    },
    {
        "id": 5,
        "title_en": "PaK 36 AMBUSH VS SOVIET T-26 TANK 🚜 #shorts",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:06:25", "00:06:31"), ("00:06:33", "00:06:39"), ("00:06:42", "00:06:48")]
    },
    {
        "id": 6,
        "title_en": "SAVAGE TANK TRACK DESTRUCTION ⛓️ #shorts",
        "music": "Clash Defiant.mp3",
        "clips": [("00:16:05", "00:16:12"), ("00:16:15", "00:16:22"), ("00:16:24", "00:16:29")]
    },
    {
        "id": 7,
        "title_en": "KV-1 MONSTER TANK VS MAGNETIC MINE 👹 #shorts",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:27:15", "00:27:22"), ("00:27:30", "00:27:37"), ("00:27:42", "00:27:48")]
    },
    {
        "id": 8,
        "title_en": "BA-10 ARMORED CAR SNOWFIELD SWEEP 🚘 #shorts",
        "music": "Clash Defiant.mp3",
        "clips": [("00:23:05", "00:23:12"), ("00:23:18", "00:23:25"), ("00:23:30", "00:23:37")]
    },
    {
        "id": 9,
        "title_en": "BRIDGE BOTTLENECK CONVOY MASSACRE 🌉 #shorts",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:43:05", "00:43:12"), ("00:43:18", "00:43:25"), ("00:43:30", "00:43:37")]
    },
    {
        "id": 10,
        "title_en": "0 AMMO TRENCH CLUTCH: SCAVENGING UNDER FIRE 🎒 #shorts",
        "music": "Clash Defiant.mp3",
        "clips": [("00:31:35", "00:31:42"), ("00:31:48", "00:31:55"), ("00:32:00", "00:32:08")]
    },
    {
        "id": 11,
        "title_en": "COUNTER-BATTERY ARTILLERY DUEL 💣 #shorts",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:35:05", "00:35:12"), ("00:35:18", "00:35:25"), ("00:35:30", "00:35:37")]
    },
    {
        "id": 12,
        "title_en": "STEALTH AMBUSH AT 5 METERS 🌲 #shorts",
        "music": "Severe Tire Damage.mp3",
        "clips": [("00:39:23", "00:39:29"), ("00:39:32", "00:39:38"), ("00:39:41", "00:39:47")]
    },
    {
        "id": 13,
        "title_en": "CAPTURED TANK POINT BLANK BLAST 🎮 #shorts",
        "music": "Clash Defiant.mp3",
        "clips": [("00:47:15", "00:47:22"), ("00:47:28", "00:47:35"), ("00:47:40", "00:47:46")]
    },
    {
        "id": 14,
        "title_en": "MOLOTOV VS T-34 ENGINE FIRE 🛑 #shorts",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:12:35", "00:12:42"), ("00:12:50", "00:12:57"), ("00:13:05", "00:13:12")]
    },
    {
        "id": 15,
        "title_en": "THE FINAL VICTORY CHARGE 🏆 #shorts",
        "music": "Volatile Reaction.mp3",
        "clips": [("00:51:05", "00:51:12"), ("00:51:20", "00:51:27"), ("00:51:35", "00:51:42"), ("00:51:44", "00:51:49")]
    },

    # --- 6 SPECIAL EXTENDED RECOMPILATION SHORTS (35s - 55s) ---
    {
        "id": 16,
        "title_en": "SPECIAL #1: ULTIMATE TANK WARFARE COMPILATION 🚜💥 #shorts",
        "music": "Severe Tire Damage.mp3",
        "clips": [
            ("00:06:25", "00:06:32"),
            ("00:06:42", "00:06:49"),
            ("00:12:50", "00:12:57"),
            ("00:16:05", "00:16:12"),
            ("00:27:15", "00:27:22"),
            ("00:27:40", "00:27:48"),
            ("00:47:30", "00:47:38")
        ] # Total ~50s
    },
    {
        "id": 17,
        "title_en": "SPECIAL #2: DIRECT CONTROL SNIPER MASTERCLASS 💀 #shorts",
        "music": "Clash Defiant.mp3",
        "clips": [
            ("00:09:15", "00:09:22"),
            ("00:09:25", "00:09:33"),
            ("00:09:36", "00:09:44"),
            ("00:19:20", "00:19:28"),
            ("00:39:25", "00:39:33"),
            ("00:39:35", "00:39:43")
        ] # Total ~46s
    },
    {
        "id": 18,
        "title_en": "SPECIAL #3: HEAVY ARTILLERY & MORTAR OBLITERATION 💣 #shorts",
        "music": "Volatile Reaction.mp3",
        "clips": [
            ("00:03:50", "00:03:57"),
            ("00:35:05", "00:35:13"),
            ("00:35:16", "00:35:24"),
            ("00:35:28", "00:35:36"),
            ("00:43:25", "00:43:33"),
            ("00:43:35", "00:43:42")
        ] # Total ~46s
    },
    {
        "id": 19,
        "title_en": "SPECIAL #4: BRUTAL INFANTRY TRENCH WARFARE 🗡️ #shorts",
        "music": "Severe Tire Damage.mp3",
        "clips": [
            ("00:19:15", "00:19:23"),
            ("00:19:25", "00:19:33"),
            ("00:19:35", "00:19:43"),
            ("00:31:35", "00:31:43"),
            ("00:31:45", "00:31:53"),
            ("00:39:20", "00:39:28")
        ] # Total ~48s
    },
    {
        "id": 20,
        "title_en": "SPECIAL #5: EPIC CONVOY AMBUSHES & BOTTLENECK DESTRUCTION 🌉 #shorts",
        "music": "Clash Defiant.mp3",
        "clips": [
            ("00:23:05", "00:23:13"),
            ("00:23:18", "00:23:26"),
            ("00:43:05", "00:43:13"),
            ("00:43:16", "00:43:24"),
            ("00:43:27", "00:43:35"),
            ("00:43:37", "00:43:44")
        ] # Total ~46s
    },
    {
        "id": 21,
        "title_en": "SPECIAL #6: 0 AMMO SCAVENGING & IMPOSSIBLE DEFENSES 🏆 #shorts",
        "music": "Volatile Reaction.mp3",
        "clips": [
            ("00:12:35", "00:12:43"),
            ("00:27:15", "00:27:23"),
            ("00:31:35", "00:31:43"),
            ("00:31:48", "00:31:56"),
            ("00:51:05", "00:51:13"),
            ("00:51:20", "00:51:30")
        ] # Total ~50s
    }
]

def compile_highlight_short(spec):
    output_filename = f"gates_of_hell_short_{spec['id']}_final.mp4"
    output_path = os.path.join(PROJECT_DIR, output_filename)
    music_file = os.path.join(MUSIC_DIR, spec['music'])
    
    print(f"\n[+] Compilando Short #{spec['id']} ({len(spec['clips'])} Clips): {spec['title_en']}")
    
    temp_clips = []
    
    for idx, (start_t, end_t) in enumerate(spec["clips"]):
        clip_path = os.path.join(PROJECT_DIR, f"subclip_{spec['id']}_{idx}.mp4")
        
        # Filtro de video dinámico con zoom in 1.4x + enfoque de nitidez
        video_filter = "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,unsharp=5:5:0.8:5:5:0.0"
        
        cmd_sub = [
            "ffmpeg", "-y",
            "-ss", start_t, "-to", end_t, "-i", VIDEO_SOURCE,
            "-ss", start_t, "-to", end_t, "-i", AUDIO_SOURCE,
            "-vf", video_filter,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "60",
            "-c:a", "aac", "-b:a", "192000",
            clip_path
        ]
        subprocess.run(cmd_sub, capture_output=True)
        if os.path.exists(clip_path) and os.path.getsize(clip_path) > 0:
            temp_clips.append(clip_path)
            
    if not temp_clips:
        print(f"[ERROR] No subclips generated for Short {spec['id']}")
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
        subprocess.run(cmd_final, capture_output=True)
    else:
        if os.path.exists(merged_raw):
            os.replace(merged_raw, output_path)
            
    for c in temp_clips:
        try: os.remove(c)
        except: pass
    try: os.remove(concat_list_file)
    except: pass
    try: os.remove(merged_raw)
    except: pass

    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"    [OK] Short #{spec['id']} Exportado: {output_filename} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"    [ERROR] Fallo al exportar Short #{spec['id']}")
        return False

def main():
    print("=================================================================")
    print("Iniciando Compilacion de 21 Shorts Dinamicos HD (15 + 6 Especiales)")
    print("=================================================================")
    
    success = 0
    for spec in COMPILED_SHORTS_SPEC:
        if compile_highlight_short(spec):
            success += 1
            
    print(f"\n================================================ metaphysics ==")
    print(f"RESULTADO DE COMPILACION: {success} de {len(COMPILED_SHORTS_SPEC)} Shorts listos.")
    print(f"Ubicacion: {PROJECT_DIR}")
    print("================================================================")

if __name__ == "__main__":
    main()
