# -*- coding: utf-8 -*-
"""
RENDER TEST FOR SHORT 2 WITH REAL AI PHOTOGRAPHY
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

sid = "narco_china_short_2"
title = "DE LAVAR DINERO NARCO A MAR-A-LAGO"
voice_path = os.path.join(BASE_DIR, "audio_assets/narco_china_short_2.mp3")
music_path = os.path.join(BASE_DIR, "music/Volatile Reaction.mp3")
badge = "DÚO 1: PARTE 2 DE 2"
out_mp4 = os.path.join(OUTPUT_DIR, "narco_china_short_2_final.mp4")

assets = ASSET_MAP.get(sid, [])
print(f"Assets loaded for '{sid}': {assets}")

dur = get_audio_duration(voice_path) or 29.5

builder = KinesioVideoBuilder(sid, width=1080, height=1920)
builder.add_scene(title, dur, asset_path=assets, effect_type="zoom_in")
if badge:
    builder.set_series_badge(badge)
if os.path.exists(music_path):
    builder.set_background_music(music_path, volume=-24)

builder.build(out_mp4, voice_audio_path=voice_path)
print(f"\n[SHORT 2 SUCCESS] Rendered file: {out_mp4}")
