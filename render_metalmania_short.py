# -*- coding: utf-8 -*-
"""
METAL MANIA - COMMERCIAL SHORT RENDERER
Propuesta 2: 'El Secreto de las Ediciones Japonesas y Firmas Auténticas'
Resolution: 1080x1920 (9:16 Vertical)
Target Duration: ~24.2s (Precise 24s commercial cut)
"""

import os
import sys
import math
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
ASSETS_DIR = os.path.join(BASE_DIR, "assets_metalmania")
MUSIC_DIR = os.path.join(BASE_DIR, "music")
AUDIO_DIR = os.path.join(BASE_DIR, "audio_assets")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_rendered_mp4s")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Timeline & Script Cue Definitions
CUES = [
    {
        "id": "scene_1",
        "start": 0.0,
        "end": 4.30,
        "asset": os.path.join(ASSETS_DIR, "scene1_obi_strip.jpg"),
        "header": "¿POR QUÉ BUSCAN EL OBI JAPONÉS?",
        "header_color": (250, 200, 21, 255), # Neon Gold
        "header_badge": "🇯🇵 EDICIÓN JAPONESA",
        "effect": "zoom_in_macro",
        "subtitles": [
            {"start": 0.10, "end": 4.30, "text": "¿Sabías que un OBI japonés original puede multiplicar el valor de un disco?"}
        ],
        "footer_text": "📦 COLECCIONISMO EXCLUSIVO • EDICIONES JAPONESAS"
    },
    {
        "id": "scene_2",
        "start": 4.30,
        "end": 12.40,
        "asset": os.path.join(ASSETS_DIR, "scene2_signed_metal.jpg"),
        "header": "SIN REPRODUCCIONES • FIRMAS 100% REALES",
        "header_color": (0, 229, 255, 255), # Electric Cyan
        "header_badge": "✍️ AUTENTICIDAD GARANTIZADA",
        "effect": "pan_down",
        "subtitles": [
            {"start": 4.30, "end": 6.89, "text": "Pero el mercado está lleno de copias falsas."},
            {"start": 6.90, "end": 12.40, "text": "En Metal Mania no vendemos reproducciones: garantizamos autenticidad total en prensajes y firmas."}
        ],
        "footer_text": "🛡️ CERTIFICADO DE AUTENTICIDAD • PRENSAJES ORIGINALES"
    },
    {
        "id": "scene_3",
        "start": 12.40,
        "end": 17.96,
        "asset": os.path.join(ASSETS_DIR, "scene3_safe_packaging.jpg"),
        "header": "STOCK FÍSICO REAL • MÁXIMA PROTECCIÓN",
        "header_color": (250, 200, 21, 255), # Gold
        "header_badge": "📦 EMBALAJE REFORZADO",
        "effect": "zoom_in_packaging",
        "subtitles": [
            {"start": 12.40, "end": 17.96, "text": "Todo está en stock y protegido con embalaje especial de grado coleccionista para llegar intacto a cualquier país."}
        ],
        "footer_text": "✈️ ENVÍOS INTERNACIONALES PROTEGIDOS • PROTECTORES DE ESQUINAS"
    },
    {
        "id": "scene_4",
        "start": 17.96,
        "end": 24.19,
        "asset": os.path.join(ASSETS_DIR, "scene4_metalmania_store.jpg"),
        "header": "STOCK LIMITADO 🔥 metalmaniach.com",
        "header_color": (255, 77, 77, 255), # Fire Red / Orange
        "header_badge": "🛒 TIENDA ONLINE OFICIAL",
        "effect": "pan_up_store",
        "subtitles": [
            {"start": 17.96, "end": 20.74, "text": "Consigue estas rarezas antes de que se agoten."},
            {"start": 20.75, "end": 24.19, "text": "Visita el link de la bio o entra a metalmaniach.com."}
        ],
        "footer_text": "🔥 COMPRA AHORA EN metalmaniach.com • LINK EN BIO"
    }
]

WIDTH = 1080
HEIGHT = 1920
FPS = 30
TOTAL_DURATION = 24.19

