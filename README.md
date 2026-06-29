# KINESIO: Ecosistema Agéntico y Compositor Automático para Producción Multiformato (YouTube Shorts & Horizontal)

KINESIO es un ecosistema agéntico para la creación y producción automatizada de videos en formato vertical (9:16, 1080x1920) y horizontal (16:9, 1920x1080) optimizados para YouTube Shorts, TikTok, Instagram Reels y publicaciones de larga duración de YouTube. Diseñado bajo los patrones de arquitectura de investigación y ensamble visual inspired by **VideoAgent** (HKUDS), KINESIO orquesta agentes especializados que investigan ofertas, redactan guiones persuasivos en español, sintetizan locuciones neuronales, extraen clips de juego oficiales en alta definición y ensamblan de forma 100% programática y local la salida multimedia final.

Este repositorio es una solución de nivel empresarial para creadores de contenido que buscan escalar su alcance y reactivar el crecimiento de sus canales mediante contenido altamente curado, estéticamente superior y estructurado para SEO.

---

## 🏗️ Arquitectura de la Solución (Volumen 1, 2 & 3)

El ecosistema opera mediante una arquitectura de pipeline desacoplada y secuencial, garantizando la resiliencia en cada fase del proceso:

```mermaid
graph TD
    subgraph Fase 1: Extracción e Investigación de Mercado
        A[ContentScraperAgent] -->|Steam Storefront API / Web Scraper| B[(Base de Datos: game_data_v2.md)]
    end

    subgraph Fase 2: Producción Editorial y Diseño de Guiones
        B --> C[ScriptwriterAgent]
        C -->|Análisis Horizontales + 12 Shorts| D[(Guiones: script_mow.md, script_dune.md, script_pathfinder.md & scripts_shorts_v3.md)]
    end

    subgraph Fase 3: Síntesis de Audio y Efectos Sonoros (SFX)
        D --> E[VoiceProducerAgent]
        E -->|Edge-TTS locución acelerada y clara| F[(audio_*.mp3)]
        G[SFX Generator] -->|Síntesis matemática de ondas| H[(whoosh.wav / pop.wav)]
    end

    subgraph Fase 4: Renderizado y Composición Visual
        D --> I[VideoEditorAgent]
        I -->|Cápsulas y Avances Oficiales| J[Slicing & Ken Burns Engine]
        J -->|Fotogramas Animados + Clips 30fps| K[FFmpeg Multi-Track Assembly]
        F --> K
        H --> K
        K -->|Videos Horizontal & Shorts .mp4| L[(Deliverables)]
    end

    subgraph Fase 5: Aseguramiento de Calidad y Curation
        L --> M[ContentCuratorAgent]
        M -->|Verificación programática CQA| N[(Reporte: curation_report_v3.md)]
        N -->|Publicación Optimizada SEO| O[YouTube Channel @dominus8735]
    end
```

---

## 🌟 Características Técnicas Avanzadas (Volumen 3)

*   **Alineación Temporal Dinámica por Proporción de Palabras (Word-Count Alignment):** 
    *   *Videos Horizontales (Men of War, Dune, Pathfinder):* El motor analiza el guion Markdown en tiempo de ejecución, divide el texto por capítulos y cuenta las palabras de cada bloque locutado. Al calcular el porcentaje de palabras de cada capítulo respecto al total, define de forma dinámica la duración exacta de cada sección sobre el archivo de audio sintetizado. Esto garantiza una transición visual perfecta (corte de jugabilidad a diapositivas) sincronizada con la voz al milisegundo.
    *   *Shorts Comparativos de Precios:* Cada Short de ~31s incorpora una cabecera traslúcida estática, una barra de progreso que llena la pantalla y un bloque central animado. Durante el segundo 8 al 22, se proyecta un avance cinematográfico en una ventana 16:9 con borde brillante, mientras que en la parte inferior se renderiza una tabla con la comparación de precios regionales de la oferta (USA, Europa y Latinoamérica).
