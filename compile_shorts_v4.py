import os
import sys
import math
import struct
import wave
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")

BG_MUSIC_PATH = os.path.join(BASE_DIR, "background_music.mp3")
POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

SHORTS_GAMES_V4 = [
    {
        "key": "cossacks3",
        "appid": 333420,
        "title": "COSSACKS 3",
        "prices": {"usa": "$7.99", "eur": "7,99 €", "latam": "$3.99"},
        "desc": "Batallas de 10.000 Soldados"
    },
    {
        "key": "aoh3",
        "appid": 2772750,
        "title": "AGE OF HISTORY 3",
        "prices": {"usa": "$7.49", "eur": "7,49 €", "latam": "$3.49"},
        "desc": "Gran Estrategia Minimalista"
    },
    {
        "key": "diplomacy_v4",
        "appid": 1272320,
        "title": "DIPLOMACY IS NOT AN OPTION",
        "prices": {"usa": "$19.49", "eur": "19,49 €", "latam": "$9.99"},
        "desc": "Sobrevive a la Horda"
    },
    {
        "key": "anno1404",
        "appid": 1281630,
        "title": "ANNO 1404 HISTORY EDITION",
        "prices": {"usa": "$3.74", "eur": "3,74 €", "latam": "$1.87"},
        "desc": "Mega Gestión Marítima"
    },
    {
        "key": "planetary",
        "appid": 386070,
        "title": "PLANETARY ANNIHILATION: TITANS",
        "prices": {"usa": "$7.49", "eur": "7,49 €", "latam": "$3.74"},
        "desc": "Destrucción Galáctica Total"
    }
]

def generate_sfx_waves():
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
        duration = 0.8
        num_samples = int(duration * 44100)
        for i in range(num_samples):
            t = i / 44100
            freq = 80 + 200 * (t / duration)
            vol = math.sin(math.pi * (t / duration)) ** 2
            val = int(math.sin(2 * math.pi * freq * t) * vol * 18000)
            data = struct.pack('<h', val)
            obj.writeframesraw(data)
        obj.close()

def get_audio_duration(file_path):
    if not os.path.exists(file_path):
        return 0.0
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except:
        return 0.0

