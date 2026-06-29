import os
import sys
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

BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")

BG_MUSIC_PATH = os.path.join(BASE_DIR, "music", "Severe Tire Damage.mp3") # High energy rock for GTA
POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

SHORTS_DATA = [
    {
        "key": "gta6_short_1",
        "title": "GTA VI: LANZAMIENTO",
        "desc": "¡GTA 6 CAMBIARÁ LA HISTORIA! 🎮",
        "hook": "¡EL JUEGO MÁS GRANDE DE LA HISTORIA!"
    },
    {
        "key": "gta6_short_2",
        "title": "GTA VI: FILTRACIONES",
        "desc": "¡LAS FILTRACIONES DE GTA 6! 🚨",
        "hook": "¡EL HACKEO MÁS BRUTAL A ROCKSTAR!"
    },
    {
        "key": "gta6_short_3",
        "title": "GTA VI: RETRASOS",
        "desc": "¿RETRASADO HASTA 2026? 📅",
        "hook": "¡RUMORES DE RETRASO OFICIAL!"
    },
    {
        "key": "gta6_short_4",
        "title": "GTA VI: EL PRECIO",
        "desc": "¿GTA 6 A $150 DÓLARES? 💸",
        "hook": "¡TODA LA VERDAD SOBRE EL PRECIO!"
    },
    {
        "key": "gta6_short_5",
        "title": "GTA VI: EL CATACLISMO",
        "desc": "EL EFECTO DESTRUCTOR DE GTA 6 💥",
        "hook": "¡NINGÚN JUEGO QUIERE COMPETIRLE!"
    }
]

def split_into_phrases(text):
    """Splits a paragraph into short, punchy 2-4 word phrases for dynamic subtitles."""
    words = text.split()
    phrases = []
    chunk_size = 3
    for i in range(0, len(words), chunk_size):
        phrase = " ".join(words[i:i+chunk_size]).strip().upper()
        # Clean special chars for drawing
        phrase = re.sub(r'[¿?¡!.,]', '', phrase)
        phrases.append(phrase)
    return phrases

def get_audio_duration(path):
    if not os.path.exists(path):
        return 0.0
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except:
        return 0.0

def create_dynamic_gameplay_sequence():
    """Cuts and stitches 6 high-action scenes from the GTA 6 trailer to make it feel alive."""
    trailer_path = os.path.join(TRAILERS_DIR, "gta6_trailer.mp4")
    seq_output = os.path.join(TRAILERS_DIR, "gta6_dynamic_gameplay.mp4")
    
    if os.path.exists(seq_output) and os.path.getsize(seq_output) > 0:
        return seq_output
        
    print("Preparing high-action gameplay cuts from GTA 6 trailer...")
    cuts = [
        "3.00",   # Bridge/Highway Vice City
        "14.00",  # Beach/Pool Party
        "28.00",  # Strip Club / Neon Lights
        "37.00",  # Mud Wrestling truck drift
        "52.00",  # Lucia and Jason driving fast
        "73.00"   # Store Robbery Standoff
    ]
    
    temp_cuts_dir = os.path.join(BASE_DIR, "temp_gta_cuts")
    os.makedirs(temp_cuts_dir, exist_ok=True)
    
    cut_files = []
    for idx, ss in enumerate(cuts):
        cut_file = os.path.join(temp_cuts_dir, f"cut_{idx}.mp4")
        # Cut 10 seconds per scene, scale and pad to 900x506
        cmd = [
            "ffmpeg", "-y",
            "-ss", ss,
            "-i", trailer_path,
            "-t", "10",
            "-vf", "scale=900:506:force_original_aspect_ratio=decrease,pad=900:506:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
            cut_file
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(cut_file) and os.path.getsize(cut_file) > 0:
            cut_files.append(cut_file)
            
    # Concatenate the cuts
    concat_txt = os.path.join(temp_cuts_dir, "concat.txt")
    with open(concat_txt, "w") as f:
        for cf in cut_files:
            f.write(f"file '{cf}'\n")
            
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-c", "copy",
        seq_output
    ]
    subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    try:
        shutil.rmtree(temp_cuts_dir)
    except:
        pass
        
    return seq_output

