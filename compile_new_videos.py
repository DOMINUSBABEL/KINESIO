import os
import sys
import json
import math
import struct
import wave
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

BG_MUSIC_PATH = os.path.join(BASE_DIR, "background_music.mp3")
POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

# 7 Shorts configuration
SHORTS_GAMES = [
    {
        "key": "jc2",
        "appid": 8190,
        "title": "JUST CAUSE 2",
        "normal_title": "Just Cause 2",
        "prices": {"usa": "$2.24", "eur": "2,24 €", "latam": "$1.19"},
        "desc": "Caos Absoluto Barato"
    },
    {
        "key": "jc3",
        "appid": 225540,
        "title": "JUST CAUSE 3",
        "normal_title": "Just Cause 3",
        "prices": {"usa": "$2.99", "eur": "2,99 €", "latam": "$1.49"},
        "desc": "Destrucción y Traje Aéreo"
    },
    {
        "key": "aoe2",
        "appid": 813780,
        "title": "AGE OF EMPIRES II DE",
        "normal_title": "Age of Empires II: Definitive Edition",
        "prices": {"usa": "$9.99", "eur": "9,99 €", "latam": "$4.99"},
        "desc": "Rey del RTS Medieval"
    },
    {
        "key": "warband",
        "appid": 48700,
        "title": "MOUNT & BLADE: WARBAND",
        "normal_title": "Mount & Blade: Warband",
        "prices": {"usa": "$4.99", "eur": "4,99 €", "latam": "$2.49"},
        "desc": "Rol Medieval e Infinitos Mods"
    },
    {
        "key": "diplomacy",
        "appid": 1272320,
        "title": "DIPLOMACY IS NOT AN OPTION",
        "normal_title": "Diplomacy is Not an Option",
        "prices": {"usa": "$19.49", "eur": "19,49 €", "latam": "$9.99"},
        "desc": "Sobrevive a la Horda"
    },
    {
        "key": "syx",
        "appid": 1162750,
        "title": "SONGS OF SYX",
        "normal_title": "Songs of Syx",
        "prices": {"usa": "$19.99", "eur": "19,99 €", "latam": "$9.99"},
        "desc": "Mega Gestión Pixel Art"
    },
    {
        "key": "rimworld",
        "appid": 294100,
        "title": "RIMWORLD",
        "normal_title": "RimWorld",
        "prices": {"usa": "$27.99", "eur": "27,99 €", "latam": "$13.99"},
        "desc": "Simulador de Historias Emergentes"
    }
]

def generate_sfx_waves():
    """Generates Pop and Whoosh WAV files programmatically if missing."""
    if not os.path.exists(POP_SFX):
        # Pop: Fast rising pitch, rapid exp decay
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
        # Whoosh: Sine sweep 150Hz -> 800Hz with white noise overlay, parabolic volume envelope
        obj = wave.open(WHOOSH_SFX, 'w')
        obj.setnchannels(1)
        obj.setsampwidth(2)
        obj.setframerate(44100)
        duration = 0.8
        num_samples = int(duration * 44100)
        import random
        for i in range(num_samples):
            t = i / 44100
            freq = 150 + 650 * (t / duration)
            vol = 4 * (t / duration) * (1 - (t / duration)) # Parabolic envelope
            noise = random.uniform(-0.15, 0.15)
            val = int((math.sin(2 * math.pi * freq * t) + noise) * vol * 18000)
            data = struct.pack('<h', val)
            obj.writeframesraw(data)
        obj.close()

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except:
        return 0.0

