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

# Reconfigure terminal output to UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Root Directories
BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
FONT_PATH = r"C:\Windows\Fonts\segoeuib.ttf"
BG_PATH = os.path.join(BASE_DIR, "background.jpg")
BG_MUSIC_PATH = os.path.join(BASE_DIR, "background_music.mp3")

# Ensure subdirectories exist
os.makedirs(os.path.join(BASE_DIR, "temp_render"), exist_ok=True)

# ----------------------------------------------------
# Game Metadata for the 5 New Shorts
# ----------------------------------------------------
SHORTS_GAMES_DATA = {
    "openworld": [
        {"title": "Red Dead Redemption 2", "discount": "-67%", "price": "AHORA $19.79 | ANTES $59.99", "appid": 1174180},
        {"title": "Grand Theft Auto V", "discount": "-63%", "price": "AHORA $14.98 | ANTES $39.98", "appid": 271590},
        {"title": "Rust", "discount": "-50%", "price": "AHORA $19.99 | ANTES $39.99", "appid": 252490},
        {"title": "Subnautica", "discount": "-50%", "price": "AHORA $14.99 | ANTES $29.99", "appid": 264710},
        {"title": "Terraria", "discount": "-50%", "price": "AHORA $4.99 | ANTES $9.99", "appid": 105600}
    ],
    "racing": [
        {"title": "Forza Horizon 5", "discount": "-50%", "price": "AHORA $29.99 | ANTES $59.99", "appid": 1551360},
        {"title": "Assetto Corsa", "discount": "-80%", "price": "AHORA $3.99 | ANTES $19.99", "appid": 244210},
        {"title": "Need for Speed Unbound", "discount": "-90%", "price": "AHORA $6.99 | ANTES $69.99", "appid": 1846380},
        {"title": "Euro Truck Simulator 2", "discount": "-75%", "price": "AHORA $4.99 | ANTES $19.99", "appid": 227300},
        {"title": "Wreckfest", "discount": "-90%", "price": "AHORA $2.99 | ANTES $29.99", "appid": 228380}
    ],
    "sports": [
        {"title": "EA SPORTS FC 24", "discount": "-80%", "price": "AHORA $13.99 | ANTES $69.99", "appid": 2195250},
        {"title": "Riders Republic", "discount": "-90%", "price": "AHORA $3.99 | ANTES $39.99", "appid": 2290180},
        {"title": "Golf With Your Friends", "discount": "-67%", "price": "AHORA $4.94 | ANTES $14.99", "appid": 431240},
        {"title": "Football Manager 2024", "discount": "-50%", "price": "AHORA $29.99 | ANTES $59.99", "appid": 2252600},
        {"title": "PGA TOUR 2K23", "discount": "-75%", "price": "AHORA $14.99 | ANTES $59.99", "appid": 2380510}
    ],
    "cooking": [
        {"title": "Overcooked! 2", "discount": "-75%", "price": "AHORA $6.24 | ANTES $24.99", "appid": 728880},
        {"title": "PlateUp!", "discount": "-70%", "price": "AHORA $5.99 | ANTES $19.99", "appid": 1599600},
        {"title": "Cooking Simulator", "discount": "-60%", "price": "AHORA $7.99 | ANTES $19.99", "appid": 641320},
        {"title": "Overcooked! All You Can Eat", "discount": "-60%", "price": "AHORA $15.99 | ANTES $39.99", "appid": 1243830},
        {"title": "Good Pizza, Great Pizza", "discount": "-40%", "price": "AHORA $5.99 | ANTES $9.99", "appid": 770810}
    ],
    "4x": [
        {"title": "Civilization VI", "discount": "-90%", "price": "AHORA $5.99 | ANTES $59.99", "appid": 289070},
        {"title": "Stellaris", "discount": "-75%", "price": "AHORA $9.99 | ANTES $39.99", "appid": 281990},
        {"title": "Hearts of Iron IV", "discount": "-80%", "price": "AHORA $9.99 | ANTES $49.99", "appid": 394360},
        {"title": "Age of Wonders 4", "discount": "-50%", "price": "AHORA $24.99 | ANTES $49.99", "appid": 1669000},
        {"title": "Endless Space 2", "discount": "-75%", "price": "AHORA $9.99 | ANTES $39.99", "appid": 392110}
    ]
}

