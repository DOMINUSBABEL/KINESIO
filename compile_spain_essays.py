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
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

ESSAYS_DATA = {
    "spain_essay_1": {
        "essay_num": 1,
        "badge": "MUNDIAL 2026 🏆",
        "music": "Clash Defiant.mp3",
        "bg_screenshots": ["spain_team", "referee_red_card", "spain_trophy"],
        "chapters": {
            1: {"subtitle": "El Camino al MetLife", "badge": "EL CAMINO 🇪🇸", "bullets": ["Fase de grupos impecable", "El liderazgo de de la Fuente", "La unión del vestuario"]},
            2: {"subtitle": "El Plan de Luis de la Fuente", "badge": "PIZARRA TÁCTICA 📋", "bullets": ["Mediocampo asfixiante", "Presión alta coordinada", "Rodri en el eje central"]},
            3: {"subtitle": "La Resistencia de Argentina", "badge": "LA ALBICELESTE 🇦🇷", "bullets": ["Scaloni y el orden táctico", "Desgaste físico extremo", "Despedida de leyendas"]},
            4: {"subtitle": "La Expulsión de Enzo Fernández", "badge": "MOMENTO CLAVE 🔴", "bullets": ["Tarjeta roja directa", "Superioridad numérica roja", "Argentina sin contención"]},
            5: {"subtitle": "El Minuto 106: El Gol de Ferran", "badge": "EL GOL ⚽", "bullets": ["Pase milimétrico de Pedri", "Definición perfecta de Ferran", "Delirio en el banquillo"]},
            6: {"subtitle": "La Segunda Estrella y el Legado", "badge": "LA SEGUNDA ESTRELLA ⭐", "bullets": ["Segunda estrella mundialista", "El triunfo de un estilo", "Festa histórica en España"]}
        }
    },
    "spain_essay_2": {
        "essay_num": 2,
        "badge": "LA FINAL 👑",
        "music": "Moorland.mp3",
        "bg_screenshots": ["messi_celebration", "argentina_stadium", "spain_stars"],
        "chapters": {
            1: {"subtitle": "El Fin de una Era", "badge": "EL FIN DE UNA ERA 👑", "bullets": ["El último partido de Messi", "Treinta y nueve años de magia", "Tristeza en el MetLife"]},
            2: {"subtitle": "El Marcaje a Messi", "badge": "TÁCTICA DEFENSIVA 🛡️", "bullets": ["Bloque defensivo bajo", "Presión constante de Rodri", "Sin libertad para crear"]},
            3: {"subtitle": "El Control de Rodri y Pedri", "badge": "CONTROL TOTAL 🧠", "bullets": ["Posesión inteligente roja", "Sincronización en el pase", "Desgaste del rival"]},
            4: {"subtitle": "Las Ocasiones Perdidas de Argentina", "badge": "LAS CONTRAS ⚔️", "bullets": ["Contragolpes anulados", "La ausencia de Di María", "Falta de pegada en el área"]},
            5: {"subtitle": "La Batalla Física de la Prórroga", "badge": "LA PRÓRROGA 🥵", "bullets": ["Calor extremo en la cancha", "Jugadores al límite", "El banquillo fue vital"]},
            6: {"subtitle": "El Futuro del Fútbol Mundial", "badge": "EL FUTURO 🪐", "bullets": ["La consagración joven", "Relevo generacional exitoso", "España reina en el mundo"]}
        }
    }
}

from kinesio_core import get_audio_duration, get_ken_burns_crop

def get_chapter_timestamps(script_path, total_duration, essay_num):
    if not os.path.exists(script_path):
        return []
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    essay_key = f"### 📽️ Ensayo {essay_num}:"
    if essay_key not in content:
        return []
        
    essay_block = content.split(essay_key)[1]
    if essay_num == 1:
        essay_block = essay_block.split("### 📽️ Ensayo 2:")[0]
    else:
        essay_block = essay_block.split("## 📱 PARTE 2:")[0]
        
    chapters = essay_block.split('#### Capítulo ')
    sections = []
    total_words = 0
    
    for ch in chapters[1:]:
        lines = ch.split('\n')
        title = lines[0].strip()
        
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

