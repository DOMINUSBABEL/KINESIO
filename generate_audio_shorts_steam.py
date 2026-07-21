import os
import sys
import asyncio
import re
import subprocess

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

try:
    import edge_tts
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
    import edge_tts

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCRIPT_FILE = os.path.join(BASE_DIR, "scripts_shorts_steam.md")
SHORTS_KEYS = [f"steam_short_{i}" for i in range(1, 7)]

def extract_short_text(file_path, key):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = content.split(f"## 📌 {key}:")
    if len(parts) < 2:
        return ""
        
    block = parts[1].strip()
    lines = block.split('\n')
    for i, line in enumerate(lines):
        if "Voz en off" in line:
            for j in range(i+1, min(i+5, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('"') and next_line.endswith('"'):
                    return next_line[1:-1].strip()
    return ""

def text_to_ssml(text, voice="es-MX-JorgeNeural", rate="+0%"):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r'(?<!\d)\.(?=\s|$)', '. <break time="450ms"/>', text)
    text = re.sub(r',(?=\s|$)', ', ', text) # Keep commas simple for Steam shorts
    text = re.sub(r':(?=\s|$)', ': <break time="350ms"/>', text)
    text = re.sub(r'\?(?=\s|$)', '? <break time="500ms"/>', text)
    text = re.sub(r'!(?=\s|$)', '! <break time="500ms"/>', text)
    
    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="es-MX">
  <voice name="{voice}">
    <prosody rate="{rate}">
      {text}
    </prosody>
  </voice>
</speak>"""
    return ssml

async def generate_short_tts(key, text):
    output_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
    ssml = text_to_ssml(text)
    
    try:
        communicate = edge_tts.Communicate(ssml)
        await communicate.save(output_path)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Generated TTS for {key} -> audio_{key}.mp3")
            return True
        else:
            print(f"  [FAILED] Failed saving TTS for {key}")
            return False
    except Exception as e:
        print(f"  [ERROR] TTS generation for {key} failed: {e}")
        return False

async def main():
    print("====================================================")
    print("TTS Voice Generator for Steam Shorts")
    print("====================================================")
    
    tasks = []
    for key in SHORTS_KEYS:
        text = extract_short_text(SCRIPT_FILE, key)
        words = text.split()
        print(f"Extracting Short '{key}': {len(words)} words")
        if text:
            tasks.append(generate_short_tts(key, text))
            
    if not tasks:
        print("[ERROR] No short scripts extracted. Check scripts file format.")
        sys.exit(1)
        
    print("\nRunning neural voice synthesis asynchronously...")
    results = await asyncio.gather(*tasks)
    
    successful = sum(1 for r in results if r)
    print(f"\n====================================================")
    print(f"Shorts TTS Generation Complete: {successful}/{len(tasks)} files successfully generated")
    print("====================================================")

if __name__ == "__main__":
    asyncio.run(main())
