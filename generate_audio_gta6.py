import os
import sys
import asyncio
import subprocess

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCRIPT_FILE = os.path.join(BASE_DIR, "scripts_shorts_gta6.md")

SHORTS_KEYS = ["gta6_short_1", "gta6_short_2", "gta6_short_3", "gta6_short_4", "gta6_short_5"]

def extract_short_text(file_path, key):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = content.split(f"### {key}")
    if len(parts) < 2:
        return ""
        
    block = parts[1].strip()
    subparts = block.split("---")
    return subparts[0].strip()

async def generate_tts(text, output_path):
    cmd = [
        "edge-tts",
        "--voice", "es-MX-JorgeNeural",
        "--rate", "+0%",
        "--text", text,
        "--write-media", output_path
    ]
    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Saved TTS: {os.path.basename(output_path)}")
            return True
        else:
            print(f"  [FAILED] Failed TTS for {os.path.basename(output_path)}: {stderr.decode('utf-8').strip()}")
            return False
    except Exception as e:
        print(f"  [ERROR] edge-tts execution failed for {os.path.basename(output_path)}: {e}")
        return False

async def main():
    print("====================================================")
    print("GTA VI Shorts TTS Voice Generator")
    print("====================================================")
    
    tasks = []
    for key in SHORTS_KEYS:
        print(f"Extracting GTA VI Short '{key}' text...")
        text = extract_short_text(SCRIPT_FILE, key)
        print(f"  Word count: {len(text.split())} words")
        if text:
            output_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
            tasks.append(generate_tts(text, output_path))
            
    if not tasks:
        print("[WARNING] No text extracted. Verify scripts_shorts_gta6.md path.")
        return
        
    print("\nSynthesizing neural audio files...")
    results = await asyncio.gather(*tasks)
    successful = sum(1 for r in results if r)
    print(f"\nTTS Generation Complete: {successful}/{len(tasks)} files generated successfully")

if __name__ == "__main__":
    asyncio.run(main())