def draw_progress_bar(draw_img, x, y, w, h, progress, color=(56, 189, 248, 220), bg_color=(255, 255, 255, 20)):
    draw_img.line([x, y + h//2, x + w, y + h//2], fill=bg_color, width=h)
    draw_img.line([x, y + h//2, x + int(w * progress), y + h//2], fill=color, width=h)

def draw_horizontal_frame(draw, width, height, title, subtitle, bullets, badge, font_title, font_sub, font_badge, blurred_bg_img, progress, vignette_img=None, effect_type="zoom_in"):
    if blurred_bg_img:
        img_bg = get_ken_burns_crop(blurred_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
        
    # Apply pre-rendered vignette overlay
    if vignette_img:
        img_bg = Image.alpha_composite(img_bg, vignette_img)
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # Sinoidal Card Float Animation
    float_offset = int(math.sin(progress * math.pi * 2.0) * 8.0)
    
    # Glass Panel dimensions (Double border neon card)
    panel_w = 1200
    panel_h = 600
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + float_offset
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    # Neon cyan borders
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(12, 20, 38, 160), outline=(56, 189, 248, 60), width=3)
    draw_img.rounded_rectangle([panel_left - 4, panel_top - 4, panel_right + 4, panel_bottom + 4], radius=28, fill=(0, 0, 0, 0), outline=(56, 189, 248, 15), width=2)
    
    # Chapter Title Text
    draw_img.text((panel_left + 80, panel_top + 80), title.upper(), font=font_title, fill=(255, 255, 255, 255))
    draw_img.text((panel_left + 80, panel_top + 155), subtitle, font=font_sub, fill=(148, 163, 184, 255))
    
    # Divider line
    draw_img.line([panel_left + 80, panel_top + 220, panel_right - 80, panel_top + 220], fill=(56, 189, 248, 40), width=2)
    
    # Chapter Bullet Points (floated dynamically)
    bullets_y = panel_top + 260
    bullet_font = font_sub
    for i, bullet in enumerate(bullets):
        # Progressively highlight bullets based on video progress
        threshold = (i + 1) / (len(bullets) + 1)
        is_highlighted = progress >= threshold
        text_color = (255, 255, 255, 255) if is_highlighted else (148, 163, 184, 120)
        dot_color = (56, 189, 248, 255) if is_highlighted else (56, 189, 248, 80)
        
        # Bullet Dot neon capsule
        dot_x = panel_left + 90
        dot_y = bullets_y + i * 75 + 14
        draw_img.rounded_rectangle([dot_x, dot_y - 6, dot_x + 12, dot_y + 6], radius=6, fill=dot_color)
        
        draw_img.text((panel_left + 130, bullets_y + i * 75), f"{bullet}", font=bullet_font, fill=text_color)
        
    # Badge floating top right of card
    if badge:
        badge_w = int(draw_img.textlength(badge, font=font_badge)) + 40
        badge_h = 44
        badge_x = panel_right - badge_w - 40
        badge_y = panel_top + 40
        draw_img.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=12, fill=(56, 189, 248, 40), outline=(56, 189, 248, 200), width=2)
        draw_img.text((badge_x + badge_w // 2, badge_y + badge_h // 2), badge, font=font_badge, fill=(255, 255, 255, 255), anchor="mm")
        
    # Progress Bar drawing at the bottom
    bar_w = panel_w
    bar_x = panel_left
    bar_y = panel_bottom + 15
    draw_progress_bar(draw_img, bar_x, bar_y, bar_w, 8, progress)
    
    return img_bg

def compile_essays():
    script_path = os.path.join(BASE_DIR, "scripts_spain_campaign.md")
    
    print("\n====================================================")
    print("DOMINUSBABEL SPAIN VIDEO ESSAYS COMPILER")
    print("====================================================\n")
    
    width, height = 1920, 1080
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 34)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    
    # Pre-render static vignette overlay to save massive CPU cycles in inner loops
    print("Pre-rendering static vignette overlay...")
    vignette_img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette_img)
    for r in range(0, int(width * 0.85), 15):
        alpha = int((r / (width * 0.85)) ** 2.2 * 175)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(6, 10, 20, alpha), width=16)
        
    for key, info in ESSAYS_DATA.items():
        output_path = os.path.join(BASE_DIR, f"{key}_final.mp4")
        audio_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"Video Essay '{key}' already exists on disk. Skipping.")
            continue
            
        print(f"Compiling Video Essay: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio missing for {key}. Skipping.")
            continue
            
        boundaries = get_chapter_timestamps(script_path, audio_dur, info["essay_num"])
        if not boundaries:
            print(f"  [ERROR] Failed to parse boundaries for {key}. Skipping.")
            continue
            
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
            
            ch_info = info["chapters"].get(ch_num, {})
            bg_key = info["bg_screenshots"][idx_ch % len(info["bg_screenshots"])]
            
            # Load background image dynamically to conserve memory
            base_img = None
            fpath_jpg = os.path.join(SCREENSHOTS_DIR, f"{bg_key}.jpg")
            if os.path.exists(fpath_jpg):
                try:
                    base_img = Image.open(fpath_jpg)
                except Exception as e:
                    print(f"    Failed loading {bg_key}.jpg: {e}")
            
            blurred_bg_img = None
            if base_img:
                blurred_bg_img = base_img.convert("RGBA").filter(ImageFilter.GaussianBlur(12))
                overlay = Image.new("RGBA", base_img.size, (8, 12, 24, 160))
                blurred_bg_img = Image.alpha_composite(blurred_bg_img, overlay)
                base_img.close()
                
            frame_dir = os.path.join(temp_dir, f"frames_{idx_ch}")
            if os.path.exists(frame_dir):
                try:
                    shutil.rmtree(frame_dir)
                except:
                    pass
            os.makedirs(frame_dir, exist_ok=True)
            total_frames = int(dur * 30)
            
            # Rotate camera motions
            kb_effects = ["zoom_in", "zoom_out", "pan_left", "pan_right"]
            effect_type = kb_effects[idx_ch % len(kb_effects)]
            
            t0 = time.time()
            for f_idx in range(total_frames):
                progress = f_idx / total_frames
                frame_img = draw_horizontal_frame(
                    None, width, height, ch_title,
                    f"Capítulo {ch_num}: {ch_info.get('subtitle','')}",
                    ch_info.get("bullets", []), ch_info.get("badge", info["badge"]),
                    font_title, font_sub, font_badge,
                    blurred_bg_img, progress, vignette_img=vignette_img, effect_type=effect_type
                )
                frame_img.convert("RGB").save(os.path.join(frame_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
                frame_img.close()
                
            if blurred_bg_img:
                blurred_bg_img.close()
                
            fps_render = total_frames / (time.time() - t0)
            print(f"    Rendered {total_frames} frames in {time.time()-t0:.1f}s ({fps_render:.1f} FPS)")
            
            # Compile chapter segment
            raw_seg = os.path.join(frame_dir, "raw_seg.mp4")
            cmd_frames = [
                "ffmpeg", "-y",
                "-framerate", "30",
                "-i", os.path.join(frame_dir, "frame_%05d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-t", f"{dur:.2f}",
                raw_seg
            ]
            subprocess.run(cmd_frames, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # We compile the raw segment directly as the chapter segment (no audio mixing at this level)
            seg_video = os.path.join(temp_dir, f"seg_{idx_ch:02d}.mp4")
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
                print(f"  [SUCCESS] Chapter {ch_num} compiled successfully.")
            else:
                print(f"  [ERROR] Chapter {ch_num} compilation failed.")
                
        # Concatenate all segment videos and merge with the voiceover, background music, and whoosh SFX
        if len(segment_files) == len(boundaries):
            print("Concatenating all chapter segments...")
            concat_list_path = os.path.join(temp_dir, "concat_list.txt")
            with open(concat_list_path, "w", encoding="utf-8") as f_list:
                for f_seg in segment_files:
                    path_slashes = f_seg.replace('\\', '/')
                    f_list.write(f"file '{path_slashes}'\n")
                    
            concat_video = os.path.join(temp_dir, "concat_video.mp4")
            cmd_concat = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", concat_list_path,
                "-c", "copy",
                concat_video
            ]
            subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print(f"Assembling audio tracks with {info['music']} background...")
            audio_inputs = ["-i", concat_video, "-i", audio_path]
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
                
                # Split whoosh SFX for each chapter transition boundary
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
            
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"  [SUCCESS] Video essay compiled: {output_path}")
                try:
                    shutil.rmtree(temp_dir)
                except:
                    pass
            else:
                print(f"  [ERROR] Final assembly failed for {key}")
        else:
            print(f"  [ERROR] Cannot assemble {key}: not all chapter segments were compiled.")

if __name__ == "__main__":
    compile_essays()
