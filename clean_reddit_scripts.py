import os
import re

input_path = r"C:\Users\jegom\reddit_shorts_project\extracted_scripts.txt"
output_path = r"C:\Users\jegom\reddit_shorts_project\scripts_reddit_clean.md"

with open(input_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Normalize all whitespace to single spaces
clean_text = re.sub(r'\s+', ' ', text)

# 2. Add structural line breaks before keys
# We use regex with optional double-spacing formatting from the PDF extraction
replacements = [
    (r'(Historia\s+\d+:)', r'\n\n# \1'),
    (r'(Origen:\s+\w+)', r'\n**\1'),
    (r'(\|\s+Categoría:)', r' \1'),
    (r'(\|\s+Partes\s+Totales:)', r' \1\n'),
    (r'([a-zA-Z0-9íáéóúñíÑÁÉÍÓÚ\s,.:;\-\'\"]+\-\s+Parte\s+\d+\s+de\s+\d+)', r'\n\n## \1'),
    (r'(\[Efectos\s+de\s+Sonido\s+y\s+Música\])', r'\n*   **SFX & Música:** '),
    (r'(\[Indicación\s+Visual\s+para\s+IA\s+-\s+Video\s+Prompt\])', r'\n*   **Prompt Visual:** '),
    (r'(\[Guión\s+de\s+Narración\s+\(Voiceover\)\])', r'\n*   **Narración (Voiceover):**\n    "'),
]

formatted_text = clean_text
for pattern, replacement in replacements:
    formatted_text = re.sub(pattern, replacement, formatted_text, flags=re.IGNORECASE)

# Clean up voiceover quotes (add closing quotes at the end of sections or before the next list item/header)
# Every time a Narración starts, it has a opening quote. We close it before the next structural tag.
lines = formatted_text.split('\n')
refined_lines = []
in_voiceover = False

for line in lines:
    stripped = line.strip()
    if in_voiceover:
        # If we hit a new list item or header, close the previous quote
        if stripped.startswith('*') or stripped.startswith('#') or stripped.startswith('##') or not stripped:
            if refined_lines and refined_lines[-1].endswith('\n    "'):
                refined_lines[-1] = refined_lines[-1][:-6] # remove empty quotes
            elif refined_lines:
                refined_lines[-1] = refined_lines[-1] + '"'
            in_voiceover = False
            
    if 'Narración (Voiceover):' in line:
        in_voiceover = True
        
    refined_lines.append(line)

if in_voiceover and refined_lines:
    refined_lines[-1] = refined_lines[-1] + '"'

final_content = '\n'.join(refined_lines)

# Fix duplicate headers and formatting anomalies
final_content = re.sub(r'#{1,}\s*=== PAGE \d+ ===', '', final_content)
final_content = re.sub(r'=== PAGE \d+ ===', '', final_content)
# Normalize spaces inside words (PDF had double spaces)
final_content = re.sub(r' {2,}', ' ', final_content)

with open(output_path, "w", encoding="utf-8") as f:
    f.write("# COMPILADO DE 15 HISTORIAS VIRALES DE REDDIT PARA SHORTS\n\n")
    f.write(final_content)

print(f"¡Guiones limpios estructurados y guardados en: {output_path}!")
