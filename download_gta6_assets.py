import os
import sys
import subprocess

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
os.makedirs(TRAILERS_DIR, exist_ok=True)
os.makedirs(CAPSULES_DIR, exist_ok=True)

GTA6_TRAILER_URL = "https://www.youtube.com/watch?v=QdBZY2fkU-0"
OUTPUT_TRAILER = os.path.join(TRAILERS_DIR, "gta6_trailer.mp4")

def download_trailer():
    print(f"Downloading GTA VI Trailer from: {GTA6_TRAILER_URL}")
    cmd = [
        "yt-dlp",
        "-f", "mp4",
        "-o", OUTPUT_TRAILER,
        GTA6_TRAILER_URL
    ]
    try:
        # Clear environment variables that might pollute the subprocess
        sub_env = os.environ.copy()
        for key in ["PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV"]:
            sub_env.pop(key, None)
            
        process = subprocess.run(
            cmd,
            env=sub_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if process.returncode == 0 and os.path.exists(OUTPUT_TRAILER) and os.path.getsize(OUTPUT_TRAILER) > 0:
            print(f"  [SUCCESS] Downloaded GTA 6 Trailer to {OUTPUT_TRAILER}")
            return True
        else:
            print(f"  [FAILED] yt-dlp returned code {process.returncode}: {process.stderr}")
            return False
    except Exception as e:
        print(f"  [ERROR] Running yt-dlp failed: {e}")
        return False

def main():
    print("====================================================")
    print("GTA VI Asset Downloader")
    print("====================================================")
    
    if os.path.exists(OUTPUT_TRAILER) and os.path.getsize(OUTPUT_TRAILER) > 0:
        print("  GTA 6 trailer already exists. Skipping download.")
    else:
        download_trailer()

if __name__ == "__main__":
    main()
