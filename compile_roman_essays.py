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

AVAILABLE_TRAILERS = [
    "wewhoare_trailer.mp4",
    "warband_trailer.mp4",
    "pathfinder_wrath_of_the_righteous_trailer.mp4",
    "chaosbane_trailer.mp4"
]

ESSAYS_DATA = {
    "augusto_essay": {
        "title": "AUGUSTO: EL ARQUITECTO DEL IMPERIO",
        "badge": "PAX ROMANA 🏛",
        "chapters": {
            1: {
                "subtitle": "El Sucesor Oculto",
                "bullets": [
                    "✔ Sucesor de Julio César a los 18 años",
                    "✔ Venganza sangrienta del Segundo Triunvirato",
                    "✔ Derrota de Marco Antonio en Actio"
                ],
                "badge": "EL SUCESOR ⚔",
                "bg_idx": 0
            },
            2: {
                "subtitle": "Las Luces de la Pax Romana",
                "bullets": [
                    "✔ Monarquía oculta bajo ropaje republicano",
                    "✔ Fundación de Pax Romana y ejército estable",
                    "✔ 'Encontré Roma en ladrillo y la dejé en mármol'"
                ],
                "badge": "PAX ROMANA 🏛",
                "bg_idx": 0
            },
            3: {
                "subtitle": "Las Sombras del Actor",
                "bullets": [
                    "✔ Destierro implacable de su propia hija Julia",
                    "✔ Desastre de Teutoburgo: 'Varo, devuélveme mis legiones'",
                    "✔ Último acto: 'Si he actuado bien, aplaudid'"
                ],
                "badge": "EL ACTOR 🎭",
                "bg_idx": 0
            }
        }
    },
    "trajano_essay": {
        "title": "TRAJANO: EL EMPERADOR MILITAR",
        "badge": "OPTIMUS PRINCEPS ⚔",
        "chapters": {
            1: {
                "subtitle": "El Soldado del Rin",
                "bullets": [
                    "✔ General hispano adoptado por Nerva",
                    "✔ Primer emperador provincial de Roma",
                    "✔ Camaradería absoluta con sus soldados"
                ],
                "badge": "EL SOLDADO 🛡",
                "bg_idx": 1
            },
            2: {
                "subtitle": "Las Luces del Imperio Máximo",
                "bullets": [
                    "✔ Conquistas dacias y captura de riquezas reales",
                    "✔ Foro y Columna de Trajano erigidos en Roma",
                    "✔ Programas sociales alimentarios infantiles"
                ],
                "badge": "OPTIMUS 🏆",
                "bg_idx": 1
            },
            3: {
                "subtitle": "Las Sombras de la Extensión",
                "bullets": [
                    "✔ Campaña de Partia estira las líneas logísticas",
                    "✔ Estallido de rebelión judía en Oriente",
                    "✔ Muerte en Cilicia y abandono de conquistas"
                ],
                "badge": "EXTENSIÓN 💥",
                "bg_idx": 1
            }
        }
    },
    "aureliano_essay": {
        "title": "AURELIANO: RESTAURADOR DE ROMA",
        "badge": "RESTITUTOR ORBIS 🛡",
        "chapters": {
            1: {
                "subtitle": "El Siglo del Caos",
                "bullets": [
                    "✔ Ascenso al trono en la Crisis del Siglo III",
                    "✔ Imperio fragmentado en tres secciones autónomas",
                    "✔ Disciplina militar indomable ante la invasión"
                ],
                "badge": "CRISIS III ⚔",
                "bg_idx": 2
            },
            2: {
                "subtitle": "Las Luces del Restaurador",
                "bullets": [
                    "✔ Edificación de murallas defensivas de Roma",
                    "✔ Derrota de Zenobia de Palmira y del Imperio Galo",
                    "✔ Reunificación territorial en solo 4 años"
                ],
                "badge": "REUNIFICACIÓN 🗺",
                "bg_idx": 2
            },
            3: {
                "subtitle": "Las Sombras del Autócrata",
                "bullets": [
                    "✔ Masacre obrera en la ceca de Roma",
                    "✔ Establecimiento del culto absolutista del Sol Invictus",
                    "✔ Asesinato a traición debido a lista falsa"
                ],
                "badge": "EL COMPLOT ☠",
                "bg_idx": 2
            }
        }
    },
    "constantino_essay": {
        "title": "CONSTANTINO: EL VISIONARIO DE LA FE",
        "badge": "NUEVA ROMA ✝",
        "chapters": {
            1: {
                "subtitle": "El Puente de la Visión",
                "bullets": [
                    "✔ Batalla decisiva en el Puente Milvio",
                    "✔ Visión mística de cruz: 'Con este signo vencerás'",
                    "✔ Adopción de símbolos cristianos en escudos"
                ],
                "badge": "MILVIO 312 ⚔",
                "bg_idx": 3
            },
            2: {
                "subtitle": "Las Luces de la Tolerancia",
                "bullets": [
                    "✔ Promulgación del Edicto de Milán en 313",
                    "✔ Convocatoria del Concilio ecuménico de Nicea",
                    "✔ Fundación de Constantinopla como capital"
                ],
                "badge": "TOLERANCIA 📜",
                "bg_idx": 3
            },
            3: {
                "subtitle": "Las Sombras del Palacio",
                "bullets": [
                    "✔ Ejecución misteriosa de su hijo Crispo",
                    "✔ Muerte de su esposa Fausta en baño hirviendo",
                    "✔ Bautismo demorado hasta su lecho de muerte"
                ],
                "badge": "TRAGEDIA 🎭",
                "bg_idx": 3
            }
        }
    },
    "mayoriano_essay": {
        "title": "MAYORIANO: EL ÚLTIMO HÉROE DE ROMA",
        "badge": "EL ÚLTIMO HÉROE 🕯",
        "chapters": {
            1: {
                "subtitle": "El Crepúsculo de Occidente",
                "bullets": [
                    "✔ Colapso inminente de Occidente en el siglo V",
                    "✔ Invasiones bárbaras constantes sobre Italia",
                    "✔ Ascenso al trono y reformas contra corrupción"
                ],
                "badge": "AGONÍA 🏛",
                "bg_idx": 4
            },
            2: {
                "subtitle": "Las Luces de la Reconquista",
                "bullets": [
                    "✔ Campaña militar reconquista Galia e Hispania",
                    "✔ Construcción de flota romana en Alicante",
                    "✔ Elogiado como el último gran carácter romano"
                ],
                "badge": "MILAGRO 🛡",
                "bg_idx": 4
            },
            3: {
                "subtitle": "Las Sombras de la Traición",
                "bullets": [
                    "✔ Destrucción de flota en Alicante por traidores",
                    "✔ Arrestado y ejecutado por el general Ricimero",
                    "✔ Fin definitivo de la fuerza militar de Occidente"
                ],
                "badge": "TRAICIÓN ⚔",
                "bg_idx": 4
            }
        }
    },
    "justiniano_essay": {
        "title": "JUSTINIANO: EL SUEÑO DE OCCIDENTE",
        "badge": "RENOVATIO IMPERII 👑",
        "chapters": {
            1: {
                "subtitle": "El Campesino que no Dormía",
                "bullets": [
                    "✔ Origen campesino humilde en los Balcanes",
                    "✔ Teodora como cogobernante imperial firme",
                    "✔ Obsesión con reconquistar el imperio de Occidente"
                ],
                "badge": "EL SUEÑO 📜",
                "bg_idx": 5
            },
            2: {
                "subtitle": "Las Luces del Derecho",
                "bullets": [
                    "✔ Reconquista de Italia, África y sur de Hispania",
                    "✔ Construcción de la Catedral de Santa Sofía",
                    "✔ Recopilación del Corpus Juris Civilis"
                ],
                "badge": "DERECHO 🏛",
                "bg_idx": 5
            },
            3: {
                "subtitle": "Las Sombras de Nika",
                "bullets": [
                    "✔ Masacre en Hipódromo: 30.000 ciudadanos muertos",
                    "✔ Epidemia devastadora de la Peste de Justiniano",
                    "✔ Arcas estatales agotadas por guerras costosas"
                ],
                "badge": "LA PESTE 💀",
                "bg_idx": 5
            }
        }
    }
}

