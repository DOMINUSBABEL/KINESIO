import os
import sys
import json

# Ensure UTF-8 console output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
MANIFEST_FILE = os.path.join(BASE_DIR, "master_39_shorts_manifest.json")
MUSIC_DIR = os.path.join(BASE_DIR, "music")

def verify_production_readiness():
    print("==================================================================")
    print("VERIFICACIÓN MAESTRA DE PRODUCCIÓN: 39 SHORTS (DOMINUSBABEL @dominus8735)")
    print("==================================================================")
    
    if not os.path.exists(MANIFEST_FILE):
        print(f"[ERROR] Manifiesto no encontrado: {MANIFEST_FILE}")
        return False
        
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    total_audios = 0
    missing_audios = []
    missing_music = []
    
    for campaign in data.get("campaigns", []):
        print(f"\n📂 Campaña: {campaign['name']} ({campaign['count']} Shorts)")
        for s in campaign.get("shorts", []):
            audio_path = os.path.join(BASE_DIR, s["audio"])
            music_path = os.path.join(BASE_DIR, s["music"])
            
            audio_ok = os.path.exists(audio_path) and os.path.getsize(audio_path) > 0
            music_ok = os.path.exists(music_path) and os.path.getsize(music_path) > 0
            
            if audio_ok:
                total_audios += 1
                size_kb = os.path.getsize(audio_path) / 1024
                status = f"✅ Audio OK ({size_kb:.1f} KB)"
            else:
                missing_audios.append(s["audio"])
                status = f"❌ Audio Faltante"
                
            music_status = "✅ Música OK" if music_ok else "❌ Música Faltante"
            if not music_ok:
                missing_music.append(s["music"])
                
            print(f"  • {s['id']} [{s['duration']}]: {s['title'][:45]}... | {status} | {music_status}")

    print("\n------------------------------------------------------------------")
    print(f"RESUMEN DE AUDIOS: {total_audios}/39 sintetizados con éxito.")
    if missing_audios:
        print(f"[ALERTA] Audios faltantes: {len(missing_audios)}")
    if missing_music:
        print(f"[ALERTA] Pistas musicales faltantes: {len(missing_music)}")
        
    if not missing_audios and not missing_music:
        print("\n🚀 ¡TODO EL PIPELINE ESTÁ 100% LISTO PARA MONTAJE Y COMPILACIÓN DE LOS 39 SHORTS!")
    return True

if __name__ == "__main__":
    verify_production_readiness()
