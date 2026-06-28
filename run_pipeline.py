import os
import sys
import time
import subprocess
import psutil

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

print("====================================================")
print("KINESIO Pipeline Manager (v4 Shorts Queue)")
print("====================================================")

while True:
    active = False
    for p in psutil.process_iter():
        try:
            cmd = p.cmdline()
            # Ignore our own inspection and look for compile_new_videos.py
            if any('compile_new_videos.py' in arg for arg in cmd) and p.pid != os.getpid():
                active = True
                break
        except:
            pass
    if not active:
        print("\n[INFO] compile_new_videos.py is no longer active. Starting compile_shorts_v4.py...")
        break
    print("[INFO] compile_new_videos.py is still running. Waiting 60 seconds...")
    time.sleep(60)

# Run compile_shorts_v4.py
cmd_shorts = ["python", "compile_shorts_v4.py"]
try:
    subprocess.run(cmd_shorts, check=True)
    print("\n[SUCCESS] compile_shorts_v4.py finished successfully!")
except Exception as e:
    print(f"\n[ERROR] Failed to run compile_shorts_v4.py: {e}")
