import os
import sys
import re
import asyncio
import edge_tts

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCRIPT_FILE = os.path.join(BASE_DIR, "scripts_spain_campaign.md")

def clean_text(text):
    # Remove surrounding quotes if present
    text = text.strip()
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1].strip()
    return text

def parse_scripts(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] Script file not found: {file_path}")
        return {}, {}
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Parse Widescreen Essays
    essays = {}
    
    # Essay 1
    essay1_parts = content.split('### 📽️ Ensayo 1: La Segunda Estrella: Cómo España conquistó el Mundial de 2026')
    if len(essay1_parts) >= 2:
        essay1_block = essay1_parts[1].split('### 📽️ Ensayo 2:')[0]
        # Find all Audio (Voz en off) matches
        matches = re.findall(r'\*\s+\*\*Audio \(Voz en off\):\*\*\s*\n\s*"([^"]+)"', essay1_block)
        if not matches:
            # Fallback line by line parsing
            matches = []
            lines = essay1_block.split('\n')
            for i, line in enumerate(lines):
                if "Audio (Voz en off)" in line:
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip()
                        if next_line.startswith('"') and next_line.endswith('"'):
                            matches.append(clean_text(next_line))
                            break
        essays["spain_essay_1"] = " ".join(matches)
        
    # Essay 2
    essay2_parts = content.split('### 📽️ Ensayo 2: El Último Baile de Messi y la Pizarra Táctica de la Final')
    if len(essay2_parts) >= 2:
        essay2_block = essay2_parts[1].split('## 📱 PARTE 2:')[0]
        matches = re.findall(r'\*\s+\*\*Audio \(Voz en off\):\*\*\s*\n\s*"([^"]+)"', essay2_block)
        if not matches:
            matches = []
            lines = essay2_block.split('\n')
            for i, line in enumerate(lines):
                if "Audio (Voz en off)" in line:
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip()
                        if next_line.startswith('"') and next_line.endswith('"'):
                            matches.append(clean_text(next_line))
                            break
        essays["spain_essay_2"] = " ".join(matches)

    # 2. Parse 18 Shorts
    shorts = {}
    shorts_parts = content.split('## 📱 PARTE 2: GUIONES DE SHORTS VERTICALES (9:16)')
    if len(shorts_parts) >= 2:
        shorts_block = shorts_parts[1]
        for idx in range(1, 19):
            sh_key = f"### 📱 Short {idx}:"
            if sh_key in shorts_block:
                sh_part = shorts_block.split(sh_key)[1]
                if idx < 18:
                    sh_part = sh_part.split(f"### 📱 Short {idx+1}:")[0]
                else:
                    # End of file
                    pass
                
                # Extract Audio line
                lines = sh_part.split('\n')
                for i, line in enumerate(lines):
                    if "Audio (Voz en off)" in line:
                        for j in range(i+1, min(i+5, len(lines))):
                            next_line = lines[j].strip()
                            if next_line.startswith('"') and next_line.endswith('"'):
                                shorts[f"spain_short_{idx}"] = clean_text(next_line)
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
    print("TTS Voice Generator for Spain World Cup Campaign")
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
    
    print("Running neural voice synthesis for 20 items asynchronously...")
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
