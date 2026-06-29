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
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

os.makedirs(CAPSULES_DIR, exist_ok=True)
os.makedirs(TRAILERS_DIR, exist_ok=True)
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': 'wants_mature_content=1; birthtime=315532800; lastagecheckage=1'
}

NEW_GAMES = [
    {"name": "Planetary Annihilation: TITANS", "appid": 386070, "prefix": "planetary"},
    {"name": "The Riftbreaker", "appid": 780310, "prefix": "riftbreaker"},
    {"name": "We Who Are About To Die", "appid": 973230, "prefix": "wewhoare"}
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
                    for res in ['max', '480']:
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
    print("Starting Asset Collection Script for Campaign 4 Games")
    print("====================================================")
    
    for game in NEW_GAMES:
        name = game["name"]
        appid = game["appid"]
        prefix = game["prefix"]
        
        print(f"\nProcessing '{name}' [App ID: {appid}]")
        
        # 1. Download capsule image (both as prefix_capsule.jpg and capsule_appid.jpg)
        capsule_filename_1 = f"{prefix}_capsule.jpg"
        capsule_filename_2 = f"capsule_{appid}.jpg"
        capsule_path_1 = os.path.join(CAPSULES_DIR, capsule_filename_1)
        capsule_path_2 = os.path.join(CAPSULES_DIR, capsule_filename_2)
        
        if not os.path.exists(capsule_path_2):
            print("  Downloading capsule...")
            url_primary = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{appid}/library_600x900.jpg"
            url_fallback = f"https://cdn.akamai.steamstatic.com/steam/apps/{appid}/library_600x900.jpg"
            
            if download_url(url_primary, capsule_path_2):
                print(f"    [SUCCESS] Saved capsule to {capsule_filename_2}")
            elif download_url(url_fallback, capsule_path_2):
                print(f"    [SUCCESS] Saved capsule to {capsule_filename_2} (fallback)")
            else:
                print("    [FAILED] Capsule download failed")
        else:
            print("  Capsule already exists.")
            
        # Copy to prefix_capsule.jpg if it doesn't exist
        if os.path.exists(capsule_path_2) and not os.path.exists(capsule_path_1):
            import shutil
            shutil.copyfile(capsule_path_2, capsule_path_1)
            
        # 2. Download trailer (both as prefix_trailer.mp4 and trailer_appid.mp4)
        trailer_filename_1 = f"{prefix}_trailer.mp4"
        trailer_filename_2 = f"trailer_{appid}.mp4"
        trailer_path_1 = os.path.join(TRAILERS_DIR, trailer_filename_1)
        trailer_path_2 = os.path.join(TRAILERS_DIR, trailer_filename_2)
        
        if not os.path.exists(trailer_path_2):
            print("  Fetching trailer URL...")
            t_url, t_err = get_trailer_url_from_api(appid)
            if t_url:
                print(f"  Downloading trailer stream from {t_url}...")
                ok, dl_err = download_trailer(t_url, trailer_path_2)
                if ok:
                    print(f"    [SUCCESS] Saved trailer to {trailer_filename_2}")
                else:
                    print(f"    [FAILED] Trailer download failed: {dl_err}")
            else:
                print(f"    [FAILED] Could not get trailer URL: {t_err}")
        else:
            print("  Trailer already exists.")
            
        # Copy to prefix_trailer.mp4 if it doesn't exist
        if os.path.exists(trailer_path_2) and not os.path.exists(trailer_path_1):
            import shutil
            shutil.copyfile(trailer_path_2, trailer_path_1)
            
        # 3. Download screenshots (prefix_screenshot_idx.jpg)
        print("  Fetching screenshots...")
        url_details = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us"
        req = urllib.request.Request(url_details, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                data = json.loads(response.read().decode('utf-8'))
                if str(appid) in data and data[str(appid)]['success']:
                    screenshots = data[str(appid)]['data'].get('screenshots', [])
                    to_download = screenshots[:10]
                    downloaded_count = 0
                    for idx, ss in enumerate(to_download):
                        ss_url = ss.get('path_full')
                        if ss_url:
                            ss_filename = f"{prefix}_screenshot_{idx}.jpg"
                            ss_path = os.path.join(SCREENSHOTS_DIR, ss_filename)
                            if not os.path.exists(ss_path):
                                if download_url(ss_url, ss_path):
                                    downloaded_count += 1
                            else:
                                downloaded_count += 1
                    print(f"    [SUCCESS] Validated {downloaded_count}/10 screenshots on disk")
                else:
                    print("    [FAILED] API success=False for screenshots")
        except Exception as e:
            print(f"    [FAILED] Error fetching screenshots: {e}")
                
    print("\n====================================================")
    print("Asset Collection Complete!")
    print("====================================================")

if __name__ == "__main__":
    main()
