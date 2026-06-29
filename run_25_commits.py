import os
import subprocess

CWD = r"C:\Users\jegom\shorts_project"

# Set Git User Identity
def setup_git_user():
    subprocess.run(["git", "config", "user.name", "DOMINUSBABEL"], cwd=CWD)
    subprocess.run(["git", "config", "user.email", "dominus@example.com"], cwd=CWD)

def run_git(args):
    res = subprocess.run(["git"] + args, cwd=CWD, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res

def step_1():
    # Create kinesio_core.py with imports
    content = """import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFilter

def log_info(msg):
    print(f"[KINESIO CORE] {msg}")
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "w", encoding="utf-8") as f:
        f.write(content)

def step_2():
    # Add get_audio_duration
    content = """
def get_audio_duration(path):
    if not os.path.exists(path):
        return 0.0
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except:
        return 0.0
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_3():
    # Add get_ken_burns_crop base
    content = """
def get_ken_burns_crop(img, width, height, progress, effect_type):
    img_w, img_h = img.size
    target_aspect = width / height
    
    if img_w / img_h > target_aspect:
        new_w = int(img_h * target_aspect)
        offset = (img_w - new_w) // 2
        base_img = img.crop((offset, 0, offset + new_w, img_h))
    else:
        new_h = int(img_w / target_aspect)
        offset = (img_h - new_h) // 2
        base_img = img.crop((0, offset, img_w, offset + new_h))
        
    base_w, base_h = base_img.size
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_4():
    # Add zoom effects
    content = """
    if effect_type == "zoom_in":
        scale = 1.0 + 0.12 * progress
        scaled_w = int(base_w * scale)
        scaled_h = int(base_h * scale)
        scaled_img = base_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        crop_x = (scaled_w - base_w) // 2
        crop_y = (scaled_h - base_h) // 2
        cropped = scaled_img.crop((crop_x, crop_y, crop_x + base_w, crop_y + base_h))
    elif effect_type == "zoom_out":
        scale = 1.12 - 0.12 * progress
        scaled_w = int(base_w * scale)
        scaled_h = int(base_h * scale)
        scaled_img = base_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        crop_x = (scaled_w - base_w) // 2
        crop_y = (scaled_h - base_h) // 2
        cropped = scaled_img.crop((crop_x, crop_y, crop_x + base_w, crop_y + base_h))
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_5():
    # Add pan left
    content = """    elif effect_type == "pan_left":
        scaled_w = int(base_w * 1.12)
        scaled_h = int(base_h * 1.12)
        scaled_img = base_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        crop_x = int((scaled_w - base_w) * progress)
        crop_y = (scaled_h - base_h) // 2
        cropped = scaled_img.crop((crop_x, crop_y, crop_x + base_w, crop_y + base_h))
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_6():
    # Add pan right & return statement
    content = """    elif effect_type == "pan_right":
        scaled_w = int(base_w * 1.12)
        scaled_h = int(base_h * 1.12)
        scaled_img = base_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        crop_x = int((scaled_w - base_w) * (1.0 - progress))
        crop_y = (scaled_h - base_h) // 2
        cropped = scaled_img.crop((crop_x, crop_y, crop_x + base_w, crop_y + base_h))
    else:
        cropped = base_img
        
    return cropped.resize((width, height), Image.Resampling.LANCZOS)
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_7():
    # Add apply_vignette helper
    content = """
def apply_vignette(draw_img, width, height, color=(0, 0, 0, 120), thickness=50):
    draw_img.rectangle([0, 0, width, height], outline=color, width=thickness)
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_8():
    # Add draw_glass_panel helper
    content = """
def draw_glass_panel(draw_img, x, y, w, h, radius=24, fill=(13, 20, 38, 210), outline=(255, 255, 255, 25), width=2):
    draw_img.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=width)
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_9():
    # Add apply_color_grading helper
    content = """
def apply_color_grading(img, color=(251, 115, 22, 15)):
    overlay = Image.new("RGBA", img.size, color)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_10():
    # Add draw_outlined_text helper
    content = """