*   **Locución Neuronal Multiformato:** Locuciones de alta fidelidad con `edge-tts` (voz `es-MX-JorgeNeural`) configuradas con diferentes tasas de velocidad según el formato:
    *   *Formato Horizontal (Análisis Profundo):* Velocidad de `+5%` para mantener la claridad expositiva y la solemnidad del análisis sin aburrir al usuario.
    *   *Formato Short (Retención Máxima):* Velocidad de `+28%` para enganchar en los primeros 3 segundos y entregar la información de ofertas de forma rápida.
*   **Composición Gráfica de Alta Fidelidad (PIL):** Renderizado fotograma a fotograma (30 fps) aplicando:
    *   **Filtros de Desenfoque:** Fondo animado aplicando filtros de desenfoque gaussiano de 25 píxeles y reducción de brillo por multiplicación alfa del 60%.
    *   **Máscaras de Transparencia:** Redimensionamiento y esquinas redondeadas de 20px en cápsulas usando máscaras de canal alfa.
    *   **Animación por Interpolación (Keyframing):** Transiciones de zoom elástico para portadas (0.8x a 1.0x) y efectos de rebote para insignias de descuento.
*   **Humor de Internet y Superposición de Memes:**
    *   El motor detecta menciones clave en los guiones e incorpora insignias animadas con humor y memes nativos en las esquinas de los videos horizontales (como un pop-up de "STONKS 📈", "OFERTAZO 💸" o "GIGACHAD 😎"), mejorando el enganche emocional con la audiencia de habla hispana.
*   **Síntesis Programática de SFX:** Generación matemática de archivos WAV sin dependencias externas:
    *   *Whoosh (Transiciones):* Barrido de frecuencia sinusoidal de 150 Hz a 800 Hz modulado con ruido blanco y una curva de volumen de envolvente parabólica.
    *   *Pop (Aparición de Descuentos):* Onda senoidal con decaimiento exponencial rápido de volumen y barrido de pitch ascendente.
*   **Resiliencia y Manejo de Juegos Descatalogados:** Rutina de respaldo automático que intercepta códigos de error (404) de la API de Steam (ej. *Football Manager 2024* o *PGA TOUR 2K23*) y asocia automáticamente activos precacheados equivalentes de alta fidelidad.

---

## 📁 Estructura del Ecosistema

```text
├── capsules/                  # Portadas de juegos oficiales (600x900) descargadas de Steam
├── screenshots/               # Capturas de pantalla de alta resolución de juegos horizontales
├── trailers/                  # Videos de avances oficiales (.mp4) de Steam
├── compile_expanded.py        # Agente VideoEditor v2: Renderizado horizontal (MOW) y vertical
├── compile_new_videos.py      # Agente VideoEditor v3: Renderizado horizontal (Dune, Pathfinder) y los 7 Shorts
├── verify_coherence_v3.py     # Agente ContentCurator v3: Auditoría y validación de coherencia CQA
├── generate_audio_v3.py       # Agente VoiceProducer v3: Síntesis de voz en off multiformato
├── download_new_assets.py     # Agente AssetsCollector v3: Descarga programática de trailers y capturas
├── game_data_v2.md            # Base de datos de juegos, descuentos, precios e IDs (Verano 2026)
├── script_dune.md             # Guion táctico extendido para Dune: Spice Wars
├── script_pathfinder.md       # Guion táctico extendido para Pathfinder: Wrath of the Righteous
├── scripts_shorts_v3.md       # Guiones estructurados en español para los 7 Shorts comparativos
├── curation_report_v3.md      # Informe final de auditoría y coherencia semántica CQA de Volumen 3
├── youtube_seo.md             # Títulos y metadatos optimizados para SEO de YouTube (Ecosistema Completo)
├── dune_thumbnail.jpg         # Miniatura generada en 16:9 para Dune: Spice Wars
├── pathfinder_thumbnail.jpg   # Miniatura generada en 16:9 para Pathfinder: Wrath of the Righteous
└── README.md                  # Documentación del sistema
```

