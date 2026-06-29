import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFilter

def log_info(msg):
    print(f"[KINESIO CORE] {msg}")

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
    elif effect_type == "pan_left":
        scaled_w = int(base_w * 1.12)
        scaled_h = int(base_h * 1.12)
        scaled_img = base_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        crop_x = int((scaled_w - base_w) * progress)
        crop_y = (scaled_h - base_h) // 2
        cropped = scaled_img.crop((crop_x, crop_y, crop_x + base_w, crop_y + base_h))
    elif effect_type == "pan_right":
        scaled_w = int(base_w * 1.12)
        scaled_h = int(base_h * 1.12)
        scaled_img = base_img.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
        crop_x = int((scaled_w - base_w) * (1.0 - progress))
        crop_y = (scaled_h - base_h) // 2
        cropped = scaled_img.crop((crop_x, crop_y, crop_x + base_w, crop_y + base_h))
    else:
        cropped = base_img
        
    return cropped.resize((width, height), Image.Resampling.LANCZOS)

def apply_vignette(draw_img, width, height, color=(0, 0, 0, 120), thickness=50):
    draw_img.rectangle([0, 0, width, height], outline=color, width=thickness)

def draw_glass_panel(draw_img, x, y, w, h, radius=24, fill=(13, 20, 38, 210), outline=(255, 255, 255, 25), width=2):
    draw_img.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=width)

def apply_color_grading(img, color=(251, 115, 22, 15)):
    overlay = Image.new("RGBA", img.size, color)
    return Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")

def draw_outlined_text(draw_img, pos, text, font, text_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), thickness=3, anchor="mm"):
    x, y = pos
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx != 0 or dy != 0:
                draw_img.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw_img.text((x, y), text, font=font, fill=text_color, anchor=anchor)

def build_ffmpeg_slice_cmd(in_file, out_file, ss, t, filter_str=None):
    cmd = ["ffmpeg", "-y", "-ss", str(ss), "-i", in_file, "-t", str(t)]
    if filter_str:
        cmd.extend(["-vf", filter_str])
    cmd.extend(["-c:v", "libx264", "-pix_fmt", "yuv420p", "-an", out_file])
    return cmd
