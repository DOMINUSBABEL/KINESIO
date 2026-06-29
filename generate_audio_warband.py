import os
import sys
import asyncio
import re
import subprocess

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"

# Input files
SCRIPT_LONG = os.path.join(BASE_DIR, "script_warband_long.md")
SCRIPT_SHORTS = os.path.join(BASE_DIR, "scripts_shorts_warband_curiosities.md")

# Output files
AUDIO_LONG = os.path.join(BASE_DIR, "audio_warband_long.mp3")

SHORTS_KEYS = ["warband_short_1", "warband_short_2", "warband_short_3", "warband_short_4", "warband_short_5"]

def extract_long_locution(file_path):
    """Extracts all locution text from the horizontal video scripts robustly."""
    locution_parts = []
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if "Audio (Voz en off)" in line:
            # Search next lines for double quotes
            for j in range(i+1, min(i+5, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('"') and next_line.endswith('"'):
                    locution_parts.append(next_line[1:-1].strip())
                    break
    return " ".join(locution_parts)

def extract_short_text(file_path, key):
    """Extracts the paragraph text for a short key from the curiosities markdown file."""
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

async def generate_tts(text, output_path, rate_pct):
    """Invokes edge-tts command line to generate audio track."""
    rate_str = f"+{rate_pct}%" if rate_pct >= 0 else f"{rate_pct}%"
    cmd = [
        "edge-tts",
        "--voice", "es-MX-JorgeNeural",
        "--rate", rate_str,
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
        print(f"  [ERROR] Executing edge-tts failed for {os.path.basename(output_path)}: {e}")
        return False

async def main():
    print("====================================================")
    print("TTS Voice Generator for Mount & Blade: Warband")
    print("====================================================")
    
    tasks = []
    
    # 1. Long horizontal video (0% rate for natural 9-11 min pacing)
    print("Extracting Mount & Blade: Warband long locution...")
    text_long = extract_long_locution(SCRIPT_LONG)
    print(f"  Long word count: {len(text_long.split())} words")
    if text_long:
        tasks.append(generate_tts(text_long, AUDIO_LONG, 0)) # +0%
        
    # 2. The 5 Shorts (0% rate to make them between 45 and 70 seconds)
    # A word count of ~145 words at +0% (150 WPM) takes around 58 seconds, which is perfect!
    for key in SHORTS_KEYS:
        print(f"Extracting Short '{key}' locution...")
        short_text = extract_short_text(SCRIPT_SHORTS, key)
        print(f"  Short '{key}' word count: {len(short_text.split())} words")
        if short_text:
            output_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
            tasks.append(generate_tts(short_text, output_path, 0)) # +0%
            
    if not tasks:
        print("[WARNING] No locution text extracted. Verify script files are present.")
        return
        
    print("\nRunning neural synthesis asynchronously...")
    results = await asyncio.gather(*tasks)
    
    successful = sum(1 for r in results if r)
    print(f"\n====================================================")
    print(f"TTS Generation Complete: {successful}/{len(tasks)} files generated successfully")
    print("====================================================")

if __name__ == "__main__":
    asyncio.run(main())
