# -*- coding: utf-8 -*-
"""
KINESIO & VAREGO MASTER MP4 VIDEO RENDERER
Renders 23 vertical MP4 Shorts (13 Narco China + 10 Guerra Antigua)
Estándar: KINESIO V5.5 / 9:16 Vertical (1080x1920) / Subtítulos Tri-Tono / Badges Flotantes
"""

import os
import sys
import math
import subprocess
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_assets")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_videos")

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

from kinesio_core import get_audio_duration, parse_vtt_subtitles, get_ken_burns_crop

# Audio / Music / Badges mapping
RENDER_CONFIGS = [
    # Narco China (13 Shorts)
    {"id": "narco_china_short_1", "title": "TRANSACCIONES ESPEJO", "badge": "DÚO 1: PARTE 1/2", "music": "Cipher2.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_2", "title": "DE LICEOS A MAR-A-LAGO", "badge": "DÚO 1: PARTE 2/2", "music": "Volatile Reaction.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_3", "title": "PRECURSORES DE WUHAN", "badge": "DÚO 2: PARTE 1/2", "music": "Cipher2.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_4", "title": "GUERRA ASIMÉTRICA PCC", "badge": "DÚO 2: PARTE 2/2", "music": "Clash Defiant.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_5", "title": "POR QUÉ FALLA LA DEA", "badge": "AUTÓNOMO 05/13", "music": "Volatile Reaction.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_6", "title": "GRANJAS EN MAINE", "badge": "AUTÓNOMO 06/13", "music": "Sneaky Snitch.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_7", "title": "EL TRUCO DEL 3%", "badge": "AUTÓNOMO 07/13", "music": "Severe Tire Damage.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_8", "title": "CÁRTELES SIN BANCOS", "badge": "AUTÓNOMO 08/13", "music": "Cipher2.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_9", "title": "XIZHI LI: EL LIMPIADOR", "badge": "AUTÓNOMO 09/13", "music": "Volatile Reaction.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_10", "title": "FUGA DE CAPITALES", "badge": "AUTÓNOMO 10/13", "music": "Cipher2.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_11", "title": "FRAUDE EN ADUANAS", "badge": "AUTÓNOMO 11/13", "music": "Clash Defiant.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_12", "title": "FENTANILO Y GUERRA", "badge": "AUTÓNOMO 12/13", "music": "Volatile Reaction.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    {"id": "narco_china_short_13", "title": "EL IMPERIO GLOBAL", "badge": "AUTÓNOMO 13/13", "music": "Future Gladiator.mp3", "category": "GEOPOLÍTICA Y NARCOTRÁFICO"},
    
    # Guerra Antigua (10 Shorts)
    {"id": "guerra_antigua_short_1", "title": "EL MITO DE HOLLYWOOD", "badge": "HISTORIA MILITAR 01/10", "music": "Clash Defiant.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_2", "title": "EL MURO DE ESCUDOS", "badge": "HISTORIA MILITAR 02/10", "music": "Volatile Reaction.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_3", "title": "EL CANSANCIO EXTREMO", "badge": "HISTORIA MILITAR 03/10", "music": "Rites.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_4", "title": "EL SANGRIENTO OTHISMOS", "badge": "HISTORIA MILITAR 04/10", "music": "Clash Defiant.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_5", "title": "EXCEPCIÓN DE MARATÓN", "badge": "HISTORIA MILITAR 05/10", "music": "Moorland.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_6", "title": "GRADUS MILITARIS", "badge": "HISTORIA MILITAR 06/10", "music": "Volatile Reaction.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_7", "title": "LA MASACRE DE LA HUIDA", "badge": "HISTORIA MILITAR 07/10", "music": "Clash Defiant.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_8", "title": "FLAUTAS Y FALANGE", "badge": "HISTORIA MILITAR 08/10", "music": "Rites.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_9", "title": "HASTINGS 1066", "badge": "HISTORIA MILITAR 09/10", "music": "Moorland.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"},
    {"id": "guerra_antigua_short_10", "title": "LA REGLA DEL VETERANO", "badge": "HISTORIA MILITAR 10/10", "music": "Volatile Reaction.mp3", "category": "HISTORIA & BATALLAS ANTIGUAS"}
]

def load_fonts():
    font_path_bold = "C:\\Windows\\Fonts\\arialbd.ttf"
    font_path_reg = "C:\\Windows\\Fonts\\arial.ttf"
    if not os.path.exists(font_path_bold):
        font_path_bold = "C:\\Windows\\Fonts\\dejavusans-bold.ttf"
    if not os.path.exists(font_path_reg):
        font_path_reg = "C:\\Windows\\Fonts\\dejavusans.ttf"
        
    return {
        "title": ImageFont.truetype(font_path_bold, 54),
        "category": ImageFont.truetype(font_path_bold, 32),
        "badge": ImageFont.truetype(font_path_bold, 28),
        "caption": ImageFont.truetype(font_path_bold, 52)
    }

FONTS = load_fonts()

def render_short_video(cfg):
    item_id = cfg["id"]
    mp3_voice = os.path.join(AUDIO_DIR, f"{item_id}.mp3")
    vtt_sub = os.path.join(AUDIO_DIR, f"{item_id}.vtt")
    bg_music = os.path.join(MUSIC_DIR, cfg["music"])
    output_mp4 = os.path.join(OUTPUT_DIR, f"{item_id}.mp4")
    
    if not os.path.exists(mp3_voice):
        print(f"  [SKIP] Voice file missing for {item_id}")
        return False
        
    duration = get_audio_duration(mp3_voice)
    if not duration:
        print(f"  [SKIP] Could not probe audio duration for {item_id}")
        return False
        
    cues = parse_vtt_subtitles(vtt_sub)
    
    # 1. Create mixed audio (Voice + Background Music at -24dB)
    mixed_audio = os.path.join(AUDIO_DIR, f"{item_id}_mixed.wav")
    
    if os.path.exists(bg_music):
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", mp3_voice,
            "-stream_loop", "-1", "-i", bg_music,
            "-filter_complex", "[1:a]volume=0.06[music];[0:a][music]amix=inputs=2:duration=first[aout]",
            "-map", "[aout]",
            "-ac", "2", "-ar", "44100",
            mixed_audio
        ]
    else:
        cmd_audio = [
            "ffmpeg", "-y",
            "-i", mp3_voice,
            "-ac", "2", "-ar", "44100",
            mixed_audio
        ]
        
    subprocess.run(cmd_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # 2. Render Video Frames
    temp_frames_dir = os.path.join(BASE_DIR, f"temp_frames_{item_id}")
    if os.path.exists(temp_frames_dir):
        shutil.rmtree(temp_frames_dir)
    os.makedirs(temp_frames_dir, exist_ok=True)
    
    fps = 30
    total_frames = int(duration * fps)
    width, height = 1080, 1920
    
    # Simple aesthetic canvas
    bg_color_top = (12, 18, 34)
    bg_color_bot = (5, 8, 16)
    
    for f_idx in range(total_frames):
        t_sec = f_idx / fps
        prog = f_idx / max(1, total_frames - 1)
        
        # Base frame
        img = Image.new("RGBA", (width, height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(img)
        
        # Gradient background
        for y in range(height):
            ratio = y / height
            r = int(bg_color_top[0] * (1 - ratio) + bg_color_bot[0] * ratio)
            g = int(bg_color_top[1] * (1 - ratio) + bg_color_bot[1] * ratio)
            b = int(bg_color_top[2] * (1 - ratio) + bg_color_bot[2] * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b, 255))
            
        # Top banner
        header_y = 140
        draw.text((width // 2, header_y), cfg["category"], font=FONTS["category"], fill=(56, 189, 248, 255), anchor="mm")
        draw.text((width // 2, header_y + 65), cfg["title"], font=FONTS["title"], fill=(255, 255, 255, 255), anchor="mm")
        
        # Floating badge
        badge_y = header_y + 135
        badge_w, badge_h = 420, 60
        badge_x = (width - badge_w) // 2
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(15, 23, 42, 220), outline=(250, 200, 21, 230), width=3)
        draw.text((width // 2, badge_y + badge_h // 2), cfg["badge"], font=FONTS["badge"], fill=(255, 255, 255, 255), anchor="mm")
        
        # Center Illustration Panel
        panel_w, panel_h = 920, 840
        panel_x = (width - panel_w) // 2
        panel_y = 480
        bob = int(12 * math.sin(2 * math.pi * f_idx / 60))
        panel_y += bob
        
        draw.rounded_rectangle([panel_x, panel_y, panel_x + panel_w, panel_y + panel_h], radius=24, fill=(20, 30, 55, 180), outline=(56, 189, 248, 160), width=3)
        
        # Active caption text
        current_cue = None
        for c in cues:
            if c["start"] <= t_sec <= c["end"]:
                current_cue = c["text"]
                break
                
        if current_cue:
            caption_y = 1520
            # Draw tri-tone highlighted caption
            draw.text((width // 2, caption_y), current_cue, font=FONTS["caption"], fill=(250, 200, 21, 255), anchor="mm")
            
        frame_file = os.path.join(temp_frames_dir, f"frame_{f_idx:05d}.jpg")
        img.convert("RGB").save(frame_file, quality=90)
        
    # 3. Assemble MP4 with FFmpeg
    cmd_mp4 = [
        "ffmpeg", "-y",
        "-r", str(fps),
        "-i", os.path.join(temp_frames_dir, "frame_%05d.jpg"),
        "-i", mixed_audio,
        "-c:v", "libx264", "-preset", "fast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_mp4
    ]
    
    subprocess.run(cmd_mp4, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # Cleanup temp frames & mixed audio
    shutil.rmtree(temp_frames_dir)
    if os.path.exists(mixed_audio):
        os.remove(mixed_audio)
        
    file_size_mb = os.path.getsize(output_mp4) / (1024 * 1024)
    print(f"  [SUCCESS] RENDERED: {os.path.basename(output_mp4)} ({duration:.1f}s, {file_size_mb:.2f} MB)")
    return True

def main():
    print("=" * 80)
    print("  KINESIO & VAREGO MASTER MP4 RENDER SUITE")
    print("  Rendering 23 Vertical Shorts (1080x1920)")
    print("=" * 80)
    
    success_count = 0
    for idx, cfg in enumerate(RENDER_CONFIGS, 1):
        print(f"\n[{idx:02d}/23] Rendering Short '{cfg['id']}'...")
        res = render_short_video(cfg)
        if res:
            success_count += 1
            
    print("\n" + "=" * 80)
    print(f"  FINAL SUMMARY: {success_count} / {len(RENDER_CONFIGS)} MP4 Videos Rendered Successfully!")
    print(f"  Output Directory: {OUTPUT_DIR}")
    print("=" * 80)

if __name__ == "__main__":
    main()
