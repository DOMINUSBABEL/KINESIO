import os
import sys
import json
import math
import subprocess
import shutil
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from concurrent.futures import ProcessPoolExecutor, as_completed

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
MANIFEST_FILE = os.path.join(BASE_DIR, "master_46_shorts_manifest.json")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_rendered_46_shorts")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load fonts
def load_fonts():
    font_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
    font_reg = "C:\\Windows\\Fonts\\arial.ttf"
    if not os.path.exists(font_bold):
        font_bold = "C:\\Windows\\Fonts\\dejavusans-bold.ttf"
    if not os.path.exists(font_reg):
        font_reg = "C:\\Windows\\Fonts\\dejavusans.ttf"
        
    return {
        "title": ImageFont.truetype(font_bold, 50),
        "category": ImageFont.truetype(font_bold, 30),
        "badge": ImageFont.truetype(font_bold, 26),
        "caption": ImageFont.truetype(font_bold, 54),
        "caption_sub": ImageFont.truetype(font_bold, 44),
        "channel": ImageFont.truetype(font_bold, 24)
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

# Map best thematic visual asset for each short
def get_best_image_for_short(short_id, campaign_id):
    # Specific mappings
    if "justiniano" in short_id or "roma" in short_id:
        roman_imgs = [
            os.path.join(CAPSULES_DIR, "roman_short_6.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_1.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_2.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_3.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_4.jpg"),
            os.path.join(CAPSULES_DIR, "roman_short_5.jpg"),
            os.path.join(BASE_DIR, "jerusalem_586bc_burn_1785101757603.jpg"),
            os.path.join(BASE_DIR, "nebuchadnezzar_ishtar_gate_1785101770911.jpg")
        ]
        for img in roman_imgs:
            if os.path.exists(img):
                return img
    elif "rts" in short_id:
        rts_imgs = [
            os.path.join(BASE_DIR, "starcraft_art.jpg"),
            os.path.join(BASE_DIR, "seoul_starcraft_esports_stadium_1785096583089.jpg"),
            os.path.join(BASE_DIR, "warcraft_dota_art.jpg"),
            os.path.join(BASE_DIR, "manor_lords_art.jpg"),
            os.path.join(BASE_DIR, "cnc_art.jpg"),
            os.path.join(CAPSULES_DIR, "company_of_heroes_3_1675900.jpg")
        ]
        for img in rts_imgs:
            if os.path.exists(img):
                return img
    elif "creadores" in short_id:
        creator_imgs = [
            os.path.join(BASE_DIR, "steam_library_1000_games_1785096605488.jpg"),
            os.path.join(BASE_DIR, "min_max_tier_list_guides_1785096628584.jpg"),
            os.path.join(BASE_DIR, "comfort_games_league_valorant_1785096616986.jpg"),
            os.path.join(BASE_DIR, "comfort_games_art.jpg")
        ]
        for img in creator_imgs:
            if os.path.exists(img):
                return img
    elif "terremoto" in short_id:
        bpo_imgs = [
            os.path.join(BASE_DIR, "bank_fee_penalty_1785106717402.jpg"),
            os.path.join(BASE_DIR, "poverty_premium_cycle_1785106693618.jpg"),
            os.path.join(BASE_DIR, "time_tax_transit_1785106749926.jpg")
        ]
        for img in bpo_imgs:
            if os.path.exists(img):
                return img
                
    # Fallback to default background
    fallback = os.path.join(BASE_DIR, "background.jpg")
    return fallback if os.path.exists(fallback) else None

def draw_outlined_text(draw, position, text, font, fill_color, outline_color, thickness=4, anchor="mm"):
    x, y = position
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx*dx + dy*dy <= thickness*thickness:
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def render_single_short(short_item, campaign_info):
    fonts = load_fonts()
    short_id = short_item["id"]
    output_mp4 = os.path.join(OUTPUT_DIR, f"{short_id}_final.mp4")
    
    audio_path = os.path.join(BASE_DIR, short_item["audio"])
    music_path = os.path.join(BASE_DIR, short_item["music"])
    
    if not os.path.exists(audio_path):
        return f"[SKIP] Missing audio for {short_id}"
        
    duration = get_audio_duration(audio_path)
    if not duration:
        return f"[ERROR] Could not probe audio duration for {short_id}"
        
    # 1. Mix Audio (Jorge Voice at 1.0 + Music at -23dB / 0.07 volume)
    temp_mixed_wav = os.path.join(BASE_DIR, f"temp_{short_id}_mixed.wav")
    if os.path.exists(music_path):
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", audio_path,
            "-stream_loop", "-1", "-i", music_path,
            "-filter_complex", "[1:a]volume=0.07,afade=t=out:st=" + str(max(1.0, duration-0.8)) + ":d=0.8[music];[0:a][music]amix=inputs=2:duration=first[aout]",
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
    
    # 2. Render Frames
    temp_frames_dir = os.path.join(BASE_DIR, f"temp_frames_{short_id}")
    if os.path.exists(temp_frames_dir):
        shutil.rmtree(temp_frames_dir)
    os.makedirs(temp_frames_dir, exist_ok=True)
    
    fps = 30
    total_frames = int(duration * fps)
    width, height = 1080, 1920
    
    # Visual source image
    art_path = get_best_image_for_short(short_id, campaign_info.get("campaign_id", ""))
    center_img = None
    if art_path and os.path.exists(art_path):
        try:
            center_img = Image.open(art_path).convert("RGBA")
        except Exception:
            center_img = None
            
    # Theme color palettes
    if "justiniano" in short_id or "roma" in short_id:
        bg_top = (16, 22, 38)
        bg_bot = (7, 10, 20)
        accent_color = (250, 200, 21) # Oro bizantino
        category_tag = "DOMINUSBABEL • HISTORIA TÁCTICA"
    elif "rts" in short_id:
        bg_top = (10, 26, 42)
        bg_bot = (4, 12, 22)
        accent_color = (56, 189, 248) # Cyan Neón
        category_tag = "DOMINUSBABEL • RTS & PC GAMING"
    elif "creadores" in short_id:
        bg_top = (28, 14, 38)
        bg_bot = (12, 6, 18)
        accent_color = (244, 63, 94) # Rosa Neón
        category_tag = "DOMINUSBABEL • CULTURA DIGITAL"
    else: # Terremoto
        bg_top = (30, 20, 12)
        bg_bot = (14, 8, 4)
        accent_color = (245, 158, 11) # Ámbar Alerta
        category_tag = "DOMINUSBABEL • SUCESOS & NEGOCIOS"
        
    title_text = short_item.get("title", "")
    # Clean emojis from primary header title to ensure crisp font rendering
    clean_title = title_text.split("#")[0].strip()
    if len(clean_title) > 38:
        clean_title = clean_title[:36] + "..."
        
    for f_idx in range(total_frames):
        t_sec = f_idx / fps
        progress = f_idx / max(1, total_frames - 1)
        
        # Base frame canvas
        frame = Image.new("RGBA", (width, height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(frame)
        
        # Gradient background
        for y in range(0, height, 4):
            ratio = y / height
            r = int(bg_top[0] * (1 - ratio) + bg_bot[0] * ratio)
            g = int(bg_top[1] * (1 - ratio) + bg_bot[1] * ratio)
            b = int(bg_top[2] * (1 - ratio) + bg_bot[2] * ratio)
            draw.rectangle([(0, y), (width, y + 4)], fill=(r, g, b, 255))
            
        # Top Channel & Category Bar
        header_y = 130
        draw.text((width // 2, header_y), category_tag, font=fonts["category"], fill=accent_color, anchor="mm")
        
        # Main Title Banner
        draw_outlined_text(draw, (width // 2, header_y + 60), clean_title.upper(), fonts["title"], (255, 255, 255), (0, 0, 0), thickness=3)
        
        # Floating Pill Badge
        badge_text = short_item.get("block", "ESPECIAL").upper()
        badge_y = header_y + 125
        badge_w, badge_h = 440, 54
        badge_x = (width - badge_w) // 2
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=14, fill=(15, 23, 42, 230), outline=accent_color, width=2)
        draw.text((width // 2, badge_y + badge_h // 2), badge_text, font=fonts["badge"], fill=(255, 255, 255), anchor="mm")
        
        # Center Showcase Box (Ken Burns slow zoom + Floating bob)
        panel_w, panel_h = 920, 880
        panel_x = (width - panel_w) // 2
        panel_y = 480
        bob = int(10 * math.sin(2 * math.pi * f_idx / 90)) # Harmonic breathing
        cur_panel_y = panel_y + bob
        
        if center_img:
            # Ken Burns zoom calculation
            scale = 1.0 + (0.12 * progress)
            cw = int(panel_w * scale)
            ch = int(panel_h * scale)
            
            # Crop center
            cropped = center_img.resize((cw, ch), Image.BICUBIC)
            ox = (cw - panel_w) // 2
            oy = (ch - panel_h) // 2
            cropped = cropped.crop((ox, oy, ox + panel_w, oy + panel_h))
            
            # Mask rounded corners
            mask = Image.new("L", (panel_w, panel_h), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.rounded_rectangle([0, 0, panel_w, panel_h], radius=24, fill=255)
            
            frame.paste(cropped, (panel_x, cur_panel_y), mask)
            draw.rounded_rectangle([panel_x, cur_panel_y, panel_x + panel_w, cur_panel_y + panel_h], radius=24, outline=accent_color, width=3)
        else:
            draw.rounded_rectangle([panel_x, cur_panel_y, panel_x + panel_w, cur_panel_y + panel_h], radius=24, fill=(20, 30, 50, 200), outline=accent_color, width=3)
            draw.text((width // 2, cur_panel_y + panel_h // 2), "DOMINUSBABEL", font=fonts["title"], fill=(255, 255, 255, 100), anchor="mm")
            
        # Lower Subtitle & Engagement Card
        sub_card_y = 1460
        sub_card_w, sub_card_h = 940, 260
        sub_card_x = (width - sub_card_w) // 2
        draw.rounded_rectangle([sub_card_x, sub_card_y, sub_card_x + sub_card_w, sub_card_y + sub_card_h], radius=20, fill=(10, 15, 28, 220), outline=(255, 255, 255, 40), width=2)
        
        # Audio / Spoken Callout Text in center of lower card
        draw_outlined_text(draw, (width // 2, sub_card_y + 80), "DOMINUSBABEL", fonts["channel"], accent_color, (0, 0, 0), thickness=2)
        draw_outlined_text(draw, (width // 2, sub_card_y + 160), "ESCUCHA CON ATENCIÓN 🎧", fonts["caption_sub"], (255, 255, 255), (0, 0, 0), thickness=3)
        
        # Bottom Neon Progress Bar
        bar_x1 = 70
        bar_x2 = width - 70
        bar_y = height - 120
        draw.line([(bar_x1, bar_y), (bar_x2, bar_y)], fill=(40, 50, 70, 200), width=6)
        
        cur_prog_x = bar_x1 + int((bar_x2 - bar_x1) * progress)
        draw.line([(bar_x1, bar_y), (cur_prog_x, bar_y)], fill=accent_color, width=6)
        
        # Save frame
        frame_path = os.path.join(temp_frames_dir, f"frame_{f_idx:05d}.jpg")
        frame.convert("RGB").save(frame_path, quality=88)
        
    # 3. Assemble Final MP4 with FFmpeg (Ultra High Quality CRF 19)
    cmd_mp4 = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%05d.jpg"),
        "-i", temp_mixed_wav,
        "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
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
    print("MASTER VIDEO RENDERER: 46 SHORTS (DOMINUSBABEL @dominus8735)")
    print("Estándar: 1080x1920 @ 30 FPS / Ken Burns / Tri-Tone / Audio Mixing")
    print("==================================================================")
    
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    tasks = []
    for campaign in data.get("campaigns", []):
        for s in campaign.get("shorts", []):
            tasks.append((s, campaign))
            
    print(f"\nIniciando renderizado de {len(tasks)} shorts con multiprocesamiento...")
    start_time = time.time()
    
    # Max workers set to 4 to balance CPU & Disk I/O smoothly
    completed = 0
    with ProcessPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(render_single_short, item[0], item[1]): item[0]["id"] for item in tasks}
        for future in as_completed(futures):
            res = future.result()
            completed += 1
            print(f"[{completed}/{len(tasks)}] {res}")
            
    elapsed = time.time() - start_time
    print(f"\n==================================================================")
    print(f"RENDERIZADO FINALIZADO: {completed}/{len(tasks)} videos en {elapsed:.1f} segundos.")
    print(f"Directorio de salida: {OUTPUT_DIR}")
    print("==================================================================")

if __name__ == "__main__":
    main()
