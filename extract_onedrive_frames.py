import os
import subprocess

BASE_DIR = r"C:\Users\jegom\shorts_project"
VIDEO_PATH = os.path.join(BASE_DIR, "onedrive_ref.mp4")
OUTPUT_DIR = os.path.join(BASE_DIR, "screenshots")

TIMESTAMPS = {
    "onedrive_ref_1": 30,    # Windows / OneDrive integration
    "onedrive_ref_2": 90,    # File explorer / backup prompt
    "onedrive_ref_3": 180,   # OneDrive paradox / specs
    "onedrive_ref_4": 270,   # Google Drive / Chromebooks
    "onedrive_ref_5": 360,   # Cloud storage competition
    "onedrive_ref_6": 450,   # Storage quota cuts / Trust issues
    "onedrive_ref_7": 540,   # Sync errors / Notification nags
    "onedrive_ref_8": 630,   # Ecosystem lock-in
    "onedrive_ref_9": 690,   # Microsoft vs Google cloud
    "onedrive_ref_10": 740   # Conclusion / tech strategy
}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("====================================================")
    print("Extracting frames from OneDrive reference video")
    print("====================================================\n")
    
    for key, t_sec in TIMESTAMPS.items():
        out_jpg = os.path.join(OUTPUT_DIR, f"{key}.jpg")
        print(f"Extracting frame at {t_sec}s -> {key}.jpg...")
        
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(t_sec),
            "-i", VIDEO_PATH,
            "-vframes", "1",
            "-q:v", "2",
            out_jpg
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(out_jpg) and os.path.getsize(out_jpg) > 0:
            print(f"  [SUCCESS] Extracted: {out_jpg}")
        else:
            print(f"  [FAILED] Failed to extract frame at {t_sec}s")

if __name__ == "__main__":
    main()
