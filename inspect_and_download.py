import os
import sys
import subprocess
import urllib.request
import urllib.error

# Configure standard output to UTF-8 to prevent encoding issues on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Audio files to inspect
AUDIO_FILES = [
    r"C:\Users\jegom\shorts_project\audio_rts.mp3",
    r"C:\Users\jegom\shorts_project\audio_city.mp3",
    r"C:\Users\jegom\shorts_project\audio_arpg.mp3"
]

# Games and their App IDs by category
GAMES_DATA = {
    "RTS": {
        "Age of Empires IV": 1466860,
        "Company of Heroes 3": 1675900,
        "Dune: Spice Wars": 1171690,
        "Age of Mythology: Retold": 1934680,
        "Sins of a Solar Empire II": 1575940
    },
    "City Builder": {
        "Against the Storm": 1336490,
        "Frostpunk 2": 1601580,
        "Farthest Frontier": 1044720,
        "Manor Lords": 1363080,
        "Satisfactory": 526870
    },
    "ARPG": {
        "The Witcher 3": 292030,
        "Grim Dawn": 219990,
        "Monster Hunter: World": 582010,
        "Cyberpunk 2077": 1091500,
        "Diablo IV": 2344520
    }
}

CAPSULES_DIR = r"C:\Users\jegom\shorts_project\capsules"

def get_audio_duration(file_path):
    """Gets the duration of an audio file in seconds using ffprobe."""
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        duration_str = result.stdout.strip()
        duration = float(duration_str)
        return f"{duration:.3f} seconds"
    except subprocess.CalledProcessError as e:
        return f"Error running ffprobe: {e.stderr.strip()}"
    except ValueError:
        return f"Could not parse duration from ffprobe output: {result.stdout.strip()}"

def download_image(appid, dest_path):
    """Downloads a Steam library capsule image using the primary URL or the fallback URL."""
    url_primary = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg"
    url_fallback = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/library_600x900.jpg"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Try primary URL
    req = urllib.request.Request(url_primary, headers=headers)
    try:
        print(f"  Attempting primary URL for App ID {appid}...")
        with urllib.request.urlopen(req, timeout=10) as response:
            with open(dest_path, 'wb') as out_file:
                out_file.write(response.read())
        return True, "Primary CDN"
    except Exception as e:
        print(f"  Primary URL failed: {e}. Trying fallback URL...")
        
        # Try fallback URL
        req_fallback = urllib.request.Request(url_fallback, headers=headers)
        try:
            with urllib.request.urlopen(req_fallback, timeout=10) as response:
                with open(dest_path, 'wb') as out_file:
                    out_file.write(response.read())
            return True, "Fallback CDN"
        except Exception as ef:
            print(f"  Fallback URL also failed: {ef}")
            return False, str(ef)

def main():
    print("=== Phase 1: Inspecting Audio Durations ===")
    for audio_file in AUDIO_FILES:
        name = os.path.basename(audio_file)
        duration = get_audio_duration(audio_file)
        print(f"{name}: {duration}")
    
    print("\n=== Phase 2: Downloading Steam Capsule Images ===")
    if not os.path.exists(CAPSULES_DIR):
        os.makedirs(CAPSULES_DIR, exist_ok=True)
        print(f"Created capsules directory: {CAPSULES_DIR}")
        
    downloaded_files = []
    failures = []
    
    for category, games in GAMES_DATA.items():
        print(f"\nCategory: {category}")
        for game_name, appid in games.items():
            # Create a clean filename
            safe_name = game_name.replace(":", "").replace(" ", "_").replace("'", "").lower()
            filename = f"{safe_name}_{appid}.jpg"
            dest_path = os.path.join(CAPSULES_DIR, filename)
            
            print(f"Downloading capsule for '{game_name}' (App ID: {appid})...")
            success, source_or_err = download_image(appid, dest_path)
            
            if success:
                print(f"  [SUCCESS] Saved to: {dest_path} (from {source_or_err})")
                downloaded_files.append(dest_path)
            else:
                print(f"  [FAILED] Reason: {source_or_err}")
                failures.append((game_name, appid, source_or_err))
                
    print("\n=== Summary ===")
    print(f"Successfully downloaded: {len(downloaded_files)} / {sum(len(g) for g in GAMES_DATA.values())}")
    if failures:
        print("Failures:")
        for name, appid, err in failures:
            print(f"  - {name} ({appid}): {err}")
    else:
        print("All downloads completed successfully!")

if __name__ == "__main__":
    main()
