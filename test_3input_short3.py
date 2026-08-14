import os
import subprocess

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
MUSIC_DIR = os.path.join(PROJECT_DIR, "music")
VIDEO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_720p.mp4")
AUDIO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_audio.webm")

spec = {
    "id": 3,
    "category": "Explosions & Tanks",
    "title_en": "Hidden in the Bush at 10 Meters: The Ultimate Anti-Tank Trap 🚜 #shorts",
    "banner": "10m ANTI-TANK AMBUSH TRAP",
    "music": "Volatile Reaction.mp3",
    "start": "00:06:22",
    "to": "00:06:50"
}

banner_clean = spec['banner'].replace(":", "\\:").replace("'", "")
music_file = os.path.join(MUSIC_DIR, spec['music'])
output_path = os.path.join(PROJECT_DIR, "gates_of_hell_short_3_final.mp4")

video_filter = (
    "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,"
    "crop=1080:1920,"
    "eq=contrast=1.12:brightness=0.02:saturation=1.2,"
    "unsharp=5:5:0.8:5:5:0.0,"
    f"drawtext=text='{banner_clean}':fontcolor=yellow:fontsize=40:x=(w-text_w)/2:y=180:box=1:boxcolor=black@0.7:boxborderw=12[v]"
)

filter_complex = f"{video_filter};[1:a]volume=1.0[a1];[2:a]volume=0.07[a2];[a1][a2]amix=inputs=2:duration=first[a]"

cmd = [
    "ffmpeg", "-y",
    "-ss", spec["start"], "-to", spec["to"], "-i", VIDEO_SOURCE,
    "-ss", spec["start"], "-to", spec["to"], "-i", AUDIO_SOURCE,
    "-i", music_file,
    "-filter_complex", filter_complex,
    "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "60",
    "-c:a", "aac", "-b:a", "192000",
    output_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return Code:", res.returncode)
if res.returncode == 0 and os.path.exists(output_path):
    print(f"SUCCESS! Output size: {os.path.getsize(output_path)/(1024*1024):.2f} MB")
else:
    print("Error:", res.stderr[-600:])
