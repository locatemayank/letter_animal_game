import json, subprocess, io, xml.etree.ElementTree as ET, cairosvg, sys
from PIL import Image, ImageDraw, ImageFont
p="/sessions/keen-intelligent-gates/mnt/outputs/tests/garden.js"
data=json.loads(subprocess.check_output(["node","-e",f"process.stdout.write(JSON.stringify(require('{p}')))"]))
tiles=[]; T=160 if len(sys.argv)<2 else int(sys.argv[1])
for k,arr in data.items():
    for it in arr:
        ET.fromstring(it["svg"]); s=it["svg"]
        assert 'viewBox="0 0 100 100"' in s and 'width=' not in s.split('>')[0]
        png=cairosvg.svg2png(bytestring=s.encode(),output_width=T,output_height=T,background_color="white")
        tiles.append((f'{k}: {it["name"]}  ({len(s)})',Image.open(io.BytesIO(png)).convert("RGB")))
cols=7; rows=(len(tiles)+cols-1)//cols; W=T+20; H=T+30
sheet=Image.new("RGB",(cols*W,rows*H),"white"); d=ImageDraw.Draw(sheet)
try: font=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",12)
except: font=ImageFont.load_default()
for i,(lab,im) in enumerate(tiles):
    x=(i%cols)*W+10; y=(i//cols)*H+5
    sheet.paste(im,(x,y)); d.rectangle([x,y,x+T-1,y+T-1],outline="#ddd")
    d.text((x,y+T+4),lab,fill="black",font=font)
out=sys.argv[2] if len(sys.argv)>2 else "/sessions/keen-intelligent-gates/mnt/outputs/garden_sheet.png"
sheet.save(out); print("tiles",len(tiles),"->",out)
