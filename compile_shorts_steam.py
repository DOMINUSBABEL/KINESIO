import os
import sys
import re
import time
import shutil
import subprocess
import wave
import math
import struct
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
MUSIC_DIR = os.path.join(BASE_DIR, "music")

POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

SHORTS_DATA = {
    "steam_short_1": {"title": "EL MONOPOLIO QUE AMAMOS", "badge": "HEGEMONÍA 🌐", "bg_idx": 0},
    "steam_short_2": {"title": "EL IMPUESTO DE VALVE", "badge": "COMISIONES 💸", "bg_idx": 1},
    "steam_short_3": {"title": "LA PARIDAD DE PRECIOS", "badge": "CONTRATOS ⚖", "bg_idx": 2},
    "steam_short_4": {"title": "LOS CORREOS REVELADOS", "badge": "CONSPIRACIÓN 💼", "bg_idx": 3},
    "steam_short_5": {"title": "SOPORTE RADICAL", "badge": "EXCELENCIA 🔄", "bg_idx": 4},
    "steam_short_6": {"title": "EL PODER DE VALVE", "badge": "PRIVADA 👑", "bg_idx": 5}
}

from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_outlined_text

def clean_word_for_display(word):
    cleaned = re.sub(r'^[¿"\'\(]+|[?"\'\),\.]+$', '', word)
    return cleaned.upper()

def draw_rotated_outlined_text(img, position, text, font, text_color, outline_color, thickness, angle):
    text_w = 700
    text_h = 250
    text_img = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    w, h = text_w // 2, text_h // 2
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx*dx + dy*dy <= thickness*thickness:
                text_draw.text((w + dx, h + dy), text, font=font, fill=outline_color, anchor="mm")
    text_draw.text((w, h), text, font=font, fill=text_color, anchor="mm")
    rotated_img = text_img.rotate(angle, resample=Image.BICUBIC, expand=True)
    rx, ry = rotated_img.size
    px = position[0] - rx // 2
    py = position[1] - ry // 2
    img.paste(rotated_img, (px, py), mask=rotated_img)

