# KINESIO: Ecosistema Agéntico y Compositor Automático para Producción Multiformato (YouTube Shorts & Horizontal)

KINESIO es un ecosistema agéntico para la creación y producción automatizada de videos en formato vertical (9:16, 1080x1920) y horizontal (16:9, 1920x1080) optimizados para YouTube Shorts, TikTok, Instagram Reels y publicaciones de larga duración de YouTube. Diseñado bajo los patrones de arquitectura de investigación y ensamble visual inspired by **VideoAgent** (HKUDS), KINESIO orquesta agentes especializados que investigan ofertas, redactan guiones persuasivos en español, sintetizan locuciones neuronales, extraen clips de juego oficiales en alta definición y ensamblan de forma 100% programática y local la salida multimedia final.

Este repositorio es una solución de nivel empresarial para creadores de contenido que buscan escalar su alcance y reactivar el crecimiento de sus canales mediante contenido altamente curado, estéticamente superior y estructurado para SEO.

---

## 🏗️ Arquitectura de la Solución (Volumen 1 & 2)

El ecosistema opera mediante una arquitectura de pipeline desacoplada y secuencial, garantizando la resiliencia en cada fase del proceso:

```mermaid
graph TD
    subgraph Fase 1: Extracción e Investigación de Mercado
        A[ContentScraperAgent] -->|Steam Storefront API / Web Scraper| B[(Base de Datos: game_data_v2.md)]
    end

    subgraph Fase 2: Producción Editorial y Diseño de Guiones
        B --> C[ScriptwriterAgent]
        C -->|Análisis Horizontal + 5 Shorts| D[(Guiones: script_mow.md & scripts_shorts_v2.md)]
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
        M -->|Verificación programática CQA| N[(Reporte: curation_report_v2.md)]
        N -->|Publicación Optimizada SEO| O[YouTube Channel @dominus8735]
    end
```

---

## 🌟 Características Técnicas Avanzadas

*   **Alineación Temporal por Segmentos (Shot Planning):** 
    *   *Video Horizontal (Men of War):* La locución de 7 minutos y 49 segundos se subdivide automáticamente en 18 segmentos mediante conteo de palabras para un alineamiento preciso. El motor alterna dinámicamente diapositivas estéticas (efecto Ken Burns con texto en paneles translúcidos) y clips fluidos del avance oficial en momentos de acción táctica.
    *   *Shorts Verticales:* Cada Short de ~31s muestra portadas con escala elástica durante 1.5s y realiza una transición fluida hacia 3.0s de jugabilidad en un contenedor enmarcado con barras neon de contraste.
*   **Locución Neuronal Acelerada:** Utiliza la librería neural `edge-tts` con la voz `es-MX-JorgeNeural` configurada a una velocidad del `+28%` para Shorts (energía máxima y retención rápida) y `+5%` para el video largo (claridad táctica e instructiva).
*   **Composición Gráfica de Alta Fidelidad (PIL):** Renderizado fotograma a fotograma (30 fps) aplicando:
    *   **Filtros de Desenfoque:** Fondo animado aplicando filtros de desenfoque gaussiano de 25 píxeles y reducción de brillo por multiplicación alfa del 60%.
    *   **Máscaras de Transparencia:** Redimensionamiento y esquinas redondeadas de 20px en cápsulas usando máscaras de canal alfa.
    *   **Animación por Interpolación (Keyframing):** Transiciones de zoom elástico para portadas (0.8x a 1.0x) y efectos de rebote para insignias de descuento.
*   **Síntesis Programática de SFX:** Generación matemática de archivos WAV sin dependencias externas:
    *   *Whoosh (Transiciones):* Barrido de frecuencia sinusoidal de 150 Hz a 800 Hz modulado con ruido blanco y una curva de volumen de envolvente parabólica.
    *   *Pop (Aparición de Descuentos):* Onda senoidal con decaimiento exponencial rápido de volumen y barrido de pitch ascendente.
