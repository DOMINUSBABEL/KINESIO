import os
import re
import json
import asyncio
import subprocess
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\reddit_shorts_project"
scripts_path = os.path.join(PROJECT_DIR, "scripts_reddit_clean.md")
audio_dir = os.path.join(PROJECT_DIR, "audio")
manifest_path = os.path.join(PROJECT_DIR, "manifest.json")

os.makedirs(audio_dir, exist_ok=True)

try:
    import edge_tts
except ImportError:
    print("Installing edge-tts...")
    subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import edge_tts

def get_audio_duration(path):
    if not os.path.exists(path):
        return 0.0
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(res.stdout.strip())
    except:
        return 0.0

def parse_markdown_scripts(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        
    stories_raw = content.split("\n# Historia ")
    # First split might have title, skip if empty
    if len(stories_raw) > 1 and not stories_raw[0].strip().startswith("Historia"):
        stories_raw = stories_raw[1:]
        
    parsed_stories = []
    
    for idx, story_block in enumerate(stories_raw):
        # Restore the Historia prefix
        story_text = "Historia " + story_block
        lines = story_text.split('\n')
        
        story_title = lines[0].strip()
        origen = ""
        parts_blocks = story_text.split("\n## ")
        
        # Origen is typically the second line
        for line in lines[1:5]:
            if "origen:" in line.lower():
                origen = line.replace("**", "").strip()
                break
                
        story_id = idx + 1
        
        parts = []
        for p_block in parts_blocks[1:]:
            p_lines = p_block.split('\n')
            part_title = p_lines[0].strip()
            
            sfx = ""
            prompt = ""
            voiceover = ""
            
            for line in p_lines[1:]:
                line = line.strip()
                if "**SFX & Música:**" in line:
                    sfx = line.replace("* **SFX & Música:**", "").replace("* **SFX & Musica:**", "").strip()
                elif "**Prompt Visual:**" in line:
                    prompt = line.replace("* **Prompt Visual:**", "").strip()
                elif "**Narración (Voiceover):**" in line:
                    # Narración voiceover is multi-line or starts on the next line
                    pass
                elif line.startswith('"') or (voiceover == "" and not line.startswith("*") and len(line) > 10):
                    # It's the voiceover text!
                    text_clean = line.strip().strip('"')
                    if voiceover:
                        voiceover += " " + text_clean
                    else:
                        voiceover = text_clean
            
            # Extract part number and total parts from title (e.g. "El Secreto del Sótano de mi Abuelo - Parte 1 de 3")
            part_num = 1
            total_parts = 1
            match = re.search(r'parte\s+(\d+)\s+de\s+(\d+)', part_title, re.IGNORECASE)
            if match:
                part_num = int(match.group(1))
                total_parts = int(match.group(2))
                
            parts.append({
                "part_title": part_title,
                "part_num": part_num,
                "total_parts": total_parts,
                "sfx": sfx,
                "prompt": prompt,
                "voiceover": voiceover
            })
            
        parsed_stories.append({
            "story_id": story_id,
            "story_title": story_title,
            "origen": origen,
            "parts": parts
        })
        
    return parsed_stories

async def generate_voiceover(text, output_file):
    # rate=+22% to match official Spanish narration speed
    communicate = edge_tts.Communicate(text, "es-MX-JorgeNeural", rate="+22%")
    await communicate.save(output_file)

async def main():
    print("Parsing scripts_reddit_clean.md...")
    stories = parse_markdown_scripts(scripts_path)
    print(f"Parsed {len(stories)} stories.")
    
    tasks = []
    metadata = []
    
    for s in stories:
        print(f"Story {s['story_id']}: {s['story_title']} ({len(s['parts'])} parts)")
        for p in s['parts']:
            audio_filename = f"audio_story_{s['story_id']}_part_{p['part_num']}.mp3"
            audio_path = os.path.join(audio_dir, audio_filename)
            
            # Schedule generation
            tasks.append((p, audio_path, s))
            
    print(f"Generating {len(tasks)} audio files in parallel...")
    
    # Run in batches of 5 to avoid API rate limits
    batch_size = 5
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i+batch_size]
        running_tasks = []
        for p, path, s in batch:
            print(f"  [TTS] Generating voiceover for Story {s['story_id']} Part {p['part_num']}...")
            running_tasks.append(generate_voiceover(p['voiceover'], path))
            
        await asyncio.gather(*running_tasks)
        print(f"Completed batch {i // batch_size + 1} of {len(tasks) // batch_size + 1}")
        
    print("Verifying durations and compiling manifest.json...")
    manifest_data = []
    for p, path, s in tasks:
        duration = get_audio_duration(path)
        # Determine background music dynamically based on category
        origen_lower = s['origen'].lower()
        if "horror" in origen_lower or "mystery" in origen_lower:
            bg_music = "Sneaky Snitch.mp3"
        elif "drama" in origen_lower or "revenge" in origen_lower:
            bg_music = "Scheming Weasel.mp3"
        else:
            bg_music = "Take a Chance.mp3"
            
        manifest_data.append({
            "key": f"reddit_story_{s['story_id']}_part_{p['part_num']}",
            "story_id": s['story_id'],
            "story_title": s['story_title'],
            "part_title": p['part_title'],
            "part_num": p['part_num'],
            "total_parts": p['total_parts'],
            "audio_path": path,
            "duration": duration,
            "prompt": p['prompt'],
            "voiceover": p['voiceover'],
            "sfx": p['sfx'],
            "bg_music": bg_music,
            "bg_name": f"story_{s['story_id']}.jpg"
        })
        
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest_data, f, indent=2, ensure_ascii=False)
        
    print(f"¡Todo listo! Manifest guardado en: {manifest_path}")

if __name__ == "__main__":
    asyncio.run(main())
