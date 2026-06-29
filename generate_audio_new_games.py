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
SCRIPT_GATES_OF_HELL = os.path.join(BASE_DIR, "script_gates_of_hell.md")
SCRIPT_CHAOSBANE = os.path.join(BASE_DIR, "script_chaosbane.md")

# Output files
AUDIO_GATES_OF_HELL = os.path.join(BASE_DIR, "audio_gates_of_hell.mp3")
AUDIO_CHAOSBANE = os.path.join(BASE_DIR, "audio_chaosbane.mp3")

def extract_long_locution(file_path):
    """Extracts all locution text from the horizontal video scripts robustly."""
    locution_parts = []
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if "Audio (Voz en off)" in line:
            # Search next lines for double quotes (supporting multiline quotes)
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
    print("TTS Voice Generator for Gates of Hell & Chaosbane")
    print("====================================================")
    
    tasks = []
    
    # 1. Gates of Hell
    print("Extracting Gates of Hell locution...")
    text_goh = extract_long_locution(SCRIPT_GATES_OF_HELL)
    print(f"  Gates of Hell word count: {len(text_goh.split())} words")
    if text_goh:
        tasks.append(generate_tts(text_goh, AUDIO_GATES_OF_HELL, 0)) # +0%
        
    # 2. Chaosbane
    print("Extracting Chaosbane locution...")
    text_cb = extract_long_locution(SCRIPT_CHAOSBANE)
    print(f"  Chaosbane word count: {len(text_cb.split())} words")
    if text_cb:
        tasks.append(generate_tts(text_cb, AUDIO_CHAOSBANE, 0)) # +0%
        
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
