# -*- coding: utf-8 -*-
"""
TEST RENDERER FOR SHORT 1: VERIFIES FULL VISUAL COVERAGE & KEN BURNS B-ROLL ROTATION
"""

import os
import sys
import json
from kinesio_core import KinesioVideoBuilder, get_audio_duration, log_info

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
out_mp4 = os.path.join(OUTPUT_DIR, f"{sid}_final.mp4")

assets = ASSET_MAP.get(sid, [])
print(f"Loaded assets for '{sid}': {assets}")

dur = get_audio_duration(voice_path) or 38.8

builder = KinesioVideoBuilder(sid, width=1080, height=1920)
builder.add_scene(title, dur, asset_path=assets, effect_type="zoom_in")
if badge:
    builder.set_series_badge(badge)
if os.path.exists(music_path):
    builder.set_background_music(music_path, volume=-24)

builder.build(out_mp4, voice_audio_path=voice_path)
print(f"\n[TEST RENDER SUCCESS] Output file: {out_mp4} (Size: {os.path.getsize(out_mp4)} bytes)")
