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
POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

SHORTS_DATA = {
    "siberia_short_1": {
        "title": "¿Cuánto vale un soldado? 🇷🇺💸",
        "badge": "SIBERIA ❄",
        "music": "Moorland.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_0",
        "short_num": 1
    },
    "siberia_short_2": {
        "title": "El negocio de los Grobovye ⚰",
        "badge": "NEGOCIO 💸",
        "music": "Sneaky Snitch.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_1",
        "short_num": 2
    },
    "siberia_short_3": {
        "title": "La subasta regional ⚔",
        "badge": "SUBASTA 🏛",
        "music": "Clash Defiant.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_2",
        "short_num": 3
    },
    "siberia_short_4": {
        "title": "Contratos a -40 grados ❄",
        "badge": "YAKUTIA 🏔",
        "music": "Moorland.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_3",
        "short_num": 4
    },
    "siberia_short_5": {
        "title": "Entrenamiento express ☠",
        "badge": "TRINCHERA ⚔",
        "music": "Volatile Reaction.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_4",
        "short_num": 5
    },
    "siberia_short_6": {
        "title": "Presos al frente ⛓",
        "badge": "AMNISTÍA ⚖",
        "music": "Sneaky Snitch.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_5",
        "short_num": 6
    },
    "siberia_short_7": {
        "title": "La gran mentira de Moscú 🏙",
        "badge": "DESIGUALDAD ⚖",
        "music": "Clash Defiant.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_6",
        "short_num": 7
    },
    "siberia_short_8": {
        "title": "Billones para la guerra 💳",
        "badge": "PRESUPUESTO 💰",
        "music": "Sneaky Snitch.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_7",
        "short_num": 8
    },
    "siberia_short_9": {
        "title": "De civil a combatiente 🌲",
        "badge": "TRINCHERA ⚔",
        "music": "Volatile Reaction.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_8",
        "short_num": 9
    },
    "siberia_short_10": {
        "title": "La deuda familiar 🏠",
        "badge": "MOTOR ECONÓMICO 💰",
        "music": "Moorland.mp3",
        "bg_screenshot": "gates_of_hell_screenshot_9",
        "short_num": 10
    },
    "siberia_short_11": {
        "title": "¿Y si el dinero se acaba? 📉",
        "badge": "FUTURO SOCIAL 👥",
        "music": "Moorland.mp3",
        "bg_screenshot": "iron_harvest_screenshot_0",
        "short_num": 11
    },
    "siberia_short_12": {
        "title": "Inflación y bonos 💵",
        "badge": "INFLACIÓN 📈",
        "music": "Sneaky Snitch.mp3",
        "bg_screenshot": "iron_harvest_screenshot_1",
        "short_num": 12
    },
    "siberia_short_13": {
        "title": "Minorías étnicas 👥",
        "badge": "DEMOGRAFÍA 👥",
        "music": "Moorland.mp3",
        "bg_screenshot": "iron_harvest_screenshot_2",
        "short_num": 13
    },
    "siberia_short_14": {
        "title": "Las bajas invisibles 📊",
        "badge": "CENSURA 🤫",
        "music": "Moorland.mp3",
        "bg_screenshot": "iron_harvest_screenshot_3",
        "short_num": 14
    },
    "siberia_short_15": {
        "title": "El decouple ruso 🪐",
        "badge": "FINANZAS 🌍",
        "music": "Cipher2.mp3",
        "bg_screenshot": "iron_harvest_screenshot_4",
        "short_num": 15
    }
}

from kinesio_core import get_audio_duration, get_ken_burns_crop

