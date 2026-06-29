import os
import sys
import json
import time
import shutil
import subprocess
import wave
import math
import struct
import re
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from kinesio_core import get_audio_duration, get_ken_burns_crop
def generate_sfx_waves():
    """Generates basic pop and whoosh wav files if they are missing."""
    if not os.path.exists(POP_SFX):
        obj = wave.open(POP_SFX, 'w')
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(44100)
        duration = 0.15
        num_samples = int(duration * 44100)
        for i in range(num_samples):
            t = i / 44100
            freq = 300 + 400 * (t / duration)
            vol = t / 0.01 if t < 0.01 else math.exp(-30 * (t - 0.01))
            val = int(math.sin(2 * math.pi * freq * t) * vol * 22000)
            data = struct.pack('<h', val)
            obj.writeframesraw(data)
        obj.close()
        
    if not os.path.exists(WHOOSH_SFX):
        obj = wave.open(WHOOSH_SFX, 'w')
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(44100)
        duration = 0.60
        num_samples = int(duration * 44100)
        for i in range(num_samples):
            t = i / 44100
            freq = 80 + 350 * math.sin(math.pi * (t / duration))
            vol = math.sin(math.pi * (t / duration))
            val = int(math.sin(2 * math.pi * freq * t) * vol * 18000)
            data = struct.pack('<h', val)
            obj.writeframesraw(data)
        obj.close()

def get_chapter_timestamps(script_path, total_duration):
    """Parses script.md to extract sections and dynamically computes timestamps based on word counts."""
    if not os.path.exists(script_path):
        return []
        
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    chapters = content.split("## 📌 Capítulo ")
    if len(chapters) < 2:
        return []
        
    sections = []
    total_words = 0
    
    for ch in chapters[1:]:
        lines = ch.split('\n')
        title_line = lines[0].strip()
        title = title_line.split(":")[-1].strip() if ":" in title_line else title_line
        
        # Clean title parentheses
        title = re.sub(r'\([^\)]+\)', '', title).strip()
        
        # Find voiceover block
        voc_text = ""
        for i, line in enumerate(lines):
            if "Audio (Voz en off)" in line:
                for j in range(i+1, min(i+5, len(lines))):
                    next_line = lines[j].strip()
                    if next_line.startswith('"') and next_line.endswith('"'):
                        voc_text = next_line[1:-1].strip()
                        break
        
        words_count = len(voc_text.split())
        total_words += words_count
        sections.append({"title": title, "words": words_count})
        
    boundaries = []
    current_time = 0.0
    for idx, sec in enumerate(sections):
        pct = sec["words"] / total_words if total_words > 0 else (1.0 / len(sections))
        duration = pct * total_duration
        boundaries.append((current_time, current_time + duration, sec["title"]))
        current_time += duration
        
    return boundaries

