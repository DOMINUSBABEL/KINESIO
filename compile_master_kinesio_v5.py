# -*- coding: utf-8 -*-
"""
KINESIO MASTER COMPILER V5.5: RE-RENDER FIRST 23 SHORTS WITH VERIFIED AUDIO MIXING
Shorts 24 to 48 already have perfect audio and are preserved intact.
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

# Only First 23 Shorts Table (Campaigns 1 & 2)
FIRST_23_SHORTS_CONFIG = [
    # Campaign 1: Narco China (13 Shorts)
    ("narco_china_short_1", "TRANSACCIONES ESPEJO (FLYING MONEY)", "audio_assets/narco_china_short_1.mp3", "music/Cipher2.mp3", "DÚO 1: PARTE 1 DE 2"),
    ("narco_china_short_2", "DE LAVAR DINERO NARCO A MAR-A-LAGO", "audio_assets/narco_china_short_2.mp3", "music/Volatile Reaction.mp3", "DÚO 1: PARTE 2 DE 2"),
    ("narco_china_short_3", "EL NEGOCIO SECRET DE LOS PRECURSORES", "audio_assets/narco_china_short_3.mp3", "music/Cipher2.mp3", "DÚO 2: PARTE 1 DE 2"),
    ("narco_china_short_4", "LA GUERRA ASIMETRICA DEL PCC", "audio_assets/narco_china_short_4.mp3", "music/Clash Defiant.mp3", "DÚO 2: PARTE 2 DE 2"),
    ("narco_china_short_5", "POR QUE LA DEA FALLA ANTE EL SISTEMA CHINO", "audio_assets/narco_china_short_5.mp3", "music/Volatile Reaction.mp3", "AUTÓNOMO 05/13"),
    ("narco_china_short_6", "LAS GRANJAS ILEGALES DE MARIHUANA EN MAINE", "audio_assets/narco_china_short_6.mp3", "music/Sneaky Snitch.mp3", "AUTÓNOMO 06/13"),
    ("narco_china_short_7", "EL TRUCO DEL 3%: TARIFAS DE LAVADO NARCO", "audio_assets/narco_china_short_7.mp3", "music/Severe Tire Damage.mp3", "AUTÓNOMO 07/13"),
    ("narco_china_short_8", "CARTELes SIN BANCOS TRADICIONALES", "audio_assets/narco_china_short_8.mp3", "music/Cipher2.mp3", "AUTÓNOMO 08/13"),
    ("narco_china_short_9", "XIZHI LI: EL LIMPIADOR DEFINITIVO", "audio_assets/narco_china_short_9.mp3", "music/Volatile Reaction.mp3", "AUTÓNOMO 09/13"),
    ("narco_china_short_10", "FUGA DE CAPITALES INVERSA DE LA ELITE CHINA", "audio_assets/narco_china_short_10.mp3", "music/Cipher2.mp3", "AUTÓNOMO 10/13"),
    ("narco_china_short_11", "TRADE-BASED MONEY LAUNDERING: FRAUDE ADUANERO", "audio_assets/narco_china_short_11.mp3", "music/Clash Defiant.mp3", "AUTÓNOMO 11/13"),
    ("narco_china_short_12", "FENTANILO Y GUERRA HIBRIDA: OPIO AL REVES", "audio_assets/narco_china_short_12.mp3", "music/Volatile Reaction.mp3", "AUTÓNOMO 12/13"),
    ("narco_china_short_13", "EL FUTURO GLOBAL DEL NARCOTRAFICO", "audio_assets/narco_china_short_13.mp3", "music/Future Gladiator.mp3", "AUTÓNOMO 13/13"),

    # Campaign 2: Guerra Antigua (10 Shorts)
    ("guerra_antigua_short_1", "EL GRAN MITO DE HOLLYWOOD", "audio_assets/guerra_antigua_short_1.mp3", "music/Clash Defiant.mp3", "HISTORIA MILITAR 01/10"),
    ("guerra_antigua_short_2", "LA FUERZA DEL MURO DE ESCUDOS", "audio_assets/guerra_antigua_short_2.mp3", "music/Volatile Reaction.mp3", "HISTORIA MILITAR 02/10"),
    ("guerra_antigua_short_3", "LA BIOMECANICA DEL CANSANCIO EXTREMO", "audio_assets/guerra_antigua_short_3.mp3", "music/Rites.mp3", "HISTORIA MILITAR 03/10"),
    ("guerra_antigua_short_4", "EL EMPUJE DEL OTHISMOS Y EL CHOQUE", "audio_assets/guerra_antigua_short_4.mp3", "music/Clash Defiant.mp3", "HISTORIA MILITAR 04/10"),
    ("guerra_antigua_short_5", "LA EXCEPCION DE MARATON (490 A.C.)", "audio_assets/guerra_antigua_short_5.mp3", "music/Moorland.mp3", "HISTORIA MILITAR 05/10"),
    ("guerra_antigua_short_6", "LA DISCIPLINA TACTICA DE LA LEGION ROMANA", "audio_assets/guerra_antigua_short_6.mp3", "music/Volatile Reaction.mp3", "HISTORIA MILITAR 06/10"),
    ("guerra_antigua_short_7", "LA MASACRE DE LA HUIDA: MUERTE POR LA ESPALDA", "audio_assets/guerra_antigua_short_7.mp3", "music/Clash Defiant.mp3", "HISTORIA MILITAR 07/10"),
    ("guerra_antigua_short_8", "LA FLAUTA Y LA FALANGE ESPARTANA", "audio_assets/guerra_antigua_short_8.mp3", "music/Rites.mp3", "HISTORIA MILITAR 08/10"),
    ("guerra_antigua_short_9", "EL MURO SAXON EN HASTINGS (1066)", "audio_assets/guerra_antigua_short_9.mp3", "music/Moorland.mp3", "HISTORIA MILITAR 09/10"),
    ("guerra_antigua_short_10", "LA REGLA DE ORO DEL VETERANO ANTIGUO", "audio_assets/guerra_antigua_short_10.mp3", "music/Volatile Reaction.mp3", "HISTORIA MILITAR 10/10")
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

def compile_first_23_shorts():
    print("=== RE-COMPILING FIRST 23 SHORTS (CAMPAIGNS 1 & 2) WITH AUDIO VERIFICATION ===", flush=True)
    os.chdir(BASE_DIR)
    
    for idx, (sid, title, voice_rel, music_rel, badge) in enumerate(FIRST_23_SHORTS_CONFIG, 1):
        out_mp4 = os.path.join(OUTPUT_DIR, f"{sid}_final.mp4")
        
        if has_audio_stream(out_mp4):
            print(f"  [SKIP] '{sid}' already compiled with verified audio stream.", flush=True)
            continue
            
        voice_path = os.path.join(BASE_DIR, voice_rel)
        music_path = os.path.join(BASE_DIR, music_rel)
        assets = ASSET_MAP.get(sid, [])
        if not assets:
            assets = [os.path.join(BASE_DIR, "screenshots", "background.jpg")]
            
        dur = get_audio_duration(voice_path) or 35.0
        
        print(f"\n[RE-BUILDING SHORT {idx}/23] '{sid}' | Voice: {os.path.basename(voice_path)} ({dur:.1f}s) | Badge: '{badge}'", flush=True)
        
        builder = KinesioVideoBuilder(sid, width=1080, height=1920)
        builder.add_scene(title, dur, asset_path=assets, effect_type="zoom_in")
        if badge:
            builder.set_series_badge(badge)
            
        if os.path.exists(music_path):
            builder.set_background_music(music_path, volume=-24)
            
        builder.build(out_mp4, voice_audio_path=voice_path)
        if has_audio_stream(out_mp4):
            print(f"  [SUCCESS] FINAL MP4 RE-RENDERED WITH AUDIO: {os.path.basename(out_mp4)} ({os.path.getsize(out_mp4)} bytes)", flush=True)

if __name__ == "__main__":
    compile_first_23_shorts()