def draw_vertical_frame(draw, width, height, title, phrase, hook, progress, font_title, font_sub, font_bold, font_subtitles, capsule_path_or_img):
    img_src = None
    if capsule_path_or_img:
        if isinstance(capsule_path_or_img, str):
            if os.path.exists(capsule_path_or_img):
                img_src = Image.open(capsule_path_or_img)
        else:
            img_src = capsule_path_or_img

    if img_src:
        if not hasattr(draw_vertical_frame, "bg_cache") or draw_vertical_frame.bg_cache_src != img_src:
            bg_scale = 1.15
            bg_w = int(width * bg_scale)
            bg_h = int(height * bg_scale)
            img_bg_static = img_src.resize((bg_w, bg_h))
            crop_x = (bg_w - width) // 2
            crop_y = (bg_h - height) // 2
            img_bg_static = img_bg_static.crop((crop_x, crop_y, crop_x + width, crop_y + height))
            img_bg_static = img_bg_static.filter(ImageFilter.GaussianBlur(15))
            overlay = Image.new("RGBA", (width, height), (12, 10, 24, 190))
            draw_vertical_frame.bg_cache = Image.alpha_composite(img_bg_static.convert("RGBA"), overlay)
            draw_vertical_frame.bg_cache_src = img_src
        img_bg = draw_vertical_frame.bg_cache.copy()
    else:
        img_bg = Image.new("RGBA", (width, height), (15, 10, 30, 255))
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Border vignette
    draw_img.rectangle([0, 0, width, height], outline=(0, 0, 0, 160), width=65)
    
    # 1. Top Header (GTA VI Themed Neon Border)
    header_w = 920
    header_h = 110
    header_x = (width - header_w) // 2
    header_y = 60
    
    # Glassmorphism panel with neon outline (pink/orange glow)
    draw_img.rounded_rectangle([header_x, header_y, header_x + header_w, header_y + header_h], radius=15, fill=(13, 20, 38, 220), outline=(244, 63, 94, 120), width=3) # Neon pink border
    draw_img.text((width // 2, header_y + 35), "GRAND THEFT AUTO VI", font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, header_y + 75), title, font=font_bold, fill=(244, 63, 94, 255), anchor="mm") # Bright pink-red title
    
    # Progress line below header
    bar_width = header_w
    bar_fill = int(bar_width * progress)
    draw_img.rounded_rectangle([header_x, header_y + header_h + 10, header_x + bar_width, header_y + header_h + 14], radius=2, fill=(30, 41, 59, 255))
    draw_img.rounded_rectangle([header_x, header_y + header_h + 10, header_x + bar_fill, header_y + header_h + 14], radius=2, fill=(249, 115, 22, 255)) # Orange progress
    
    # 2. Main Center Box for Gameplay
    box_w = 900
    box_h = 506
    box_x = (width - box_w) // 2
    box_y = 350
    
    # Monitor border (thick slate gray with orange neon accent)
    draw_img.rounded_rectangle([box_x - 15, box_y - 15, box_x + box_w + 15, box_y + box_h + 15], radius=16, fill=(17, 24, 39, 255), outline=(249, 115, 22, 220), width=4)
    draw_img.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill=(0, 0, 0, 255))
    
    # 3. First 3 Seconds Hook Badge Overlay!
    if progress < 0.08: # First 4.5 seconds
        badge_w = 780
        badge_h = 90
        badge_x = (width - badge_w) // 2
        badge_y = box_y + 50
        
        # Red flashing badge
        draw_img.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=16, fill=(225, 29, 72, 240), outline=(255, 255, 255, 255), width=3)
        draw_img.text((width // 2, badge_y + badge_h // 2), hook, font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
        
    # 4. Animated Subtitle captions in the center (Viral style)
    text_y = 1020
    if phrase:
        # Draw heavy drop shadow / outline to make it readable over gameplay
        outline_range = 3
        for dx in range(-outline_range, outline_range+1):
            for dy in range(-outline_range, outline_range+1):
                if dx != 0 or dy != 0:
                    draw_img.text((width // 2 + dx, text_y + dy), phrase, font=font_subtitles, fill=(0, 0, 0, 255), anchor="mm")
        
        # Flashing color logic: alternate color for visual punch!
        color = (255, 255, 255, 255) # White
        if len(phrase) % 2 == 0:
            color = (253, 224, 71, 255) # Bright Yellow
            
        draw_img.text((width // 2, text_y), phrase, font=font_subtitles, fill=color, anchor="mm")
        
    # 5. Call to Action Panel at the bottom
    cta_y = 1150
    cta_w = 900
    cta_h = 650
    cta_x = (width - cta_w) // 2
    
    # Card layout
    draw_img.rounded_rectangle([cta_x, cta_y, cta_x + cta_w, cta_y + cta_h], radius=24, fill=(13, 20, 38, 220), outline=(244, 63, 94, 60), width=2)
    
    # Display logo
    logo_y = cta_y + 160
    draw_img.rounded_rectangle([width//2 - 95, logo_y - 65, width//2 + 95, logo_y + 65], radius=20, fill=(244, 63, 94, 255))
    draw_img.polygon([(width//2 - 25, logo_y - 30), (width//2 - 25, logo_y + 30), (width//2 + 35, logo_y)], fill=(255, 255, 255, 255))
    
    draw_img.text((width // 2, cta_y + 340), "SUSCRÍBETE A @dominus8735", font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, cta_y + 420), "¡PARA MÁS NOTICIAS DE GTA VI!", font=font_sub, fill=(156, 163, 175, 255), anchor="mm")
    
    # Floating interactive sticker at the very bottom
    draw_img.rounded_rectangle([cta_x + 50, cta_y + 510, cta_x + cta_w - 50, cta_y + 580], radius=12, fill=(249, 115, 22, 200))
    draw_img.text((width // 2, cta_y + 545), "🔔 ACTIVA LA CAMPANITA DE NOTIFICACIONES", font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
    
    return img_bg.convert("RGB")

def compile_gta6_short(short_obj, gameplay_seq):
    key = short_obj["key"]
    title = short_obj["title"]
    desc = short_obj["desc"]
    hook = short_obj["hook"]
    
    output_path = os.path.join(BASE_DIR, f"{key}_short.mp4")
    audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
    capsule_path = os.path.join(CAPSULES_DIR, "gta6_capsule.jpg")
    
    # Read script to split into phrases
    script_file = os.path.join(BASE_DIR, "scripts_shorts_gta6.md")
    # Parse text
    with open(script_file, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split(f"### {key}")
    text_block = parts[1].strip().split("---")[0].strip()
    
    phrases = split_into_phrases(text_block)
    
    print(f"\nCompiling GTA VI Short: {desc} ({key})")
    audio_dur = get_audio_duration(audio_path)
    if audio_dur == 0.0:
        print(f"  [ERROR] Audio file missing or empty: {audio_path}")
        return
        
    temp_dir = os.path.join(BASE_DIR, f"temp_gta_{key}")
    os.makedirs(temp_dir, exist_ok=True)
    
    width, height = 1080, 1920
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 45)
    font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 40)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 32)
    
    # Bold heavy font for subtitles (flashing impact style!)
    font_subtitles = ImageFont.truetype("C:\\Windows\\Fonts\\impact.ttf", 75)
    
    total_frames = int(audio_dur * 30)
    img_capsule = Image.open(capsule_path) if os.path.exists(capsule_path) else None
    
    for f_idx in range(total_frames):
        progress = f_idx / total_frames
        
        # Calculate active subtitle phrase
        p_idx = min(int(progress * len(phrases)), len(phrases) - 1)
        phrase = phrases[p_idx]
        
        frame_img = draw_vertical_frame(
            None, width, height, title, phrase, hook, progress, font_title, font_sub, font_bold, font_subtitles, img_capsule
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
    
    # Overlay gameplay video in the center box
    if os.path.exists(gameplay_seq):
        final_video_only = os.path.join(temp_dir, "final_video_only.mp4")
        # Start and end timestamps for the gameplay window (fits nicely between 10% and 90% progress)
        start_t = 0.08 * audio_dur
        end_t = 0.92 * audio_dur
        overlay_dur = end_t - start_t
        
        # Slice gameplay sequence
        gameplay_clip = os.path.join(temp_dir, "gameplay_clip.mp4")
        cmd_slice = [
            "ffmpeg", "-y",
            "-ss", "0.00",
            "-i", gameplay_seq,
            "-t", f"{overlay_dur:.2f}",
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
    
    use_bg = os.path.exists(BG_MUSIC_PATH)
    if use_bg:
        audio_inputs.extend(["-stream_loop", "-1", "-i", BG_MUSIC_PATH])
        audio_mix_filter += "[2:a]volume=-24dB[bg_music];"
        
    sfx_available = os.path.exists(POP_SFX) and os.path.exists(WHOOSH_SFX)
    if sfx_available:
        p_idx = 3 if use_bg else 2
        w_idx = 4 if use_bg else 3
        audio_inputs.extend(["-i", POP_SFX, "-i", WHOOSH_SFX])
        
        # Flash SFX during phrase transitions
        # We can add pop sounds at 15% and 50% and whoosh at start and end
        audio_mix_filter += (
            f"[{p_idx}:a]asplit=2[p0][p1];"
            f"[{w_idx}:a]asplit=2[w0][w1];"
            f"[p0]adelay={int(0.20*audio_dur*1000)}|{int(0.20*audio_dur*1000)}[pd0];"
            f"[p1]adelay={int(0.60*audio_dur*1000)}|{int(0.60*audio_dur*1000)}[pd1];"
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
        "-c:v", "libx264",
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
    print("GTA VI Shorts Compiler Suite")
    print("====================================================")
    
    gameplay_seq = create_dynamic_gameplay_sequence()
    
    for short_obj in SHORTS_DATA:
        try:
            compile_gta6_short(short_obj, gameplay_seq)
        except Exception as e:
            print(f"  [ERROR] Failed to compile Short {short_obj['key']}: {e}")
            
    print("\n====================================================")
    print("GTA VI Compilation suite completed!")
    print("====================================================")

if __name__ == "__main__":
    main()