# 2. Helper Graphics Functions
def load_font(font_name, size):
    path = os.path.join(r"C:\Windows\Fonts", font_name)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        try:
            return ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", size)
        except Exception:
            return ImageFont.load_default()

FONT_BRAND = load_font("segoeuib.ttf", 26)
FONT_BADGE = load_font("segoeuib.ttf", 24)
FONT_HEADER = load_font("impact.ttf", 46)
FONT_SUBTITLE = load_font("segoeuib.ttf", 44)
FONT_FOOTER = load_font("segoeuib.ttf", 26)
FONT_CTA = load_font("impact.ttf", 40)

def get_ken_burns_frame(img, width, height, progress, effect_type):
    bw, bh = img.size
    target_aspect = width / height # 1080 / 1920 = 0.5625
    
    if effect_type == "zoom_in_macro":
        # Start showing 95% down to 80% with slight center drift
        scale = 0.95 - (0.18 * progress)
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = int((bw - cw) * (0.35 + 0.15 * progress))
        cy = int((bh - ch) * (0.30 + 0.20 * progress))
        
    elif effect_type == "pan_down":
        scale = 0.82
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = (bw - cw) // 2
        cy = int((bh - ch) * (0.15 + 0.65 * progress))
        
    elif effect_type == "zoom_in_packaging":
        scale = 0.92 - (0.16 * progress)
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = int((bw - cw) * (0.45 + 0.10 * progress))
        cy = int((bh - ch) * (0.25 + 0.30 * progress))
        
    elif effect_type == "pan_up_store":
        scale = 0.84
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = (bw - cw) // 2
        cy = int((bh - ch) * (0.65 - 0.50 * progress))
        
    else: # Default zoom in
        scale = 0.90 - (0.10 * progress)
        cw = int(bw * scale)
        ch = int(cw / target_aspect)
        if ch > bh:
            ch = int(bh * scale)
            cw = int(ch * target_aspect)
        cx = (bw - cw) // 2
        cy = (bh - ch) // 2

    cx = max(0, min(bw - cw, cx))
    cy = max(0, min(bh - ch, cy))
    
    crop = img.crop((cx, cy, cx + cw, cy + ch))
    return crop.resize((width, height), Image.Resampling.LANCZOS)

def draw_outlined_text(draw, pos, text, font, fill_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), thickness=4, anchor="mm"):
    x, y = pos
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx*dx + dy*dy <= thickness*thickness and (dx != 0 or dy != 0):
                draw.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill_color, anchor=anchor)

def get_word_highlight(word):
    clean = word.lower().strip(".,!?:;\"'¿¡")
    gold_keywords = ["obi", "japonés", "japones", "original", "multiplicar", "valor", "metal", "mania", "autenticidad", "firmas", "prensajes", "coleccionista", "stock", "rarezas", "metalmaniach.com"]
    red_keywords = ["falsas", "reproducciones", "copias", "agotarse", "agoten", "limitado"]
    cyan_keywords = ["grado", "embalaje", "protegido", "intacto", "país", "pais", "link", "bio"]
    
    if any(k in clean for k in gold_keywords):
        return (250, 200, 21, 255) # Bright Gold
    if any(k in clean for k in red_keywords):
        return (255, 77, 77, 255) # Fiery Red
    if any(k in clean for k in cyan_keywords):
        return (0, 229, 255, 255) # Electric Cyan
    return (255, 255, 255, 255) # Crisp White

