import os
import sys
import json
import math
import subprocess
import shutil
import time
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from concurrent.futures import ProcessPoolExecutor, as_completed

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
MANIFEST_FILE = os.path.join(BASE_DIR, "master_46_shorts_manifest.json")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_rendered_46_shorts")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load High Impact Fonts
def load_fonts():
    font_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
    font_reg = "C:\\Windows\\Fonts\\arial.ttf"
    if not os.path.exists(font_bold):
        font_bold = "C:\\Windows\\Fonts\\dejavusans-bold.ttf"
    if not os.path.exists(font_reg):
        font_reg = "C:\\Windows\\Fonts\\dejavusans.ttf"
        
    return {
        "title": ImageFont.truetype(font_bold, 44),
        "tag": ImageFont.truetype(font_bold, 28),
        "word_active": ImageFont.truetype(font_bold, 62),
        "word_normal": ImageFont.truetype(font_bold, 54),
        "badge": ImageFont.truetype(font_bold, 24)
    }

def get_audio_duration(filepath):
    if not filepath or not os.path.exists(filepath):
        return None
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        os.path.abspath(filepath)
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except Exception:
        return None

def extract_script_words_for_short(short_id):
    # Mapping to script files
    script_files = [
        os.path.join(BASE_DIR, "scripts_16_shorts_justiniano_belisario.md"),
        os.path.join(BASE_DIR, "scripts_15_shorts_rts_roma_2026.md"),
        os.path.join(BASE_DIR, "scripts_8_shorts_creadores_crisis.md"),
        os.path.join(BASE_DIR, "scripts_7_shorts_terremoto_bpo.md")
    ]
    
    for s_file in script_files:
        if not os.path.exists(s_file):
            continue
        with open(s_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        parts = content.split(f"## 📌 {short_id}:")
        if len(parts) >= 2:
            block = parts[1].strip()
            lines = block.split('\n')
            for i, line in enumerate(lines):
                if "Voz en off" in line:
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip()
                        if next_line.startswith('"') and next_line.endswith('"'):
                            raw_text = next_line[1:-1].strip()
                            words = [re.sub(r'^[¿"\'\(«]+|[?"\'\),\.»]+$', '', w).upper() for w in raw_text.split() if w.strip()]
                            return words
    return ["DOMINUSBABEL", "ESTRATEGIA", "Y", "TACTICA"]

def get_ken_burns_crop(img, width, height, progress, zoom_amount=0.15):
    base_w, base_h = img.size
    scale = 1.0 - (zoom_amount * progress)
    
    crop_w = int(base_w * scale)
    crop_h = int(base_h * scale)
    
    target_aspect = width / height
    if crop_w / crop_h > target_aspect:
        crop_w = int(crop_h * target_aspect)
    else:
        crop_h = int(crop_w / target_aspect)
        
    crop_x = int((base_w - crop_w) * 0.5)
    crop_y = int((base_h - crop_h) * 0.5)
    
    cropped = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
    return cropped.resize((width, height), Image.BICUBIC)

def select_thematic_background(short_id):
    # Select from local library of 2200+ high-res images
    if "justiniano" in short_id or "roma" in short_id:
        choices = [
            os.path.join(CAPSULES_DIR, "roman_short_6.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_1.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_2.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_3.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_4.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_5.jpg"),
            os.path.join(BASE_DIR, "jerusalem_586bc_burn_1785101757603.jpg"),
            os.path.join(BASE_DIR, "nebuchadnezzar_ishtar_gate_1785101770911.jpg")
        ]
    elif "rts" in short_id:
        choices = [
            os.path.join(BASE_DIR, "starcraft_art.jpg"),
            os.path.join(BASE_DIR, "seoul_starcraft_esports_stadium_1785096583089.jpg"),
            os.path.join(BASE_DIR, "warcraft_dota_art.jpg"),
            os.path.join(BASE_DIR, "manor_lords_art.jpg"),
            os.path.join(BASE_DIR, "cnc_art.jpg"),
            os.path.join(CAPSULES_DIR, "company_of_heroes_3_1675900.jpg"),
            os.path.join(CAPSULES_DIR, "against_the_storm_1336490.jpg"),
            os.path.join(CAPSULES_DIR, "age_of_empires_iv_1466860.jpg")
        ]
    elif "creadores" in short_id:
        choices = [
            os.path.join(BASE_DIR, "steam_library_1000_games_1785096605488.jpg"),
            os.path.join(BASE_DIR, "min_max_tier_list_guides_1785096628584.jpg"),
            os.path.join(BASE_DIR, "comfort_games_league_valorant_1785096616986.jpg"),
            os.path.join(BASE_DIR, "comfort_games_art.jpg")
        ]
    else: # Terremoto
        choices = [
            os.path.join(BASE_DIR, "bank_fee_penalty_1785106717402.jpg"),
            os.path.join(BASE_DIR, "poverty_premium_cycle_1785106693618.jpg"),
            os.path.join(BASE_DIR, "time_tax_transit_1785106749926.jpg"),
            os.path.join(BASE_DIR, "cheapflation_trap_1785106737875.jpg")
        ]
        
    for c in choices:
        if os.path.exists(c):
            return c
    return os.path.join(BASE_DIR, "background.jpg")

def create_vignette_overlay(width, height):
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vignette)
    
    # Top shadow for header readability
    for y in range(360):
        alpha = int(220 * (1.0 - (y / 360.0)**1.5))
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
        
    # Bottom shadow for subtitle readability
    for y in range(height - 600, height):
        ratio = (y - (height - 600)) / 600.0
        alpha = int(240 * (ratio**1.2))
        draw.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
        
    return vignette

