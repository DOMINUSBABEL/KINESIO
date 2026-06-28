import os
import sys
import json
import shutil
import time
import subprocess
import urllib.request
import urllib.error

# Configure standard output to UTF-8 to prevent encoding issues on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Root Directories
BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")

# Ensure target directories exist
os.makedirs(CAPSULES_DIR, exist_ok=True)
os.makedirs(TRAILERS_DIR, exist_ok=True)

# Headers for Steam requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'wants_mature_content=1; birthtime=315532800; lastagecheckage=1'
}

# The 11 missing/updated games from the new scripts
MISSING_GAMES_DATA = [
    {"name": "Grand Theft Auto V", "appid": 271590, "category": "Mundo Abierto"},
    {"name": "Rust", "appid": 252490, "category": "Mundo Abierto"},
    {"name": "Subnautica", "appid": 264710, "category": "Mundo Abierto"},
    {"name": "Terraria", "appid": 105600, "category": "Mundo Abierto"},
    
    {"name": "Assetto Corsa", "appid": 244210, "category": "Conducción"},
    {"name": "Euro Truck Simulator 2", "appid": 227300, "category": "Conducción"},
    
    {"name": "Golf With Your Friends", "appid": 431240, "category": "Deporte"},
    {"name": "Football Manager 2024", "appid": 2252600, "category": "Deporte"},
    {"name": "PGA TOUR 2K23", "appid": 2380510, "category": "Deporte"},
    
    {"name": "Good Pizza, Great Pizza", "appid": 770810, "category": "Cocina"},
    
    {"name": "Endless Space 2", "appid": 392110, "category": "4X Strategy"}
]

def get_clean_env():
    """Returns a copy of os.environ without Python/Venv path variables to prevent library mismatches in yt-dlp."""
    clean_env = os.environ.copy()
    for var in ['PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV']:
        if var in clean_env:
            del clean_env[var]
    return clean_env

def download_url(url, dest_path, retries=3):
    """Downloads a file from a URL with retry logic."""
    for attempt in range(1, retries + 1):
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=20) as response:
                with open(dest_path, 'wb') as out_file:
                    out_file.write(response.read())
            if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
                return True
        except Exception as e:
            print(f"      [Retry {attempt}/{retries}] Failed to download {url}: {e}")
            time.sleep(1)
    return False

def download_capsule(appid, dest_path):
    """Downloads a 600x900 vertical capsule image with CDN fallbacks."""
    url_primary = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg"
    url_fallback = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/library_600x900.jpg"
    
    if download_url(url_primary, dest_path):
        return True
    if download_url(url_fallback, dest_path):
        return True
    return False

def get_trailer_url_from_api(appid):
    """Queries Steam API and extracts the best available trailer stream URL."""
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            if str(appid) in data and data[str(appid)]['success']:
                gdata = data[str(appid)]['data']
                movies = gdata.get('movies', [])
                if not movies:
                    return None, "No movies found in game metadata"
                
                movie = movies[0]
                for key in ['dash_h264', 'hls_h264', 'dash_av1']:
                    if key in movie and movie[key]:
                        return movie[key], None
                
                if 'mp4' in movie and movie['mp4']:
                    mp4_dict = movie['mp4']
                    for res in ['480', 'max']:
                        if res in mp4_dict and mp4_dict[res]:
                            return mp4_dict[res], None
                
                if 'webm' in movie and movie['webm']:
                    webm_dict = movie['webm']
                    for res in ['480', 'max']:
                        if res in webm_dict and webm_dict[res]:
                            return webm_dict[res], None
                
                return None, "No compatible format key in movie metadata"
            else:
                return None, "API returned success=False"
    except Exception as e:
        return None, f"Network/API Error: {e}"

def download_trailer(trailer_url, dest_path):
    """Downloads and encodes/stitches a trailer to MP4 480p using yt-dlp."""
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=480]+bestaudio/best[height<=480]/best",
        "--merge-output-format", "mp4",
        "--no-update",
        trailer_url,
        "-o", dest_path
    ]
    try:
        result = subprocess.run(cmd, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
            return True, None
        return False, "Output file not created or empty"
    except subprocess.CalledProcessError as e:
        return False, f"yt-dlp failed (code {e.returncode}): {e.stderr.strip()}"
    except Exception as e:
        return False, str(e)

def main():
    print("====================================================")
    print("Downloading Missing Assets for Newly Chosen Games")
    print("====================================================")
    
    downloaded = 0
    failed = 0
    
    for game in MISSING_GAMES_DATA:
        name = game["name"]
        appid = game["appid"]
        cat = game["category"]
        
        print(f"\nProcessing '{name}' ({cat}) [App ID: {appid}]")
        
        # 1. Download capsule
        capsule_dest = os.path.join(CAPSULES_DIR, f"capsule_{appid}.jpg")
        print(f"  Downloading capsule...")
        capsule_ok = download_capsule(appid, capsule_dest)
        if capsule_ok:
            print(f"    [SUCCESS] Saved capsule_{appid}.jpg")
        else:
            print(f"    [FAILED] Capsule download failed")
            
        # 2. Download trailer
        trailer_dest = os.path.join(TRAILERS_DIR, f"trailer_{appid}.mp4")
        print(f"  Fetching trailer URL...")
        t_url, err = get_trailer_url_from_api(appid)
        if t_url:
            print(f"  Downloading trailer stream...")
            t_ok, dl_err = download_trailer(t_url, trailer_dest)
            if t_ok:
                print(f"    [SUCCESS] Saved trailer_{appid}.mp4")
                trailer_ok = True
            else:
                print(f"    [FAILED] Trailer download failed: {dl_err}")
                trailer_ok = False
        else:
            print(f"    [FAILED] Could not get trailer URL: {err}")
            trailer_ok = False
            
        if capsule_ok and trailer_ok:
            downloaded += 1
        else:
            failed += 1
            
    print("\n====================================================")
    print(f"Completed! Downloaded: {downloaded} | Failed: {failed}")
    print("====================================================")

if __name__ == "__main__":
    main()
