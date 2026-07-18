import os
import re

input_path = r"C:\Users\jegom\reddit_shorts_project\extracted_scripts.txt"
output_path = r"C:\Users\jegom\reddit_shorts_project\scripts_reddit_clean.md"

with open(input_path, "r", encoding="utf-8") as f:
    raw_content = f.read()

# Split into lines and clean them
raw_lines = raw_content.split('\n')
initial_lines = []
for line in raw_lines:
    line_clean = re.sub(r'\s+', ' ', line).strip()
    if not line_clean:
        continue
    if re.match(r'^=== PAGE \d+ ===$', line_clean):
        continue
    initial_lines.append(line_clean)

# Preprocessing: Merge wrapped headers and titles
clean_lines = []
i = 0
n = len(initial_lines)

while i < n:
    line = initial_lines[i]
    
    # 1. Merge Story Header if wrapped
    # e.g., line = "Historia 9: Escuché un Golpe Rítmico desde el Búnker de mi"
    # and next line = "Vecino" (not starting with Origen, and not a number, and not a part)
    if re.match(r'^Historia\s+\d+:', line, re.IGNORECASE) and i + 1 < n:
        next_line = initial_lines[i+1]
        if not next_line.lower().startswith("origen:") and not re.search(r'parte\s+\d+', next_line, re.IGNORECASE):
            line = line + " " + next_line
            i += 1 # skip next line
            
    # 2. Merge Part Header if wrapped
    # e.g., line = "... - Parte 1 de" and next line = "3"
    # Or line ends with "de" and next line is a digit
    if re.search(r'parte\s+\d+\s+de\s*$', line, re.IGNORECASE) and i + 1 < n:
        next_line = initial_lines[i+1]
        if re.match(r'^\d+$', next_line):
            line = line + " " + next_line
            i += 1 # skip next line
            
    # Clean up lone page numbers
    if re.match(r'^\d+$', line):
        i += 1
        continue
        
    clean_lines.append(line)
    i += 1

stories = []
current_story = None
current_part = None
current_section = None

for line in clean_lines:
    # 1. Detect Story Header
    if re.match(r'^Historia\s+\d+:', line, re.IGNORECASE):
        current_story = {
            "title": line,
            "origen": "",
            "parts": []
        }
        stories.append(current_story)
        current_part = None
        current_section = None
        continue
        
    # 2. Detect Origen line
    if line.lower().startswith("origen:"):
        if current_story:
            current_story["origen"] = line
        continue
        
    # 3. Detect Part Header
    is_part = False
    if "parte" in line.lower() and "de" in line.lower():
        if re.search(r'parte\s+\d+\s+de\s+\d+', line, re.IGNORECASE):
            is_part = True
            
    if is_part:
        label_match = re.search(r'(\[Efectos.*?\]|\[Indicación.*?\]|\[Guión.*?\])', line, re.IGNORECASE)
        part_title = line
        label_found = None
        if label_match:
            part_title = line[:label_match.start()].strip()
            label_found = line[label_match.start():].strip()
            
        current_part = {
            "title": part_title,
            "sfx": "",
            "prompt": "",
            "voiceover": ""
        }
        if current_story:
            current_story["parts"].append(current_part)
        else:
            current_story = {"title": "Historia General", "origen": "", "parts": [current_part]}
            stories.append(current_story)
            
        current_section = None
        
        if label_found:
            line = label_found
        else:
            continue

    # 4. Check for Section Labels and keep trailing text
    sfx_match = re.search(r'\[Efectos\s+de\s+Sonido\s+y\s+Música\]', line, re.IGNORECASE)
    prompt_match = re.search(r'\[Indicación\s+Visual\s+para\s+IA\s+-\s+Video\s+Prompt\]', line, re.IGNORECASE)
    voiceover_match = re.search(r'\[Guión\s+de\s+Narración\s+\(Voiceover\)\]', line, re.IGNORECASE)

    leftover_content = None
    if sfx_match:
        current_section = 'SFX'
        idx = sfx_match.end()
        leftover_content = line[idx:].strip()
    elif prompt_match:
        current_section = 'PROMPT'
        idx = prompt_match.end()
        leftover_content = line[idx:].strip()
    elif voiceover_match:
        current_section = 'VOICEOVER'
        idx = voiceover_match.end()
        leftover_content = line[idx:].strip()
        leftover_content = re.sub(r'^(9:16|--ar\s+9:16)\s*', '', leftover_content).strip()
    else:
        leftover_content = line

    if not leftover_content:
        continue

    # 5. Accumulate content lines
    if current_part and current_section:
        if current_section == 'SFX':
            if current_part["sfx"]:
                current_part["sfx"] += " " + leftover_content
            else:
                current_part["sfx"] = leftover_content
        elif current_section == 'PROMPT':
            if current_part["prompt"]:
                current_part["prompt"] += " " + leftover_content
            else:
                current_part["prompt"] = leftover_content
        elif current_section == 'VOICEOVER':
            leftover_content = re.sub(r'^(9:16|--ar\s+9:16)\s*', '', leftover_content).strip()
            if current_part["voiceover"]:
                current_part["voiceover"] += " " + leftover_content
            else:
                current_part["voiceover"] = leftover_content

# 6. Write structured Markdown
with open(output_path, "w", encoding="utf-8") as f:
    f.write("# COMPILADO DE 15 HISTORIAS VIRALES DE REDDIT PARA SHORTS\n\n")
    for s in stories:
        f.write(f"# {s['title']}\n")
        if s["origen"]:
            origen_clean = re.sub(r'\s+', ' ', s['origen']).strip()
            f.write(f"**{origen_clean}**\n\n")
        else:
            f.write("\n")
            
        for p in s["parts"]:
            title_clean = re.sub(r'\s+', ' ', p['title']).strip()
            f.write(f"## {title_clean}\n")
            
            sfx_clean = re.sub(r'\s+', ' ', p['sfx']).strip() if p['sfx'] else ""
            if sfx_clean:
                f.write(f"*   **SFX & Música:** {sfx_clean}\n")
                
            prompt_clean = re.sub(r'\s+', ' ', p['prompt']).strip() if p['prompt'] else ""
            if prompt_clean:
                if "--ar" not in prompt_clean:
                    prompt_clean += " --ar 9:16"
                f.write(f"*   **Prompt Visual:** {prompt_clean}\n")
                
            voice_clean = re.sub(r'\s+', ' ', p['voiceover']).strip() if p['voiceover'] else ""
            if voice_clean:
                f.write(f"*   **Narración (Voiceover):**\n    \"{voice_clean}\"\n")
            f.write("\n")
        f.write("---\n\n")

print(f"¡Guiones analizados y guardados correctamente en: {output_path}!")