def get_chapter_timestamps(script_path, audio_duration):
    """Calculates timestamps dynamically based on chapter word count proportion, handling multi-line quotes properly."""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    chapters = content.split("## 📌 ")
    chapter_texts = []
    chapter_titles = []
    
    for ch in chapters[1:]:
        lines = ch.split('\n')
        title = lines[0].split(':')[1].strip() if ':' in lines[0] else lines[0].strip()
        chapter_titles.append(title)
        
        # Extract locution robustly across multiple lines
        audio_lines = []
        capture = False
        for line in lines:
            if "Audio (Voz en off)" in line:
                capture = True
                idx_q = line.find('"')
                if idx_q != -1:
                    audio_lines.append(line[idx_q:])
                continue
            if capture:
                if line.strip().startswith('*') and ("Visual" in line or "Efecto" in line or "Meme" in line):
                    capture = False
                else:
                    audio_lines.append(line.strip())
        
        full_ch_text = " ".join(audio_lines)
        first_q = full_ch_text.find('"')
        last_q = full_ch_text.rfind('"')
        if first_q != -1 and last_q != -1 and last_q > first_q:
            loc = full_ch_text[first_q+1:last_q]
        else:
            loc = full_ch_text
            
        loc = loc.replace('**', '').replace('"', '').strip()
        chapter_texts.append(loc)
        
    word_counts = [len(text.split()) for text in chapter_texts]
    total_words = sum(word_counts)
    
    boundaries = []
    current_time = 0.0
    for wc, title in zip(word_counts, chapter_titles):
        duration = (wc / total_words) * audio_duration
        boundaries.append((current_time, current_time + duration, title))
        current_time += duration
        
    return boundaries

