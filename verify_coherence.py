import os
import sys
import re
import subprocess
import json

# Set standard output encoding to UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
sys.path.append(BASE_DIR)

# Import lists from compile_shorts
try:
    import compile_shorts
    RTS_CS = compile_shorts.RTS_GAMES
    CITY_CS = compile_shorts.CITY_GAMES
    ARPG_CS = compile_shorts.ARPG_GAMES
except ImportError as e:
    print(f"Error importing compile_shorts: {e}")
    sys.exit(1)

def parse_markdown_table(filepath, section_markers):
    """
    Parses a markdown file and extracts table rows under sections matching the list of section_markers.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    tables = {}
    current_section = None
    in_table = False

    for line in lines:
        line_strip = line.strip()
        # Detect sections
        if line_strip.startswith('#'):
            # Match sections
            matched = False
            for marker in section_markers:
                if marker.lower() in line_strip.lower():
                    current_section = marker
                    tables[current_section] = []
                    in_table = False
                    matched = True
                    break
            if not matched:
                current_section = None
                in_table = False
        
        elif current_section and line_strip.startswith('|'):
            # Check for header divider line
            if re.match(r'^\|[\s:|\\-]+$', line_strip):
                continue
            
            # Extract row cells
            cells = [c.strip() for c in line_strip.split('|')[1:-1]]
            
            # Check if this is header row
            if cells and ('game' in cells[0].lower() or 'tiempo' in cells[0].lower() or 'segmento' in cells[0].lower()):
                continue
                
            tables[current_section].append(cells)

    return tables

def get_duration(file_path):
    if not os.path.exists(file_path):
        return None
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        return f"Error: {e}"

def clean_markdown_bold(text):
    return re.sub(r'\*\*|\*', '', text).strip()

def extract_price(price_str):
    # Extracts numbers from price string (e.g. "$13.99" or "~$23.99" or "AHORA $13.99 | ANTES $39.99")
    # Returns (sale_price, reg_price) as floats
    prices = re.findall(r'\$?([0-9]+\.[0-9]+)', price_str)
    if len(prices) == 2:
        return float(prices[0]), float(prices[1])
    elif len(prices) == 1:
        return float(prices[0]), None
    return None, None

def verify():
    report = {
        "capsules": [],
        "game_data_vs_compile_shorts": [],
        "scripts_vs_compile_shorts": [],
        "videos": []
    }
    
    # 1. Verify capsules directory
    capsules_dir = os.path.join(BASE_DIR, "capsules")
    all_capsules_in_folder = os.listdir(capsules_dir) if os.path.exists(capsules_dir) else []
    
    cs_all_capsules = []
    for g in RTS_CS + CITY_CS + ARPG_CS:
        cs_all_capsules.append(g["capsule"])
        
    for cap_file in cs_all_capsules:
        cap_path = os.path.join(capsules_dir, cap_file)
        exists = os.path.exists(cap_path)
        size = os.path.getsize(cap_path) if exists else 0
        report["capsules"].append({
            "filename": cap_file,
            "exists": exists,
            "size_bytes": size,
            "valid": exists and size > 0
        })
        
    # Check if there are orphaned capsule files in the folder
    orphaned = [f for f in all_capsules_in_folder if f not in cs_all_capsules]
    
    # 2. Parse game_data.md and compare with compile_shorts
    game_data_path = os.path.join(BASE_DIR, "game_data.md")
    gd_tables = parse_markdown_table(game_data_path, ["RTS", "City Builder", "ARPG"])
    
    # Map parsed tables to compile_shorts lists
    genres = [
        {"name": "RTS", "gd_key": "RTS", "cs_list": RTS_CS},
        {"name": "City Builder", "gd_key": "City Builder", "cs_list": CITY_CS},
        {"name": "ARPG", "gd_key": "ARPG", "cs_list": ARPG_CS}
    ]
    
    for gen in genres:
        gd_rows = gd_tables.get(gen["gd_key"], [])
        cs_list = gen["cs_list"]
        
        # Check matching counts
        if len(gd_rows) != len(cs_list):
            report["game_data_vs_compile_shorts"].append({
                "genre": gen["name"],
                "error": f"Count mismatch: game_data.md has {len(gd_rows)} games, compile_shorts.py has {len(cs_list)} games"
            })
            
        for i, cs_game in enumerate(cs_list):
            if i >= len(gd_rows):
                break
            gd_row = gd_rows[i]
            # gd_row format: [Game Name, Discount, Sale Price, Regular Price, Status]
            gd_title = clean_markdown_bold(gd_row[0])
            gd_discount = clean_markdown_bold(gd_row[1])
            gd_sale_price_str = gd_row[2]
            gd_reg_price_str = gd_row[3]
            
            cs_title = cs_game["title"]
            cs_discount = cs_game["discount"]
            cs_price_str = cs_game["price"]
            
            # Compare Titles (loose match or exact)
            title_exact = gd_title == cs_title
            title_starts = gd_title.startswith(cs_title) or cs_title.startswith(gd_title)
            
            # Compare Discounts (e.g. "65%" vs "-65%")
            clean_gd_disc = gd_discount.replace('%', '').replace('-', '').strip()
            clean_cs_disc = cs_discount.replace('%', '').replace('-', '').strip()
            discount_match = clean_gd_disc == clean_cs_disc
            
            # Compare Prices
            # Parse game_data prices
            gd_sale_num = re.findall(r'([0-9]+\.[0-9]+)', gd_sale_price_str)
            gd_reg_num = re.findall(r'([0-9]+\.[0-9]+)', gd_reg_price_str)
            
            # Parse compile_shorts prices
            cs_sale_val, cs_reg_val = extract_price(cs_price_str)
            
            sale_price_match = False
            reg_price_match = False
            
            # Deal with potential price ranges in Witcher 3 (e.g., "$3.99–$9.99")
            if gd_sale_num:
                if len(gd_sale_num) > 1:
                    # check if cs_sale_val is in range
                    sale_price_match = float(gd_sale_num[0]) <= cs_sale_val <= float(gd_sale_num[1])
                else:
                    sale_price_match = abs(float(gd_sale_num[0]) - cs_sale_val) < 0.01 if cs_sale_val else False
            
            if gd_reg_num:
                if len(gd_reg_num) > 1:
                    reg_price_match = float(gd_reg_num[0]) <= cs_reg_val <= float(gd_reg_num[1])
                else:
                    reg_price_match = abs(float(gd_reg_num[0]) - cs_reg_val) < 0.01 if cs_reg_val else False
                    
            report["game_data_vs_compile_shorts"].append({
                "genre": gen["name"],
                "index": i + 1,
                "compile_shorts_title": cs_title,
                "game_data_title": gd_title,
                "title_match": title_exact or title_starts,
                "compile_shorts_discount": cs_discount,
                "game_data_discount": gd_discount,
                "discount_match": discount_match,
                "compile_shorts_price": cs_price_str,
                "game_data_prices": f"Sale: {gd_sale_price_str} | Reg: {gd_reg_price_str}",
                "sale_price_match": sale_price_match,
                "reg_price_match": reg_price_match,
                "overall_match": (title_exact or title_starts) and discount_match and sale_price_match and reg_price_match
            })

    # 3. Parse scripts.md and compare with compile_shorts
    scripts_path = os.path.join(BASE_DIR, "scripts.md")
    # Section markers in scripts.md
    script_tables = parse_markdown_table(scripts_path, ["Estrategia en Tiempo Real", "Construcción y Gestión", "Rol de Acción"])
    
    genres_script = [
        {"name": "RTS", "s_key": "Estrategia en Tiempo Real", "cs_list": RTS_CS},
        {"name": "City Builder", "s_key": "Construcción y Gestión", "cs_list": CITY_CS},
        {"name": "ARPG", "s_key": "Rol de Acción", "cs_list": ARPG_CS}
    ]
    
    for gen in genres_script:
        s_rows = script_tables.get(gen["s_key"], [])
        cs_list = gen["cs_list"]
        
        # Filter game-specific rows (exclude Hook and CTA rows)
        # Game rows have "Primero", "Segundo", etc. in the locution or just match the 5 mid rows
        game_rows = []
        for row in s_rows:
            # We want rows that represent the 5 games.
            # Row index 1 to 5 (assuming 0 is Gancho, 6 is CTA)
            # Let's verify by the "Tiempo / Segmento" or presence of game name
            time_seg = row[0] if len(row) > 0 else ""
            if "Gancho" in time_seg or "Llamado" in time_seg:
                continue
            game_rows.append(row)
            
        if len(game_rows) != len(cs_list):
            report["scripts_vs_compile_shorts"].append({
                "genre": gen["name"],
                "error": f"Count mismatch: scripts.md has {len(game_rows)} game rows, compile_shorts.py has {len(cs_list)} games"
            })
            
        for i, cs_game in enumerate(cs_list):
            if i >= len(game_rows):
                break
            s_row = game_rows[i]
            # s_row format: [Tiempo/Segmento, Locucion, Sugerencia, Texto en Pantalla]
            # Column 4 has the text in screen: `**Game Title**<br>💥 **-65%** 💥`
            screen_text = s_row[3] if len(s_row) > 3 else ""
            
            # Extract game title and discount from screen_text
            # It uses markdown and HTML tags.
            # Let's extract bold strings
            bolds = re.findall(r'\*\*([^*]+)\*\*', screen_text)
            
            s_title = ""
            s_discount = ""
            if len(bolds) >= 2:
                s_title = bolds[0].strip()
                s_discount = bolds[1].strip()
            elif len(bolds) == 1:
                s_title = bolds[0].strip()
                
            cs_title = cs_game["title"]
            cs_discount = cs_game["discount"]
            
            title_exact = s_title == cs_title
            title_starts = s_title.startswith(cs_title) or cs_title.startswith(s_title)
            
            clean_s_disc = s_discount.replace('%', '').replace('-', '').strip()
            clean_cs_disc = cs_discount.replace('%', '').replace('-', '').strip()
            discount_match = clean_s_disc == clean_cs_disc
            
            # Also parse the locution to verify
            locution = s_row[1] if len(s_row) > 1 else ""
            
            report["scripts_vs_compile_shorts"].append({
                "genre": gen["name"],
                "index": i + 1,
                "compile_shorts_title": cs_title,
                "script_title": s_title,
                "title_match": title_exact or title_starts,
                "compile_shorts_discount": cs_discount,
                "script_discount": s_discount,
                "discount_match": discount_match,
                "locution": locution,
                "overall_match": (title_exact or title_starts) and discount_match
            })
            
    # 4. Verify compiled videos
    videos = [
        {"id": "RTS", "video": "RTS_short.mp4", "audio": "audio_rts.mp3"},
        {"id": "City", "video": "City_short.mp4", "audio": "audio_city.mp3"},
        {"id": "ARPG", "video": "ARPG_short.mp4", "audio": "audio_arpg.mp3"}
    ]
    
    for v in videos:
        v_path = os.path.join(BASE_DIR, v["video"])
        a_path = os.path.join(BASE_DIR, v["audio"])
        
        v_exists = os.path.exists(v_path)
        v_size = os.path.getsize(v_path) if v_exists else 0
        
        v_dur = get_duration(v_path) if v_exists else None
        a_dur = get_duration(a_path) if os.path.exists(a_path) else None
        
        durations_match = False
        duration_diff = None
        if isinstance(v_dur, float) and isinstance(a_dur, float):
            duration_diff = abs(v_dur - a_dur)
            durations_match = duration_diff <= 0.5 # Allow 0.5s difference
            
        report["videos"].append({
            "short_id": v["id"],
            "video_filename": v["video"],
            "video_exists": v_exists,
            "video_size_bytes": v_size,
            "video_duration": v_dur,
            "audio_filename": v["audio"],
            "audio_duration": a_dur,
            "duration_diff": duration_diff,
            "durations_match": durations_match,
            "valid": v_exists and v_size > 0 and durations_match
        })
        
    # Return formatted JSON report
    return report

if __name__ == "__main__":
    results = verify()
    print(json.dumps(results, indent=2, ensure_ascii=False))
