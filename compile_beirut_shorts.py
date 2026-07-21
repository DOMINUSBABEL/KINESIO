import os
import sys
import re
import time
import shutil
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
MUSIC_DIR = os.path.join(BASE_DIR, "music")

SHORTS_DATA = {
    1: {"bg": "beirut_ref_1", "title": "El Barco Maldito Rhosus", "music": "Moorland.mp3"},
    2: {"bg": "beirut_ref_2", "title": "Bomba de Tiempo Hangar 12", "music": "Sneaky Snitch.mp3"},
    3: {"bg": "beirut_ref_3", "title": "Alertas Rojas Archivadas", "music": "Scheming Weasel.mp3"},
    4: {"bg": "beirut_ref_4", "title": "Pirotecnia y Nitrato Mezcla", "music": "Volatile Reaction.mp3"},
    5: {"bg": "beirut_ref_8", "title": "El Milagro Novia Beirut", "music": "Moorland.mp3"},
    6: {"bg": "beirut_ref_6", "title": "Nube Wilson Onda Expansiva", "music": "Cipher2.mp3"},
    7: {"bg": "beirut_ref_9", "title": "Silos Trigo Escudo Ciudad", "music": "Clash Defiant.mp3"},
    8: {"bg": "beirut_ref_7", "title": "Explosión No Nuclear Potente", "music": "Severe Tire Damage.mp3"},
    9: {"bg": "beirut_ref_8", "title": "Hospitales Ruinas Catástrofe", "music": "Moorland.mp3"},
    10: {"bg": "beirut_ref_9", "title": "Desastre Económico Puerto", "music": "Cipher2.mp3"},
    11: {"bg": "beirut_ref_10", "title": "Caída del Gobierno Ira", "music": "Clash Defiant.mp3"},
    12: {"bg": "beirut_ref_3", "title": "Cargamento Fantasma Nitrato", "music": "Sneaky Snitch.mp3"},
    13: {"bg": "beirut_ref_5", "title": "Bomberos Héroes Beirut", "music": "Moorland.mp3"},
    14: {"bg": "beirut_ref_10", "title": "Heridas Abiertas Impunidad", "music": "Moorland.mp3"}
}

from kinesio_core import get_audio_duration, get_ken_burns_crop

def parse_shorts_scripts(script_path):
    if not os.path.exists(script_path):
        return {}
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    shorts_text = {}
    parts = content.split('## 🎥 PARTE 2: GUIONES DE SHORTS VERTICALES (9:16)')
    if len(parts) >= 2:
        shorts_block = parts[1]
        for idx in range(1, 15):
            sh_key = f"### 📱 Short {idx}:"
            if sh_key in shorts_block:
                sh_part = shorts_block.split(sh_key)[1]
                if idx < 14:
                    sh_part = sh_part.split(f"### 📱 Short {idx+1}:")[0]
                lines = sh_part.split('\n')
                for i, line in enumerate(lines):
                    if "Audio (Voz en off)" in line:
                        for j in range(i+1, min(i+5, len(lines))):
                            next_line = lines[j].strip()
                            if next_line.startswith('"') and next_line.endswith('"'):
                                shorts_text[idx] = next_line[1:-1].strip()
                                break
    return shorts_text

