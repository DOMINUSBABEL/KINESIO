# -*- coding: utf-8 -*-
"""
LINK REAL AI PHOTOGRAPHY TO CAMPAIGN ASSET MAP
Maps every generated AI photograph directly to campaign_assets_map.json
"""

import os
import sys
import json
import glob

BASE_DIR = r"C:\Users\jegom\shorts_project"
BRAIN_DIR = r"C:\Users\jegom\.gemini\antigravity-cli\brain\b440111e-f299-42bc-bfbd-181f6ef4fb00"
ASSET_MAP_PATH = os.path.join(BASE_DIR, "campaign_assets_map.json")

# Map of Short ID to prompt pattern in BRAIN_DIR
PHOTO_PATTERNS = {
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
    
    "guerra_antigua_short_1": "guerra_antigua_1_photo1_*.jpg",
    "guerra_antigua_short_2": "guerra_antigua_2_photo1_*.jpg",
    "guerra_antigua_short_3": "guerra_antigua_3_photo1_*.jpg",
    "guerra_antigua_short_4": "guerra_antigua_4_photo1_*.jpg",
    "guerra_antigua_short_5": "guerra_antigua_5_photo1_*.jpg",
    "guerra_antigua_short_6": "guerra_antigua_6_photo1_*.jpg",
    "guerra_antigua_short_7": "guerra_antigua_7_photo1_*.jpg",
    "guerra_antigua_short_8": "guerra_antigua_8_photo1_*.jpg",
    "guerra_antigua_short_9": "guerra_antigua_9_photo1_*.jpg",
    "guerra_antigua_short_10": "guerra_antigua_10_photo1_*.jpg"
}

with open(ASSET_MAP_PATH, "r", encoding="utf-8") as f:
    asset_map = json.load(f)

for sid, pattern in PHOTO_PATTERNS.items():
    matches = glob.glob(os.path.join(BRAIN_DIR, pattern))
    if matches:
        photo_path = matches[0]
        curr_list = asset_map.get(sid, [])
        # Put real AI photo at the start of the list
        if photo_path not in curr_list:
            curr_list.insert(0, photo_path)
        asset_map[sid] = curr_list
        print(f"Mapped Real AI Photo for '{sid}': {os.path.basename(photo_path)}")
    else:
        print(f"WARNING: No AI photo match found for '{sid}' with pattern '{pattern}'")

with open(ASSET_MAP_PATH, "w", encoding="utf-8") as f:
    json.dump(asset_map, f, indent=2, ensure_ascii=False)

print("\n[SUCCESS] Updated campaign_assets_map.json with 23 Real AI Photographic Artworks!")
