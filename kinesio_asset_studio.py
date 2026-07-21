import os
import sys
import json
import math
from datetime import datetime
from PIL import Image, ImageDraw, ImageFilter, ImageFont

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\jegom\shorts_project"
MANIFEST_PATH = os.path.join(BASE_DIR, "assets_manifest.json")

# --- 1. MANIFEST & ASSET DATING INDEXING ---
def date_and_tag_asset(asset_path, timestamp_str=None, source_url=None, tags=None):
    """
    Registers asset with chronological date metadata, source provenance, and semantic tags.
    """
    manifest = {}
    if os.path.exists(MANIFEST_PATH):
        try:
            with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}
            
    asset_name = os.path.basename(asset_path)
    img_size = None
    if os.path.exists(asset_path):
        try:
            with Image.open(asset_path) as img:
                img_size = img.size
        except Exception:
            img_size = (0, 0)
            
    manifest[asset_name] = {
        "filepath": asset_path,
        "date_timestamp": timestamp_str or datetime.now().strftime("%Y-%m-%d"),
        "source_url": source_url or "Local Capture",
        "tags": tags or [],
        "resolution": img_size,
        "indexed_at": datetime.now().isoformat()
    }
    
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        
    print(f"[ASSET STUDIO] Indexed '{asset_name}' with date: {timestamp_str or 'Today'}")
    return manifest[asset_name]

# --- 2. PRESS CLIPPING & DATED NEWSPAPER CARD GENERATOR ---
def create_press_clipping_card(headline, snippet_text, date_str="2008-12-24", source_name="WALL STREET JOURNAL", width=1920, height=1080):
    """
    Generates a high-taste realistic press clipping card with aged paper texture and date badge.
    """
    card = Image.new("RGBA", (width, height), (10, 13, 20, 255))
    draw = ImageDraw.Draw(card)
    
    # Paper cutout rectangle
    paper_w = int(width * 0.7)
    paper_h = int(height * 0.65)
    paper_x = (width - paper_w) // 2
    paper_y = (height - paper_h) // 2
    
    # Paper drop shadow
    draw.rounded_rectangle([paper_x + 12, paper_y + 12, paper_x + paper_w + 12, paper_y + paper_h + 12], radius=16, fill=(0, 0, 0, 180))
    # Aged paper background
    draw.rounded_rectangle([paper_x, paper_y, paper_x + paper_w, paper_y + paper_h], radius=16, fill=(245, 242, 232, 255), outline=(200, 195, 180, 255), width=3)
    
    font_header = ImageFont.truetype("C:\\Windows\\Fonts\\georgiab.ttf", 38)
    font_body = ImageFont.truetype("C:\\Windows\\Fonts\\georgia.ttf", 26)
    font_badge = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 20)
    
    # Newspaper Header
    draw.text((paper_x + 60, paper_y + 40), source_name.upper(), font=font_header, fill=(20, 20, 20, 255))
    draw.line([paper_x + 60, paper_y + 95, paper_x + paper_w - 60, paper_y + 95], fill=(40, 40, 40, 255), width=2)
    
    # Date Badge
    badge_str = f"📅 ARCHIVO HISTÓRICO: {date_str}"
    badge_w = int(draw.textlength(badge_str, font=font_badge)) + 24
    draw.rounded_rectangle([paper_x + paper_w - badge_w - 60, paper_y + 45, paper_x + paper_w - 60, paper_y + 85], radius=8, fill=(232, 33, 39, 230))
    draw.text((paper_x + paper_w - badge_w - 48, paper_y + 52), badge_str, font=font_badge, fill=(255, 255, 255, 255))
    
    # Headline
    draw.text((paper_x + 60, paper_y + 120), headline, font=font_header, fill=(10, 10, 10, 255))
    
    # Snippet text wrapping
    words = snippet_text.split()
    lines = []
    curr_line = ""
    for w in words:
        test_line = f"{curr_line} {w}".strip()
        if draw.textlength(test_line, font=font_body) < (paper_w - 120):
            curr_line = test_line
        else:
            lines.append(curr_line)
            curr_line = w
    if curr_line:
        lines.append(curr_line)
        
    line_y = paper_y + 200
    for l in lines[:8]:
        draw.text((paper_x + 60, line_y), l, font=font_body, fill=(40, 40, 40, 255))
        line_y += 42
        
    out_file = os.path.join(BASE_DIR, "screenshots", f"press_{date_str.replace('-','')}.jpg")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    card.convert("RGB").save(out_file, quality=92)
    print(f"[ASSET STUDIO] Generated Press Clipping Card: {out_file}")
    return out_file

