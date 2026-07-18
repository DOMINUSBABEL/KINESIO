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

# Widescreen Essays configuration
ESSAYS_DATA = {
    "argentina_essay_1": {
        "title": "EL FACTOR SOBERBIA Y EL ÉXITO",
        "badge": "ARGENTINOFOBIA ⚽",
        "music": "Volatile Reaction.mp3",
        "bg_name": "argentina_stadium.jpg",
        "chapters": {
            1: {"subtitle": "Mito: El hincha argentino es agrandado por naturaleza", "bullets": ["✔ Visto desde fuera como arrogancia", "✔ Para ellos es 'chicana' y folklore", "✔ Fina línea entre confianza y soberbia"], "badge": "SOBERBIA 😤"},
            2: {"subtitle": "Mito: Los cantos de cancha son solo folklore", "bullets": ["✔ Letras hirientes sobre crisis y derrotas", "✔ Humillación que enfurece al rival", "✔ El debate ético sobre los estadios"], "badge": "CÁNTICOS 🗣"},
            3: {"subtitle": "Mito: Argentina es el centro de atención injustamente", "bullets": ["✔ Búsqueda mediática de protagonismo", "✔ Monopolio informativo en redes sociales", "✔ Deseo global de ver caer al campeón"], "badge": "EGO 👑"},
            4: {"subtitle": "Mito: El rechazo a Argentina no tiene sentido", "bullets": ["✔ Envidia natural por su éxito histórico", "✔ Tres Copas del Mundo y múltiples títulos", "✔ La tendencia de apoyar al más débil"], "badge": "ÉXITO 🏆"},
            5: {"subtitle": "Mito: Su forma de vivir el fútbol es insana", "bullets": ["✔ El fútbol se vive como una religión", "✔ Pasión extrema que asusta a otras culturas", "✔ Lealtad incomprensible para el extranjero"], "badge": "PASIÓN 🔥"},
            6: {"subtitle": "Mito: Su tono de voz es siempre altanero", "bullets": ["✔ El humor ácido y la ironía rioplatense", "✔ Tono directo que genera rechazo previo", "✔ Barrera idiomática en Latinoamérica"], "badge": "CULTURA 🗣"}
        }
    },
    "argentina_essay_2": {
        "title": "LA SOSPECHA ARBITRAL Y POLÉMICAS",
        "badge": "EN LA CANCHA ⚽",
        "music": "Volatile Reaction.mp3",
        "bg_name": "referee_red_card.jpg",
        "chapters": {
            1: {"subtitle": "Mito: El Mundial de Qatar fue un regalo", "bullets": ["✔ Polémica por los penales cobrados", "✔ Narrativa del 'Mundial comprado' en redes", "✔ Sombra de sospecha sobre el campeón"], "badge": "QATAR 2022 🇶🇦"},
            2: {"subtitle": "Mito: El Dibu Martínez es maleducado", "bullets": ["✔ Provocaciones y bailes polémicos", "✔ Héroe local y enemigo en el exterior", "✔ Guerra psicológica brillante en el arco"], "badge": "EL DIBU 🧤"},
            3: {"subtitle": "Mito: El plantel argentino juega sucio", "bullets": ["✔ Estilo de juego agresivo e intimidante", "✔ Rodrigo De Paul y Cuti Romero al límite", "✔ Disciplina al borde del reglamento"], "badge": "AGRESIVIDAD ⚔"},
            4: {"subtitle": "Mito: FIFA siempre favorece a Lionel Messi", "bullets": ["✔ Teoría de protección para cuidar el negocio", "✔ Análisis microscópico de faltas no cobradas", "✔ Impunidad percibida por sus detractores"], "badge": "FAVORITISMO ⚖"},
            5: {"subtitle": "Mito: Sus declaraciones no tienen filtros", "bullets": ["✔ Tono descontracturado y desafiante", "✔ Falta de humildad vista por la prensa", "✔ Amplificación mediática de la polémica"], "badge": "PRENSA 🎙"},
            6: {"subtitle": "Mito: Argentina es el villano por capricho", "bullets": ["✔ Rol natural de antagonista en el fútbol", "✔ Aporta drama y emoción extrema al juego", "✔ La narrativa de cine en cada torneo"], "badge": "ANTAGONISTA 🎭"}
        }
    },
    "argentina_essay_3": {
        "title": "GEOPOLÍTICA, XENOFOBIA Y REDES",
        "badge": "CONFLITOS Y REDES ⚽",
        "music": "Volatile Reaction.mp3",
        "bg_name": "messi_celebration.jpg",
        "chapters": {
            1: {"subtitle": "Mito: Inglaterra es solo un partido más", "bullets": ["✔ Tensión geopolítica por las Malvinas", "✔ El partido del 86 y el gol con la mano", "✔ La revancha patriótica de Diego Maradona"], "badge": "MALVINAS 🇬🇧"},
            2: {"subtitle": "Mito: El clásico con Brasil es solo deportivo", "bullets": ["✔ Guerra cultural por el trono de Sudamérica", "✔ Incidentes violentos en estadios como el Maracaná", "✔ Duelo constante entre Pelé y Maradona"], "badge": "BRASIL 🇧🇷"},
            3: {"subtitle": "Mito: La rivalidad con México es pacífica", "bullets": ["✔ Batalla digital campal en redes sociales", "✔ Insultos clasistas y descalificaciones mutuas", "✔ Anonimato web radicaliza el folklore"], "badge": "MÉXICO 🇲🇽"},
            4: {"subtitle": "Mito: El canto contra Francia fue inofensivo", "bullets": ["✔ Incidentes tras Copa América desatan polémica", "✔ Acusaciones de racismo y xenofobia en Europa", "✔ Choque sobre los límites del humor"], "badge": "FRANCIA 🇫🇷"},
            5: {"subtitle": "Mito: El odio a Argentina es orgánico", "bullets": ["✔ Algoritmos premian el rechazo viral", "✔ Memes y clics fáciles usando el antiargentinismo", "✔ Secciones de comentarios polarizadas"], "badge": "ALGORITMOS 📱"},
            6: {"subtitle": "Mito: Hay un odio real y profundo en el fútbol", "bullets": ["✔ El folklore deportivo es un teatro", "✔ La pasión extrema une y divide a la vez", "✔ Al apagar la pantalla, la rivalidad muere"], "badge": "FOLKLORE 🎭"}
        }
    }
}

