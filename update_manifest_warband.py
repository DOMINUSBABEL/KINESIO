import os
import subprocess
import re

BASE_DIR = r"C:\Users\jegom\shorts_project"
MANIFEST_PATHS = [
    os.path.join(BASE_DIR, "video_manifest.md"),
    r"C:\Users\jegom\.gemini\antigravity-cli\brain\394e928e-28ac-4dc9-8f51-f60f12b678cd\video_manifest.md"
]

files_to_add = [
    {
        "type": "horizontal",
        "title": "Mount & Blade: Warband - Joya Inmortal",
        "file": "warband_retrospective.mp4"
    },
    {
        "type": "short",
        "title": "Warband Short 1 - Cofre Samurái de Rivacheg",
        "file": "warband_short_1_short.mp4"
    },
    {
        "type": "short",
        "title": "Warband Short 2 - Colapso de Calradia",
        "file": "warband_short_2_short.mp4"
    },
    {
        "type": "short",
        "title": "Warband Short 3 - Lanza Acoplada y Velocidad",
        "file": "warband_short_3_short.mp4"
    },
    {
        "type": "short",
        "title": "Warband Short 4 - Arte del Bloqueo Manual",
        "file": "warband_short_4_short.mp4"
    },
    {
        "type": "short",
        "title": "Warband Short 5 - Formaciones Tácticas",
        "file": "warband_short_5_short.mp4"
    }
]

def get_duration(path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except:
        return 0.0

def format_duration(seconds, is_short):
    if is_short:
        return f"{int(round(seconds))}s"
    else:
        mins = int(seconds // 60)
        secs = int(round(seconds % 60))
        return f"{mins}:{secs:02d} min"

def get_size_mb(path):
    if not os.path.exists(path):
        return "0.0 MB"
    size = os.path.getsize(path)
    return f"{size / (1024 * 1024):.1f} MB"

def main():
    print("Reading and calculating durations/sizes for Mount & Blade videos...")
    
    horizontal_rows = []
    short_rows = []
    
    for f in files_to_add:
        filepath = os.path.join(BASE_DIR, f["file"])
        if not os.path.exists(filepath):
            print(f"  [WARNING] File {f['file']} does not exist on disk!")
            continue
            
        dur_raw = get_duration(filepath)
        dur_str = format_duration(dur_raw, f["type"] == "short")
        size_str = get_size_mb(filepath)
        
        row = f"| **{f['title']}** | [{f['file']}](file:///{filepath.replace(os.sep, '/')}) | {dur_str} | {size_str} |\n"
        if f["type"] == "horizontal":
            horizontal_rows.append(row)
        else:
            short_rows.append(row)
            
    # We update both manifest files
    for manifest_path in MANIFEST_PATHS:
        if not os.path.exists(manifest_path):
            print(f"Manifest not found at {manifest_path}")
            continue
            
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Insert horizontal video row under "### 🪐 Videos Nuevos de la Campaña 4"
        # We can find the line after "We Who Are About To Die" and insert it there.
        # Or look for We Who Are About To Die table line:
        pattern_horiz = r"(\| \*\*We Who Are About To Die\*\* \|.*?\n)"
        match_horiz = re.search(pattern_horiz, content)
        if match_horiz and horizontal_rows:
            matched_line = match_horiz.group(0)
            if horizontal_rows[0] not in content:
                content = content.replace(matched_line, matched_line + horizontal_rows[0])
                print(f"  Inserted horizontal row in {os.path.basename(manifest_path)}")
                
        # 2. Append a new section "## 📱 5. SHORTS TEMÁTICOS DE CURIOSIDADES - MOUNT & BLADE"
        section_shorts_title = "\n## 📱 5. SHORTS TEMÁTICOS DE CURIOSIDADES - MOUNT & BLADE (VERTICALES 9:16)\nShorts enfocados en detalles ocultos, historia de Calradia y consejos avanzados de combate.\n\n| Título del Short | Archivo MP4 de Salida | Duración Real | Tamaño |\n| :--- | :--- | :---: | :---: |\n"
        
        if section_shorts_title.strip() not in content:
            # We append to the end of the file
            content += section_shorts_title + "".join(short_rows)
            print(f"  Appended Mount & Blade shorts section in {os.path.basename(manifest_path)}")
            
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Manifests updated successfully!")

if __name__ == "__main__":
    main()
