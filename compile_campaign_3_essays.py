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
    "war_myths_essay_1": {
        "title": "MITOS DE GUERRA (PARTE 1)",
        "badge": "COMBATE REAL ⚔",
        "music": "Clash Defiant.mp3",
        "bg_prefix": "gates_of_hell_screenshot_",
        "chapters": {
            1: {"subtitle": "Mito: El combate real tiene música épica", "bullets": ["✔ En realidad, impera un silencio tenso", "✔ Explosiones y ráfagas repentinas", "✔ Pitido constante por trauma acústico"], "badge": "SONIDO 🔇"},
            2: {"subtitle": "Mito: Siempre ves de frente a tu enemigo", "bullets": ["✔ Se dispara a destellos y humo", "✔ Combates urbanos tras coberturas", "✔ Lucha a distancia contra invisibles"], "badge": "VISIÓN 👁"},
            3: {"subtitle": "Mito: El rango militar equivale a habilidad", "bullets": ["✔ Oficiales novatos con teoría académica", "✔ Sargentos veteranos liderando el frente", "✔ La competencia real se mide en batalla"], "badge": "LIDERAZGO 🎖"},
            4: {"subtitle": "Mito: Disparas tu fusil todo el tiempo", "bullets": ["✔ 99% es carga, excavación y espera", "✔ Fuego sostenido es solo un instante", "✔ Munición limitada y disparo selectivo"], "badge": "LOGÍSTICA 🎒"},
            5: {"subtitle": "Mito: La guerra es puro ruido ensordecedor", "bullets": ["✔ Estrés induce exclusión auditiva", "✔ El cerebro bloquea disparos para salvarte", "✔ Sensación de estar bajo el agua"], "badge": "MENTE 🧠"},
            6: {"subtitle": "Mito: Conoces la situación táctica completa", "bullets": ["✔ La niebla de guerra es absoluta", "✔ Solo sabes lo que pasa en tu trinchera", "✔ Órdenes tardías y comunicaciones rotas"], "badge": "TÁCTICA 🗺"},
            7: {"subtitle": "Mito: Sientes dolor de inmediato al ser herido", "bullets": ["✔ La adrenalina bloquea receptores de dolor", "✔ Soldados luchan heridos sin saberlo", "✔ Se descubre por la sangre o debilidad"], "badge": "FISIOLOGÍA 💉"},
            8: {"subtitle": "Mito: Recuerdas cada segundo de la batalla", "bullets": ["✔ El trauma severo fragmenta la memoria", "✔ Recuerdas detalles absurdos aislados", "✔ Cronología confusa y lagunas mentales"], "badge": "MEMORIA 🧠"},
            9: {"subtitle": "Mito: Las milicias locales son inútiles", "bullets": ["✔ Guerrilla desgasta ejércitos modernos", "✔ Ventaja extrema por conocer el terreno", "✔ Motivación defensiva supera equipo puro"], "badge": "GUERRILLA 🛡"},
            10: {"subtitle": "Mito: El soldado occidental es superior en todo", "bullets": ["✔ Clima y selva anulan adiestramiento", "✔ Fuerzas locales son más adaptables", "✔ Sobrevive el que mejor entiende el terreno"], "badge": "ADAPTACIÓN 🌴"}
        }
    },
    "war_myths_essay_2": {
        "title": "MITOS DE GUERRA (PARTE 2)",
        "badge": "TECNOLOGÍA Y CAOS ⚔",
        "music": "Clash Defiant.mp3",
        "bg_prefix": "gates_of_hell_screenshot_",
        "chapters": {
            1: {"subtitle": "Mito: Siempre distingues al bando enemigo", "bullets": ["✔ Conflictos modernos sin uniformes", "✔ Insurgentes vestidos como civiles", "✔ Pesadilla diaria de evitar fuego amigo"], "badge": "IDENTIDAD 👥"},
            2: {"subtitle": "Mito: Los drones son armas indestructibles", "bullets": ["✔ Guerra electrónica tumba miles al día", "✔ Inhibidores de señal inutilizan GPS", "✔ Uso de escopetas de caza y redes físicas"], "badge": "DRONES 🛸"},
            3: {"subtitle": "Mito: Los pilotos de drones están a salvo", "bullets": ["✔ Operadores son objetivos prioritarios", "✔ Triangulación de señales en minutos", "✔ Movilidad constante para evitar artillería"], "badge": "PILOTOS 🎯"},
            4: {"subtitle": "Mito: Los drones FPV suicidas reemplazarán todo", "bullets": ["✔ Baterías limitadas a pocos minutos", "✔ Inutilizables con lluvia o viento fuerte", "✔ No reemplazan el volumen de artillería"], "badge": "LIMITACIÓN 🔋"},
            5: {"subtitle": "Mito: Todos reaccionan igual ante el trauma", "bullets": ["✔ El TEPT se manifiesta de formas infinitas", "✔ Bloqueos mudos vs ansiedad tardía", "✔ No existe respuesta psicológica estándar"], "badge": "TRAUMA 🧠"},
            6: {"subtitle": "Mito: El veterano curtido es rudo y agresivo", "bullets": ["✔ Los más arrogantes suelen entrar en pánico", "✔ Verdaderos veteranos son callados y fríos", "✔ La templanza real es discreta y metódica"], "badge": "VETERANO 🎖"},
            7: {"subtitle": "Mito: La estrategia militar es brillante y lógica", "bullets": ["✔ Órdenes contradictorias y absurdas", "✔ Misiones inútiles y fallos logísticos", "✔ La guerra real es caos desorganizado"], "badge": "REALIDAD ⚖"},
            8: {"subtitle": "Mito: Las granadas causan bolas de fuego", "bullets": ["✔ Estallido seco, polvo y metralla invisible", "✔ Metralla supersónica es lo letal", "✔ Bolas de fuego son efectos de cine"], "badge": "EXPLOSIÓN 💥"},
            9: {"subtitle": "Mito: El chaleco antibalas te hace inmune", "bullets": ["✔ Placas solo cubren el torso superior", "✔ Energía causa fracturas y daño interno", "✔ Extremidades y cuello quedan expuestos"], "badge": "ARMADURA 🛡"},
            10: {"subtitle": "Mito: Los silenciadores hacen el arma muda", "bullets": ["✔ Solo mitiga ruido de gases de salida", "✔ Evita sordera y oculta destello", "✔ Proyectil sigue creando crack supersónico"], "badge": "SILENCIOSO 🤫"}
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

def draw_horizontal_frame(draw, width, height, title, subtitle, bullets, badge, font_title, font_sub, font_badge, blurred_bg_img, progress, effect_type="zoom_in"):
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
    panel_w = 1200
    panel_h = 600
    panel_left = (width - panel_w) // 2
    panel_top = (height - panel_h) // 2 + 10 + float_offset
    panel_right = panel_left + panel_w
    panel_bottom = panel_top + panel_h
    
    # Double Neon Border Card
    draw_img.rounded_rectangle([panel_left, panel_top, panel_right, panel_bottom], radius=24, fill=(10, 18, 36, 155), outline=(56, 189, 248, 40), width=2)
    draw_img.rounded_rectangle([panel_left - 3, panel_top - 3, panel_right + 3, panel_bottom + 3], radius=27, fill=(0, 0, 0, 0), outline=(56, 189, 248, 15), width=2)
    
    # Text
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
    script_path = os.path.join(BASE_DIR, "scripts_war_myths.md")
    
    print("\n====================================================")
    print("CAMPAIGN 3 ESSAYS COMPILER (WAR MYTHS)")
    print("====================================================\n")
    
    width, height = 1920, 1080
    font_title = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 52)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 34)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
    
    # Load gates_of_hell screenshots
    screenshots = {}
    for i in range(10):
        fname = f"gates_of_hell_screenshot_{i}.jpg"
        fpath = os.path.join(SCREENSHOTS_DIR, fname)
        if os.path.exists(fpath):
            try:
                screenshots[f"gates_of_hell_screenshot_{i}"] = Image.open(fpath)
                print(f"Loaded screenshot: {fname}")
            except Exception as e:
                print(f"Error loading {fname}: {e}")
                
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
            bg_key = f"gates_of_hell_screenshot_{idx_ch}"
            base_img = screenshots.get(bg_key)
            
            blurred_bg_img = None
            if base_img:
                blurred_bg_img = base_img.convert("RGBA").filter(ImageFilter.GaussianBlur(12))
                overlay = Image.new("RGBA", base_img.size, (8, 12, 24, 160))
                blurred_bg_img = Image.alpha_composite(blurred_bg_img, overlay)
                
            frame_dir = os.path.join(temp_dir, f"frames_{idx_ch}")
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
                    f"Mito {ch_num}: {ch_info.get('subtitle','')}",
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
        
        print("Assembling audio tracks with Clash Defiant.mp3 background...")
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

if __name__ == "__main__":
    compile_essays()
