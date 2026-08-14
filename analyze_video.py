import subprocess
import os

video_path = r"C:\Users\jegom\shorts_project\gameplay_lowres.mp4"
output_dir = r"C:\Users\jegom\shorts_project\frames_analysis"

os.makedirs(output_dir, exist_ok=True)

if os.path.exists(video_path):
    print("Video file found. Extracting frames every 60 seconds...")
    # Extract 1 frame every 60 seconds
    cmd = [
        "ffmpeg", "-y", "-i", video_path,
        "-vf", "fps=1/60,scale=320:-1",
        os.path.join(output_dir, "frame_%03d.jpg")
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Frames extracted:", len(os.listdir(output_dir)))
else:
    print("Video file not ready yet.")
