"""Contact sheet of a picture pack for visual review.
Usage: python tests/pack_sheet.py tests/sports.js out.png [tile]"""
import io, json, os, subprocess, sys, xml.etree.ElementTree as ET
import cairosvg
from PIL import Image, ImageDraw, ImageFont
src = os.path.abspath(sys.argv[1]); out = sys.argv[2]; T = int(sys.argv[3]) if len(sys.argv) > 3 else 160
data = json.loads(subprocess.check_output(["node", "-e", f"process.stdout.write(JSON.stringify(require({json.dumps(src)})))"]))
tiles = []
for k, arr in data.items():
    for it in arr:
        s = it["svg"]; ET.fromstring(s)
        png = cairosvg.svg2png(bytestring=s.encode(), output_width=T, output_height=T, background_color="white")
        tiles.append((f'{k}: {it["name"]}', Image.open(io.BytesIO(png)).convert("RGB")))
cols = 7; rows = (len(tiles) + cols - 1) // cols; W = T + 20; H = T + 30
sheet = Image.new("RGB", (cols * W, rows * H), "white"); d = ImageDraw.Draw(sheet)
try: font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
except Exception: font = ImageFont.load_default()
for i, (lab, im) in enumerate(tiles):
    x = (i % cols) * W + 10; y = (i // cols) * H + 5
    sheet.paste(im, (x, y)); d.rectangle([x, y, x + T - 1, y + T - 1], outline="#ddd")
    d.text((x, y + T + 4), lab, fill="black", font=font)
sheet.save(out); print("tiles", len(tiles), "->", out)
