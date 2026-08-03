# -*- coding: utf-8 -*-
import os
import sys
import asyncio
import subprocess
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_assets")
os.makedirs(AUDIO_DIR, exist_ok=True)

# Technical script translated and adapted for high-impact English commercial short (24s target)
ENGLISH_TEXT = (
    "Did you know an original Japanese OBI strip can multiply a record's value? "
    "But the market is flooded with fake bootlegs. "
    "At Metal Mania, we never sell reproductions: we guarantee 100% authenticity on every pressing and signed autograph. "
    "Everything is in physical stock and protected with collector-grade packaging to arrive mint anywhere in the world. "
    "Claim these rare grails before they sell out. "
    "Tap the link in bio or visit metalmaniach.com."
)

VOICE = "en-US-GuyNeural" # Punchy, clear, dynamic American commercial voice
RATE = "+6%"

async def generate():
    mp3_path = os.path.join(AUDIO_DIR, "metalmania_obi_english.mp3")
    vtt_path = os.path.join(AUDIO_DIR, "metalmania_obi_english.vtt")
    
    communicate = edge_tts.Communicate(ENGLISH_TEXT, VOICE, rate=RATE)
    submaker = edge_tts.SubMaker()
    audio_data = bytearray()
    
    async for chunk in communicate.stream():
        if chunk.get("type") == "audio":
            audio_data.extend(chunk["data"])
        elif chunk.get("type") in ("WordBoundary", "SentenceBoundary"):
            submaker.feed(chunk)
            print(f"CUE: offset={chunk['offset']/10000000:.2f}s, dur={chunk['duration']/10000000:.2f}s -> {chunk['text']}")
            
    with open(mp3_path, "wb") as f:
        f.write(audio_data)
        
    srt_content = submaker.get_srt()
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)
        
    res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3_path], capture_output=True, text=True)
    dur = float(res.stdout.strip())
    print(f"\n[SUCCESS] Audio generated at: {mp3_path}")
    print(f"Total Duration: {dur:.2f} seconds")
    print(f"SRT Subtitles:\n{srt_content}")

if __name__ == "__main__":
    asyncio.run(generate())
