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
SCRIPT_FILE = os.path.join(BASE_DIR, "script_sony_essay.md")
AUDIO_OUTPUT = os.path.join(BASE_DIR, "audio_sony_essay.mp3")

def extract_locution(file_path):
    locution_parts = []
    if not os.path.exists(file_path):
        return ""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for i, line in enumerate(lines):
        if "Audio (Voz en off)" in line:
            for j in range(i+1, min(i+5, len(lines))):
                next_line = lines[j].strip()
                if next_line.startswith('"') and next_line.endswith('"'):
                    locution_parts.append(next_line[1:-1].strip())
                    break
    return " ".join(locution_parts)

def text_to_ssml(text, voice="es-MX-JorgeNeural", rate="+0%"):
    # Clean special XML characters
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # Introduce natural pauses (breath breaks) at punctuation marks
    text = re.sub(r'(?<!\d)\.(?=\s|$)', '. <break time="450ms"/>', text)
    text = re.sub(r',(?=\s|$)', ', <break time="200ms"/>', text)
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

async def generate_ssml_audio():
    print("====================================================")
    print("SSML TTS Voice Generator for Sony Video Essay")
    print("====================================================")
    
    print("Extracting Sony locution...")
    text_long = extract_locution(SCRIPT_FILE)
    words = text_long.split()
    print(f"  Raw word count: {len(words)} words")
    
    if not text_long:
        print("[ERROR] No locution text extracted. Verify script file exists.")
        sys.exit(1)
        
    print("Converting text to SSML with natural punctuation breaks...")
    ssml = text_to_ssml(text_long, voice="es-MX-JorgeNeural", rate="+0%")
    
    print("\nSynthesizing voiceover via Microsoft Edge neural engine...")
    try:
        communicate = edge_tts.Communicate(ssml)
        await communicate.save(AUDIO_OUTPUT)
        
        if os.path.exists(AUDIO_OUTPUT) and os.path.getsize(AUDIO_OUTPUT) > 0:
            print(f"  [SUCCESS] Saved premium SSML voiceover to {AUDIO_OUTPUT}")
            return True
        else:
            print("  [FAILED] Voiceover file was empty or not saved.")
            return False
    except Exception as e:
        print(f"  [ERROR] Synthesis failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(generate_ssml_audio())
