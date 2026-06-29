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
SCRIPT_PLANETARY = os.path.join(BASE_DIR, "script_planetary.md")
SCRIPT_RIFTBREAKER = os.path.join(BASE_DIR, "script_riftbreaker.md")
SCRIPT_WEWHOARE = os.path.join(BASE_DIR, "script_wewhoare.md")
SCRIPT_SHORTS = os.path.join(BASE_DIR, "scripts_shorts_campaign_4.md")

# Output files for horizontal videos
AUDIO_PLANETARY = os.path.join(BASE_DIR, "audio_planetary.mp3")
AUDIO_RIFTBREAKER = os.path.join(BASE_DIR, "audio_riftbreaker.mp3")
AUDIO_WEWHOARE = os.path.join(BASE_DIR, "audio_wewhoare.mp3")

# Shorts mappings
SHORTS_MAPPING = {
    "planetary_short_1": os.path.join(BASE_DIR, "audio_planetary_short_1.mp3"),
    "planetary_short_2": os.path.join(BASE_DIR, "audio_planetary_short_2.mp3"),
    "planetary_short_3": os.path.join(BASE_DIR, "audio_planetary_short_3.mp3"),
    "riftbreaker_short_1": os.path.join(BASE_DIR, "audio_riftbreaker_short_1.mp3"),
    "riftbreaker_short_2": os.path.join(BASE_DIR, "audio_riftbreaker_short_2.mp3"),
    "riftbreaker_short_3": os.path.join(BASE_DIR, "audio_riftbreaker_short_3.mp3"),
    "wewhoare_short_1": os.path.join(BASE_DIR, "audio_wewhoare_short_1.mp3"),
    "wewhoare_short_2": os.path.join(BASE_DIR, "audio_wewhoare_short_2.mp3"),
    "wewhoare_short_3": os.path.join(BASE_DIR, "audio_wewhoare_short_3.mp3"),
}

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

def extract_short_locution_v4(file_path, key_token):
    """Extracts all Audio locutions for a specific Short in the v4 script robustly using regex."""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    pattern = r"Key:\s*" + re.escape(key_token)
    parts = re.split(pattern, content)
    if len(parts) < 2:
        return ""
    
    block = parts[1]
    match = re.search(r'\"([^\"]{30,})\"', block)
    if match:
        return match.group(1).strip().replace('\n', ' ')
    return ""

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
    print("TTS Voice Generator (Campaign 4 Multiformat)")
    print("====================================================")
    
    tasks = []
    
    # 1. Horizontal Videos (rate = +0% for natural pacing and >10 min duration)
    horizontal_scripts = [
        (SCRIPT_PLANETARY, AUDIO_PLANETARY, "Planetary Annihilation"),
        (SCRIPT_RIFTBREAKER, AUDIO_RIFTBREAKER, "The Riftbreaker"),
        (SCRIPT_WEWHOARE, AUDIO_WEWHOARE, "We Who Are About To Die")
    ]
    
    for script_path, audio_path, name in horizontal_scripts:
        print(f"Extracting {name} locution...")
        text = extract_long_locution(script_path)
        print(f"  {name} word count: {len(text.split())} words")
        if text:
            tasks.append(generate_tts(text, audio_path, 0)) # +0% normal speed
            
    # 2. Shorts (rate = +0% or slightly faster if needed, we'll keep at +0% to make them pacing 45-70s)
    # At 150-180 words, +0% speed rate is perfect to get exactly 50-70 seconds.
    for key, path in SHORTS_MAPPING.items():
        print(f"Extracting Short '{key}' locution...")
        short_text = extract_short_locution_v4(SCRIPT_SHORTS, key)
        print(f"  Short '{key}' word count: {len(short_text.split())} words")
        if short_text:
            tasks.append(generate_tts(short_text, path, 0)) # +0% normal speed
            
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