def draw_outlined_text(draw, position, text, font, fill_color, outline_color, thickness=5, anchor="mm"):
    x, y = position
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx*dx + dy*dy <= thickness*thickness:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def render_pro_short(short_item, campaign_info):
    fonts = load_fonts()
    short_id = short_item["id"]
    output_mp4 = os.path.join(OUTPUT_DIR, f"{short_id}_final.mp4")
    
    audio_path = os.path.join(BASE_DIR, short_item["audio"])
    music_path = os.path.join(BASE_DIR, short_item["music"])
    
    if not os.path.exists(audio_path):
        return f"[SKIP] Missing audio: {audio_path}"
        
    duration = get_audio_duration(audio_path)
    if not duration:
        return f"[ERROR] Could not probe audio: {audio_path}"
        
    # 1. Clean Audio Mixing (Voice nominal 1.0 + Music at -23dB / 0.065)
    temp_mixed_wav = os.path.join(BASE_DIR, f"temp_{short_id}_mixed.wav")
    if os.path.exists(music_path):
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-stream_loop", "-1", "-i", music_path,
            "-filter_complex", f"[1:a]volume=0.065,afade=t=out:st={max(1.0, duration-0.8):.2f}:d=0.8[music];[0:a][music]amix=inputs=2:duration=first[aout]",
            "-map", "[aout]",
            "-ac", "2", "-ar", "44100",
            temp_mixed_wav
        ]
    else:
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-ac", "2", "-ar", "44100",
            temp_mixed_wav
        ]
    subprocess.run(cmd_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # 2. Extract Spoken Words for Dynamic Highlight Subtitles
    words = extract_script_words_for_short(short_id)
    total_words = len(words)
    
    # 3. Setup Canvas & Background
    fps = 30
    total_frames = int(duration * fps)
    width, height = 1080, 1920
    
    bg_img_path = select_thematic_background(short_id)
    raw_bg_img = Image.open(bg_img_path).convert("RGBA")
    vignette = create_vignette_overlay(width, height)
    
    # Theme Accent Colors
    if "justiniano" in short_id or "roma" in short_id:
        accent_color = (250, 200, 21) # Oro Bizantino (#FAC815)
        tag_text = "DOMINUSBABEL • HISTORIA Y TÁCTICA"
    elif "rts" in short_id:
        accent_color = (56, 189, 248) # Cyan Neón (#38BDF8)
        tag_text = "DOMINUSBABEL • ESTRATEGIA RTS 2026"
    elif "creadores" in short_id:
        accent_color = (244, 63, 94) # Magenta Neón (#F43F5E)
        tag_text = "DOMINUSBABEL • CULTURA DIGITAL & DEBATE"
    else: # Terremoto
        accent_color = (245, 158, 11) # Ámbar Alerta (#F59E0B)
        tag_text = "DOMINUSBABEL • SUCESOS & CRISIS"
        
    title_text = short_item.get("title", "").split("#")[0].strip().upper()
    if len(title_text) > 42:
        title_text = title_text[:40] + "..."
        
    temp_frames_dir = os.path.join(BASE_DIR, f"temp_frames_{short_id}")
    if os.path.exists(temp_frames_dir):
        shutil.rmtree(temp_frames_dir)
    os.makedirs(temp_frames_dir, exist_ok=True)
    
    # 4. Generate High-End Dynamic Frames
    for f_idx in range(total_frames):
        progress = f_idx / max(1, total_frames - 1)
        
        # A. Full-screen Cinematic Ken Burns Background
        frame = get_ken_burns_crop(raw_bg_img, width, height, progress, zoom_amount=0.14)
        
        # B. Apply Vignette / Contrast Darkening
        frame = Image.alpha_composite(frame, vignette)
        draw = ImageDraw.Draw(frame)
        
        # C. Top Glassmorphism Capsule Banner (Tercio Superior)
        top_y = 110
        draw_outlined_text(draw, (width // 2, top_y), tag_text, fonts["tag"], accent_color, (0, 0, 0), thickness=3)
        
        # Title with High Contrast Drop Shadow
        draw_outlined_text(draw, (width // 2, top_y + 60), title_text, fonts["title"], (255, 255, 255), (0, 0, 0), thickness=4)
        
        # Category Pill Badge
        badge_text = short_item.get("block", "ESPECIAL").upper()
        badge_w = 400
        badge_h = 48
        badge_x = (width - badge_w) // 2
        badge_y = top_y + 115
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(10, 15, 26, 200), outline=accent_color, width=2)
        draw.text((width // 2, badge_y + badge_h // 2), badge_text, font=fonts["badge"], fill=(255, 255, 255), anchor="mm")
        
        # D. Dynamic Kinetic Subtitle Window (Tercio Inferior: y = 1460px)
        active_idx = int(progress * total_words)
        active_idx = min(active_idx, total_words - 1)
        
        window_size = 4
        start_idx = max(0, active_idx - 1)
        end_idx = min(total_words, start_idx + window_size)
        if end_idx - start_idx < window_size and start_idx > 0:
            start_idx = max(0, end_idx - window_size)
            
        sub_chunk = words[start_idx:end_idx]
        
        # Subtitle Glass Panel
        sub_panel_w = 940
        sub_panel_h = 220
        sub_panel_x = (width - sub_panel_w) // 2
        sub_panel_y = 1420
        
        draw.rounded_rectangle([sub_panel_x, sub_panel_y, sub_panel_x + sub_panel_w, sub_panel_y + sub_panel_h], radius=24, fill=(12, 16, 28, 210), outline=(255, 255, 255, 60), width=2)
        
        # Render line of words with active word in Bold Gold / Neon
        line_text = "  ".join(sub_chunk)
        line_y = sub_panel_y + sub_panel_h // 2
        
        # Measure word positions
        word_spacings = []
        total_line_w = 0
        for i, w in enumerate(sub_chunk):
            is_active = (start_idx + i == active_idx)
            f_use = fonts["word_active"] if is_active else fonts["word_normal"]
            bbox = f_use.getbbox(w)
            w_width = bbox[2] - bbox[0]
            word_spacings.append((w, w_width, is_active, f_use))
            total_line_w += w_width + 24
            
        cur_x = (width - total_line_w) // 2 + 12
        for w, w_width, is_active, f_use in word_spacings:
            cx = cur_x + w_width // 2
            if is_active:
                # Active Spoken Word: Golden Yellow (#FAC815) with heavy black outline
                draw_outlined_text(draw, (cx, line_y), w, f_use, (250, 200, 21), (0, 0, 0), thickness=6)
            else:
                # Normal Word: Crisp White (#FFFFFF) with black outline
                draw_outlined_text(draw, (cx, line_y), w, f_use, (255, 255, 255), (0, 0, 0), thickness=4)
            cur_x += w_width + 24
            
        # E. Bottom Sleek Neon Progress Bar
        bar_x1 = 60
        bar_x2 = width - 60
        bar_y = height - 100
        draw.line([(bar_x1, bar_y), (bar_x2, bar_y)], fill=(50, 60, 80, 180), width=6)
        
        curr_bar_x = bar_x1 + int((bar_x2 - bar_x1) * progress)
        draw.line([(bar_x1, bar_y), (curr_bar_x, bar_y)], fill=accent_color, width=6)
        
        # Save frame
        frame_file = os.path.join(temp_frames_dir, f"frame_{f_idx:05d}.jpg")
        frame.convert("RGB").save(frame_file, quality=90)
        
    # 5. Compile with FFmpeg (CRF 19, Ultra-Crisp Quality)
    cmd_mp4 = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%05d.jpg"),
        "-i", temp_mixed_wav,
        "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    subprocess.run(cmd_mp4, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # Cleanup
    shutil.rmtree(temp_frames_dir)
    if os.path.exists(temp_mixed_wav):
        os.remove(temp_mixed_wav)
        
    size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    return f"[SUCCESS] {short_id} -> {output_mp4} ({size_mb:.2f} MB)"

def main():
    print("==================================================================")
    print("PRO SHORT COMPILER: 46 SHORTS (DOMINUSBABEL @dominus8735)")
    print("Standard: Full-Screen Ken Burns / Kinetic Tri-Tone Subtitles / Jorge TTS")
    print("==================================================================")
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    tasks = []
    for campaign in data.get("campaigns", []):
        for s in campaign.get("shorts", []):
            tasks.append((s, campaign))
            
    print(f"\nRenderizando {len(tasks)} shorts profesionales con multiprocesamiento...")
    start_time = time.time()
    
    completed = 0
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(render_pro_short, item[0], item[1]): item[0]["id"] for item in tasks}
        for future in as_completed(futures):
            res = future.result()
            completed += 1
            print(f"[{completed}/{len(tasks)}] {res}")
            
    elapsed = time.time() - start_time
    print(f"\n==================================================================")
    print(f"RENDERIZADO MAESTRO COMPLETADO: {completed}/{len(tasks)} videos en {elapsed:.1f}s")
    print(f"Carpeta de Salida: {OUTPUT_DIR}")
    print("==================================================================")

if __name__ == "__main__":
    main()
