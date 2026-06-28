import os
import sys
import json
import time
import subprocess
import urllib.request

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")

os.makedirs(CAPSULES_DIR, exist_ok=True)
os.makedirs(TRAILERS_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'wants_mature_content=1; birthtime=315532800; lastagecheckage=1'
}

GAMES = [
    {"appid": 333420, "key": "cossacks3", "name": "Cossacks 3"},
    {"appid": 2772750, "key": "aoh3", "name": "Age of History 3"},
    {"appid": 1272320, "key": "diplomacy_v4", "name": "Diplomacy is Not an Option"},
    {"appid": 1281630, "key": "anno1404", "name": "Anno 1404 History Edition"},
    {"appid": 386070, "key": "planetary", "name": "Planetary Annihilation Titans"}
]

def get_clean_env():
    clean_env = os.environ.copy()
    for var in ['PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV']:
        if var in clean_env:
            del clean_env[var]
    return clean_env

def download_url(url, dest_path, retries=3):
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

def get_trailer_url_from_api(appid):
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
                
                return None, "No compatible stream URL found"
            else:
                return None, "API returned success=False"
    except Exception as e:
        return None, f"Network/API Error: {e}"

def download_trailer(trailer_url, dest_path):
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=480]+bestaudio/best[height<=480]/best",
        "--merge-output-format", "mp4",
        "--no-update",
        trailer_url,
        "-o", dest_path
    ]
    try:
        subprocess.run(cmd, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        if os.path.exists(dest_path) and os.path.getsize(dest_path) > 0:
            return True, None
        return False, "Output file not created or empty"
    except subprocess.CalledProcessError as e:
        return False, f"yt-dlp failed (code {e.returncode}): {e.stderr.strip()}"
    except Exception as e:
        return False, str(e)

def main():
    print("====================================================")
    print("Starting Asset Collection Script for Shorts v4")
    print("====================================================")
    
    for game in GAMES:
        appid = game["appid"]
        key = game["key"]
        name = game["name"]
        
        print(f"\nProcessing '{name}' [App ID: {appid}]")
        
        # 1. Capsule
        capsule_filename = f"capsule_{appid}.jpg"
        capsule_path = os.path.join(CAPSULES_DIR, capsule_filename)
        if not os.path.exists(capsule_path):
            print("  Downloading capsule...")
            url_primary = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg"
            url_fallback = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/library_600x900.jpg"
            if download_url(url_primary, capsule_path):
                print(f"    [SUCCESS] Saved capsule to {capsule_filename}")
            elif download_url(url_fallback, capsule_path):
                print(f"    [SUCCESS] Saved capsule to {capsule_filename} (fallback)")
            else:
                print("    [FAILED] Capsule download failed")
        else:
            print("  Capsule already exists.")
            
        # 2. Trailer
        trailer_filename = f"trailer_{appid}.mp4"
        trailer_path = os.path.join(TRAILERS_DIR, trailer_filename)
        if not os.path.exists(trailer_path):
            print("  Fetching trailer URL...")
            t_url, t_err = get_trailer_url_from_api(appid)
            if t_url:
                print(f"  Downloading trailer stream from {t_url}...")
                ok, dl_err = download_trailer(t_url, trailer_path)
                if ok:
                    print(f"    [SUCCESS] Saved trailer to {trailer_filename}")
                else:
                    print(f"    [FAILED] Trailer download failed: {dl_err}")
            else:
                print(f"    [FAILED] Could not get trailer URL: {t_err}")
        else:
            print("  Trailer already exists.")
            
    print("\n====================================================")
    print("Shorts v4 Asset Collection Complete!")
    print("====================================================")

if __name__ == "__main__":
    main()
