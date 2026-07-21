import os
import sys
import re
import asyncio
import edge_tts

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCRIPT_FILE = os.path.join(BASE_DIR, "scripts_tesla_campaign.md")

def clean_text(text):
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    # Strip any hashtags from TTS text strictly
    text = re.sub(r'#\w+', '', text).strip()
    return text

def parse_scripts(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] Script file not found: {file_path}")
        return {}, {}
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Parse Widescreen Essay 1
    essays = {}
    essay_parts = content.split('### 📽️ Ensayo 1: Warp Drive: La Apuesta Imposible de Tesla que Humilló a la Industria del Software')
    if len(essay_parts) >= 2:
        essay_block = essay_parts[1].split('## 🎥 PARTE 2:')[0]
        chapters = essay_block.split('#### Capítulo ')
        chapter_audios = []
        for ch in chapters[1:]:
            lines = ch.split('\n')
            for i, line in enumerate(lines):
                if "Audio (Voz en off):" in line:
                    audio_text = ""
                    for j in range(i+1, len(lines)):
                        l_str = lines[j].strip()
                        if l_str.startswith('"'):
                            audio_text += l_str.lstrip('"') + " "
                            if l_str.endswith('"') and len(l_str) > 1:
                                audio_text = audio_text.rstrip('" ')
                                break
                        elif audio_text:
                            audio_text += l_str + " "
                            if l_str.endswith('"'):
                                audio_text = audio_text.rstrip('" ')
                                break
                    if audio_text:
                        chapter_audios.append(clean_text(audio_text))
                        break
        essays["tesla_essay_1"] = " ".join(chapter_audios)
        
    # 2. Parse 6 Shorts
    shorts = {}
    shorts_parts = content.split('## 🎥 PARTE 2: GUIONES DE SHORTS VERTICALES (9:16)')
    if len(shorts_parts) >= 2:
        shorts_block = shorts_parts[1]
        for idx in range(1, 7):
            sh_key = f"### 📱 Short {idx}:"
            if sh_key in shorts_block:
                sh_part = shorts_block.split(sh_key)[1]
                if idx < 6:
                    sh_part = sh_part.split(f"### 📱 Short {idx+1}:")[0]
                
                lines = sh_part.split('\n')
                for i, line in enumerate(lines):
                    if "Audio (Voz en off)" in line:
                        for j in range(i+1, min(i+5, len(lines))):
                            next_line = lines[j].strip()
                            if next_line.startswith('"') and next_line.endswith('"'):
                                cleaned = clean_text(next_line)
                                shorts[f"tesla_short_{idx}"] = cleaned
                                break
                                
    return essays, shorts

async def generate_tts(key, text):
    output_path = os.path.join(BASE_DIR, f"audio_{key}.mp3")
    
    try:
        communicate = edge_tts.Communicate(text, voice="es-MX-JorgeNeural")
        await communicate.save(output_path)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print(f"  [SUCCESS] Generated TTS for {key} -> audio_{key}.mp3 ({len(text.split())} words)")
            return True
        else:
            print(f"  [FAILED] Failed saving TTS for {key}")
            return False
    except Exception as e:
        print(f"  [ERROR] TTS generation for {key} failed: {e}")
        return False

async def main():
    print("====================================================")
    print("TTS Voice Generator for Tesla SAP Campaign")
    print("====================================================\n")
    
    essays, shorts = parse_scripts(SCRIPT_FILE)
    
    print("--- EXTRACTED ESSAYS ---")
    for k, v in essays.items():
        print(f"Essay '{k}': {len(v.split())} words")
    print()
    
    print("--- EXTRACTED SHORTS ---")
    for k, v in shorts.items():
        print(f"Short '{k}': {len(v.split())} words")
    print()
    
    print("Running neural voice synthesis for 7 items asynchronously...")
    tasks = []
    for k, text in essays.items():
        tasks.append(generate_tts(k, text))
    for k, text in shorts.items():
        tasks.append(generate_tts(k, text))
        
    results = await asyncio.gather(*tasks)
    success_count = sum(1 for r in results if r)
    
    print(f"\nCompleted! {success_count}/{len(tasks)} audios generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