# Shorts configuration
SHORTS_DATA = {}
shorts_titles_c4 = [
    "El Mito del 'Agrandado' Argentino 😤",
    "¿Por Qué Hinchas Cantan Así? 🗣",
    "El Precio de la Gloria Deportiva 🏆",
    "La Pasión que Asusta al Mundo 🔥",
    "El Choque Rioplatense de Voces 🗣",
    "¿Un Mundial Comprado en Qatar? 🇶🇦",
    "El Dibu Martínez: ¿Genio o Loco? 🧤",
    "El Juego Rudo de la Albiceleste ⚔",
    "¿Protege FIFA a Lionel Messi? 🐐",
    "La Honestidad Brutal en Prensa 🎙",
    "Inglaterra vs Argentina: Malvinas 🇬🇧",
    "Brasil vs Argentina: Guerra por Trono 🇧🇷",
    "El Tenso Choque con México 🇲🇽",
    "El Escándalo del Canto a Francia 🇫🇷",
    "El Gran Negocio del Odio Digital 📱",
    "¿Es Odio Real o Solo Folklore? 🎭"
]

for idx in range(16):
    essay_num = 1 if idx < 5 else (2 if idx < 10 else 3)
    short_num = (idx % 5) + 1 if idx < 5 else ((idx - 5) % 5 + 1 if idx < 10 else (idx - 10) % 6 + 1)
    key = f"argentina_essay_{essay_num}_short_{short_num}"
    
    SHORTS_DATA[key] = {
        "title": shorts_titles_c4[idx],
        "badge": "FÚTBOL RIVALIDAD ⚽",
        "music": "Volatile Reaction.mp3",
        "bg_name": "argentina_stadium.jpg" if idx % 3 == 0 else ("referee_red_card.jpg" if idx % 3 == 1 else "messi_celebration.jpg")
    }

from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_progress_bar

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

