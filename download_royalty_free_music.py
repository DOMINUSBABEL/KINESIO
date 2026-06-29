import os
import sys
import json
import urllib.request

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
MUSIC_DIR = os.path.join(BASE_DIR, "music")
os.makedirs(MUSIC_DIR, exist_ok=True)

CATALOG_URL = "https://incompetech.com/music/royalty-free/pieces.json"
BASE_DOWNLOAD_URL = "https://incompetech.com/music/royalty-free/mp3-royaltyfree/"

# Diverse list of Kevin MacLeod tracks to target for gaming videos
TARGET_TRACKS = [
    # Epic/Action/Combat
    "Volatile Reaction",
    "Clash Defiant",
    "Unconquered",
    
    # Medieval/Fantasy (Warband, Chaosbane, Pathfinder)
    "Moorland",
    "Rites",
    
    # Sci-Fi/Electronic (Planetary Annihilation, Riftbreaker)
    "Cipher",
    "Future Gladiator",
    
    # Sneaky/Curiosities (For shorts tips/curiosities)
    "Sneaky Snitch",
    "Scheming Weasel",
    "Monkeys Spinning Monkeys",
    
    # High-Energy/Rock
    "Severe Tire Damage",
    "Take a Chance"
]

def download_file(url, output_path):
    try:
        # Incompetech requires a User-Agent header, otherwise it may block Python's default agent
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            with open(output_path, 'wb') as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"  [ERROR] Downloading {url} failed: {e}")
        return False

def main():
    print("====================================================")
    print("Royalty-Free Music Downloader (Kevin MacLeod / Incompetech)")
    print("====================================================")
    
    catalog_path = os.path.join(MUSIC_DIR, "pieces.json")
    print(f"Downloading master catalog pieces.json...")
    if not download_file(CATALOG_URL, catalog_path):
        print("[ERROR] Failed to download pieces.json. Exiting.")
        return
        
    try:
        with open(catalog_path, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse pieces.json: {e}")
        return
        
    print(f"Catalog loaded successfully. Searching for {len(TARGET_TRACKS)} target tracks...")
    
    downloaded_count = 0
    
    for target in TARGET_TRACKS:
        # Search the catalog list for matching title (case-insensitive)
        matched_entry = None
        for entry in catalog:
            if entry.get("title", "").strip().lower() == target.lower():
                matched_entry = entry
                break
                
        if matched_entry:
            filename = matched_entry.get("filename")
            title = matched_entry.get("title")
            print(f"\nFound track: '{title}' -> Filename: '{filename}'")
            
            filename_quoted = urllib.parse.quote(filename)
            download_url = BASE_DOWNLOAD_URL + filename_quoted
            output_file = os.path.join(MUSIC_DIR, filename)
            
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"  [SKIPPED] {filename} already exists and is non-empty.")
                downloaded_count += 1
                continue
                
            print(f"  Downloading from {download_url}...")
            if download_file(download_url, output_file):
                print(f"  [SUCCESS] Saved to {output_file}")
                downloaded_count += 1
            else:
                print(f"  [FAILED] Could not download {filename}")
        else:
            # Try to guess filename fallback if catalog match failed
            guessed_filename = target.replace(" ", "") + ".mp3"
            print(f"\n[WARNING] Track '{target}' not found in pieces.json. Trying guessed filename '{guessed_filename}'...")
            download_url = BASE_DOWNLOAD_URL + guessed_filename
            output_file = os.path.join(MUSIC_DIR, guessed_filename)
            
            if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
                print(f"  [SKIPPED] {guessed_filename} already exists.")
                downloaded_count += 1
                continue
                
            if download_file(download_url, output_file):
                print(f"  [SUCCESS] Saved to {output_file} (fallback)")
                downloaded_count += 1
            else:
                print(f"  [FAILED] Guess download failed for {guessed_filename}")
                
    print(f"\n====================================================")
    print(f"Download complete: {downloaded_count}/{len(TARGET_TRACKS)} tracks ready in C:\\Users\\jegom\\shorts_project\\music\\")
    print("====================================================")

if __name__ == "__main__":
    main()