# --- 3. DYNAMIC HIGHLIGHT OVERLAY (MARCADOR AMARILLO ANIMADO) ---
def apply_highlight_overlay(img, box_coords, color=(255, 215, 0, 160), progress=1.0):
    """
    Applies an animated yellow/gold highlighter marker over headline or snippet text.
    box_coords: [x1, y1, x2, y2]
    """
    img_rgba = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    x1, y1, x2, y2 = box_coords
    current_x2 = x1 + int((x2 - x1) * min(1.0, max(0.0, progress)))
    
    if current_x2 > x1:
        draw.rounded_rectangle([x1, y1, current_x2, y2], radius=6, fill=color)
        
    return Image.alpha_composite(img_rgba, overlay)

# --- 4. AUTOMATED MEME & REACTION CARD GENERATOR ---
def create_meme_card(top_text, bottom_text, bg_img_path=None, width=1080, height=1080):
    """
    Renders custom meme reaction card with impact typography and stroke contour.
    """
    if bg_img_path and os.path.exists(bg_img_path):
        card = Image.open(bg_img_path).convert("RGBA").resize((width, height), Image.Resampling.BILINEAR)
    else:
        card = Image.new("RGBA", (width, height), (15, 23, 42, 255))
        
    draw = ImageDraw.Draw(card)
    font_impact = ImageFont.truetype("C:\\Windows\\Fonts\\impact.ttf", 64)
    
    def draw_impact_text(pos_y, text):
        if not text:
            return
        text_w = draw.textlength(text.upper(), font=font_impact)
        pos_x = (width - text_w) / 2
        
        # Black contour stroke
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx != 0 or dy != 0:
                    draw.text((pos_x + dx, pos_y + dy), text.upper(), font=font_impact, fill=(0, 0, 0, 255))
        draw.text((pos_x, pos_y), text.upper(), font=font_impact, fill=(255, 255, 255, 255))
        
    draw_impact_text(40, top_text)
    draw_impact_text(height - 120, bottom_text)
    
    out_file = os.path.join(BASE_DIR, "screenshots", "meme_reaction.jpg")
    card.convert("RGB").save(out_file, quality=92)
    print(f"[ASSET STUDIO] Generated Meme Reaction Card: {out_file}")
    return out_file

# --- 5. CINEMATIC LUT & COLOR PRESETS ---
def apply_cinematic_preset(img, preset="cyber_obsidian"):
    """
    Applies color grading LUT preset (cyber_obsidian, vintage_sepia, cloud_blue, monochrome_archive).
    """
    img_rgba = img.convert("RGBA")
    
    if preset == "cyber_obsidian":
        tint = Image.new("RGBA", img.size, (10, 13, 20, 60))
        img_rgba = Image.alpha_composite(img_rgba, tint)
        # Boost contrast
        img_rgba = Image.blend(img_rgba, img_rgba.filter(ImageFilter.EDGE_ENHANCE), 0.15)
    elif preset == "vintage_sepia":
        tint = Image.new("RGBA", img.size, (112, 66, 20, 70))
        img_rgba = Image.alpha_composite(img_rgba, tint)
    elif preset == "cloud_blue":
        tint = Image.new("RGBA", img.size, (14, 116, 144, 50))
        img_rgba = Image.alpha_composite(img_rgba, tint)
    elif preset == "monochrome_archive":
        gray = img_rgba.convert("L").convert("RGBA")
        tint = Image.new("RGBA", img.size, (20, 20, 20, 40))
        img_rgba = Image.alpha_composite(gray, tint)
        
    return img_rgba.convert("RGB")