def get_chapter_timestamps(script_path, total_duration, key):
    if not os.path.exists(script_path):
        return []
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    parts = content.split(f"## 📌 {key}")
    if len(parts) < 2:
        return []
    block = parts[1].strip()
    subparts = block.split("\n## 📌 ")
    target_block = subparts[0].strip()
    
    chapters = target_block.split("### 📌 Capítulo ")
    sections = []
    total_words = 0
    for ch in chapters[1:]:
        lines = ch.split('\n')
        title_line = lines[0].strip()
        title = title_line.split(":")[-1].strip() if ":" in title_line else title_line
        
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

def draw_horizontal_frame(draw, width, height, title, subtitle, bullets, badge, font_title, font_sub, font_badge, blurred_bg_img, progress, effect_type="zoom_in"):
    if blurred_bg_img:
        img_bg = get_ken_burns_crop(blurred_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
    draw_img = ImageDraw.Draw(img_bg)
    
    # 1. Radial Vignette (Deep dark blue/black borders for football aesthetic)
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for r in range(0, int(width * 0.85), 15):
        alpha = int((r / (width * 0.85)) ** 2.2 * 190)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(5, 6, 12, alpha), width=16)
    img_bg = Image.alpha_composite(img_bg, vignette)
    draw_img = ImageDraw.Draw(img_bg)
    
    # 2. Card Float Animation
    float_offset = int(math.sin(progress * math.pi * 2.0) * 8.0)
    
    # Card Coordinates
    panel_w = 1200
    panel_h = 600
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + 10 + float_offset
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    # Argentine Flag Colors: Neon Light Blue and White
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(10, 14, 28, 165), outline=(116, 172, 223, 50), width=2)
    draw_img.rounded_rectangle([panel_left - 3, panel_top - 3, panel_right + 3, panel_bottom + 3], radius=27, fill=(0, 0, 0, 0), outline=(255, 255, 255, 20), width=2)
    
    # Text Drawing
    draw_img.text((width // 2, panel_top + 80), title.upper(), font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, panel_top + 210), subtitle, font=font_sub, fill=(116, 172, 223, 255), anchor="mm")
    
    # Active bullet highlight logic
    num_bullets = len(bullets)
    active_b_idx = int(progress * num_bullets)
    active_b_idx = min(active_b_idx, num_bullets - 1)
    
    bullet_y = panel_top + 295
    for idx_b, b in enumerate(bullets):
        if idx_b == active_b_idx:
            glow_alpha = int(140 + math.sin(time.time() * 8) * 40)
            draw_img.text((width // 2, bullet_y), b, font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
            t_w = draw_img.textlength(b, font=font_sub)
            draw_img.line([width//2 - t_w//2, bullet_y + 26, width//2 + t_w//2, bullet_y + 26], fill=(116, 172, 223, glow_alpha), width=2)
        else:
            draw_img.text((width // 2, bullet_y), b, font=font_sub, fill=(130, 150, 180, 220), anchor="mm")
        bullet_y += 70
        
    # Badge
    if badge:
        badge_w = 280
        badge_h = 60
        badge_x = panel_right - badge_w - 40
        badge_y = panel_top + 40
        draw_img.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(116, 172, 223, 40), outline=(116, 172, 223, 200), width=2)
        draw_img.text((badge_x + badge_w // 2, badge_y + badge_h // 2), badge, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
    # Progress Bar at the bottom of the card
    bar_w = panel_w
    bar_x = panel_left
    bar_y = panel_bottom + 15
    draw_progress_bar(draw_img, bar_x, bar_y, bar_w, 8, progress)
    
    return img_bg

def draw_vertical_short_frame(draw, width, height, title, badge, active_words, font_title, font_sub, font_badge, font_act, font_side, sharp_bg_img, progress, effect_type="zoom_in"):
    if sharp_bg_img:
        img_bg = get_ken_burns_crop(sharp_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Vignette
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for r in range(0, int(height * 0.75), 20):
        alpha = int((r / (height * 0.75)) ** 1.8 * 210)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(6, 8, 16, alpha), width=22)
    img_bg = Image.alpha_composite(img_bg, vignette)
    draw_img = ImageDraw.Draw(img_bg)
    
    # Float animation
    float_offset = int(math.sin(progress * math.pi * 2.0) * 6.0)
    
    # Top Card
    card_w = 900
    card_h = 240
    card_left = (width - card_w) // 2
    card_top = 120 + float_offset
    card_right = card_left + card_w
    card_bottom = card_top + card_h
    
    # Double Neon Border Card (Sky Blue & White)
    draw_img.rounded_rectangle([card_left, card_top, card_right, card_bottom], radius=24, fill=(10, 14, 28, 170), outline=(116, 172, 223, 60), width=2)
    draw_img.rounded_rectangle([card_left - 3, card_top - 3, card_right + 3, card_bottom + 3], radius=27, fill=(0, 0, 0, 0), outline=(255, 255, 255, 20), width=2)
    
    # Card Text
    draw_img.text((width // 2, card_top + 60), badge, font=font_badge, fill=(116, 172, 223, 255), anchor="mm")
    draw_img.text((width // 2, card_top + 140), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    
    # Caption Box
    prev_w, active_w, next_w = active_words
    cap_y = height // 2 + 100
    
    active_clean = re.sub(r'[^\wáéíóúÁÉÍÓÚñÑ]', '', active_w).upper()
    prev_clean = prev_w.lower()
    next_clean = next_w.lower()
    
    if len(prev_clean) > 10: prev_clean = prev_clean[:9] + "..."
    if len(next_clean) > 10: next_clean = next_clean[:9] + "..."
    
    # Active Word pill background
    act_w = draw_img.textlength(active_clean, font=font_act)
    pill_padding_x = 40
    pill_padding_y = 25
    pill_left = width // 2 - act_w // 2 - pill_padding_x
    pill_top = cap_y - pill_padding_y
    pill_right = width // 2 + act_w // 2 + pill_padding_x
    pill_bottom = cap_y + font_act.size + pill_padding_y
    
    # Blue capsule outline
    draw_img.rounded_rectangle([pill_left, pill_top, pill_right, pill_bottom], radius=16, fill=(10, 14, 28, 195), outline=(116, 172, 223, 130), width=3)
    
    draw_img.text((width // 2, cap_y), active_clean, font=font_act, fill=(255, 255, 255, 255), anchor="mt")
    
    if prev_clean:
        draw_img.text((width // 2 - act_w // 2 - 120, cap_y + 15), prev_clean, font=font_side, fill=(160, 180, 200, 140), anchor="rm")
    if next_clean:
        draw_img.text((width // 2 + act_w // 2 + 120, cap_y + 15), next_clean, font=font_side, fill=(160, 180, 200, 140), anchor="lm")
        
    # Progress Bar at the bottom
    bar_padding = 80
    bar_w = width - bar_padding * 2
    bar_y = height - 140
    draw_img.line([bar_padding, bar_y, width - bar_padding, bar_y], fill=(255, 255, 255, 20), width=6)
    draw_img.line([bar_padding, bar_y, bar_padding + int(bar_w * progress), bar_y], fill=(116, 172, 223, 220), width=6)
    
    return img_bg

def compile_videos():
    script_path = os.path.join(BASE_DIR, "scripts_argentina_rivalries.md")
    
    print("\n====================================================")
    print("CAMPAIGN 4 VIDEOS COMPILER (ARGENTINA RIVALRIES)")
    print("====================================================\n")
    
    width_h, height_h = 1920, 1080
    width_v, height_v = 1080, 1920
    
    font_title_h = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub_h = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 34)
    font_badge_h = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    
    font_title_v = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 46)
    font_sub_v = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 32)
    font_badge_v = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 30)
    
    font_caption_active = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 64)
    font_caption_side = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 36)
    
    # Load custom backgrounds
    bgs = {}
    for name in ["argentina_stadium.jpg", "referee_red_card.jpg", "messi_celebration.jpg"]:
        bg_path = os.path.join(SCREENSHOTS_DIR, name)
        if os.path.exists(bg_path):
            try:
                bgs[name] = Image.open(bg_path)
                print(f"Loaded visual asset background: {name}")
            except Exception as e:
                print(f"Error loading background {name}: {e}")
                
    # --------------------------------------
    # 1. COMPILE WIDESCREEN VIDEO ESSAYS
    # --------------------------------------
    for key, info in ESSAYS_DATA.items():
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Video essay '{key}' already exists on disk. Skipping.")
            continue
            
        print(f"\nCompiling Video Essay: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio track missing for {key}. Skipping.")
            continue
            
        boundaries = get_chapter_timestamps(script_path, audio_dur, key)
        if not boundaries:
            print(f"  [ERROR] Failed to parse boundaries for {key}. Skipping.")
            continue
            
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        segment_files = []
        
        base_img = bgs.get(info["bg_name"])
        blurred_bg_img = None
        if base_img:
            blurred_bg_img = base_img.convert("RGBA").filter(ImageFilter.GaussianBlur(12))
            overlay = Image.new("RGBA", base_img.size, (5, 6, 12, 160)) # Deep dark overlay
            blurred_bg_img = Image.alpha_composite(blurred_bg_img, overlay)
            
        for idx_ch, (start, end, ch_title) in enumerate(boundaries):
            ch_num = idx_ch + 1
            dur = end - start
            seg_video = os.path.join(temp_dir, f"seg_{idx_ch:02d}.mp4")
            
            if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
                print(f"  [CACHE] Chapter {ch_num}: '{ch_title}' exists. Skipping.")
                segment_files.append(seg_video)
                continue
                
            print(f"  [RENDER] Chapter {ch_num} ({dur:.2f}s): '{ch_title}'")
            
            ch_info = info["chapters"].get(ch_num, {})
            frame_dir = os.path.join(temp_dir, f"frames_{idx_ch}")
            os.makedirs(frame_dir, exist_ok=True)
            total_frames = int(dur * 30)
            
            kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
            effect_type = kb_effects[idx_ch % len(kb_effects)]
            
            t0 = time.time()
            for f_idx in range(total_frames):
                progress = f_idx / total_frames
                frame_img = draw_horizontal_frame(
                    None, width_h, height_h, ch_title,
                    f"Capítulo {ch_num}: {ch_info.get('subtitle','')}",
                    ch_info.get("bullets", []), ch_info.get("badge",""),
                    font_title_h, font_sub_h, font_badge_h,
                    blurred_bg_img, progress, effect_type=effect_type
                )
                frame_img.convert("RGB").save(os.path.join(frame_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
                
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
            try:
                shutil.rmtree(frame_dir)
            except:
                pass
                
            if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
                segment_files.append(seg_video)
                
        print("\nConcatenating all chapter segments...")
        raw_video = os.path.join(temp_dir, "raw_video.mp4")
        concat_inputs = []
        filter_concat_parts = []
        for i_seg, sf in enumerate(segment_files):
            concat_inputs.extend(["-i", sf])
            filter_concat_parts.append(f"[{i_seg}:v]")
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
        
        print("Assembling audio tracks with Volatile Reaction.mp3 background...")
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.0[speech];"
        
        bg_music_path = os.path.join(MUSIC_DIR, info["music"])
        use_bg = os.path.exists(bg_music_path)
        if use_bg:
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
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
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
            
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Video essay compiled: {output_path}")
        else:
            print(f"  [FAILED] Compile failed for {key}")

    # --------------------------------------
    # 2. COMPILE VERTICAL SHORTS
    # --------------------------------------
    print("\nStarting compilation of the 16 Campaign 4 Shorts...")
    for idx, (key, info) in enumerate(SHORTS_DATA.items()):
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Short '{key}' already exists on disk. Skipping.")
            continue
            
        print(f"Compiling Campaign 4 Short: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio missing for {key}. Skipping.")
            continue
            
        script_text = extract_short_text(script_path, key)
        words = script_text.split()
        total_words = len(words)
        
        base_img = bgs.get(info["bg_name"])
        sharp_bg_img = None
        if base_img:
            bg_scale = 1.4
            bg_w = int(width_v * bg_scale)
            bg_h = int(height_v * bg_scale)
            sharp_bg_img = base_img.resize((bg_w, bg_h)).convert("RGBA")
            
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        total_frames = int(audio_dur * 30)
        
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
                None, width_v, height_v,
                info["title"], info["badge"],
                (prev_w, active_w, next_w),
                font_title_v, font_sub_v, font_badge_v,
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
        
        # Clause pop pause SFX
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
    compile_videos()
