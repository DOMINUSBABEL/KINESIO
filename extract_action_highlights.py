import cv2
import numpy as np
import os
import json

video_path = r"C:\Users\jegom\shorts_project\gameplay_720p.mp4"
output_json = r"C:\Users\jegom\shorts_project\action_highlights.json"

def analyze_video_action():
    print(f"Opening video: {video_path}")
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return
        
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration_sec = total_frames / fps
    print(f"FPS: {fps}, Total Frames: {total_frames}, Duration: {duration_sec/60:.2f} minutes")
    
    # Sample every 15 frames (~0.25 seconds)
    sample_interval = int(fps * 0.25)
    
    prev_frame = None
    scores = []
    
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        if frame_idx % sample_interval == 0:
            gray = cv2.cvtColor(cv2.resize(frame, (320, 180)), cv2.COLOR_BGR2GRAY)
            if prev_frame is not None:
                # Frame difference as measure of motion/explosions
                diff = cv2.absdiff(gray, prev_frame)
                score = np.mean(diff) + np.std(diff) * 1.5
                timestamp = frame_idx / fps
                scores.append({
                    "timestamp": round(timestamp, 2),
                    "frame": frame_idx,
                    "score": round(score, 2),
                    "time_str": f"{int(timestamp//3600):02d}:{int((timestamp%3600)//60):02d}:{int(timestamp%60):02d}"
                })
            prev_frame = gray
            
        frame_idx += 1
        
    cap.release()
    
    # Sort by highest score
    scores.sort(key=lambda x: x["score"], reverse=True)
    
    # Filter out timestamps too close to each other (keep 5 sec minimum distance)
    filtered = []
    for s in scores:
        if not any(abs(s["timestamp"] - f["timestamp"]) < 5 for f in filtered):
            filtered.append(s)
            if len(filtered) >= 100:
                break
                
    filtered.sort(key=lambda x: x["timestamp"])
    
    print(f"Top {len(filtered)} action moments detected!")
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2)
        
    print(f"Saved analysis to {output_json}")

if __name__ == "__main__":
    analyze_video_action()
