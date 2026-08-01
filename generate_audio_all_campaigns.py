# -*- coding: utf-8 -*-
"""
Neural TTS Generator (Edge-TTS) for Campaign: Mike Ehrmantraut (Breaking Bad / Better Call Saul)
Generates 16 Clean Spoken Dialogue Tracks & VTT Subtitle Cues for DOMINUSBABEL.
"""

import os
import sys
import re
import asyncio
import edge_tts

VOICE = "es-ES-AlvaroNeural" # High quality Spanish masculine narration
PROJECT_DIR = r"C:\Users\jegom\shorts_project"

def clean_speech_text(raw_text):
    lines = raw_text.split('\n')
    clean = []
    for l in lines:
        l_str = l.strip()
        if not l_str:
            continue
        if l_str.startswith('#') or l_str.startswith('---'):
            continue
        if re.search(r'^SHORT \d+:', l_str, re.IGNORECASE):
            continue
        if re.search(r'^(INTRODUCCIÓN|GUIÓN|VÍDEO|Duración|Voz)', l_str, re.IGNORECASE):
            continue
        clean.append(l_str)
    return " ".join(clean)

def extract_short_text(filepath, short_num):
    if not os.path.exists(filepath):
        return ""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    header = f"## 📱 SHORT {short_num}:"
    next_header = f"## 📱 SHORT {short_num + 1}:" if short_num < 16 else "---"
    
    if header in content:
        start_idx = content.find(header)
        end_idx = content.find(next_header, start_idx) if next_header in content else len(content)
        raw_text = content[start_idx:end_idx]
        return clean_speech_text(raw_text)

    return ""

def load_all_scripts():
    script_md = os.path.join(PROJECT_DIR, "scripts_mike_ehrmantraut_shorts.md")
    scripts = {}
    
    for i in range(1, 17):
        fname = f"audio_mike_short_{i}.mp3"
        scripts[fname] = extract_short_text(script_md, i)
        
    return scripts

async def generate_tts(audio_filename, text):
    mp3_path = os.path.join(PROJECT_DIR, audio_filename)
    vtt_path = mp3_path.replace(".mp3", ".vtt")
    
    if not text:
        print(f"[ERROR] Empty text for {audio_filename}")
        return
        
    print(f"[TTS] Generating: {audio_filename} ({len(text.split())} words)...")
    communicate = edge_tts.Communicate(text, VOICE)
    submaker = edge_tts.SubMaker()
    
    with open(mp3_path, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.create_sub(chunk["offset"], chunk["duration"], chunk["text"])
                
    with open(vtt_path, "w", encoding="utf-8") as f:
        if hasattr(submaker, 'generate_subs'):
            f.write(submaker.generate_subs())
        elif hasattr(submaker, 'get_srt'):
            f.write(submaker.get_srt())
        else:
            f.write("")
    print(f"[TTS SUCCESS] Created {mp3_path}")

async def main():
    print("==================================================")
    print("  NEURAL TTS GENERATOR: CAMPAIGN MIKE EHRMANTRAUT ")
    print("==================================================")
    scripts = load_all_scripts()
    tasks = []
    for fname, text in scripts.items():
        tasks.append(generate_tts(fname, text))
    await asyncio.gather(*tasks)
    print("\n[ALL SUCCESS] Generated 16 Clean Audio Tracks & Subtitles for Mike Ehrmantraut Campaign!")

if __name__ == "__main__":
    asyncio.run(main())
