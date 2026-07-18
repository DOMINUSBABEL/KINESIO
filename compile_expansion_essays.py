import os
import sys
import re
import time
import shutil
import subprocess
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
POP_SFX = os.path.join(BASE_DIR, "pop.wav")
WHOOSH_SFX = os.path.join(BASE_DIR, "whoosh.wav")

ESSAYS_DATA = {
    # 1. ESTOICISMO
    "stoic_essay_1": {
        "title": "EL CAMINO DE LA ATARAXIA",
        "badge": "ESTOICISMO 🛡",
        "music": "Moorland.mp3",
        "bg_prefix": "stoic_screenshot_",
        "chapters": {
            1: {"subtitle": "La Dicotomía del Control", "bullets": ["✔ Distinguir lo que depende de ti", "✔ Desapego de las opiniones ajenas", "✔ Concentración en la virtud interior"], "badge": "CONTROL 👑"},
            2: {"subtitle": "La Fortaleza en la Adversidad", "bullets": ["✔ Premeditación de los males futuras", "✔ Control racional de las pasiones", "✔ Mantener el rumbo en el caos"], "badge": "FORTALEZA 🏛"},
            3: {"subtitle": "El Amor Fati y el Destino", "bullets": ["✔ Aceptación activa de la realidad", "✔ El obstáculo es el combustible", "✔ Alinear el alma con el cosmos"], "badge": "AMOR FATI 💎"}
        }
    },
    "stoic_essay_2": {
        "title": "LA CIUDADELA INTERIOR",
        "badge": "MARCO AURELIO 🏛",
        "music": "Moorland.mp3",
        "bg_prefix": "stoic_screenshot_",
        "chapters": {
            1: {"subtitle": "La Fortaleza Inexpugnable", "bullets": ["✔ El refugio sagrado de la mente", "✔ Nada externo puede dañarte", "✔ Eres el guardián de tu propia paz"], "badge": "TEMPLO 🛡"},
            2: {"subtitle": "El Silencio como Poder", "bullets": ["✔ Dominio absoluto de los impulsos", "✔ Moderación en palabras y gestos", "✔ Contracción reflexiva del ego"], "badge": "SILENCIO 🤫"},
            3: {"subtitle": "El Obstáculo es el Camino", "bullets": ["✔ Convertir barreras en oportunidades", "✔ Practicar el perdón ante traición", "✔ Cincelar la verdadera grandeza"], "badge": "CAMINO ⚔"}
        }
    },
    "stoic_essay_3": {
        "title": "LA RAZÓN EN EL CAOS",
        "badge": "SÉNECA y EPICTETO 🕯",
        "music": "Moorland.mp3",
        "bg_prefix": "stoic_screenshot_",
        "chapters": {
            1: {"subtitle": "La Brevedad de la Existencia", "bullets": ["✔ Valorar el recurso del tiempo", "✔ Memento mori como motivación", "✔ Vivir hoy con virtud absoluta"], "badge": "TIEMPO ⏳"},
            2: {"subtitle": "La Templanza como Escudo", "bullets": ["✔ Moderar los deseos materiales", "✔ Independencia de lo superficial", "✔ Quien menos necesita es más rico"], "badge": "TEMPLANZA ⚖"},
            3: {"subtitle": "La Libertad del Alma", "bullets": ["✔ Libertad mental sobre la física", "✔ Ninguna cadena somete el juicio", "✔ Superar el miedo al destino ajeno"], "badge": "SOBERANÍA 👑"}
        }
    },
    # 2. CÁBALA
    "kabbalah_essay_1": {
        "title": "EL ÁRBOL DE LA VIDA",
        "badge": "CÁBALA MÍSTICA 📜",
        "music": "Rites.mp3",
        "bg_prefix": "kabbalah_screenshot_",
        "chapters": {
            1: {"subtitle": "Emanaciones del Ein Sof", "bullets": ["✔ Las 10 dimensiones de la luz", "✔ El mapa cósmico de la conciencia", "✔ Conexión terrenal con lo divino"], "badge": "SEFIROT 🌟"},
            2: {"subtitle": "El Tzimtzum o Contracción", "bullets": ["✔ El repliegue divino original", "✔ Creación del vacío de existencia", "✔ Hacer espacio para la sabiduría"], "badge": "TZIMTZUM 🤫"},
            3: {"subtitle": "La Construcción de la Vasija", "bullets": ["✔ Transformar el deseo de recibir", "✔ Dar altruista para albergar luz", "✔ El valor real de la vasija espiritual"], "badge": "KLI 🏺"}
        }
    },
    "kabbalah_essay_2": {
        "title": "EL SECRETO DEL TIKÚN",
        "badge": "CORRECCIÓN DEL ALMA 💎",
        "music": "Rites.mp3",
        "bg_prefix": "kabbalah_screenshot_",
        "chapters": {
            1: {"subtitle": "La Misión de Corrección", "bullets": ["✔ Superar los defectos inherentes", "✔ Pruebas diseñadas para el alma", "✔ Aceptar la evolución espiritual"], "badge": "TIKÚN ⚖"},
            2: {"subtitle": "El Rigor y la Misericordia", "bullets": ["✔ Jésed: amor e inmensidad infinita", "✔ Gevurá: el rigor y el límite útil", "✔ Delicado equilibrio de las fuerzas"], "badge": "EQUILIBRIO ☯"},
            3: {"subtitle": "Armonía del Corazón", "bullets": ["✔ Tiferet: la Sefirá de la belleza", "✔ Punto central del árbol místico", "✔ Integrar compasión y firmeza"], "badge": "TIFERET ❤️"}
        }
    },
    "kabbalah_essay_3": {
        "title": "LOS MISTERIOS DEL ZOHAR",
        "badge": "EL LIBRO DEL ESPLENDOR 🌟",
        "music": "Rites.mp3",
        "bg_prefix": "kabbalah_screenshot_",
        "chapters": {
            1: {"subtitle": "La Revelación del Libro", "bullets": ["✔ Escritos del rabino Shimon bar Yojai", "✔ La realidad física como ilusión", "✔ Rasgar el velo de la materia"], "badge": "EL ZOHAR 📖"},
            2: {"subtitle": "La Conciencia y la Shejiná", "bullets": ["✔ Presencia divina en lo terrenal", "✔ Elevar la chispa con rectitud", "✔ Reconciliación con la luz eterna"], "badge": "SHEJINÁ ✨"},
            3: {"subtitle": "El Retorno al Ein Sof", "bullets": ["✔ El viaje del alma purificada", "✔ Desapego definitivo del cuerpo", "✔ Muerte física como liberación"], "badge": "EL RETORNO 🌌"}
        }
    },
    # 3. MAGNIFICA HUMANITAS
    "humanitas_essay_1": {
        "title": "LA CUSTODIA DEL SER HUMANO",
        "badge": "ENCÍCLICA LEÓN XIV 📜",
        "music": "Cipher2.mp3",
        "bg_prefix": "humanitas_screenshot_",
        "chapters": {
            1: {"subtitle": "Dignidad Humana ante la IA", "bullets": ["✔ Custodia del ser humano en la era digital", "✔ La tecnología como una herramienta", "✔ La chispa divina no copiable"], "badge": "DIGNIDAD 🏛"},
            2: {"subtitle": "Ética en la IA y Algoritmos", "bullets": ["✔ Exclusión del lucro desmedido", "✔ Decisiones críticas sin empatía", "✔ No renunciar a la moralidad"], "badge": "ÉTICA ⚖"},
            3: {"subtitle": "Peligros del Transhumanismo", "bullets": ["✔ Superar límites como soberbia", "✔ Peligro de destruir la esencia", "✔ Cultivar virtud y trascendencia"], "badge": "ESPÍRITU 🛡"}
        }
    },
    "humanitas_essay_2": {
        "title": "BABEL CONTRA JERUSALÉN",
        "badge": "METÁFORA SOCIAL 🏰",
        "music": "Cipher2.mp3",
        "bg_prefix": "humanitas_screenshot_",
        "chapters": {
            1: {"subtitle": "La Soberbia de Babel", "bullets": ["✔ Confianza ciega en lo tecnocrático", "✔ Aislamiento y división social", "✔ El colapso inminente de la soberbia"], "badge": "BABEL 🗼"},
            2: {"subtitle": "La Reconstrucción de Jerusalén", "bullets": ["✔ Modelo de comunión y fraternidad", "✔ IA para sanar y erradicar pobreza", "✔ Tecnología al servicio común"], "badge": "JERUSALÉN 🕊"},
            3: {"subtitle": "Protección de los Vulnerables", "bullets": ["✔ Inclusión ante automatización", "✔ Cuidado de niños en redes digitales", "✔ Beneficios para los marginados"], "badge": "INCLUSIÓN 👵"}
        }
    },
    "humanitas_essay_3": {
        "title": "LA ÉTICA DE LA INTELIGENCIA ARTIFICIAL",
        "badge": "GOBERNANZA GLOBAL 🌐",
        "music": "Cipher2.mp3",
        "bg_prefix": "humanitas_screenshot_",
        "chapters": {
            1: {"subtitle": "Gobernanza Global de la IA", "bullets": ["✔ Marcos éticos regulatorios vinculantes", "✔ Prohibición de armas autónomas letales", "✔ La paz no depende de algoritmos"], "badge": "GOBERNANZA 🤝"},
            2: {"subtitle": "El Futuro del Trabajo Humano", "bullets": ["✔ El derecho al trabajo digno y real", "✔ IA para elevar capacidades humanas", "✔ No al reemplazo masivo de familias"], "badge": "TRABAJO 💼"},
            3: {"subtitle": "La Desinformación y la Verdad", "bullets": ["✔ Deepfakes y manipulación de masas", "✔ Algoritmos del miedo y la división", "✔ Educación en discernimiento ético"], "badge": "VERDAD 🕯"}
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
    
    # 1. Radial Vignette
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    vig_draw = ImageDraw.Draw(vignette)
    for r in range(0, int(width * 0.85), 15):
        alpha = int((r / (width * 0.85)) ** 2.2 * 175)
        vig_draw.ellipse([width//2 - r, height//2 - r, width//2 + r, height//2 + r], outline=(6, 10, 20, alpha), width=16)
    img_bg = Image.alpha_composite(img_bg, vignette)
    draw_img = ImageDraw.Draw(img_bg)
    
    # 2. Sinoidal Card Float Animation
    float_offset = int(math.sin(progress * math.pi * 2.0) * 8.0)
    
    # Glass Panel dimensions
    panel_w = 1100
    panel_h = 580
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + 10 + float_offset
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    # Glow borders shadow
    shadow_offset = 12
    if not hasattr(draw_horizontal_frame, 'shadow_blur'):
        shadow_mask = Image.new("L", (panel_w + 40, panel_h + 40), 0)
        ImageDraw.Draw(shadow_mask).rounded_rectangle([15, 15, panel_w + 15, panel_h + 15], radius=30, fill=150)
        draw_horizontal_frame.shadow_blur = shadow_mask.filter(ImageFilter.GaussianBlur(20))
        draw_horizontal_frame.shadow_color = Image.new("RGBA", (panel_w + 40, panel_h + 40), (0, 0, 0, 220))
    img_bg.paste(draw_horizontal_frame.shadow_color, (panel_left - 15 + shadow_offset, panel_top - 15 + shadow_offset), mask=draw_horizontal_frame.shadow_blur)
    
    # Double Neon Border Card
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(10, 18, 36, 145), outline=(56, 189, 248, 40), width=2)
    draw_img.rounded_rectangle([panel_left - 3, panel_top - 3, panel_right + 3, panel_bottom + 3], radius=27, fill=(0, 0, 0, 0), outline=(56, 189, 248, 15), width=2)
    
    # Text
    draw_img.text((width // 2, panel_top + 80), title, font=font_title, fill=(255, 255, 255, 255), anchor="mm")
    draw_img.text((width // 2, panel_top + 210), subtitle, font=font_sub, fill=(56, 189, 248, 255), anchor="mm")
    
    # Active bullet highlight logic
    num_bullets = len(bullets)
    active_b_idx = int(progress * num_bullets)
    active_b_idx = min(active_b_idx, num_bullets - 1)
    
    bullet_y = panel_top + 290
    for idx_b, b in enumerate(bullets):
        if idx_b == active_b_idx:
            # Senoidal active glow highlight
            glow_alpha = int(140 + math.sin(time.time() * 8) * 40)
            draw_img.text((width // 2, bullet_y), b, font=font_sub, fill=(255, 255, 255, 255), anchor="mm")
            # Subtle underline
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

def compile_expansion_essays():
    script_path = os.path.join(BASE_DIR, "scripts_expansion_essays.md")
    
    print("\n====================================================")
    print("EXPANSION ESSAYS COMPILER (STOIC, KABBALAH, HUMANITAS)")
    print("====================================================\n")
    
    width, height = 1920, 1080
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 34)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    
    # Preload generated screenshots
    screenshots = {}
    for prefix in ["stoic_screenshot_", "kabbalah_screenshot_", "humanitas_screenshot_"]:
        for i in range(3):
            fname = f"{prefix}{i}.jpg"
            fpath = os.path.join(SCREENSHOTS_DIR, fname)
            if os.path.exists(fpath):
                try:
                    screenshots[f"{prefix}{i}"] = Image.open(fpath)
                    print(f"Loaded screenshot: {fname}")
                except Exception as e:
                    print(f"Error loading {fname}: {e}")
                    
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
            
            ch_info = info["chapters"].get(ch_num, {})
            
            # Map chapter 1->0, 2->1, 3->2 for screenshots
            bg_key = f"{info['bg_prefix']}{ch_num-1}"
            base_img = screenshots.get(bg_key)
            
            blurred_bg_img = None
            if base_img:
                blurred_bg_img = base_img.convert("RGBA").filter(ImageFilter.GaussianBlur(12))
                overlay = Image.new("RGBA", base_img.size, (8, 12, 24, 160))
                blurred_bg_img = Image.alpha_composite(blurred_bg_img, overlay)
                
            frame_dir = os.path.join(temp_dir, f"frames_{idx_ch}")
            os.makedirs(frame_dir, exist_ok=True)
            total_frames = int(dur * 30)
            
            # Rotate effects
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
        
        print("Assembling audio tracks...")
        audio_inputs = ["-i", raw_video, "-i", audio_path]
        audio_mix_filter = "[1:a]volume=1.0[speech];"
        
        # Background music track variety mapping
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

if __name__ == "__main__":
    compile_expansion_essays()
