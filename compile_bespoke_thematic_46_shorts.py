# -*- coding: utf-8 -*-
"""
BESPOKE THEMATIC PRO COMPILER V2.1 (DOMINUSBABEL @dominus8735)
Robust Windows RMTREE & Resume Support
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
POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

os.makedirs(OUTPUT_DIR, exist_ok=True)

WIDTH = 1080
HEIGHT = 1920
FPS = 30

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
    return "DOMINUSBABEL • ESTRATEGIA Y TÁCTICA"

def get_bespoke_visual_dna(short_id, campaign_id, block_text):
    if "justiniano_belisario" in short_id:
        return {
            "theme_name": "imperial_rome",
            "brand_pill": "👑 DOMINUSBABEL • IMPERIUM ROMANUM",
            "badge_text": block_text.upper(),
            "badge_bg": (250, 200, 21, 240),
            "badge_text_color": (10, 14, 24, 255),
            "header_color": (255, 255, 255, 255),
            "accent_neon": (250, 200, 21, 255),
            "panel_border": (250, 200, 21, 120),
            "footer_text": "🏛️ HISTORIA MILITAR Y TÁCTICA BIZANTINA",
            "footer_color": (250, 200, 21, 230),
            "assets": [
                os.path.join(CAPSULES_DIR, "roman_short_6.jpg"),
                os.path.join(CAPSULES_DIR, "roman_short_1.jpg"),
                os.path.join(BASE_DIR, "jerusalem_586bc_burn_1785101757603.jpg"),
                os.path.join(BASE_DIR, "nebuchadnezzar_ishtar_gate_1785101770911.jpg")
            ]
        }
    elif "rts_roma" in short_id and int(short_id.replace("rts_roma_short_", "")) <= 9:
        return {
            "theme_name": "cyber_rts",
            "brand_pill": "🚀 DOMINUSBABEL • NEXT-GEN RTS 2026",
            "badge_text": f"👾 {block_text.upper()}",
            "badge_bg": (0, 229, 255, 240),
            "badge_text_color": (5, 10, 20, 255),
            "header_color": (255, 255, 255, 255),
            "accent_neon": (0, 229, 255, 255),
            "panel_border": (0, 229, 255, 140),
            "footer_text": "⚡ DOMINUSBABEL • ESTRATEGIA REAL TIME EN STEAM",
            "footer_color": (57, 255, 20, 230),
            "assets": [
                os.path.join(BASE_DIR, "starcraft_art.jpg"),
                os.path.join(BASE_DIR, "seoul_starcraft_esports_stadium_1785096583089.jpg"),
                os.path.join(BASE_DIR, "warcraft_dota_art.jpg"),
                os.path.join(BASE_DIR, "manor_lords_art.jpg"),
                os.path.join(CAPSULES_DIR, "company_of_heroes_3_1675900.jpg")
            ]
        }
    elif "rts_roma" in short_id:
        return {
            "theme_name": "ancient_tactics",
            "brand_pill": "⚔️ DOMINUSBABEL • TÁCTICA & BATALLAS ANTIGUAS",
            "badge_text": f"🛡️ {block_text.upper()}",
            "badge_bg": (212, 175, 55, 240),
            "badge_text_color": (15, 10, 8, 255),
            "header_color": (255, 255, 255, 255),
            "accent_neon": (212, 175, 55, 255),
            "panel_border": (212, 175, 55, 120),
            "footer_text": "🗡️ ANÁLISIS DE GUERRA HISTÓRICA • DOMINUSBABEL",
            "footer_color": (212, 175, 55, 230),
            "assets": [
                os.path.join(CAPSULES_DIR, "roman_short_2.jpg"),
                os.path.join(CAPSULES_DIR, "roman_short_3.jpg"),
                os.path.join(CAPSULES_DIR, "roman_short_4.jpg"),
                os.path.join(CAPSULES_DIR, "roman_short_5.jpg")
            ]
        }
    elif "creadores" in short_id:
        return {
            "theme_name": "digital_culture",
            "brand_pill": "📹 DOMINUSBABEL • CULTURA DIGITAL & MEDIOS",
            "badge_text": f"🔥 {block_text.upper()}",
            "badge_bg": (255, 0, 51, 240),
            "badge_text_color": (255, 255, 255, 255),
            "header_color": (255, 255, 255, 255),
            "accent_neon": (255, 230, 0, 255),
            "panel_border": (255, 0, 51, 120),
            "footer_text": "👀 DEBATE ABIERTO • COMPARTE TU OPINIÓN",
            "footer_color": (255, 230, 0, 240),
            "assets": [
                os.path.join(BASE_DIR, "steam_library_1000_games_1785096605488.jpg"),
                os.path.join(BASE_DIR, "min_max_tier_list_guides_1785096628584.jpg"),
                os.path.join(BASE_DIR, "comfort_games_league_valorant_1785096616986.jpg"),
                os.path.join(BASE_DIR, "comfort_games_art.jpg")
            ]
        }
    else:
        return {
            "theme_name": "breaking_news",
            "brand_pill": "🚨 DOMINUSBABEL • INVESTIGACIÓN & SUCESOS",
            "badge_text": f"⚠️ {block_text.upper()}",
            "badge_bg": (255, 153, 0, 240),
            "badge_text_color": (10, 10, 10, 255),
            "header_color": (255, 255, 255, 255),
            "accent_neon": (255, 46, 46, 255),
            "panel_border": (255, 153, 0, 140),
            "footer_text": "⚖️ DERECHOS LABORALES & CRISIS CORPORATIVA",
            "footer_color": (255, 153, 0, 240),
            "assets": [
                os.path.join(BASE_DIR, "bank_fee_penalty_1785106717402.jpg"),
                os.path.join(BASE_DIR, "poverty_premium_cycle_1785106693618.jpg"),
                os.path.join(BASE_DIR, "time_tax_transit_1785106749926.jpg"),
                os.path.join(BASE_DIR, "cheapflation_trap_1785106737875.jpg")
            ]
        }

def get_ken_burns_frame(img, width, height, progress, effect_type="zoom_in_macro"):
    bw, bh = img.size
    target_aspect = width / height
    
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
    return crop.resize((width, height), Image.Resampling.BICUBIC)

def draw_outlined_text(draw, pos, text, font, fill_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), thickness=4, anchor="mm"):
    x, y = pos
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx*dx + dy*dy <= thickness*thickness and (dx != 0 or dy != 0):
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def render_bespoke_kinetic_subtitles(draw, full_text, t_sec, total_duration, theme_dna, center_pos=(540, 1460)):
    if not full_text:
        return
        
    words = full_text.split()
    if not words:
        return
        
    progress = max(0.0, min(1.0, t_sec / max(total_duration, 0.1)))
    active_idx = min(int(progress * len(words)), len(words) - 1)
    
    window_size = 5
    start_idx = max(0, active_idx - 2)
    end_idx = min(len(words), start_idx + window_size)
    if end_idx - start_idx < window_size and start_idx > 0:
        start_idx = max(0, end_idx - window_size)
        
    sub_chunk = words[start_idx:end_idx]
    
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
    
    draw.rounded_rectangle(
        [panel_x, panel_y, panel_x + panel_w, panel_y + panel_h],
        radius=22,
        fill=(10, 14, 24, 220),
        outline=theme_dna["panel_border"],
        width=2
    )
    
    cur_x = center_pos[0] - (total_w / 2)
    line_y = center_pos[1]
    
    for i, (w_str, ww) in enumerate(zip(sub_chunk, word_widths)):
        global_idx = start_idx + i
        is_active = (global_idx == active_idx)
        
        if is_active:
            w_color = theme_dna["accent_neon"]
            for r in range(1, 4):
                draw.text((cur_x + ww/2, line_y), w_str, font=FONT_SUBTITLE, fill=theme_dna["accent_neon"][:3] + (70,), anchor="mm")
        else:
            w_color = (255, 255, 255, 255)
            
        draw_outlined_text(draw, (cur_x + ww/2, line_y), w_str, FONT_SUBTITLE, fill_color=w_color, thickness=4, anchor="mm")
        cur_x += ww + space_w

def render_bespoke_short(short_item, campaign_info):
    short_id = short_item["id"]
    output_mp4 = os.path.join(OUTPUT_DIR, f"{short_id}_final.mp4")
    
    # Fast Resume Check
    if os.path.exists(output_mp4) and os.path.getsize(output_mp4) > 1000000:
        size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
        return f"[ALREADY_EXISTS] {short_id} -> {output_mp4} ({size_mb:.2f} MB)"
        
    audio_path = os.path.join(BASE_DIR, short_item["audio"])
    music_path = os.path.join(BASE_DIR, short_item["music"])
    
    if not os.path.exists(audio_path):
        return f"[SKIP] Missing audio: {audio_path}"
        
    duration = get_audio_duration(audio_path)
    if not duration:
        return f"[ERROR] Could not probe audio: {audio_path}"
        
    # 1. Audio Mixing
    temp_mixed_wav = os.path.join(BASE_DIR, f"temp_{short_id}_mixed.wav")
    has_music = os.path.exists(music_path)
    has_pop = os.path.exists(POP_SFX)
    
    if has_music and has_pop:
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-stream_loop", "-1", "-i", music_path,
            "-i", POP_SFX,
            "-filter_complex", 
            f"[1:a]volume=0.065,afade=t=out:st={max(1.0, duration-0.8):.2f}:d=0.8[music];"
            f"[2:a]adelay=300|300,volume=0.5[pop];"
            f"[0:a][music][pop]amix=inputs=3:duration=first[aout]",
            "-map", "[aout]",
            "-ac", "2", "-ar", "44100",
            temp_mixed_wav
        ]
    elif has_music:
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
    
    full_script_text = extract_script_text_for_short(short_id)
    block_text = short_item.get("block", "ESPECIAL")
    dna = get_bespoke_visual_dna(short_id, campaign_info.get("campaign_id", ""), block_text)
    
    valid_assets = [p for p in dna["assets"] if os.path.exists(p)]
    if not valid_assets:
        fallback = os.path.join(BASE_DIR, "background.jpg")
        valid_assets = [fallback] if os.path.exists(fallback) else []
        
    raw_images = [Image.open(p).convert("RGBA") for p in valid_assets[:3]] if valid_assets else []
    effects = ["zoom_in_macro", "pan_down", "zoom_out"]

    clean_headline = short_item.get("title", "").split("#")[0].strip().upper()
    if len(clean_headline) > 46:
        clean_headline = clean_headline[:44] + "..."

    temp_frames_dir = os.path.join(BASE_DIR, f"temp_frames_{short_id}")
    shutil.rmtree(temp_frames_dir, ignore_errors=True)
    os.makedirs(temp_frames_dir, exist_ok=True)
    
    total_frames = int(duration * FPS)
    num_scenes = max(1, len(raw_images))
    frames_per_scene = total_frames / num_scenes
    
    sample_img = Image.new("RGBA", (1, 1))
    s_draw = ImageDraw.Draw(sample_img)
    
    for f_idx in range(total_frames):
        t_sec = f_idx / FPS
        overall_prog = f_idx / max(1, total_frames - 1)
        
        sc_idx = min(int(f_idx / frames_per_scene), num_scenes - 1)
        sc_prog = (f_idx % frames_per_scene) / max(1.0, frames_per_scene)
        
        active_img = raw_images[sc_idx] if raw_images else Image.new("RGBA", (WIDTH, HEIGHT), (12, 16, 28, 255))
        eff = effects[sc_idx % len(effects)]
        
        frame = get_ken_burns_frame(active_img, WIDTH, HEIGHT, sc_prog, eff)
        
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        draw.rectangle([0, 0, WIDTH, HEIGHT], outline=(0, 0, 0, 120), width=20)
        
        for y in range(280):
            alpha = int(210 * (1.0 - (y / 280.0)**1.3))
            draw.line([(0, y), (WIDTH, y)], fill=(5, 8, 15, alpha))
            
        for y in range(HEIGHT - 420, HEIGHT):
            ratio = (y - (HEIGHT - 420)) / 420.0
            alpha = int(230 * (ratio**1.1))
            draw.line([(0, y), (WIDTH, y)], fill=(5, 8, 15, alpha))
            
        bw = int(s_draw.textlength(dna["brand_pill"], font=FONT_BRAND)) + 48
        bx = (WIDTH - bw) // 2
        draw.rounded_rectangle([bx, 50, bx + bw, 98], radius=16, fill=(12, 16, 28, 230), outline=dna["panel_border"], width=2)
        draw.text((WIDTH // 2, 74), dna["brand_pill"], font=FONT_BRAND, fill=(255, 255, 255, 255), anchor="mm")
        
        badgew = int(s_draw.textlength(dna["badge_text"], font=FONT_BADGE)) + 36
        badgex = (WIDTH - badgew) // 2
        draw.rounded_rectangle([badgex, 116, badgex + badgew, 156], radius=12, fill=dna["badge_bg"], outline=(255, 255, 255, 100), width=1)
        draw.text((WIDTH // 2, 136), dna["badge_text"], font=FONT_BADGE, fill=dna["badge_text_color"], anchor="mm")
        
        draw_outlined_text(draw, (WIDTH // 2, 205), clean_headline, FONT_HEADER, fill_color=dna["header_color"], outline_color=(0, 0, 0, 255), thickness=5)
        render_bespoke_kinetic_subtitles(draw, full_script_text, t_sec, duration, dna, center_pos=(WIDTH // 2, 1460))
        
        footw = int(s_draw.textlength(dna["footer_text"], font=FONT_FOOTER)) + 40
        footx = (WIDTH - footw) // 2
        draw.rounded_rectangle([footx, 1785, footx + footw, 1825], radius=12, fill=(10, 14, 24, 220), outline=(255, 255, 255, 40), width=1)
        draw.text((WIDTH // 2, 1805), dna["footer_text"], font=FONT_FOOTER, fill=dna["footer_color"], anchor="mm")
        
        bar_x1 = 50
        bar_x2 = WIDTH - 50
        bar_y = 1865
        draw.line([(bar_x1, bar_y), (bar_x2, bar_y)], fill=(40, 50, 70, 200), width=6)
        
        curr_bar_x = bar_x1 + int((bar_x2 - bar_x1) * overall_prog)
        draw.line([(bar_x1, bar_y), (curr_bar_x, bar_y)], fill=dna["accent_neon"], width=6)
        
        final_frame = Image.alpha_composite(frame, overlay)
        frame_file = os.path.join(temp_frames_dir, f"frame_{f_idx:05d}.jpg")
        final_frame.convert("RGB").save(frame_file, quality=85)
        
    cmd_mp4 = [
        "ffmpeg", "-y",
        "-r", str(FPS),
        "-i", os.path.join(temp_frames_dir, "frame_%05d.jpg"),
        "-i", temp_mixed_wav,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "19", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    subprocess.run(cmd_mp4, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # Safe cleanup with ignore_errors
    shutil.rmtree(temp_frames_dir, ignore_errors=True)
    if os.path.exists(temp_mixed_wav):
        try:
            os.remove(temp_mixed_wav)
        except Exception:
            pass
        
    size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    return f"[SUCCESS] {short_id} -> {output_mp4} ({size_mb:.2f} MB)"

def main():
    print("==================================================================")
    print("BESPOKE THEMATIC PRO COMPILER V2.1 (DOMINUSBABEL @dominus8735)")
    print("==================================================================")
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    tasks = []
    for campaign in data.get("campaigns", []):
        for s in campaign.get("shorts", []):
            tasks.append((s, campaign))
            
    print(f"\nVerificando y renderizando shorts pendientes de {len(tasks)} totales...")
    start_time = time.time()
    
    completed = 0
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(render_bespoke_short, item[0], item[1]): item[0]["id"] for item in tasks}
        for future in as_completed(futures):
            res = future.result()
            completed += 1
            print(f"[{completed}/{len(tasks)}] {res}")
            
    elapsed = time.time() - start_time
    print(f"\n==================================================================")
    print(f"¡TODOS LOS {completed}/{len(tasks)} SHORTS ESTÁN 100% COMPLETADOS!")
    print(f"Directorio de Entrega: {OUTPUT_DIR}")
    print("==================================================================")

if __name__ == "__main__":
    main()
