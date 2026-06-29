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
        "title": "GTA VI Short 1 - Lanzamiento y Vice City",
        "file": "gta6_short_1_short.mp4"
    },
    {
        "title": "GTA VI Short 2 - Filtraciones y Polémicas",
        "file": "gta6_short_2_short.mp4"
    },
    {
        "title": "GTA VI Short 3 - Rumores de Retraso a 2026",
        "file": "gta6_short_3_short.mp4"
    },
    {
        "title": "GTA VI Short 4 - ¿Precio de $150 Dólares?",
        "file": "gta6_short_4_short.mp4"
    },
    {
        "title": "GTA VI Short 5 - Cataclismo y Competidores",
        "file": "gta6_short_5_short.mp4"
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

def format_duration(seconds):
    return f"{int(round(seconds))}s"

def get_size_mb(path):
    if not os.path.exists(path):
        return "0.0 MB"
    size = os.path.getsize(path)
    return f"{size / (1024 * 1024):.1f} MB"

def main():
    print("Reading and calculating durations/sizes for GTA VI Shorts...")
    
    short_rows = []
    for f in files_to_add:
        filepath = os.path.join(BASE_DIR, f["file"])
        if not os.path.exists(filepath):
            print(f"  [WARNING] File {f['file']} does not exist on disk!")
            continue
            
        dur_raw = get_duration(filepath)
        dur_str = format_duration(dur_raw)
        size_str = get_size_mb(filepath)
        
        row = f"| **{f['title']}** | [{f['file']}](file:///{filepath.replace(os.sep, '/')}) | {dur_str} | {size_str} |\n"
        short_rows.append(row)
        
    for manifest_path in MANIFEST_PATHS:
        if not os.path.exists(manifest_path):
            print(f"Manifest not found at {manifest_path}")
            continue
            
        with open(manifest_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        section_title = "\n## 📱 6. SHORTS DE GRAND THEFT AUTO VI - CAMPAÑA ESPECIAL 2026 (VERTICALES 9:16)\nShorts dinámicos con subtítulos de impacto, efectos de sonido y cortes de jugabilidad.\n\n| Título del Short | Archivo MP4 de Salida | Duración Real | Tamaño |\n| :--- | :--- | :---: | :---: |\n"
        
        if section_title.strip() not in content:
            content += section_title + "".join(short_rows)
            print(f"  Appended GTA 6 section to {os.path.basename(manifest_path)}")
            
        with open(manifest_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    print("Manifests updated with GTA VI news!")

if __name__ == "__main__":
    main()
