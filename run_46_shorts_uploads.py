import os
import sys
import json
import time
import subprocess

# Ensure UTF-8 console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
MANIFEST_FILE = os.path.join(PROJECT_DIR, "master_46_shorts_manifest.json")
RENDER_DIR = os.path.join(PROJECT_DIR, "final_rendered_46_shorts")
UPLOAD_LOG = os.path.join(PROJECT_DIR, "uploaded_46_shorts_log.json")
UPLOADER_SCRIPT = r"C:\Users\jegom\VAREGO\upload_youtube_dominus.js"

def load_upload_history():
    if os.path.exists(UPLOAD_LOG):
        try:
            with open(UPLOAD_LOG, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_upload_history(history):
    with open(UPLOAD_LOG, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def main():
    print("==================================================================")
    print("ORQUESTADOR DE SUBIDAS Y PROGRAMACIÓN: 46 SHORTS (@dominus8735)")
    print("Canal: DOMINUSBABEL | Espaciado: 4-6 Horas (Evitar Sandbox Penalty)")
    print("==================================================================")
    
    if not os.path.exists(MANIFEST_FILE):
        print(f"[ERROR] Manifiesto no encontrado: {MANIFEST_FILE}")
        sys.exit(1)
        
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    history = load_upload_history()
    
    all_shorts = []
    for c in data.get("campaigns", []):
        for s in c.get("shorts", []):
            s["campaign_name"] = c["name"]
            all_shorts.append(s)
            
    print(f"\nTotal de Shorts en catálogo: {len(all_shorts)}")
    ready_count = 0
    uploaded_count = 0
    
    for idx, s in enumerate(all_shorts, 1):
        short_id = s["id"]
        video_path = os.path.join(RENDER_DIR, f"{short_id}_final.mp4")
        is_rendered = os.path.exists(video_path) and os.path.getsize(video_path) > 0
        is_uploaded = short_id in history
        
        status = "⏳ RENDERIZANDO..."
        if is_rendered:
            ready_count += 1
            status = "✅ LISTO PARA SUBIR"
        if is_uploaded:
            uploaded_count += 1
            status = f"🚀 PUBLICADO ({history[short_id].get('date', 'OK')})"
            
        print(f"[{idx:02d}/46] {short_id} -> {status} | {s['title'][:45]}...")
        
    print("\n------------------------------------------------------------------")
    print(f"RESUMEN OPERATIVO: {ready_count}/46 Renderizados | {uploaded_count}/46 Publicados")
    print("------------------------------------------------------------------")

if __name__ == "__main__":
    main()
