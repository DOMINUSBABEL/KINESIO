import asyncio
import edge_tts
import subprocess

async def test():
    text = (
        "En Buriatia, Siberia, la vida tiene un precio exacto fijado por el estado. "
        "El salario promedio mensual aquí es de cuatrocientos dólares, pero si te enlistas, "
        "el bono inicial y el pago de combate multiplican tus ingresos por seis de inmediato. "
        "Si mueres en combate, tu familia recibe doce millones de rublos. "
        "Para muchos hogares rurales, un hijo vale más fallecido en la trinchera que trabajando "
        "toda su vida útil en el campo. Es la cruda realidad siberiana."
    )
    comm = edge_tts.Communicate(text, voice='es-MX-JorgeNeural')
    await comm.save('test_raw.mp3')
    
    res = subprocess.run([
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        'test_raw.mp3'
    ], stdout=subprocess.PIPE, text=True)
    print('Duration of raw text TTS:', res.stdout.strip())

if __name__ == "__main__":
    asyncio.run(test())
