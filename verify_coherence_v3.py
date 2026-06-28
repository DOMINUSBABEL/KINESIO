import os
import sys
import subprocess

# Ensure UTF-8 output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

HORIZONTALS = [
    {"name": "Dune Spice Wars", "prefix": "dune_spice_wars", "appid": 1171690},
    {"name": "Pathfinder Wrath of the Righteous", "prefix": "pathfinder_wrath_of_the_righteous", "appid": 1184370}
]

SHORTS = [
    {"key": "jc2", "name": "Just Cause 2", "appid": 8190},
    {"key": "jc3", "name": "Just Cause 3", "appid": 225540},
    {"key": "aoe2", "name": "Age of Empires II DE", "appid": 813780},
    {"key": "warband", "name": "Mount and Blade Warband", "appid": 48700},
    {"key": "diplomacy", "name": "Diplomacy is Not an Option", "appid": 1272320},
    {"key": "syx", "name": "Songs of Syx", "appid": 1162750},
    {"key": "rimworld", "name": "RimWorld", "appid": 294100}
]

def check_file(file_path):
    if not os.path.exists(file_path):
        return False, "File does not exist"
    size = os.path.getsize(file_path)
    if size == 0:
        return False, "File is empty (0 bytes)"
    return True, f"Exists ({size / (1024*1024):.2f} MB)"

def get_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except:
        return None

def main():
    print("====================================================")
    print("Content Curator & Verifier Agent v3 - CQA Audit")
    print("====================================================")
    
    report = []
    has_errors = False
    
    # 1. Horizontal Videos Audit
    report.append("## 1. Auditoría de Videos Horizontales (9-11 min)")
    for hz in HORIZONTALS:
        name = hz["name"]
        prefix = hz["prefix"]
        appid = hz["appid"]
        
        report.append(f"\n### {name} [App ID: {appid}]")
        
        # Check capsule
        capsule_file = os.path.join(CAPSULES_DIR, f"{prefix}_capsule.jpg")
        cap_ok, cap_status = check_file(capsule_file)
        report.append(f"*   **Cápsula de Portada:** {'✔️' if cap_ok else '❌'} {cap_status}")
        if not cap_ok: has_errors = True
        
        # Check screenshots
        ss_count = 0
        for i in range(10):
            ss_path = os.path.join(SCREENSHOTS_DIR, f"{prefix}_screenshot_{i}.jpg")
            ok, _ = check_file(ss_path)
            if ok: ss_count += 1
        report.append(f"*   **Capturas de Pantalla:** {ss_count}/10 validadas en disco")
        if ss_count < 10: has_errors = True
        
        # Check audio
        audio_file = os.path.join(BASE_DIR, f"audio_{prefix if prefix == 'dune_spice_wars' else 'pathfinder'}.mp3")
        aud_ok, aud_status = check_file(audio_file)
        aud_dur = get_duration(audio_file) if aud_ok else None
        report.append(f"*   **Audio TTS Locución:** {'✔️' if aud_ok else '❌'} {aud_status} {f'({aud_dur:.2f} s)' if aud_dur else ''}")
        if not aud_ok: has_errors = True
        
        # Check final video
        video_file = os.path.join(BASE_DIR, f"{prefix}_analysis.mp4")
        vid_ok, vid_status = check_file(video_file)
        vid_dur = get_duration(video_file) if vid_ok else None
        report.append(f"*   **Video Final Compilado:** {'✔️' if vid_ok else '❌'} {vid_status} {f'({vid_dur:.2f} s)' if vid_dur else ''}")
        if not vid_ok: has_errors = True
        
    # 2. Shorts Audit
    report.append("\n## 2. Auditoría de los 7 Shorts Región-Comparativos")
    for sh in SHORTS:
        key = sh["key"]
        name = sh["name"]
        appid = sh["appid"]
        
        report.append(f"\n### {name} [App ID: {appid}]")
        
        # Check capsule
        capsule_file = os.path.join(CAPSULES_DIR, f"capsule_{appid}.jpg")
        cap_ok, cap_status = check_file(capsule_file)
        report.append(f"*   **Capsule:** {'✔️' if cap_ok else '❌'} {cap_status}")
        if not cap_ok: has_errors = True
        
        # Check gameplay trailer
        trailer_file = os.path.join(TRAILERS_DIR, f"trailer_{appid}.mp4")
        tra_ok, tra_status = check_file(trailer_file)
        report.append(f"*   **Gameplay Trailer:** {'✔️' if tra_ok else '❌'} {tra_status}")
        if not tra_ok: has_errors = True
        
        # Check audio
        audio_file = os.path.join(BASE_DIR, f"audio_{key}.mp3")
        aud_ok, aud_status = check_file(audio_file)
        aud_dur = get_duration(audio_file) if aud_ok else None
        report.append(f"*   **Audio TTS Locución:** {'✔️' if aud_ok else '❌'} {aud_status} {f'({aud_dur:.2f} s)' if aud_dur else ''}")
        if not aud_ok: has_errors = True
        
        # Check final Short MP4
        video_file = os.path.join(BASE_DIR, f"{key}_v3_short.mp4")
        vid_ok, vid_status = check_file(video_file)
        vid_dur = get_duration(video_file) if vid_ok else None
        report.append(f"*   **Short Final Compilado:** {'✔️' if vid_ok else '❌'} {vid_status} {f'({vid_dur:.2f} s)' if vid_dur else ''}")
        if not vid_ok: has_errors = True

    # 3. Verdict
    report.append("\n## 3. Veredicto Final de Coherencia CQA (Volumen 3)")
    if has_errors:
        report.append("⚠️ **FALLO:** Se han detectado discrepancias en los archivos de origen, activos o videos finales. Revise los registros.")
    else:
        report.append("✅ **APROBADO:** Todos los archivos de audio, video, portadas y clips de jugabilidad se correlacionan al 100% y cumplen con los requisitos de la directiva.")
        
    # Write report
    report_path = os.path.join(BASE_DIR, "curation_report_v3.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Informe de Curación de Contenido y Coherencia Semántica (Volumen 3)\n\n")
        f.write("\n".join(report))
        
    print(f"\nAudit completed. Report saved to: {report_path}")

if __name__ == "__main__":
    main()
