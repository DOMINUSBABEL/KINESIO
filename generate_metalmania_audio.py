# -*- coding: utf-8 -*-
import os
import sys
import asyncio
import edge_tts

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_assets")
os.makedirs(AUDIO_DIR, exist_ok=True)

VOICEOVER_TEXT = (
    "¿Sabías que un OBI japonés original puede multiplicar el valor de un disco? "
    "Pero el mercado está lleno de copias falsas. En Metal Mania no vendemos reproducciones: "
    "garantizamos autenticidad total en prensajes y firmas. "
    "Todo está en stock y protegido con embalaje especial de grado coleccionista para llegar intacto a cualquier país. "
    "Consigue estas rarezas antes de que se agoten. Visita el link de la bio o entra a metalmaniach.com."
)

VOICE = "es-MX-JorgeNeural"

async def main():
    mp3_path = os.path.join(AUDIO_DIR, "metalmania_obi_short.mp3")
    vtt_path = os.path.join(AUDIO_DIR, "metalmania_obi_short.vtt")
    
    # We want a dynamic, confident, professional commercial pace (~23-24s)
    communicate = edge_tts.Communicate(VOICEOVER_TEXT, VOICE, rate="+5%")
    submaker = edge_tts.SubMaker()
    
    with open(mp3_path, "wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                submaker.feed(chunk)
                
    with open(vtt_path, "w", encoding="utf-8") as f:
        f.write(submaker.get_srt())
        
    print(f"Generated audio: {mp3_path} ({os.path.getsize(mp3_path)} bytes)")
    print(f"Generated subtitles: {vtt_path}")

if __name__ == "__main__":
    asyncio.run(main())