def get_current_word_highlights(words, progress):
    num_words = len(words)
    current_idx = int(progress * num_words)
    current_idx = min(current_idx, num_words - 1)
    
    # Subtitle window of 4 words due to longer duration (34s-54s)
    window_size = 4
    start_idx = max(0, current_idx - (window_size // 2))
    end_idx = min(num_words, start_idx + window_size)
    if end_idx - start_idx < window_size and start_idx > 0:
        start_idx = max(0, end_idx - window_size)
        
    chunk = words[start_idx:end_idx]
    active_in_chunk = current_idx - start_idx
    return chunk, active_in_chunk

def draw_vertical_frame(width, height, words, title, font_sub, font_title, font_sub_bold, blurred_bg_img, progress, vignette_img=None, effect_type="zoom_in"):
    if blurred_bg_img:
        img_bg = get_ken_burns_crop(blurred_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
        
    if vignette_img:
        img_bg = Image.alpha_composite(img_bg, vignette_img)
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Brand Top Capsule
    brand_w = 900
    brand_h = 100
    brand_left = (width - brand_w) // 2
    brand_top = 100
    draw_img.rounded_rectangle([brand_left, brand_top, brand_left + brand_w, brand_top + brand_h], radius=18, fill=(12, 16, 26, 170), outline=(239, 68, 68, 80), width=2)
    draw_img.text((width // 2, brand_top + brand_h // 2), title.upper(), font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    # Subtitle Glass Panel
    box_w = 900
    box_h = 320
    box_left = (width - box_w) // 2
    box_top = height // 2 - 100
    box_right = box_left + box_w
    box_bottom = box_top + box_h
    
    # Floating sinoidal shift
    float_offset = int(math.sin(progress * math.pi * 2.0) * 6.0)
    box_top += float_offset
    box_bottom += float_offset
    
    draw_img.rounded_rectangle([box_left, box_top, box_right, box_bottom], radius=24, fill=(12, 16, 26, 150), outline=(239, 68, 68, 50), width=2)
    
    # Word Highlighting
    if words:
        chunk, active_in_chunk = get_current_word_highlights(words, progress)
        
        spacing = 30
        total_w = 0
        word_widths = []
        for idx, wd in enumerate(chunk):
            font = font_sub_bold if idx == active_in_chunk else font_sub
            w_size = draw_img.textlength(wd, font=font)
            word_widths.append(w_size)
            total_w += w_size
        total_w += spacing * (len(chunk) - 1)
        
        start_x = (width - total_w) // 2
        curr_x = start_x
        for idx, wd in enumerate(chunk):
            is_active = idx == active_in_chunk
            font = font_sub_bold if is_active else font_sub
            color = (250, 204, 21, 255) if is_active else (255, 255, 255, 140) # Bright yellow/gold for active word
            
            outline_color = (0, 0, 0, 255)
            y_pos = (box_top + box_bottom) // 2
            
            # Thick black outline for subtitle readability
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (-3, 0), (3, 0), (0, -3), (0, 3)]:
                draw_img.text((curr_x + dx, y_pos + dy), wd, font=font, fill=outline_color, anchor="lm")
                
            draw_img.text((curr_x, y_pos), wd, font=font, fill=color, anchor="lm")
            curr_x += word_widths[idx] + spacing
            
    # Progress Bar at bottom
    bar_w = 900
    bar_x = (width - bar_w) // 2
    bar_y = height - 150
    draw_img.line([bar_x, bar_y, bar_x + bar_w, bar_y], fill=(255, 255, 255, 15), width=8)
    draw_img.line([bar_x, bar_y, bar_x + int(bar_w * progress), bar_y], fill=(239, 68, 68, 220), width=8)
    
    return img_bg

def compile_shorts():
    script_path = os.path.join(BASE_DIR, "scripts_beirut_campaign.md")
    shorts_text = parse_shorts_scripts(script_path)
    
    print("\n====================================================")
    print("DOMINUSBABEL BEIRUT VERTICAL SHORTS COMPILER")
    print("====================================================\n")
    
    width, height = 1080, 1920
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 46)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 48)
    font_sub_bold = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    
    # Pre-render vertical vignette overlay once
    vignette_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette_img)
    for r in range(0, int(height * 0.7), 15):
        alpha = int((r / (height * 0.7)) ** 2.2 * 175)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(6, 8, 16, alpha), width=16)
        
    for idx in range(1, 15):
        key = f"beirut_short_{idx}"
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Short '{key}' already exists on disk. Skipping.")
            continue
            
        print(f"Compiling Short: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio missing for {key}. Skipping.")
            continue
            
        sh_info = SHORTS_DATA.get(idx, {})
        txt = shorts_text.get(idx, "")
        words = txt.split() if txt else []
        
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
        os.makedirs(temp_dir, exist_ok=True)
        
        # Load background image dynamically
        base_img = None
        fpath_jpg = os.path.join(SCREENSHOTS_DIR, f"{sh_info['bg']}.jpg")
        if os.path.exists(fpath_jpg):
            try:
                base_img = Image.open(fpath_jpg)
            except Exception as e:
                print(f"    Failed loading {sh_info['bg']}.jpg: {e}")
                
        blurred_bg_img = None
        if base_img:
            blurred_bg_img = base_img.convert("RGBA").filter(ImageFilter.GaussianBlur(16))
            overlay = Image.new("RGBA", base_img.size, (6, 8, 16, 150))
            blurred_bg_img = Image.alpha_composite(blurred_bg_img, overlay)
            base_img.close()
            
        total_frames = int(audio_dur * 30)
        
        # Rotate camera motions
        kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
        effect_type = kb_effects[idx % len(kb_effects)]
        
        t0 = time.time()
        for f_idx in range(total_frames):
            progress = f_idx / total_frames
            frame_img = draw_vertical_frame(
                width, height, words, sh_info.get("title", f"Short {idx}"),
                font_sub, font_title, font_sub_bold,
                blurred_bg_img, progress, vignette_img=vignette_img, effect_type=effect_type
            )
            frame_img.convert("RGB").save(os.path.join(temp_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
            frame_img.close()
            
        if blurred_bg_img:
            blurred_bg_img.close()
            
        fps_render = total_frames / (time.time() - t0)
        print(f"    Rendered {total_frames} frames in {time.time()-t0:.1f}s ({fps_render:.1f} FPS)")
        
        # Compile raw video segment
        raw_video = os.path.join(temp_dir, "raw_video.mp4")
        cmd_frames = [
            "ffmpeg", "-y",
            "-framerate", "30",
            "-i", os.path.join(temp_dir, "frame_%05d.jpg"),
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-t", f"{audio_dur:.2f}",
            raw_video
        ]
        subprocess.run(cmd_frames, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Mix vocals and background music
        bg_music_path = os.path.join(MUSIC_DIR, sh_info["music"])
        use_bg = os.path.exists(bg_music_path)
        
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.0[speech];"
        
        if use_bg:
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            audio_mix_filter += f"[2:a]volume=-24dB[bg_music];[speech][bg_music]amix=inputs=2:normalize=0[a]"
        else:
            audio_mix_filter += "[speech]anull[a]"
            
        cmd_final = ["ffmpeg", "-y"]
        cmd_final.extend(audio_inputs)
        cmd_final.extend([
            "-filter_complex", audio_mix_filter,
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ])
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Short compiled: {output_path}")
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
        else:
            print(f"  [ERROR] Final assembly failed for {key}")

if __name__ == "__main__":
    compile_shorts()
