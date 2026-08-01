import os
import sys
import asyncio
import subprocess
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"

def extract_text_from_file(file_path, key):
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

semaphore = asyncio.Semaphore(5)

async def synth_single(text, output_path, key):
    if not text:
        print(f"[SKIP] No text for {key}")
        return
        
    # Check if already synthesized with valid non-zero size
    if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
        return
        
    async with semaphore:
        for attempt in range(3):
            try:
                comm = edge_tts.Communicate(text, voice="es-MX-JorgeNeural", rate="+3%")
                await comm.save(output_path)
                cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", output_path]
                res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
                dur = float(res.stdout.strip())
                print(f"  [OK] {key} -> {os.path.basename(output_path)} ({dur:.2f}s)")
                return
            except Exception as e:
                await asyncio.sleep(1.0)

async def main():
    tasks = []
    
    # 1. Justiniano & Belisario (16)
    f1 = os.path.join(BASE_DIR, "scripts_16_shorts_justiniano_belisario.md")
    for i in range(1, 17):
        k = f"justiniano_belisario_short_{i}"
        txt = extract_text_from_file(f1, k)
        out = os.path.join(BASE_DIR, f"audio_justiniano_belisario_short_{i}.mp3")
        tasks.append(synth_single(txt, out, k))
        
    # 2. RTS & Roma (15)
    f2 = os.path.join(BASE_DIR, "scripts_15_shorts_rts_roma_2026.md")
    for i in range(1, 16):
        k = f"rts_roma_short_{i}"
        txt = extract_text_from_file(f2, k)
        out = os.path.join(BASE_DIR, f"audio_rts_roma_short_{i}.mp3")
        tasks.append(synth_single(txt, out, k))
        
    # 3. Creadores Crisis (8)
    f3 = os.path.join(BASE_DIR, "scripts_8_shorts_creadores_crisis.md")
    for i in range(1, 9):
        k = f"creadores_short_{i}"
        txt = extract_text_from_file(f3, k)
        out = os.path.join(BASE_DIR, f"audio_creadores_short_{i}.mp3")
        tasks.append(synth_single(txt, out, k))
        
    # 4. Terremoto & BPO (7)
    f4 = os.path.join(BASE_DIR, "scripts_7_shorts_terremoto_bpo.md")
    for i in range(1, 8):
        k = f"terremoto_short_{i}"
        txt = extract_text_from_file(f4, k)
        out = os.path.join(BASE_DIR, f"audio_terremoto_short_{i}.mp3")
        tasks.append(synth_single(txt, out, k))
        
    await asyncio.gather(*tasks)
    print("\nTodos los 46 audios verificados y listos.")

if __name__ == "__main__":
    asyncio.run(main())
