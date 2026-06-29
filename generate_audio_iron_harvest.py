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
SCRIPT_IRON_HARVEST = os.path.join(BASE_DIR, "script_iron_harvest.md")

# Output files
AUDIO_IRON_HARVEST = os.path.join(BASE_DIR, "audio_iron_harvest.mp3")

def extract_long_locution(file_path):
    """Extracts all locution text from the horizontal video scripts robustly."""
    locution_parts = []
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if "Audio (Voz en off)" in line:
            quoted_text = []
            quote_started = False
            for j in range(i+1, min(i+15, len(lines))):
                next_line = lines[j].strip()
                if not quote_started:
                    if next_line.startswith('"'):
                        quote_started = True
                        if next_line.endswith('"') and len(next_line) > 1:
                            quoted_text.append(next_line[1:-1].strip())
                            break
                        else:
                            quoted_text.append(next_line[1:].strip())
                else:
                    if next_line.endswith('"'):
                        quoted_text.append(next_line[:-1].strip())
                        break
                    else:
                        quoted_text.append(next_line)
            if quoted_text:
                locution_parts.append(" ".join(quoted_text).strip())
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
    print("TTS Voice Generator for Iron Harvest")
    print("====================================================")
    
    print("Extracting Iron Harvest locution...")
    text_ih = extract_long_locution(SCRIPT_IRON_HARVEST)
    print(f"  Iron Harvest word count: {len(text_ih.split())} words")
    
    if text_ih:
        success = await generate_tts(text_ih, AUDIO_IRON_HARVEST, 0) # +0%
        if success:
            print("[INFO] Audio generated successfully!")
        else:
            print("[ERROR] Failed to generate audio!")
    else:
        print("[WARNING] No locution text extracted. Verify script files are present.")

if __name__ == "__main__":
    asyncio.run(main())