---

## 🚀 Instalación y Despliegue

### Prerrequisitos
1. **Python 3.11+**
2. **FFmpeg** configurado en las variables de entorno de tu sistema (con soporte para `libx264` y `aac`).

### Clonar e Instalar Dependencias
```bash
git clone https://github.com/DOMINUSBABEL/KINESIO.git
cd KINESIO
pip install Pillow edge-tts gTTS
```

### Ejecutar el Pipeline de Producción (Volumen 3)

1. **Investigar y Clasificar Juegos:**
   Los precios y App IDs ya se encuentran estructurados y validados en [game_data_v2.md](file:///C:/Users/jegom/shorts_project/game_data_v2.md).

2. **Generar Locución Neural (TTS):**
   ```bash
   python generate_audio_v3.py
   ```
   Esto sintetizará las pistas en el directorio raíz (`audio_dune.mp3`, `audio_pathfinder.mp3`, `audio_jc2.mp3`, etc.).

3. **Descargar y Validar Activos Visuales:**
   ```bash
   python download_new_assets.py
   ```
   Esto descargará de la API de Steam e integrará cápsulas en `/capsules`, capturas en `/screenshots` y videos en `/trailers`.

4. **Compilar y Renderizar Videos (Video Engine):**
   ```bash
   python compile_new_videos.py
   ```
   *Nota: Este script compilará los análisis de 10 minutos de Dune y Pathfinder, y los 7 Shorts regionales en vertical.*

5. **Auditar Calidad y Coherencia Semántica (CQA):**
   ```bash
   python verify_coherence_v3.py
   ```
   Este script revisará la correlación entre fotogramas, clips de video y metadatos, y exportará la validación en [curation_report_v3.md](file:///C:/Users/jegom/shorts_project/curation_report_v3.md).

---

## 🛠️ Detalles del Generador de Sonido (SFX Generator)

Los efectos de sonido se generan de forma programática utilizando cálculos trigonométricos puros sobre la onda portadora. Por ejemplo:

```python
# Muestra matemática de generación de efecto "Pop"
import math, wave

def generate_pop(filename, duration=0.15, sample_rate=44100):
    samples = []
    num_samples = int(duration * sample_rate)
    for i in range(num_samples):
        t = i / sample_rate
        freq = 300 + 400 * (t / duration)  # Sweeping pitch ascendente
        # Ataque rápido de 10ms, seguido de un decaimiento exponencial rápido
        vol = t / 0.01 if t < 0.01 else math.exp(-30 * (t - 0.01))
        val = math.sin(2 * math.pi * freq * t) * vol * 0.7
        samples.append(val)
    # Codificación de 16-bit PCM en archivo WAV...
```

---

## ✒️ Créditos y Desarrollo

Este proyecto ha sido desarrollado bajo los estándares de ingeniería de software agéntica por:

*   **Creador y Director del Proyecto:** [Juan Esteban Gómez Bernal (DOMINUSBABEL)](https://github.com/DOMINUSBABEL)
*   **Empresa Desarrolladora:** [BABYLON.IA](https://babylonias.com)

KINESIO es una marca registrada de **BABYLON.IA** y su arquitectura agéntica de video se distribuye bajo la licencia MIT.

## ⚙️ Ecosistema Core (kinesio_core.py)
KINESIO cuenta con un núcleo de utilidades optimizado para procesamiento multimedia en memoria. Este módulo encapsula las funciones matemáticas de redimensionado, efectos de difuminado y generación de barras de progreso dinámicas.

### 🎬 Efectos Ken Burns y Paneo Dinámico
El motor calcula progresiones geométricas para recortar y desplazar las imágenes de fondo en tiempo real, logrando transiciones fluidas de cámara y combatiendo la fatiga estática.

### 🔊 Mezclador de Audio y SFX Avanzado
El motor inyecta sonidos de impacto (`pop` y `whoosh`) y realiza la elusión de límites físicos de FFmpeg para bucles infinitos de audio mediante `-stream_loop -1`.
