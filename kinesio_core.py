# -*- coding: utf-8 -*-
"""
KINESIO CORE ENGINE V5.5.0
Supports Series Badge Overlay (SERIE 1: PARTE 1/3), Tri-Tone Kinetic Subtitles (#FAC815 / #FF4D4D / #00E5FF),
Millisecond-Precise VTT Synchronization, Multi-Asset B-Roll Rotation, and Sidechain Audio Ducking.
"""

import os
import sys
import json
import math
import subprocess
from PIL import Image, ImageDraw, ImageFilter, ImageFont

__version__ = "5.5.0"

def log_info(msg):
    print(f"[KINESIO CORE] {msg}")

def get_audio_duration(filepath):
    if not filepath or not os.path.exists(filepath):
        return None
    abs_p = os.path.abspath(filepath)
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "csv=p=0",
        abs_p
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except Exception as e:
        log_info(f"Failed to get audio duration for {filepath}: {e}")
        return None

def parse_vtt_subtitles(vtt_file):
    if not vtt_file or not os.path.exists(vtt_file):
        return []
    cues = []
    try:
        with open(vtt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if "-->" in line:
                parts = line.split("-->")
                def to_sec(t_str):
                    t_str = t_str.strip().replace(',', '.')
                    sp = t_str.split(':')
                    if len(sp) == 3:
                        return float(sp[0])*3600 + float(sp[1])*60 + float(sp[2])
                    elif len(sp) == 2:
                        return float(sp[0])*60 + float(sp[1])
                    return 0.0

                start_sec = to_sec(parts[0])
                end_sec = to_sec(parts[1])
                text_lines = []
                j = i + 1
                while j < len(lines) and lines[j].strip() and "-->" not in lines[j]:
                    text_lines.append(lines[j].strip())
                    j += 1
                text = " ".join(text_lines)
                if text:
                    cues.append({'start': start_sec, 'end': end_sec, 'text': text})
                i = j
            else:
                i += 1
    except Exception as e:
        log_info(f"VTT parse notice: {e}")
    return cues

def get_ken_burns_crop(img, width, height, progress, effect_type="zoom_in"):
    base_w, base_h = img.size
    
    if effect_type == "zoom_in":
        scale = 1.0 - (0.15 * progress)
    elif effect_type == "zoom_out":
        scale = 0.85 + (0.15 * progress)
    elif effect_type == "pan_left":
        scale = 0.88
    elif effect_type == "pan_right":
        scale = 0.88
    else:
        scale = 0.90
        
    crop_w = int(base_w * scale)
    crop_h = int(base_h * scale)
    
    target_aspect = width / height
    if crop_w / crop_h > target_aspect:
        crop_w = int(crop_h * target_aspect)
    else:
        crop_h = int(crop_w / target_aspect)
        
    if effect_type == "pan_left":
        crop_x = int((base_w - crop_w) * (1.0 - progress))
        crop_y = (base_h - crop_h) // 2
    elif effect_type == "pan_right":
        crop_x = int((base_w - crop_w) * progress)
        crop_y = (base_h - crop_h) // 2
    else:
        crop_x = (base_w - crop_w) // 2
        crop_y = (base_h - crop_h) // 2
        
    crop_x = max(0, min(base_w - crop_w, crop_x))
    crop_y = max(0, min(base_h - crop_h, crop_y))
    
    cropped = img.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
    return cropped.resize((width, height), Image.Resampling.BILINEAR)

def get_multi_broll_crop(img_list, width, height, progress, effect_type="zoom_in"):
    if not img_list:
        return Image.new("RGB", (width, height), (12, 16, 28))
    if len(img_list) == 1:
        return get_ken_burns_crop(img_list[0], width, height, progress, effect_type)
        
    num_imgs = len(img_list)
    step = 1.0 / num_imgs
    idx = min(int(progress / step), num_imgs - 1)
    
    local_prog = (progress - (idx * step)) / step
    curr_crop = get_ken_burns_crop(img_list[idx], width, height, local_prog, effect_type).convert("RGBA")
    
    if idx < num_imgs - 1 and local_prog > 0.85:
        trans_alpha = (local_prog - 0.85) / 0.15
        next_crop = get_ken_burns_crop(img_list[idx + 1], width, height, 0.0, effect_type).convert("RGBA")
        blended = Image.blend(curr_crop, next_crop, trans_alpha)
        return blended.convert("RGB")
        
    return curr_crop.convert("RGB")

def apply_vignette(draw_img, width, height, color=(0, 0, 0, 140), thickness=40):
    draw_img.rectangle([0, 0, width, height], outline=color, width=thickness)

def draw_glass_panel(draw_img, x, y, w, h, radius=24, fill=(10, 15, 30, 220), outline=(255, 255, 255, 30), width=2):
    draw_img.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill, outline=outline, width=width)

