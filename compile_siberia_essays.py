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
    "siberia_essay_1": {
        "title": "LA SUBASTA DE SIBERIA",
        "badge": "GEOPOLÍTICA 🇷🇺",
        "music": "Clash Defiant.mp3",
        "essay_num": 1,
        "bg_screenshots": [
            "gates_of_hell_screenshot_0",
            "gates_of_hell_screenshot_1",
            "gates_of_hell_screenshot_2",
            "gates_of_hell_screenshot_3",
            "gates_of_hell_screenshot_4",
            "gates_of_hell_screenshot_5",
        ],
        "chapters": {
            1: {"subtitle": "El sesgo de la conscripción rural", "bullets": ["✔ Concentración en repúblicas periféricas", "✔ Buriatia y Yakutia con tasas críticas", "✔ La guerra como salida a la escasez"]},
            2: {"subtitle": "La competencia entre provincias", "bullets": ["✔ Bonos de firma que duplican ofertas", "✔ Descentralización de cuotas del Kremlin", "✔ El soldado cotizado al mejor postor"]},
            3: {"subtitle": "Clima extremo y contratos de oro", "bullets": ["✔ Temperaturas bajo cincuenta grados", "✔ Sin alternativas laborales viables", "✔ Redención financiera mediante el fusil"]},
            4: {"subtitle": "Contrasto salarial trágico", "bullets": ["✔ Sueldo rural de 400 dólares mensuales", "✔ Pago militar de más de 200 mil rublos", "✔ Multiplicación de ingresos por seis veces"]},
            5: {"subtitle": "El presupuesto de la guerra", "bullets": ["✔ Reorientación histórica de las arcas", "✔ Flujo incombustible de petrodólares", "✔ El conflicto como la industria nacional"]},
            6: {"subtitle": "El vaciamiento demográfico", "bullets": ["✔ Pérdida insostenible de mano de obra", "✔ Consecuencias étnicas y estructurales", "✔ Una factura que se pagará por décadas"]}
        }
    },
    "siberia_essay_2": {
        "title": "EL NEGOCIO DE LA MUERTE",
        "badge": "REALIDAD SOCIAL ⚖",
        "music": "Moorland.mp3",
        "essay_num": 2,
        "bg_screenshots": [
            "gates_of_hell_screenshot_6",
            "gates_of_hell_screenshot_7",
            "gates_of_hell_screenshot_8",
            "gates_of_hell_screenshot_9",
            "iron_harvest_screenshot_0",
            "iron_harvest_screenshot_1",
        ],
        "chapters": {
            1: {"subtitle": "El dinero de ataúd en Siberia", "bullets": ["✔ Compensación federal por fallecimiento", "✔ Seguros masivos que fluyen al campo", "✔ Un fenómeno macroeconómico forense"]},
            2: {"subtitle": "Soldado muerto vale más", "bullets": ["✔ Indemnización de doce millones de rublos", "✔ Equivalente a treinta años de salario rural", "✔ El sacrificio como rescate familiar"]},
            3: {"subtitle": "Burbuja de consumo en la periferia", "bullets": ["✔ Auge de construcción y compra de autos", "✔ Cancelación de deudas históricas", "✔ Aldeas sustentadas por bajas del frente"]},
            4: {"subtitle": "La realidad en el adiestramiento", "bullets": ["✔ Entrenamiento express de quince días", "✔ Abusos físicos y novatadas de veteranos", "✔ Desgaste moral antes del combate real"]},
            5: {"subtitle": "Infantería desechable de bajo costo", "bullets": ["✔ Contratos de seis meses por libertad", "✔ Misiones de asalto de máximo riesgo", "✔ Ahorro carcelario y trabas de seguros"]},
            6: {"subtitle": "El futuro de los pueblos huérfanos", "bullets": ["✔ Colapso de consumo post-conflicto", "✔ Regiones sin juventud para producir", "✔ Un trauma generacional e irreversible"]}
        }
    }
}

