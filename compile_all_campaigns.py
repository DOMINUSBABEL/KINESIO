# -*- coding: utf-8 -*-
"""
KINESIO MASTER COMPILER V5.5.0: CAMPAIGN MIKE EHRMANTRAUT (16 SHORTS)
Includes Two 3-Part Miniseries with Floating Series Badges, Tri-Tone Kinetic Subtitles (#FAC815 / #FF4D4D / #00E5FF),
Multi-Asset B-Roll Ken Burns Rotation, and Sidechain Audio Ducking (-24dB).
"""

import os
import glob
from kinesio_core import KinesioVideoBuilder, get_audio_duration, log_info

PROJECT_DIR = r"C:\Users\jegom\shorts_project"

def find_asset(pattern):
    matches = glob.glob(os.path.join(PROJECT_DIR, f"*{pattern}*"))
    if matches:
        return matches[0]
    return os.path.join(PROJECT_DIR, "mike_ehrmantraut_portrait_1785110278647.jpg")

def compile_mike_ehrmantraut_campaign():
    log_info("=== COMPILING CAMPAIGN: MIKE EHRMANTRAUT (16 SHORTS WITH 2 TRILOGIES) ===")
    
    # Custom AI Artworks for Mike Ehrmantraut Campaign
    mike_portrait = find_asset("mike_ehrmantraut_portrait")
    mike_walter = find_asset("mike_walter_standoff")
    gus_pollos = find_asset("gus_fring_pollos")
    mike_werner = find_asset("mike_werner_tragedy")
    kaylee_bag = find_asset("kaylee_money_bag")
    
    shorts_data = [
        # TRILOGÍA 1: La Caída Moral de Mike
        ("mike_short_1_final.mp4", "TRILOGIA 1 (PARTE 1/3): EL ORIGEN TRAGICO DE MIKE 🚓", "audio_mike_short_1.mp3", [mike_portrait, kaylee_bag], 42.0, "music/Rites.mp3", "TRILOGÍA 1: PARTE 1 DE 3"),
        ("mike_short_2_final.mp4", "TRILOGIA 1 (PARTE 2/3): LA VENGANZA Y ALBUQUERQUE 🏜️", "audio_mike_short_2.mp3", [mike_portrait, gus_pollos], 46.0, "music/Clash Defiant.mp3", "TRILOGÍA 1: PARTE 2 DE 3"),
        ("mike_short_3_final.mp4", "TRILOGIA 1 (PARTE 3/3): EL PACTO DE HIERRO CON GUS FRING 👑", "audio_mike_short_3.mp3", [gus_pollos, mike_portrait], 48.0, "music/Cipher2.mp3", "TRILOGÍA 1: PARTE 3 DE 3"),
        
        # TRILOGÍA 2: El Error Fatal con Walter White y Werner Ziegler
        ("mike_short_4_final.mp4", "TRILOGIA 2 (PARTE 1/3): WERNER ZIEGLER Y LA GRIETA 🏗️", "audio_mike_short_4.mp3", [mike_werner, mike_portrait], 50.0, "music/Rites.mp3", "TRILOGÍA 2: PARTE 1 DE 3"),
        ("mike_short_5_final.mp4", "TRILOGIA 2 (PARTE 2/3): LA LLEGADA DEL CAOS WALTE WHITE 🧪", "audio_mike_short_5.mp3", [mike_walter, gus_pollos], 52.0, "music/Volatile Reaction.mp3", "TRILOGÍA 2: PARTE 2 DE 3"),
        ("mike_short_6_final.mp4", "TRILOGIA 2 (PARTE 3/3): EL DISPARO FINAL EN EL RIO 🌊", "audio_mike_short_6.mp3", [mike_walter, mike_werner], 55.0, "music/Rites.mp3", "TRILOGÍA 2: PARTE 3 DE 3"),
        
        # 10 SHORTS TEMÁTICOS INDIVIDUALES
        ("mike_short_7_final.mp4", "NO MAS MEDIDAS A MEDIAS: LA REGLA DE ORO DE MIKE 📏", "audio_mike_short_7.mp3", [mike_portrait, mike_walter], 44.0, "music/Clash Defiant.mp3", None),
        ("mike_short_8_final.mp4", "POR QUE MIKE PROTEGIA TANTO A SU NIETA KAYLEE 👧", "audio_mike_short_8.mp3", [kaylee_bag, mike_portrait], 40.0, "music/Moorland.mp3", None),
        ("mike_short_9_final.mp4", "MIKE VS WALTER WHITE: LA GUERRA DE FILOSOFIAS ⚔️", "audio_mike_short_9.mp3", [mike_walter, gus_pollos], 49.0, "music/Volatile Reaction.mp3", None),
        ("mike_short_10_final.mp4", "LA RELACION DE RESPETO CON JESSE PINKMAN 🤝", "audio_mike_short_10.mp3", [mike_portrait, kaylee_bag], 47.0, "music/Take a Chance.mp3", None),
        ("mike_short_11_final.mp4", "COMO MIKE LOGRABA DESAPARECER SIN DEJAR RASTRO 🕵️‍♂️", "audio_mike_short_11.mp3", [mike_portrait, gus_pollos], 43.0, "music/Cipher2.mp3", None),
        ("mike_short_12_final.mp4", "NACHO VARGA Y EL REFLEJO EN BETTER CALL SAUL 🚘", "audio_mike_short_12.mp3", [mike_werner, mike_portrait], 46.0, "music/Rites.mp3", None),
        ("mike_short_13_final.mp4", "LA LEALTAD INQUEBRANTABLE HACIA GUS FRING 👑", "audio_mike_short_13.mp3", [gus_pollos, mike_portrait], 42.0, "music/Cipher2.mp3", None),
        ("mike_short_14_final.mp4", "SAUL GOODMAN Y MIKE: UNA ALIANZA DE NECESIDAD 💼", "audio_mike_short_14.mp3", [mike_portrait, kaylee_bag], 41.0, "music/Scheming Weasel.mp3", None),
        ("mike_short_15_final.mp4", "EL CODIGO DE HONOR DEL LIMPIADOR DEFINITIVO 🧹", "audio_mike_short_15.mp3", [mike_portrait, gus_pollos], 45.0, "music/Clash Defiant.mp3", None),
        ("mike_short_16_final.mp4", "EL LEGADO DE MIKE EHRMANTRAUT EN LA TELEVISION 📺", "audio_mike_short_16.mp3", [mike_portrait, mike_werner, kaylee_bag], 50.0, "music/Rites.mp3", None)
    ]
    
    for out_name, title, voice_f, asset_list, default_dur, music, badge in shorts_data:
        v_builder = KinesioVideoBuilder(out_name.replace(".mp4", ""), width=1080, height=1920)
        v_dur = get_audio_duration(voice_f) or default_dur
        v_builder.add_scene(title, v_dur, asset_path=asset_list, effect_type="zoom_in")
        if badge:
            v_builder.set_series_badge(badge)
        v_builder.set_background_music(music, volume=-24)
        v_builder.build(out_name, voice_audio_path=voice_f)

def main():
    os.chdir(PROJECT_DIR)
    print("==================================================")
    print("  KINESIO MASTER COMPILER: MIKE EHRMANTRAUT SHORTS")
    print("==================================================")
    compile_mike_ehrmantraut_campaign()
    print("\n[ALL SUCCESS] All 16 Shorts compiled with floating series badges & tri-tone subtitles!")

if __name__ == "__main__":
    main()