# --- 6. STICKER CUTOUT WITH DROP SHADOW ---
def create_sticker_cutout(img, stroke_color=(255, 255, 255, 255), stroke_width=6):
    """
    Creates a floating sticker cutout with drop shadow and border contour for overlay graphics.
    """
    img_rgba = img.convert("RGBA")
    w, h = img_rgba.size
    
    canvas = Image.new("RGBA", (w + stroke_width * 4, h + stroke_width * 4), (0, 0, 0, 0))
    # Drop shadow
    shadow = Image.new("RGBA", (w, h), (0, 0, 0, 140))
    canvas.paste(shadow, (stroke_width * 3, stroke_width * 3), img_rgba.split()[3])
    canvas = canvas.filter(ImageFilter.GaussianBlur(6))
    
    # Main sticker
    canvas.paste(img_rgba, (stroke_width * 2, stroke_width * 2), img_rgba)
    return canvas

# --- 7. GEOGRAPHIC MAP LOCATION BADGE ---
def draw_map_location_badge(draw_img, location_name, coords_str, date_str, pos=(80, 80)):
    """
    Overlays a geographic pin badge with lat/long and historical timestamp.
    """
    font_bold = ImageFont.truetype("C:\\Windows\\Fonts\\segoeuib.ttf", 22)
    font_sub = ImageFont.truetype("C:\\Windows\\Fonts\\segoeui.ttf", 18)
    
    badge_text = f"📍 {location_name.upper()}  |  {coords_str}  [{date_str}]"
    w = int(draw_img.textlength(badge_text, font=font_bold)) + 36
    h = 44
    x, y = pos
    
    draw_img.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=(10, 13, 20, 210), outline=(0, 210, 255, 120), width=2)
    draw_img.text((x + 18, y + 10), badge_text, font=font_bold, fill=(255, 255, 255, 255))

# --- 8. AUTOMATED PREVIEW CONTACT SHEET (VISUAL CURATION) ---
def generate_contact_sheet(output_html_path="assets_curation_preview.html"):
    """
    Builds an interactive HTML contact sheet for quick 5-second visual inspection of all indexed resources.
    """
    if not os.path.exists(MANIFEST_PATH):
        print("[ASSET STUDIO] Manifest file not found.")
        return
        
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
        
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>DOMINUSBABEL Asset Curation Contact Sheet</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0A0D14; color: #E2E8F0; padding: 20px; }
        h1 { color: #00D2FF; border-bottom: 2px solid #E82127; padding-bottom: 10px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
        .card { background: #1E293B; border-radius: 12px; padding: 15px; border: 1px solid #334155; }
        .card img { width: 100%; height: 180px; object-fit: cover; border-radius: 8px; }
        .title { font-weight: bold; margin-top: 10px; color: #FACC15; font-size: 14px; }
        .meta { font-size: 12px; color: #94A3B8; margin-top: 5px; }
        .badge { display: inline-block; background: #E82127; color: white; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
    </style>
</head>
<body>
    <h1>🎬 DOMINUSBABEL - Catálogo y Curaduría de Recursos</h1>
    <div class="grid">
"""
    for name, info in manifest.items():
        rel_path = info.get("filepath", "")
        date_ts = info.get("date_timestamp", "N/A")
        tags_str = ", ".join(info.get("tags", []))
        html += f"""
        <div class="card">
            <img src="{rel_path}" alt="{name}" onerror="this.src='https://via.placeholder.com/300x180?text=No+Image';">
            <div class="title">{name}</div>
            <div class="meta"><span class="badge">{date_ts}</span> {tags_str}</div>
        </div>
"""
    html += """
    </div>
</body>
</html>
"""
    out_path = os.path.join(BASE_DIR, output_html_path)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"[ASSET STUDIO] Contact Sheet HTML generated: {out_path}")
    return out_path

if __name__ == "__main__":
    print("====================================================")
    print("KINESIO & VAREGO ASSET STUDIO ENGINE v1.0.0")
    print("====================================================\n")
    
    # Test generation of a Dated Press Clipping Card
    test_press = create_press_clipping_card(
        headline="Tesla a 48 Horas del Colapso Financiero",
        snippet_text="Elon Musk invierte sus últimos fondos personales en Nochebuena para evitar la bancarrota de Tesla. El desarrollo del software propio Warp Drive sustituirá los módulos alemanes de SAP.",
        date_str="2008-12-24"
    )
    
    # Index asset
    date_and_tag_asset(test_press, "2008-12-24", "https://wallstreetjournal.com", ["tesla", "quiebra", "sap", "2008"])
    
    # Generate curation preview sheet
    generate_contact_sheet()
