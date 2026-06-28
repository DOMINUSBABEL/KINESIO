import sys
import os
import asyncio
import re
import subprocess
import edge_tts

# Configurar la salida estándar a UTF-8 para prevenir errores de codificación en Windows
sys.stdout.reconfigure(encoding='utf-8')

VOICE = "es-MX-JorgeNeural"
BASE_DIR = r"C:\Users\jegom\shorts_project"

def extract_mow_text(filepath):
    locution_texts = []
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo del guion de Men of War: {filepath}")
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        if not line.strip().startswith('|'):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 4:
            continue
        time_col = parts[1]
        locution_col = parts[3]
        
        clean_time = time_col.replace('*', '').strip()
        if re.search(r'\d+:\d+', clean_time) and not clean_time.lower().startswith('tiempo'):
            clean_loc = locution_col.replace('<br>', ' ').replace('<br/>', ' ')
            clean_loc = re.sub(r'\s+', ' ', clean_loc).strip()
            if clean_loc:
                locution_texts.append(clean_loc)
                
    return " ".join(locution_texts)

def extract_shorts_texts(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"No se encontró el archivo de guiones de Shorts: {filepath}")
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = re.split(r'## Guion\s+\d+:', content)
    results = {}
    categories = [
        ("Mundo Abierto", "openworld"),
        ("Conducción", "racing"),
        ("Deporte", "sports"),
        ("Cocina", "cooking"),
        ("Estrategia 4X", "4x")
    ]
    
    for sect in sections[1:]:
        matched_key = None
        for title, key in categories:
            if title.lower() in sect.lower() or (key == "sports" and "deporte" in sect.lower()) or (key == "4x" and "4x" in sect.lower()):
                matched_key = key
                break
        
        if not matched_key:
            continue
            
        locution_texts = []
        lines = sect.split('\n')
        for line in lines:
            if not line.strip().startswith('|'):
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) < 4:
                continue
            time_col = parts[1]
            locution_col = parts[2]
            
            clean_time = time_col.replace('*', '').strip()
            if re.search(r'\d+:\d+', clean_time) and not clean_time.lower().startswith('tiempo'):
                clean_loc = locution_col.replace('<br>', ' ').replace('<br/>', ' ')
                clean_loc = re.sub(r'\s+', ' ', clean_loc).strip()
                if clean_loc:
                    locution_texts.append(clean_loc)
        
        results[matched_key] = " ".join(locution_texts)
        
    return results

def get_audio_duration(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Archivo de audio no encontrado: {file_path}")
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(result.stdout.strip())

async def generate_audio(text: str, output_path: str, voice: str, rate: str) -> None:
    print(f"Generando audio en: {output_path} con velocidad {rate}...")
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        duration = get_audio_duration(output_path)
        print(f"¡Éxito! Creado {output_path} | Tamaño: {os.path.getsize(output_path)} bytes | Duración: {duration:.2f} s")
    else:
        raise RuntimeError(f"Error: El archivo {output_path} no se creó o está vacío.")

async def main():
    mow_path = os.path.join(BASE_DIR, "script_mow.md")
    shorts_path = os.path.join(BASE_DIR, "scripts_shorts_v2.md")
    
    print("Extrayendo textos de locución...")
    mow_text = extract_mow_text(mow_path)
    shorts_texts = extract_shorts_texts(shorts_path)
    
    tasks = [
        generate_audio(
            mow_text,
            os.path.join(BASE_DIR, "audio_mow.mp3"),
            VOICE,
            "+5%"
        ),
        generate_audio(
            shorts_texts["openworld"],
            os.path.join(BASE_DIR, "audio_openworld.mp3"),
            VOICE,
            "+28%"
        ),
        generate_audio(
            shorts_texts["racing"],
            os.path.join(BASE_DIR, "audio_racing.mp3"),
            VOICE,
            "+28%"
        ),
        generate_audio(
            shorts_texts["sports"],
            os.path.join(BASE_DIR, "audio_sports.mp3"),
            VOICE,
            "+28%"
        ),
        generate_audio(
            shorts_texts["cooking"],
            os.path.join(BASE_DIR, "audio_cooking.mp3"),
            VOICE,
            "+28%"
        ),
        generate_audio(
            shorts_texts["4x"],
            os.path.join(BASE_DIR, "audio_4x.mp3"),
            VOICE,
            "+28%"
        )
    ]
    
    print("Iniciando generación asíncrona de pistas de audio...")
    await asyncio.gather(*tasks)
    print("¡Proceso completado con éxito!")

if __name__ == "__main__":
    asyncio.run(main())