def extract_short_text(file_path, short_num):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = content.split('## 📱 PARTE 2: GUIONES DE SHORTS VERTICALES (9:16)')
    if len(parts) < 2:
        return ""
    shorts_block = parts[1]
    
    sh_key = f"### 📱 Short {short_num}:"
    if sh_key not in shorts_block:
        return ""
        
    sh_part = shorts_block.split(sh_key)[1]
    if short_num < 15:
        sh_part = sh_part.split(f"### 📱 Short {short_num+1}:")[0]
    else:
        sh_part = sh_part.split('---')[0]
        
    lines = sh_part.split('\n')
    for i, line in enumerate(lines):
        if "Audio (Voz en off)" in line:
            for j in range(i+1, min(i+5, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('"') and next_line.endswith('"'):
                    return next_line[1:-1].strip()
                    
    return ""

def draw_vertical_short_frame(draw, width, height, title, badge, active_words, font_title, font_sub, font_badge, font_act, font_side, sharp_bg_img, progress, vignette_img=None, effect_type="zoom_in"):
    if sharp_bg_img:
        img_bg = get_ken_burns_crop(sharp_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
        
    # Apply pre-rendered vignette overlay
    if vignette_img:
        img_bg = Image.alpha_composite(img_bg, vignette_img)
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # 1. Floating card float
    float_offset = int(math.sin(progress * math.pi * 2.0) * 6.0)
    
    # 2. Draw Top Card Info Panel
    card_w = 900
    card_h = 240
    card_left = (width - card_w) // 2
    card_top = 120 + float_offset
    card_right = card_left + card_w
    card_bottom = card_top + card_h
    
    # Double Neon Border Card (Cyan border)
    draw_img.rounded_rectangle([card_left, card_top, card_right, card_bottom], radius=24, fill=(12, 20, 38, 160), outline=(56, 189, 248, 50), width=2)
    draw_img.rounded_rectangle([card_left - 3, card_top - 3, card_right + 3, card_bottom + 3], radius=27, fill=(0, 0, 0, 0), outline=(56, 189, 248, 15), width=2)
    
    # Top Card Text
    draw_img.text((width // 2, card_top + 60), badge, font=font_badge, fill=(56, 189, 248, 255), anchor="mm")
    draw_img.text((width // 2, card_top + 140), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    # 3. Progressive Subtitles Caption Box
    prev_w, active_w, next_w = active_words
    cap_y = height // 2 + 100
    
    # Clean brackets/punctuation
    active_clean = re.sub(r'[^\wáéíóúÁÉÍÓÚñÑ]', '', active_w).upper()
    prev_clean = prev_w.lower()
    next_clean = next_w.lower()
    
    # Side words size limit
    if len(prev_clean) > 10: prev_clean = prev_clean[:9] + "..."
    if len(next_clean) > 10: next_clean = next_clean[:9] + "..."
    
    # Draw Background pill for active word
    act_w = draw_img.textlength(active_clean, font=font_act)
    pill_padding_x = 40
    pill_padding_y = 25
    pill_left = width // 2 - act_w // 2 - pill_padding_x
    pill_top = cap_y - pill_padding_y
    pill_right = width // 2 + act_w // 2 + pill_padding_x
    pill_bottom = cap_y + font_act.size + pill_padding_y
    
    # Draw double neon glowing capsule border
    draw_img.rounded_rectangle([pill_left, pill_top, pill_right, pill_bottom], radius=16, fill=(12, 20, 38, 190), outline=(56, 189, 248, 120), width=3)
    
    # Write words
    draw_img.text((width // 2, cap_y), active_clean, font=font_act, fill=(255, 255, 255, 255), anchor="mt")
    
    if prev_clean:
        draw_img.text((width // 2 - act_w // 2 - 120, cap_y + 15), prev_clean, font=font_side, fill=(160, 180, 200, 140), anchor="rm")
    if next_clean:
        draw_img.text((width // 2 + act_w // 2 + 120, cap_y + 15), next_clean, font=font_side, fill=(160, 180, 200, 140), anchor="lm")
        
    # 4. Progress bar at the bottom
    bar_padding = 80
    bar_w = width - bar_padding * 2
    bar_y = height - 140
    draw_img.line([bar_padding, bar_y, width - bar_padding, bar_y], fill=(255, 255, 255, 20), width=6)
    draw_img.line([bar_padding, bar_y, bar_padding + int(bar_w * progress), bar_y], fill=(56, 189, 248, 220), width=6)
    
    return img_bg

def compile_shorts():
    script_path = os.path.join(BASE_DIR, "scripts_siberia_campaign.md")
    
    print("\n====================================================")
    print("DOMINUSBABEL SIBERIA VERTICAL SHORTS COMPILER")
    print("====================================================\n")
    
    width, height = 1080, 1920
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 46)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 32)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 30)
    
    font_caption_active = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 64)
    font_caption_side = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 36)
    
    # Pre-render static vignette overlay to save massive CPU cycles in inner loops
    print("Pre-rendering static vignette overlay...")
    vignette_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette_img)
    for r in range(0, int(height * 0.75), 20):
        alpha = int((r / (height * 0.75)) ** 1.8 * 210)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(6, 10, 20, alpha), width=22)
    
    for idx, (key, info) in enumerate(SHORTS_DATA.items()):
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
            
        script_text = extract_short_text(script_path, info["short_num"])
        words = script_text.split()
        total_words = len(words)
        if total_words == 0:
            print(f"  [ERROR] Failed to extract script for Short {info['short_num']}. Skipping.")
            continue
            
        bg_path = os.path.join(SCREENSHOTS_DIR, f"{info['bg_screenshot']}.jpg")
        base_img = Image.open(bg_path) if os.path.exists(bg_path) else None
        
        sharp_bg_img = None
        if base_img:
            bg_scale = 1.4
            bg_w = int(width * bg_scale)
            bg_h = int(height * bg_scale)
            sharp_bg_img = base_img.resize((bg_w, bg_h)).convert("RGBA")
            base_img.close()
            
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
        os.makedirs(temp_dir, exist_ok=True)
        total_frames = int(audio_dur * 30)
        
        # Camera motions rotation
        kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
        effect_type = kb_effects[idx % len(kb_effects)]
        
        t0 = time.time()
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
                info["title"], info["badge"],
                (prev_w, active_w, next_w),
                font_title, font_sub, font_badge,
                font_caption_active, font_caption_side,
                sharp_bg_img, progress, vignette_img=vignette_img, effect_type=effect_type
            )
            frame_img.convert("RGB").save(os.path.join(temp_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
            frame_img.close()
            
        if sharp_bg_img:
            sharp_bg_img.close()
            
        fps_render = total_frames / (time.time() - t0)
        print(f"    Rendered {total_frames} frames in {time.time()-t0:.1f}s ({fps_render:.1f} FPS)")
        
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
        
        # Audio assembly with background music loop
        print(f"    Assembling audio with {info['music']}...")
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.0[speech];"
        
        bg_music_path = os.path.join(MUSIC_DIR, info["music"])
        use_bg = os.path.exists(bg_music_path)
        if use_bg:
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            # Music volume attenuated as per requirement (-22dB to -25dB)
            audio_mix_filter += "[2:a]volume=-24dB[bg_music];"
            
        # Optional: insert transition pop SFX at the start or end
        sfx_available = os.path.exists(POP_SFX)
        if sfx_available:
            p_idx = 3 if use_bg else 2
            audio_inputs.extend(["-i", POP_SFX])
            audio_mix_filter += f"[{p_idx}:a]volume=-6dB[sfx_pop];"
            
            if use_bg:
                audio_mix_filter += "[speech][bg_music][sfx_pop]amix=inputs=3:normalize=0[a]"
            else:
                audio_mix_filter += "[speech][sfx_pop]amix=inputs=2:normalize=0[a]"
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
            print(f"  [SUCCESS] Short compiled: {output_path}")
        else:
            print(f"  [FAILED] Compile failed for {key}")

if __name__ == "__main__":
    compile_shorts()
