import os
import subprocess

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
MUSIC_DIR = os.path.join(PROJECT_DIR, "music")
VIDEO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_720p.mp4")

spec = {
    "id": 3,
    "category": "Explosions & Tanks",
    "title_en": "Hidden in the Bush at 10 Meters: The Ultimate Anti-Tank Trap 🚜 #shorts",
    "banner": "10m ANTI-TANK AMBUSH TRAP",
    "music": "Volatile Reaction.mp3",
    "clips": [("00:06:22", "00:06:31"), ("00:06:33", "00:06:41"), ("00:06:42", "00:06:50")]
}

banner_clean = spec['banner'].replace(":", "\\:").replace("'", "")
video_filter = (
    "scale=1080:1920:force_original_aspect_ratio=increase,"
    "crop=1080:1920,"
    "eq=contrast=1.12:brightness=0.02:saturation=1.2,"
    "unsharp=5:5:0.8:5:5:0.0,"
    f"drawtext=text='{banner_clean}':fontcolor=yellow:fontsize=40:x=(w-text_w)/2:y=180:box=1:boxcolor=black@0.7:boxborderw=12"
)

temp_clips = []
for idx, (start_t, end_t) in enumerate(spec["clips"]):
    clip_path = os.path.join(PROJECT_DIR, f"temp_clip_fix_{idx}.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-ss", start_t,
        "-i", VIDEO_SOURCE,
        "-to", end_t,
        "-vf", video_filter,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "60",
        "-c:a", "aac", "-b:a", "192000",
        clip_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Clip {idx} return code:", res.returncode)
    if res.returncode == 0 and os.path.exists(clip_path) and os.path.getsize(clip_path) > 0:
        temp_clips.append(clip_path)
    else:
        print("Error in clip:", res.stderr[-400:])

print(f"Successfully generated {len(temp_clips)} clips!")

concat_file = os.path.join(PROJECT_DIR, "concat_fix.txt")
with open(concat_file, "w", encoding="utf-8") as f:
    for c in temp_clips:
        f.write(f"file '{c.replace(os.sep, '/')}'\n")

merged_raw = os.path.join(PROJECT_DIR, "merged_fix_raw.mp4")
cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_file, "-c", "copy", merged_raw]
res_concat = subprocess.run(cmd_concat, capture_output=True, text=True)
print("Concat code:", res_concat.returncode)
if os.path.exists(merged_raw):
    print("Merged raw size:", os.path.getsize(merged_raw))

music_file = os.path.join(MUSIC_DIR, spec['music'])
output_path = os.path.join(PROJECT_DIR, "gates_of_hell_short_3_final.mp4")
audio_filter = "[0:a]volume=1.0[a1];[1:a]volume=0.07[a2];[a1][a2]amix=inputs=2:duration=first[a]"

cmd_final = [
    "ffmpeg", "-y",
    "-i", merged_raw,
    "-i", music_file,
    "-filter_complex", audio_filter,
    "-map", "0:v",
    "-map", "[a]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192000",
    "-shortest", output_path
]
res_final = subprocess.run(cmd_final, capture_output=True, text=True)
print("Final render code:", res_final.returncode)
if res_final.returncode == 0 and os.path.exists(output_path):
    print(f"SUCCESS! Output short generated ({os.path.getsize(output_path)/(1024*1024):.2f} MB)")
else:
    print("Final error:", res_final.stderr[-400:])
