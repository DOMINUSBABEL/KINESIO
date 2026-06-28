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
SCRIPT_DUNE = os.path.join(BASE_DIR, "script_dune.md")
SCRIPT_PATHFINDER = os.path.join(BASE_DIR, "script_pathfinder.md")
SCRIPT_SHORTS = os.path.join(BASE_DIR, "scripts_shorts_v3.md")

# Output files
AUDIO_DUNE = os.path.join(BASE_DIR, "audio_dune.mp3")
AUDIO_PATHFINDER = os.path.join(BASE_DIR, "audio_pathfinder.mp3")

SHORTS_AUDIO_MAPPING = {
    "jc2": (os.path.join(BASE_DIR, "audio_jc2.mp3"), "Just Cause 2"),
    "jc3": (os.path.join(BASE_DIR, "audio_jc3.mp3"), "Just Cause 3"),
    "aoe2": (os.path.join(BASE_DIR, "audio_aoe2.mp3"), "Age of Empires II: Definitive Edition"),
    "warband": (os.path.join(BASE_DIR, "audio_warband.mp3"), "Mount & Blade: Warband"),
    "diplomacy": (os.path.join(BASE_DIR, "audio_diplomacy.mp3"), "Diplomacy is Not an Option"),
    "syx": (os.path.join(BASE_DIR, "audio_syx.mp3"), "Songs of Syx"),
    "rimworld": (os.path.join(BASE_DIR, "audio_rimworld.mp3"), "RimWorld")
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

def extract_short_locution(file_path, title_token):
    """Extracts all Audio locutions for a specific Short in the v3 script robustly."""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    sections = content.split("## 📱 Short ")
    target_section = None
    for sec in sections:
        # Check if the title matches
        first_line = sec.strip().split('\n')[0].strip()
        if title_token.lower() in first_line.lower():
            target_section = sec
            break
            
    if not target_section:
        return ""
        
    locution_parts = []
    lines = target_section.split('\n')
    for i, line in enumerate(lines):
        if "Locución" in line:
            # Check if quote is on the same line or next line
            combined = " ".join(lines[i:i+3])
            match = re.search(r'\"([^\"]+)\"', combined)
            if match:
                locution_parts.append(match.group(1).strip())
                
    return " ".join(locution_parts)

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
    print("TTS Voice Generator v3 (KINESIO Multiformat)")
    print("====================================================")
    
    tasks = []
    
    # 1. Long-form Dune: Spice Wars
    print("Extracting Dune: Spice Wars locution...")
    text_dune = extract_long_locution(SCRIPT_DUNE)
    print(f"  Dune word count: {len(text_dune.split())} words")
    if text_dune:
        tasks.append(generate_tts(text_dune, AUDIO_DUNE, 5)) # +5%
        
    # 2. Long-form Pathfinder
    print("Extracting Pathfinder: Wrath of the Righteous locution...")
    text_pathfinder = extract_long_locution(SCRIPT_PATHFINDER)
    print(f"  Pathfinder word count: {len(text_pathfinder.split())} words")
    if text_pathfinder:
        tasks.append(generate_tts(text_pathfinder, AUDIO_PATHFINDER, 5)) # +5%
        
    # 3. The 7 Shorts
    for key, (path, title) in SHORTS_AUDIO_MAPPING.items():
        print(f"Extracting Short '{title}' locution...")
        short_text = extract_short_locution(SCRIPT_SHORTS, title)
        print(f"  Short '{key}' word count: {len(short_text.split())} words")
        if short_text:
            tasks.append(generate_tts(short_text, path, 28)) # +28%
            
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