# Category formatting details
SHORTS_META = {
    "openworld": {"header": "MUNDOS ABIERTOS", "outro_title": "¿QUÉ MUNDO ELEGIRÁS?", "outro_subtitle": "¡Comenta y Suscríbete!"},
    "racing": {"header": "VELOCIDAD MÁXIMA", "outro_title": "¿CUÁL PILOTARÁS?", "outro_subtitle": "¡Comenta y Suscríbete!"},
    "sports": {"header": "JUEGOS DEPORTIVOS", "outro_title": "¿CUÁL GANARÁS?", "outro_subtitle": "¡Comenta y Suscríbete!"},
    "cooking": {"header": "PASIÓN CULINARIA", "outro_title": "¿QUÉ COCINARÁS?", "outro_subtitle": "¡Comenta y Suscríbete!"},
    "4x": {"header": "ESTRATEGIA 4X", "outro_title": "¿CUÁL CONQUISTARÁS?", "outro_subtitle": "¡Comenta y Suscríbete!"}
}

# ----------------------------------------------------
# General Helpers
# ----------------------------------------------------
def get_clean_env():
    clean_env = os.environ.copy()
    for var in ['PYTHONPATH', 'PYTHONHOME', 'VIRTUAL_ENV']:
        if var in clean_env:
            del clean_env[var]
    return clean_env

def get_audio_duration(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(result.stdout.strip())

def get_video_duration(file_path):
    return get_audio_duration(file_path)

def slice_trailer_clip(appid, duration_sec, start_offset, output_path, is_vertical=True):
    """Slices a gameplay video segment from the trailer and scales/formats it."""
    trailer_path = os.path.join(TRAILERS_DIR, f"trailer_{appid}.mp4" if appid != 244450 else "mow_trailer.mp4")
    if not os.path.exists(trailer_path):
        print(f"    [WARNING] Trailer for App ID {appid} not found! Fallback to static will occur.")
        return False

    try:
        total_dur = get_video_duration(trailer_path)
    except Exception:
        total_dur = 120.0
    
    # Wrap-around if start_offset exceeds duration
    ss = start_offset % max(1.0, total_dur - duration_sec - 1.0)
    
    # Dimensions: 16:9 box inside vertical is 540x304. Full-screen horizontal is 1920x1080.
    scale_filter = "scale=540:304,pad=552:316:6:6:white" if is_vertical else "scale=1920:1080"
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", f"{ss:.2f}",
        "-t", f"{duration_sec:.2f}",
        "-i", trailer_path,
        "-vf", scale_filter,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-an", # No audio for overlay clips
        output_path
    ]
    
    try:
        subprocess.run(cmd, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 0
    except Exception as e:
        print(f"    [WARNING] Failed to slice clip for App ID {appid}: {e}")
        return False

# ----------------------------------------------------
# Drawing / Composition Helpers
# ----------------------------------------------------
def draw_centered_text(draw, text, center_x, center_y, font_path, base_size, fill_color, max_width=900):
    size = base_size
    font = ImageFont.truetype(font_path, size)
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    
    while w > max_width and size > 14:
        size -= 2
        font = ImageFont.truetype(font_path, size)
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
    x = center_x - w / 2
    y = center_y - h / 2
    draw.text((x + 2, y + 2), text, font=font, fill=(0, 0, 0, 160))
    draw.text((x, y), text, font=font, fill=fill_color)

def get_bounce_scale(frame_offset):
    if frame_offset < 0:
        return 0.0
    if frame_offset >= 15:
        return 1.0
    t = frame_offset / 15.0
    if t < 0.7:
        return 1.2 * (t / 0.7)
    else:
        return 1.2 - 0.2 * ((t - 0.7) / 0.3)

def render_scaled_capsule(capsule_base, scale, center_x, center_y, base_w=540, base_h=810):
    w = int(base_w * scale)
    h = int(base_h * scale)
    if w <= 0 or h <= 0:
        return None, (center_x, center_y, center_x, center_y)
    
    capsule_scaled = capsule_base.resize((w, h), Image.Resampling.LANCZOS)
    mask = Image.new('L', (w, h), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, w, h), radius=int(20 * scale), fill=255)
    capsule_scaled.putalpha(mask)
    
    x0 = center_x - w // 2
    y0 = center_y - h // 2
    return capsule_scaled, (x0, y0, x0 + w, y0 + h)

def draw_vertical_header(draw, font_path, title_text):
    draw.rounded_rectangle((80, 80, 1000, 220), radius=30, fill=(0, 0, 0, 165), outline=(255, 255, 255, 45), width=2)
    draw_centered_text(draw, title_text, 540, 125, font_path, 34, (255, 255, 255, 255))
    draw_centered_text(draw, "OFERTAS DE VERANO", 540, 175, font_path, 22, (255, 106, 0, 255))