def render_kinetic_subtitles(draw, current_text, t_sec, cue_start, cue_end, center_pos=(540, 1480)):
    if not current_text:
        return
    
    words = current_text.split()
    if not words:
        return
        
    cue_dur = max(cue_end - cue_start, 0.1)
    progress_cue = max(0.0, min(1.0, (t_sec - cue_start) / cue_dur))
    active_idx = min(int(progress_cue * len(words)), len(words) - 1)
    
    # Calculate text wrapping
    max_w = 920
    sample_img = Image.new("RGBA", (1, 1))
    sample_draw = ImageDraw.Draw(sample_img)
    space_w = sample_draw.textlength(" ", font=FONT_SUBTITLE)
    
    lines = []
    cur_line = []
    cur_line_w = 0
    for idx, w in enumerate(words):
        ww = sample_draw.textlength(w, font=FONT_SUBTITLE)
        if cur_line and (cur_line_w + space_w + ww > max_w):
            lines.append(cur_line)
            cur_line = [(idx, w, ww)]
            cur_line_w = ww
        else:
            cur_line.append((idx, w, ww))
            cur_line_w += (space_w if cur_line else 0) + ww
    if cur_line:
        lines.append(cur_line)
        
    line_h = 60
    total_h = len(lines) * line_h
    start_y = center_pos[1] - (total_h / 2) + (line_h / 2)
    
    # Draw dark frosted glass backing for subtitles
    panel_pad_x = 40
    panel_pad_y = 24
    max_measured_w = max(sum(ww for _, _, ww in l) + space_w * (len(l) - 1) for l in lines)
    panel_w = int(max_measured_w + panel_pad_x * 2)
    panel_h = int(total_h + panel_pad_y * 2)
    panel_x = center_pos[0] - panel_w // 2
    panel_y = center_pos[1] - panel_h // 2
    
    draw.rounded_rectangle(
        [panel_x, panel_y, panel_x + panel_w, panel_y + panel_h],
        radius=24,
        fill=(10, 14, 24, 215),
        outline=(250, 200, 21, 60),
        width=2
    )
    
    for l_idx, line in enumerate(lines):
        line_w = sum(ww for _, _, ww in line) + space_w * (len(line) - 1)
        cur_x = center_pos[0] - (line_w / 2)
        y_pos = start_y + (l_idx * line_h)
        
        for w_idx, word_str, ww in line:
            if w_idx == active_idx:
                w_color = (250, 200, 21, 255) # Highlight Gold
                # Small glow / pulse effect on active word
                for r in range(1, 4):
                    draw.text((cur_x, y_pos), word_str, font=FONT_SUBTITLE, fill=(250, 200, 21, 80), anchor="lt")
            else:
                w_color = get_word_highlight(word_str)
                
            draw_outlined_text(draw, (cur_x + ww/2, y_pos + line_h/2 - 6), word_str, FONT_SUBTITLE, fill_color=w_color, thickness=4, anchor="mm")
            cur_x += ww + space_w

