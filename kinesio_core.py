import os
import sys
import subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont

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

def build_audio_mix_filter(speech_vol="1.0", bg_vol="-24dB"):
    return f"[1:a]volume={speech_vol}[speech];[2:a]volume={bg_vol}[bg_music];[speech][bg_music]amix=inputs=2:normalize=0[a]"

def draw_progress_bar(draw_img, x, y, w, h, progress, bg_color=(30, 41, 59, 255), fill_color=(249, 115, 22, 255)):
    draw_img.rounded_rectangle([x, y, x + w, y + h], radius=h//2, fill=bg_color)
    draw_img.rounded_rectangle([x, y, x + int(w * progress), y + h], radius=h//2, fill=fill_color)

def draw_progress_ring(draw_img, pos, radius, progress, outline_color=(249, 115, 22, 255), width=8):
    x, y = pos
    bbox = [x - radius, y - radius, x + radius, y + radius]
    draw_img.arc(bbox, start=-90, end=-90 + int(360 * progress), fill=outline_color, width=width)

def apply_letterbox(img, height_ratio=0.12):
    w, h = img.size
    draw = ImageDraw.Draw(img)
    bar_h = int(h * height_ratio)
    draw.rectangle([0, 0, w, bar_h], fill=(0, 0, 0, 255))
    draw.rectangle([0, h - bar_h, w, h], fill=(0, 0, 0, 255))
    return img

def load_safe_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

class KinesioVideoBuilder:
    """Generalized orchestration engine to compile any type of widescreen essays or vertical shorts."""
    def __init__(self, project_name, width=1920, height=1080, fps=30):
        self.project_name = project_name
        self.width = width
        self.height = height
        self.fps = fps
        self.scenes = []
        self.bg_music = None
        self.bg_music_vol = -24
        self.sfx_tracks = []
        
    def add_scene(self, title, duration, asset_path=None, template="default", effect_type="zoom_in", gameplay_overlay=None):
        self.scenes.append({
            "title": title,
            "duration": duration,
            "asset_path": asset_path,
            "template": template,
            "effect_type": effect_type,
            "gameplay_overlay": gameplay_overlay
        })
        
    def set_background_music(self, path, volume=-24):
        self.bg_music = path
        self.bg_music_vol = volume
        
    def add_sfx(self, path, delay_seconds, volume=-6):
        self.sfx_tracks.append({
            "path": path,
            "delay": delay_seconds,
            "volume": volume
        })
        
    def build(self, output_path, voice_audio_path=None):
        log_info(f"Building generalized video project: {self.project_name}")
        temp_dir = f"temp_builder_{self.project_name}"
        os.makedirs(temp_dir, exist_ok=True)
        
        segment_files = []
        for idx, sc in enumerate(self.scenes):
            seg_file = os.path.join(temp_dir, f"scene_{idx:02d}.mp4")
            dur = sc["duration"]
            title = sc["title"]
            asset = sc["asset_path"]
            effect = sc["effect_type"]
            overlay = sc["gameplay_overlay"]
            
            # If gameplay overlay is present, slice and scale
            if overlay and os.path.exists(overlay):
                cmd_slice = build_ffmpeg_slice_cmd(overlay, seg_file, 0.0, dur)
                subprocess.run(cmd_slice, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                # Render slides dynamically
                frame_dir = os.path.join(temp_dir, f"frames_{idx}")
                os.makedirs(frame_dir, exist_ok=True)
                total_frames = int(dur * self.fps)
                
                img_asset = Image.open(asset) if asset and os.path.exists(asset) else None
                font_title = load_safe_font("C:\\Windows\\Fonts\\segoeuib.ttf", 55 if self.width > self.height else 40)
                font_sub = load_safe_font("C:\\Windows\\Fonts\\segoeui.ttf", 32 if self.width > self.height else 26)
                
                for f_idx in range(total_frames):
                    progress = f_idx / total_frames
                    
                    if img_asset:
                        frame_img = get_ken_burns_crop(img_asset, self.width, self.height, progress, effect)
                        frame_img = frame_img.filter(ImageFilter.GaussianBlur(15))
                    else:
                        frame_img = Image.new("RGB", (self.width, self.height), (15, 20, 35))
                        
                    draw = ImageDraw.Draw(frame_img)
                    apply_vignette(draw, self.width, self.height)
                    
                    # Draw title card panel
                    if self.width > self.height: # Widescreen
                        draw_glass_panel(draw, self.width//2 - 600, self.height//2 - 200, 1200, 400)
                        draw_outlined_text(draw, (self.width//2, self.height//2 - 50), title.upper(), font_title)
                        draw_progress_bar(draw, self.width//2 - 500, self.height//2 + 80, 1000, 8, progress)
                    else: # Vertical Short
                        draw_glass_panel(draw, 90, 400, 900, 700)
                        draw_outlined_text(draw, (self.width//2, 550), title.upper(), font_title)
                        draw_progress_bar(draw, 140, 950, 800, 6, progress)
                        
                    frame_img.save(os.path.join(frame_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
                    
                cmd_frames = [
                    "ffmpeg", "-y", "-framerate", str(self.fps),
                    "-i", os.path.join(frame_dir, "frame_%05d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-t", f"{dur:.2f}",
                    seg_file
                ]
                subprocess.run(cmd_frames, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                
            if os.path.exists(seg_file) and os.path.getsize(seg_file) > 0:
                segment_files.append(seg_file)
                
        # Concatenate scenes
        if not segment_files:
            log_info("[ERROR] No segments compiled successfully.")
            return False
            
        raw_video = os.path.join(temp_dir, "raw_video.mp4")
        concat_inputs = []
        filter_parts = []
        for idx, sf in enumerate(segment_files):
            concat_inputs.extend(["-i", sf])
            filter_parts.append(f"[{idx}:v]")
            
        filter_str = "".join(filter_parts) + f"concat=n={len(segment_files)}:v=1:a=0[v]"
        cmd_concat = ["ffmpeg", "-y"] + concat_inputs + ["-filter_complex", filter_str, "-map", "[v]", "-c:v", "libx264", "-pix_fmt", "yuv420p", raw_video]
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Audio track assembly
        audio_inputs = ["-i", raw_video]
        audio_mix = ""
        
        if voice_audio_path and os.path.exists(voice_audio_path):
            audio_inputs.extend(["-i", voice_audio_path])
            audio_mix += "[1:a]volume=1.0[speech];"
            
        if self.bg_music and os.path.exists(self.bg_music):
            audio_inputs.extend(["-stream_loop", "-1", "-i", self.bg_music])
            music_idx = len(audio_inputs) - 1
            audio_mix += f"[{music_idx}:a]volume={self.bg_music_vol}dB[bg_music];"
            
        if voice_audio_path and self.bg_music:
            audio_mix += "[speech][bg_music]amix=inputs=2:normalize=0[a]"
        elif voice_audio_path:
            audio_mix += "[speech]anull[a]"
        elif self.bg_music:
            audio_mix += "[bg_music]anull[a]"
        else:
            audio_mix = "[0:a]anull[a]"
            
        cmd_final = ["ffmpeg", "-y"] + audio_inputs + ["-filter_complex", audio_mix, "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-shortest", output_path]
        res = subprocess.run(cmd_final, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Clean up temp
        try:
            import shutil
            shutil.rmtree(temp_dir)
        except:
            pass
            
        if res.returncode == 0:
            log_info(f"[SUCCESS] Video fully compiled at {output_path}")
            return True
        else:
            log_info(f"[ERROR] Final assembly failed: {res.stderr.decode('utf-8', errors='ignore')}")
            return False

__version__ = '5.0.0'

