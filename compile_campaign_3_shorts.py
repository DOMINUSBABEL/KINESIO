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

SHORTS_DATA = {}

# Build metadata for all 20 shorts
short_titles_c3 = [
    # Essay 1 Shorts
    "El Mito de la Música en Combate 🔇",
    "¿Siempre Ves a Tu Enemigo? 👁",
    "El Rango No Equivale a Competencia 🎖",
    "¿Disparan Todo el Tiempo? 🎒",
    "La Guerra No Siempre es Ruidosa 🔇",
    "La Mentira del Control Absoluto 🗺",
    "¿Sientes Cuando te Disparan? 💉",
    "La Memoria Bajo Fuego se Rompe 🧠",
    "Las Milicias Locales No Sirven 🛡",
    "El Soldado Occidental es Superior 🌴",
    # Essay 2 Shorts
    "Distinguiendo al Enemigo Real 👥",
    "Los Drones No Son Indestructibles 🛸",
    "Los Pilotos de Drones Están a Salvo 🎯",
    "Los Drones FPV No Reemplazan Todo 🔋",
    "El Trauma No es Igual para Todos 🧠",
    "El Mito del Soldado Rudo 🎖",
    "La Guerra No Tiene Lógica ⚖",
    "Las Granadas No Causan Bolas de Fuego 💥",
    "El Chaleco Antibalas No Te Hace Inmune 🛡",
    "Los Silenciadores No Hacen el Arma Muda 🤫"
]

for idx in range(20):
    essay_num = 1 if idx < 10 else 2
    short_num = (idx % 10) + 1
    key = f"war_myths_essay_{essay_num}_short_{short_num}"
    
    SHORTS_DATA[key] = {
        "title": short_titles_c3[idx],
        "badge": "MITO MILITAR ⚔",
        "music": "Clash Defiant.mp3",
        "bg_idx": idx % 10,
        "bg_prefix": "gates_of_hell_screenshot_"
    }

from kinesio_core import get_audio_duration, get_ken_burns_crop

def extract_short_text(file_path, key):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split(f"### {key}")
    if len(parts) < 2:
        return ""
    block = parts[1].strip()
    subparts = block.split("---")
    text = subparts[0].strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    return text

def draw_vertical_short_frame(draw, width, height, title, badge, active_words, font_title, font_sub, font_badge, font_act, font_side, sharp_bg_img, progress, effect_type="zoom_in"):
    if sharp_bg_img:
        img_bg = get_ken_burns_crop(sharp_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Dark Vignette Overlay
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for r in range(0, int(height * 0.75), 20):
        alpha = int((r / (height * 0.75)) ** 1.8 * 210)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(6, 10, 20, alpha), width=22)
    img_bg = Image.alpha_composite(img_bg, vignette)
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
    
    # Double Neon Border Card
    draw_img.rounded_rectangle([card_left, card_top, card_right, card_bottom], radius=24, fill=(10, 18, 36, 160), outline=(56, 189, 248, 45), width=2)
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
    draw_img.rounded_rectangle([pill_left, pill_top, pill_right, pill_bottom], radius=16, fill=(10, 18, 36, 190), outline=(56, 189, 248, 120), width=3)
    
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
    script_path = os.path.join(BASE_DIR, "scripts_war_myths.md")
    
    print("\n====================================================")
    print("CAMPAIGN 3 SHORTS COMPILER (20 SHORTS)")
    print("====================================================\n")
    
    width, height = 1080, 1920
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 46)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 32)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 30)
    
    font_caption_active = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 64)
    font_caption_side = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 36)
    
    for idx, (key, info) in enumerate(SHORTS_DATA.items()):
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Short '{key}' already exists on disk. Skipping.")
            continue
            
        print(f"Compiling Campaign 3 Short: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio missing for {key}. Skipping.")
            continue
            
        script_text = extract_short_text(script_path, key)
        words = script_text.split()
        total_words = len(words)
        
        bg_path = os.path.join(SCREENSHOTS_DIR, f"{info['bg_prefix']}{info['bg_idx']}.jpg")
        base_img = Image.open(bg_path) if os.path.exists(bg_path) else None
        
        sharp_bg_img = None
        if base_img:
            bg_scale = 1.4
            bg_w = int(width * bg_scale)
            bg_h = int(height * bg_scale)
            sharp_bg_img = base_img.resize((bg_w, bg_h)).convert("RGBA")
            
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        total_frames = int(audio_dur * 30)
        
        # Rotated camera motions
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
                sharp_bg_img, progress, effect_type=effect_type
            )
            frame_img.convert("RGB").save(os.path.join(temp_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
            
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
        
        # Calculate clause/pause POP sfx times
        pause_times = [0.0]
        for w_idx in range(1, len(words)):
            w = words[w_idx - 1]
            if w.endswith('.') or w.endswith(',') or w.endswith('?') or w.endswith('!'):
                p_time = w_idx * (audio_dur / total_words)
                pause_times.append(p_time)
        pop_times = [t for t in pause_times if t > 0.1][:12]
        
        bg_music_path = os.path.join(MUSIC_DIR, info["music"])
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.2[speech];"
        
        use_bg = os.path.exists(bg_music_path)
        if use_bg:
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            audio_mix_filter += "[2:a]volume=-24dB[bg_music];"
            
        use_sfx = os.path.exists(WHOOSH_SFX) and os.path.exists(POP_SFX)
        if use_sfx:
            w_idx = 3 if use_bg else 2
            p_idx = 4 if use_bg else 3
            audio_inputs.extend(["-i", WHOOSH_SFX, "-i", POP_SFX])
            audio_mix_filter += f"[{w_idx}:a]volume=-8dB,adelay=0|0[whoosh_delayed];"
            
            num_pops = len(pop_times)
            if num_pops > 0:
                audio_mix_filter += f"[{p_idx}:a]asplit={num_pops}" + "".join(f"[p{i}]" for i in range(num_pops)) + ";"
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
    compile_shorts()
