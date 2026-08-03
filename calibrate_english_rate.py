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

ENGLISH_TEXT = (
    "Did you know an original Japanese OBI strip can multiply a record's value? "
    "But the market is full of fake bootlegs. "
    "At Metal Mania, we never sell reproductions: we guarantee total authenticity in pressings and autographs. "
    "Everything is in physical stock, protected in collector-grade packaging to arrive mint anywhere in the world. "
    "Claim these rare grails before they're gone. "
    "Tap the link in bio or visit metalmaniach.com."
)

VOICE = "en-US-GuyNeural"

async def test():
    for r in ["+16%", "+18%", "+20%", "+22%"]:
        c = edge_tts.Communicate(ENGLISH_TEXT, VOICE, rate=r)
        fn = f"temp_eng_{r}.mp3"
        await c.save(fn)
        res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fn], capture_output=True, text=True)
        dur = float(res.stdout.strip())
        print(f"Rate {r}: {dur:.2f}s")
        if os.path.exists(fn): os.remove(fn)

if __name__ == "__main__":
    asyncio.run(test())