from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_progress_bar

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
    # Bullet 1 active: progress < 0.33
    # Bullet 2 active: 0.33 <= progress < 0.66
    # Bullet 3 active: progress >= 0.66
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
    1: "Rites.mp3",
    2: "Clash Defiant.mp3",
    3: "Moorland.mp3"
}

def generate_dynamic_soundtrack(boundaries, temp_dir):
    print("Generating dynamic mood-based background soundtrack...")
    sliced_clips = []
    for idx, (start, end, title) in enumerate(boundaries):
        ch_num = idx + 1
        dur = end - start
        music_name = CHAPTER_MUSIC.get(ch_num, "Moorland.mp3")
        music_path = os.path.join(MUSIC_DIR, music_name)
        
        sliced_file = os.path.join(temp_dir, f"music_seg_{idx:02d}.mp3")
        music_dur = get_audio_duration(music_path)
        clip_start = (idx * 25.0) % (music_dur - dur - 5.0) if music_dur > (dur + 5.0) else 0.0
        
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

def compile_roman_essays():
    script_path = os.path.join(BASE_DIR, "scripts_roman_essays.md")
    
    print("\n====================================================")
    print("KINESIO ESSAYS COMPILER: ROMAN EMPERORS CHRONICLES")
    print("====================================================\n")
    
    width, height = 1920, 1080
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 34)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    
    # Preload Roman screenshots (Augustus to Justinian)
    screenshots = {}
    for i in range(6):
        ss_path = os.path.join(SCREENSHOTS_DIR, f"roman_screenshot_{i}.jpg")
        if os.path.exists(ss_path):
            try:
                screenshots[i] = Image.open(ss_path)
                print(f"Loaded screenshot {i}: roman_screenshot_{i}.jpg")
            except Exception as e:
                print(f"Error loading screenshot {i}: {e}")
                
    for idx_essay, (key, info) in enumerate(ESSAYS_DATA.items()):
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Video essay '{key}' already exists. Skipping.")
            continue
            
        print(f"\nCompiling Video Essay: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio track missing for {key}. Skipping.")
            continue
            
        boundaries = get_chapter_timestamps(script_path, audio_dur, key)
        temp_dir = os.path.join(BASE_DIR, f"temp_render_{key}")
        os.makedirs(temp_dir, exist_ok=True)
        segment_files = []
        
        for idx_ch, (start, end, ch_title) in enumerate(boundaries):
            ch_num = idx_ch + 1
            dur = end - start
            seg_video = os.path.join(temp_dir, f"seg_{idx_ch:02d}.mp4")
            
            if os.path.exists(seg_video) and os.path.getsize(seg_video) > 0:
                print(f"  [CACHE] Chapter {ch_num}: '{ch_title}' exists. Skipping.")
                segment_files.append(seg_video)
                continue
                
            print(f"  [RENDER] Chapter {ch_num} ({dur:.2f}s): '{ch_title}'")
            
            # SCRIPT RULE: Odd chapters (1, 3) are PIL slides with Roman screenshots.
            # Even chapters (2) are B-roll slices from combat/historical trailers.
            if False: # Disabled gameplay B-rolls completely
                trailer_name = AVAILABLE_TRAILERS[(idx_ch + idx_essay) % len(AVAILABLE_TRAILERS)]
                trailer_file = os.path.join(TRAILERS_DIR, trailer_name)
                trailer_dur = get_audio_duration(trailer_file) if os.path.exists(trailer_file) else 0.0
                
                if trailer_dur > 10.0:
                    print(f"    Slicing B-roll from {trailer_name}...")
                    clip_start = (idx_ch * 20.0) % (trailer_dur - dur - 2.0) if trailer_dur > (dur + 2.0) else 0.0
                    temp_slice = os.path.join(temp_dir, f"temp_slice_{idx_ch}.mp4")
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
                    
                    ch_info = info["chapters"].get(ch_num, {})
                    overlay_png = os.path.join(temp_dir, f"overlay_{idx_ch}.png")
                    draw_overlay_png(width, height, ch_title.upper(), f"Capítulo {ch_num}: {ch_info.get('subtitle','')}", ch_info.get("bullets",[]), ch_info.get("badge",""), font_title, font_sub, font_badge, overlay_png)
                    
                    cmd_overlay = [
                        "ffmpeg", "-y",
                        "-i", temp_slice,
                        "-i", overlay_png,
                        "-filter_complex", "[0:v][1:v]overlay=0:0",
                        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-an",
                        seg_video
                    ]
                    subprocess.run(cmd_overlay, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    try:
                        os.remove(temp_slice)
                        os.remove(overlay_png)
                    except:
                        pass
                else:
                    print(f"    [WARNING] Trailer {trailer_name} not found. Falling back to slide.")
                    ch_num = 1
                    
            if ch_num % 2 == 1 or not os.path.exists(seg_video) or os.path.getsize(seg_video) == 0:
                ch_info = info["chapters"].get(ch_num, {})
                bg_idx = ch_info.get("bg_idx", 0)
                base_img = screenshots.get(bg_idx)
                
                blurred_bg_img = None
                if base_img:
                    blurred_bg_img = base_img.convert("RGBA").filter(ImageFilter.GaussianBlur(12))
                    overlay = Image.new("RGBA", base_img.size, (8, 12, 24, 160))
                    blurred_bg_img = Image.alpha_composite(blurred_bg_img, overlay)
                    
                frame_dir = os.path.join(temp_dir, f"frames_{idx_ch}")
                os.makedirs(frame_dir, exist_ok=True)
                total_frames = int(dur * 30)
                kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
                effect_type = kb_effects[idx_ch % len(kb_effects)]
                
                t0 = time.time()
                for f_idx in range(total_frames):
                    progress = f_idx / total_frames
                    frame_img = draw_horizontal_frame(
                        None, width, height, ch_title.upper(),
                        f"Capítulo {ch_num}: {ch_info.get('subtitle','')}",
                        ch_info.get("bullets", []), ch_info.get("badge",""),
                        font_title, font_sub, font_badge,
                        blurred_bg_img, progress, effect_type=effect_type
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
        
        print("Assembling audio tracks...")
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.0[speech];"
        
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
        subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            shutil.rmtree(temp_dir)
        except:
            pass
            
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Video essay compiled: {output_path}")
        else:
            print(f"  [FAILED] Compile failed for {key}")

if __name__ == "__main__":
    compile_roman_essays()
