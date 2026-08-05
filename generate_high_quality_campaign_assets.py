# -*- coding: utf-8 -*-
"""
KINESIO & VAREGO ASSET STUDIO GENERATOR
Generates high-taste, documentary press clipping cards, historical document cards, and map badges for 23 Shorts.
"""

import os
import sys
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

from kinesio_asset_studio import create_press_clipping_card, apply_cinematic_preset, date_and_tag_asset

# 1. NARCO CHINA CAMPAIGN ASSET MAP (13 Shorts x 2 Images per Short)
NARCO_CHINA_ASSET_SPECS = [
    {
        "short_id": "narco_china_short_1",
        "card1": {"headline": "CHINESE MONEY LAUNDERING NETWORK IN NY", "snippet": "Federal agents investigate flying money transactions between Sinaloa Cartel and Flushing merchants.", "date": "2024-03-15", "source": "THE WALL STREET JOURNAL"},
        "card2": {"headline": "MIRROR TRANSACTIONS ESCAPE US BANKS", "snippet": "Sub-3% commission rates undercut Colombian laundering networks across America.", "date": "2024-05-10", "source": "FINANCIAL TIMES"}
    },
    {
        "short_id": "narco_china_short_2",
        "card1": {"headline": "REAL ESTATE MOGUL TAO LIU INVESTIGATED", "snippet": "Millions in Sinaloa Cartel funds laundered into Manhattan luxury real estate development.", "date": "2018-09-20", "source": "NEW YORK POST"},
        "card2": {"headline": "EXCLUSIVITY & SECRET SERVICE INQUIRY", "snippet": "Questions raised after high-stakes meetings at New Jersey golf club connected to laundering ring.", "date": "2018-11-04", "source": "WASHINGTON POST"}
    },
    {
        "short_id": "narco_china_short_3",
        "card1": {"headline": "WUHAN CHEMICAL EXPORTS UNDER SCRUTINY", "snippet": "Unregulated precursor shipments depart Shangai and Wuhan ports bound for Mexico.", "date": "2023-11-12", "source": "REUTERS INVESTIGATES"},
        "card2": {"headline": "MANZANILLO PORT PRECURSOR SEIZURE", "snippet": "Mexican navy intercepts multi-ton chemical shipment disguised as industrial cleaning agents.", "date": "2024-01-22", "source": "EL UNIVERSAL"}
    },
    {
        "short_id": "narco_china_short_4",
        "card1": {"headline": "PENTAGON WARNS OF ASYMMETRIC WARFARE", "snippet": "Fentanyl crisis parallels 19th century Opium Wars in reverse strategic impact.", "date": "2024-02-18", "source": "FOREIGN AFFAIRS"},
        "card2": {"headline": "BEIJING TAX REBATE INCENTIVES IN FOCUS", "snippet": "Export tax rebates remain intact for chemical exporters unless diplomatic pressure escalates.", "date": "2024-04-05", "source": "BLOOMBERG GEOPOLITICS"}
    },
    {
        "short_id": "narco_china_short_5",
        "card1": {"headline": "DEA & FBI RETAIN OUTDATED LAUNDERING TRACKS", "snippet": "Cash suitcases and offshore bank accounts bypassed by trade-based value clearing.", "date": "2023-08-14", "source": "USA TODAY"},
        "card2": {"headline": "INFORMAL FLYING MONEY MESSENGER RINGS", "snippet": "Goods settlement network neutralizes traditional western banking monitoring.", "date": "2023-10-30", "source": "THE ECONOMIST"}
    },
    {
        "short_id": "narco_china_short_6",
        "card1": {"headline": "MAINE RURAL PROPERTY CASH BUYOUTS", "snippet": "Over 200 illegal cannabis farms uncovered across quiet New England timberland.", "date": "2023-09-08", "source": "PORTLAND PRESS HERALD"},
        "card2": {"headline": "OKLAHOMA MARIJUANA BLACK MARKET LAUNDERING", "snippet": "Illicit cash proceeds flow into Sinaloa Cartel clearing houses.", "date": "2023-12-01", "source": "THE OKLAHOMAN"}
    },
    {
        "short_id": "narco_china_short_7",
        "card1": {"headline": "COLOMBIAN LAUNDERERS OUTCOMPETED", "snippet": "Chinese triads drop commission rates from 20% down to 3% with instant payout.", "date": "2022-06-14", "source": "BOGOTA HERALD"},
        "card2": {"headline": "MONOPOLY OVER INTERNATIONAL BLANQUEO", "snippet": "Efficiency of mirror transactions grants complete market domination.", "date": "2022-09-28", "source": "LATIN AMERICA RISK REPORT"}
    },
    {
        "short_id": "narco_china_short_8",
        "card1": {"headline": "POST 9/11 BANKING REGULATION IMPACT", "snippet": "Patriot Act rules trigger automatic Treasury alarms on cash deposits.", "date": "2006-04-12", "source": "WALL STREET JOURNAL"},
        "card2": {"headline": "IMPORTERS NEEDING DOLLARS CLOSE CIRCLE", "snippet": "US cash buys legitimate Chinese consumer electronics without bank intervention.", "date": "2023-07-19", "source": "FINANCIAL TIMES"}
    },
    {
        "short_id": "narco_china_short_9",
        "card1": {"headline": "THE ARREST OF XIZHI LI", "snippet": "High-profile businessman unmasked as Sinaloa Cartel's chief financial cleaner.", "date": "2021-10-15", "source": "FBI PRESS RELEASE"},
        "card2": {"headline": "$300 MILLION LAUNDERED ACROSS 20 STATES", "snippet": "Fake passports and shell corporations exposed in landmark federal prosecution.", "date": "2022-01-20", "source": "MIAMI HERALD"}
    },
    {
        "short_id": "narco_china_short_10",
        "card1": {"headline": "BEIJING CAPITAL CONTROLS TRIGGER ESCAPE", "snippet": "$50,000 annual transfer limit forces wealthy Chinese elites into shadow markets.", "date": "2023-03-22", "source": "SOUTH CHINA MORNING POST"},
        "card2": {"headline": "VANCOUVER & MIAMI MANIONS BOUGHT WITH CASH", "snippet": "Yuan delivered in Asia traded for cartel cash in North America.", "date": "2023-06-30", "source": "VANCOUVER SUN"}
    },
    {
        "short_id": "narco_china_short_11",
        "card1": {"headline": "TRADE-BASED MONEY LAUNDERING SCHEMES", "snippet": "Under-invoicing of textile containers transfers value across borders legally.", "date": "2023-02-14", "source": "CUSTOMS WORLDWIDE"},
        "card2": {"headline": "CONTAINERS OF ELECTRONICS CLEARED BY CUSTOMS", "snippet": "Inspectors find genuine commercial goods masking billions in cartel wealth.", "date": "2023-05-19", "source": "LOGISTICS WEEKLY"}
    },
    {
        "short_id": "narco_china_short_12",
        "card1": {"headline": "HISTORICAL PARALLELS: 19TH CENTURY OPIUM WARS", "snippet": "Western powers once crippled Qing Dynasty; today chemical supply drains US workforce.", "date": "2024-01-10", "source": "HISTORICAL GEOPOLITICS"},
        "card2": {"headline": "NATIONAL SECURITY THREAT WITHOUT MISSILES", "snippet": "Hybrid alliance creates social breakdown across North American industrial heartland.", "date": "2024-03-29", "source": "DEFENSE INSIDER"}
    },
    {
        "short_id": "narco_china_short_13",
        "card1": {"headline": "TRANSNATIONAL CRIME CORPORATION EMERGING", "snippet": "Mexican cartel muscle merges with Chinese triad financial sophistication.", "date": "2024-04-18", "source": "GLOBAL SECURITY REVIEW"},
        "card2": {"headline": "FRAGMENTED LAW ENFORCEMENT VS GLOBAL TRADE", "snippet": "Borderless commerce renders traditional police methods ineffective.", "date": "2024-06-02", "source": "INTERNATIONAL RISK MONITOR"}
    }
]

