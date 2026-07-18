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
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
MUSIC_DIR = os.path.join(BASE_DIR, "music")

POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

# Available game trailers to rotate as B-roll in even chapters
AVAILABLE_TRAILERS = [
    "gta6_trailer.mp4",
    "dune_spice_wars_trailer.mp4",
    "riftbreaker_trailer.mp4",
    "iron_harvest_trailer.mp4",
    "chaosbane_trailer.mp4",
    "pathfinder_wrath_of_the_righteous_trailer.mp4",
    "gates_of_hell_trailer.mp4",
    "planetary_trailer.mp4",
    "warband_trailer.mp4"
]

CHAPTER_DATA = {
    1: {
        "subtitle": "Introducción a la hegemonía de Valve",
        "bullets": [
            "✔ 74% de cuota de mercado en PC",
            "✔ 17.000 millones en ingresos anuales",
            "✔ Más de 100 millones de usuarios activos"
        ],
        "badge": "HEGEMONÍA 🌐",
        "bg_idx": 0
    },
    2: {
        "subtitle": "El estándar arancelario digital",
        "bullets": [
            "✔ Tasa de comisión fija del 30%",
            "✔ Epic Games y MS Store cobran 12%",
            "✔ Demanda colectiva de $900M en UK"
        ],
        "badge": "TASAS 30% 💸",
        "bg_idx": 1
    },
    3: {
        "subtitle": "La batalla legal de Wolfire",
        "bullets": [
            "✔ Obligaciones de paridad de precios",
            "✔ Cláusula de Nación Más Favorecida",
            "✔ Demanda antitrust de Wolfire Games"
        ],
        "badge": "CONTRATO ⚖",
        "bg_idx": 2
    },
    4: {
        "subtitle": "Acuerdos bajo la mesa de los gigantes",
        "bullets": [
            "✔ Supuesta colusión Steam-Microsoft",
            "✔ Correos internos de Microsoft revelados",
            "✔ Impacto en los precios finales"
        ],
        "badge": "ALIANZAS 💼",
        "bg_idx": 2
    },
    5: {
        "subtitle": "Presión a los gigantes del desarrollo",
        "bullets": [
            "✔ Caso de Ubisoft y Rainbow Six Siege",
            "✔ Amenazas de retirada de la tienda",
            "✔ Gabe Newell niega la fijación de precios"
        ],
        "badge": "UBISOFT 💥",
        "bg_idx": 0
    },
    6: {
        "subtitle": "La cruzada moral de Tim Sweeney",
        "bullets": [
            "✔ Epic Games Store y su comisión del 12%",
            "✔ Cientos de millones en exclusividades",
            "✔ Hipocresía comercial según la comunidad"
        ],
        "badge": "TIM SWEENEY 🎮",
        "bg_idx": 3
    },
    7: {
        "subtitle": "Por qué el dinero no puede comprar la lealtad",
        "bullets": [
            "✔ Caídas de EA App y Ubisoft Connect",
            "✔ Admisión de derrota de Amazon Prime",
            "✔ Subestimar los hábitos del consumidor"
        ],
        "badge": "GOLIATS CAEN ❌",
        "bg_idx": 3
    },
    8: {
        "subtitle": "La realidad económica tras las demandas",
        "bullets": [
            "✔ Búsqueda de mayor margen de ganancia",
            "✔ Descenso de precios altamente improbable",
            "✔ Fragmentación del mercado de lanzadores"
        ],
        "badge": "MONEY TALKS 💵",
        "bg_idx": 1
    },
    9: {
        "subtitle": "La era de las obras maestras y los mods",
        "bullets": [
            "✔ Half-Life, Portal, Counter-Strike y Dota",
            "✔ Contratación de modders comunitarios",
            "✔ Respeto y apoyo al talento aficionado"
        ],
        "badge": "HALF-LIFE 🏆",
        "bg_idx": 4
    },
    10: {
        "subtitle": "El poder de no cotizar en bolsa",
        "bullets": [
            "✔ Libertad de no tener accionistas externos",
            "✔ Salvación del PC gaming en los 2000",
            "✔ Gabe Newell posee la mayoría accionaria"
        ],
        "badge": "PRIVADA 👑",
        "bg_idx": 4
    },
    11: {
        "subtitle": "Reembolsos y soporte de hardware",
        "bullets": [
            "✔ Reembolso automático en <2h de juego",
            "✔ Reemplazos gratuitos de Steam Deck",
            "✔ Enfoque radical en soporte y garantía"
        ],
        "badge": "GARANTÍA 🔄",
        "bg_idx": 5
    },
    12: {
        "subtitle": "Compartir en familia de forma gratuita",
        "bullets": [
            "✔ Préstamo familiar gratuito desde 2013",
            "✔ Múltiples perfiles en la misma biblioteca",
            "✔ Oposición a DRM restrictivos de consolas"
        ],
        "badge": "COMPARTIR 👨‍👩‍👧‍👦",
        "bg_idx": 5
    },
    13: {
        "subtitle": "Equidad en mercados emergentes",
        "bullets": [
            "✔ Precios regionales con 40-70% descuento",
            "✔ Prohibición de publicidad intrusiva",
            "✔ Transparencia obligatoria en IA"
        ],
        "badge": "REGIONAL 🌎",
        "bg_idx": 0
    },
    14: {
        "subtitle": "Liderazgo abierto y salarios récord",
        "bullets": [
            "✔ Correo gaben@valvesoftware.com público",
            "✔ Mayor ingreso por empleado del mundo",
            "✔ Cultura corporativa sin jerarquías"
        ],
        "badge": "GABEN 📧",
        "bg_idx": 4
    },
    15: {
        "subtitle": "El monopolio del buen servicio",
        "bullets": [
            "✔ El PC gaming premia la excelencia",
            "✔ Mat Piscatella sobre la definición de monopolio",
            "✔ El valor incalculable de la confianza"
        ],
        "badge": "SERVICIOS 🤔",
        "bg_idx": 0
    }
}

