import os
import subprocess

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
MUSIC_DIR = os.path.join(PROJECT_DIR, "music")

merged_raw = os.path.join(PROJECT_DIR, "merged_test_raw.mp4")
music_file = os.path.join(MUSIC_DIR, "Volatile Reaction.mp3")
output_path = os.path.join(PROJECT_DIR, "test_short_3_final.mp4")

audio_filter = "[0:a]volume=1.0[a1];[1:a]volume=0.07[a2];[a1][a2]amix=inputs=2:duration=first[a]"

cmd_final = [
    "ffmpeg", "-y",
    "-i", merged_raw,
    "-i", music_file,
    "-filter_complex", audio_filter,
    "-map", "0:v:0",
    "-map", "[a]",
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "192000",
    "-shortest", output_path
]

res = subprocess.run(cmd_final, capture_output=True, text=True)
print("Final code with 0:v:0:", res.returncode)
if res.returncode != 0:
    print("Error:", res.stderr[-500:])
else:
    print("SUCCESS! Output size:", os.path.getsize(output_path))
