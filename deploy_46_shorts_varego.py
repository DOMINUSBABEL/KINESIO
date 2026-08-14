# -*- coding: utf-8 -*-
r"""
VAREGO MASTER DEPLOYMENT CONTROLLER (DOMINUSBABEL @dominus8735)
Orchestrates automated publishing of the 46 Master Shorts to YouTube Studio
Using persistent session in C:\Users\jegom\VAREGO\browser_profile\youtube_shorts_profile
"""

import os
import sys
import json
import time
import subprocess
import argparse

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
VAREGO_DIR = r"C:\Users\jegom\VAREGO"
MANIFEST_FILE = os.path.join(BASE_DIR, "master_46_shorts_manifest.json")
VIDEOS_DIR = os.path.join(BASE_DIR, "final_rendered_46_shorts")
LOG_FILE = os.path.join(BASE_DIR, "varego_upload_history.json")

AUTH_SCRIPT = os.path.join(VAREGO_DIR, "open_auth_browser.js")
UPLOADER_SCRIPT = os.path.join(VAREGO_DIR, "upload_youtube_dominus.js")

def load_history():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_history(history):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

def open_auth_session():
    print("==================================================================")
    print("VAREGO • DESPLEGANDO VENTANA DE LOGIN DE YOUTUBE STUDIO")
    print("Canal: DOMINUSBABEL (@dominus8735)")
    print("==================================================================")
    print("Iniciando navegador Chrome con perfil persistente...")
    subprocess.run(["node", AUTH_SCRIPT], cwd=VAREGO_DIR)

def upload_short(short_item, schedule_hours=0, draft=False):
    short_id = short_item["id"]
    video_path = os.path.join(VIDEOS_DIR, f"{short_id}_final.mp4")
    
    if not os.path.exists(video_path):
        print(f"❌ [ERROR] El archivo de video no existe: {video_path}")
        return False
        
    title = short_item["title"]
    block = short_item.get("block", "DOMINUSBABEL")
    
    # Generate SEO Description & Pinned Comment
    desc = f"{title}\n\nAnálisis y estrategia por DOMINUSBABEL (@dominus8735).\nBloque: {block}\n\n#shorts #historia #estrategia #dominus #viral #gaming"
    
    cmd = [
        "node", UPLOADER_SCRIPT,
        "--file", video_path,
        "--title", title,
        "--desc", desc,
        "--is_short"
    ]
    
    if schedule_hours > 0:
        cmd.extend(["--schedule", str(schedule_hours)])
    if draft:
        cmd.append("--draft")
        
    print(f"\n🚀 [VAREGO] Subiendo: {short_id} ({title})...")
    res = subprocess.run(cmd, cwd=VAREGO_DIR)
    
    if res.returncode == 0:
        history = load_history()
        history[short_id] = {
            "title": title,
            "file": video_path,
            "uploaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "schedule_hours": schedule_hours,
            "status": "DRAFT" if draft else "SCHEDULED"
        }
        save_history(history)
        print(f"✅ [SUCCESS] {short_id} procesado con éxito en YouTube Studio.")
        return True
    else:
        print(f"❌ [FAILED] Error al subir {short_id} (Código: {res.returncode})")
        return False

def list_status():
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    history = load_history()
    all_shorts = []
    for c in data.get("campaigns", []):
        for s in c.get("shorts", []):
            all_shorts.append(s)
            
    print("==================================================================")
    print("ESTADO DEL CATÁLOGO EN VAREGO: 46 SHORTS (@dominus8735)")
    print("==================================================================")
    
    ready_count = 0
    uploaded_count = 0
    
    for idx, s in enumerate(all_shorts, 1):
        short_id = s["id"]
        v_path = os.path.join(VIDEOS_DIR, f"{short_id}_final.mp4")
        is_ready = os.path.exists(v_path)
        is_uploaded = short_id in history
        
        if is_ready:
            ready_count += 1
        if is_uploaded:
            uploaded_count += 1
            
        status = "🚀 PUBLICADO" if is_uploaded else ("✅ LISTO PARA SUBIR" if is_ready else "❌ FALTA MP4")
        print(f"[{idx:02d}/46] {short_id} -> {status} | {s['title'][:40]}...")
        
    print("------------------------------------------------------------------")
    print(f"Total Listos en Disco: {ready_count}/46 | Total Procesados en YouTube: {uploaded_count}/46")
    print("==================================================================")

def main():
    parser = argparse.ArgumentParser(description="VAREGO Master YouTube Uploader")
    parser.add_argument("--auth", action="store_true", help="Abrir ventana para iniciar sesión en YouTube Studio")
    parser.add_argument("--status", action="store_true", help="Ver estado de los 46 shorts")
    parser.add_argument("--upload-all", action="store_true", help="Subir todos los shorts programándolos cada 4 horas")
    parser.add_argument("--upload-single", type=str, help="Subir un short específico por su ID")
    parser.add_argument("--draft", action="store_true", help="Guardar como borrador en vez de publicar")
    
    args = parser.parse_args()
    
    if args.auth:
        open_auth_session()
    elif args.status:
        list_status()
    elif args.upload_single:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        target = None
        for c in data.get("campaigns", []):
            for s in c.get("shorts", []):
                if s["id"] == args.upload_single:
                    target = s
                    break
        if target:
            upload_short(target, draft=args.draft)
        else:
            print(f"❌ Short no encontrado: {args.upload_single}")
    elif args.upload_all:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        history = load_history()
        offset = 4
        for c in data.get("campaigns", []):
            for s in c.get("shorts", []):
                if s["id"] not in history:
                    upload_short(s, schedule_hours=offset, draft=args.draft)
                    offset += 4
                    time.sleep(3)
    else:
        list_status()

if __name__ == "__main__":
    main()