def draw_series_badge(draw_img, x, y, series_text, font, fill=(255, 77, 77, 230), text_color=(255, 255, 255, 255)):
    # Draw top-right floating series badge
    sample_img = Image.new("RGBA", (1, 1))
    sample_draw = ImageDraw.Draw(sample_img)
    w_text = sample_draw.textlength(series_text, font=font)
    w_panel = int(w_text + 40)
    h_panel = 54
    draw_glass_panel(draw_img, x - w_panel, y, w_panel, h_panel, radius=16, fill=fill, outline=(255, 255, 255, 50))
    draw_img.text((x - (w_panel / 2), y + 27), series_text, font=font, fill=text_color, anchor="mm")

def draw_outlined_text(draw_img, pos, text, font, text_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), thickness=4, anchor="mm"):
    x, y = pos
    for dx in range(-thickness, thickness + 1):
        for dy in range(-thickness, thickness + 1):
            if dx != 0 or dy != 0:
                draw_img.text((x + dx, y + dy), text, font=font, fill=outline_color, anchor=anchor)
    draw_img.text((x, y), text, font=font, fill=text_color, anchor=anchor)

def get_word_highlight_color(word):
    clean = word.lower().strip(".,!?:;\"'")
    alert_keywords = ["error", "muerte", "disparo", "sangre", "orgullo", "morir", "matar", "tragedia", "walter", "heisenberg", "asesinado", "400%", "multa", "trampa"]
    code_keywords = ["regla", "reglas", "código", "codigo", "profesional", "respeto", "kaylee", "niña", "principios", "lealtad", "mitad", "medidas"]
    
    if any(k in clean for k in alert_keywords):
        return (255, 77, 77, 255) # Red Alert
    if any(k in clean for k in code_keywords):
        return (0, 229, 255, 255) # Electric Cyan
    return (250, 200, 21, 255) # Yellow Neon default

def draw_kinetic_caption_precise(draw_img, pos, text, font, active_word_idx=0, text_color=(255, 255, 255, 255), outline_color=(0, 0, 0, 255), thickness=4, max_width=900):
    words = text.split()
    if not words:
        return
        
    x_center, y_center = pos
    sample_img = Image.new("RGBA", (1, 1))
    sample_draw = ImageDraw.Draw(sample_img)
    space_w = sample_draw.textlength(" ", font=font)
    
    lines = []
    curr_line = []
    curr_line_w = 0
    
    for idx, w in enumerate(words):
        w_w = sample_draw.textlength(w, font=font)
        if curr_line and (curr_line_w + space_w + w_w > max_width):
            lines.append(curr_line)
            curr_line = [(idx, w, w_w)]
            curr_line_w = w_w
        else:
            curr_line.append((idx, w, w_w))
            curr_line_w += (space_w if curr_line else 0) + w_w
    if curr_line:
        lines.append(curr_line)
        
    line_height = font.size + 14
    total_height = len(lines) * line_height
    start_y = y_center - (total_height / 2) + (line_height / 2)
    
    for line_idx, line_words in enumerate(lines):
        line_total_w = sum(w_w for _, _, w_w in line_words) + space_w * (len(line_words) - 1)
        curr_x = x_center - (line_total_w / 2)
        y_pos = start_y + (line_idx * line_height)
        
        for w_global_idx, word_str, w_w in line_words:
            if w_global_idx == active_word_idx:
                color = get_word_highlight_color(word_str)
            else:
                color = text_color
                
            for dx in range(-thickness, thickness + 1):
                for dy in range(-thickness, thickness + 1):
                    if dx != 0 or dy != 0:
                        draw_img.text((curr_x + dx, y_pos + dy), word_str, font=font, fill=outline_color)
            draw_img.text((curr_x, y_pos), word_str, font=font, fill=color)
            curr_x += w_w + space_w