def draw_vertical_progress_bar(draw, frame_idx, total_frames, y_pos=232, height=12):
    progress = frame_idx / max(1, total_frames - 1)
    w = int(progress * 920)
    draw.rounded_rectangle((80, y_pos, 1000, y_pos + height), radius=height//2, fill=(40, 40, 40, 160))
    if w > 0:
        glow_x0, glow_x1 = 80, 80 + w
        draw.rounded_rectangle((glow_x0, y_pos - 4, glow_x1, y_pos + height + 4), radius=(height+8)//2, fill=(255, 106, 0, 50))
        draw.rounded_rectangle((glow_x0, y_pos, glow_x1, y_pos + height), radius=height//2, fill=(255, 106, 0, 255))

# ----------------------------------------------------
# 1. compile_vertical_short
# ----------------------------------------------------
def compile_vertical_short(category_key):
    meta = SHORTS_META[category_key]
    games = SHORTS_GAMES_DATA[category_key]
    audio_path = os.path.join(BASE_DIR, f"audio_{category_key}.mp3")
    output_path = os.path.join(BASE_DIR, f"{category_key}_v2_short.mp4")
    
    print(f"\n====================================================")
    print(f"Compiling Short Category: {category_key} -> {output_path}")
    print("====================================================")
    
    if not os.path.exists(audio_path):
        print(f"[ERROR] Audio file not found: {audio_path}")
        return False
        
    duration = get_audio_duration(audio_path)
    total_frames = int(duration * 30)
    print(f"Duration: {duration:.2f}s | Total Frames: {total_frames}")
    
    # Create temp frame directory
    temp_dir = os.path.join(BASE_DIR, f"temp_frames_{category_key}")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Load background and prepare font
    bg_img = Image.open(BG_PATH).resize((1080, 1920)).filter(ImageFilter.GaussianBlur(25))
    dimmer = Image.new("RGBA", (1080, 1920), (0, 0, 0, 150))
    bg_base = Image.alpha_composite(bg_img.convert("RGBA"), dimmer)
    
    # Slice the gameplay clips (Game 1 has 3.5s, others have 3.0s)
    clips_data = []
    print("Slicing gameplay clips...")
    for idx, game in enumerate(games):
        clip_fn = f"temp_clip_{category_key}_{game['appid']}.mp4"
        clip_path = os.path.join(temp_dir, clip_fn)
        start_t = 20.0 + idx * 5.0
        dur_t = 3.5 if idx == 0 else 3.0
        ok = slice_trailer_clip(game["appid"], dur_t, start_t, clip_path, is_vertical=True)
        clips_data.append({"ok": ok, "path": clip_path, "game": game, "idx": idx})
        
    # Render frames to JPEG
    print("Rendering frames to disk...")
    for frame_idx in range(total_frames):
        frame = bg_base.copy()
        draw = ImageDraw.Draw(frame)
        
        # Draw permanent headers & progress
        draw_vertical_header(draw, FONT_PATH, meta["header"])
        draw_vertical_progress_bar(draw, frame_idx, total_frames)
        
        # Watermark
        draw_centered_text(draw, "@dominus8735", 540, 1850, FONT_PATH, 20, (255, 255, 255, 100))
        
        if frame_idx < 90:
            # Pulsing Intro Text
            pulse = 1.0 + 0.05 * math.sin(frame_idx * 0.2)
            draw_centered_text(draw, meta["header"], 540, 785, FONT_PATH, int(48 * pulse), (255, 255, 255, 255))
            draw_centered_text(draw, "🔥 REBAJAS DE VERANO 🔥", 540, 900, FONT_PATH, 26, (255, 106, 0, 255))
            
        elif frame_idx < 780:
            # Active game index
            if frame_idx < 240:
                g_idx, start_f, end_f = 0, 90, 240
            elif frame_idx < 375:
                g_idx, start_f, end_f = 1, 240, 375
            elif frame_idx < 510:
                g_idx, start_f, end_f = 2, 375, 510
            elif frame_idx < 645:
                g_idx, start_f, end_f = 3, 510, 645
            else:
                g_idx, start_f, end_f = 4, 645, 780
                
            game = games[g_idx]
            offset = frame_idx - start_f
            
            # Text information
            draw_centered_text(draw, game["title"], 540, 1260, FONT_PATH, 34, (255, 255, 255, 255))
            draw_centered_text(draw, game["price"], 540, 1340, FONT_PATH, 24, (255, 255, 255, 200))
            
            # Discount Badge Bounce Animation
            badge_scale = get_bounce_scale(offset - 10)
            if badge_scale > 0:
                bw, bh = int(220 * badge_scale), int(80 * badge_scale)
                bx0, by0 = 540 - bw // 2, 1420 - bh // 2
                draw.rounded_rectangle((bx0, by0, bx0 + bw, by0 + bh), radius=bh//2, fill=(220, 20, 60, 255))
                draw_centered_text(draw, game["discount"], 540, 1420, FONT_PATH, int(30 * badge_scale), (255, 255, 255, 255))
            
            is_gameplay = offset >= 45
            clip_ok = clips_data[g_idx]["ok"]
            
            if is_gameplay and clip_ok:
                # White border (552x316) for the 16:9 gameplay box (540x304)
                draw.rectangle((264, 627, 816, 943), outline=(255, 255, 255, 255), width=6)
            else:
                # Render capsule art
                caps_file = os.path.join(CAPSULES_DIR, f"capsule_{game['appid']}.jpg")
                if os.path.exists(caps_file):
                    caps_img = Image.open(caps_file)
                    scale = 0.8 + 0.2 * min(1.0, offset / 15.0)
                    scaled_caps, bbox = render_scaled_capsule(caps_img, scale, 540, 785)
                    if scaled_caps:
                        frame.paste(scaled_caps, bbox, scaled_caps)
                        draw.rounded_rectangle(bbox, radius=int(20*scale), outline=(255, 255, 255, 255), width=6)
                else:
                    draw_centered_text(draw, "[Sin Imagen]", 540, 785, FONT_PATH, 32, (255, 255, 255, 128))
                    
        else:
            # Outro / CTA Call
            pulse = 1.0 + 0.05 * math.sin(frame_idx * 0.2)
            draw_centered_text(draw, meta["outro_title"], 540, 750, FONT_PATH, 38, (255, 255, 255, 255))
            
            sb_w, sb_h = int(500 * pulse), int(100 * pulse)
            sb_x0, sb_y0 = 540 - sb_w // 2, 920 - sb_h // 2
            draw.rounded_rectangle((sb_x0, sb_y0, sb_x0 + sb_w, sb_y0 + sb_h), radius=sb_h//2, fill=(255, 69, 0, 255))
            draw_centered_text(draw, meta["outro_subtitle"], 540, 920, FONT_PATH, int(28 * pulse), (255, 255, 255, 255))
            
        frame.convert("RGB").save(os.path.join(temp_dir, f"frame_{frame_idx:05d}.jpg"), quality=85)
        
    temp_base_mp4 = os.path.join(temp_dir, "temp_base.mp4")
    print("Compiling temporary base video...")
    cmd_base = [
        "ffmpeg", "-y", "-f", "image2", "-framerate", "30",
        "-i", os.path.join(temp_dir, "frame_%05d.jpg"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", temp_base_mp4
    ]
    subprocess.run(cmd_base, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # Overlay gameplay video clips
    filter_inputs = ["-i", temp_base_mp4]
    filter_overlay_str = "[0:v]"
    
    active_clips_count = 0
    for idx, c in enumerate(clips_data):
        if c["ok"] and os.path.exists(c["path"]):
            filter_inputs.extend(["-i", c["path"]])
            active_clips_count += 1
            
            start_t = 4.5 if idx == 0 else 9.5 + (idx - 1) * 4.5
            end_t = 8.0 if idx == 0 else 12.5 + (idx - 1) * 4.5
            
            input_label = f"[{active_clips_count}:v]"
            out_label = f"[v{active_clips_count}]" if idx < 4 else "[v_overlayed]"
            
            filter_overlay_str += f"{input_label}overlay=270:633:enable='between(t,{start_t:.2f},{end_t:.2f})'"
            if idx < 4:
                filter_overlay_str += f"{out_label};{out_label}"
            else:
                filter_overlay_str += "[v_overlayed]"
                
    if active_clips_count == 0:
        filter_overlay_str = "[0:v]copy[v_overlayed]"
        
    # Audio elements
    whoosh_wav = os.path.join(BASE_DIR, "whoosh.wav")
    pop_wav = os.path.join(BASE_DIR, "pop.wav")
    sfx_available = os.path.exists(whoosh_wav) and os.path.exists(pop_wav)
    use_bg = os.path.exists(BG_MUSIC_PATH) and os.path.getsize(BG_MUSIC_PATH) > 0
    
    audio_inputs_idx = active_clips_count + 1
    audio_inputs = ["-i", audio_path]
    vo_idx = audio_inputs_idx
    
    bg_idx = None
    
    if use_bg:
        audio_inputs.extend(["-ss", "15", "-i", BG_MUSIC_PATH])
        bg_idx = vo_idx + 1
        
    if sfx_available:
        audio_inputs.extend(["-i", whoosh_wav, "-i", pop_wav])
        w_idx = vo_idx + 2 if use_bg else vo_idx + 1
        p_idx = w_idx + 1
        
        sfx_filter = (
            f"[{w_idx}:a]asplit=6[w0][w1][w2][w3][w4][w5];"
            f"[{p_idx}:a]asplit=5[p0][p1][p2][p3][p4];"
            f"[w0]adelay=3000|3000[wd0];"
            f"[w1]adelay=8000|8000[wd1];"
            f"[w2]adelay=12500|12500[wd2];"
            f"[w3]adelay=17000|17000[wd3];"
            f"[w4]adelay=21500|21500[wd4];"
            f"[w5]adelay=26000|26000[wd5];"
            f"[p0]adelay=3300|3300[pd0];"
            f"[p1]adelay=8300|8300[pd1];"
            f"[p2]adelay=12800|12800[pd2];"
            f"[p3]adelay=16300|16300[pd3];"
            f"[p4]adelay=21800|21800[pd4];"
            f"[wd0][wd1][wd2][wd3][wd4][wd5][pd0][pd1][pd2][pd3][pd4]amix=inputs=11:normalize=0[sfx_raw];"
            f"[sfx_raw]volume=-8dB[sfx_final];"
        )
        if use_bg:
            audio_mix_filter = sfx_filter + (
                f"[{vo_idx}:a]volume=1.0[vo];"
                f"[{bg_idx}:a]volume=-22dB[bg];"
                f"[vo][bg][sfx_final]amix=inputs=3:duration=first:dropout_transition=0[a]"
            )
        else:
            audio_mix_filter = sfx_filter + (
                f"[{vo_idx}:a]volume=1.0[vo];"
                f"[vo][sfx_final]amix=inputs=2:duration=first:dropout_transition=0[a]"
            )
    else:
        if use_bg:
            audio_mix_filter = (
                f"[{vo_idx}:a]volume=1.0[vo];"
                f"[{bg_idx}:a]volume=-22dB[bg];"
                f"[vo][bg]amix=inputs=2:duration=first:dropout_transition=0[a]"
            )
        else:
            audio_mix_filter = f"[{vo_idx}:a]volume=1.0[a]"
            
    filter_complex_final = f"{filter_overlay_str};{audio_mix_filter}"
    
    cmd_final = []
    cmd_final.extend(["ffmpeg", "-y"])
    cmd_final.extend(filter_inputs)
    cmd_final.extend(audio_inputs)
    cmd_final.extend([
        "-filter_complex", filter_complex_final,
        "-map", "[v_overlayed]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        output_path
    ])
    
    print("Compiling final Short with gameplay clips and mixed audio...")
    subprocess.run(cmd_final, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"¡SUCCESS! Video compiled successfully: {output_path}")
    return True

# ----------------------------------------------------
# 2. compile_horizontal_mow (Men of War Long Video)
# ----------------------------------------------------
def compile_horizontal_mow():
    audio_path = os.path.join(BASE_DIR, "audio_mow.mp3")
    output_path = os.path.join(BASE_DIR, "MenOfWar_AssaultSquad2_analysis.mp4")
    
    print(f"\n====================================================")
    print(f"Compiling Horizontal Video: Men of War AS2 -> {output_path}")
    print("====================================================")
    
    if not os.path.exists(audio_path):
        print(f"[ERROR] Audio file not found: {audio_path}")
        return False
        
    duration = get_audio_duration(audio_path)
    print(f"Total Audio Duration: {duration:.2f} s")
    
    temp_dir = os.path.join(BASE_DIR, "temp_render_mow")
    os.makedirs(temp_dir, exist_ok=True)
    
    segments_word_counts = [
        100, 110, 110, 50,
        110, 120, 100, 70,
        110, 110, 100, 80,
        110, 110, 100,
        100, 90, 110
    ]
    
    total_words = sum(segments_word_counts)
    segment_durations = [duration * (count / total_words) for count in segments_word_counts]
    
    segments_config = [
        {"type": "promo", "asset": "mow_capsule.jpg", "text": "MEN OF WAR: ASSAULT SQUAD 2", "sub": "Recomendación Principal - Rebajas de Steam 2026", "has_gameplay": True},
        {"type": "promo", "asset": "mow_capsule.jpg", "text": "LIBERTAD DE ACCIÓN Y TÁCTICA", "sub": "Cada soldado es un individuo, cada bala calcula su física", "has_gameplay": True},
        {"type": "ss", "asset": "screenshot_0.jpg", "text": "SISTEMA DE CONTROL DIRECTO", "sub": "Toma el control manual de cualquier unidad del campo de batalla", "has_gameplay": True},
        {"type": "promo", "asset": "mow_capsule.jpg", "text": "JOYA DE LA SIMULACIÓN MILITAR", "sub": "A fondo: balística, blindajes, inventario y mods", "has_gameplay": True},
        
        {"type": "gameplay", "text": "FÍSICAS DE DESTRUCCIÓN COMPLETAS", "sub": "El entorno interactúa y se destruye dinámicamente bajo fuego artillado", "has_gameplay": False},
        {"type": "gameplay", "text": "COBERTURAS DEGRADABLES", "sub": "Los parapetos se destruyen, exponiendo la infantería en el campo", "has_gameplay": False},
        {"type": "gameplay", "text": "BALÍSTICA DE ALTA PRECISIÓN", "sub": "Velocidad, penetración, desviación y colisiones reales", "has_gameplay": False},
        {"type": "gameplay", "text": "CONTROL DIRECTO ACTIVADO", "sub": "Pasa de la visión de general a la puntería manual de soldado", "has_gameplay": False},
        
        {"type": "gameplay", "text": "DAÑO DE COMPONENTES EN BLINDADOS", "sub": "Transmisión, motor, oruga, tripulación y munición modelados", "has_gameplay": False},
        {"type": "gameplay", "text": "PENETRACIÓN Y DETONACIÓN", "sub": "Incendios realistas y fuegos artificiales al estallar el compartimento de obuses", "has_gameplay": False},
        {"type": "ss", "asset": "screenshot_4.jpg", "text": "INVENTARIO COMPLETO INDIVIDUAL", "sub": "Fusil, mochila, cascos, vendajes y granadas por mochila", "has_gameplay": True},
        {"type": "gameplay", "text": "MICROGESTIÓN Y REPARACIONES", "sub": "Lootear cadáveres y reparar vehículos en el fragor de la batalla", "has_gameplay": False},
        
        {"type": "promo", "asset": "mow_capsule.jpg", "text": "PLATAFORMA MILITAR ILIMITADA", "sub": "Miles de modificaciones en Steam Workshop: Cold War, Modern Combat...", "has_gameplay": True},
        {"type": "ss", "asset": "screenshot_7.jpg", "text": "ESPECTACULAR TRABAJO DE COMUNIDAD", "sub": "Campañas cooperativas históricas y efectos de sonido realistas", "has_gameplay": True},
        {"type": "gameplay", "text": "ASALTO COOPERATIVO MULTIJUGADOR", "sub": "Dirige infantería, blindados y artillería coordinado con amigos", "has_gameplay": False},
        
        {"type": "ss", "asset": "screenshot_8.jpg", "text": "OFERTA IMPERDIBLE: 80% DESCUENTO", "sub": "Adquiere el simulador táctico definitivo por solo $5.99 en Steam", "has_gameplay": True},
        {"type": "ss", "asset": "screenshot_9.jpg", "text": "CENTENAS DE HORAS TÁCTICAS", "sub": "Una joya inagotable para tu biblioteca militar de Steam", "has_gameplay": True},
        {"type": "promo", "asset": "mow_capsule.jpg", "text": "DOMINUSBABEL - TÁCTICA Y ESTRATEGIA", "sub": "Comenta tu mod preferido, dale a me gusta y suscríbete", "has_gameplay": True}
    ]
    
    print("Generating individual segment video clips...")
    segment_files = []
    
    for i, cfg in enumerate(segments_config):
        dur = segment_durations[i]
        seg_fn = f"seg_{i:02d}.mp4"
        seg_path = os.path.join(temp_dir, seg_fn)
        
        print(f"  Rendering Segment {i+1}/18: {cfg['text']} ({dur:.2f} s)")
        
        if cfg["type"] == "gameplay":
            start_offset = i * 15.0
            ok = slice_trailer_clip(244450, dur, start_offset, seg_path, is_vertical=False)
            if not ok:
                cfg["type"] = "ss"
                cfg["asset"] = f"screenshot_{i%10}.jpg"
                
        if cfg["type"] in ["promo", "ss"]:
            split_slide = cfg["has_gameplay"] and dur > 6.0
            slide_dur = 4.0 if split_slide else dur
            gameplay_dur = dur - slide_dur
            
            slide_fn = f"temp_slide_{i}.mp4"
            slide_path = os.path.join(temp_dir, slide_fn)
            slide_frames_dir = os.path.join(temp_dir, f"slide_{i}_frames")
            os.makedirs(slide_frames_dir, exist_ok=True)
            
            asset_path = os.path.join(CAPSULES_DIR if cfg["type"] == "promo" else SCREENSHOTS_DIR, cfg["asset"])
            if not os.path.exists(asset_path):
                asset_path = os.path.join(SCREENSHOTS_DIR, "screenshot_0.jpg")
                
            img_base = Image.open(asset_path).resize((1920, 1080))
            bg_blurred = img_base.filter(ImageFilter.GaussianBlur(30))
            dimmer = Image.new("RGBA", (1920, 1080), (0, 0, 0, 160))
            bg_final = Image.alpha_composite(bg_blurred.convert("RGBA"), dimmer)
            
            total_slide_frames = int(slide_dur * 30)
            
            for f_idx in range(total_slide_frames):
                frame = bg_final.copy()
                draw = ImageDraw.Draw(frame)
                
                zoom = 1.0 + 0.05 * (f_idx / max(1, total_slide_frames - 1))
                
                img_fg = img_base.copy()
                fg_w, fg_h = int(1280 * zoom), int(720 * zoom)
                img_scaled = img_fg.resize((fg_w, fg_h), Image.Resampling.LANCZOS)
                
                mask = Image.new('L', (fg_w, fg_h), 255)
                fg_x = 960 - fg_w // 2
                fg_y = 480 - fg_h // 2
                frame.paste(img_scaled, (fg_x, fg_y), mask)
                
                draw.rectangle((fg_x, fg_y, fg_x + fg_w, fg_y + fg_h), outline=(255, 255, 255, 255), width=6)
                
                # Bottom text bar
                draw.rounded_rectangle((100, 880, 1820, 1020), radius=20, fill=(0, 0, 0, 180), outline=(255, 255, 255, 30), width=1)
                
                draw_centered_text(draw, cfg["text"].upper(), 960, 920, FONT_PATH, 36, (255, 255, 255, 255), max_width=1600)
                draw_centered_text(draw, cfg["sub"], 960, 975, FONT_PATH, 20, (255, 106, 0, 255), max_width=1600)
                
                # Top header bar
                draw.rounded_rectangle((100, 40, 1820, 120), radius=15, fill=(0, 0, 0, 140))
                draw_centered_text(draw, "MEN OF WAR: ASSAULT SQUAD 2 - OFERTAS STEAM 2026", 960, 80, FONT_PATH, 22, (255, 255, 255, 255))
                
                draw.text((100, 1040), "@dominus8735", font=ImageFont.truetype(FONT_PATH, 18), fill=(255, 255, 255, 80))
                
                frame.convert("RGB").save(os.path.join(slide_frames_dir, f"frame_{f_idx:05d}.jpg"), quality=85)
                
            cmd_slide = [
                "ffmpeg", "-y", "-f", "image2", "-framerate", "30",
                "-i", os.path.join(slide_frames_dir, "frame_%05d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", slide_path
            ]
            subprocess.run(cmd_slide, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            shutil.rmtree(slide_frames_dir, ignore_errors=True)
            
            if split_slide:
                game_fn = f"temp_gameplay_{i}.mp4"
                game_path = os.path.join(temp_dir, game_fn)
                start_offset = 10.0 + i * 8.0
                
                ok_gameplay = slice_trailer_clip(244450, gameplay_dur, start_offset, game_path, is_vertical=False)
                if ok_gameplay:
                    concat_list_path = os.path.join(temp_dir, f"concat_{i}.txt")
                    with open(concat_list_path, 'w', encoding='utf-8') as f:
                        f.write(f"file '{slide_fn}'\n")
                        f.write(f"file '{game_fn}'\n")
                        
                    cmd_cat = [
                        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
                        "-i", concat_list_path,
                        "-c", "copy", seg_path
                    ]
                    subprocess.run(cmd_cat, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
                else:
                    shutil.copy2(slide_path, seg_path)
            else:
                shutil.copy2(slide_path, seg_path)
                
        segment_files.append(seg_path)
        
    print("Concatenating all segments...")
    concat_all_list = os.path.join(temp_dir, "concat_all_segments.txt")
    with open(concat_all_list, 'w', encoding='utf-8') as f:
        for sf in segment_files:
            f.write(f"file '{os.path.basename(sf)}'\n")
            
    temp_concat_video = os.path.join(temp_dir, "mow_video_only.mp4")
    cmd_concat_all = [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", concat_all_list,
        "-c", "copy", temp_concat_video
    ]
    subprocess.run(cmd_concat_all, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    
    # Audio mixing
    whoosh_wav = os.path.join(BASE_DIR, "whoosh.wav")
    pop_wav = os.path.join(BASE_DIR, "pop.wav")
    sfx_available = os.path.exists(whoosh_wav) and os.path.exists(pop_wav)
    use_bg = os.path.exists(BG_MUSIC_PATH) and os.path.getsize(BG_MUSIC_PATH) > 0
    
    audio_inputs = ["-i", temp_concat_video, "-i", audio_path]
    vo_idx = 1
    
    if use_bg:
        audio_inputs.extend(["-ss", "45", "-i", BG_MUSIC_PATH])
        bg_idx = 2
        
    if sfx_available:
        audio_inputs.extend(["-i", whoosh_wav])
        w_idx = 3 if use_bg else 2
        
        boundary_1 = sum(segment_durations[:4])
        boundary_2 = sum(segment_durations[:8])
        boundary_3 = sum(segment_durations[:12])
        boundary_4 = sum(segment_durations[:15])
        
        sfx_filter = (
            f"[{w_idx}:a]asplit=4[w0][w1][w2][w3];"
            f"[w0]adelay={int(boundary_1*1000)}|{int(boundary_1*1000)}[wd0];"
            f"[w1]adelay={int(boundary_2*1000)}|{int(boundary_2*1000)}[wd1];"
            f"[w2]adelay={int(boundary_3*1000)}|{int(boundary_3*1000)}[wd2];"
            f"[w3]adelay={int(boundary_4*1000)}|{int(boundary_4*1000)}[wd3];"
            f"[wd0][wd1][wd2][wd3]amix=inputs=4:normalize=0[sfx_raw];"
            f"[sfx_raw]volume=-8dB[sfx_final];"
        )
        if use_bg:
            audio_mix_filter = sfx_filter + (
                f"[{vo_idx}:a]volume=1.0[vo];"
                f"[{bg_idx}:a]volume=-24dB[bg];"
                f"[vo][bg][sfx_final]amix=inputs=3:duration=first:dropout_transition=0[a]"
            )
        else:
            audio_mix_filter = sfx_filter + (
                f"[{vo_idx}:a]volume=1.0[vo];"
                f"[vo][sfx_final]amix=inputs=2:duration=first:dropout_transition=0[a]"
            )
    else:
        if use_bg:
            audio_mix_filter = (
                f"[{vo_idx}:a]volume=1.0[vo];"
                f"[{bg_idx}:a]volume=-24dB[bg];"
                f"[vo][bg]amix=inputs=2:duration=first:dropout_transition=0[a]"
            )
        else:
            audio_mix_filter = f"[{vo_idx}:a]volume=1.0[a]"
            
    cmd_final = []
    cmd_final.extend(["ffmpeg", "-y"])
    cmd_final.extend(audio_inputs)
    cmd_final.extend([
        "-filter_complex", audio_mix_filter,
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-shortest",
        output_path
    ])
    
    print("Mixing final horizontal video...")
    subprocess.run(cmd_final, env=get_clean_env(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    shutil.rmtree(temp_dir, ignore_errors=True)
    print(f"¡SUCCESS! Video compiled successfully: {output_path}")
    return True

# ----------------------------------------------------
# Main execution entry
# ----------------------------------------------------
def main():
    print("====================================================")
    print("Video Render Engine v2 (KINESIO Expanded Ecosytem)")
    print("====================================================")
    
    # 1. Verify SFX and Music
    print("Verifying audio assets...")
    whoosh_path = os.path.join(BASE_DIR, "whoosh.wav")
    pop_path = os.path.join(BASE_DIR, "pop.wav")
    
    if not (os.path.exists(whoosh_path) and os.path.exists(pop_path)):
        print("SFX files missing. Re-generating...")
        sr = 44100
        with wave.open(whoosh_path, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(sr)
            for i in range(int(sr * 0.5)):
                t = i / sr
                freq = 150 + 300 * (t / 0.5)
                angle = 2 * math.pi * freq * t
                sine_val = math.sin(angle)
                noise_val = random.uniform(-1.0, 1.0)
                val = 0.3 * sine_val + 0.7 * noise_val
                env = math.sin(math.pi * (t / 0.5))
                sample = int(val * env * 12000)
                wav.writeframes(struct.pack('<hh', sample, sample))
                
        with wave.open(pop_path, 'w') as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(sr)
            for i in range(int(sr * 0.15)):
                t = i / sr
                freq = 600 * math.exp(-15 * t) + 200
                phase = 2 * math.pi * (-40 * math.exp(-15 * t) + 200 * t)
                sine_val = math.sin(phase)
                env = math.exp(-20 * t)
                sample = int(sine_val * env * 24000)
                wav.writeframes(struct.pack('<hh', sample, sample))
        print("SFX files created.")
        
    if not (os.path.exists(BG_MUSIC_PATH) and os.path.getsize(BG_MUSIC_PATH) > 0):
        print("Background music missing. Downloading...")
        try:
            req = urllib.request.Request("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=20) as response:
                with open(BG_MUSIC_PATH, 'wb') as out_file:
                    out_file.write(response.read())
            print("Background music downloaded.")
        except Exception as e:
            print(f"Failed to download background music: {e}. Mixing will use voiceover only.")
            
    # 2. Compile Men of War long video
    try:
        compile_horizontal_mow()
    except Exception as e:
        print(f"[ERROR] Failed to compile Men of War video: {e}")
        
    # 3. Compile the 5 vertical Shorts
    for category in ["openworld", "racing", "sports", "cooking", "4x"]:
        try:
            compile_vertical_short(category)
        except Exception as e:
            print(f"[ERROR] Failed to compile Short category '{category}': {e}")
            
    print("\n====================================================")
    print("ALL COMPILATIONS AND RENDERS COMPLETED!")
    print("====================================================")

if __name__ == "__main__":
    main()
