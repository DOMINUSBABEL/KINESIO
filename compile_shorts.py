import os
import sys
import math
import shutil
import subprocess
import urllib.request
import wave
import struct
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Reconfigure terminal output to UTF-8 to prevent encoding issues on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Paths setup
BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
BG_PATH = os.path.join(BASE_DIR, "background.jpg")
FONT_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
BG_MUSIC_PATH = os.path.join(BASE_DIR, "background_music.mp3")

# Background music URL
BG_MUSIC_URL = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"

# Games data
RTS_GAMES = [
    {
        "title": "Age of Empires IV",
        "capsule": "age_of_empires_iv_1466860.jpg",
        "discount": "-65%",
        "price": "AHORA $13.99 | ANTES $39.99"
    },
    {
        "title": "Company of Heroes 3",
        "capsule": "company_of_heroes_3_1675900.jpg",
        "discount": "-60%",
        "price": "AHORA $23.99 | ANTES $59.99"
    },
    {
        "title": "Dune: Spice Wars",
        "capsule": "dune_spice_wars_1171690.jpg",
        "discount": "-60%",
        "price": "AHORA $15.99 | ANTES $39.99"
    },
    {
        "title": "Age of Mythology: Retold",
        "capsule": "age_of_mythology_retold_1934680.jpg",
        "discount": "-50%",
        "price": "AHORA $14.99 | ANTES $29.99"
    },
    {
        "title": "Sins of a Solar Empire II",
        "capsule": "sins_of_a_solar_empire_ii_1575940.jpg",
        "discount": "-50%",
        "price": "AHORA $19.99 | ANTES $39.99"
    }
]

CITY_GAMES = [
    {
        "title": "Against the Storm",
        "capsule": "against_the_storm_1336490.jpg",
        "discount": "-70%",
        "price": "AHORA $8.99 | ANTES $29.99"
    },
    {
        "title": "Frostpunk 2",
        "capsule": "frostpunk_2_1601580.jpg",
        "discount": "-50%",
        "price": "AHORA $22.49 | ANTES $44.99"
    },
    {
        "title": "Farthest Frontier",
        "capsule": "farthest_frontier_1044720.jpg",
        "discount": "-50%",
        "price": "AHORA $14.99 | ANTES $29.99"
    },
    {
        "title": "Manor Lords",
        "capsule": "manor_lords_1363080.jpg",
        "discount": "-35%",
        "price": "AHORA $25.99 | ANTES $39.99"
    },
    {
        "title": "Satisfactory",
        "capsule": "satisfactory_526870.jpg",
        "discount": "-30%",
        "price": "AHORA $27.99 | ANTES $39.99"
    }
]

ARPG_GAMES = [
    {
        "title": "The Witcher 3: Wild Hunt",
        "capsule": "the_witcher_3_292030.jpg",
        "discount": "-90%",
        "price": "AHORA $3.99 | ANTES $39.99"
    },
    {
        "title": "Grim Dawn",
        "capsule": "grim_dawn_219990.jpg",
        "discount": "-90%",
        "price": "AHORA $2.49 | ANTES $24.99"
    },
    {
        "title": "Monster Hunter: World",
        "capsule": "monster_hunter_world_582010.jpg",
        "discount": "-74%",
        "price": "AHORA $7.79 | ANTES $29.99"
    },
    {
        "title": "Cyberpunk 2077",
        "capsule": "cyberpunk_2077_1091500.jpg",
        "discount": "-70%",
        "price": "AHORA $17.99 | ANTES $59.99"
    },
    {
        "title": "Diablo IV",
        "capsule": "diablo_iv_2344520.jpg",
        "discount": "-40%",
        "price": "AHORA $29.99 | ANTES $49.99"
    }
]