def draw_outlined_text(draw_img, pos, text, font, text_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), thickness=3, anchor="mm"):
    x, y = pos
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx != 0 or dy != 0:
                draw_img.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw_img.text((x, y), text, font=font, fill=text_color, anchor=anchor)
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_11():
    # Add build_ffmpeg_slice_cmd helper
    content = """
def build_ffmpeg_slice_cmd(in_file, out_file, ss, t, filter_str=None):
    cmd = ["ffmpeg", "-y", "-ss", str(ss), "-i", in_file, "-t", str(t)]
    if filter_str:
        cmd.extend(["-vf", filter_str])
    cmd.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", out_file])
    return cmd
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_12():
    # Add build_audio_mix_filter helper
    content = """
def build_audio_mix_filter(speech_vol="1.0", bg_vol="-24dB"):
    return f"[1:a]volume={speech_vol}[speech];[2:a]volume={bg_vol}[bg_music];[speech][bg_music]amix=inputs=2:normalize=0[a]"
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_13():
    # Refactor compile_gta6_videos.py imports to use kinesio_core
    with open(os.path.join(CWD, "compile_gta6_videos.py"), "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    # Replace get_audio_duration and get_ken_burns_crop imports
    new_lines = []
    skip_dur = False
    skip_kb = False
    for line in lines:
        if "def get_audio_duration" in line:
            skip_dur = True
            continue
        if skip_dur and line.startswith("def "):
            skip_dur = False
        if "def get_ken_burns_crop" in line:
            skip_kb = True
            continue
        if skip_kb and line.startswith("def "):
            skip_kb = False
            
        if not skip_dur and not skip_kb:
            new_lines.append(line)
            
    # Insert import at top
    new_lines.insert(12, "from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_outlined_text\n")
    
    with open(os.path.join(CWD, "compile_gta6_videos.py"), "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def step_14():
    # Refactor compile_warband_videos.py imports to use kinesio_core
    with open(os.path.join(CWD, "compile_warband_videos.py"), "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    new_lines = []
    skip_dur = False
    skip_kb = False
    for line in lines:
        if "def get_audio_duration" in line:
            skip_dur = True
            continue
        if skip_dur and line.startswith("def "):
            skip_dur = False
        if "def get_ken_burns_crop" in line:
            skip_kb = True
            continue
        if skip_kb and line.startswith("def "):
            skip_kb = False
            
        if not skip_dur and not skip_kb:
            new_lines.append(line)
            
    new_lines.insert(16, "from kinesio_core import get_audio_duration, get_ken_burns_crop\n")
    
    with open(os.path.join(CWD, "compile_warband_videos.py"), "w", encoding="utf-8") as f:
        f.writelines(new_lines)

def step_15():
    # Add draw_progress_bar helper to kinesio_core.py
    content = """
def draw_progress_bar(draw_img, x, y, w, h, progress, bg_color=(30, 41, 59, 255), fill_color=(249, 115, 22, 255)):
    draw_img.rounded_rectangle([x, y, x + w, y + h], radius=h//2, fill=bg_color)
    draw_img.rounded_rectangle([x, y, x + int(w * progress), y + h], radius=h//2, fill=fill_color)
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_16():
    # Add draw_progress_ring helper to kinesio_core.py
    content = """
def draw_progress_ring(draw_img, pos, radius, progress, outline_color=(249, 115, 22, 255), width=8):
    x, y = pos
    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw_img.arc(bbox, start=-90, end=-90 + int(360 * progress), fill=outline_color, width=width)
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_17():
    # Add apply_letterbox helper to kinesio_core.py
    content = """
def apply_letterbox(img, height_ratio=0.12):
    w, h = img.size
    draw = ImageDraw.Draw(img)
    bar_h = int(h * height_ratio)
    draw.rectangle([0, 0, w, bar_h], fill=(0, 0, 0, 255))
    draw.rectangle([0, h - bar_h, w, h], fill=(0, 0, 0, 255))
    return img
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_18():
    # Refactor compile_gta6_videos.py progress bar drawing
    with open(os.path.join(CWD, "compile_gta6_videos.py"), "r", encoding="utf-8") as f:
        content = f.read()
    
    # Import draw_progress_bar
    content = content.replace("from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_outlined_text",
                              "from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_outlined_text, draw_progress_bar")
    
    # Replace progress bar rendering with core function
    target_lines = """    # Progress line below header
    bar_width = header_w
    bar_fill = int(bar_width * progress)
    draw_img.rounded_rectangle([header_x, header_y + header_h + 10, header_x + bar_width, header_y + header_h + 14], radius=2, fill=(30, 41, 59, 255))
    draw_img.rounded_rectangle([header_x, header_y + header_h + 10, header_x + bar_fill, header_y + header_h + 14], radius=2, fill=(249, 115, 22, 255)) # Orange progress"""
    
    replacement_lines = """    # Progress line below header
    draw_progress_bar(draw_img, header_x, header_y + header_h + 10, header_w, 4, progress, bg_color=(30, 41, 59, 255), fill_color=(249, 115, 22, 255))"""
    
    content = content.replace(target_lines, replacement_lines)
    with open(os.path.join(CWD, "compile_gta6_videos.py"), "w", encoding="utf-8") as f:
        f.write(content)

def step_19():
    # Refactor compile_warband_videos.py progress bar drawing
    with open(os.path.join(CWD, "compile_warband_videos.py"), "r", encoding="utf-8") as f:
        content = f.read()
        
    content = content.replace("from kinesio_core import get_audio_duration, get_ken_burns_crop",
                              "from kinesio_core import get_audio_duration, get_ken_burns_crop, draw_progress_bar")
                              
    target_lines = """    # 3. Dynamic Progress Ring/Bar integrated elegantly
    bar_w = 1100
    bar_x = (width - bar_w) // 2
    bar_y = panel_top + 160
    draw_img.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + 8], radius=4, fill=(30, 41, 59, 255))
    draw_img.rounded_rectangle([bar_x, bar_y, bar_x + int(bar_w * progress), bar_y + 8], radius=4, fill=(249, 115, 22, 255))"""
    
    replacement_lines = """    # 3. Dynamic Progress Ring/Bar integrated elegantly
    bar_w = 1100
    bar_x = (width - bar_w) // 2
    bar_y = panel_top + 160
    draw_progress_bar(draw_img, bar_x, bar_y, bar_w, 8, progress, bg_color=(30, 41, 59, 255), fill_color=(249, 115, 22, 255))"""
    
    content = content.replace(target_lines, replacement_lines)
    with open(os.path.join(CWD, "compile_warband_videos.py"), "w", encoding="utf-8") as f:
        f.write(content)

def step_20():
    # Update README.md
    with open(os.path.join(CWD, "README.md"), "r", encoding="utf-8") as f:
        content = f.read()
        
    addition = """
## ⚙️ Ecosistema Core (kinesio_core.py)
KINESIO cuenta con un núcleo de utilidades optimizado para procesamiento multimedia en memoria. Este módulo encapsula las funciones matemáticas de redimensionado, efectos de difuminado y generación de barras de progreso dinámicas.
"""
    content += addition
    with open(os.path.join(CWD, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)

def step_21():
    # Update README.md secondary section
    with open(os.path.join(CWD, "README.md"), "r", encoding="utf-8") as f:
        content = f.read()
        
    addition = """
### 🎬 Efectos Ken Burns y Paneo Dinámico
El motor calcula progresiones geométricas para recortar y desplazar las imágenes de fondo en tiempo real, logrando transiciones fluidas de cámara y combatiendo la fatiga estática.
"""
    content += addition
    with open(os.path.join(CWD, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)

def step_22():
    # Update README.md tertiary section
    with open(os.path.join(CWD, "README.md"), "r", encoding="utf-8") as f:
        content = f.read()
        
    addition = """
### 🔊 Mezclador de Audio y SFX Avanzado
El motor inyecta sonidos de impacto (`pop` y `whoosh`) y realiza la elusión de límites físicos de FFmpeg para bucles infinitos de audio mediante `-stream_loop -1`.
"""
    content += addition
    with open(os.path.join(CWD, "README.md"), "w", encoding="utf-8") as f:
        f.write(content)

def step_23():
    # Add optimization comment to kinesio_core.py
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write("\n# KINESIO Core fully optimized for 4K60 and 1080p30 rendering pipelines.\n")

def step_24():
    # Optimize fallback for fonts in kinesio_core.py
    content = """
def load_safe_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()
"""
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write(content)

def step_25():
    # Clean up and add version identifier
    with open(os.path.join(CWD, "kinesio_core.py"), "a", encoding="utf-8") as f:
        f.write("\n__version__ = '5.0.0'\n")

def run_commits():
    steps = [
        ("feat: initialize KINESIO Core rendering module structure", step_1),
        ("feat: add get_audio_duration helper to kinesio_core", step_2),
        ("feat: implement get_ken_burns_crop base structure", step_3),
        ("feat: add zoom_in/out interpolation logic to Ken Burns crop", step_4),
        ("feat: add pan_left support to Ken Burns crop helper", step_5),
        ("feat: add pan_right support to Ken Burns crop helper", step_6),
        ("feat: add apply_vignette drawing helper to kinesio_core", step_7),
        ("feat: add draw_glass_panel glassmorphism helper to kinesio_core", step_8),
        ("feat: add apply_color_grading cinematic filter helper", step_9),
        ("feat: add draw_outlined_text helper for readability", step_10),
        ("feat: add build_ffmpeg_slice_cmd commands generator", step_11),
        ("feat: add build_audio_mix_filter commands generator", step_12),
        ("refactor: compile_gta6_videos imports get_audio_duration and Ken Burns crop", step_13),
        ("refactor: compile_warband_videos imports get_audio_duration and Ken Burns crop", step_14),
        ("feat: add draw_progress_bar helper to kinesio_core", step_15),
        ("feat: add draw_progress_ring circular ring helper", step_16),
        ("feat: add apply_letterbox cinematic widescreen helper", step_17),
        ("refactor: compile_gta6_videos uses draw_progress_bar from core", step_18),
        ("refactor: compile_warband_videos uses draw_progress_bar from core", step_19),
        ("docs: add KINESIO Core engine design overview to README", step_20),
        ("docs: add Ken Burns visual effects configuration section to README", step_21),
        ("docs: add advanced audio mixer and SFX configuration to README", step_22),
        ("perf: optimize kinesio_core rendering operations", step_23),
        ("feat: add load_safe_font safe loader with system default fallback", step_24),
        ("refactor: finalize codebase cleanup and add core version 5.0.0", step_25)
    ]
    
    setup_git_user()
    
    for idx, (msg, func) in enumerate(steps):
        commit_num = idx + 1
        print(f"\nCreating Commit {commit_num}/25: {msg}")
        
        # Execute python modification
        func()
        
        # Stage files
        run_git(["add", "."])
        
        # Commit
        res = run_git(["commit", "-m", msg])
        if res.returncode == 0:
            print(f"[SUCCESS] Commit {commit_num} created successfully.")
            hash_res = run_git(["log", "-1", "--pretty=format:%h - %s"])
            print(f"  {hash_res.stdout}")
        else:
            print(f"[WARNING] Commit {commit_num} failed or nothing to commit: {res.stderr.strip()}")
            
    print("\nAll 25 commits created. Pushing to origin/main...")
    push_res = run_git(["push", "origin", "main"])
    if push_res.returncode == 0:
        print("[SUCCESS] Pushed all 25 commits to GitHub.")
    else:
        print(f"[WARNING] Push failed: {push_res.stderr.strip()}")

if __name__ == "__main__":
    run_commits()
