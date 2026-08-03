# -*- coding: utf-8 -*-
import os
import sys
import time
import asyncio
import subprocess
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_assets")
os.makedirs(AUDIO_DIR, exist_ok=True)

ENGLISH_TEXT = (
    "Did you know an original Japanese OBI strip can multiply a record's value? "
    "But the market is full of fake bootlegs. "
    "At Metal Mania, we never sell reproductions: we guarantee total authenticity in pressings and autographs. "
    "Everything is in physical stock, protected in collector-grade packaging to arrive mint anywhere in the world. "
    "Claim these rare grails before they're gone. "
    "Tap the link in bio or visit metalmaniach.com."
)

VOICE = "en-US-GuyNeural"
RATE = "+18%"

async def generate():
    mp3_path = os.path.join(AUDIO_DIR, "metalmania_obi_english.mp3")
    vtt_path = os.path.join(AUDIO_DIR, "metalmania_obi_english.vtt")
    
    for attempt in range(8):
        try:
            print(f"Connecting to Edge-TTS (Attempt {attempt+1}/8)...")
            communicate = edge_tts.Communicate(ENGLISH_TEXT, VOICE, rate=RATE)
            submaker = edge_tts.SubMaker()
            audio_data = bytearray()
            
            async for chunk in communicate.stream():
                if chunk.get("type") == "audio":
                    audio_data.extend(chunk["data"])
                elif chunk.get("type") in ("WordBoundary", "SentenceBoundary"):
                    submaker.feed(chunk)
                    print(f"  CUE: offset={chunk['offset']/10000000:.3f}s, dur={chunk['duration']/10000000:.3f}s -> {chunk['text']}")
                    
            if len(audio_data) > 1000:
                with open(mp3_path, "wb") as f:
                    f.write(audio_data)
                    
                srt_content = submaker.get_srt()
                with open(vtt_path, "w", encoding="utf-8") as f:
                    f.write(srt_content)
                    
                res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", mp3_path], capture_output=True, text=True)
                dur = float(res.stdout.strip())
                print(f"\n[SUCCESS] English Audio generated: {mp3_path} ({dur:.2f}s)")
                print(f"SRT Subtitles:\n{srt_content}")
                return
        except Exception as e:
            print(f"  Warning on attempt {attempt+1}: {e}")
            await asyncio.sleep(2.5)
            
    raise RuntimeError("Failed to generate audio after 8 attempts.")

if __name__ == "__main__":
    asyncio.run(generate())
