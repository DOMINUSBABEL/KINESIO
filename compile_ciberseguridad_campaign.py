# -*- coding: utf-8 -*-
"""
KINESIO MASTER COMPILER V5.5: CAMPAIGN 5 (CIBERSEGURIDAD & IA - 11 SHORTS)
"""

import os
import sys
import json
import subprocess
from kinesio_core import KinesioVideoBuilder, get_audio_duration

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
AUDIO_DIR = os.path.join(BASE_DIR, "audio_assets")
ASSET_MAP_PATH = os.path.join(BASE_DIR, "campaign_assets_map.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_rendered_mp4s")
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(ASSET_MAP_PATH, "r", encoding="utf-8") as f:
    ASSET_MAP = json.load(f)

CAMPAIGN_5_SHORTS_CONFIG = [
    ("ciberseguridad_short_1", "EL DIA QUE EE.UU. PROHIBIO LA IA MAS AVANZADA", "audio_assets/ciberseguridad_short_1.mp3", "music/Volatile Reaction.mp3", "DÚO 1: PARTE 1 DE 2"),
    ("ciberseguridad_short_2", "LA IA HACKER DE 0 DIAS QUE ATERRORA AL PENTAGONO", "audio_assets/ciberseguridad_short_2.mp3", "music/Cipher2.mp3", "DÚO 1: PARTE 2 DE 2"),
    ("ciberseguridad_short_3", "EL IMPUESTO OBLIGATORIO QUE TODA EMPRESA PAGA", "audio_assets/ciberseguridad_short_3.mp3", "music/Future Gladiator.mp3", "DÚO 2: PARTE 1 DE 2"),
    ("ciberseguridad_short_4", "POR QUE LA CIBERSEGURIDAD NUNCA CAERA EN RECESION", "audio_assets/ciberseguridad_short_4.mp3", "music/Severe Tire Damage.mp3", "DÚO 2: PARTE 2 DE 2"),
    ("ciberseguridad_short_5", "LA CIBERGUERRA SILENCIOSA CONTRA INFRAESTRUCTURA", "audio_assets/ciberseguridad_short_5.mp3", "music/Clash Defiant.mp3", "AUTÓNOMO 05/11"),
    ("ciberseguridad_short_6", "EL MODELO OSI EXPLICADO PARA INVERSORES TECH", "audio_assets/ciberseguridad_short_6.mp3", "music/Cipher2.mp3", "AUTÓNOMO 06/11"),
    ("ciberseguridad_short_7", "CAPA BAJA: EL IMPERIO HARDWARE DE CISCO Y ARISTA", "audio_assets/ciberseguridad_short_7.mp3", "music/Future Gladiator.mp3", "AUTÓNOMO 07/11"),
    ("ciberseguridad_short_8", "CAPA MEDIA: LA MURALLA DE FUEGO DE PALO ALTO", "audio_assets/ciberseguridad_short_8.mp3", "music/Volatile Reaction.mp3", "AUTÓNOMO 08/11"),
    ("ciberseguridad_short_9", "CAPA ALTA: CROWDSTRIKE Y EL NEGOCIO DE IDENTIDAD", "audio_assets/ciberseguridad_short_9.mp3", "music/Severe Tire Damage.mp3", "AUTÓNOMO 09/11"),
    ("ciberseguridad_short_10", "DEEPFAKES DE VOZ Y LA ESTAFA DEL CEO POR IA", "audio_assets/ciberseguridad_short_10.mp3", "music/Sneaky Snitch.mp3", "AUTÓNOMO 10/11"),
    ("ciberseguridad_short_11", "FUTURO DE LA IA: ESPADA HACKER O ESCUDO GLOBAL", "audio_assets/ciberseguridad_short_11.mp3", "music/Clash Defiant.mp3", "AUTÓNOMO 11/11")
]

def has_audio_stream(filepath):
    if not os.path.exists(filepath):
        return False
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "stream=codec_type",
        "-of", "default=noprint_wrappers=1",
        filepath
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return "codec_type=audio" in res.stdout

def compile_ciberseguridad_campaign():
    print("=== COMPILING CAMPAIGN 5: CIBERSEGURIDAD & IA (11 SHORTS) ===", flush=True)
    os.chdir(BASE_DIR)
    
    for idx, (sid, title, voice_rel, music_rel, badge) in enumerate(CAMPAIGN_5_SHORTS_CONFIG, 1):
        out_mp4 = os.path.join(OUTPUT_DIR, f"{sid}_final.mp4")
        
        if has_audio_stream(out_mp4):
            print(f"  [SKIP] '{sid}' already compiled with verified audio stream.", flush=True)
            continue
            
        voice_path = os.path.join(BASE_DIR, voice_rel)
        music_path = os.path.join(BASE_DIR, music_rel)
        assets = ASSET_MAP.get(sid, [])
        if not assets:
            assets = [os.path.join(BASE_DIR, "screenshots", "background.jpg")]
            
        dur = get_audio_duration(voice_path) or 45.0
        
        print(f"\n[BUILDING SHORT {idx}/11] '{sid}' | Voice: {os.path.basename(voice_path)} ({dur:.1f}s) | Badge: '{badge}'", flush=True)
        
        builder = KinesioVideoBuilder(sid, width=1080, height=1920)
        builder.add_scene(title, dur, asset_path=assets, effect_type="zoom_in")
        if badge:
            builder.set_series_badge(badge)
            
        if os.path.exists(music_path):
            builder.set_background_music(music_path, volume=-24)
            
        builder.build(out_mp4, voice_audio_path=voice_path)
        if has_audio_stream(out_mp4):
            print(f"  [SUCCESS] FINAL MP4 RENDERED WITH AUDIO: {os.path.basename(out_mp4)} ({os.path.getsize(out_mp4)} bytes)", flush=True)
        else:
            print(f"  [WARNING] Audio stream missing for '{sid}'!", flush=True)

if __name__ == "__main__":
    compile_ciberseguridad_campaign()
