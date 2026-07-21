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
SCRIPT_FILE = os.path.join(BASE_DIR, "scripts_siberia_campaign.md")

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

    # 1. Parse Video Essays
    essays = {}
    
    # Extract Essay 1
    essay1_parts = content.split('### 📽️ Video Essay 1: "La Subasta de Siberia: ¿Cuánto vale un soldado en Rusia?"')
    if len(essay1_parts) >= 2:
        # Get everything up to the start of Essay 2
        essay1_block = essay1_parts[1].split('### 📽️ Video Essay 2:')[0]
        # Find all Audio blocks
        matches = re.findall(r'\*\s+\*\*Audio \(Voz en off\):\*\*\s*\n\s*"([^"]+)"', essay1_block)
        if not matches:
            # Try parsing line-by-line
            matches = []
            lines = essay1_block.split('\n')
            for i, line in enumerate(lines):
                if "Audio (Voz en off)" in line:
                    for j in range(i+1, min(i+5, len(lines))):
                        next_line = lines[j].strip()
                        if next_line.startswith('"') and next_line.endswith('"'):
                            matches.append(clean_text(next_line))
                            break
        essays["siberia_essay_1"] = " ".join(matches)

    # Extract Essay 2
    essay2_parts = content.split('### 📽️ Video Essay 2: "El Negocio de la Muerte: Los \'Grobovye\' en la Rusia Rural"')
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
        essays["siberia_essay_2"] = " ".join(matches)

    # 2. Parse 15 Shorts
    shorts = {}
    shorts_parts = content.split('## 📱 PARTE 2: GUIONES DE SHORTS VERTICALES (9:16)')
    if len(shorts_parts) >= 2:
        shorts_block = shorts_parts[1]
        # Split by ### 📱 Short X:
        for idx in range(1, 16):
            sh_key = f"### 📱 Short {idx}:"
            if sh_key in shorts_block:
                sh_part = shorts_block.split(sh_key)[1]
                # End of this short is the next short or end of file
                if idx < 15:
                    sh_part = sh_part.split(f"### 📱 Short {idx+1}:")[0]
                else:
                    sh_part = sh_part.split('---')[0]
                
                # Extract Audio line
                lines = sh_part.split('\n')
                for i, line in enumerate(lines):
                    if "Audio (Voz en off)" in line:
                        for j in range(i+1, min(i+5, len(lines))):
                            next_line = lines[j].strip()
                            if next_line.startswith('"') and next_line.endswith('"'):
                                shorts[f"siberia_short_{idx}"] = clean_text(next_line)
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
    print("TTS Voice Generator for Siberia Campaign")
    print("====================================================")
    
    essays, shorts = parse_scripts(SCRIPT_FILE)
    
    tasks = []
    print("\n--- EXTRACTED ESSAYS ---")
    for key, text in essays.items():
        words = len(text.split())
        print(f"Essay '{key}': {words} words")
        if text:
            tasks.append(generate_tts(key, text))
            
    print("\n--- EXTRACTED SHORTS ---")
    for key, text in shorts.items():
        words = len(text.split())
        print(f"Short '{key}': {words} words")
        if text:
            tasks.append(generate_tts(key, text))
            
    if not tasks:
        print("[ERROR] No scripts could be extracted. Check script markdown formatting.")
        sys.exit(1)
        
    print(f"\nRunning neural voice synthesis for {len(tasks)} items asynchronously...")
    results = await asyncio.gather(*tasks)
    
    successful = sum(1 for r in results if r)
    print(f"\nCompleted! {successful}/{len(tasks)} audios generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
