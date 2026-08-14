# -*- coding: utf-8 -*-
"""
MASTER KINESIO V5.5 SINGLE RENDER TEST
"""

import os
import sys
import json
from kinesio_core import KinesioVideoBuilder, get_audio_duration

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
ASSET_MAP_PATH = os.path.join(BASE_DIR, "campaign_assets_map.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "final_rendered_mp4s")
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(ASSET_MAP_PATH, "r", encoding="utf-8") as f:
    ASSET_MAP = json.load(f)

sid = "narco_china_short_1"
title = "TRANSACCIONES ESPEJO (FLYING MONEY)"
voice_path = os.path.join(BASE_DIR, "audio_assets/narco_china_short_1.mp3")
music_path = os.path.join(BASE_DIR, "music/Cipher2.mp3")
badge = "DÚO 1: PARTE 1 DE 2"
out_mp4 = os.path.join(OUTPUT_DIR, "narco_china_short_1_final.mp4")

assets = ASSET_MAP.get(sid, [])
print(f"Assets loaded for {sid}: {assets}")

dur = get_audio_duration(voice_path) or 38.8

builder = KinesioVideoBuilder(sid, width=1080, height=1920)
builder.add_scene(title, dur, asset_path=assets, effect_type="zoom_in")
if badge:
    builder.set_series_badge(badge)
if os.path.exists(music_path):
    builder.set_background_music(music_path, volume=-24)

builder.build(out_mp4, voice_audio_path=voice_path)
print(f"\n[SINGLE RENDER DONE] File: {out_mp4}")
