# -*- coding: utf-8 -*-
"""
MASTER PRO SHORT COMPILER (METALMANIA HIGH-END AUDIOVISUAL STANDARD)
Standard: 1080x1920 (9:16 Vertical HD @ 30 FPS / CRF 19)
Aesthetic: Multi-Scene Ken Burns (LANCZOS) / Glassmorphism Pills /
           Impact Headlines / Tri-Tone Kinetic Subtitles / Bottom Progress Bar
Audio: 100% Spanish Jorge Neural TTS + Sidechain Music (-23dB)
"""

import os
import sys
import json
import math
import shutil
import subprocess
import time
import re
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from concurrent.futures import ProcessPoolExecutor, as_completed

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
MANIFEST_FILE = os.path.join(BASE_DIR, "master_46_shorts_manifest.json")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_rendered_46_shorts")
os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
FPS = 30

# Typography Loader
def load_font(font_name, size):
    path = os.path.join(r"C:\Windows\Fonts", font_name)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", size)
        except Exception:
            return ImageFont.load_default()

FONT_BRAND = load_font("segoeuib.ttf", 26)
FONT_BADGE = load_font("segoeuib.ttf", 24)
FONT_HEADER = load_font("impact.ttf", 46)
FONT_SUBTITLE = load_font("segoeuib.ttf", 42)
FONT_FOOTER = load_font("segoeuib.ttf", 24)

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

def extract_script_text_for_short(short_id):
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
                            return next_line[1:-1].strip()
    return "DOMINUSBABEL • ESTRATEGIA Y TÁCTICA MILITAR"

def get_thematic_assets_for_short(short_id):
    if "justiniano" in short_id or "roma" in short_id:
        pool = [
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
        pool = [
            os.path.join(BASE_DIR, "starcraft_art.jpg"),
            os.path.join(BASE_DIR, "seoul_starcraft_esports_stadium_1785096583089.jpg"),
            os.path.join(BASE_DIR, "warcraft_dota_art.jpg"),
            os.path.join(BASE_DIR, "manor_lords_art.jpg"),
            os.path.join(BASE_DIR, "cnc_art.jpg"),
            os.path.join(CAPSULES_DIR, "company_of_heroes_3_1675900.jpg"),
            os.path.join(CAPSULES_DIR, "age_of_empires_iv_1466860.jpg"),
            os.path.join(CAPSULES_DIR, "against_the_storm_1336490.jpg")
        ]
    elif "creadores" in short_id:
        pool = [
            os.path.join(BASE_DIR, "steam_library_1000_games_1785096605488.jpg"),
            os.path.join(BASE_DIR, "min_max_tier_list_guides_1785096628584.jpg"),
            os.path.join(BASE_DIR, "comfort_games_league_valorant_1785096616986.jpg"),
            os.path.join(BASE_DIR, "comfort_games_art.jpg")
        ]
    else: # Terremoto
        pool = [
            os.path.join(BASE_DIR, "bank_fee_penalty_1785106717402.jpg"),
            os.path.join(BASE_DIR, "poverty_premium_cycle_1785106693618.jpg"),
            os.path.join(BASE_DIR, "time_tax_transit_1785106749926.jpg"),
            os.path.join(BASE_DIR, "cheapflation_trap_1785106737875.jpg")
        ]
        
    valid_pool = [p for p in pool if os.path.exists(p)]
    if not valid_pool:
        fallback = os.path.join(BASE_DIR, "background.jpg")
        valid_pool = [fallback] if os.path.exists(fallback) else []
    return valid_pool

def get_ken_burns_frame(img, width, height, progress, effect_type="zoom_in_macro"):
    bw, bh = img.size
    target_aspect = width / height # 0.5625
    
    if effect_type == "zoom_in_macro":
        scale = 0.96 - (0.16 * progress)
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = int((bw - cw) * (0.30 + 0.20 * progress))
        cy = int((bh - ch) * (0.25 + 0.20 * progress))
        
    elif effect_type == "pan_down":
        scale = 0.84
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = (bw - cw) // 2
        cy = int((bh - ch) * (0.15 + 0.60 * progress))
        
    elif effect_type == "zoom_out":
        scale = 0.80 + (0.16 * progress)
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = (bw - cw) // 2
        cy = (bh - ch) // 2
    else:
        scale = 0.88
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = (bw - cw) // 2
        cy = int((bh - ch) * (0.60 - 0.40 * progress))

    cx = max(0, min(bw - cw, cx))
    cy = max(0, min(bh - ch, cy))
    
    crop = img.crop((cx, cy, cx + cw, cy + ch))
    return crop.resize((width, height), Image.Resampling.LANCZOS)

def draw_outlined_text(draw, pos, text, font, fill_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), thickness=4, anchor="mm"):
    x, y = pos
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx*dx + dy*dy <= thickness*thickness and (dx != 0 or dy != 0):
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def get_word_highlight(word):
    clean = word.lower().strip(".,!?:;\"'¿¡«»")
    gold_keywords = ["roma", "belisario", "justiniano", "imperio", "victoria", "oro", "starcraft", "warhammer", "estrategia", "rts", "triunfo", "general", "trono", "leyes"]
    red_keywords = ["muertos", "masacre", "peste", "traicion", "destruyo", "suicida", "emboscada", "asesinato", "amenaza", "despido", "falsas", "colapso"]
    cyan_keywords = ["15.000", "30.000", "7.000", "150.000", "2.000", "532", "537", "541", "unreal", "steam", "esports", "dinero", "hipoteca", "ceo"]
    
    if any(k in clean for k in gold_keywords):
        return (250, 200, 21, 255) # Bright Gold (#FAC815)
    if any(k in clean for k in red_keywords):
        return (255, 77, 77, 255) # Fiery Red (#FF4D4D)
    if any(k in clean for k in cyan_keywords):
        return (0, 229, 255, 255) # Electric Cyan (#00E5FF)
    return (255, 255, 255, 255) # Crisp White