def draw_progress_bar(draw_img, x, y, w, h, progress, bg_color=(30, 41, 59, 255), fill_color=(250, 200, 21, 255)):
    draw_img.rounded_rectangle([x, y, x + w, y + h], radius=h//2, fill=bg_color)
    draw_img.rounded_rectangle([x, y, x + int(w * progress), y + h], radius=h//2, fill=fill_color)

def load_safe_font(font_path, size):
    try:
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

class KinesioVideoBuilder:
    def __init__(self, project_name, width=1920, height=1080, fps=30):
        self.project_name = project_name
        self.width = width
        self.height = height
        self.fps = fps
        self.scenes = []
        self.bg_music = None
        self.bg_music_vol = -24
        self.series_badge = None # e.g. "TRILOGÍA 1: PARTE 1 DE 3"
        self.enable_split_screen = True if height > width else False
        
    def add_scene(self, title, duration, asset_path=None, template="default", effect_type="zoom_in", gameplay_overlay=None):
        self.scenes.append({
            "title": title,
            "duration": duration,
            "asset_path": asset_path,
            "template": template,
            "effect_type": effect_type,
            "gameplay_overlay": gameplay_overlay
        })
        
    def set_series_badge(self, badge_text):
        self.series_badge = badge_text
        
    def set_background_music(self, path, volume=-24):
        self.bg_music = path
        self.bg_music_vol = volume
        
    def build(self, output_path, voice_audio_path=None):
        log_info(f"Building video project: {self.project_name}")
        temp_dir = f"temp_builder_{self.project_name}"
        os.makedirs(temp_dir, exist_ok=True)
        
        vtt_cues = []
        if voice_audio_path:
            vtt_path = voice_audio_path.replace(".mp3", ".vtt")
            if os.path.exists(vtt_path):
                vtt_cues = parse_vtt_subtitles(vtt_path)

        font_title_short = load_safe_font("C:\\Windows\\Fonts\\segoeuib.ttf", 38)
        font_sub_short = load_safe_font("C:\\Windows\\Fonts\\segoeuib.ttf", 46)
        font_badge_short = load_safe_font("C:\\Windows\\Fonts\\segoeuib.ttf", 24)
        font_title_essay = load_safe_font("C:\\Windows\\Fonts\\segoeuib.ttf", 54)
        font_sub_essay = load_safe_font("C:\\Windows\\Fonts\\segoeui.ttf", 36)
        
        segment_files = []
        cumulative_time = 0.0
        
        for idx, sc in enumerate(self.scenes):
            seg_file = os.path.join(temp_dir, f"scene_{idx:02d}.mp4")
            dur = sc["duration"]
            title = sc["title"]
            asset = sc["asset_path"]
            effect = sc["effect_type"]
            
            frame_dir = os.path.join(temp_dir, f"frames_{idx}")
            import shutil
            shutil.rmtree(frame_dir, ignore_errors=True)
            os.makedirs(frame_dir, exist_ok=True)
            total_frames = int(dur * self.fps)
            
            img_list = []
            if isinstance(asset, list):
                for a in asset:
                    if a and os.path.exists(a):
                        try:
                            img_list.append(Image.open(a))
                        except:
                            pass
            elif isinstance(asset, str) and os.path.exists(asset):
                try:
                    img_list.append(Image.open(asset))
                except:
                    pass
            if not img_list:
                img_list = [Image.new("RGB", (1920, 1080), (20, 30, 50))]
                
            for f_idx in range(total_frames):
                progress = f_idx / total_frames
                t_sec = cumulative_time + (f_idx / self.fps)
                
                active_cue = next((c for c in vtt_cues if c['start'] <= t_sec <= c['end']), None)
                active_text = active_cue['text'] if active_cue else ""
                
                if self.height > self.width and self.enable_split_screen: # Vertical Short (1080x1920)
                    frame_img = Image.new("RGB", (1080, 1920), (12, 16, 28))
                    
                    top_crop = get_multi_broll_crop(img_list, 1080, 960, progress, effect)
                    frame_img.paste(top_crop, (0, 0))
                    
                    draw = ImageDraw.Draw(frame_img)
                    draw.line([(0, 960), (1080, 960)], fill=(250, 200, 21, 255), width=6)
                    
                    apply_vignette(draw, 1080, 1920, thickness=25)
                    
                    if self.series_badge:
                        draw_series_badge(draw, 1020, 50, self.series_badge.upper(), font_badge_short)
                        
                    draw_glass_panel(draw, 60, 1040, 960, 780, radius=32, fill=(10, 15, 30, 230), outline=(255, 255, 255, 35))
                    draw_outlined_text(draw, (540, 1110), title.upper(), font_title_short, text_color=(250, 200, 21, 255))
                    
                    if active_text and active_cue:
                        cue_start = active_cue['start']
                        cue_end = active_cue['end']
                        cue_dur = max(cue_end - cue_start, 0.1)
                        cue_prog = max(0.0, min(1.0, (t_sec - cue_start) / cue_dur))
                        words_sub = active_text.split()
                        active_word_idx = min(int(cue_prog * len(words_sub)), max(len(words_sub) - 1, 0))
                        draw_kinetic_caption_precise(draw, (540, 1400), active_text, font_sub_short, active_word_idx=active_word_idx, max_width=860)
                    else:
                        draw_kinetic_caption_precise(draw, (540, 1400), title.upper(), font_sub_short, active_word_idx=0, max_width=860)
                        
                    draw_progress_bar(draw, 140, 1720, 800, 8, progress, fill_color=(250, 200, 21, 255))
                    
                else: # Widescreen Video Essay (1920x1080)
                    frame_img = get_multi_broll_crop(img_list, 1920, 1080, progress, effect)
                    
                    draw = ImageDraw.Draw(frame_img)
                    apply_vignette(draw, 1920, 1080, thickness=40)
                    draw_glass_panel(draw, 360, 40, 1200, 90, radius=20, fill=(10, 15, 30, 210))
                    draw_outlined_text(draw, (960, 85), title.upper(), font_title_essay, text_color=(250, 200, 21, 255))
                    
                    sub_display = active_text if active_text else ""
                    if sub_display:
                        draw_glass_panel(draw, 200, 890, 1520, 120, radius=24, fill=(10, 15, 30, 230), outline=(255, 255, 255, 40))
                        draw_outlined_text(draw, (960, 950), sub_display, font_sub_essay, text_color=(255, 255, 255, 255))
                        
                    draw_progress_bar(draw, 260, 1030, 1400, 6, progress, fill_color=(250, 200, 21, 255))
                    
                os.makedirs(frame_dir, exist_ok=True)
                frame_img.save(os.path.join(frame_dir, f"frame_{f_idx:05d}.jpg"), quality=90)
                
            cumulative_time += dur
            
            cmd_frames = [
                "ffmpeg", "-y", "-framerate", str(self.fps),
                "-i", os.path.join(frame_dir, "frame_%05d.jpg"),
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                seg_file
            ]
            subprocess.run(cmd_frames, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            segment_files.append(seg_file)
            
        # Concat segments
        concat_list_file = os.path.join(temp_dir, "concat.txt")
        with open(concat_list_file, "w", encoding="utf-8") as f:
            for sf in segment_files:
                f.write(f"file '{os.path.abspath(sf)}'\n")
                
        raw_video = os.path.join(temp_dir, "raw_concat.mp4")
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list_file,
            "-c", "copy", raw_video
        ]
        subprocess.run(cmd_concat, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        
        # Audio Muxing & Ducking (Loud & Crystal Clear Voice + Subtly Ducked Music)
        music_path = self.bg_music if (self.bg_music and os.path.exists(self.bg_music)) else None
        
        if voice_audio_path and os.path.exists(voice_audio_path) and music_path:
            cmd_audio = [
                "ffmpeg", "-y",
                "-i", raw_video,
                "-i", voice_audio_path,
                "-i", music_path,
                "-filter_complex",
                f"[1:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=2.8[voice];[2:a]aformat=sample_rates=44100:channel_layouts=stereo,volume={self.bg_music_vol}dB[bg];[voice][bg]amix=inputs=2:duration=first:dropout_transition=2:normalize=0[outa]",
                "-map", "0:v", "-map", "[outa]",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-ac", "2",
                "-shortest",
                output_path
            ]
        elif voice_audio_path and os.path.exists(voice_audio_path):
            cmd_audio = [
                "ffmpeg", "-y",
                "-i", raw_video,
                "-i", voice_audio_path,
                "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                output_path
            ]
        else:
            cmd_audio = [
                "ffmpeg", "-y",
                "-i", raw_video,
                "-c:v", "copy",
                output_path
            ]
            
        subprocess.run(cmd_audio, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        log_info(f"[SUCCESS] Video fully compiled at {output_path}")

        # Cleanup frame directories
        try:
            for idx in range(len(self.scenes)):
                fd = os.path.join(temp_dir, f"frames_{idx}")
                if os.path.exists(fd):
                    import shutil
                    shutil.rmtree(fd, ignore_errors=True)
        except Exception as e:
            log_info(f"Cleanup note: {e}")
