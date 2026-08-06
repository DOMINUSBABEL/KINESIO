# -*- coding: utf-8 -*-
"""
Map all 21 AI photorealistic images into campaign_assets_map.json for Campaign 6 & Campaign 7
"""

import os
import sys
import json
import glob

BASE_DIR = r"C:\Users\jegom\shorts_project"
BRAIN_DIR = r"C:\Users\jegom\.gemini\antigravity-cli\brain\b440111e-f299-42bc-bfbd-181f6ef4fb00"
ASSET_MAP_PATH = os.path.join(BASE_DIR, "campaign_assets_map.json")

with open(ASSET_MAP_PATH, "r", encoding="utf-8") as f:
    asset_map = json.load(f)

# Campaign 6: propiedad_short_1..13
for i in range(1, 14):
    sid = f"propiedad_short_{i}"
    pattern = os.path.join(BRAIN_DIR, f"propiedad_{i}_photo1_*.jpg")
    matches = glob.glob(pattern)
    if matches:
        matches.sort(key=os.path.getmtime, reverse=True)
        asset_map[sid] = [matches[0]]
        print(f"Mapped {sid} -> {os.path.basename(matches[0])}")
    else:
        print(f"WARNING: No image found for {sid}")

# Campaign 7: estafa_anime_short_1..8
for i in range(1, 9):
    sid = f"estafa_anime_short_{i}"
    pattern = os.path.join(BRAIN_DIR, f"estafa_anime_{i}_photo1_*.jpg")
    matches = glob.glob(pattern)
    if matches:
        matches.sort(key=os.path.getmtime, reverse=True)
        asset_map[sid] = [matches[0]]
        print(f"Mapped {sid} -> {os.path.basename(matches[0])}")
    else:
        print(f"WARNING: No image found for {sid}")

with open(ASSET_MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(asset_map, f, ensure_ascii=False, indent=2)

print("\n[SUCCESS] Asset map updated for Campaigns 6 & 7!")
