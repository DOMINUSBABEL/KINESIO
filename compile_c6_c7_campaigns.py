# -*- coding: utf-8 -*-
"""
KINESIO MASTER COMPILER V5.5: CAMPAIGNS 6 (13 SHORTS) AND 7 (8 SHORTS)
"""

import os
import sys
import json
import subprocess
from kinesio_core import KinesioVideoBuilder, get_audio_duration

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
ASSET_MAP_PATH = os.path.join(BASE_DIR, "campaign_assets_map.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_rendered_mp4s")
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(ASSET_MAP_PATH, "r", encoding="utf-8") as f:
    ASSET_MAP = json.load(f)

# Campaign 6: Propiedad Digital (13 Shorts)
CAMPAIGN_6_SHORTS_CONFIG = [
    ("propiedad_short_1", "SABIAS QUE TU PS5 NO ES REALMENTE TUYA", "audio_assets/propiedad_short_1.mp3", "music/Severe Tire Damage.mp3", "DÚO 1: PARTE 1 DE 2"),
    ("propiedad_short_2", "EL BANEO A DISTANCIA QUE INVALIDA TU CONSOLA DE $500", "audio_assets/propiedad_short_2.mp3", "music/Cipher2.mp3", "DÚO 1: PARTE 2 DE 2"),
    ("propiedad_short_3", "EL DIA QUE UBISOFT BORRO UN JUEGO QUE PAGASTE", "audio_assets/propiedad_short_3.mp3", "music/Volatile Reaction.mp3", "DÚO 2: PARTE 1 DE 2"),
    ("propiedad_short_4", "POR QUE LAS TIENDAS DIGITALES PUEDEN QUITARTE TODO", "audio_assets/propiedad_short_4.mp3", "music/Future Gladiator.mp3", "DÚO 2: PARTE 2 DE 2"),
    ("propiedad_short_5", "SONY BORRANDO PELICULAS COMPRADAS EN PSN", "audio_assets/propiedad_short_5.mp3", "music/Scheming Weasel.mp3", "AUTÓNOMO 05/13"),
    ("propiedad_short_6", "LA TRAMPA DE LAS CONSOLAS SIN LECTOR DE DISCO", "audio_assets/propiedad_short_6.mp3", "music/Severe Tire Damage.mp3", "AUTÓNOMO 06/13"),
    ("propiedad_short_7", "GAME PASS Y LA ILUSION DE BIBLIOTECA INFINITA", "audio_assets/propiedad_short_7.mp3", "music/Cipher2.mp3", "AUTÓNOMO 07/13"),
    ("propiedad_short_8", "ASIENTOS CALEFACTABLES POR SUSCRIPCION: BMW", "audio_assets/propiedad_short_8.mp3", "music/Sneaky Snitch.mp3", "AUTÓNOMO 08/13"),
    ("propiedad_short_9", "QUE PASARA CON TU CUENTA DE STEAM CUANDO FALTES", "audio_assets/propiedad_short_9.mp3", "music/Future Gladiator.mp3", "AUTÓNOMO 09/13"),
    ("propiedad_short_10", "EL DERECHO A REPARAR: MARCAS CONTRA HERRAMIENTAS", "audio_assets/propiedad_short_10.mp3", "music/Clash Defiant.mp3", "AUTÓNOMO 10/13"),
    ("propiedad_short_11", "LA DESTRUCCION DE HISTORIA GAMING: PRESERVACION", "audio_assets/propiedad_short_11.mp3", "music/Volatile Reaction.mp3", "AUTÓNOMO 11/13"),
    ("propiedad_short_12", "NO POSEERAS NADA Y SERAS FELIZ: DISTOPIA TECH", "audio_assets/propiedad_short_12.mp3", "music/Cipher2.mp3", "AUTÓNOMO 12/13"),
    ("propiedad_short_13", "EL MOVIMIENTO DE RESISTENCIA: PROPIEDAD REAL", "audio_assets/propiedad_short_13.mp3", "music/Clash Defiant.mp3", "AUTÓNOMO 13/13")
]