def draw_horizontal_frame(draw, width, height, title, subtitle, font_title, font_sub, screenshot_path, progress, meme_text=None, font_meme=None):
    # 1. Background image with slow zoom (Ken Burns) and Blur
    if os.path.exists(screenshot_path):
        img_src = Image.open(screenshot_path)
        # Slow zoom: 1.0x to 1.12x
        bg_scale = 1.0 + 0.12 * progress
        bg_w = int(width * bg_scale)
        bg_h = int(height * bg_scale)
        img_bg = img_src.resize((bg_w, bg_h))
        crop_x = (bg_w - width) // 2
        crop_y = (bg_h - height) // 2
        img_bg = img_bg.crop((crop_x, crop_y, crop_x + width, crop_y + height))
        img_bg = img_bg.filter(ImageFilter.GaussianBlur(18))
        overlay = Image.new("RGBA", (width, height), (8, 12, 24, 160))
        img_bg = Image.alpha_composite(img_bg.convert("RGBA"), overlay)
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
    
    # Draw drop shadow behind the panel
    shadow_offset = 15
    shadow_mask = Image.new("L", (panel_w + 40, panel_h + 40), 0)
    ImageDraw.Draw(shadow_mask).rounded_rectangle([15, 15, panel_w + 15, panel_h + 15], radius=30, fill=150)
    shadow_blur = shadow_mask.filter(ImageFilter.GaussianBlur(20))
    shadow_color = Image.new("RGBA", (panel_w + 40, panel_h + 40), (0, 0, 0, 220))
    img_bg.paste(shadow_color, (panel_left - 15 + shadow_offset, panel_top - 15 + shadow_offset), mask=shadow_blur)
    
    # Translucent glass panel
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(13, 20, 38, 210), outline=(255, 255, 255, 25), width=2)
    
    # Glowing neon accent bar at the top of the panel
    draw_img.rounded_rectangle([panel_left + 40, panel_top + 30, panel_right - 40, panel_top + 34], radius=2, fill=(30, 41, 59, 255))
    bar_width = panel_w - 80
    bar_fill = int(bar_width * progress)
    draw_img.rounded_rectangle([panel_left + 40, panel_top + 30, panel_left + 40 + bar_fill, panel_top + 34], radius=2, fill=(249, 115, 22, 255))
    
    # Top Center Indicator Badge
    badge_w = 260
    badge_h = 42
    badge_x = width // 2 - badge_w // 2
    badge_y = panel_top - 20
    draw_img.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=8, fill=(249, 115, 22, 255), outline=(255, 255, 255, 255), width=2)
    draw_img.text((width // 2, badge_y + badge_h // 2), "RECOMENDACIÓN", font=font_meme if font_meme else font_sub, fill=(255, 255, 255, 255), anchor="mm")
    
    # Draw Title
    draw_img.text((width // 2, panel_top + 110), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    # Subtitle separator line
    draw_img.line([width // 2 - 150, panel_top + 175, width // 2 + 150, panel_top + 175], fill=(249, 115, 22, 120), width=2)
    
    # Wrap subtitle
    words = subtitle.split()
    lines = []
    curr = []
    for w in words:
        if len(" ".join(curr + [w])) < 55:
            curr.append(w)
        else:
            lines.append(" ".join(curr))
            curr = [w]
    if curr:
        lines.append(" ".join(curr))
        
    y_offset = panel_top + 230
    for line in lines:
        draw_img.text((width // 2, y_offset), line, font=font_sub, fill=(215, 225, 245, 255), anchor="mm")
        y_offset += 60
        
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

def compile_horizontal_video(appid, game_name, prefix, output_path, script_path, audio_path):
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
    
    segment_files = []
    
    # 6 Chapters
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
            # Slice gameplay from the trailer
            clip_start = (idx * 15.0) % (trailer_dur - dur)
            cmd_slice = [
                "ffmpeg", "-y",
                "-ss", f"{clip_start:.2f}",
                "-i", trailer_file,
                "-t", f"{dur:.2f}",
                "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
                seg_video
            ]
            subprocess.run(cmd_slice, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            # Render PIL slide
            frame_dir = os.path.join(temp_dir, f"frames_{idx}")
            os.makedirs(frame_dir, exist_ok=True)
            
            # Select screenshot
            ss_file = os.path.join(SCREENSHOTS_DIR, f"{prefix}_screenshot_{idx % 10}.jpg")
            total_frames = int(dur * 30)
            
            # Memes definitions
            meme = None
            if "cállate y toma mi dinero" in title.lower() or "cómpralo" in title.lower() or "comprar" in title.lower():
                meme = "STONKS 📈"
            elif "falla" in title.lower() or "veredicto" in title.lower():
                meme = "GIGACHAD 😎"
            elif "gratis" in title.lower() or "solari" in title.lower() or "descuento" in title.lower():
                meme = "OFERTAZO 💸"
                
            for f_idx in range(total_frames):
                progress = f_idx / total_frames
                frame_img = draw_horizontal_frame(
                    None, width, height, title.upper(),
                    f"Sección {idx + 1}: Analizando mecánicas, fidelidad y rejugabilidad de la cruzada en Arrakis.",
                    font_title, font_sub, ss_file, progress,
                    meme_text=meme if progress > 0.4 else None, font_meme=font_meme
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
            subprocess.run(cmd_frames, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
            segment_files.append(seg_video)
            
    # Concatenate video segments using the concat filter to decode and re-encode,
    # ensuring identical timebase, headers, and codecs across mismatched streams.
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
    subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Mix Audio, SFX (whoosh at chapter boundaries), and BG Music
    audio_inputs = ["-i", raw_video, "-i", audio_path]
    audio_mix_filter = "[1:a]volume=1.0[speech];"
    
    # Add optional background music
    use_bg = os.path.exists(BG_MUSIC_PATH)
    if use_bg:
        audio_inputs.extend(["-i", BG_MUSIC_PATH])
        audio_mix_filter += "[2:a]volume=-22dB,aloop=loop=-1:size=3e7[bg_music];"
        
    # SFX stitching for chapter boundaries
    sfx_available = os.path.exists(WHOOSH_SFX)
    if sfx_available:
        w_idx = len(audio_inputs) // 2
        audio_inputs.extend(["-i", WHOOSH_SFX])
        
        # Build adelay commands for each chapter transition
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
        
        # Merge speech, music, and sfx
        if use_bg:
            audio_mix_filter += "[speech][bg_music][sfx_final]amix=inputs=3:normalize=0[a]"
        else:
            audio_mix_filter += "[speech][sfx_final]amix=inputs=2:normalize=0[a]"
    else:
        if use_bg:
            audio_mix_filter += "[speech][bg_music]amix=inputs=2:normalize=0[a]"
        else:
            audio_mix_filter += "[speech]anull[a]"
            
    # Compile final video (copy video stream, encode audio to prevent lengthy re-encoding!)
    cmd_final = ["ffmpeg", "-y"]
    cmd_final.extend(audio_inputs)
    cmd_final.extend([
        "-filter_complex", audio_mix_filter,
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy", # FAST MIXING
        "-c:a", "aac",
        "-shortest",
        output_path
    ])
    subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Cleanup temp
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
    print(f"  [SUCCESS] Horizonal video generated at {output_path}")

def draw_vertical_frame(draw, width, height, title, desc, prices, progress, font_title, font_sub, font_bold, capsule_path):
    # 1. Background image with motion zoom (Ken Burns) and Blur
    if os.path.exists(capsule_path):
        img_src = Image.open(capsule_path)
        # Slow zoom: from 1.0x to 1.15x
        bg_scale = 1.0 + 0.15 * progress
        bg_w = int(width * bg_scale)
        bg_h = int(height * bg_scale)
        img_bg = img_src.resize((bg_w, bg_h))
        crop_x = (bg_w - width) // 2
        crop_y = (bg_h - height) // 2
        img_bg = img_bg.crop((crop_x, crop_y, crop_x + width, crop_y + height))
        img_bg = img_bg.filter(ImageFilter.GaussianBlur(30))
        overlay = Image.new("RGBA", (width, height), (8, 12, 24, 180))
        img_bg = Image.alpha_composite(img_bg.convert("RGBA"), overlay)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Subtle vignette border (darkened edges)
    draw_img.rectangle([0, 0, width, height], outline=(0, 0, 0, 100), width=40)
    
    # 2. Modern Glassmorphism Header Bar (Translucent backdrop with thin white border)
    draw_img.rounded_rectangle([40, 45, width-40, 155], radius=16, fill=(13, 20, 38, 220), outline=(255, 255, 255, 30), width=2)
    draw_img.text((width // 2, 75), "OFERTAS DE VERANO", font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, 118), "STEAM SUMMER SALE 2026", font=font_sub, fill=(249, 115, 22, 255), anchor="mm")
    
    # Progress Bar: modern neon indicator line below header
    bar_width = width - 120
    bar_fill = int(bar_width * progress)
    draw_img.rounded_rectangle([60, 175, width-60, 181], radius=3, fill=(30, 41, 59, 255))
    draw_img.rounded_rectangle([60, 175, 60 + bar_fill, 181], radius=3, fill=(249, 115, 22, 255))
    
    # Phase 1: Intro (0.0 to 0.25 progress)
    if progress < 0.25:
        # Elastic Scale Intro: Zoom in with smooth ease out
        t = progress / 0.25
        scale = 0.5 + 0.55 * (1.0 - (1.0 - t)**3)
        cap_w = int(540 * scale)
        cap_h = int(810 * scale)
        
        if os.path.exists(capsule_path):
            img_cap = Image.open(capsule_path).resize((cap_w, cap_h))
            
            # Draw Drop Shadow behind capsule (creates professional depth)
            shadow_offset = 12
            shadow_mask = Image.new("L", (cap_w + 30, cap_h + 30), 0)
            ImageDraw.Draw(shadow_mask).rounded_rectangle([10, 10, cap_w + 10, cap_h + 10], radius=24, fill=120)
            shadow_blur = shadow_mask.filter(ImageFilter.GaussianBlur(15))
            shadow_color = Image.new("RGBA", (cap_w + 30, cap_h + 30), (0, 0, 0, 200))
            img_bg.paste(shadow_color, (((width - cap_w) // 2) - 10 + shadow_offset, 280 - 10 + shadow_offset), mask=shadow_blur)
            
            # Mask rounded corners for Capsule
            mask = Image.new("L", (cap_w, cap_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, cap_w, cap_h], radius=24, fill=255)
            img_bg.paste(img_cap, ((width - cap_w) // 2, 280), mask=mask)
            
            # Glowing border around capsule
            draw_img.rounded_rectangle([((width - cap_w) // 2) - 1, 279, ((width - cap_w) // 2) + cap_w + 1, 280 + cap_h + 1], radius=24, outline=(249, 115, 22, 200), width=3)
            
        # Text block with glassmorphism backdrop
        draw_img.rounded_rectangle([60, 1180, width-60, 1370], radius=20, fill=(13, 20, 38, 200), outline=(255, 255, 255, 20), width=2)
        draw_img.text((width // 2, 1240), title, font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
        draw_img.text((width // 2, 1310), desc.upper(), font=font_sub, fill=(249, 115, 22, 255), anchor="mm")
        
    # Phase 2: Gameplay & Price comparison (0.25 to 0.75 progress)
    elif progress < 0.75:
        # Curated screen mockup frame for gameplay clip!
        box_w = 920
        box_h = 518
        box_x = (width - box_w) // 2
        box_y = 280
        
        # Monitor outer bezel
        draw_img.rounded_rectangle([box_x - 8, box_y - 8, box_x + box_w + 8, box_y + box_h + 8], radius=16, fill=None, outline=(30, 41, 59, 255), width=8)
        # Glowing inner neon accent
        draw_img.rounded_rectangle([box_x - 3, box_y - 3, box_x + box_w + 3, box_y + box_h + 3], radius=12, fill=None, outline=(249, 115, 22, 255), width=3)
        
        # Comparative prices list inside sleek glass cards
        panel_y = 860
        # Main glass panel container
        draw_img.rounded_rectangle([50, panel_y, width-50, panel_y + 350], radius=24, fill=(10, 15, 30, 210), outline=(255, 255, 255, 30), width=2)
        draw_img.text((width // 2, panel_y + 40), "PRECIOS COMPARATIVOS", font=font_bold, fill=(249, 115, 22, 255), anchor="mm")
        
        # USA Price Pill
        draw_img.rounded_rectangle([70, panel_y + 80, width-70, panel_y + 150], radius=12, fill=(20, 27, 48, 180), outline=(255, 255, 255, 10), width=1)
        draw_img.text((100, panel_y + 115), "🇺🇸  ESTADOS UNIDOS (USA)", font=font_sub, fill=(200, 210, 230, 255), anchor="lm")
        draw_img.text((width - 100, panel_y + 115), prices["usa"], font=font_bold, fill=(255, 255, 255, 255), anchor="rm")
        
        # EUR Price Pill
        draw_img.rounded_rectangle([70, panel_y + 165, width-70, panel_y + 235], radius=12, fill=(20, 27, 48, 180), outline=(255, 255, 255, 10), width=1)
        draw_img.text((100, panel_y + 200), "🇪🇺  EUROPA (EUR)", font=font_sub, fill=(200, 210, 230, 255), anchor="lm")
        draw_img.text((width - 100, panel_y + 200), prices["eur"], font=font_bold, fill=(255, 255, 255, 255), anchor="rm")
        
        # LATAM Region Price Pill (Highlight: green card!)
        draw_img.rounded_rectangle([70, panel_y + 250, width-70, panel_y + 320], radius=12, fill=(16, 40, 32, 200), outline=(34, 197, 94, 80), width=2)
        draw_img.text((100, panel_y + 285), "🌎  LATINOAMÉRICA (REG)", font=font_sub, fill=(187, 247, 208, 255), anchor="lm")
        draw_img.text((width - 100, panel_y + 285), prices["latam"], font=font_bold, fill=(34, 197, 94, 255), anchor="rm")
        
    # Phase 3: Outro CTA (0.75 to 1.0 progress)
    else:
        # Subscribe Panel and Branding
        draw_img.rounded_rectangle([80, 400, width-80, 1400], radius=24, fill=(13, 20, 38, 220), outline=(249, 115, 22, 100), width=2)
        
        # Giant pulsing YouTube logo or similar shape
        logo_y = 580
        draw_img.rounded_rectangle([width//2 - 60, logo_y - 40, width//2 + 60, logo_y + 40], radius=15, fill=(239, 68, 68, 255))
        # Draw play triangle inside logo
        draw_img.polygon([(width//2 - 15, logo_y - 20), (width//2 - 15, logo_y + 20), (width//2 + 20, logo_y)], fill=(255, 255, 255, 255))
        
        # Channel name
        draw_img.text((width // 2, 700), "@dominus8735", font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
        draw_img.text((width // 2, 760), "ANÁLISIS & RECOMENDACIONES", font=font_sub, fill=(200, 210, 230, 255), anchor="mm")
        
        # Pulsing CTA Subscribe button
        pulse = 1.0 + 0.05 * math.sin(progress * 25)
        btn_w = int(640 * pulse)
        btn_h = int(130 * pulse)
        btn_x = (width - btn_w) // 2
        btn_y = 950
        
        # Draw Drop Shadow behind button
        btn_shadow = Image.new("L", (btn_w + 20, btn_h + 20), 0)
        ImageDraw.Draw(btn_shadow).rounded_rectangle([5, 5, btn_w + 5, btn_h + 5], radius=16, fill=150)
        btn_blur = btn_shadow.filter(ImageFilter.GaussianBlur(10))
        btn_shadow_color = Image.new("RGBA", (btn_w + 20, btn_h + 20), (0, 0, 0, 180))
        img_bg.paste(btn_shadow_color, (btn_x - 5, btn_y - 5), mask=btn_blur)
        
        # Red pulsing subscribe button
        draw_img.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=16, fill=(239, 68, 68, 255), outline=(255, 255, 255, 255), width=4)
        draw_img.text((width // 2, btn_y + btn_h // 2), "SUSCRÍBETE", font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
        
        draw_img.text((width // 2, 1200), "🔔 Activa la campanita para más ofertas", font=font_sub, fill=(249, 115, 22, 255), anchor="mm")
        
    return img_bg.convert("RGB")

def compile_vertical_short(game):
    key = game["key"]
    appid = game["appid"]
    title = game["title"]
    prices = game["prices"]
    desc = game["desc"]
    
    output_path = os.path.join(BASE_DIR, f"{key}_v3_short.mp4")
    audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
    trailer_path = os.path.join(TRAILERS_DIR, f"trailer_{appid}.mp4")
    capsule_path = os.path.join(CAPSULES_DIR, f"capsule_{appid}.jpg")
    
    print(f"\nCompiling Vertical Short: {title}")
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
    for f_idx in range(total_frames):
        progress = f_idx / total_frames
        frame_img = draw_vertical_frame(
            None, width, height, title, desc, prices, progress, font_title, font_sub, font_bold, capsule_path
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
    subprocess.run(cmd_base, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Overlay gameplay video in central box during 0.25 to 0.75 progress
    final_video_only = os.path.join(temp_dir, "video_only.mp4")
    trailer_dur = get_audio_duration(trailer_path) if os.path.exists(trailer_path) else 0.0
    
    if trailer_dur > 15.0:
        start_t = 0.25 * audio_dur
        end_t = 0.75 * audio_dur
        overlay_dur = end_t - start_t
        
        # Crop/slice gameplay segment
        gameplay_clip = os.path.join(temp_dir, "gameplay_clip.mp4")
        cmd_slice = [
            "ffmpeg", "-y",
            "-ss", f"{10.0:.2f}",
            "-i", trailer_path,
            "-t", f"{overlay_dur:.2f}",
            "-vf", "scale=900:506:force_original_aspect_ratio=decrease,pad=900:506:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
            gameplay_clip
        ]
        subprocess.run(cmd_slice, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Overlay gameplay_clip over base_video
        cmd_overlay = [
            "ffmpeg", "-y",
            "-i", base_video,
            "-i", gameplay_clip,
            "-filter_complex", f"[0:v][1:v]overlay=90:350:enable='between(t,{start_t:.2f},{end_t:.2f})'[out]",
            "-map", "[out]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p",
            final_video_only
        ]
        subprocess.run(cmd_overlay, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        final_video_only = base_video
        
    # Audio track assembly: mix voiceover, pop SFX (at 0.25 and 0.75), whoosh SFX (at start and end), and background music
    audio_inputs = ["-i", final_video_only, "-i", audio_path]
    audio_mix_filter = "[1:a]volume=1.0[speech];"
    
    use_bg = os.path.exists(BG_MUSIC_PATH)
    if use_bg:
        audio_inputs.extend(["-i", BG_MUSIC_PATH])
        audio_mix_filter += "[2:a]volume=-22dB,aloop=loop=-1:size=3e7[bg_music];"
        
    sfx_available = os.path.exists(POP_SFX) and os.path.exists(WHOOSH_SFX)
    if sfx_available:
        p_idx = len(audio_inputs) // 2
        w_idx = p_idx + 1
        audio_inputs.extend(["-i", POP_SFX, "-i", WHOOSH_SFX])
        
        # Split pop and whoosh
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
            
    # Final render
    cmd_final = ["ffmpeg", "-y"]
    cmd_final.extend(audio_inputs)
    cmd_final.extend([
        "-filter_complex", audio_mix_filter,
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy" if final_video_only != base_video else "libx264", # fast mix if possible
        "-c:a", "aac",
        "-shortest",
        output_path
    ])
    subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Cleanup temp
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
    print(f"  [SUCCESS] Vertical Short compiled at {output_path}")

def main():
    print("====================================================")
    print("KINESIO Render Engine v3 (Horizontal & Regional Shorts)")
    print("====================================================")
    
    generate_sfx_waves()
    
    # 1. Compile long videos
    compile_horizontal_video(
        1605220, "Dune Spice Wars", "dune_spice_wars",
        os.path.join(BASE_DIR, "dune_spice_wars_analysis.mp4"),
        os.path.join(BASE_DIR, "script_dune.md"),
        os.path.join(BASE_DIR, "audio_dune.mp3")
    )
    
    compile_horizontal_video(
        1184370, "Pathfinder Wrath of the Righteous", "pathfinder_wrath_of_the_righteous",
        os.path.join(BASE_DIR, "pathfinder_wrath_of_the_righteous_analysis.mp4"),
        os.path.join(BASE_DIR, "script_pathfinder.md"),
        os.path.join(BASE_DIR, "audio_pathfinder.mp3")
    )

    compile_horizontal_video(
        400750, "Call to Arms Gates of Hell Ostfront", "gates_of_hell",
        os.path.join(BASE_DIR, "gates_of_hell_analysis.mp4"),
        os.path.join(BASE_DIR, "script_gates_of_hell.md"),
        os.path.join(BASE_DIR, "audio_gates_of_hell.mp3")
    )

    compile_horizontal_video(
        774241, "Warhammer Chaosbane", "chaosbane",
        os.path.join(BASE_DIR, "chaosbane_analysis.mp4"),
        os.path.join(BASE_DIR, "script_chaosbane.md"),
        os.path.join(BASE_DIR, "audio_chaosbane.mp3")
    )

    compile_horizontal_video(
        826630, "Iron Harvest", "iron_harvest",
        os.path.join(BASE_DIR, "iron_harvest_analysis.mp4"),
        os.path.join(BASE_DIR, "script_iron_harvest.md"),
        os.path.join(BASE_DIR, "audio_iron_harvest.mp3")
    )
    
    # 2. Compile Shorts
    for game in SHORTS_GAMES:
        try:
            compile_vertical_short(game)
        except Exception as e:
            print(f"  [ERROR] Failed to compile Short for {game['title']}: {e}")
            
    print("\n====================================================")
    print("All compilations and renders completed!")
    print("====================================================")

if __name__ == "__main__":
    main()