def draw_vertical_frame(draw, width, height, title, desc, prices, progress, font_title, font_sub, font_bold, capsule_path_or_img):
    # 1. Background image with slow zoom and Blur
    img_src = None
    if capsule_path_or_img:
        if isinstance(capsule_path_or_img, str):
            if os.path.exists(capsule_path_or_img):
                img_src = Image.open(capsule_path_or_img)
        else:
            img_src = capsule_path_or_img

    if img_src:
        if not hasattr(draw_vertical_frame, "bg_cache") or draw_vertical_frame.bg_cache_src != img_src:
            bg_scale = 1.12
            bg_w = int(width * bg_scale)
            bg_h = int(height * bg_scale)
            img_bg_static = img_src.resize((bg_w, bg_h))
            crop_x = (bg_w - width) // 2
            crop_y = (bg_h - height) // 2
            img_bg_static = img_bg_static.crop((crop_x, crop_y, crop_x + width, crop_y + height))
            img_bg_static = img_bg_static.filter(ImageFilter.GaussianBlur(15))
            overlay = Image.new("RGBA", (width, height), (8, 12, 24, 180))
            draw_vertical_frame.bg_cache = Image.alpha_composite(img_bg_static.convert("RGBA"), overlay)
            draw_vertical_frame.bg_cache_src = img_src
        img_bg = draw_vertical_frame.bg_cache.copy()
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
    draw_img.text((width // 2, header_y + 30), "REBAJAS DE VERANO STEAM", font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, header_y + 70), "RECOMENDACIÓN REGIONAL", font=font_bold, fill=(249, 115, 22, 255), anchor="mm")
    
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
        
        # Sombra de tarjeta
        s_mask = Image.new("L", (card_w + 30, card_h + 30), 0)
        ImageDraw.Draw(s_mask).rounded_rectangle([15, 15, card_w + 15, card_h + 15], radius=20, fill=160)
        s_blur = s_mask.filter(ImageFilter.GaussianBlur(10))
        s_color = Image.new("RGBA", (card_w + 30, card_h + 30), (0, 0, 0, 200))
        img_bg.paste(s_color, (card_x - 15, card_y - 15), mask=s_blur)
        
        draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=20, fill=(13, 20, 38, 220), outline=(255, 255, 255, 30), width=2)
        
        # Display capsule art with shadow inside the card
        img_cap_src = None
        if capsule_path_or_img:
            if isinstance(capsule_path_or_img, str):
                if os.path.exists(capsule_path_or_img):
                    img_cap_src = Image.open(capsule_path_or_img)
            else:
                img_cap_src = capsule_path_or_img

        if img_cap_src:
            cap_img = img_cap_src.resize((360, 540))
            # Round capsule corners
            mask = Image.new("L", (360, 540), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, 360, 540], radius=15, fill=255)
            cap_x = card_x + 60
            cap_y = card_y + 100
            
            c_shadow = Image.new("L", (380, 560), 0)
            ImageDraw.Draw(c_shadow).rounded_rectangle([10, 10, 370, 550], radius=15, fill=180)
            c_blur = c_shadow.filter(ImageFilter.GaussianBlur(10))
            img_bg.paste(Image.new("RGBA", (380, 560), (0,0,0,180)), (cap_x - 10, cap_y - 10), mask=c_blur)
            
            img_bg.paste(cap_img, (cap_x, cap_y), mask=mask)
            # Border around capsule
            draw_img.rounded_rectangle([cap_x, cap_y, cap_x + 360, cap_y + 540], radius=15, outline=(255, 255, 255, 100), width=3)
            
        # Text details
        text_x = card_x + 460
        draw_img.text((text_x, card_y + 220), "ANÁLISIS FLASH", font=font_bold, fill=(249, 115, 22, 255))
        
        # Wrap title
        t_words = title.split()
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
            
        draw_img.text((text_x, ty + 20), desc, font=font_sub, fill=(156, 163, 175, 255))
        
    elif progress < 0.75:
        # State B: Gameplay Video frame (Render placeholder/frame overlay)
        box_w = 900
        box_h = 506
        box_x = (width - box_w) // 2
        box_y = 350
        
        # Draw dynamic monitor bezels
        draw_img.rounded_rectangle([box_x - 15, box_y - 15, box_x + box_w + 15, box_y + box_h + 15], radius=16, fill=(17, 24, 39, 255), outline=(249, 115, 22, 255), width=3)
        draw_img.rectangle([box_x, box_y, box_x + box_w, box_y + box_h], fill=(0, 0, 0, 255))
        
        # Title of the game overlayed nicely at the bottom of the screen
        card_w = 900
        card_h = 420
        card_x = (width - card_w) // 2
        card_y = 900
        
        s_mask = Image.new("L", (card_w + 20, card_h + 20), 0)
        ImageDraw.Draw(s_mask).rounded_rectangle([10, 10, card_w + 10, card_h + 10], radius=16, fill=160)
        s_blur = s_mask.filter(ImageFilter.GaussianBlur(8))
        img_bg.paste(Image.new("RGBA", (card_w + 20, card_h + 20), (0,0,0,200)), (card_x - 10, card_y - 10), mask=s_blur)
        
        draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=16, fill=(13, 20, 38, 220), outline=(255, 255, 255, 30), width=2)
        
        # Regional prices labels
        draw_img.text((width // 2, card_y + 40), f"PRECIOS DE OFERTA EN REGIONES", font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
        draw_img.line([width // 2 - 150, card_y + 75, width // 2 + 150, card_y + 75], fill=(249, 115, 22, 255), width=3)
        
        # Draw Flag Pills with modern rounded cards
        px = card_x + 60
        py = card_y + 110
        pill_w = 780
        pill_h = 75
        
        # USA Pill
        draw_img.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=12, fill=(30, 41, 59, 180), outline=(255, 255, 255, 20), width=1)
        draw_img.text((px + 30, py + 22), "🇺🇸 USA (Precio Base):", font=font_sub, fill=(243, 244, 246, 255))
        draw_img.text((px + pill_w - 30, py + 22), prices["usa"], font=font_bold, fill=(255, 255, 255, 255), anchor="rt")
        
        # EUR Pill
        py += 95
        draw_img.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=12, fill=(30, 41, 59, 180), outline=(255, 255, 255, 20), width=1)
        draw_img.text((px + 30, py + 22), "🇪🇺 EUR (Europa):", font=font_sub, fill=(243, 244, 246, 255))
        draw_img.text((px + pill_w - 30, py + 22), prices["eur"], font=font_bold, fill=(255, 255, 255, 255), anchor="rt")
        
        # LATAM Pill
        py += 95
        draw_img.rounded_rectangle([px, py, px + pill_w, py + pill_h], radius=12, fill=(13, 148, 136, 180), outline=(255, 255, 255, 30), width=1)
        draw_img.text((px + 30, py + 22), "🌎 LATAM (Ajuste Regional):", font=font_sub, fill=(204, 251, 241, 255))
        draw_img.text((px + pill_w - 30, py + 22), prices["latam"], font=font_bold, fill=(52, 211, 153, 255), anchor="rt")
        
    else:
        # State C: Outro & Call to Action (CTA)
        card_w = 900
        card_h = 750
        card_x = (width - card_w) // 2
        card_y = 350
        
        s_mask = Image.new("L", (card_w + 25, card_h + 25), 0)
        ImageDraw.Draw(s_mask).rounded_rectangle([12, 12, card_w + 12, card_h + 12], radius=24, fill=170)
        s_blur = s_mask.filter(ImageFilter.GaussianBlur(10))
        img_bg.paste(Image.new("RGBA", (card_w + 25, card_h + 25), (0,0,0,220)), (card_x - 12, card_y - 12), mask=s_blur)
        
        draw_img.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=24, fill=(13, 20, 38, 220), outline=(255, 255, 255, 30), width=2)
        
        # Draw Outro details
        draw_img.text((width // 2, card_y + 140), "¡NO TE PIERDAS ESTA COMPRA!", font=font_bold, fill=(249, 115, 22, 255), anchor="mm")
        draw_img.text((width // 2, card_y + 220), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
        
        # Wrap CTA instructions
        cta_words = "¿Vas a agregar esta joya de la estrategia a tu biblioteca de Steam?".split()
        cta_lines = []
        curr = []
        for w in cta_words:
            if len(" ".join(curr + [w])) < 28:
                curr.append(w)
            else:
                cta_lines.append(" ".join(curr))
                curr = [w]
        if curr:
            cta_lines.append(" ".join(curr))
            
        cy = card_y + 310
        for l in cta_lines:
            draw_img.text((width // 2, cy), l, font=font_sub, fill=(156, 163, 175, 255), anchor="mm")
            cy += 50
            
        # Draw subscription button (Pulsing sinusoidally)
        pulse_scale = 1.0 + 0.04 * math.sin(progress * 40 * math.pi)
        btn_w = int(580 * pulse_scale)
        btn_h = int(100 * pulse_scale)
        btn_x = width // 2 - btn_w // 2
        btn_y = card_y + 490
        
        b_shadow = Image.new("L", (btn_w + 15, btn_h + 15), 0)
        ImageDraw.Draw(b_shadow).rounded_rectangle([7, 7, btn_w + 7, btn_h + 7], radius=15, fill=160)
        b_blur = b_shadow.filter(ImageFilter.GaussianBlur(6))
        img_bg.paste(Image.new("RGBA", (btn_w + 15, btn_h + 15), (0,0,0,180)), (btn_x - 7, btn_y - 7), mask=b_blur)
        
        draw_img.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=15, fill=(220, 38, 38, 255), outline=(255, 255, 255, 255), width=3)
        draw_img.text((width // 2, btn_y + btn_h // 2), "¡SUSCRÍBETE AHORA!", font=font_bold, fill=(255, 255, 255, 255), anchor="mm")
        
    return img_bg.convert("RGB")

def compile_vertical_short(game):
    key = game["key"]
    appid = game["appid"]
    title = game["title"]
    prices = game["prices"]
    desc = game["desc"]
    
    output_path = os.path.join(BASE_DIR, f"{key}_v4_short.mp4")
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
    img_capsule = Image.open(capsule_path) if os.path.exists(capsule_path) else None
    for f_idx in range(total_frames):
        progress = f_idx / total_frames
        frame_img = draw_vertical_frame(
            None, width, height, title, desc, prices, progress, font_title, font_sub, font_bold, img_capsule
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
    
    # Overlay gameplay video in central box during 0.25 to 0.75 progress
    final_video_only = os.path.join(temp_dir, "video_only.mp4")
    trailer_dur = get_audio_duration(trailer_path) if os.path.exists(trailer_path) else 0.0
    
    if trailer_dur > 15.0:
        start_t = 0.25 * audio_dur
        end_t = 0.75 * audio_dur
        overlay_dur = end_t - start_t
        
        # Crop/slice gameplay segment
        gameplay_clip = os.path.join(temp_dir, "gameplay_clip.mp4")
        
        # Slice gameplay starting 10s into the trailer
        cmd_slice = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-ss", f"{10.0:.2f}",
            "-i", trailer_path,
            "-t", f"{overlay_dur:.2f}",
            "-vf", "scale=900:506:force_original_aspect_ratio=decrease,pad=900:506:(ow-iw)/2:(oh-ih)/2,setsar=1",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
            gameplay_clip
        ]
        subprocess.run(cmd_slice, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
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
        subprocess.run(cmd_overlay, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        final_video_only = base_video
        
    # Audio track assembly: mix voiceover, pop SFX, whoosh SFX, and background music
    audio_inputs = ["-i", final_video_only, "-i", audio_path]
    audio_mix_filter = "[1:a]volume=1.0[speech];"
    
    use_bg = os.path.exists(BG_MUSIC_PATH)
    if use_bg:
        audio_inputs.extend(["-stream_loop", "-1", "-i", BG_MUSIC_PATH])
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
    print("KINESIO Shorts v4 Compilation Suite")
    print("====================================================")
    
    generate_sfx_waves()
    
    for game in SHORTS_GAMES_V4:
        try:
            compile_vertical_short(game)
        except Exception as e:
            print(f"  [ERROR] Failed to compile Short for {game['title']}: {e}")
            
    print("\n====================================================")
    print("Shorts v4 compilation complete!")
    print("====================================================")

if __name__ == "__main__":
    main()