def draw_horizontal_frame(draw, width, height, title, subtitle, font_title, font_sub, screenshot_path_or_img, progress, meme_text=None, font_meme=None, effect_type="zoom_in"):
    # 1. Background image with dynamic Ken Burns crop
    img_src = None
    if screenshot_path_or_img:
        if isinstance(screenshot_path_or_img, str):
            if os.path.exists(screenshot_path_or_img):
                img_src = Image.open(screenshot_path_or_img)
        else:
            img_src = screenshot_path_or_img

    if img_src:
        img_bg_static = get_ken_burns_crop(img_src, width, height, progress, effect_type)
        img_bg_static = img_bg_static.filter(ImageFilter.GaussianBlur(18))
        overlay = Image.new("RGBA", (width, height), (8, 12, 24, 160))
        img_bg = Image.alpha_composite(img_bg_static.convert("RGBA"), overlay)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))

        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Subtle vignette border (darkened edges)
    draw_img.rectangle([0, 0, width, height], outline=(0, 0, 0, 120), width=50)
    
    # 2. Centered Glassmorphism Panel
    panel_w = 1280
    panel_h = 580
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + 30
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    # Draw drop shadow behind the panel (use cached blur)
    shadow_offset = 15
    if not hasattr(draw_horizontal_frame, "shadow_blur"):
        shadow_mask = Image.new("L", (panel_w + 40, panel_h + 40), 0)
        ImageDraw.Draw(shadow_mask).rounded_rectangle([15, 15, panel_w + 15, panel_h + 15], radius=30, fill=150)
        draw_horizontal_frame.shadow_blur = shadow_mask.filter(ImageFilter.GaussianBlur(20))
        draw_horizontal_frame.shadow_color = Image.new("RGBA", (panel_w + 40, panel_h + 40), (0, 0, 0, 220))
    img_bg.paste(draw_horizontal_frame.shadow_color, (panel_left - 15 + shadow_offset, panel_top - 15 + shadow_offset), mask=draw_horizontal_frame.shadow_blur)
    
    # Translucent glass panel
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(13, 20, 38, 210), outline=(255, 255, 255, 25), width=2)
    
    # 3. Dynamic Progress Ring/Bar integrated elegantly
    bar_w = 1100
    bar_x = (width - bar_w) // 2
    bar_y = panel_top + 160
    draw_img.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + 8], radius=4, fill=(30, 41, 59, 255))
    draw_img.rounded_rectangle([bar_x, bar_y, bar_x + int(bar_w * progress), bar_y + 8], radius=4, fill=(249, 115, 22, 255))
    
    # 4. Text Layout (Title, Section Indicator, Narrative Hook)
    draw_img.text((width // 2, panel_top + 80), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    # Section indicator
    draw_img.text((width // 2, bar_y + 50), subtitle, font=font_sub, fill=(249, 115, 22, 255), anchor="mm")
    
    # Core review points
    bullet_y = bar_y + 120
    bullets = [
        "✔   El Sandbox e Imperio de Calradia",
        "✔   Combate Direccional y Sistema de Físicas",
        "✔   Mods Infinitos y Comunidad Eterna"
    ]
    for b in bullets:
        draw_img.text((width // 2, bullet_y), b, font=font_sub, fill=(200, 210, 230, 255), anchor="mm")
        bullet_y += 65
        
    # Meme overlay popups: Styled as a clean floating cartoon sticker!
    if meme_text and font_meme:
        meme_width = 380
        meme_height = 100
        meme_x = width - 480
        meme_y = height - 240
        
        # Meme card drop shadow
        m_shadow = Image.new("L", (meme_width + 20, meme_height + 20), 0)
        ImageDraw.Draw(m_shadow).rounded_rectangle([5, 5, meme_width + 5, meme_height + 5], radius=16, fill=180)
        m_blur = m_shadow.filter(ImageFilter.GaussianBlur(8))
        m_shadow_color = Image.new("RGBA", (meme_width + 20, meme_height + 20), (0, 0, 0, 180))
        img_bg.paste(m_shadow_color, (meme_x - 5, meme_y - 5), mask=m_blur)
        
        # Meme sticker card
        draw_img.rounded_rectangle([meme_x, meme_y, meme_x + meme_width, meme_y + meme_height], radius=16, fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=3)
        draw_img.text((meme_x + meme_width // 2, meme_y + meme_height // 2), meme_text, font=font_meme, fill=(255, 255, 255, 255), anchor="mm")
        
    return img_bg.convert("RGB")

def compile_horizontal_video(appid, game_name, prefix, output_path, script_path, audio_path, custom_subtitle, bg_music_filename="Moorland.mp3"):
    print(f"\nCompiling Horizontal Video: {game_name}")
    audio_dur = get_audio_duration(audio_path)
    if audio_dur == 0.0:
        print(f"  [ERROR] Audio file missing or empty: {audio_path}")
        return
        
    boundaries = get_chapter_timestamps(script_path, audio_dur)
    temp_dir = os.path.join(BASE_DIR, f"temp_render_{prefix}")
    os.makedirs(temp_dir, exist_ok=True)
    
    width, height = 1920, 1080
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 60)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 36)
    font_meme = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 32)
    
    # Locate gameplay trailer
    trailer_file = os.path.join(TRAILERS_DIR, f"{prefix}_trailer.mp4")
    trailer_dur = get_audio_duration(trailer_file) if os.path.exists(trailer_file) else 0.0
    
    # Pre-load all 10 screenshots to avoid disk I/O in the loop and enable rotation!
    loaded_screenshots = []
    for i in range(10):
        ss_path = os.path.join(SCREENSHOTS_DIR, f"{prefix}_screenshot_{i}.jpg")
        if os.path.exists(ss_path):
            try:
                loaded_screenshots.append(Image.open(ss_path))
            except:
                pass
    if not loaded_screenshots:
        print(f"  [WARNING] No screenshots found for {prefix}, rendering will fall back to solid background.")
        
    segment_files = []
    
    # 7 Chapters (or whatever script has)
    for idx, (start, end, title) in enumerate(boundaries):
        dur = end - start
        seg_video = os.path.join(temp_dir, f"seg_{idx:02d}.mp4")
        
        if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
            print(f"  [INFO] Segment {idx} already exists. Skipping render.")
            segment_files.append(seg_video)
            continue
            
        # Decide if this chapter has gameplay overlay
        # Odd chapters have slides, Even chapters slice gameplay!
        if idx % 2 == 1 and trailer_dur > 10.0:
            # Slice gameplay from the trailer (looping to guarantee enough length)
            clip_start = (idx * 15.0) % trailer_dur
            gp_filters = [
                "scale=2200:-1,crop=w='in_w*(1-0.12*t/dur)':h='in_h*(1-0.12*t/dur)':x='(in_w-out_w)/2':y='(in_h-out_h)/2',scale=1920:1080", # Zoom In
                "scale=2200:-1,crop=w='in_w*(0.88+0.12*t/dur)':h='in_h*(0.88+0.12*t/dur)':x='(in_w-out_w)/2':y='(in_h-out_h)/2',scale=1920:1080", # Zoom Out
                "scale=2400:-1,crop=w='in_h*1.777':h='in_h':x='(in_w-out_w)*(t/dur)':y=0,scale=1920:1080", # Pan Left-to-Right
                "scale=2400:-1,crop=w='in_h*1.777':h='in_h':x='(in_w-out_w)*(1-t/dur)':y=0,scale=1920:1080" # Pan Right-to-Left
            ]
            gp_filter = gp_filters[idx % len(gp_filters)].replace("dur", f"{dur:.2f}")
            cmd_slice = [
                "ffmpeg", "-y",
                "-stream_loop", "-1",
                "-ss", f"{clip_start:.2f}",
                "-i", trailer_file,
                "-t", f"{dur:.2f}",
                "-vf", f"{gp_filter},force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
                seg_video
            ]
            subprocess.run(cmd_slice, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            # Render PIL slide
            frame_dir = os.path.join(temp_dir, f"frames_{idx}")
            os.makedirs(frame_dir, exist_ok=True)
            
            total_frames = int(dur * 30)
            
            # Memes definitions
            meme = None
            if "emperador" in title.lower() or "inmortal" in title.lower() or "joya" in title.lower():
                meme = "GIGACHAD 😎"
            elif "físico" in title.lower() or "combate" in title.lower():
                meme = "STONKS 📈"
            elif "imperfección" in title.lower() or "janko" in title.lower():
                meme = "OFERTAZO 💸"
                
            kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
            
            for f_idx in range(total_frames):
                progress = f_idx / total_frames
                
                # Rotate background screenshot every 600 frames (20 seconds) for variety!
                if loaded_screenshots:
                    ss_idx = (idx * 3 + (f_idx // 600)) % len(loaded_screenshots)
                    img_src = loaded_screenshots[ss_idx]
                else:
                    img_src = None
                    
                effect_type = kb_effects[(idx + (f_idx // 600)) % len(kb_effects)]
                frame_img = draw_horizontal_frame(
                    None, width, height, title.upper(),
                    f"Sección {idx + 1}: {custom_subtitle}",
                    font_title, font_sub, img_src, progress,
                    meme_text=meme if progress > 0.4 else None, font_meme=font_meme,
                    effect_type=effect_type
                )
                frame_img.save(os.path.join(frame_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
                
            # Compile frames to segment
            cmd_frames = [
                "ffmpeg", "-y",
                "-framerate", "30",
                "-i", os.path.join(frame_dir, "frame_%05d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-t", f"{dur:.2f}",
                seg_video
            ]
            subprocess.run(cmd_frames, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
        if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
            segment_files.append(seg_video)
            
    # Concatenate video segments
    raw_video = os.path.join(temp_dir, "raw_video.mp4")
    concat_inputs = []
    filter_concat_parts = []
    for idx, sf in enumerate(segment_files):
        concat_inputs.extend(["-i", sf])
        filter_concat_parts.append(f"[{idx}:v]")
    filter_concat_str = "".join(filter_concat_parts) + f"concat=n={len(segment_files)}:v=1:a=0[v]"
    
    cmd_concat = ["ffmpeg", "-y"]
    cmd_concat.extend(concat_inputs)
    cmd_concat.extend([
        "-filter_complex", filter_concat_str,
        "-map", "[v]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        raw_video
    ])
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Mix Audio, SFX, and BG Music
    audio_inputs = ["-i", raw_video, "-i", audio_path]
    audio_mix_filter = "[1:a]volume=1.0[speech];"
    
    bg_music_path = os.path.join(BASE_DIR, "music", bg_music_filename)
    use_bg = os.path.exists(bg_music_path)
    if use_bg:
        audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
        audio_mix_filter += "[2:a]volume=-22dB[bg_music];"
        
    sfx_available = os.path.exists(WHOOSH_SFX)
    if sfx_available:
        w_idx = 3 if use_bg else 2
        audio_inputs.extend(["-i", WHOOSH_SFX])
        
        sfx_filter = f"[{w_idx}:a]asplit={len(boundaries)-1}"
        for i in range(len(boundaries)-1):
            sfx_filter += f"[w{i}]"
        sfx_filter += ";"
        
        sfx_mixes = []
        for i in range(len(boundaries)-1):
            boundary_time = boundaries[i][1]
            delay_ms = int(boundary_time * 1000)
            sfx_filter += f"[w{i}]adelay={delay_ms}|{delay_ms}[wd{i}];"
            sfx_mixes.append(f"[wd{i}]")
            
        sfx_filter += f"{''.join(sfx_mixes)}amix=inputs={len(boundaries)-1}:normalize=0[sfx_raw];[sfx_raw]volume=-6dB[sfx_final];"
        audio_mix_filter += sfx_filter
        
        if use_bg:
            audio_mix_filter += "[speech][bg_music][sfx_final]amix=inputs=3:normalize=0[a]"
        else:
            audio_mix_filter += "[speech][sfx_final]amix=inputs=2:normalize=0[a]"
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
    res = subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
        
    if res.returncode != 0:
        print(f"  [ERROR] FFmpeg failed with exit code {res.returncode}")
        print(res.stderr.decode('utf-8', errors='ignore'))
    else:
        print(f"  [SUCCESS] Horizonal video generated at {output_path}")

def draw_vertical_frame(draw, width, height, title, desc, card_data, progress, font_title, font_sub, font_bold, capsule_path_or_img, effect_type="zoom_in"):
    img_src = None
    if capsule_path_or_img:
        if isinstance(capsule_path_or_img, str):
            if os.path.exists(capsule_path_or_img):
                img_src = Image.open(capsule_path_or_img)
        else:
            img_src = capsule_path_or_img

    if img_src:
        img_bg_static = get_ken_burns_crop(img_src, width, height, progress, effect_type)
        img_bg_static = img_bg_static.filter(ImageFilter.GaussianBlur(15))
        overlay = Image.new("RGBA", (width, height), (8, 12, 24, 180))
        img_bg = Image.alpha_composite(img_bg_static.convert("RGBA"), overlay)
    else:
        img_bg = Image.new("RGBA", (width, height), (13, 20, 38, 255))

        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Vignette overlay
    draw_img.rectangle([0, 0, width, height], outline=(0, 0, 0, 150), width=60)
    
    # Top Header
    header_w = 900
    header_h = 100
    header_x = (width - header_w) // 2
    header_y = 60
    draw_img.rounded_rectangle([header_x, header_y, header_x + header_w, header_y + header_h], radius=15, fill=(13, 20, 38, 210), outline=(255, 255, 255, 25), width=2)
    draw_img.text((width // 2, header_y + 30), "MOUNT & BLADE: WARBAND", font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, header_y + 70), "DETALLES Y CURIOSIDADES", font=font_bold, fill=(249, 115, 22, 255), anchor="mm")
    
    # Bottom progress indicator
    bar_width = header_w
    bar_fill = int(bar_width * progress)
    draw_img.rounded_rectangle([header_x, header_y + header_h + 10, header_x + bar_width, header_y + header_h + 14], radius=2, fill=(30, 41, 59, 255))
    draw_img.rounded_rectangle([header_x, header_y + header_h + 10, header_x + bar_fill, header_y + header_h + 14], radius=2, fill=(249, 115, 22, 255))
    
    # Dynamic content based on temporal progress
    if progress < 0.25:
        # State A: Title & Description
        card_w = 900
        card_h = 750
        card_x = (width - card_w) // 2
        card_y = 350
        
        # Shadow
        s_mask = Image.new("L", (card_w + 30, card_h + 30), 0)
        ImageDraw.Draw(s_mask).rounded_rectangle([15, 15, card_w + 15, card_h + 15], radius=20, fill=160)
        s_blur = s_mask.filter(ImageFilter.GaussianBlur(10))
        s_color = Image.new("RGBA", (card_w + 30, card_h + 30), (0, 0, 0, 200))
        img_bg.paste(s_color, (card_x - 15, card_y - 15), mask=s_blur)
        
        draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=20, fill=(13, 20, 38, 220), outline=(255, 255, 255, 30), width=2)
        
        # Display capsule art
        if img_src:
            cap_img = img_src.resize((360, 540))
            mask = Image.new("L", (360, 540), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, 360, 540], radius=15, fill=255)
            cap_x = card_x + 60
            cap_y = card_y + 100
            
            c_shadow = Image.new("L", (380, 560), 0)
            ImageDraw.Draw(c_shadow).rounded_rectangle([10, 10, 370, 550], radius=15, fill=180)
            c_blur = c_shadow.filter(ImageFilter.GaussianBlur(10))
            img_bg.paste(Image.new("RGBA", (380, 560), (0,0,0,180)), (cap_x - 10, cap_y - 10), mask=c_blur)
            
            img_bg.paste(cap_img, (cap_x, cap_y), mask=mask)
            draw_img.rounded_rectangle([cap_x, cap_y, cap_x + 360, cap_y + 540], radius=15, outline=(255, 255, 255, 100), width=3)
            
        # Text details
        text_x = card_x + 460
        draw_img.text((text_x, card_y + 220), "SABÍAS QUE...", font=font_bold, fill=(249, 115, 22, 255))
        
        # Wrap description
        t_words = desc.split()
        t_lines = []
        curr = []
        for w in t_words:
            if len(" ".join(curr + [w])) < 16:
                curr.append(w)
            else:
                t_lines.append(" ".join(curr))
                curr = [w]
        if curr:
            t_lines.append(" ".join(curr))
            
        ty = card_y + 290
        for l in t_lines:
            draw_img.text((text_x, ty), l, font=font_title, fill=(255, 255, 255, 255))
            ty += 60
            
        draw_img.text((text_x, ty + 20), "Warband Retrospectiva", font=font_sub, fill=(156, 163, 175, 255))
        
    elif progress < 0.75:
        # State B: Gameplay Video frame and Custom details card!
        box_w = 900
        box_h = 506
        box_x = (width - box_w) // 2
        box_y = 350
        
        # Draw dynamic monitor bezels
        draw_img.rounded_rectangle([box_x - 15, box_y - 15, box_x + box_w + 15, box_y + box_h + 15], radius=16, fill=(17, 24, 39, 255), outline=(249, 115, 22, 255), width=3)
        draw_img.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill=(0, 0, 0, 255))
        
        card_w = 900
        card_h = 420
        card_x = (width - card_w) // 2
        card_y = 900
        
        s_mask = Image.new("L", (card_w + 30, card_h + 30), 0)
        ImageDraw.Draw(s_mask).rounded_rectangle([15, 15, card_w + 15, card_h + 15], radius=20, fill=160)
        s_blur = s_mask.filter(ImageFilter.GaussianBlur(10))
        img_bg.paste(Image.new("RGBA", (card_w + 30, card_h + 30), (0, 0, 0, 200)), (card_x - 15, card_y - 15), mask=s_blur)
        
        draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=20, fill=(13, 20, 38, 220), outline=(255, 255, 255, 25), width=2)
        
        # Custom card bullets instead of price tables!
        if card_data:
            draw_img.text((width // 2, card_y + 40), card_data["header"], font=font_bold, fill=(249, 115, 22, 255), anchor="mm")
            bullet_y = card_y + 130
            for bullet in card_data["bullets"]:
                # Translucent row background
                draw_img.rounded_rectangle([card_x + 40, bullet_y - 35, card_x + card_w - 40, bullet_y + 35], radius=10, fill=(20, 27, 48, 180), outline=(255, 255, 255, 10), width=1)
                draw_img.text((card_x + 70, bullet_y), bullet, font=font_sub, fill=(255, 255, 255, 255), anchor="lm")
                bullet_y += 100
        
    else:
        # State C: Call to Action Subscribe Panel
        card_w = 900
        card_h = 1000
        card_x = (width - card_w) // 2
        card_y = 350
        
        s_mask = Image.new("L", (card_w + 30, card_h + 30), 0)
        ImageDraw.Draw(s_mask).rounded_rectangle([15, 15, card_w + 15, card_h + 15], radius=24, fill=160)
        s_blur = s_mask.filter(ImageFilter.GaussianBlur(10))
        img_bg.paste(Image.new("RGBA", (card_w + 30, card_h + 30), (0, 0, 0, 200)), (card_x - 15, card_y - 15), mask=s_blur)
        
        draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill=(13, 20, 38, 220), outline=(249, 115, 22, 100), width=2)
        
        logo_y = 560
        draw_img.rounded_rectangle([width//2 - 90, logo_y - 60, width//2 + 90, logo_y + 60], radius=20, fill=(239, 68, 68, 255))
        draw_img.polygon([(width//2 - 25, logo_y - 30), (width//2 - 25, logo_y + 30), (width//2 + 35, logo_y)], fill=(255, 255, 255, 255))
        
        draw_img.text((width // 2, 740), "@dominus8735", font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
        draw_img.text((width // 2, 810), "CURIOSIDADES & CONSEJOS TÁCTICOS", font=font_sub, fill=(200, 210, 230, 255), anchor="mm")
        
        btn_w = 400
        btn_h = 90
        btn_x = (width - btn_w) // 2
        btn_y = 920
        
        btn_shadow = Image.new("L", (btn_w + 20, btn_h + 20), 0)
        ImageDraw.Draw(btn_shadow).rounded_rectangle([5, 5, btn_w + 5, btn_h + 5], radius=16, fill=150)
        btn_blur = btn_shadow.filter(ImageFilter.GaussianBlur(10))
        img_bg.paste(Image.new("RGBA", (btn_w + 20, btn_h + 20), (0,0,0,180)), (btn_x - 5, btn_y - 5), mask=btn_blur)
        
        draw_img.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=16, fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=4)
        draw_img.text((width // 2, btn_y + btn_h // 2), "SUSCRÍBETE", font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
        
        draw_img.text((width // 2, 1120), "🔔 Activa la campanita para más secretos", font=font_sub, fill=(249, 115, 22, 255), anchor="mm")
        
    return img_bg.convert("RGB")

def compile_vertical_short(short_obj, bg_music_filename="Sneaky Snitch.mp3"):
    key = short_obj["key"]
    title = short_obj["title"]
    desc = short_obj["desc"]
    card = short_obj["card"]
    
    output_path = os.path.join(BASE_DIR, f"{key}_short.mp4")
    audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
    trailer_path = os.path.join(TRAILERS_DIR, "warband_trailer.mp4")
    capsule_path = os.path.join(CAPSULES_DIR, "warband_capsule.jpg")
    
    print(f"\nCompiling Vertical Short: {desc} ({key})")
    audio_dur = get_audio_duration(audio_path)
    if audio_dur == 0.0:
        print(f"  [ERROR] Audio file missing or empty: {audio_path}")
        return
        
    temp_dir = os.path.join(BASE_DIR, f"temp_frames_{key}")
    os.makedirs(temp_dir, exist_ok=True)
    
    width, height = 1080, 1920
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 45)
    font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 40)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 32)
    
    total_frames = int(audio_dur * 30)
    img_capsule = Image.open(capsule_path) if os.path.exists(capsule_path) else None
    
    kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right", "zoom_in"]
    short_idx = int(key.split("_")[-1]) - 1
    effect_type = kb_effects[short_idx % len(kb_effects)]
    
    for f_idx in range(total_frames):
        progress = f_idx / total_frames
        frame_img = draw_vertical_frame(
            None, width, height, title, desc, card, progress, font_title, font_sub, font_bold, img_capsule, effect_type
        )
        frame_img.save(os.path.join(temp_dir, f"frame_{f_idx:05d}.jpg"), quality=90)

        
    # Compile base video
    base_video = os.path.join(temp_dir, "base_video.mp4")
    cmd_base = [
        "ffmpeg", "-y",
        "-framerate", "30",
        "-i", os.path.join(temp_dir, "frame_%05d.jpg"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-t", f"{audio_dur:.2f}",
        base_video
    ]
    subprocess.run(cmd_base, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Overlay gameplay video in the center box for state B (0.25 to 0.75 progress)
    trailer_dur = get_audio_duration(trailer_path)
    if trailer_dur > 5.0:
        final_video_only = os.path.join(temp_dir, "final_video_only.mp4")
        start_t = 0.25 * audio_dur
        end_t = 0.75 * audio_dur
        overlay_dur = end_t - start_t
        
        # Sliced gameplay clip to overlay
        gameplay_clip = os.path.join(temp_dir, "gameplay_clip.mp4")
        cmd_slice = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-ss", "10.00",
            "-i", trailer_path,
            "-t", f"{overlay_dur:.2f}",
            "-vf", f"scale=1280:-1,crop=w='in_w*(1-0.12*t/{overlay_dur:.2f})':h='in_h*(1-0.12*t/{overlay_dur:.2f})':x='(in_w-out_w)/2':y='(in_h-out_h)/2',scale=900:506,force_original_aspect_ratio=decrease,pad=900:506:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
            gameplay_clip
        ]
        subprocess.run(cmd_slice, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        cmd_overlay = [
            "ffmpeg", "-y",
            "-i", base_video,
            "-i", gameplay_clip,
            "-filter_complex", f"[0:v][1:v]overlay=90:350:enable='between(t,{start_t:.2f},{end_t:.2f})'[out]",
            "-map", "[out]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            final_video_only
        ]
        subprocess.run(cmd_overlay, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        final_video_only = base_video
        
    # Audio track assembly
    audio_inputs = ["-i", final_video_only, "-i", audio_path]
    audio_mix_filter = "[1:a]volume=1.0[speech];"
    
    bg_music_path = os.path.join(BASE_DIR, "music", bg_music_filename)
    use_bg = os.path.exists(bg_music_path)
    if use_bg:
        audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
        audio_mix_filter += "[2:a]volume=-22dB[bg_music];"
        
    sfx_available = os.path.exists(POP_SFX) and os.path.exists(WHOOSH_SFX)
    if sfx_available:
        p_idx = 3 if use_bg else 2
        w_idx = 4 if use_bg else 3
        audio_inputs.extend(["-i", POP_SFX, "-i", WHOOSH_SFX])
        
        audio_mix_filter += (
            f"[{p_idx}:a]asplit=2[p0][p1];"
            f"[{w_idx}:a]asplit=2[w0][w1];"
            f"[p0]adelay={int(0.25*audio_dur*1000)}|{int(0.25*audio_dur*1000)}[pd0];"
            f"[p1]adelay={int(0.75*audio_dur*1000)}|{int(0.75*audio_dur*1000)}[pd1];"
            f"[w0]adelay=0|0[wd0];"
            f"[w1]adelay={int((audio_dur-0.8)*1000)}|{int((audio_dur-0.8)*1000)}[wd1];"
            f"[pd0][pd1][wd0][wd1]amix=inputs=4:normalize=0[sfx_raw];[sfx_raw]volume=-6dB[sfx_final];"
        )
        if use_bg:
            audio_mix_filter += "[speech][bg_music][sfx_final]amix=inputs=3:normalize=0[a]"
        else:
            audio_mix_filter += "[speech][sfx_final]amix=inputs=2:normalize=0[a]"
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
        "-c:v", "copy" if final_video_only != base_video else "libx264",
        "-c:a", "aac",
        "-movflags", "+faststart",
        "-shortest",
        output_path
    ])
    res = subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
        
    if res.returncode != 0:
        print(f"  [ERROR] FFmpeg failed with exit code {res.returncode}")
        print(res.stderr.decode('utf-8', errors='ignore'))
    else:
        print(f"  [SUCCESS] Vertical Short compiled at {output_path}")

def main():
    print("====================================================")
    print("Mount & Blade: Warband Rendering Suite")
    print("====================================================")
    
    generate_sfx_waves()
    
    # 1. Compile long horizontal video
    compile_horizontal_video(
        48700, "Mount & Blade: Warband", "warband",
        os.path.join(BASE_DIR, "warband_retrospective.mp4"),
        os.path.join(BASE_DIR, "script_warband_long.md"),
        os.path.join(BASE_DIR, "audio_warband_long.mp3"),
        "Analizando la inmortalidad de Calradia en Mount & Blade."
    )
    
    # 2. Compile 5 Shorts
    for short_obj in SHORTS_DATA:
        try:
            compile_vertical_short(short_obj)
        except Exception as e:
            print(f"  [ERROR] Failed to compile Short {short_obj['key']}: {e}")
            
    print("\n====================================================")
    print("Mount & Blade compilation suite completed!")
    print("====================================================")

if __name__ == "__main__":
    main()
