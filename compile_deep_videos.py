import os
import sys
import re
import time
import json
import shutil
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\reddit_deep_project"
MUSIC_DIR = r"C:\Users\jegom\shorts_project\music"
CAPSULES_DIR = os.path.join(PROJECT_DIR, "capsules")
manifest_path = os.path.join(PROJECT_DIR, "manifest.json")
POP_SFX = os.path.join(PROJECT_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(PROJECT_DIR, "whoosh.wav")

from kinesio_core import get_ken_burns_crop, draw_outlined_text

def clean_word_for_display(word):
    cleaned = re.sub(r'^[¿"\'\(]+|[?"\'\),\.]+$', '', word)
    return cleaned.upper()

def draw_rotated_outlined_text(img, position, text, font, text_color, outline_color, thickness, angle):
    text_w = 700
    text_h = 250
    text_img = Image.new("RGBA", (text_w, text_h), (0, 0, 0, 0))
    text_draw = ImageDraw.Draw(text_img)
    
    w, h = text_w // 2, text_h // 2
    
    # Draw outline
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx*dx + dy*dy <= thickness*thickness:
                text_draw.text((w + dx, h + dy), text, font=font, fill=outline_color, anchor="mm")
                
    # Draw text
    text_draw.text((w, h), text, font=font, fill=text_color, anchor="mm")
    
    # Rotate
    rotated_img = text_img.rotate(angle, resample=Image.BICUBIC, expand=True)
    
    # Composite back
    rx, ry = rotated_img.size
    px = position[0] - rx // 2
    py = position[1] - ry // 2
    img.paste(rotated_img, (px, py), mask=rotated_img)

def draw_horizontal_frame(width, height, title, current_words, font_title, font_sub, font_caption_active, font_caption_side, base_img, progress):
    # Widescreen 16:9 Frame
    # 1. Background image: scaled up and heavily blurred
    if base_img:
        img_bg = get_ken_burns_crop(base_img, width, height, progress, "zoom_in").convert("RGBA")
        img_bg = img_bg.filter(ImageFilter.GaussianBlur(24))
        overlay = Image.new("RGBA", (width, height), (10, 10, 15, 170)) # Darken
        img_bg = Image.alpha_composite(img_bg, overlay)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 12, 20, 255))
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # 2. Cinema Letterbox borders (Top and Bottom)
    bar_h = 130
    draw_img.rectangle([0, 0, width, bar_h], fill=(0, 0, 0, 255))
    draw_img.rectangle([0, height - bar_h, width, height], fill=(0, 0, 0, 255))
    
    # 3. Center Illustration Card (Widescreen Ken Burns)
    card_w = 960
    card_h = 540
    card_x = (width - card_w) // 2
    card_y = (height - card_h) // 2
    
    # Card drop shadow
    c_shadow = Image.new("L", (card_w + 40, card_h + 40), 0)
    ImageDraw.Draw(c_shadow).rounded_rectangle([15, 15, card_w + 15, card_h + 15], radius=20, fill=160)
    c_blur = c_shadow.filter(ImageFilter.GaussianBlur(16))
    img_bg.paste(Image.new("RGBA", (card_w + 40, card_h + 40), (0, 0, 0, 200)), (card_x - 15, card_y - 15), mask=c_blur)
    
    # Sharp illustration crop
    if base_img:
        illustration_crop = get_ken_burns_crop(base_img, card_w - 10, card_h - 10, progress, "zoom_in")
        mask = Image.new("L", (card_w - 10, card_h - 10), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, card_w - 10, card_h - 10], radius=16, fill=255)
        
        img_bg.paste(illustration_crop, (card_x + 5, card_y + 5), mask=mask)
        
    # Draw border panel
    draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=20, fill=None, outline=(56, 189, 248, 200), width=4)
    
    # 4. Top Title Text (In Top Letterbox)
    draw_img.text((width // 2, bar_h // 2), title.upper(), font=font_title, fill=(255, 255, 255, 240), anchor="mm")
    
    # 5. Widescreen Subtitles (In Bottom Letterbox)
    prev_w, active_w, next_w = current_words
    text_y = height - bar_h // 2
    
    if active_w:
        draw_outlined_text(draw_img, (width // 2, text_y), clean_word_for_display(active_w), font_caption_active, text_color=(254, 240, 138, 255), outline_color=(0, 0, 0, 255), thickness=4)
    if prev_w:
        draw_outlined_text(draw_img, (width // 2 - 250, text_y), clean_word_for_display(prev_w), font_caption_side, text_color=(200, 200, 200, 180), outline_color=(0, 0, 0, 180), thickness=3)
    if next_w:
        draw_outlined_text(draw_img, (width // 2 + 250, text_y), clean_word_for_display(next_w), font_caption_side, text_color=(200, 200, 200, 180), outline_color=(0, 0, 0, 180), thickness=3)
        
    # Floating progress line inside bottom bar
    progress_w = int(width * progress)
    draw_img.rectangle([0, height - 6, width, height], fill=(15, 23, 42, 255))
    draw_img.rectangle([0, height - 6, progress_w, height], fill=(56, 189, 248, 255))
    
    return img_bg.convert("RGB")

def draw_vertical_short_frame(width, height, title, badge, current_words, font_title, font_sub, font_badge, font_caption_active, font_caption_side, base_img, progress, effect_type="zoom_in", frame_idx=0):
    # 1. Background image: scaled up and blurred slightly (Depth of Field)
    if base_img:
        img_bg = get_ken_burns_crop(base_img, width, height, progress, effect_type).convert("RGBA")
        img_bg = img_bg.filter(ImageFilter.GaussianBlur(14))
        overlay = Image.new("RGBA", (width, height), (10, 10, 15, 140)) # Dim slightly
        img_bg = Image.alpha_composite(img_bg, overlay)
    else:
        img_bg = Image.new("RGBA", (width, height), (15, 15, 20, 255))
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # 2. Add subtle dark gradient overlay at the bottom for subtitles readability
    for y in range(1200, 1920):
        alpha = int((y - 1200) / 720 * 180) # max opacity 180
        draw_img.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))
        
    # Also add a light dark gradient at the top for the header
    for y in range(0, 300):
        alpha = int((300 - y) / 300 * 140)
        draw_img.line([(0, y), (width, y)], fill=(0, 0, 0, alpha))

    # 3. Top Header Panel (Clean and Minimal)
    header_y = 120
    draw_img.text((width // 2, header_y), "TRABAJOS EXTREMOS 🌍", font=font_sub, fill=(56, 189, 248, 255), anchor="mm")
    
    clean_title = title.replace("Historia ", "H").upper()
    if len(clean_title) > 30:
        clean_title = clean_title[:27] + "..."
    draw_img.text((width // 2, header_y + 60), clean_title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    # Badge (Centered, below title)
    if badge:
        badge_y = header_y + 130
        badge_w = 340
        badge_h = 55
        badge_x = (width - badge_w) // 2
        draw_img.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=10, fill=(15, 23, 42, 180), outline=(56, 189, 248, 200), width=2)
        draw_img.text((width // 2, badge_y + badge_h // 2), badge.upper(), font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
    # 4. Floating Glassmorphic Card in Center with SHARP illustration
    bob_offset = int(12 * math.sin(2 * math.pi * frame_idx / 60))
    
    card_w = 900
    card_h = 800
    card_x = (width - card_w) // 2
    card_y = 480 + bob_offset
    
    # Draw drop shadow
    c_shadow = Image.new("L", (card_w + 30, card_h + 30), 0)
    ImageDraw.Draw(c_shadow).rounded_rectangle([12, 12, card_w + 12, card_h + 12], radius=24, fill=170)
    c_blur = c_shadow.filter(ImageFilter.GaussianBlur(12))
    img_bg.paste(Image.new("RGBA", (card_w + 30, card_h + 30), (0, 0, 0, 190)), (card_x - 12, card_y - 12), mask=c_blur)
    
    # Draw main card frame
    draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill=(15, 23, 42, 110), outline=(56, 189, 248, 255), width=3)
    
    # Crop and paste sharp illustration
    if base_img:
        bw, bh = base_img.size
        cx, cy = bw // 2, bh // 2
        illustration_crop = base_img.crop((cx - 440, cy - 390, cx + 440, cy + 390))
        
        mask = Image.new("L", (880, 780), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, 880, 780], radius=20, fill=255)
        
        img_bg.paste(illustration_crop, (card_x + 10, card_y + 10), mask=mask)
        
    # 5. Kinetic Subtitles Rendering (Lower third)
    prev_w, active_w, next_w = current_words
    text_y_center = 1550
    
    if active_w:
        tilt_angle = 4 if len(active_w) % 2 == 0 else -4
        draw_rotated_outlined_text(img_bg, (width // 2, text_y_center), clean_word_for_display(active_w), font_caption_active, text_color=(254, 240, 138, 255), outline_color=(0, 0, 0, 255), thickness=6, angle=tilt_angle)
        
    if prev_w:
        draw_outlined_text(draw_img, (width // 2 - 280, text_y_center + 10), clean_word_for_display(prev_w), font_caption_side, text_color=(220, 220, 220, 200), outline_color=(0, 0, 0, 200), thickness=4)
        
    if next_w:
        draw_outlined_text(draw_img, (width // 2 + 280, text_y_center + 10), clean_word_for_display(next_w), font_caption_side, text_color=(220, 220, 220, 200), outline_color=(0, 0, 0, 200), thickness=4)
        
    # Bottom progress line
    progress_w = int(width * progress)
    draw_img.rectangle([0, height - 8, width, height], fill=(15, 23, 42, 255))
    draw_img.rectangle([0, height - 8, progress_w, height], fill=(56, 189, 248, 255))
    
    # Watermark
    draw_img.text((width // 2, height - 50), "@desparchingshorts", font=font_badge, fill=(255, 255, 255, 80), anchor="mm")
    
    return img_bg.convert("RGB")

MUSIC_MAPPING = {
    1: "Moorland.mp3",          # McMurdo (Antarctica)
    2: "Cipher2.mp3",           # Saturation Diving (Deep Sea)
    3: "Severe Tire Damage.mp3",# Oregon Fire Lookout (Storm)
    4: "Sneaky Snitch.mp3",     # Svalbard (Intriguing/Osos)
    5: "Future Gladiator.mp3",  # Point Nemo (Cosmic Void)
    6: "Rites.mp3"              # Chernobyl (Eerie/Nuclear)
}

def compile_videos():
    if not os.path.exists(manifest_path):
        print(f"[ERROR] Manifest file not found at: {manifest_path}")
        return
        
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)
        
    print("\n====================================================")
    print("TRABAJOS EXTREMOS CAMPAIGN VIDEOS COMPILER")
    print("====================================================\n")
    
    # Widescreen Fonts
    font_w_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 36)
    font_w_caption_active = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 46)
    font_w_caption_side = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 30)
    
    # Vertical Fonts
    font_v_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_v_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 32)
    font_v_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    font_v_caption_active = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 82)
    font_v_caption_side = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 48)
    
    # --- 1. COMPILE LONG FORM HORIZONTAL VIDEOS ---
    print("--- STEP 1: COMPILING LONG FORM HORIZONTAL VIDEOS ---")
    for item in manifest_data["long_form"]:
        key = item["key"]
        story_num = item["story_num"]
        title = item["title"]
        audio_file = item["audio_file"]
        audio_dur = item["duration"]
        script = item["script"]
        
        output_path = os.path.join(PROJECT_DIR, f"{key}_final.mp4")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Long-form video {key} already exists on disk. Skipping.")
            continue
            
        audio_full_path = os.path.join(PROJECT_DIR, audio_file)
        if audio_dur == 0.0 or not os.path.exists(audio_full_path):
            print(f"[SKIP] Audio track missing or empty for {key}: {audio_full_path}")
            continue
            
        print(f"\nCompiling Horizontal Video: {key} ({audio_dur:.2f}s) - {title}")
        
        bg_path = os.path.join(CAPSULES_DIR, f"story_{story_num}.jpg")
        base_img = Image.open(bg_path) if os.path.exists(bg_path) else None
        
        temp_dir = os.path.join(PROJECT_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        
        words = script.split()
        total_words = len(words)
        total_frames = int(audio_dur * 30)
        t0 = time.time()
        
        raw_video = os.path.join(temp_dir, "raw_video.mp4")
        
        # Start FFmpeg subprocess to receive raw RGB24 stream on stdin
        cmd_frames = [
            "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", "1920x1080", "-r", "30", "-i", "-",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", f"{audio_dur:.2f}",
            raw_video
        ]
        proc = subprocess.Popen(cmd_frames, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        for f_idx in range(total_frames):
            progress = f_idx / total_frames
            curr_time = f_idx / 30.0
            
            # Linear word interpolation
            word_idx = int(curr_time * (total_words / audio_dur))
            word_idx = min(word_idx, total_words - 1)
            
            prev_w = words[word_idx - 1] if word_idx > 0 else ""
            active_w = words[word_idx]
            next_w = words[word_idx + 1] if word_idx < total_words - 1 else ""
            
            frame_img = draw_horizontal_frame(
                1920, 1080,
                title,
                (prev_w, active_w, next_w),
                font_w_title, font_w_title,
                font_w_caption_active, font_w_caption_side,
                base_img, progress
            )
            
            # Write raw RGB bytes directly to FFmpeg pipe
            proc.stdin.write(frame_img.tobytes())
            
        # Close pipe and wait for video compilation to finish
        proc.stdin.close()
        proc.wait()
        
        fps_render = total_frames / (time.time() - t0)
        print(f"  Piped and Compiled {total_frames} frames in {time.time()-t0:.1f}s ({fps_render:.1f} FPS)")
        
        # Audio Mix using FFmpeg
        bg_music_file = MUSIC_MAPPING.get(story_num, "Moorland.mp3")
        bg_music_path = os.path.join(MUSIC_DIR, bg_music_file)
        
        audio_mix = "[1:a]volume=1.0[speech];"
        audio_inputs = ["-i", raw_video, "-i", audio_full_path]
        
        if os.path.exists(bg_music_path):
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            music_idx = len(audio_inputs) - 1
            audio_mix += f"[{music_idx}:a]volume=-25dB[bg_music];[speech][bg_music]amix=inputs=2:normalize=0[a]"
        else:
            audio_mix += "[speech]anull[a]"
            
        cmd_final = ["ffmpeg", "-y"] + audio_inputs + ["-filter_complex", audio_mix, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-shortest", output_path]
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
            
        print(f"  [SUCCESS] Compiled horizontal video at: {output_path}")

    # --- 2. COMPILE VERTICAL SHORTS ---
    print("\n--- STEP 2: COMPILING VERTICAL SHORTS ---")
    for item in manifest_data["shorts"]:
        key = item["key"]
        parent_key = item["parent_key"]
        story_num = int(key.split("_")[2])
        part_num = item["part_num"]
        title = item["title"]
        audio_file = item["audio_file"]
        audio_dur = item["duration"]
        script = item["script"]
        parts = item["parts"]
        
        output_path = os.path.join(PROJECT_DIR, f"{key}_final.mp4")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Short {key} already exists on disk. Skipping.")
            continue
            
        audio_full_path = os.path.join(PROJECT_DIR, audio_file)
        if audio_dur == 0.0 or not os.path.exists(audio_full_path):
            print(f"[SKIP] Audio track missing or empty for {key}: {audio_full_path}")
            continue
            
        print(f"\nCompiling Short: {key} ({audio_dur:.2f}s) - {title}")
        
        bg_path = os.path.join(CAPSULES_DIR, f"story_{story_num}.jpg")
        base_img = Image.open(bg_path) if os.path.exists(bg_path) else None
        
        temp_dir = os.path.join(PROJECT_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        
        words = script.split()
        total_words = len(words)
        total_frames = int(audio_dur * 30)
        t0 = time.time()
        
        # Choose Ken Burns effect based on part_num
        kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
        effect_type = kb_effects[part_num % len(kb_effects)]
        
        raw_video = os.path.join(temp_dir, "raw_video.mp4")
        
        # Start FFmpeg subprocess to receive raw RGB24 stream on stdin
        cmd_frames = [
            "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
            "-s", "1080x1920", "-r", "30", "-i", "-",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", f"{audio_dur:.2f}",
            raw_video
        ]
        proc = subprocess.Popen(cmd_frames, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        for f_idx in range(total_frames):
            progress = f_idx / total_frames
            curr_time = f_idx / 30.0
            
            # Linear word interpolation
            word_idx = int(curr_time * (total_words / audio_dur))
            word_idx = min(word_idx, total_words - 1)
            
            prev_w = words[word_idx - 1] if word_idx > 0 else ""
            active_w = words[word_idx]
            next_w = words[word_idx + 1] if word_idx < total_words - 1 else ""
            
            badge_text = f"PARTE {part_num} DE 3"
            
            frame_img = draw_vertical_short_frame(
                1080, 1920,
                title, badge_text,
                (prev_w, active_w, next_w),
                font_v_title, font_v_sub, font_v_badge,
                font_v_caption_active, font_v_caption_side,
                base_img, progress, effect_type=effect_type,
                frame_idx=f_idx
            )
            
            # Write raw RGB bytes directly to FFmpeg pipe
            proc.stdin.write(frame_img.tobytes())
            
        # Close pipe and wait for video compilation to finish
        proc.stdin.close()
        proc.wait()
        
        fps_render = total_frames / (time.time() - t0)
        print(f"  Piped and Compiled {total_frames} frames in {time.time()-t0:.1f}s ({fps_render:.1f} FPS)")
        
        # Audio Mix (Speech + bg_music + Whoosh transitional SFX at the start)
        bg_music_file = MUSIC_MAPPING.get(story_num, "Moorland.mp3")
        bg_music_path = os.path.join(MUSIC_DIR, bg_music_file)
        
        audio_mix = "[1:a]volume=1.0[speech];"
        audio_inputs = ["-i", raw_video, "-i", audio_full_path]
        
        # Mix background music
        if os.path.exists(bg_music_path):
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            music_idx = len(audio_inputs) - 1
            audio_mix += f"[{music_idx}:a]volume=-24dB[bg_music];"
            
        # Mix Whoosh SFX
        if os.path.exists(WHOOSH_SFX):
            audio_inputs.extend(["-i", WHOOSH_SFX])
            whoosh_idx = len(audio_inputs) - 1
            audio_mix += f"[{whoosh_idx}:a]volume=-6dB[whoosh];"
            
        if os.path.exists(bg_music_path) and os.path.exists(WHOOSH_SFX):
            audio_mix += "[speech][bg_music]amix=inputs=2:normalize=0[mixed_audio];[mixed_audio][whoosh]amix=inputs=2:normalize=0[a]"
        elif os.path.exists(bg_music_path):
            audio_mix += "[speech][bg_music]amix=inputs=2:normalize=0[a]"
        elif os.path.exists(WHOOSH_SFX):
            audio_mix += "[speech][whoosh]amix=inputs=2:normalize=0[a]"
        else:
            audio_mix += "[speech]anull[a]"
            
        cmd_final = ["ffmpeg", "-y"] + audio_inputs + ["-filter_complex", audio_mix, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-shortest", output_path]
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Cleanup
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
            
        print(f"  [SUCCESS] Compiled vertical short at: {output_path}")

if __name__ == "__main__":
    compile_videos()