# Audio duration probe
def get_audio_duration(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(result.stdout.strip())

# SFX Generator (whoosh.wav and pop.wav)
def generate_sfx_files():
    whoosh_path = os.path.join(BASE_DIR, "whoosh.wav")
    pop_path = os.path.join(BASE_DIR, "pop.wav")
    
    if os.path.exists(whoosh_path) and os.path.exists(pop_path):
        print("SFX files (whoosh.wav and pop.wav) already exist.")
        return True
        
    print("Generating SFX files (whoosh.wav, pop.wav) programmatically...")
    sr = 44100
    
    # 1. Whoosh.wav (stereo, 0.5s duration)
    whoosh_samples = int(sr * 0.5)
    try:
        with wave.open(whoosh_path, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(sr)
            for i in range(whoosh_samples):
                t = i / sr
                freq = 150 + 300 * (t / 0.5)
                angle = 2 * math.pi * freq * t
                sine_val = math.sin(angle)
                noise_val = random.uniform(-1.0, 1.0)
                val = 0.3 * sine_val + 0.7 * noise_val
                env = math.sin(math.pi * (t / 0.5))
                sample = int(val * env * 12000)
                wav.writeframes(struct.pack('<hh', sample, sample))
                
        # 2. Pop.wav (stereo, 0.15s duration)
        pop_samples = int(sr * 0.15)
        with wave.open(pop_path, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(sr)
            for i in range(pop_samples):
                t = i / sr
                freq = 600 * math.exp(-15 * t) + 200
                phase = 2 * math.pi * (-40 * math.exp(-15 * t) + 200 * t)
                sine_val = math.sin(phase)
                env = math.exp(-20 * t)
                sample = int(sine_val * env * 24000)
                wav.writeframes(struct.pack('<hh', sample, sample))
                
        print("SFX files generated successfully!")
        return True
    except Exception as e:
        print(f"Error generating SFX files: {e}")
        return False

# Background music downloader
def download_bg_music():
    if os.path.exists(BG_MUSIC_PATH) and os.path.getsize(BG_MUSIC_PATH) > 0:
        print("Background music already present.")
        return True
    
    print(f"Downloading background music from: {BG_MUSIC_URL}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    req = urllib.request.Request(BG_MUSIC_URL, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            with open(BG_MUSIC_PATH, 'wb') as out_file:
                out_file.write(response.read())
        print("Background music downloaded successfully!")
        return True
    except Exception as e:
        print(f"Failed to download background music: {e}. Compilation will use voiceover only.")
        if os.path.exists(BG_MUSIC_PATH):
            try:
                os.remove(BG_MUSIC_PATH)
            except Exception:
                pass
        return False

# Drawing helpers
def draw_centered_text(draw, text, center_x, center_y, font_path, base_size, fill_color, max_width=900):
    size = base_size
    font = ImageFont.truetype(font_path, size)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    while w > max_width and size > 16:
        size -= 2
        font = ImageFont.truetype(font_path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
    x = center_x - w / 2
    y = center_y - h / 2
    # Draw drop shadow for contrast
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 160))
    draw.text((x, y), text, font=font, fill=fill_color)

def get_bounce_scale(frame_offset):
    if frame_offset < 0:
        return 0.0
    if frame_offset >= 15:
        return 1.0
    t = frame_offset / 15.0
    # Over shoot bounce curve: 0 to 1.2 then settle at 1.0
    if t < 0.7:
        return 1.2 * (t / 0.7)
    else:
        return 1.2 - 0.2 * ((t - 0.7) / 0.3)

def render_scaled_capsule(capsule_base, scale):
    w = int(540 * scale)
    h = int(810 * scale)
    if w <= 0 or h <= 0:
        return None, (540, 785, 540, 785)
    
    capsule_scaled = capsule_base.resize((w, h), Image.Resampling.LANCZOS)
    
    # Rounded corners using alpha mask
    mask = Image.new('L', (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, w, h), radius=int(20 * scale), fill=255)
    capsule_scaled.putalpha(mask)
    
    # Centered at X = 540, Y = 785
    x0 = 540 - w // 2
    y0 = 785 - h // 2
    x1 = x0 + w
    y1 = y0 + h
    
    return capsule_scaled, (x0, y0, x1, y1)

def draw_header(draw, font_path):
    # Sleek rounded translucent black rectangle
    draw.rounded_rectangle((80, 80, 1000, 220), radius=30, fill=(0, 0, 0, 165), outline=(255, 255, 255, 45), width=2)
    # Header Title
    draw_centered_text(draw, "OFERTAS DE VERANO", 540, 125, font_path, 34, (255, 255, 255, 255))
    # Subtitle
    draw_centered_text(draw, "STEAM 2026", 540, 175, font_path, 22, (255, 106, 0, 255))

def draw_progress_bar(draw, frame_idx, total_frames, y_pos=232, height=12):
    progress = frame_idx / max(1, total_frames - 1)
    w = int(progress * 920) # Max width is 920px (from X=80 to X=1000)
    
    # Progress track background
    draw.rounded_rectangle((80, y_pos, 1000, y_pos + height), radius=height//2, fill=(40, 40, 40, 160))
    
    if w > 0:
        glow_x0, glow_x1 = 80, 80 + w
        # Simulated glow layers
        draw.rounded_rectangle((glow_x0, y_pos - 4, glow_x1, y_pos + height + 4), radius=(height+8)//2, fill=(255, 106, 0, 50))
        draw.rounded_rectangle((glow_x0, y_pos - 2, glow_x1, y_pos + height + 2), radius=(height+4)//2, fill=(255, 106, 0, 120))
        draw.rounded_rectangle((glow_x0, y_pos, glow_x1, y_pos + height), radius=height//2, fill=(255, 106, 0, 255))

def get_shot_info(frame_idx, total_frames, games_list, cta_title, cta_subtitle):
    """
    Splits frames at 30 fps:
    - Shot 0: 0.0s - 3.0s (0 to 89)
    - Shot 1: 3.0s - 8.0s (90 to 239)
    - Shot 2: 8.0s - 12.0s (240 to 359)
    - Shot 3: 12.0s - 16.0s (360 to 479)
    - Shot 4: 16.0s - 20.0s (480 to 599)
    - Shot 5: 20.0s - 24.0s (600 to 719)
    - Shot 6: 24.0s - end (720 to end)
    """
    if frame_idx < 90:
        return 'intro', 0, 90, None
    elif frame_idx < 240:
        return 'game', 90, 240, games_list[0]
    elif frame_idx < 360:
        return 'game', 240, 360, games_list[1]
    elif frame_idx < 480:
        return 'game', 360, 480, games_list[2]
    elif frame_idx < 600:
        return 'game', 480, 600, games_list[3]
    elif frame_idx < 720:
        return 'game', 600, 720, games_list[4]
    else:
        return 'outro', 720, total_frames, (cta_title, cta_subtitle)

def compile_video_with_ffmpeg(temp_dir, audio_path, output_path, bg_music_path):
    whoosh_wav = os.path.join(BASE_DIR, "whoosh.wav")
    pop_wav = os.path.join(BASE_DIR, "pop.wav")
    
    sfx_available = os.path.exists(whoosh_wav) and os.path.exists(pop_wav)
    use_bg = bg_music_path and os.path.exists(bg_music_path) and os.path.getsize(bg_music_path) > 0
    
    if sfx_available:
        print("SFX files found. Mixing sound effects into video...")
        if use_bg:
            filter_complex = (
                "[3:a]asplit=6[w0][w1][w2][w3][w4][w5];"
                "[4:a]asplit=5[p0][p1][p2][p3][p4];"
                "[w0]adelay=3000|3000[wd0];"
                "[w1]adelay=8000|8000[wd1];"
                "[w2]adelay=12000|12000[wd2];"
                "[w3]adelay=16000|16000[wd3];"
                "[w4]adelay=20000|20000[wd4];"
                "[w5]adelay=24000|24000[wd5];"
                "[p0]adelay=3300|3300[pd0];"
                "[p1]adelay=8300|8300[pd1];"
                "[p2]adelay=12300|12300[pd2];"
                "[p3]adelay=16300|16300[pd3];"
                "[p4]adelay=20300|20300[pd4];"
                "[wd0][wd1][wd2][wd3][wd4][wd5][pd0][pd1][pd2][pd3][pd4]amix=inputs=11:normalize=0[sfx_raw];"
                "[sfx_raw]volume=-8dB[sfx];"
                "[1:a]volume=1.0[vo];"
                "[2:a]volume=-22dB[bg];"
                "[vo][bg][sfx]amix=inputs=3:duration=first:dropout_transition=0[a]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-f", "image2",
                "-framerate", "30",
                "-i", os.path.join(temp_dir, "frame_%05d.png"),
                "-i", audio_path,
                "-ss", "15",
                "-i", bg_music_path,
                "-i", whoosh_wav,
                "-i", pop_wav,
                "-filter_complex", filter_complex,
                "-map", "0:v",
                "-map", "[a]",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]
        else:
            filter_complex = (
                "[2:a]asplit=6[w0][w1][w2][w3][w4][w5];"
                "[3:a]asplit=5[p0][p1][p2][p3][p4];"
                "[w0]adelay=3000|3000[wd0];"
                "[w1]adelay=8000|8000[wd1];"
                "[w2]adelay=12000|12000[wd2];"
                "[w3]adelay=16000|16000[wd3];"
                "[w4]adelay=20000|20000[wd4];"
                "[w5]adelay=24000|24000[wd5];"
                "[p0]adelay=3300|3300[pd0];"
                "[p1]adelay=8300|8300[pd1];"
                "[p2]adelay=12300|12300[pd2];"
                "[p3]adelay=16300|16300[pd3];"
                "[p4]adelay=20300|20300[pd4];"
                "[wd0][wd1][wd2][wd3][wd4][wd5][pd0][pd1][pd2][pd3][pd4]amix=inputs=11:normalize=0[sfx_raw];"
                "[sfx_raw]volume=-8dB[sfx];"
                "[1:a]volume=1.0[vo];"
                "[vo][sfx]amix=inputs=2:duration=first:dropout_transition=0[a]"
            )
            cmd = [
                "ffmpeg", "-y",
                "-f", "image2",
                "-framerate", "30",
                "-i", os.path.join(temp_dir, "frame_%05d.png"),
                "-i", audio_path,
                "-i", whoosh_wav,
                "-i", pop_wav,
                "-filter_complex", filter_complex,
                "-map", "0:v",
                "-map", "[a]",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]
    else:
        print("SFX files not found or disabled. Compiling with voiceover/music only...")
        if use_bg:
            cmd = [
                "ffmpeg", "-y",
                "-f", "image2",
                "-framerate", "30",
                "-i", os.path.join(temp_dir, "frame_%05d.png"),
                "-i", audio_path,
                "-ss", "15",
                "-i", bg_music_path,
                "-filter_complex", "[1:a]volume=1.0[vo];[2:a]volume=-22dB[bg];[vo][bg]amix=inputs=2:duration=first:dropout_transition=0[a]",
                "-map", "0:v",
                "-map", "[a]",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]
        else:
            cmd = [
                "ffmpeg", "-y",
                "-f", "image2",
                "-framerate", "30",
                "-i", os.path.join(temp_dir, "frame_%05d.png"),
                "-i", audio_path,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-shortest",
                output_path
            ]
            
    print(f"Running FFmpeg: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("FFmpeg Error:")
        print(result.stderr)
        return False
    return True

def process_short(short_id, name, audio_filename, games_list, intro_title, intro_subtitle, cta_title, cta_subtitle):
    print(f"\n==================================================")
    print(f"Starting rendering process for: {name}")
    print(f"==================================================")
    
    audio_path = os.path.join(BASE_DIR, audio_filename)
    output_path = os.path.join(BASE_DIR, f"{short_id}_short.mp4")
    temp_dir = os.path.join(BASE_DIR, f"temp_frames_{short_id.lower()}_{os.getpid()}")
    
    # 1. Check audio duration
    try:
        duration = get_audio_duration(audio_path)
        print(f"Audio duration: {duration:.3f} seconds")
    except Exception as e:
        print(f"Error checking audio duration: {e}")
        return False
        
    total_frames = int(duration * 30.0)
    print(f"Total frames to render: {total_frames} (at 30 fps)")
    
    # 2. Setup background bases
    if not os.path.exists(BG_PATH):
        raise FileNotFoundError(f"Background image not found: {BG_PATH}")
        
    bg_img = Image.open(BG_PATH).convert('RGBA')
    bg_img = bg_img.resize((1080, 1920), Image.Resampling.LANCZOS)
    bg_blurred = bg_img.filter(ImageFilter.GaussianBlur(25))
    dim_layer = Image.new('RGBA', (1080, 1920), (0, 0, 0, int(255 * 0.60)))
    bg_base = Image.alpha_composite(bg_blurred, dim_layer)
    
    # 3. Create temp directory
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(temp_dir, exist_ok=True)
    
    # Preload capsule images
    loaded_capsules = {}
    for game in games_list:
        cap_path = os.path.join(CAPSULES_DIR, game["capsule"])
        if os.path.exists(cap_path):
            loaded_capsules[game["capsule"]] = Image.open(cap_path).convert('RGBA')
        else:
            print(f"Warning: Capsule not found {cap_path}, generating placeholder.")
            placeholder = Image.new('RGBA', (540, 810), (40, 40, 40, 255))
            p_draw = ImageDraw.Draw(placeholder)
            p_draw.rectangle((0, 0, 540, 810), outline=(128, 128, 128, 255), width=6)
            loaded_capsules[game["capsule"]] = placeholder
            
    # 4. Render frames
    print("Rendering frames...")
    for f in range(total_frames):
        frame = bg_base.copy()
        draw = ImageDraw.Draw(frame)
        
        # Header & progress bar
        draw_header(draw, FONT_PATH)
        draw_progress_bar(draw, f, total_frames)
        
        # Subtle watermark at the bottom center
        draw_centered_text(draw, "@dominus8735", 540, 1860, FONT_PATH, 24, (255, 255, 255, 100))
        
        # Get shot details
        stype, start_frame, end_frame, data = get_shot_info(f, total_frames, games_list, cta_title, cta_subtitle)
        frame_offset = f - start_frame
        
        if stype == 'intro':
            # Pulsing text
            pulse = 1.0 + 0.08 * math.sin(f * math.pi / 15.0)
            
            # Card background
            draw.rounded_rectangle((100, 700, 980, 1180), radius=40, fill=(0, 0, 0, 175), outline=(255, 106, 0, 255), width=6)
            
            draw_centered_text(draw, intro_title, 540, 880, FONT_PATH, int(52 * pulse), (255, 255, 255, 255))
            draw_centered_text(draw, intro_subtitle, 540, 1020, FONT_PATH, int(36 * pulse), (255, 255, 255, 255))
            
        elif stype == 'game':
            game = data
            # Scale transition
            if frame_offset < 15:
                scale = 0.8 + 0.2 * (frame_offset / 15.0)
            else:
                scale = 1.0
                
            capsule_base = loaded_capsules[game["capsule"]]
            capsule_img, bbox = render_scaled_capsule(capsule_base, scale)
            
            if capsule_img is not None:
                # Draw white outline & glowing border
                draw.rounded_rectangle((bbox[0], bbox[1], bbox[2], bbox[3]), radius=int(20 * scale), outline=(255, 255, 255, 80), width=int(10 * scale))
                draw.rounded_rectangle((bbox[0], bbox[1], bbox[2], bbox[3]), radius=int(20 * scale), outline=(255, 255, 255, 255), width=int(6 * scale))
                frame.paste(capsule_img, (bbox[0], bbox[1]), capsule_img)
                
            # Discount badge (bounce)
            badge_scale = get_bounce_scale(frame_offset)
            if badge_scale > 0:
                bx = bbox[2] - 50
                by = bbox[3] - 40
                bw = 180 * badge_scale
                bh = 80 * badge_scale
                bx0 = bx - bw / 2
                bx1 = bx + bw / 2
                by0 = by - bh / 2
                by1 = by + bh / 2
                
                draw.rounded_rectangle((bx0, by0, bx1, by1), radius=int(25 * badge_scale), fill=(220, 10, 30, 255))
                draw.rounded_rectangle((bx0, by0, bx1, by1), radius=int(25 * badge_scale), outline=(255, 255, 255, 255), width=int(4 * badge_scale))
                draw_centered_text(draw, game["discount"], bx, by, FONT_PATH, int(42 * badge_scale), (255, 255, 255, 255))
                
            # Slide up texts
            slide_offset = int(50 * (1.0 - min(1.0, frame_offset / 15.0)))
            draw_centered_text(draw, game["title"], 540, 1320 + slide_offset, FONT_PATH, 50, (255, 255, 255, 255))
            draw_centered_text(draw, game["price"], 540, 1430 + slide_offset, FONT_PATH, 42, (255, 255, 255, 255))
            
        elif stype == 'outro':
            # Pulse text & button
            pulse = 1.0 + 0.08 * math.sin(frame_offset * math.pi / 15.0)
            
            draw_centered_text(draw, cta_title, 540, 620, FONT_PATH, 56, (255, 255, 255, 255))
            draw_centered_text(draw, cta_subtitle, 540, 740, FONT_PATH, 44, (255, 255, 255, 255))
            
            # Additional Call to Action branding text
            draw_centered_text(draw, "¡SUSCRÍBETE A DOMINUSBABEL!", 540, 880, FONT_PATH, 38, (255, 106, 0, 255))
            
            # Neon pulsing channel handle button
            bw = 540 * pulse
            bh = 120 * pulse
            bx0 = 540 - bw / 2
            bx1 = 540 + bw / 2
            by0 = 1060 - bh / 2
            by1 = 1060 + bh / 2
            
            draw.rounded_rectangle((bx0, by0, bx1, by1), radius=int(60 * pulse), fill=(220, 10, 30, 255))
            draw.rounded_rectangle((bx0, by0, bx1, by1), radius=int(60 * pulse), outline=(255, 255, 255, 255), width=int(6 * pulse))
            draw_centered_text(draw, "@dominus8735", 540, 1060, FONT_PATH, int(48 * pulse), (255, 255, 255, 255))
            
        # Save image
        frame_filename = os.path.join(temp_dir, f"frame_{f:05d}.png")
        frame.convert('RGB').save(frame_filename, 'PNG')
        
        if (f + 1) % 100 == 0 or f == total_frames - 1:
            print(f"  Rendered frame {f+1}/{total_frames}")
            
    # 5. Compile video
    compile_success = compile_video_with_ffmpeg(temp_dir, audio_path, output_path, BG_MUSIC_PATH)
    
    # 6. Cleanup
    print("Cleaning up temporary frames...")
    try:
        shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception as e:
        print(f"Warning: Failed to delete temp directory {temp_dir}: {e}")
        
    if compile_success and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(f"[SUCCESS] Video created: {output_path} ({os.path.getsize(output_path)} bytes)")
        return True
    else:
        print(f"[ERROR] Failed to compile {output_path}")
        return False

def main():
    print("=== Starting compile_shorts.py ===")
    
    # Download optional background music
    download_success = download_bg_music()
    bg_music = BG_MUSIC_PATH if download_success else None
    
    # Generate transition whooshes and badge pop sound effects
    generate_sfx_files()
    
    # Render and compile RTS
    rts_ok = process_short(
        short_id="RTS",
        name="Real-Time Strategy (RTS) Short",
        audio_filename="audio_rts.mp3",
        games_list=RTS_GAMES,
        intro_title="¡OFERTAS DE ESTRATEGIA!",
        intro_subtitle="Rebajas de Steam",
        cta_title="¿CUÁL COMPRARÁS?",
        cta_subtitle="¡Comenta y Suscríbete!"
    )
    
    # Render and compile City Builders
    city_ok = process_short(
        short_id="City",
        name="City Builder / Management Short",
        audio_filename="audio_city.mp3",
        games_list=CITY_GAMES,
        intro_title="CONSTRUYE TU CIUDAD",
        intro_subtitle="Mejores Rebajas",
        cta_title="¿CUÁL GESTIONARÁS?",
        cta_subtitle="¡Comenta y Suscríbete!"
    )
    
    # Render and compile ARPG
    arpg_ok = process_short(
        short_id="ARPG",
        name="Action RPG (ARPG) Short",
        audio_filename="audio_arpg.mp3",
        games_list=ARPG_GAMES,
        intro_title="ARPG CON DESCUENTAZO",
        intro_subtitle="¡Hasta -90%!",
        cta_title="¿CUÁL DOMINARÁS?",
        cta_subtitle="¡Comenta y Suscríbete!"
    )
    
    print("\n========================= SUMMARY =========================")
    print(f"RTS Video: {'SUCCESS' if rts_ok else 'FAILED'}")
    print(f"City Video: {'SUCCESS' if city_ok else 'FAILED'}")
    print(f"ARPG Video: {'SUCCESS' if arpg_ok else 'FAILED'}")
    print("===========================================================")
    
    if rts_ok and city_ok and arpg_ok:
        print("All three shorts compiled successfully!")
        sys.exit(0)
    else:
        print("One or more compilation failures occurred.")
        sys.exit(1)

if __name__ == "__main__":
    main()