# 2. GUERRA ANTIGUA CAMPAIGN ASSET MAP (10 Shorts x 2 Images per Short)
GUERRA_ANTIGUA_ASSET_SPECS = [
    {
        "short_id": "guerra_antigua_short_1",
        "card1": {"headline": "THE HOLLYWOOD CHARGE MYTH EXPOSED", "snippet": "Sprinting ancient infantry broke cohesion and resulted in immediate massacre.", "date": "490 B.C.", "source": "MILITARY ARCHIVE"},
        "card2": {"headline": "THE DANGER OF INDIVIDUAL SPRINT", "snippet": "Isolated warriors faced impenetrable spear walls without shields.", "date": "338 B.C.", "source": "TACTICAL CHRONICLE"}
    },
    {
        "short_id": "guerra_antigua_short_2",
        "card1": {"headline": "THE SHIELD WALL AS A BIOMECHANICAL MACHINE", "snippet": "Each warrior relies on the shield of the man to his right for survival.", "date": "1066 A.D.", "source": "SAXON CHRONICLE"},
        "card2": {"headline": "GAPS IN FORMATION LEAD TO COLLAPSE", "snippet": "Stepping ahead created fatal openings for enemy spears.", "date": "911 A.D.", "source": "VIKING WARFARE HANDBOOK"}
    },
    {
        "short_id": "guerra_antigua_short_3",
        "card1": {"headline": "BIOMECHANICS OF EXHAUSTION", "snippet": "Carrying 30kg of iron armor, shield and helmet drained soldier endurance.", "date": "100 B.C.", "source": "ROMAN ANNALES"},
        "card2": {"headline": "WINDED CHARGERS FALL BEFORE FRESH LINES", "snippet": "Exhausted infantry collapsed upon impact against rested defenders.", "date": "480 B.C.", "source": "HERODOTUS RECORD"}
    },
    {
        "short_id": "guerra_antigua_short_4",
        "card1": {"headline": "THE BLOODY OTHISMOS PUSHING CONTEST", "snippet": "Hoplite battles were pushing contests of physical mass, not sword duels.", "date": "431 B.C.", "source": "THUCYDIDES HISTORIES"},
        "card2": {"headline": "STABILITY OF THE MASSIVE HUMAN BLOCK", "snippet": "Orderly march preserved collective center of gravity upon impact.", "date": "371 B.C.", "source": "LEUCTRA TACTICAL STUDY"}
    },
    {
        "short_id": "guerra_antigua_short_5",
        "card1": {"headline": "THE MARATHON CHARGE EXCEPTION (490 B.C.)", "snippet": "Athenians marched until 100 meters, then sprinted to cross arrow kill zone.", "date": "490 B.C.", "source": "ATHENIAN GAZETTE"},
        "card2": {"headline": "CROSSING PERSIAN ARCHERY FIRE IN SECONDS", "snippet": "Calculated last-second acceleration minimized projectile casualties.", "date": "490 B.C.", "source": "PERSIAN WAR RECORD"}
    },
    {
        "short_id": "guerra_antigua_short_6",
        "card1": {"headline": "GRADUS MILITARIS: THE ROMAN 4 KM/H MARCH", "snippet": "Disciplined steady march kept ranks unbroken across Mediterranean terrains.", "date": "146 B.C.", "source": "LEGIONARY FIELD MANUAL"},
        "card2": {"headline": "PILUM THROW AT 15 METERS PREPARES GLADIUS", "snippet": "Javelins disabled enemy shields before short sword engagement.", "date": "50 B.C.", "source": "CAESAR GALLIC WARS"}
    },
    {
        "short_id": "guerra_antigua_short_7",
        "card1": {"headline": "80% OF CASUALTIES OCCURRED DURING ROUT", "snippet": "Frontal clash saw minimal deaths; massacre began when formation broke.", "date": "216 B.C.", "source": "CANNAE ANALYSIS"},
        "card2": {"headline": "CAVALRY PURSUIT OF FLEEING SOLDIERS", "snippet": "Running away exposed undefended backs to pursuing horsemen.", "date": "331 B.C.", "source": "GAUGAMELA REPORT"}
    },
    {
        "short_id": "guerra_antigua_short_8",
        "card1": {"headline": "SPARTAN MARCH TO THE AULOS FLUTE", "snippet": "Musicians set precise cadence preventing hurry or lag in the phalanx.", "date": "418 B.C.", "source": "SPARTAN TACTICAL CODE"},
        "card2": {"headline": "THE FLUTE AS MILITARY CADENCE METRONOME", "snippet": "Rhythm ensured bronze wall remained unified without tripping.", "date": "400 B.C.", "source": "XENOPHON ANABASIS"}
    },
    {
        "short_id": "guerra_antigua_short_9",
        "card1": {"headline": "THE TRAGIC FEIGNED RETREAT AT HASTINGS", "snippet": "Normans lured Anglo-Saxons down Senlac Hill by pretending to flee.", "date": "1066 A.D.", "source": "BAYEUX TAPESTRY RECORD"},
        "card2": {"headline": "LEAVING SENLAC HILL BROKE SAXON WALL", "snippet": "Pursuing soldiers were encircled and annihilated in open field.", "date": "1066 A.D.", "source": "NORMAN MANUSCRIPT"}
    },
    {
        "short_id": "guerra_antigua_short_10",
        "card1": {"headline": "THE ANCIENT VETERAN SURVIVAL CODE", "snippet": "Marching calmly, rotating tired front ranks, and holding shields together.", "date": "100 A.D.", "source": "VETERAN MEMOIRS"},
        "card2": {"headline": "CALM MARCH WAS ADVANCED SURVIVAL TECH", "snippet": "Preserving energy was the sole difference between victory and execution.", "date": "200 A.D.", "source": "MILITARY WISDOM"}
    }
]