# Campaign 7: Pig Butchering Estafas (8 Shorts)
CAMPAIGN_7_SHORTS_CONFIG = [
    ("estafa_anime_short_1", "LA SOLICITUD DE LA CHICA ANIME QUE TE QUIERE ESTAFAR", "audio_assets/estafa_anime_short_1.mp3", "music/Sneaky Snitch.mp3", "DÚO 1: PARTE 1 DE 2"),
    ("estafa_anime_short_2", "QUE ES EL PIG BUTCHERING: LA ANATOMIA DEL FRAUDE", "audio_assets/estafa_anime_short_2.mp3", "music/Scheming Weasel.mp3", "DÚO 1: PARTE 2 DE 2"),
    ("estafa_anime_short_3", "DE DISCORD A WHATSAPP: TRAMPA DE AISLAMIENTO", "audio_assets/estafa_anime_short_3.mp3", "music/Sneaky Snitch.mp3", "DÚO 2: PARTE 1 DE 2"),
    ("estafa_anime_short_4", "LA FALSA APP DE CRIPTOMONEDAS DONDE SIEMPRE GANAS", "audio_assets/estafa_anime_short_4.mp3", "music/Monkeys Spinning Monkeys.mp3", "DÚO 2: PARTE 2 DE 2"),
    ("estafa_anime_short_5", "LA FALSA RETIRADA DE $50: ANZUELO DEFINITIVO", "audio_assets/estafa_anime_short_5.mp3", "music/Sneaky Snitch.mp3", "AUTÓNOMO 05/08"),
    ("estafa_anime_short_6", "EL IMPUESTO DE DESBLOQUEO: TRAMPA SIN ESCAPE", "audio_assets/estafa_anime_short_6.mp3", "music/Volatile Reaction.mp3", "AUTÓNOMO 06/08"),
    ("estafa_anime_short_7", "EL LADO OSCURO: GRANJAS DE ESTAFADORES EN ASIA", "audio_assets/estafa_anime_short_7.mp3", "music/Clash Defiant.mp3", "AUTÓNOMO 07/08"),
    ("estafa_anime_short_8", "LA REGLA DE ORO PARA NUNCA CAER EN ESTAFAS ROMANCE", "audio_assets/estafa_anime_short_8.mp3", "music/Severe Tire Damage.mp3", "AUTÓNOMO 08/08")
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

def compile_all_campaigns():
    os.chdir(BASE_DIR)
    
    print("\n=== COMPILING CAMPAIGN 6: PROPIEDAD DIGITAL (13 SHORTS) ===", flush=True)
    for idx, (sid, title, voice_rel, music_rel, badge) in enumerate(CAMPAIGN_6_SHORTS_CONFIG, 1):
        out_mp4 = os.path.join(OUTPUT_DIR, f"{sid}_final.mp4")
        if has_audio_stream(out_mp4):
            print(f"  [SKIP] '{sid}' already compiled.", flush=True)
            continue
        voice_path = os.path.join(BASE_DIR, voice_rel)
        music_path = os.path.join(BASE_DIR, music_rel)
        assets = ASSET_MAP.get(sid, [])
        if not assets:
            assets = [os.path.join(BASE_DIR, "screenshots", "background.jpg")]
        dur = get_audio_duration(voice_path) or 48.0
        print(f"\n[BUILDING SHORT C6-{idx}/13] '{sid}' | Voice: {os.path.basename(voice_path)} ({dur:.1f}s) | Badge: '{badge}'", flush=True)
        builder = KinesioVideoBuilder(sid, width=1080, height=1920)
        builder.add_scene(title, dur, asset_path=assets, effect_type="zoom_in")
        if badge:
            builder.set_series_badge(badge)
        if os.path.exists(music_path):
            builder.set_background_music(music_path, volume=-24)
        builder.build(out_mp4, voice_audio_path=voice_path)
        if has_audio_stream(out_mp4):
            print(f"  [SUCCESS] RENDERED WITH AUDIO: {os.path.basename(out_mp4)}", flush=True)

    print("\n=== COMPILING CAMPAIGN 7: PIG BUTCHERING ESTAFAS (8 SHORTS) ===", flush=True)
    for idx, (sid, title, voice_rel, music_rel, badge) in enumerate(CAMPAIGN_7_SHORTS_CONFIG, 1):
        out_mp4 = os.path.join(OUTPUT_DIR, f"{sid}_final.mp4")
        if has_audio_stream(out_mp4):
            print(f"  [SKIP] '{sid}' already compiled.", flush=True)
            continue
        voice_path = os.path.join(BASE_DIR, voice_rel)
        music_path = os.path.join(BASE_DIR, music_rel)
        assets = ASSET_MAP.get(sid, [])
        if not assets:
            assets = [os.path.join(BASE_DIR, "screenshots", "background.jpg")]
        dur = get_audio_duration(voice_path) or 45.0
        print(f"\n[BUILDING SHORT C7-{idx}/8] '{sid}' | Voice: {os.path.basename(voice_path)} ({dur:.1f}s) | Badge: '{badge}'", flush=True)
        builder = KinesioVideoBuilder(sid, width=1080, height=1920)
        builder.add_scene(title, dur, asset_path=assets, effect_type="zoom_in")
        if badge:
            builder.set_series_badge(badge)
        if os.path.exists(music_path):
            builder.set_background_music(music_path, volume=-24)
        builder.build(out_mp4, voice_audio_path=voice_path)
        if has_audio_stream(out_mp4):
            print(f"  [SUCCESS] RENDERED WITH AUDIO: {os.path.basename(out_mp4)}", flush=True)

if __name__ == "__main__":
    compile_all_campaigns()
