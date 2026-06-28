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
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")

# Ensure target directories exist
os.makedirs(CAPSULES_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
os.makedirs(TRAILERS_DIR, exist_ok=True)

# Headers for Steam requests (including age gate bypass cookies)
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'wants_mature_content=1; birthtime=315532800; lastagecheckage=1'
}

# The 25 games categorized with requested and corrected App IDs
GAMES_DATA = [
    # Category: Open World
    {"name": "Red Dead Redemption 2", "requested_id": 1174180, "corrected_id": 1174180, "category": "Open World"},
    {"name": "Cyberpunk 2077", "requested_id": 1091500, "corrected_id": 1091500, "category": "Open World"},
    {"name": "Hogwarts Legacy", "requested_id": 990080, "corrected_id": 990080, "category": "Open World"},
    {"name": "Elden Ring", "requested_id": 1245620, "corrected_id": 1245620, "category": "Open World"},
    {"name": "Horizon Forbidden West", "requested_id": 2420110, "corrected_id": 2420110, "category": "Open World"},
    
    # Category: Conducción
    {"name": "Forza Horizon 5", "requested_id": 1551360, "corrected_id": 1551360, "category": "Conducción"},
    {"name": "Assetto Corsa Competizione", "requested_id": 805550, "corrected_id": 805550, "category": "Conducción"},
    {"name": "Need for Speed Unbound", "requested_id": 1840800, "corrected_id": 1846380, "category": "Conducción"},
    {"name": "Wreckfest", "requested_id": 228380, "corrected_id": 228380, "category": "Conducción"},
    {"name": "Dirt 5", "requested_id": 1038250, "corrected_id": 1038250, "category": "Conducción"},
    
    # Category: Deporte
    {"name": "EA Sports FC 24", "requested_id": 2195250, "corrected_id": 2195250, "category": "Deporte"},
    {"name": "NBA 2K26", "requested_id": 2878980, "corrected_id": 3472040, "category": "Deporte"},
    {"name": "Football Manager 2026", "requested_id": 2980750, "corrected_id": 3551340, "category": "Deporte"},
    {"name": "Riders Republic", "requested_id": 2167200, "corrected_id": 2290180, "category": "Deporte"},
    {"name": "PGA Tour 2K23", "requested_id": 1585250, "corrected_id": 1588010, "category": "Deporte"},
    
    # Category: Cocina
    {"name": "Overcooked! 2", "requested_id": 728880, "corrected_id": 728880, "category": "Cocina"},
    {"name": "PlateUp!", "requested_id": 1599600, "corrected_id": 1599600, "category": "Cocina"},
    {"name": "Cooking Simulator", "requested_id": 641320, "corrected_id": 641320, "category": "Cocina"},
    {"name": "Overcooked! All You Can Eat", "requested_id": 1243830, "corrected_id": 1243830, "category": "Cocina"},
    {"name": "Chef Life: A Restaurant Simulator", "requested_id": 1123770, "corrected_id": 1122340, "category": "Cocina"},
    
    # Category: 4X Strategy
    {"name": "Sid Meier's Civilization VI", "requested_id": 289070, "corrected_id": 289070, "category": "4X Strategy"},
    {"name": "Stellaris", "requested_id": 281990, "corrected_id": 281990, "category": "4X Strategy"},
    {"name": "Hearts of Iron IV", "requested_id": 394360, "corrected_id": 394360, "category": "4X Strategy"},
    {"name": "Age of Wonders 4", "requested_id": 1669000, "corrected_id": 1669000, "category": "4X Strategy"},
    {"name": "Old World", "requested_id": 597180, "corrected_id": 597180, "category": "4X Strategy"}
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
    """Queries Steam API and extracts the best available trailer stream URL (using US region parameter for consistency)."""
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
                
                # Pick the first movie (usually the main trailer)
                movie = movies[0]
                # Fallback list of formats in order of preference
                for key in ['dash_h264', 'hls_h264', 'dash_av1']:
                    if key in movie and movie[key]:
                        return movie[key], None
                
                # Try legacy/explicit direct MP4/WEBM
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
    """Downloads and encodes/stitches a trailer to MP4 480p using yt-dlp with a cleaned environment."""
    cmd = [
        "yt-dlp",
        "-f", "bestvideo[height<=480]+bestaudio/best[height<=480]/best",
        "--merge-output-format", "mp4",
        "--no-update",
        trailer_url,
        "-o", dest_path
    ]
    try:
        # Run yt-dlp synchronously with a cleaned environment
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
    print("Starting Asset Collection Script v2")
    print("====================================================")
    
    summary = {
        "mow": {"capsule": False, "screenshots": 0, "trailer": False},
        "games_downloaded": 0,
        "games_failed": 0,
        "failures": []
    }
    
    # ----------------------------------------------------
    # Phase 1: Men of War: Assault Squad 2 (App ID: 244450)
    # ----------------------------------------------------
    print("\n--- Phase 1: Men of War: Assault Squad 2 (244450) ---")
    
    # 1. Capsule
    mow_capsule_path = os.path.join(CAPSULES_DIR, "mow_capsule.jpg")
    print("Downloading Men of War capsule...")
    if download_capsule(244450, mow_capsule_path):
        print("  [SUCCESS] Saved to mow_capsule.jpg")
        summary["mow"]["capsule"] = True
    else:
        print("  [FAILED] Failed to download Men of War capsule")
        summary["failures"].append("Men of War: Capsule download failed")
        
    # 2. Screenshots
    print("Fetching Men of War screenshots from API...")
    url_mow = "https://store.steampowered.com/api/appdetails?appids=244450&cc=us"
    req_mow = urllib.request.Request(url_mow, headers=HEADERS)
    try:
        with urllib.request.urlopen(req_mow, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            if '244450' in data and data['244450']['success']:
                screenshots = data['244450']['data'].get('screenshots', [])
                # Take up to 10
                to_download = screenshots[:10]
                downloaded_count = 0
                for idx, ss in enumerate(to_download):
                    ss_url = ss.get('path_full')
                    if ss_url:
                        ss_path = os.path.join(SCREENSHOTS_DIR, f"screenshot_{idx}.jpg")
                        print(f"  Downloading screenshot_{idx}.jpg...")
                        if download_url(ss_url, ss_path):
                            downloaded_count += 1
                        else:
                            print(f"    Failed screenshot_{idx}")
                print(f"  [SUCCESS] Downloaded {downloaded_count}/10 screenshots")
                summary["mow"]["screenshots"] = downloaded_count
            else:
                print("  [FAILED] API success=False for Men of War screenshots")
                summary["failures"].append("Men of War: Screenshots API failed")
    except Exception as e:
        print(f"  [FAILED] Error fetching screenshots: {e}")
        summary["failures"].append(f"Men of War: Screenshots error - {e}")
        
    # 3. Trailer
    mow_trailer_path = os.path.join(TRAILERS_DIR, "mow_trailer.mp4")
    print("Fetching Men of War trailer URL...")
    trailer_url, err = get_trailer_url_from_api(244450)
    if trailer_url:
        print("Downloading Men of War trailer...")
        ok, dl_err = download_trailer(trailer_url, mow_trailer_path)
        if ok:
            print("  [SUCCESS] Saved to mow_trailer.mp4")
            summary["mow"]["trailer"] = True
        else:
            print(f"  [FAILED] Trailer download failed: {dl_err}")
            summary["failures"].append(f"Men of War: Trailer download error - {dl_err}")
    else:
        print(f"  [FAILED] Could not get trailer URL: {err}")
        summary["failures"].append(f"Men of War: Trailer URL error - {err}")
        
    # ----------------------------------------------------
    # Phase 2: The 25 games for the 5 new Shorts
    # ----------------------------------------------------
    print("\n--- Phase 2: 25 Games for New Shorts ---")
    
    for game in GAMES_DATA:
        name = game["name"]
        req_id = game["requested_id"]
        corr_id = game["corrected_id"]
        category = game["category"]
        
        print(f"\nProcessing '{name}' ({category})")
        print(f"  Requested App ID: {req_id} | Corrected App ID: {corr_id}")
        
        # 1. Download Capsule
        capsule_dest_req = os.path.join(CAPSULES_DIR, f"capsule_{req_id}.jpg")
        capsule_dest_corr = os.path.join(CAPSULES_DIR, f"capsule_{corr_id}.jpg")
        
        print(f"  Downloading capsule...")
        if download_capsule(corr_id, capsule_dest_req):
            print(f"    [SUCCESS] Saved capsule_{req_id}.jpg")
            # If App ID was corrected, save copy to corr_id as well
            if req_id != corr_id:
                try:
                    shutil.copy2(capsule_dest_req, capsule_dest_corr)
                    print(f"    [COPY] Copied to capsule_{corr_id}.jpg")
                except Exception as cp_err:
                    print(f"    [WARNING] Failed copy capsule: {cp_err}")
            capsule_ok = True
        else:
            print(f"    [FAILED] Capsule download failed")
            summary["failures"].append(f"{name}: Capsule download failed")
            capsule_ok = False
            
        # 2. Download Trailer
        trailer_dest_req = os.path.join(TRAILERS_DIR, f"trailer_{req_id}.mp4")
        trailer_dest_corr = os.path.join(TRAILERS_DIR, f"trailer_{corr_id}.mp4")
        
        print(f"  Fetching trailer URL...")
        t_url, t_err = get_trailer_url_from_api(corr_id)
        if t_url:
            print(f"  Downloading trailer stream...")
            t_ok, t_dl_err = download_trailer(t_url, trailer_dest_req)
            if t_ok:
                print(f"    [SUCCESS] Saved trailer_{req_id}.mp4")
                if req_id != corr_id:
                    try:
                        shutil.copy2(trailer_dest_req, trailer_dest_corr)
                        print(f"    [COPY] Copied to trailer_{corr_id}.mp4")
                    except Exception as cp_err:
                        print(f"    [WARNING] Failed copy trailer: {cp_err}")
                trailer_ok = True
            else:
                print(f"    [FAILED] Trailer download failed: {t_dl_err}")
                summary["failures"].append(f"{name}: Trailer download failed - {t_dl_err}")
                trailer_ok = False
        else:
            print(f"    [FAILED] Could not get trailer URL: {t_err}")
            summary["failures"].append(f"{name}: Trailer URL error - {t_err}")
            trailer_ok = False
            
        if capsule_ok and trailer_ok:
            summary["games_downloaded"] += 1
        else:
            summary["games_failed"] += 1
            
    # ----------------------------------------------------
    # Phase 3: Final Reports
    # ----------------------------------------------------
    print("\n====================================================")
    print("Asset Collection Summary")
    print("====================================================")
    print(f"Men of War: Assault Squad 2:")
    print(f"  Capsule: {'SUCCESS' if summary['mow']['capsule'] else 'FAILED'}")
    print(f"  Screenshots: {summary['mow']['screenshots']}/10 downloaded")
    print(f"  Trailer: {'SUCCESS' if summary['mow']['trailer'] else 'FAILED'}")
    print(f"New 25 Games:")
    print(f"  Fully Completed (Capsule + Trailer): {summary['games_downloaded']} / 25")
    print(f"  Failed games: {summary['games_failed']}")
    if summary["failures"]:
        print("\nDetail of Failures:")
        for failure in summary["failures"]:
            print(f"  - {failure}")
    else:
        print("\nAll downloads completed successfully without errors!")
    print("====================================================")

if __name__ == "__main__":
    main()
