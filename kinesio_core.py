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
