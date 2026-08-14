# -*- coding: utf-8 -*-
import os
import sys
import asyncio
import subprocess
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ENGLISH_TEXT = (
    "Did you know an original Japanese OBI strip can multiply a record's value? "
    "But the market is flooded with fake bootlegs. "
    "At Metal Mania, we never sell reproductions: we guarantee 100% authenticity on every pressing and hand-signed autograph. "
    "Everything is in physical stock and packed with collector-grade armor to arrive mint anywhere in the world. "
    "Claim these rare grails before they sell out. "
    "Tap the link in bio or visit metalmaniach.com."
)

async def test_voices():
    for voice in ["en-US-GuyNeural", "en-US-ChristopherNeural", "en-US-AndrewNeural"]:
        for rate in ["+0%", "+4%", "+8%", "+12%"]:
            c = edge_tts.Communicate(ENGLISH_TEXT, voice, rate=rate)
            fn = f"test_{voice}_{rate.replace('%','').replace('+','p')}.mp3"
            await c.save(fn)
            res = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", fn], capture_output=True, text=True)
            dur = float(res.stdout.strip())
            print(f"{voice} ({rate}): {dur:.2f}s")
            if os.path.exists(fn):
                os.remove(fn)

if __name__ == "__main__":
    asyncio.run(test_voices())
