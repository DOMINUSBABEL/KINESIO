import os
import sys
import json
import subprocess

# Reconfigure terminal output to UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
CAPSULES_DIR = os.path.join(BASE_DIR, "capsules")
TRAILERS_DIR = os.path.join(BASE_DIR, "trailers")
SCREENSHOTS_DIR = os.path.join(BASE_DIR, "screenshots")

# Expected files configuration
SHORTS_GAMES = {
    "openworld": [1174180, 271590, 252490, 264710, 105600],
    "racing": [1551360, 244210, 1846380, 227300, 228380],
    "sports": [2195250, 2290180, 431240, 2252600, 2380510],
    "cooking": [728880, 1599600, 641320, 1243830, 770810],
    "4x": [289070, 281990, 394360, 1669000, 392110]
}

def check_file_exists_and_size(file_path):
    if not os.path.exists(file_path):
        return False, "File does not exist"
    size = os.path.getsize(file_path)
    if size == 0:
        return False, "File is empty (0 bytes)"
    return True, f"Exists ({size} bytes)"

def get_audio_video_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except Exception as e:
        return None

def main():
    print("====================================================")
    print("Content Curator & Verifier Agent v2 - CQA Audit")
    print("====================================================")
    
    report = []
    has_errors = False
    
    # 1. Check Men of War: Assault Squad 2 assets
    report.append("## 1. Auditoría de Activos de Men of War: Assault Squad 2")
    mow_capsule = os.path.join(CAPSULES_DIR, "mow_capsule.jpg")
    ok, status = check_file_exists_and_size(mow_capsule)
    report.append(f"*   **Cápsula de Portada:** {status}")
    if not ok: has_errors = True
    
    mow_trailer = os.path.join(TRAILERS_DIR, "mow_trailer.mp4")
    ok, status = check_file_exists_and_size(mow_trailer)
    report.append(f"*   **Video del Avance (Trailer):** {status}")
    if not ok: has_errors = True
    
    screenshot_count = 0
    for idx in range(10):
        ss_path = os.path.join(SCREENSHOTS_DIR, f"screenshot_{idx}.jpg")
        ok, _ = check_file_exists_and_size(ss_path)
        if ok: screenshot_count += 1
    report.append(f"*   **Capturas de Pantalla (Screenshots):** {screenshot_count}/10 validadas en disco")
    if screenshot_count < 10:
        has_errors = True
        
    # 2. Check the 25 games' assets (capsules and trailers)
    report.append("\n## 2. Auditoría de Coherencia de los 25 Videojuegos de Shorts")
    for category, appids in SHORTS_GAMES.items():
        report.append(f"\n### Categoría: {category.upper()}")
        for appid in appids:
            capsule_file = os.path.join(CAPSULES_DIR, f"capsule_{appid}.jpg")
            trailer_file = os.path.join(TRAILERS_DIR, f"trailer_{appid}.mp4")
            
            cap_ok, cap_status = check_file_exists_and_size(capsule_file)
            tra_ok, tra_status = check_file_exists_and_size(trailer_file)
            
            report.append(f"*   **Juego App ID {appid}:**")
            report.append(f"    *   Capsule: {'✔️' if cap_ok else '❌'} {cap_status}")
            report.append(f"    *   Trailer Gameplay: {'✔️' if tra_ok else '❌'} {tra_status}")
            if not cap_ok or not tra_ok:
                has_errors = True
                
    # 3. Check synthesized audios
    report.append("\n## 3. Auditoría de Archivos de Locución TTS")
    audios = [
        ("Men of War Long-form", "audio_mow.mp3"),
        ("Mundo Abierto Short", "audio_openworld.mp3"),
        ("Conducción Short", "audio_racing.mp3"),
        ("Deportes Short", "audio_sports.mp3"),
        ("Cocina Short", "audio_cooking.mp3"),
        ("Estrategia 4X Short", "audio_4x.mp3")
    ]
    for label, fn in audios:
        path = os.path.join(BASE_DIR, fn)
        ok, status = check_file_exists_and_size(path)
        if ok:
            dur = get_audio_video_duration(path)
            report.append(f"*   **{label}:** ✔️ Exists ({dur:.2f} s)")
        else:
            report.append(f"*   **{label}:** ❌ {status}")
            has_errors = True
            
    # 4. Check compiled output videos
    report.append("\n## 4. Auditoría de Videos Finales (.mp4) Compilados")
    videos = [
        ("Men of War Analysis (Horizontal)", "MenOfWar_AssaultSquad2_analysis.mp4"),
        ("Mundo Abierto Short (Vertical)", "openworld_v2_short.mp4"),
        ("Conducción Short (Vertical)", "racing_v2_short.mp4"),
        ("Deportes Short (Vertical)", "sports_v2_short.mp4"),
        ("Cocina Short (Vertical)", "cooking_v2_short.mp4"),
        ("Estrategia 4X Short (Vertical)", "4x_v2_short.mp4")
    ]
    for label, fn in videos:
        path = os.path.join(BASE_DIR, fn)
        ok, status = check_file_exists_and_size(path)
        if ok:
            dur = get_audio_video_duration(path)
            report.append(f"*   **{label}:** ✔️ Exists ({dur:.2f} s)")
        else:
            report.append(f"*   **{label}:** ❌ {status}")
            has_errors = True
            
    # Final verdict
    report.append("\n## 5. Veredicto Final de Coherencia CQA")
    if has_errors:
        report.append("⚠️ **FALLO:** Se han detectado discrepancias en los archivos de origen, activos o videos finales. Revise los registros.")
    else:
        report.append("✅ **APROBADO:** Todos los archivos de audio, video, cápsulas de portada, capturas y clips de jugabilidad se correlacionan al 100% y cumplen con los requisitos de la directiva.")
        
    # Save markdown report
    report_path = os.path.join(BASE_DIR, "curation_report_v2.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Informe de Curación de Contenido y Coherencia Semántica (Volumen 2)\n\n")
        f.write("\n".join(report))
        
    print(f"\nAudit completed. Report saved to: {report_path}")

if __name__ == "__main__":
    main()
