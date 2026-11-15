"""Preview and check one picture extension module (e.g. sports_more_am.py).

Usage:  python tests/more_sheet.py sports_more_am out.png [tile] [LETTERS]
Renders only that module's pictures (optionally only some letters, e.g. "ABC"),
runs the same safety checks as Pack.write, and prints a per-letter count.
"""
import io, os, sys, importlib, xml.etree.ElementTree as ET
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from svgkit import Pack

mod_name = sys.argv[1].replace(".py", "")
out = sys.argv[2]
T = int(sys.argv[3]) if len(sys.argv) > 3 else 170
only = sys.argv[4] if len(sys.argv) > 4 else None
K = Pack()
importlib.import_module(mod_name).add_more(K)
tiles, problems = [], []
for k in sorted(K.items):
    for it in K.items[k]:
        s = it["svg"]
        if it["name"][0].upper() != k: problems.append(f"{k}: name {it['name']!r} does not start with {k}")
        for bad in ("`", "${", " id=", "url("):
            if bad in s: problems.append(f"{k} {it['name']}: contains {bad!r}")
        if not s.startswith('<svg viewBox="0 0 100 100"'): problems.append(f"{k} {it['name']}: must use svg() (viewBox 0 0 100 100)")
        try: ET.fromstring(s)
        except Exception as e: problems.append(f"{k} {it['name']}: XML error {e}")
        if only and k not in only: continue
        png = cairosvg.svg2png(bytestring=s.encode(), output_width=T, output_height=T, background_color="white")
        tiles.append((f'{k}: {it["name"]}', Image.open(io.BytesIO(png)).convert("RGB")))
print("counts:", " ".join(f"{k}{len(v)}" for k, v in sorted(K.items.items())), "| total", sum(len(v) for v in K.items.values()))
print("PROBLEMS:\n  " + "\n  ".join(problems) if problems else "checks OK")
if tiles:
    cols = 6; rows = (len(tiles) + cols - 1) // cols; W = T + 20; H = T + 30
    sheet = Image.new("RGB", (cols * W, rows * H), "white"); d = ImageDraw.Draw(sheet)
    try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 13)
    except Exception: font = ImageFont.load_default()
    for i, (lab, im) in enumerate(tiles):
        x = (i % cols) * W + 10; y = (i // cols) * H + 5
        sheet.paste(im, (x, y)); d.rectangle([x, y, x + T - 1, y + T - 1], outline="#ddd")
        d.text((x, y + T + 5), lab, fill="black", font=font)
    sheet.save(out); print("sheet:", len(tiles), "tiles ->", out)