def render_kinetic_subtitles(draw, full_text, t_sec, total_duration, center_pos=(540, 1460)):
    if not full_text:
        return
        
    words = full_text.split()
    if not words:
        return
        
    progress = max(0.0, min(1.0, t_sec / max(total_duration, 0.1)))
    active_idx = min(int(progress * len(words)), len(words) - 1)
    
    # 4 to 6 word moving window
    window_size = 5
    start_idx = max(0, active_idx - 2)
    end_idx = min(len(words), start_idx + window_size)
    if end_idx - start_idx < window_size and start_idx > 0:
        start_idx = max(0, end_idx - window_size)
        
    sub_chunk = words[start_idx:end_idx]
    
    # Measure line length
    sample_img = Image.new("RGBA", (1, 1))
    sample_draw = ImageDraw.Draw(sample_img)
    space_w = sample_draw.textlength(" ", font=FONT_SUBTITLE)
    
    word_widths = [sample_draw.textlength(w, font=FONT_SUBTITLE) for w in sub_chunk]
    total_w = sum(word_widths) + space_w * (len(sub_chunk) - 1)
    
    panel_pad_x = 44
    panel_pad_y = 26
    panel_w = int(total_w + panel_pad_x * 2)
    panel_h = 130
    panel_x = center_pos[0] - panel_w // 2
    panel_y = center_pos[1] - panel_h // 2
    
    # Glassmorphism dark panel with gold border
    draw.rounded_rectangle(
        [panel_x, panel_y, panel_x + panel_w, panel_y + panel_h],
        radius=22,
        fill=(10, 14, 24, 215),
        outline=(250, 200, 21, 80),
        width=2
    )
    
    # Draw words
    cur_x = center_pos[0] - (total_w / 2)
    line_y = center_pos[1]
    
    for i, (w_str, ww) in enumerate(zip(sub_chunk, word_widths)):
        global_idx = start_idx + i
        is_active = (global_idx == active_idx)
        
        if is_active:
            w_color = (250, 200, 21, 255) # Bright Gold
            # Neon Gold Text Glow
            for r in range(1, 4):
                draw.text((cur_x + ww/2, line_y), w_str, font=FONT_SUBTITLE, fill=(250, 200, 21, 70), anchor="mm")
        else:
            w_color = get_word_highlight(w_str)
            
        draw_outlined_text(draw, (cur_x + ww/2, line_y), w_str, FONT_SUBTITLE, fill_color=w_color, thickness=4, anchor="mm")
        cur_x += ww + space_w

