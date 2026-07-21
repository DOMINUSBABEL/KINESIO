import os
import subprocess

BASE_DIR = r"C:\Users\jegom\shorts_project"
VIDEO_PATH = os.path.join(BASE_DIR, "tesla_ref.mp4")
OUTPUT_DIR = os.path.join(BASE_DIR, "screenshots")

TIMESTAMPS = {
    "tesla_ref_1": 30,    # Jay Vijayan / Intro
    "tesla_ref_2": 120,   # 2008 Tesla payroll crisis
    "tesla_ref_3": 240,   # Model S & Master Plan
    "tesla_ref_4": 360,   # Traditional automotive vs Tesla
    "tesla_ref_5": 480,   # The SAP ERP problem
    "tesla_ref_6": 600,   # Elon Musk hires Jay Vijayan
    "tesla_ref_7": 720,   # Warp Drive ERP built in 4 months
    "tesla_ref_8": 840,   # Factory line integration
    "tesla_ref_9": 960,   # Data agility & success
    "tesla_ref_10": 1050  # Why legacy auto stays on SAP
}

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("====================================================")
    print("Extracting frames from Tesla SAP reference video")
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
