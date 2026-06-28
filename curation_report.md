# Reporte de Curación y Coherencia: YouTube Shorts - Rebajas de Steam 2026

**Fecha de Verificación:** 2026-06-27  
**Estado General:** ✅ **100% COHERENTE Y COMPILADO CON ÉXITO**

Este reporte detalla los resultados de la auditoría de coherencia y verificación técnica para el proyecto de automatización de YouTube Shorts sobre las Rebajas de Verano de Steam 2026. La verificación se realizó mediante un script automatizado ([verify_coherence.py](file:///C:/Users/jegom/shorts_project/verify_coherence.py)) desarrollado para comprobar la alineación de metadatos, la integridad de las imágenes de cápsula y el estado de renderizado de los videos compilados.

---

## 📊 Resumen Ejecutivo

| Área de Control | Estado | Total Verificado | Observaciones |
| :--- | :---: | :---: | :--- |
| **Cápsulas de Juego (Imágenes)** | ✅ OK | 15 / 15 | Existentes, no vacías y mapeadas correctamente. |
| **Alineación de Metadatos (Precios/Descuentos)** | ✅ OK | 15 / 15 | Perfecta concordancia entre `game_data.md` y `compile_shorts.py`. |
| **Alineación de Guiones e Infografía** | ✅ OK | 15 / 15 | Textos en pantalla y menciones en `scripts.md` alineados con la lógica. |
| **Archivos de Video Compilados** | ✅ OK | 3 / 3 | Creados, con peso óptimo y duraciones sincronizadas al audio (~29s). |

---

## 🔍 Detalle de las Verificaciones

### 1. Cápsulas de Juego (Assets Gráficos)
Se comprobó que las imágenes de portada (cápsulas) de Steam descargadas en la ruta [capsules/](file:///C:/Users/jegom/shorts_project/capsules/) existieran físicamente, no estuvieran vacías (0 bytes) y correspondieran a los IDs y títulos correctos definidos en la lógica de compilación.

*   **Total de archivos en disco:** 15 imágenes JPG.
*   **Total de juegos en la base de datos:** 15.
*   **Resultado:** 100% de los assets requeridos están presentes. No se encontraron imágenes corruptas o vacías.

<details>
<summary>📋 Lista Completa de Cápsulas Verificadas</summary>

| Imagen de Cápsula | Juego Relacionado | Tamaño (Bytes) | Estado |
| :--- | :--- | :---: | :---: |
| `age_of_empires_iv_1466860.jpg` | Age of Empires IV | 65.7 KB | ✅ Válida |
| `company_of_heroes_3_1675900.jpg` | Company of Heroes 3 | 80.2 KB | ✅ Válida |
| `dune_spice_wars_1171690.jpg` | Dune: Spice Wars | 73.9 KB | ✅ Válida |
| `age_of_mythology_retold_1934680.jpg` | Age of Mythology: Retold | 92.0 KB | ✅ Válida |
| `sins_of_a_solar_empire_ii_1575940.jpg` | Sins of a Solar Empire II | 51.0 KB | ✅ Válida |
| `against_the_storm_1336490.jpg` | Against the Storm | 61.4 KB | ✅ Válida |
| `frostpunk_2_1601580.jpg` | Frostpunk 2 | 36.7 KB | ✅ Válida |
| `farthest_frontier_1044720.jpg` | Farthest Frontier | 71.3 KB | ✅ Válida |
| `manor_lords_1363080.jpg` | Manor Lords | 66.2 KB | ✅ Válida |
| `satisfactory_526870.jpg` | Satisfactory | 50.7 KB | ✅ Válida |
| `the_witcher_3_292030.jpg` | The Witcher 3: Wild Hunt | 55.8 KB | ✅ Válida |
| `grim_dawn_219990.jpg` | Grim Dawn | 66.2 KB | ✅ Válida |
| `monster_hunter_world_582010.jpg` | Monster Hunter: World | 75.6 KB | ✅ Válida |
| `cyberpunk_2077_1091500.jpg` | Cyberpunk 2077 | 54.2 KB | ✅ Válida |
| `diablo_iv_2344520.jpg` | Diablo IV | 56.0 KB | ✅ Válida |

</details>

---

### 2. Metadatos de Juegos (game_data.md vs compile_shorts.py)
Se validó la consistencia en los nombres de los juegos, los porcentajes de descuento y las estructuras de precios del reporte de investigación con las constantes programáticas en el script de renderizado.

Nombres comerciales extendidos (como la adición de "Anniversary Edition" o "Complete Edition") y la correspondencia entre rangos de oferta de ediciones completas (ej. $3.99 en la configuración frente al rango de $3.99–$9.99 en la investigación) fueron analizados y validados como correctos.

*   **RTS Games:** Todos los precios y descuentos del 65%, 60%, 60%, 50% y 50% coinciden perfectamente.
*   **City Builder Games:** Coincidencia exacta de descuentos del 70%, 50%, 50%, 35% y 30% y sus respectivos precios.
*   **ARPG Games:** Coincidencia del 90%, 90%, 74%, 70% y 40%. Los precios corresponden a los mínimos de oferta informados en la investigación.

---

### 3. Coherencia con el Guion y Locución (scripts.md vs compile_shorts.py)
Se cruzaron los guiones literarios de locución en español y los textos superpuestos en pantalla (`scripts.md`) con las plantillas infográficas configuradas en Python.

*   La secuencia narrativa del 1 al 5 en los tres guiones coincide exactamente con el orden físico de renderizado de las imágenes de cápsula y las barras de progreso.
*   Los descuentos en el guion escrito corresponden de forma unívoca a los datos numéricos inyectados en los carteles de descuento.

---

### 4. Integridad de los Archivos de Video Compilados
Se examinaron los archivos de salida MP4 utilizando `ffprobe` para certificar que están correctamente codificados, que el peso sea coherente con un video comprimido de alta definición vertical, y que la duración de video se alinee exactamente con la duración de la pista de audio de voz correspondiente.

| Identificador del Video | Nombre del Archivo | Tamaño (MB) | Duración Video (s) | Duración Audio (s) | Diferencia | Estado |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **RTS** | `RTS_short.mp4` | 1.84 MB | 28.80s | 28.80s | 0.00s | ✅ Perfecto |
| **City Builder** | `City_short.mp4` | 1.68 MB | 29.13s | 29.14s | < 0.01s | ✅ Perfecto |
| **ARPG** | `ARPG_short.mp4` | 1.83 MB | 29.37s | 29.38s | < 0.01s | ✅ Perfecto |

---

## 📝 Conclusiones
La validación demuestra que no existen discrepancias, desfases de audio y video, ni metadatos erróneos. El pipeline de compilación de shorts está completamente verificado y los videos listos para su distribución y publicación.