from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_progress_bar

def get_chapter_timestamps(script_path, total_duration, essay_num):
    if not os.path.exists(script_path):
        return []
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by essay
    if essay_num == 1:
        essay_parts = content.split('### 📽️ Video Essay 1: "La Subasta de Siberia: ¿Cuánto vale un soldado en Rusia?"')
        if len(essay_parts) < 2:
            return []
        essay_block = essay_parts[1].split('### 📽️ Video Essay 2:')[0]
    else:
        essay_parts = content.split('### 📽️ Video Essay 2: "El Negocio de la Muerte: Los \'Grobovye\' en la Rusia Rural"')
        if len(essay_parts) < 2:
            return []
        essay_block = essay_parts[1].split('## 📱 PARTE 2:')[0]
        
    chapters = essay_block.split("#### 📌 Capítulo ")
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

def draw_horizontal_frame(draw, width, height, title, subtitle, bullets, badge, font_title, font_sub, font_badge, blurred_bg_img, progress, vignette_img=None, effect_type="zoom_in"):
    if blurred_bg_img:
        img_bg = get_ken_burns_crop(blurred_bg_img, width, height, progress, effect_type)
    else:
        img_bg = Image.new("RGBA", (width, height), (10, 15, 30, 255))
        
    # Apply pre-rendered vignette overlay
    if vignette_img:
        img_bg = Image.alpha_composite(img_bg, vignette_img)
        
    draw_img = ImageDraw.Draw(img_bg)
    
    # 2. Sinoidal Card Float Animation
    float_offset = int(math.sin(progress * math.pi * 2.0) * 8.0)
    
    # Glass Panel dimensions
    panel_w = 1200
    panel_h = 600
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + 10 + float_offset
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    # Double Neon Border Card (Using cyan/blue/dark tones for geopolitical elegance)
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(12, 20, 38, 160), outline=(56, 189, 248, 50), width=2)
    draw_img.rounded_rectangle([panel_left - 3, panel_top - 3, panel_right + 3, panel_bottom + 3], radius=27, fill=(0, 0, 0, 0), outline=(56, 189, 248, 15), width=2)
    
    # Title & Subtitle
    draw_img.text((width // 2, panel_top + 80), title.upper(), font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, panel_top + 210), subtitle, font=font_sub, fill=(56, 189, 248, 255), anchor="mm")
    
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
            draw_img.line([width//2 - t_w//2, bullet_y + 26, width//2 + t_w//2, bullet_y + 26], fill=(56, 189, 248, glow_alpha), width=2)
        else:
            draw_img.text((width // 2, bullet_y), b, font=font_sub, fill=(130, 150, 180, 220), anchor="mm")
        bullet_y += 70
        
    # Badge
    if badge:
        badge_w = 280
        badge_h = 60
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
    script_path = os.path.join(BASE_DIR, "scripts_siberia_campaign.md")
    
    print("\n====================================================")
    print("DOMINUSBABEL SIBERIA VIDEO ESSAYS COMPILER")
    print("====================================================\n")
    
    width, height = 1920, 1080
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 34)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    
    # Load screenshots cache
    screenshots = {}
    
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
            print(f"Video essay '{key}' already exists on disk. Skipping.")
            continue
            
        print(f"\nCompiling Video Essay: {key}...")
        audio_dur = get_audio_duration(audio_path)
        if audio_dur == 0.0:
            print(f"  [ERROR] Audio track missing for {key}. Skipping.")
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
        
        print(f"Assembling audio tracks with {info['music']} background...")
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.0[speech];"
        
        bg_music_path = os.path.join(MUSIC_DIR, info["music"])
        use_bg = os.path.exists(bg_music_path)
        if use_bg:
            audio_inputs.extend(["-stream_loop", "-1", "-i", bg_music_path])
            # Music volume attenuated as per requirement (-22dB to -25dB)
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
    compile_essays()