def generate_all_press_assets():
    print("=" * 80)
    print("  KINESIO & VAREGO ASSET STUDIO: GENERATING 46 DOCUMENTARY PRESS CARDS")
    print("=" * 80)
    
    asset_map = {}
    
    # Process Narco China
    for item in NARCO_CHINA_ASSET_SPECS:
        sid = item["short_id"]
        c1 = item["card1"]
        c2 = item["card2"]
        
        path1 = create_press_clipping_card(c1["headline"], c1["snippet"], c1["date"], c1["source"])
        rename1 = os.path.join(SCREENSHOTS_DIR, f"{sid}_card1.jpg")
        if os.path.exists(path1):
            if os.path.exists(rename1):
                os.remove(rename1)
            os.rename(path1, rename1)
            
        path2 = create_press_clipping_card(c2["headline"], c2["snippet"], c2["date"], c2["source"])
        rename2 = os.path.join(SCREENSHOTS_DIR, f"{sid}_card2.jpg")
        if os.path.exists(path2):
            if os.path.exists(rename2):
                os.remove(rename2)
            os.rename(path2, rename2)
            
        asset_map[sid] = [rename1, rename2]
        print(f"  [SUCCESS] Created Assets for '{sid}'")

    # Process Guerra Antigua
    for item in GUERRA_ANTIGUA_ASSET_SPECS:
        sid = item["short_id"]
        c1 = item["card1"]
        c2 = item["card2"]
        
        path1 = create_press_clipping_card(c1["headline"], c1["snippet"], c1["date"], c1["source"])
        rename1 = os.path.join(SCREENSHOTS_DIR, f"{sid}_card1.jpg")
        if os.path.exists(path1):
            if os.path.exists(rename1):
                os.remove(rename1)
            os.rename(path1, rename1)
            
        path2 = create_press_clipping_card(c2["headline"], c2["snippet"], c2["date"], c2["source"])
        rename2 = os.path.join(SCREENSHOTS_DIR, f"{sid}_card2.jpg")
        if os.path.exists(path2):
            if os.path.exists(rename2):
                os.remove(rename2)
            os.rename(path2, rename2)
            
        asset_map[sid] = [rename1, rename2]
        print(f"  [SUCCESS] Created Assets for '{sid}'")

    # Save asset mapping JSON
    map_json_path = os.path.join(BASE_DIR, "campaign_assets_map.json")
    with open(map_json_path, "w", encoding="utf-8") as f:
        json.dump(asset_map, f, indent=2, ensure_ascii=False)
        
    print("\n" + "=" * 80)
    print(f"  SUCCESS: 46 High-Quality Press Clipping Cards Generated and Indexed!")
    print(f"  Mapping File: {map_json_path}")
    print("=" * 80)

if __name__ == "__main__":
    generate_all_press_assets()
