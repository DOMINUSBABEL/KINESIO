import os
import sys
import shutil
import urllib.request
import json
import ssl
import subprocess

# Set encoding to UTF-8 to prevent character encoding issues on Windows
sys.stdout.reconfigure(encoding='utf-8')

def fetch_steam_json(appid):
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}&cc=us"
    req = urllib.request.Request(url)
    req.add_header('Cookie', 'wants_mature_content=1')
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read().decode('utf-8'))

def download_file(url, dest_path):
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            with open(dest_path, 'wb') as f:
                f.write(r.read())
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        return False

def main():
    print("Starting download of Mount & Blade: Warband store assets...")
    
    # Define directories
    base_dir = r"C:\Users\jegom\shorts_project"
    capsules_dir = os.path.join(base_dir, "capsules")
    trailers_dir = os.path.join(base_dir, "trailers")
    screenshots_dir = os.path.join(base_dir, "screenshots")
    
    for d in [capsules_dir, trailers_dir, screenshots_dir]:
        os.makedirs(d, exist_ok=True)
        
    # 1. Download Capsule
    print("\n--- Downloading Capsule Image ---")
    data_48700 = fetch_steam_json(48700)
    game_data = data_48700["48700"]["data"]
    
    # Try 616x353 capsule URL first
    capsule_url = "https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/48700/capsule_616x353.jpg"
    dest_capsule_id = os.path.join(capsules_dir, "capsule_48700.jpg")
    dest_capsule_name = os.path.join(capsules_dir, "warband_capsule.jpg")
    
    print(f"Downloading capsule from {capsule_url}...")
    success = download_file(capsule_url, dest_capsule_id)
    if not success:
        # Fallback to header image URL from JSON
        header_url = game_data.get("header_image")
        print(f"616x353 capsule failed, falling back to header image: {header_url}")
        success = download_file(header_url, dest_capsule_id)
        
    if success:
        shutil.copy2(dest_capsule_id, dest_capsule_name)
        print("Capsule images downloaded successfully.")
    else:
        print("ERROR: Failed to download capsule images.")

    # 2. Download 10 Screenshots
    print("\n--- Downloading 10 Screenshots ---")
    screenshots = game_data.get("screenshots", [])
    screenshot_urls = [s.get("path_full") for s in screenshots]
    print(f"Found {len(screenshot_urls)} screenshots for App ID 48700.")
    
    # If we need 10 screenshots, we supplement from App ID 22100 (original Mount & Blade)
    if len(screenshot_urls) < 10:
        needed = 10 - len(screenshot_urls)
        print(f"Supplementing with {needed} screenshots from App ID 22100...")
        data_22100 = fetch_steam_json(22100)
        screenshots_22100 = data_22100["22100"]["data"].get("screenshots", [])
        for s in screenshots_22100:
            if len(screenshot_urls) >= 10:
                break
            screenshot_urls.append(s.get("path_full"))
            
    # Download them
    for i, url in enumerate(screenshot_urls[:10]):
        filename = f"warband_screenshot_{i+1}.jpg"
        dest_path = os.path.join(screenshots_dir, filename)
        print(f"Downloading screenshot {i+1}/10 to {filename}...")
        download_file(url, dest_path)
        
    # 3. Download Trailer
    print("\n--- Downloading Trailer ---")
    movies = game_data.get("movies", [])
    if movies:
        movie_url = movies[0].get("hls_h264")
        dest_trailer_id = os.path.join(trailers_dir, "trailer_48700.mp4")
        dest_trailer_name = os.path.join(trailers_dir, "warband_trailer.mp4")
        
        # Clean env to avoid python subprocess pollution
        env = os.environ.copy()
        for var in ["PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV"]:
            if var in env:
                del env[var]
                
        cmd = [
            "yt-dlp",
            "-o", dest_trailer_id,
            "--merge-output-format", "mp4",
            movie_url
        ]
        print(f"Executing: {' '.join(cmd)}")
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        if res.returncode == 0 and os.path.exists(dest_trailer_id):
            shutil.copy2(dest_trailer_id, dest_trailer_name)
            print("Trailer downloaded successfully.")
        else:
            print("ERROR downloading trailer with yt-dlp:")
            print("STDOUT:", res.stdout)
            print("STDERR:", res.stderr)
    else:
        print("ERROR: No movies found in Steam API details!")
        
    # 4. Verification
    print("\n--- Asset Verification ---")
    files_to_verify = [
        os.path.join(capsules_dir, "capsule_48700.jpg"),
        os.path.join(capsules_dir, "warband_capsule.jpg"),
        os.path.join(trailers_dir, "trailer_48700.mp4"),
        os.path.join(trailers_dir, "warband_trailer.mp4"),
    ]
    for i in range(1, 11):
        files_to_verify.append(os.path.join(screenshots_dir, f"warband_screenshot_{i}.jpg"))
        
    all_ok = True
    for f in files_to_verify:
        name = os.path.basename(f)
        parent_dir = os.path.basename(os.path.dirname(f))
        rel_name = os.path.join(parent_dir, name)
        
        if os.path.exists(f):
            size = os.path.getsize(f)
            if size > 0:
                print(f"[OK] {rel_name} exists, size: {size:,} bytes")
            else:
                print(f"[ERROR] {rel_name} exists but is ZERO bytes!")
                all_ok = False
        else:
            print(f"[ERROR] {rel_name} DOES NOT exist!")
            all_ok = False
            
    if all_ok:
        print("\nSUCCESS: All Mount & Blade: Warband assets successfully downloaded, copied, and verified!")
    else:
        print("\nFAILURE: Some assets could not be verified.")

if __name__ == '__main__':
    main()