def render_frame(t_sec, frame_idx, total_frames):
    # Determine active scene
    scene = None
    for sc in CUES:
        if sc["start"] <= t_sec <= sc["end"] + 0.05:
            scene = sc
            break
    if not scene:
        scene = CUES[-1]
        
    scene_dur = scene["end"] - scene["start"]
    local_prog = max(0.0, min(1.0, (t_sec - scene["start"]) / max(scene_dur, 0.01)))
    
    # Load and crop base image
    raw_img = Image.open(scene["asset"]).convert("RGBA")
    frame = get_ken_burns_frame(raw_img, WIDTH, HEIGHT, local_prog, scene["effect"])
    
    # Create overlay
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Cinematic Vignette
    draw.rectangle([0, 0, WIDTH, HEIGHT], outline=(0, 0, 0, 110), width=25)
    # Subtle top & bottom dark gradients for high contrast HUD
    for i in range(260):
        alpha = int(180 * (1.0 - i / 260.0))
        draw.line([(0, i), (WIDTH, i)], fill=(5, 8, 15, alpha))
    for i in range(320):
        alpha = int(210 * (i / 320.0))
        draw.line([(0, HEIGHT - 320 + i), (WIDTH, HEIGHT - 320 + i)], fill=(5, 8, 15, alpha))

    # --- TOP BRAND PILL (y=55) ---
    brand_text = "⚡ METAL MANIA IN CHINA • COLLECTOR VAULT"
    sample_img = Image.new("RGBA", (1, 1))
    s_draw = ImageDraw.Draw(sample_img)
    bw = int(s_draw.textlength(brand_text, font=FONT_BRAND)) + 48
    bx = (WIDTH - bw) // 2
    draw.rounded_rectangle([bx, 55, bx + bw, 105], radius=16, fill=(12, 16, 28, 230), outline=(250, 200, 21, 160), width=2)
    draw.text((WIDTH // 2, 80), brand_text, font=FONT_BRAND, fill=(255, 255, 255, 255), anchor="mm")

    # --- SCENE HOOK BADGE & HEADLINE (y=135) ---
    badge_text = scene["header_badge"]
    badgew = int(s_draw.textlength(badge_text, font=FONT_BADGE)) + 36
    badgex = (WIDTH - badgew) // 2
    draw.rounded_rectangle([badgex, 125, badgex + badgew, 168], radius=12, fill=(250, 200, 21, 230), outline=(255, 255, 255, 80), width=1)
    draw.text((WIDTH // 2, 146), badge_text, font=FONT_BADGE, fill=(10, 10, 10, 255), anchor="mm")

    # Main Headline Banner Card
    head_text = scene["header"]
    head_color = scene["header_color"]
    draw.rounded_rectangle([45, 185, WIDTH - 45, 275], radius=20, fill=(10, 15, 26, 235), outline=head_color, width=2)
    draw_outlined_text(draw, (WIDTH // 2, 230), head_text, FONT_HEADER, fill_color=head_color, thickness=4, anchor="mm")

    # --- KINETIC SUBTITLES (y=1460) ---
    active_sub = None
    for sub in scene["subtitles"]:
        if sub["start"] <= t_sec <= sub["end"] + 0.15:
            active_sub = sub
            break
            
    if active_sub:
        render_kinetic_subtitles(draw, active_sub["text"], t_sec, active_sub["start"], active_sub["end"], center_pos=(WIDTH // 2, 1460))

    # --- BOTTOM FOOTER / CTA BAR (y=1730) ---
    footer_str = scene["footer_text"]
    if scene["id"] == "scene_4":
        # High impact flashing CTA in final scene
        pulse = abs(math.sin(t_sec * 6.0))
        glow_alpha = int(180 + 75 * pulse)
        draw.rounded_rectangle([50, 1720, WIDTH - 50, 1820], radius=24, fill=(210, 30, 30, 240), outline=(250, 200, 21, glow_alpha), width=4)
        draw_outlined_text(draw, (WIDTH // 2, 1770), "🔥 COMPRAR AHORA: metalmaniach.com 🔥", FONT_CTA, fill_color=(255, 255, 255, 255), thickness=4, anchor="mm")
    else:
        draw.rounded_rectangle([50, 1735, WIDTH - 50, 1815], radius=20, fill=(10, 15, 26, 220), outline=(255, 255, 255, 40), width=2)
        draw_outlined_text(draw, (WIDTH // 2, 1775), footer_str, FONT_FOOTER, fill_color=(250, 200, 21, 255), thickness=3, anchor="mm")

    # --- GLOBAL DYNAMIC PROGRESS BAR (y=1870) ---
    overall_progress = min(1.0, max(0.0, t_sec / TOTAL_DURATION))
    pb_w = 980
    pb_x = (WIDTH - pb_w) // 2
    draw.rounded_rectangle([pb_x, 1865, pb_x + pb_w, 1877], radius=6, fill=(25, 30, 45, 255))
    draw.rounded_rectangle([pb_x, 1865, pb_x + int(pb_w * overall_progress), 1877], radius=6, fill=(250, 200, 21, 255))

    # Composite & return RGB
    final_frame = Image.alpha_composite(frame, overlay)
    return final_frame.convert("RGB")

def main():
    print("=" * 80)
    print("  METAL MANIA - GENERATING PROFESSIONAL COMMERCIAL SHORT (PROPUESTA 2)")
    print("=" * 80)
    
    temp_dir = os.path.join(BASE_DIR, "temp_metalmania_render")
    frames_dir = os.path.join(temp_dir, "frames")
    shutil.rmtree(temp_dir, ignore_errors=True)
    os.makedirs(frames_dir, exist_ok=True)
    
    total_frames = int(TOTAL_DURATION * FPS)
    print(f"[INFO] Rendering {total_frames} frames ({TOTAL_DURATION:.2f}s @ {FPS} FPS)...")
    
    for f in range(total_frames):
        t_sec = f / float(FPS)
        img = render_frame(t_sec, f, total_frames)
        img.save(os.path.join(frames_dir, f"frame_{f:05d}.jpg"), quality=93)
        if f % 90 == 0 or f == total_frames - 1:
            print(f"  -> Rendered frame {f+1}/{total_frames} ({t_sec:.2f}s) [{(f+1)/total_frames*100:.1f}%]")

    # Video assembly via ffmpeg
    raw_video = os.path.join(temp_dir, "raw_video.mp4")
    print(f"\n[INFO] Encoding video track with ffmpeg libx264...")
    cmd_encode = [
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", os.path.join(frames_dir, "frame_%05d.jpg"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-pix_fmt", "yuv420p",
        raw_video
    ]
    subprocess.run(cmd_encode, check=True)
    
    # Audio Muxing & Sidechain Mix
    voice_path = os.path.join(AUDIO_DIR, "metalmania_obi_short.mp3")
    music_path = os.path.join(MUSIC_DIR, "Severe Tire Damage.mp3")
    whoosh_path = os.path.join(BASE_DIR, "whoosh.wav")
    pop_path = os.path.join(BASE_DIR, "pop.wav")
    final_output = os.path.join(OUTPUT_DIR, "metalmania_propuesta2_ediciones_japonesas_final.mp4")
    
    print(f"\n[INFO] Assembling full multi-channel commercial audio mix...")
    print(f"  - Voice: Jorge TTS ({voice_path})")
    print(f"  - Music: Severe Tire Damage ({music_path}) @ -23dB")
    print(f"  - SFX: Transitions at 0.0s, 4.3s, 12.4s, 18.0s @ -6dB")
    
    # ffmpeg complex filter with SFX delays and sidechain mixing
    # Inputs:
    # 0: raw_video
    # 1: voice
    # 2: music
    # 3: whoosh
    # 4: pop
    
    filter_complex = (
        "[1:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=2.2[voice];"
        "[2:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=-23dB[bgmusic];"
        "[3:a]adelay=0|0,volume=-6dB[w0];"
        "[3:a]adelay=4300|4300,volume=-6dB[w1];"
        "[3:a]adelay=12400|12400,volume=-6dB[w2];"
        "[4:a]adelay=12450|12450,volume=-5dB[p0];"
        "[3:a]adelay=17960|17960,volume=-6dB[w3];"
        "[w0][w1][w2][p0][w3]amix=inputs=5:duration=longest:normalize=0[sfx_all];"
        "[voice][bgmusic][sfx_all]amix=inputs=3:duration=first:dropout_transition=2:normalize=0[outa]"
    )
    
    cmd_mux = [
        "ffmpeg", "-y",
        "-i", raw_video,
        "-i", voice_path,
        "-i", music_path,
        "-i", whoosh_path,
        "-i", pop_path,
        "-filter_complex", filter_complex,
        "-map", "0:v", "-map", "[outa]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "256k", "-ar", "44100", "-ac", "2",
        "-shortest",
        final_output
    ]
    
    subprocess.run(cmd_mux, check=True)
    
    # Verification
    if os.path.exists(final_output) and os.path.getsize(final_output) > 0:
        file_size_mb = os.path.getsize(final_output) / (1024 * 1024)
        print("\n" + "=" * 80)
        print(f"  [SUCCESS] COMMERCIAL SHORT RENDERED SUCCESSFULLY!")
        print(f"  File: {final_output}")
        print(f"  Size: {file_size_mb:.2f} MB")
        print(f"  Format: 1080x1920 (9:16 Vertical HD @ 30 FPS)")
        print(f"  Duration: ~{TOTAL_DURATION:.2f} seconds")
        print("=" * 80)
    else:
        raise RuntimeError("Render failed: Output file missing or empty.")

if __name__ == "__main__":
    main()
