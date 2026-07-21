import os
import subprocess

BASE_DIR = r"C:\Users\jegom\shorts_project"
VIDEO_PATH = os.path.join(BASE_DIR, "beirut_ref.mp4")
OUTPUT_DIR = os.path.join(BASE_DIR, "screenshots")

# Key timestamps in seconds to extract frames from
TIMESTAMPS = {
    "beirut_ref_1": 90,    # ~1.5m (The ship Rhosus / introduction)
    "beirut_ref_2": 180,   # ~3.0m (Storage / hangar)
    "beirut_ref_3": 270,   # ~4.5m (Warnings / letters)
    "beirut_ref_4": 360,   # ~6.0m (Work / welding)
    "beirut_ref_5": 450,   # ~7.5m (First fire / fireworks)
    "beirut_ref_6": 540,   # ~9.0m (The supersonic blast wave)
    "beirut_ref_7": 630,   # ~10.5m (Dust cloud / explosion moment)
    "beirut_ref_8": 720,   # ~12.0m (Aftermath / city destruction)
    "beirut_ref_9": 810,   # ~13.5m (Silos / ruins)
    "beirut_ref_10": 900   # ~15.0m (Protests / final analysis)
}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("====================================================")
    # Avoid hashtags in logs/output
    print("Extracting frames from Beirut Port Explosion reference video")
    print("====================================================\n")
    
    for key, t_sec in TIMESTAMPS.items():
        out_jpg = os.path.join(OUTPUT_DIR, f"{key}.jpg")
        print(f"Extracting frame at {t_sec}s -> {key}.jpg...")
        
        # Use FFmpeg to seek (-ss) and extract 1 single frame (-vframes 1)
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(t_sec),
            "-i", VIDEO_PATH,
            "-vframes", "1",
            "-q:v", "2",  # High quality
            out_jpg
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(out_jpg) and os.path.getsize(out_jpg) > 0:
            print(f"  [SUCCESS] Extracted: {out_jpg}")
        else:
            print(f"  [FAILED] Failed to extract frame at {t_sec}s")

if __name__ == "__main__":
    main()