def render_metalmania_short(short_item, campaign_info):
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
    
    # 2. Extract Full Script Text
    full_script_text = extract_script_text_for_short(short_id)
    
    # 3. Setup Thematic Scenes (Multi-Scene Ken Burns Transition)
    asset_pool = get_thematic_assets_for_short(short_id)
    raw_images = [Image.open(p).convert("RGBA") for p in asset_pool[:3]] if asset_pool else []
    
    effects = ["zoom_in_macro", "pan_down", "zoom_out"]
    
    # Category / Branding Configuration
    if "justiniano" in short_id or "roma" in short_id:
        brand_pill = "👑 DOMINUSBABEL • LA RECONQUISTA DE ROMA"
        header_badge = short_item.get("block", "HISTORIA TÁCTICA").upper()
        header_color = (250, 200, 21, 255) # Gold
        footer_text = "⚔️ SUSCRÍBETE PARA MÁS ESTRATEGIA E HISTORIA BÉLICA"
    elif "rts" in short_id:
        brand_pill = "🚀 DOMINUSBABEL • ESTRATEGIA RTS 2026"
        header_badge = short_item.get("block", "PC GAMING & STEAM").upper()
        header_color = (0, 229, 255, 255) # Electric Cyan
        footer_text = "⚡ DOMINUSBABEL • LA ERA DORADA DEL RTS"
    elif "creadores" in short_id:
        brand_pill = "🎭 DOMINUSBABEL • CULTURA DIGITAL & DEBATE"
        header_badge = short_item.get("block", "ANÁLISIS DE CREADORES").upper()
        header_color = (255, 77, 77, 255) # Fiery Red
        footer_text = "👀 DEBATE ABIERTO • COMPARTE TU OPINIÓN ABAJO"
    else: # Terremoto
        brand_pill = "🏢 DOMINUSBABEL • SUCESOS & CRISIS"
        header_badge = short_item.get("block", "DERECHOS LABORALES").upper()
        header_color = (245, 158, 11, 255) # Ámbar Alerta
        footer_text = "⚠️ SUCESOS VIRALES & RELACIONES PÚBLICAS"

    clean_headline = short_item.get("title", "").split("#")[0].strip().upper()
    if len(clean_headline) > 46:
        clean_headline = clean_headline[:44] + "..."

    # 4. Generate High-Quality Frames
    temp_frames_dir = os.path.join(BASE_DIR, f"temp_frames_{short_id}")
    if os.path.exists(temp_frames_dir):
        shutil.rmtree(temp_frames_dir)
    os.makedirs(temp_frames_dir, exist_ok=True)
    
    total_frames = int(duration * FPS)
    num_scenes = max(1, len(raw_images))
    frames_per_scene = total_frames / num_scenes
    
    sample_img = Image.new("RGBA", (1, 1))
    s_draw = ImageDraw.Draw(sample_img)
    
    for f_idx in range(total_frames):
        t_sec = f_idx / FPS
        overall_prog = f_idx / max(1, total_frames - 1)
        
        # Determine active scene & local progress
        sc_idx = min(int(f_idx / frames_per_scene), num_scenes - 1)
        sc_prog = (f_idx % frames_per_scene) / max(1.0, frames_per_scene)
        
        active_img = raw_images[sc_idx] if raw_images else Image.new("RGBA", (WIDTH, HEIGHT), (12, 16, 28, 255))
        eff = effects[sc_idx % len(effects)]
        
        # A. Ken Burns Cinematic Render
        frame = get_ken_burns_frame(active_img, WIDTH, HEIGHT, sc_prog, eff)
        
        # B. Dual Cinematic Gradient Overlays (Top & Bottom)
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Soft framing border
        draw.rectangle([0, 0, WIDTH, HEIGHT], outline=(0, 0, 0, 120), width=20)
        
        # Top gradient (280px)
        for y in range(280):
            alpha = int(210 * (1.0 - (y / 280.0)**1.3))
            draw.line([(0, y), (WIDTH, y)], fill=(5, 8, 15, alpha))
            
        # Bottom gradient (420px)
        for y in range(HEIGHT - 420, HEIGHT):
            ratio = (y - (HEIGHT - 420)) / 420.0
            alpha = int(230 * (ratio**1.1))
            draw.line([(0, y), (WIDTH, y)], fill=(5, 8, 15, alpha))
            
        # --- TOP BRAND PILL (y=55) ---
        bw = int(s_draw.textlength(brand_pill, font=FONT_BRAND)) + 48
        bx = (WIDTH - bw) // 2
        draw.rounded_rectangle([bx, 50, bx + bw, 98], radius=16, fill=(12, 16, 28, 230), outline=(250, 200, 21, 160), width=2)
        draw.text((WIDTH // 2, 74), brand_pill, font=FONT_BRAND, fill=(255, 255, 255, 255), anchor="mm")
        
        # --- SCENE HOOK BADGE (y=120) ---
        badgew = int(s_draw.textlength(header_badge, font=FONT_BADGE)) + 36
        badgex = (WIDTH - badgew) // 2
        draw.rounded_rectangle([badgex, 116, badgex + badgew, 156], radius=12, fill=header_color, outline=(255, 255, 255, 100), width=1)
        draw.text((WIDTH // 2, 136), header_badge, font=FONT_BADGE, fill=(10, 14, 24, 255), anchor="mm")
        
        # --- IMPACT HEADLINE BANNER (y=190-230) ---
        draw_outlined_text(draw, (WIDTH // 2, 205), clean_headline, FONT_HEADER, fill_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), thickness=5)
        
        # --- KINETIC TRI-TONE SUBTITLES (y=1460) ---
        render_kinetic_subtitles(draw, full_script_text, t_sec, duration, center_pos=(WIDTH // 2, 1460))
        
        # --- BOTTOM BRAND FOOTER PILL (y=1805) ---
        footw = int(s_draw.textlength(footer_text, font=FONT_FOOTER)) + 40
        footx = (WIDTH - footw) // 2
        draw.rounded_rectangle([footx, 1785, footx + footw, 1825], radius=12, fill=(10, 14, 24, 220), outline=(255, 255, 255, 40), width=1)
        draw.text((WIDTH // 2, 1805), footer_text, font=FONT_FOOTER, fill=(250, 200, 21, 240), anchor="mm")
        
        # --- BOTTOM NEON PROGRESS BAR (y=1865) ---
        bar_x1 = 50
        bar_x2 = WIDTH - 50
        bar_y = 1865
        draw.line([(bar_x1, bar_y), (bar_x2, bar_y)], fill=(40, 50, 70, 200), width=6)
        
        curr_bar_x = bar_x1 + int((bar_x2 - bar_x1) * overall_prog)
        draw.line([(bar_x1, bar_y), (curr_bar_x, bar_y)], fill=(250, 200, 21, 255), width=6)
        
        # Composite frame
        final_frame = Image.alpha_composite(frame, overlay)
        
        # Save frame
        frame_file = os.path.join(temp_frames_dir, f"frame_{f_idx:05d}.jpg")
        final_frame.convert("RGB").save(frame_file, quality=90)
        
    # 5. FFmpeg Assembly (CRF 19, Ultra-Crisp Quality)
    cmd_mp4 = [
        "ffmpeg", "-y",
        "-r", str(FPS),
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
    print("PRO MASTER SHORT COMPILER (METALMANIA AESTHETIC STANDARD)")
    print("Standard: Full-Screen Ken Burns / Glassmorphism / Impact Headers / Kinetic Subtitles")
    print("==================================================================")
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    tasks = []
    for campaign in data.get("campaigns", []):
        for s in campaign.get("shorts", []):
            tasks.append((s, campaign))
            
    print(f"\nIniciando renderizado maestro de {len(tasks)} shorts...")
    start_time = time.time()
    
    completed = 0
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(render_metalmania_short, item[0], item[1]): item[0]["id"] for item in tasks}
        for future in as_completed(futures):
            res = future.result()
            completed += 1
            print(f"[{completed}/{len(tasks)}] {res}")
            
    elapsed = time.time() - start_time
    print(f"\n==================================================================")
    print(f"COMPILACIÓN MAESTRA COMPLETADA: {completed}/{len(tasks)} videos en {elapsed:.1f}s")
    print(f"Carpeta de Salida: {OUTPUT_DIR}")
    print("==================================================================")

if __name__ == "__main__":
    main()
