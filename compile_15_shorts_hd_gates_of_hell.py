import os
import subprocess
import time

PROJECT_DIR = r"C:\Users\jegom\shorts_project"
MUSIC_DIR = os.path.join(PROJECT_DIR, "music")
VIDEO_SOURCE_HD = os.path.join(PROJECT_DIR, "gameplay_720p.mp4")
AUDIO_SOURCE = os.path.join(PROJECT_DIR, "gameplay_audio.webm")

SHORTS_SPEC = [
    {
        "id": 1,
        "start": "00:01:15",
        "to": "00:01:45",
        "music": "Clash Defiant.mp3",
        "title": "Contacto Inicial en el Bosque"
    },
    {
        "id": 2,
        "start": "00:03:40",
        "to": "00:04:10",
        "music": "Severe Tire Damage.mp3",
        "title": "Impacto Directo de Mortero"
    },
    {
        "id": 3,
        "start": "00:06:20",
        "to": "00:07:00",
        "music": "Volatile Reaction.mp3",
        "title": "Emboscada PaK 36 vs T-26"
    },
    {
        "id": 4,
        "start": "00:09:10",
        "to": "00:09:50",
        "music": "Severe Tire Damage.mp3",
        "title": "Sniper Sissit en Control Directo"
    },
    {
        "id": 5,
        "start": "00:12:30",
        "to": "00:13:20",
        "music": "Volatile Reaction.mp3",
        "title": "Defensa de Trinchera contra T-34"
    },
    {
        "id": 6,
        "start": "00:16:00",
        "to": "00:16:30",
        "music": "Clash Defiant.mp3",
        "title": "Inmovilizacion de Oruga"
    },
    {
        "id": 7,
        "start": "00:19:15",
        "to": "00:19:45",
        "music": "Severe Tire Damage.mp3",
        "title": "Limpieza de Trinchera Suomi KP-31"
    },
    {
        "id": 8,
        "start": "00:23:00",
        "to": "00:23:40",
        "music": "Clash Defiant.mp3",
        "title": "Raid con Auto-blindado BA-10"
    },
    {
        "id": 9,
        "start": "00:27:10",
        "to": "00:28:00",
        "music": "Volatile Reaction.mp3",
        "title": "Enfrentamiento contra Tanque Pesado KV-1"
    },
    {
        "id": 10,
        "start": "00:31:30",
        "to": "00:32:10",
        "music": "Clash Defiant.mp3",
        "title": "Saqueo de Municion Bajo Fuego"
    },
    {
        "id": 11,
        "start": "00:35:00",
        "to": "00:35:40",
        "music": "Volatile Reaction.mp3",
        "title": "Contrabateria de Artilleria"
    },
    {
        "id": 12,
        "start": "00:39:20",
        "to": "00:39:50",
        "music": "Severe Tire Damage.mp3",
        "title": "Emboscada Sigilosa en la Nieve"
    },
    {
        "id": 13,
        "start": "00:43:00",
        "to": "00:43:40",
        "music": "Severe Tire Damage.mp3",
        "title": "Bloqueo y Voladura de Convoy en Puente"
    },
    {
        "id": 14,
        "start": "00:47:10",
        "to": "00:47:50",
        "music": "Clash Defiant.mp3",
        "title": "Robo de Tanque Ruso y Tiro a Quemarropa"
    },
    {
        "id": 15,
        "start": "00:51:00",
        "to": "00:51:50",
        "music": "Volatile Reaction.mp3",
        "title": "Carga Final por la Victoria"
    }
]

def render_short_hd(spec):
    output_filename = f"gates_of_hell_short_{spec['id']}_final.mp4"
    output_path = os.path.join(PROJECT_DIR, output_filename)
    
    print(f"\n[+] Renderizando Short HD {spec['id']}: {spec['title']} ({spec['start']} -> {spec['to']})")
    
    music_file = os.path.join(MUSIC_DIR, spec['music'])
    
    # Filtro de video: Recorte vertical a 1080x1920, nitidez y mejor escalado
    video_filter = "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,unsharp=5:5:0.8:5:5:0.0[v]"
    filter_complex = f"{video_filter};[1:a]volume=1.0[a1];[2:a]volume=0.07[a2];[a1][a2]amix=inputs=2:duration=first[a]"
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", spec['start'], "-to", spec['to'], "-i", VIDEO_SOURCE_HD,
        "-ss", spec['start'], "-to", spec['to'], "-i", AUDIO_SOURCE,
        "-i", music_file,
        "-filter_complex", filter_complex,
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-r", "60",
        "-c:a", "aac", "-b:a", "192000",
        output_path
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"    [OK] Short HD {spec['id']} Generado: {output_filename} ({size_mb:.2f} MB)")
        return True
    else:
        print(f"    [ERROR] Fallo al renderizar Short HD {spec['id']}: {res.stderr[:200] if res.stderr else 'Error desconocido'}")
        return False

def main():
    print("=================================================================")
    print("Iniciando Renderizado HD Nítido de los 15 YouTube Shorts (9:16)")
    print("=================================================================")
    
    while not os.path.exists(VIDEO_SOURCE_HD):
        print("Esperando la descarga del archivo fuente HD (gameplay_720p.mp4)...")
        time.sleep(5)
        
    success = 0
    for spec in SHORTS_SPEC:
        if render_short_hd(spec):
            success += 1
            
    print(f"\n================================================ metaphysics ==")
    print(f"RESULTADO HD: {success} de {len(SHORTS_SPEC)} Shorts HD exportados.")
    print(f"Ubicacion de exportacion: {PROJECT_DIR}")
    print("================================================================")

if __name__ == "__main__":
    main()