def draw_vertical_short_frame(draw, width, height, title, badge, current_words, font_title, font_sub, font_badge, font_caption_active, font_caption_side, base_img, progress, effect_type="zoom_in", frame_idx=0):
    if base_img:
        img_bg = get_ken_burns_crop(base_img, width, height, progress, effect_type)
        img_bg = img_bg.filter(ImageFilter.GaussianBlur(12))
        overlay = Image.new("RGBA", (width, height), (8, 12, 24, 130))
        img_bg = Image.alpha_composite(img_bg, overlay)
    else:
        img_bg = Image.new("RGBA", (width, height), (13, 20, 38, 255))
        
    draw_img = ImageDraw.Draw(img_bg)
    for y in range(1200, 1920):
        alpha = int((y - 1200) / 720 * 180)
        draw_img.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
    for y in range(0, 300):
        alpha = int((300 - y) / 300 * 140)
        draw_img.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

    header_y = 120
    draw_img.text((width // 2, header_y), "VALVE Y LA GUERRA CONTRA STEAM", font=font_sub, fill=(56, 189, 248, 255), anchor="mm")
    draw_img.text((width // 2, header_y + 60), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    if badge:
        badge_y = header_y + 130
        badge_w = 340
        badge_h = 55
        badge_x = (width - badge_w) // 2
        draw_img.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=10, fill=(10, 18, 36, 150), outline=(56, 189, 248, 200), width=2)
        draw_img.text((width // 2, badge_y + badge_h // 2), badge.upper(), font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
    bob_offset = int(15 * math.sin(2 * math.pi * frame_idx / 60))
    card_w = 900
    card_h = 800
    card_x = (width - card_w) // 2
    card_y = 480 + bob_offset
    
    c_shadow = Image.new("L", (card_w + 30, card_h + 30), 0)
    ImageDraw.Draw(c_shadow).rounded_rectangle([12, 12, card_w + 12, card_h + 12], radius=20, fill=160)
    c_blur = c_shadow.filter(ImageFilter.GaussianBlur(12))
    img_bg.paste(Image.new("RGBA", (card_w + 30, card_h + 30), (0, 0, 0, 180)), (card_x - 12, card_y - 12), mask=c_blur)
    
    draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=20, fill=(10, 18, 36, 100), outline=(56, 189, 248, 255), width=3)
    
    if base_img:
        bw, bh = base_img.size
        cx, cy = bw // 2, bh // 2
        illustration_crop = base_img.crop((cx - 440, cy - 390, cx + 440, cy + 390))
        mask = Image.new("L", (880, 780), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 880, 780], radius=16, fill=255)
        img_bg.paste(illustration_crop, (card_x + 10, card_y + 10), mask=mask)
        
    prev_w, active_w, next_w = current_words
    text_y_center = 1550
    
    if active_w:
        tilt_angle = 4 if len(active_w) % 2 == 0 else -4
        draw_rotated_outlined_text(img_bg, (width // 2, text_y_center), clean_word_for_display(active_w), font_caption_active, text_color=(253, 224, 71, 255), outline_color=(0, 0, 0, 255), thickness=6, angle=tilt_angle)
        
    if prev_w:
        draw_outlined_text(draw_img, (width // 2 - 280, text_y_center + 10), clean_word_for_display(prev_w), font_caption_side, text_color=(200, 200, 200, 200), outline_color=(0, 0, 0, 200), thickness=4)
        
    if next_w:
        draw_outlined_text(draw_img, (width // 2 + 280, text_y_center + 10), clean_word_for_display(next_w), font_caption_side, text_color=(200, 200, 200, 200), outline_color=(0, 0, 0, 200), thickness=4)
        
    progress_w = int(width * progress)
    draw_img.rectangle([0, height - 8, width, height], fill=(23, 28, 41, 255))
    draw_img.rectangle([0, height - 8, progress_w, height], fill=(56, 189, 248, 255))
    
    draw_img.text((width // 2, height - 50), "@dominus8735", font=font_badge, fill=(255, 255, 255, 80), anchor="mm")
    
    return img_bg.convert("RGB")

def extract_short_text(file_path, key):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split(f"## 📌 {key}:")
    if len(parts) < 2:
        return ""
    block = parts[1].strip()
    lines = block.split('\n')
    for i, line in enumerate(lines):
        if "Voz en off" in line:
            for j in range(i+1, min(i+5, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('"') and next_line.endswith('"'):
                    return next_line[1:-1].strip()
    return ""

def compile_steam_shorts():
    script_path = os.path.join(BASE_DIR, "scripts_shorts_steam.md")
    
    print("\n====================================================")
    print("KINESIO SHORTS COMPILER: STEAM WAR SERIES")
    print("====================================================\n")
    
    width, height = 1080, 1920
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 26)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 22)
    font_caption_active = ImageFont.truetype("C:\\Windows\\Fonts\\impact.ttf", 82)
    font_caption_side = ImageFont.truetype("C:\\Windows\\Fonts\\impact.ttf", 54)
    
    for idx, (key, info) in enumerate(SHORTS_DATA.items()):
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Short '{key}' already exists. Skipping.")
            continue
            
        print(f"Compiling Short: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio missing for {key}. Skipping.")
            continue
            
        script_text = extract_short_text(script_path, key)
        words = script_text.split()
        total_words = len(words)
        
        bg_path = os.path.join(SCREENSHOTS_DIR, f"steam_screenshot_{info['bg_idx']}.jpg")
        base_img = Image.open(bg_path) if os.path.exists(bg_path) else None
        
        sharp_bg_img = None
        if base_img:
            bg_scale = 1.25
            bg_w = int(width * bg_scale)
            bg_h = int(height * bg_scale)
            sharp_bg_img = base_img.resize((bg_w, bg_h)).convert("RGBA")
            
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        total_frames = int(audio_dur * 30)
        
        t0 = time.time()
        kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
        effect_type = kb_effects[idx % len(kb_effects)]
        
        for f_idx in range(total_frames):
            progress = f_idx / total_frames
            curr_time = f_idx / 30.0
            word_idx = int(curr_time * (total_words / audio_dur))
            word_idx = min(word_idx, total_words - 1)
            prev_w = words[word_idx - 1] if word_idx > 0 else ""
            active_w = words[word_idx]
            next_w = words[word_idx + 1] if word_idx < total_words - 1 else ""
            
            frame_img = draw_vertical_short_frame(
                None, width, height,
                SHORTS_DATA[key]["title"], SHORTS_DATA[key]["badge"],
                (prev_w, active_w, next_w),
                font_title, font_sub, font_badge,
                font_caption_active, font_caption_side,
                sharp_bg_img, progress, effect_type=effect_type,
                frame_idx=f_idx
            )
            frame_img.save(os.path.join(temp_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
            
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
        
        pause_times = [0.0]
        for w_idx in range(1, len(words)):
            w = words[w_idx - 1]
            if w.endswith('.') or w.endswith(',') or w.endswith('?') or w.endswith('!'):
                p_time = w_idx * (audio_dur / total_words)
                pause_times.append(p_time)
        pop_times = [t for t in pause_times if t > 0.1][:12]
        
        bg_music_path = os.path.join(MUSIC_DIR, "Cipher2.mp3")
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.2[speech];"
        
        use_bg = os.path.exists(bg_music_path)
        if use_bg:
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            audio_mix_filter += "[2:a]volume=-24dB[bg_music];"
            
        use_sfx = os.path.exists(WHOOSH_SFX) and os.path.exists(POP_SFX)
        if use_sfx:
            audio_inputs.extend(["-i", WHOOSH_SFX, "-i", POP_SFX])
            audio_mix_filter += "[3:a]volume=-8dB,adelay=0|0[whoosh_delayed];"
            num_pops = len(pop_times)
            if num_pops > 0:
                audio_mix_filter += f"[4:a]asplit={num_pops}" + "".join(f"[p{i}]" for i in range(num_pops)) + ";"
                for i, t in enumerate(pop_times):
                    delay_ms = int(t * 1000)
                    audio_mix_filter += f"[p{i}]volume=-10dB,adelay={delay_ms}|{delay_ms}[pd{i}];"
            mix_inputs = ["[speech]"]
            if use_bg:
                mix_inputs.append("[bg_music]")
            mix_inputs.append("[whoosh_delayed]")
            for i in range(num_pops):
                mix_inputs.append(f"[pd{i}]")
            audio_mix_filter += "".join(mix_inputs) + f"amix=inputs={len(mix_inputs)}:normalize=0[a]"
        else:
            if use_bg:
                audio_mix_filter += "[speech][bg_music]amix=inputs=2:normalize=0[a]"
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
        
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
            
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Short generated: {output_path}")
        else:
            print(f"  [FAILED] Compile failed for {key}")

if __name__ == "__main__":
    compile_steam_shorts()
