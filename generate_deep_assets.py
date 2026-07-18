import os
import re
import sys
import json
import asyncio
import subprocess
import edge_tts

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\reddit_deep_project"
scripts_path = os.path.join(PROJECT_DIR, "scripts_deep.md")
audio_dir = os.path.join(PROJECT_DIR, "audio")
manifest_path = os.path.join(PROJECT_DIR, "manifest.json")

os.makedirs(audio_dir, exist_ok=True)

def clean_text(text):
    # Remove markdown tags, bold, brackets (visual/sfx instructions)
    text = re.sub(r'\[.*?\]', '', text) # Remove [Visual: ...] or [SFX: ...]
    text = re.sub(r'\*\*.*?\*\*', '', text) # Remove bold descriptors
    text = text.replace('\n', ' ').strip()
    # Normalize spaces
    text = re.sub(r'\s+', ' ', text)
    return text

def parse_scripts():
    with open(scripts_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Parse Long Form Scripts
    long_form_matches = re.findall(r'## Guión (\d+): (.*?)\r?\n(.*?)(?=\r?\n##\s*Guión|\r?\n#\s*PARTE 2|$)', content, re.DOTALL)
    long_scripts = {}
    for num, title, body in long_form_matches:
        idx = int(num)
        narrator_blocks = re.findall(r'\*\*NARRADOR:\*\*\r?\n(.*?)(?=\r?\n###|\r?\n##|\r?\n---|$)', body, re.DOTALL)
        full_text = " ".join(clean_text(b) for b in narrator_blocks)
        long_scripts[idx] = {
            "key": f"extreme_job_{idx}_long",
            "title": title.strip(),
            "text": full_text.strip()
        }

    # 2. Parse Shorts Scripts
    shorts_scripts = []
    short_matches = re.findall(r'### Short (\d+): (.*?)\r?\n(.*?)(?=\r?\n###|\r?\n##|\r?\n#\s*PARTE|$)', content, re.DOTALL)
    for num_str, title, body in short_matches:
        idx = int(num_str)
        # Find the 3 parts
        parts = re.findall(r'\*\s*\*Narrador:\*\s*(.*?)(?=\r?\n\*|\r?\n\s*\*|$)', body, re.DOTALL)
        parts_clean = [clean_text(p) for p in parts]
        parent_story = (idx - 1) // 3 + 1
        part_in_story = (idx - 1) % 3 + 1
        shorts_scripts.append({
            "key": f"extreme_job_{parent_story}_short_{part_in_story}",
            "parent_key": f"extreme_job_{parent_story}_long",
            "short_index": idx,
            "part_num": part_in_story,
            "title": title.strip(),
            "parts": parts_clean,
            "full_text": " ".join(parts_clean).strip()
        })

    return long_scripts, shorts_scripts

async def generate_audio(text, output_path, rate="+5%"):
    voice = "es-MX-JorgeNeural"
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        return float(res.stdout.strip())
    return 0.0

async def main():
    print("Parsing scripts from scripts_deep.md...")
    long_scripts, shorts_scripts = parse_scripts()
    
    manifest = {
        "long_form": [],
        "shorts": []
    }
    
    tasks = []
    
    # Queue Long Form Audio Generation
    for idx, item in long_scripts.items():
        audio_name = f"{item['key']}.mp3"
        audio_path = os.path.join(audio_dir, audio_name)
        print(f"Queuing long-form audio generation: {item['key']}")
        tasks.append(generate_audio(item["text"], audio_path, rate="+5%"))
        manifest["long_form"].append({
            "key": item["key"],
            "story_num": idx,
            "title": item["title"],
            "script": item["text"],
            "audio_file": f"audio/{audio_name}",
            "duration": 0.0
        })
        
    # Queue Shorts Audio Generation
    for item in shorts_scripts:
        audio_name = f"{item['key']}.mp3"
        audio_path = os.path.join(audio_dir, audio_name)
        print(f"Queuing short-form audio generation: {item['key']}")
        tasks.append(generate_audio(item["full_text"], audio_path, rate="+20%"))
        manifest["shorts"].append({
            "key": item["key"],
            "parent_key": item["parent_key"],
            "short_index": item["short_index"],
            "part_num": item["part_num"],
            "title": item["title"],
            "parts": item["parts"],
            "script": item["full_text"],
            "audio_file": f"audio/{audio_name}",
            "duration": 0.0
        })
        
    print("\nExecuting TTS generation parallel tasks...")
    await asyncio.gather(*tasks)
    print("TTS Voiceover audio files generated successfully!")
    
    # Measure Durations
    print("\nMeasuring audio file durations with ffprobe...")
    for item in manifest["long_form"]:
        file_path = os.path.join(PROJECT_DIR, item["audio_file"])
        item["duration"] = get_audio_duration(file_path)
        print(f"  {item['key']} duration: {item['duration']:.2f}s")
        
    for item in manifest["shorts"]:
        file_path = os.path.join(PROJECT_DIR, item["audio_file"])
        item["duration"] = get_audio_duration(file_path)
        print(f"  {item['key']} duration: {item['duration']:.2f}s")
        
    # Save manifest database
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=4)
    print(f"\nManifest database saved to {manifest_path} successfully!")

if __name__ == "__main__":
    asyncio.run(main())
