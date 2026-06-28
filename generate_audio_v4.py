import os
import sys
import asyncio
import re
import subprocess

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"

SCRIPT_SHORTS_V4 = os.path.join(BASE_DIR, "scripts_shorts_v4.md")

SHORTS_V4_AUDIO_MAPPING = {
    "cossacks3": os.path.join(BASE_DIR, "audio_cossacks3.mp3"),
    "aoh3": os.path.join(BASE_DIR, "audio_aoh3.mp3"),
    "diplomacy_v4": os.path.join(BASE_DIR, "audio_diplomacy_v4.mp3"),
    "anno1404": os.path.join(BASE_DIR, "audio_anno1404.mp3"),
    "planetary": os.path.join(BASE_DIR, "audio_planetary.mp3")
}

def extract_v4_locution(file_path, key_token):
    """Extracts the voiceover locution text for a specific Short in v4 script."""
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    sections = content.split("## 📱 Short ")
    target_section = None
    for sec in sections:
        first_line = sec.strip().split('\n')[0].strip()
        # Map tokens to find the matching section
        if key_token == "cossacks3" and "cossacks 3" in first_line.lower():
            target_section = sec
            break
        elif key_token == "aoh3" and "age of history 3" in first_line.lower():
            target_section = sec
            break
        elif key_token == "diplomacy_v4" and "diplomacy is not an option" in first_line.lower():
            target_section = sec
            break
        elif key_token == "anno1404" and "anno 1404" in first_line.lower():
            target_section = sec
            break
        elif key_token == "planetary" and "planetary annihilation" in first_line.lower():
            target_section = sec
            break
            
    if not target_section:
        return ""
        
    locution_parts = []
    lines = target_section.split('\n')
    for i, line in enumerate(lines):
        if "Locución" in line or "Voz en off" in line:
            # Match quotes (supporting multiline quotes)
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
    print("TTS Voice Generator for Shorts v4")
    print("====================================================")
    
    tasks = []
    
    for key, path in SHORTS_V4_AUDIO_MAPPING.items():
        print(f"Extracting Short '{key}' locution...")
        short_text = extract_v4_locution(SCRIPT_SHORTS_V4, key)
        print(f"  Word count for '{key}': {len(short_text.split())} words")
        if short_text:
            # These are 1:00 to 1:30 min long-form shorts, so speed rate of +20% (instead of rushed +28%) is ideal for better readability and a premium natural tone!
            tasks.append(generate_tts(short_text, path, 20)) 
            
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