*   **Resiliencia y Manejo de Juegos Descatalogados:** Rutina de respaldo automático que intercepta códigos de error (404) de la API de Steam (ej. *Football Manager 2024* o *PGA TOUR 2K23*) y asocia automáticamente activos precacheados equivalentes de alta fidelidad.
*   **Optimización SEO y Metadatos:** Genera el plan completo de palabras clave, etiquetas y descripciones para YouTube en [youtube_seo.md](file:///C:/Users/jegom/shorts_project/youtube_seo.md), además de diseñar de manera agéntica la miniatura horizontal de portada [mow_thumbnail.jpg](file:///C:/Users/jegom/shorts_project/mow_thumbnail.jpg).

---

## 📁 Estructura del Ecosistema

```text
├── capsules/                  # Portadas de juegos oficiales (600x900) descargadas de Steam
├── screenshots/               # Capturas de pantalla de alta resolución de Men of War AS2
├── trailers/                  # Videos de avances oficiales (.mp4) de Steam
├── compile_expanded.py        # Agente VideoEditor v2: Renderizado horizontal y vertical FFmpeg
├── verify_coherence_v2.py     # Agente ContentCurator v2: Auditoría y validación de coherencia CQA
├── generate_audio_v2.py       # Agente VoiceProducer v2: Síntesis de voz en off con edge-tts
├── download_assets_v2.py      # Agente AssetsCollector v2: Descarga programática de recursos
├── download_missing_assets.py # Script de descarga de activos faltantes y resolución de fallas
├── game_data_v2.md            # Base de datos de juegos, descuentos, precios e IDs (Verano 2026)
├── script_mow.md              # Guion táctico extendido para Men of War: Assault Squad 2
├── scripts_shorts_v2.md       # Guiones estructurados en español para los 5 nuevos Shorts
├── curation_report_v2.md      # Informe final de auditoría y coherencia semántica CQA
├── youtube_seo.md             # Títulos y metadatos optimizados para SEO de YouTube
├── mow_thumbnail.jpg          # Miniatura generada en 16:9 para Men of War AS2
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

### Ejecutar el Pipeline Completo de Producción

1. **Investigar y Clasificar Juegos:**
   Los precios y App IDs ya se encuentran estructurados y validados en [game_data_v2.md](file:///C:/Users/jegom/shorts_project/game_data_v2.md).

2. **Generar Locución Neural (TTS):**
   ```bash
   python generate_audio_v2.py
   ```
   Esto sintetizará las pistas en el directorio raíz (`audio_mow.mp3`, `audio_openworld.mp3`, etc.).

3. **Descargar y Validar Activos Visuales:**
   ```bash
   python download_assets_v2.py
   python download_missing_assets.py
   ```
   Esto guardará las cápsulas en `/capsules`, capturas en `/screenshots` y videos en `/trailers`.

4. **Compilar y Renderizar Videos (Video Engine):**
   ```bash
   python compile_expanded.py
   ```
   *Nota: Este script compilará el análisis de 7:49 minutos en horizontal y los 5 Shorts verticales con jugabilidad de forma totalmente secuencial.*

5. **Auditar Calidad y Coherencia Semántica (CQA):**
   ```bash
   python verify_coherence_v2.py
   ```
   Este script revisará la correlación entre fotogramas, clips de video y metadatos, y exportará la validación en [curation_report_v2.md](file:///C:/Users/jegom/shorts_project/curation_report_v2.md).

Los entregables finales se exportarán en la raíz como:
*   `MenOfWar_AssaultSquad2_analysis.mp4` (Análisis Horizontal 16:9)
*   `openworld_v2_short.mp4` (Short Vertical 9:16)
*   `racing_v2_short.mp4` (Short Vertical 9:16)
*   `sports_v2_short.mp4` (Short Vertical 9:16)
*   `cooking_v2_short.mp4` (Short Vertical 9:16)
*   `4x_v2_short.mp4` (Short Vertical 9:16)

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
