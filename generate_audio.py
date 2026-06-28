import sys
import os
import asyncio
import edge_tts

# Configurar la salida estándar a UTF-8 para prevenir errores de codificación en Windows
sys.stdout.reconfigure(encoding='utf-8')

# Textos de los guiones
RTS_TEXT = (
    "¡Las rebajas de verano de Steam están aquí y estos son los cinco mejores "
    "juegos de estrategia en tiempo real que debes comprar ya! Primero, Age of "
    "Empires IV a mitad de precio con un sesenta y cinco por ciento de descuento. "
    "Segundo, Company of Heroes 3 al sesenta por ciento. Tercero, Dune: Spice Wars "
    "también al sesenta. Cuarto, el renovado Age of Mythology: Retold a mitad de "
    "precio. Y quinto, Sins of a Solar Empire II con cincuenta por ciento de "
    "descuento. ¿Cuál vas a comprar tú? ¡Cuéntanos abajo y suscríbete ya!"
)

CITY_TEXT = (
    "¡Las rebajas de verano de Steam traen las mejores ofertas para construir tu "
    "propia ciudad de ensueño! Aquí tienes cinco joyas. Primero, Against the Storm, "
    "el aclamado constructor de fantasía con un increíble setenta por ciento de "
    "descuento. Segundo, el crudo frío de Frostpunk 2 a mitad de precio. Tercero, "
    "la supervivencia medieval de Farthest Frontier al cincuenta por ciento. "
    "Cuarto, el realismo detallado de Manor Lords con treinta y cinco. Y quinto, "
    "las fábricas de Satisfactory al treinta por ciento. ¿Cuál vas a gestionar? "
    "¡Cuéntanos en los comentarios y suscríbete!"
)

ARPG_TEXT = (
    "¡Las rebajas de verano de Steam traen descuentos brutales de hasta el noventa "
    "por ciento en juegos de rol de acción! Primero, la obra maestra The Witcher 3 "
    "a un precio ridículo con noventa por ciento de descuento. Segundo, el clásico "
    "sombrío Grim Dawn también rebajado un noventa. Tercero, la cacería en Monster "
    "Hunter: World con setenta y cuatro por ciento de ahorro. Cuarto, el futuro de "
    "Cyberpunk 2077 con un setenta. Y quinto, las temporadas de Diablo IV con "
    "cuarenta por ciento. ¿Cuál de estos mundos vas a dominar? ¡Comenta abajo y "
    "suscríbete!"
)

VOICE = "es-MX-JorgeNeural"

async def generate_audio(text: str, output_path: str, voice: str, rate: str) -> None:
    print(f"Generando audio en: {output_path} con velocidad {rate}...")
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(output_path)
    if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
        print(f"¡Éxito! Archivo creado correctamente ({os.path.getsize(output_path)} bytes).")
    else:
        raise RuntimeError(f"Error: El archivo {output_path} no se creó o está vacío.")

async def main() -> None:
    tasks = [
        generate_audio(RTS_TEXT, r"C:\Users\jegom\shorts_project\audio_rts.mp3", VOICE, "+28%"),
        generate_audio(CITY_TEXT, r"C:\Users\jegom\shorts_project\audio_city.mp3", VOICE, "+38%"),
        generate_audio(ARPG_TEXT, r"C:\Users\jegom\shorts_project\audio_arpg.mp3", VOICE, "+32%"),
    ]
    await asyncio.gather(*tasks)
    print("Todos los archivos de audio se han generado exitosamente.")

if __name__ == "__main__":
    asyncio.run(main())
