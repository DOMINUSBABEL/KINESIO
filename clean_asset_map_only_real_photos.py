# -*- coding: utf-8 -*-
"""
MAP ALL 48 SHORTS ACROSS 4 CAMPAIGNS TO THEIR EXCLUSIVE REAL AI PHOTOGRAPHIC ARTWORKS
"""

import os
import sys
import json
import glob

BASE_DIR = r"C:\Users\jegom\shorts_project"
BRAIN_DIR = r"C:\Users\jegom\.gemini\antigravity-cli\brain\b440111e-f299-42bc-bfbd-181f6ef4fb00"
ASSET_MAP_PATH = os.path.join(BASE_DIR, "campaign_assets_map.json")

# 48 Shorts Mapping Table
PHOTO_PATTERNS = {
    # Campaign 1: Narco China (13 Shorts)
    "narco_china_short_1": "narco_china_1_photo1_*.jpg",
    "narco_china_short_2": "narco_china_2_photo1_*.jpg",
    "narco_china_short_3": "narco_china_3_photo1_*.jpg",
    "narco_china_short_4": "narco_china_4_photo1_*.jpg",
    "narco_china_short_5": "narco_china_5_photo1_*.jpg",
    "narco_china_short_6": "narco_china_6_photo1_*.jpg",
    "narco_china_short_7": "narco_china_7_photo1_*.jpg",
    "narco_china_short_8": "narco_china_8_photo1_*.jpg",
    "narco_china_short_9": "narco_china_9_photo1_*.jpg",
    "narco_china_short_10": "narco_china_10_photo1_*.jpg",
    "narco_china_short_11": "narco_china_11_photo1_*.jpg",
    "narco_china_short_12": "narco_china_12_photo1_*.jpg",
    "narco_china_short_13": "narco_china_13_photo1_*.jpg",

    # Campaign 2: Guerra Antigua (10 Shorts)
    "guerra_antigua_short_1": "guerra_antigua_1_photo1_*.jpg",
    "guerra_antigua_short_2": "guerra_antigua_2_photo1_*.jpg",
    "guerra_antigua_short_3": "guerra_antigua_3_photo1_*.jpg",
    "guerra_antigua_short_4": "guerra_antigua_4_photo1_*.jpg",
    "guerra_antigua_short_5": "guerra_antigua_5_photo1_*.jpg",
    "guerra_antigua_short_6": "guerra_antigua_6_photo1_*.jpg",
    "guerra_antigua_short_7": "guerra_antigua_7_photo1_*.jpg",
    "guerra_antigua_short_8": "guerra_antigua_8_photo1_*.jpg",
    "guerra_antigua_short_9": "guerra_antigua_9_photo1_*.jpg",
    "guerra_antigua_short_10": "guerra_antigua_10_photo1_*.jpg",

    # Campaign 3: Steam Monopolio (12 Shorts)
    "steam_short_1": "steam_1_photo1_*.jpg",
    "steam_short_2": "steam_2_photo1_*.jpg",
    "steam_short_3": "steam_3_photo1_*.jpg",
    "steam_short_4": "steam_4_photo1_*.jpg",
    "steam_short_5": "steam_5_photo1_*.jpg",
    "steam_short_6": "steam_6_photo1_*.jpg",
    "steam_short_7": "steam_7_photo1_*.jpg",
    "steam_short_8": "steam_8_photo1_*.jpg",
    "steam_short_9": "steam_9_photo1_*.jpg",
    "steam_short_10": "steam_10_photo1_*.jpg",
    "steam_short_11": "steam_11_photo1_*.jpg",
    "steam_short_12": "steam_12_photo1_*.jpg",

    # Campaign 4: Programadores IA (13 Shorts)
    "programadores_short_1": "programadores_1_photo1_*.jpg",
    "programadores_short_2": "programadores_2_photo1_*.jpg",
    "programadores_short_3": "programadores_3_photo1_*.jpg",
    "programadores_short_4": "programadores_4_photo1_*.jpg",
    "programadores_short_5": "programadores_5_photo1_*.jpg",
    "programadores_short_6": "programadores_6_photo1_*.jpg",
    "programadores_short_7": "programadores_7_photo1_*.jpg",
    "programadores_short_8": "programadores_8_photo1_*.jpg",
    "programadores_short_9": "programadores_9_photo1_*.jpg",
    "programadores_short_10": "programadores_10_photo1_*.jpg",
    "programadores_short_11": "programadores_11_photo1_*.jpg",
    "programadores_short_12": "programadores_12_photo1_*.jpg",
    "programadores_short_13": "programadores_13_photo1_*.jpg"
}

clean_map = {}

for sid, pattern in PHOTO_PATTERNS.items():
    matches = glob.glob(os.path.join(BRAIN_DIR, pattern))
    if matches:
        clean_map[sid] = [matches[0]]
        print(f"Mapped Real AI Photo for '{sid}': {os.path.basename(matches[0])}")
    else:
        print(f"WARNING: No photo match for '{sid}' (pattern: {pattern})")

with open(ASSET_MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(clean_map, f, indent=2, ensure_ascii=False)

print(f"\n[SUCCESS] campaign_assets_map.json updated with {len(clean_map)} Real AI Photographic Artworks!")