from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_progress_bar

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
        title = re.sub(r'\([^\)]+\)', '', title).strip()
        
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

def draw_horizontal_frame(draw, width, height, title, subtitle, bullets, badge, font_title, font_sub, font_badge, blurred_bg_img, progress, effect_type="zoom_in", frame_idx=0):
    if blurred_bg_img:
        img_bg = get_ken_burns_crop(blurred_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
    draw_img = ImageDraw.Draw(img_bg)
    
    # 1. Radial Vignette Overlay
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    cx, cy = width // 2, height // 2
    max_dist = math.sqrt(cx*cx + cy*cy)
    for r_idx in range(0, 120, 15):
        alpha = int((r_idx / 120) * 180)
        v_draw.rectangle([r_idx, r_idx, width - r_idx, height - r_idx], outline=(0, 0, 0, alpha), width=15)
    img_bg = Image.alpha_composite(img_bg, vignette)
    draw_img = ImageDraw.Draw(img_bg)
    
    # 2. Bobbing floating card calculation
    bob_offset = int(12 * math.sin(2 * math.pi * frame_idx / 90))
    
    panel_w = 1280
    panel_h = 580
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + 30 + bob_offset
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    # 3. Dynamic blurred glassmorphic shadow
    shadow_offset = 15
    if not hasattr(draw_horizontal_frame, "shadow_blur"):
        shadow_mask = Image.new("L", (panel_w + 40, panel_h + 40), 0)
        ImageDraw.Draw(shadow_mask).rounded_rectangle([15, 15, panel_w + 15, panel_h + 15], radius=30, fill=150)
        draw_horizontal_frame.shadow_blur = shadow_mask.filter(ImageFilter.GaussianBlur(20))
        draw_horizontal_frame.shadow_color = Image.new("RGBA", (panel_w + 40, panel_h + 40), (0, 0, 0, 220))
    img_bg.paste(draw_horizontal_frame.shadow_color, (panel_left - 15 + shadow_offset, panel_top - 15 + shadow_offset), mask=draw_horizontal_frame.shadow_blur)
    
    # 4. Neon glassmorphic double borders
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(8, 14, 28, 220))
    # Outer glowing border
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=None, outline=(56, 189, 248, 120), width=3)
    # Inner border
    draw_img.rounded_rectangle([panel_left + 3, panel_top + 3, panel_right - 3, panel_bottom - 3], radius=21, fill=None, outline=(255, 255, 255, 180), width=1)
    
    bar_w = 1100
    bar_x = (width - bar_w) // 2
    bar_y = panel_top + 160
    draw_progress_bar(draw_img, bar_x, bar_y, bar_w, 8, progress, bg_color=(23, 28, 41, 255), fill_color=(56, 189, 248, 255))
    
    draw_img.text((width // 2, panel_top + 80), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, bar_y + 50), subtitle, font=font_sub, fill=(56, 189, 248, 255), anchor="mm")
    
    # 5. Active progressive bullet highlighting
    bullet_y = bar_y + 120
    for b_idx, b in enumerate(bullets):
        is_active = False
        if b_idx == 0 and progress < 0.33:
            is_active = True
        elif b_idx == 1 and 0.33 <= progress < 0.66:
            is_active = True
        elif b_idx >= 2 and progress >= 0.66:
            is_active = True
            
        display_text = b
        if is_active:
            display_text = b.replace("✔", "⮚")
            text_color = (253, 224, 71, 255) # Highlight Active yellow
        else:
            text_color = (180, 195, 210, 100) # Dim inactive bullets
            
        draw_img.text((width // 2, bullet_y), display_text, font=font_sub, fill=text_color, anchor="mm")
        bullet_y += 65
        
    if badge:
        badge_w = 260
        badge_h = 60
        badge_x = panel_right - badge_w - 40
        badge_y = panel_top + 40
        draw_img.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(56, 189, 248, 40), outline=(56, 189, 248, 200), width=2)
        draw_img.text((badge_x + badge_w // 2, badge_y + badge_h // 2), badge, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
    return img_bg.convert("RGB")

CHAPTER_MUSIC = {
    1: "Cipher2.mp3",          # Hegemonía (Tech/Intro)
    2: "Future Gladiator.mp3",  # Tasas 30% (Business)
    3: "Clash Defiant.mp3",     # Wolfire Lawsuit (Tension/Court)
    4: "Rites.mp3",             # Microsoft collusion (Conspiracy)
    5: "Volatile Reaction.mp3", # Ubisoft delisting threat (High Tension)
    6: "Cipher2.mp3",           # Tim Sweeney/Epic (Tech Battle)
    7: "Clash Defiant.mp3",     # EA/Ubisoft/Amazon failure (Action/Drama)
    8: "Future Gladiator.mp3",  # Corporate Interests (Intrigue)
    9: "Moorland.mp3",          # Valve's Golden Era (Nostalgia/Classics)
    10: "Rites.mp3",            # Private company structure (Calm/Business)
    11: "Take a Chance.mp3",    # Support & Steam Deck (Upbeat/Friendly)
    12: "Take a Chance.mp3",    # Family sharing (Upbeat/Friendly)
    13: "Take a Chance.mp3",    # Regional pricing (Upbeat/Friendly)
    14: "Moorland.mp3",         # Gabe Newell's mística (Nostalgia/Goodwill)
    15: "Moorland.mp3"          # Conclusion (Nostalgia/Goodwill)
}

def generate_dynamic_soundtrack(boundaries, temp_dir):
    print("Generating dynamic mood-based background soundtrack...")
    sliced_clips = []
    
    for idx, (start, end, title) in enumerate(boundaries):
        ch_num = idx + 1
        dur = end - start
        music_name = CHAPTER_MUSIC.get(ch_num, "Cipher2.mp3")
        music_path = os.path.join(MUSIC_DIR, music_name)
        
        sliced_file = os.path.join(temp_dir, f"music_seg_{idx:02d}.mp3")
        
        # Calculate clip start to make it dynamic
        music_dur = get_audio_duration(music_path)
        clip_start = (idx * 25.0) % (music_dur - dur - 5.0) if music_dur > (dur + 5.0) else 0.0
        
        # Apply 1.0s fade-in and 1.0s fade-out for smooth cross-fading
        cmd_slice_music = [
            "ffmpeg", "-y",
            "-ss", f"{clip_start:.2f}",
            "-i", music_path,
            "-t", f"{dur:.2f}",
            "-af", f"afade=t=in:ss=0:d=1,afade=t=out:st={dur-1.0:.2f}:d=1",
            "-c:a", "libmp3lame", "-q:a", "2",
            sliced_file
        ]
        subprocess.run(cmd_slice_music, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if os.path.exists(sliced_file) and os.path.getsize(sliced_file) > 0:
            sliced_clips.append(sliced_file)
            
    if not sliced_clips:
        return None
        
    # Write concat text file
    concat_txt_path = os.path.join(temp_dir, "music_concat.txt")
    with open(concat_txt_path, "w", encoding="utf-8") as f:
        for sc in sliced_clips:
            safe_path = sc.replace("\\", "/")
            f.write(f"file '{safe_path}'\n")
            
    output_bg_music = os.path.join(temp_dir, "dynamic_bg_music.mp3")
    cmd_concat_music = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt_path,
        "-c:a", "copy",
        output_bg_music
    ]
    subprocess.run(cmd_concat_music, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    if os.path.exists(output_bg_music) and os.path.getsize(output_bg_music) > 0:
        print(f"Dynamic background music generated successfully at {output_bg_music}")
        return output_bg_music
    return None

def draw_overlay_png(width, height, title, subtitle, bullets, badge, font_title, font_sub, font_badge, output_png):
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    panel_w = 1280
    panel_h = 580
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + 30
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    shadow_offset = 15
    if not hasattr(draw_overlay_png, "shadow_blur"):
        shadow_mask = Image.new("L", (panel_w + 40, panel_h + 40), 0)
        ImageDraw.Draw(shadow_mask).rounded_rectangle([15, 15, panel_w + 15, panel_h + 15], radius=30, fill=150)
        draw_overlay_png.shadow_blur = shadow_mask.filter(ImageFilter.GaussianBlur(20))
        draw_overlay_png.shadow_color = Image.new("RGBA", (panel_w + 40, panel_h + 40), (0, 0, 0, 220))
    img.paste(draw_overlay_png.shadow_color, (panel_left - 15 + shadow_offset, panel_top - 15 + shadow_offset), mask=draw_overlay_png.shadow_blur)
    
    draw.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(10, 18, 36, 145), outline=(255, 255, 255, 30), width=2)
    
    draw.text((width // 2, panel_top + 80), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw.text((width // 2, panel_top + 210), subtitle, font=font_sub, fill=(56, 189, 248, 255), anchor="mm")
    
    bullet_y = panel_top + 280
    for b in bullets:
        draw.text((width // 2, bullet_y), b, font=font_sub, fill=(210, 225, 245, 255), anchor="mm")
        bullet_y += 65
        
    if badge:
        badge_w = 260
        badge_h = 60
        badge_x = panel_right - badge_w - 40
        badge_y = panel_top + 40
        draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(56, 189, 248, 40), outline=(56, 189, 248, 200), width=2)
        draw.text((badge_x + badge_w // 2, badge_y + badge_h // 2), badge, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
    img.save(output_png, "PNG")

def compile_steam_video():
    script_path = os.path.join(BASE_DIR, "script_steam_long.md")
    audio_path = os.path.join(BASE_DIR, "audio_steam_long.mp3")
    output_path = os.path.join(BASE_DIR, "steam_essay_final.mp4")
    
    print("\n====================================================")
    print("KINESIO ESSAY COMPILER: THE HIDDEN WAR AGAINST STEAM")
    print("====================================================\n")
    
    generate_sfx_waves()
    
    audio_dur = get_audio_duration(audio_path)
    if audio_dur == 0.0:
        print(f"[ERROR] Audio track missing or empty: {audio_path}")
        return False
        
    print(f"Narrator Audio Track Duration: {audio_dur:.2f} seconds ({audio_dur/60.0:.2f} minutes)")
    boundaries = get_chapter_timestamps(script_path, audio_dur)
    
    temp_dir = os.path.join(BASE_DIR, "temp_render_steam")
    os.makedirs(temp_dir, exist_ok=True)
    
    width, height = 1920, 1080
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 34)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    
    # Pre-load all generated screenshots
    screenshots = {}
    for i in range(6):
        ss_path = os.path.join(SCREENSHOTS_DIR, f"steam_screenshot_{i}.jpg")
        if os.path.exists(ss_path):
            try:
                screenshots[i] = Image.open(ss_path)
                print(f"Loaded screenshot {i}: steam_screenshot_{i}.jpg")
            except Exception as e:
                print(f"Error loading screenshot {i}: {e}")
                
    segment_files = []
    
    # Compile each chapter segment
    for idx, (start, end, title) in enumerate(boundaries):
        ch_num = idx + 1
        dur = end - start
        seg_video = os.path.join(temp_dir, f"seg_{idx:02d}.mp4")
        
        # If segment is cached, skip render
        if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
            print(f"  [CACHE] Chapter {ch_num}: '{title}' already exists. Skipping render.")
            segment_files.append(seg_video)
            continue
            
        print(f"  [RENDER] Chapter {ch_num} ({dur:.2f}s): '{title}'")
        
        # SCRIPT RULE: Odd chapters (1, 3, 5, etc.) are PIL slides.
        # Even chapters (2, 4, 6, etc.) are game B-roll slices from trailers.
        if False: # Disabled gameplay B-rolls completely
            # Map an available trailer
            trailer_name = AVAILABLE_TRAILERS[(idx // 2) % len(AVAILABLE_TRAILERS)]
            trailer_file = os.path.join(TRAILERS_DIR, trailer_name)
            
            trailer_dur = get_audio_duration(trailer_file) if os.path.exists(trailer_file) else 0.0
            
            if trailer_dur > 10.0:
                print(f"    Slicing game B-roll from {trailer_name}...")
                clip_start = (idx * 20.0) % (trailer_dur - dur - 2.0) if trailer_dur > (dur + 2.0) else 0.0
                
                temp_slice = os.path.join(temp_dir, f"temp_slice_{idx}.mp4")
                cmd_slice = [
                    "ffmpeg", "-y",
                    "-ss", f"{clip_start:.2f}",
                    "-i", trailer_file,
                    "-t", f"{dur:.2f}",
                    "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
                    temp_slice
                ]
                subprocess.run(cmd_slice, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Draw the translucent glass panel overlay
                ch_info = CHAPTER_DATA.get(ch_num, {
                    "subtitle": "Análisis del mercado de PC gaming",
                    "bullets": ["✔ Liderazgo tecnológico", "✔ Preferencias del consumidor", "✔ Regulación del mercado"],
                    "badge": "STEAM 🌐",
                    "bg_idx": 0
                })
                overlay_png = os.path.join(temp_dir, f"overlay_{idx}.png")
                draw_overlay_png(width, height, title.upper(), f"Capítulo {ch_num}: {ch_info['subtitle']}", ch_info["bullets"], ch_info["badge"], font_title, font_sub, font_badge, overlay_png)
                
                # Overlay PNG on top of B-roll gameplay using FFmpeg
                cmd_overlay = [
                    "ffmpeg", "-y",
                    "-i", temp_slice,
                    "-i", overlay_png,
                    "-filter_complex", "[0:v][1:v]overlay=0:0",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
                    seg_video
                ]
                subprocess.run(cmd_overlay, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
                # Cleanup temp items
                try:
                    os.remove(temp_slice)
                    os.remove(overlay_png)
                except:
                    pass
            else:
                # Fallback to slides if trailer is not available
                print(f"    [WARNING] Trailer {trailer_name} not found. Falling back to static slide.")
                ch_num = 1 # Force slide branch
                
        # Odd chapters or fallback
        if ch_num % 2 == 1 or not os.path.exists(seg_video) or os.path.getsize(seg_video) == 0:
            ch_info = CHAPTER_DATA.get(ch_num, {
                "subtitle": "Análisis del mercado de PC gaming",
                "bullets": ["✔ Liderazgo tecnológico", "✔ Preferencias del consumidor", "✔ Regulación del mercado"],
                "badge": "STEAM 🌐",
                "bg_idx": 0
            })
            
            bg_idx = ch_info["bg_idx"]
            base_img = screenshots.get(bg_idx)
            
            # OPTIMIZATION: pre-blur the background image ONCE per chapter!
            blurred_bg_img = None
            if base_img:
                # Convert to RGBA and apply blur
                blurred_bg_img = base_img.convert("RGBA").filter(ImageFilter.GaussianBlur(18))
                # Add dark tint overlay once
                overlay = Image.new("RGBA", base_img.size, (8, 12, 24, 160))
                blurred_bg_img = Image.alpha_composite(blurred_bg_img, overlay)
                
            frame_dir = os.path.join(temp_dir, f"frames_{idx}")
            os.makedirs(frame_dir, exist_ok=True)
            
            total_frames = int(dur * 30)
            kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
            effect_type = kb_effects[idx % len(kb_effects)]
            
            t0 = time.time()
            for f_idx in range(total_frames):
                progress = f_idx / total_frames
                frame_img = draw_horizontal_frame(
                    None, width, height, title.upper(),
                    f"Capítulo {ch_num}: {ch_info['subtitle']}",
                    ch_info["bullets"], ch_info["badge"],
                    font_title, font_sub, font_badge,
                    blurred_bg_img, progress, effect_type=effect_type,
                    frame_idx=f_idx
                )
                frame_img.save(os.path.join(frame_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
                
            fps_render = total_frames / (time.time() - t0)
            print(f"    Rendered {total_frames} frames in {time.time()-t0:.1f}s ({fps_render:.1f} FPS)")
            
            cmd_frames = [
                "ffmpeg", "-y",
                "-framerate", "30",
                "-i", os.path.join(frame_dir, "frame_%05d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-t", f"{dur:.2f}",
                seg_video
            ]
            subprocess.run(cmd_frames, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Cleanup frame images right away to save disk space
            try:
                shutil.rmtree(frame_dir)
            except:
                pass
                
        if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
            segment_files.append(seg_video)
            
    # Concatenate all segment MP4s
    print("\nConcatenating all chapter video segments...")
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
    
    # Assemble multi-track audio: voiceover, BGM, and transition SFXs
    print("Assembling audio tracks and final multiplexing...")
    audio_inputs = ["-i", raw_video, "-i", audio_path]
    audio_mix_filter = "[1:a]volume=1.0[speech];"
    
    # Generate dynamic, cohesive background music matching the narrative arc of each chapter
    dynamic_bg_path = generate_dynamic_soundtrack(boundaries, temp_dir)
    use_bg = dynamic_bg_path is not None and os.path.exists(dynamic_bg_path)
    if use_bg:
        audio_inputs.extend(["-i", dynamic_bg_path])
        audio_mix_filter += "[2:a]volume=-24dB[bg_music];"
        
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
    
    print("Compiling final production MP4 file...")
    res = subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    try:
        shutil.rmtree(temp_dir)
    except:
        pass
        
    if res.returncode != 0:
        print(f"\n[ERROR] FFmpeg final build failed (code {res.returncode}):")
        print(res.stderr.decode('utf-8', errors='ignore'))
        return False
    else:
        print(f"\n====================================================")
        print(f"[SUCCESS] Video fully compiled at {output_path}")
        print("====================================================")
        return True

if __name__ == "__main__":
    compile_steam_video()
