import subprocess
import os

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
VIDEO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_720p.mp4")

banner = "AMMO RACK BLAST: TURRET FLIES 100m"
# Escape colons and single quotes for FFmpeg drawtext
banner_clean = banner.replace(":", "\\:").replace("'", "")

video_filter = (
    "scale=1080:1920:force_original_aspect_ratio=increase,"
    "crop=1080:1920,"
    "eq=contrast=1.12:brightness=0.02:saturation=1.2,"
    "unsharp=5:5:0.8:5:5:0.0,"
    f"drawtext=text='{banner_clean}':fontcolor=yellow:fontsize=40:x=(w-text_w)/2:y=180:box=1:boxcolor=black@0.7:boxborderw=12"
)

cmd = [
    "ffmpeg", "-y",
    "-ss", "00:06:42", "-to", "00:06:51", "-i", VIDEO_SOURCE,
    "-vf", video_filter,
    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "60",
    "-c:a", "aac", "-b:a", "192000",
    "test_subclip.mp4"
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
print("STDERR tail:\n", res.stderr[-1000:])
