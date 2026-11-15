import math, json, random
O = "#3b2a1e"
SW = 3
def st(c=O, w=SW): return f'stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'
def P(d, fill, c=O, w=SW, extra=""): return f'<path d="{d}" fill="{fill}" {st(c,w)}{extra}/>'
def C(x,y,r,fill,c=O,w=SW): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {st(c,w)}/>'
def E(x,y,rx,ry,fill,c=O,w=SW,rot=None):
    t = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" {st(c,w)}{t}/>'
def L(d, c=O, w=SW): return f'<path d="{d}" fill="none" {st(c,w)}/>'
def F(d, fill, op=None):  # flat fill no stroke
    o = f' opacity="{op}"' if op else ""
    return f'<path d="{d}" fill="{fill}"{o}/>'
def dot(x,y,r,fill,op=None):
    o = f' opacity="{op}"' if op else ""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{o}/>'
def HL(x,y,rx,ry,rot=-30):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff" opacity=".55" transform="rotate({rot} {x} {y})"/>'
def face(x,y,s=1.0,eye=O):
    sp=6*s; r=2.5*s if s>=1 else max(2.0, 2.5*s)
    g = (f'<circle cx="{x-sp:g}" cy="{y}" r="{r:g}" fill="{eye}"/><circle cx="{x+sp:g}" cy="{y}" r="{r:g}" fill="{eye}"/>'
         f'<path d="M{x-4*s:g} {y+5*s:g}Q{x:g} {y+9*s:g} {x+4*s:g} {y+5*s:g}" fill="none" stroke="{eye}" stroke-width="2.2" stroke-linecap="round"/>')
    return g
def G(fill, c, w, *parts): return f'<g fill="{fill}" stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round">' + ''.join(parts) + '</g>'
def gp(d): return f'<path d="{d}"/>'
def svg(*parts): return '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"
def poly_path(pts):
    return "M" + " ".join(f"{x:.1f} {y:.1f}" for x,y in pts) + "Z"
def smooth_closed(pts):
    # Catmull-Rom -> cubic bezier closed path
    n=len(pts); d=f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p0=pts[i-1]; p1=pts[i]; p2=pts[(i+1)%n]; p3=pts[(i+2)%n]
        c1=(p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6)
        c2=(p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d+=f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d+"Z"
LEAF="#5cb85c"; LEAFD="#3f8f3f"; BROWN="#7a4a2a"

items = {}
def add(letter, name, line, s): items.setdefault(letter, []).append({"name":name,"line":line,"svg":s})

# ---------- A ----------
add("A","Apple","Crunchy and red!", svg(
    P("M50 30C40 20 16 22 16 50C16 76 34 90 50 85C66 90 84 76 84 50C84 22 60 20 50 30Z","#d92b2b"),
    L("M50 31Q49 20 54 11",BROWN,4),
    P("M54 20Q62 8 76 12Q68 25 54 20Z",LEAF),
    HL(30,44,5,10,20), face(50,58)))
add("A","Avocado","Green and creamy!", svg(
    P("M50 10C38 10 36 26 30 38C20 52 18 66 24 78C32 92 68 92 76 78C82 66 80 52 70 38C64 26 62 10 50 10Z","#3e6b23"),
    P("M50 17C42 17 41 29 36 40C27 53 25 65 30 75C36 86 64 86 70 75C75 65 73 53 64 40C59 29 58 17 50 17Z","#d6ea8c","#a9c25a",2),
    C(50,66,13,"#9a5b2c"), HL(46,61,3,5,30), face(50,42,0.8)))
# ---------- B ----------
add("B","Banana","Long and yellow!", svg(
    P("M22 22C10 62 44 90 86 68Q90 64 84 60C56 64 34 48 32 22Z","#ffd83a"),
    P("M21 23L20 13L30 12L32 22Z","#8a5a2b"),
    P("M86 68Q91 64 84 60L82 64Z","#5a3a1a",O,2),
    L("M30 40C34 54 46 64 62 68","#e0b020",2),
    face(44,58,0.85)))
add("B","Broccoli","Green little trees!", svg(
    P("M42 58L38 88Q50 93 62 88L58 58Z","#9ccc65"),
    L("M50 66L50 84","#7cb342",2),
    P("M22 58A13 13 0 0 1 22 36A15 15 0 0 1 44 18A15 15 0 0 1 70 22A14 14 0 0 1 80 44A12 12 0 0 1 70 62Q50 66 22 58Z","#43a047"),
    dot(30,40,3,"#2e7d32"),dot(70,34,3,"#2e7d32"),dot(62,24,2.5,"#2e7d32"),dot(36,26,2.5,"#2e7d32"),
    HL(34,30,4,7,40), face(50,44,0.9)))
def crown(x,y,r=4):
    pts=[]
    for i in range(10):
        a=math.pi*i/5-math.pi/2; rr=r if i%2==0 else r*0.45
        pts.append((x+rr*math.cos(a), y+rr*math.sin(a)))
    return F(poly_path(pts),"#1f2a6b")
add("B","Blueberries","Small, round and blue!", svg(
    C(31,40,18,"#3f51b5"), C(69,40,18,"#3f51b5"),
    crown(29,34), crown(71,34),
    C(50,63,24,"#4a63d0"),
    crown(50,45,3.5),
    HL(37,55,4,8,30), face(50,64)))
# ---------- C ----------
add("C","Carrot","Crunchy and orange!", svg(
    P("M44 30Q34 14 38 8Q46 16 48 28Z",LEAF), P("M52 28Q54 10 62 8Q64 20 56 30Z",LEAF), P("M50 28Q48 12 50 6Q56 14 54 28Z","#4caf50"),
    P("M28 34Q50 22 72 34L55 88Q50 94 45 88Z","#fb8c00"),
    L("M36 48L41 48M57 60L61 60M45 76L48 76","#c25e00",2.5),
    HL(37,40,3,6,-20), face(50,46,0.9)))
add("C","Cherries","Sweet and red!", svg(
    L("M34 56Q38 30 58 14",LEAFD,3), L("M66 52Q64 32 58 14",LEAFD,3),
    P("M58 14Q70 4 84 10Q74 22 58 14Z",LEAF),
    C(66,64,16,"#c2185b"), C(34,68,18,"#e01e3c"),
    HL(26,62,3.5,6,30), HL(60,58,3,5,30), face(34,70,0.9)))
add("C","Corn","Sweet and yellow!", svg(
    P("M50 10C34 10 32 32 32 50C32 70 40 82 50 82C60 82 68 70 68 50C68 32 66 10 50 10Z","#ffd23f"),
    L("M38 22L62 22M35 32L65 32M34 62L66 62M37 72L63 72","#e8a900",2),
    L("M43 13L41 30M57 13L59 30M42 64L43 80M58 64L57 80","#e8a900",2),
    P("M50 92Q22 86 20 44Q30 60 46 70Z","#66bb6a"), P("M50 92Q78 86 80 44Q70 60 54 70Z","#4caf50"),
    HL(40,40,3,6,0), face(50,46,0.9)))
# ---------- D ----------
add("D","Dragon fruit","Pink and spiky!", svg(
    G("#8bc34a",O,3, gp("M40 26Q34 12 44 6Q48 16 50 24Z"), gp("M56 24Q60 10 70 10Q66 20 62 28Z"),
      gp("M24 44Q10 40 8 30Q20 30 30 36Z"), gp("M76 44Q90 40 92 30Q80 30 70 36Z"),
      gp("M22 70Q10 74 8 84Q20 82 28 76Z"), gp("M78 70Q90 74 92 84Q80 82 72 76Z")),
    E(50,56,30,32,"#e8338a"),
    G("#9ccc65",O,2, gp("M28 50Q22 42 24 36Q32 42 34 48Z"), gp("M72 50Q78 42 76 36Q68 42 66 48Z"),
      gp("M36 78Q30 84 32 90Q40 86 42 80Z"), gp("M64 78Q70 84 68 90Q60 86 58 80Z")),
    HL(38,40,4,8,30), face(50,58)))
# ---------- E ----------
add("E","Edamame","Green beans in a pod!", svg(
    P("M8 60Q4 54 10 50",LEAFD),
    P("M10 52Q12 34 30 34Q40 28 50 34Q60 28 70 34Q90 34 90 52Q90 68 70 66Q60 72 50 66Q40 72 30 66Q12 68 10 52Z","#7cb342"),
    C(30,50,12,"#b5dc6e",LEAFD,2.5), C(50,50,13,"#b5dc6e",LEAFD,2.5), C(70,50,12,"#b5dc6e",LEAFD,2.5),
    HL(26,45,2.5,4,30), HL(66,45,2.5,4,30), face(50,49,0.75)))
# ---------- F ----------
add("F","Fig","Soft and sweet!", svg(
    P("M50 20C44 20 44 30 40 36C24 46 16 62 22 76C28 90 72 90 78 76C84 62 76 46 60 36C56 30 56 20 50 20Z","#7b3f8c"),
    L("M38 46Q30 62 34 80M62 46Q70 62 66 80","#5a2a6a",2),
    P("M47 22L46 10Q52 8 54 10L53 22Z","#7cb342"),
    P("M53 14Q66 4 78 12Q68 22 53 14Z",LEAF),
    HL(36,54,4,8,25), face(50,62)))
# ---------- G ----------
gr="#8e44ad"
add("G","Grapes","Juicy and purple!", svg(
    L("M50 22L52 8",BROWN,4), P("M52 12Q66 2 80 10Q68 20 52 12Z",LEAF),
    G(gr,O,3, *[f'<circle cx="{x}" cy="{y}" r="11"/>' for x,y in [(23,30),(41,27),(59,27),(77,30),(32,47),(68,47),(41,64),(59,64),(50,81)]]),
    C(50,47,13,"#a05cc0"),
    HL(26,26,2,4,30),HL(42,42,2.5,5,30), face(50,48,0.8)))
add("G","Garlic","White and smelly!", svg(
    P("M50 8Q47 22 42 28C18 38 14 72 30 84Q50 92 70 84C86 72 82 38 58 28Q53 22 50 8Z","#f7f1e3"),
    L("M42 30Q30 52 36 84M58 30Q70 52 64 84","#c9b9d9",2.2),
    L("M42 88L40 94M50 89L50 95M58 88L60 94","#a08a70",2),
    HL(30,52,3,8,15), face(50,60)))
# ---------- H ----------
add("H","Honeydew","Sweet and green!", svg(
    C(44,42,32,"#cfe69a"),
    L("M26 24Q18 42 24 60M62 20Q72 30 74 44","#b0cf72",2.2),
    P("M38 70L92 70Q90 91 65 91Q40 91 38 70Z","#a8cf5f"),
    F("M43 70L87 70Q85 86 65 86Q45 86 43 70Z","#e4f7c0"),
    dot(55,75,1.6,"#f5f0d0"),dot(65,77,1.6,"#f5f0d0"),dot(75,75,1.6,"#f5f0d0"),
    L("M38 70L92 70Q90 91 65 91Q40 91 38 70Z"),
    HL(30,30,4,8,40), face(44,44)))
# ---------- I ----------
add("I","Iceberg lettuce","Cool and crunchy!", svg(
    C(50,52,34,"#d4ed9a"),
    L("M50 22Q46 40 50 56M34 30Q42 40 44 52M66 30Q58 40 56 52","#a8d060",2),
    P("M50 88C22 88 10 66 16 44Q22 34 30 30Q24 50 30 64Q38 80 50 88Z","#8bc34a"),
    P("M50 88C78 88 90 66 84 44Q78 34 70 30Q76 50 70 64Q62 80 50 88Z","#7cb342"),
    HL(38,36,4,7,40), face(50,62)))
# ---------- J ----------
pts=[]
for i in range(56):
    a=2*math.pi*i/56; r = 1.0 if i%2==0 else 1.07
    pts.append((50+30*r*math.cos(a), 54+36*r*math.sin(a)))
jf = poly_path(pts)
spk=""
for (x,y) in [(36,36),(50,30),(64,36),(32,52),(68,52),(36,74),(50,80),(64,74),(28,66),(72,66),(42,22),(58,22)]:
    spk += f"M{x-2} {y+1.5}L{x} {y-1.5}L{x+2} {y+1.5}"
add("J","Jackfruit","Big and bumpy!", svg(
    L("M50 18Q50 10 56 6",BROWN,4),
    P(jf,"#b8c43a"),
    L(spk,"#7f8f1a",1.8),
    HL(34,42,3,7,25), face(50,56)))
# ---------- K ----------
seeds=""
for i in range(12):
    a=2*math.pi*i/12; x=50+17*math.cos(a); y=46+17*math.sin(a)
    if 0.6 < a < 2.5:  # skip bottom area for face
        continue
    seeds+=f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="1.6" ry="3" fill="#222" transform="rotate({math.degrees(a)+90:.0f} {x:.1f} {y:.1f})"/>'
add("K","Kiwi","Green and fuzzy!", svg(
    C(50,50,40,"#8b6a3e"),
    C(50,50,34,"#7cc242","#5f9a2c",2),
    E(50,46,8,10,"#f2f8d8","#d0e3a0",1.5),
    seeds, HL(30,34,3,7,40), face(50,70,0.9)))
# ---------- L ----------
add("L","Lemon","Sour and yellow!", svg(
    P("M10 54Q12 48 18 46C26 22 74 22 82 46Q88 48 90 54Q88 60 82 62C74 86 26 86 18 62Q12 60 10 54Z","#ffe23a"),
    P("M50 26Q58 12 74 14Q66 28 50 26Z",LEAF),
    HL(32,42,4,8,50), face(50,56)))
add("L","Lime","Small, green and sour!", svg(
    P("M84 52Q90 52 90 56Q88 60 84 58Z","#5c9a25"),
    C(52,56,32,"#7cbf3a","#3b2a1e"),
    P("M52 24Q48 12 36 10Q36 24 52 24Z",LEAF),
    dot(66,44,1.4,"#5c9a25"),dot(70,62,1.4,"#5c9a25"),dot(38,74,1.4,"#5c9a25"),dot(60,76,1.4,"#5c9a25"),
    HL(38,42,4,7,40), face(52,58)))
# ---------- M ----------
add("M","Mango","Sweet and juicy!", svg(
    P("M58 16C82 18 92 48 82 70C72 90 40 94 24 80C12 68 18 46 34 38C46 32 44 16 58 16Z","#ffb300"),
    F("M58 16C82 18 92 48 82 70C76 62 70 44 58 36Q50 30 54 17Z","#f4511e",".75"),
    L("M58 17Q58 10 62 6",BROWN,3.5), P("M60 10Q72 2 84 8Q74 18 60 10Z",LEAF),
    L("M58 16C82 18 92 48 82 70C72 90 40 94 24 80C12 68 18 46 34 38C46 32 44 16 58 16Z"),
    HL(34,52,4,8,30), face(52,62)))
add("M","Mushroom","Soft and brown!", svg(
    P("M38 52L35 84Q50 92 65 84L62 52Z","#f6e7c8"),
    P("M12 54C10 20 90 20 88 54Q50 62 12 54Z","#b06a3a"),
    dot(34,36,4,"#d9a47a"),dot(64,32,3,"#d9a47a"),dot(72,46,3.5,"#d9a47a"),
    HL(28,40,3,6,40), face(50,70,0.85)))
# ---------- N ----------
add("N","Nectarine","Smooth and sweet!", svg(
    C(50,56,34,"#ffb52e"),
    F("M50 22A34 34 0 0 1 84 56Q82 74 66 84Q60 60 40 46Q30 30 50 22Z","#e8402c",".9"),
    L("M48 24Q34 38 36 64","#c0392b",2.5),
    C(50,56,34,"none"),
    P("M50 24Q50 14 52 10",BROWN,O,3),
    P("M52 16Q62 6 76 10Q68 22 52 16Z",LEAF), P("M50 16Q40 6 28 12Q38 22 50 16Z","#6cc26c"),
    HL(30,50,3.5,7,15), face(60,60)))
# ---------- O ----------
add("O","Orange","Round and juicy!", svg(
    C(50,54,34,"#ff9a1f"),
    P("M50 20Q56 8 70 10Q64 22 50 20Z",LEAF),
    dot(50,22,2.5,"#6b8e23"),
    dot(68,40,1.3,"#e07b00"),dot(72,54,1.3,"#e07b00"),dot(66,72,1.3,"#e07b00"),dot(32,70,1.3,"#e07b00"),dot(60,30,1.3,"#e07b00"),
    HL(34,40,4,8,40), face(50,58)))
add("O","Onion","Crunchy and purple!", svg(
    L("M44 86L42 94M50 88L50 95M56 86L58 94","#a08a70",2),
    P("M50 6Q48 20 44 24C14 30 12 74 32 84Q50 92 68 84C88 74 86 30 56 24Q52 20 50 6Z","#b04a8a"),
    L("M44 26Q28 50 38 84M56 26Q72 50 62 84","#83306a",2),
    HL(30,48,3.5,8,15), face(50,60)))
# ---------- P ----------
add("P","Pear","Soft and sweet!", svg(
    P("M50 20C40 20 40 34 36 44C22 54 18 70 26 80C34 92 66 92 74 80C82 70 78 54 64 44C60 34 60 20 50 20Z","#b5d33a"),
    L("M50 21Q50 12 54 7",BROWN,4), P("M54 14Q66 6 76 12Q66 22 54 14Z",LEAF),
    HL(34,62,3.5,7,15), face(50,66)))
cross="".join(f"M{30+i*10} 36L{20+i*10} 90" for i in range(0,1))
add("P","Pineapple","Spiky and sweet!", svg(
    P("M50 34Q40 18 30 12Q42 14 46 22Q44 8 50 2Q56 8 54 22Q58 14 70 12Q60 18 50 34Z","#4caf50"),
    P("M38 34Q32 26 24 26Q30 34 40 38Z","#43a047"), P("M62 34Q68 26 76 26Q70 34 60 38Z","#43a047"),
    E(50,64,26,30,"#ffc928"),
    L("M30 48L60 90M40 38L72 82M28 66L46 92M54 36L76 66M70 48L40 90M60 38L28 82M72 66L54 92M46 36L24 66","#d79a00",2),
    E(50,64,26,30,"none"),
    HL(34,54,3,7,15), face(50,64)))
add("P","Pumpkin","Big and orange!", svg(
    L("M50 26Q50 14 58 10","#6d4c1d",6),
    E(30,58,18,28,"#f57c00"), E(70,58,18,28,"#f57c00"), E(50,58,20,30,"#fb8c00"),
    P("M58 16Q72 10 80 20Q68 26 58 16Z",LEAF),
    HL(42,42,3,6,15), face(50,60)))
# ---------- Q ----------
random.seed(3)
qp=[(50,20),(58,22),(64,30),(68,38),(78,46),(84,58),(82,72),(72,84),(58,90),(50,88),(40,90),(26,84),(18,72),(18,58),(24,46),(34,38),(38,30),(42,22)]
add("Q","Quince","Golden and fuzzy!", svg(
    L("M50 21Q49 12 52 8",BROWN,4), P("M52 12Q68 0 86 8Q72 22 52 12Z",LEAF), L("M56 12Q70 8 80 9",LEAFD,1.5),
    P(smooth_closed(qp),"#f2c018"),
    L("M24 60l-2 1M76 56l2 1M30 76l-2 2M70 78l2 2M50 86l0 2M36 44l-2 -1M64 44l2 -1","#c89a00",1.8),
    dot(34,62,1.3,"#c89a00"),dot(68,66,1.3,"#c89a00"),dot(56,34,1.3,"#c89a00"),dot(42,78,1.3,"#c89a00"),
    HL(30,58,3.5,7,15), face(50,62)))
# ---------- R ----------
add("R","Radish","Crunchy and pink!", svg(
    P("M44 32Q36 14 26 8Q24 22 40 34Z",LEAF), P("M56 32Q64 14 74 8Q76 22 60 34Z",LEAF), P("M50 30Q46 12 50 4Q56 12 52 30Z","#4caf50"),
    L("M50 82L50 96",O,2.5),
    P("M50 30C24 30 18 50 24 64C30 78 44 84 50 84C56 84 70 78 76 64C82 50 76 30 50 30Z","#e3245c"),
    F("M38 78Q50 88 62 78Q56 84 50 84Q44 84 38 78Z","#fff"),
    HL(32,46,3.5,6,30), face(50,56)))
rasp=G("#ef4a6a","#b81d42",1.5,*[f'<circle cx="{x}" cy="{y}" r="6"/>' for (x,y) in [(36,42),(50,40),(64,42),(30,56),(70,56),(36,70),(64,70),(44,82),(56,82),(50,70),(42,56),(58,56)]])
add("R","Raspberry","Soft and sweet!", svg(
    P("M50 30C26 30 18 46 22 62C26 80 40 92 50 92C60 92 74 80 78 62C82 46 74 30 50 30Z","#e83358"),
    rasp,
    P("M50 34L38 26L44 22L50 18L56 22L62 26Z","#66bb6a",O,2.5), L("M50 18L50 8",LEAFD,3),
    C(50,58,12,"#ef4a6a","#b81d42",1.5),
    HL(32,50,2.5,5,30), face(50,57,0.8)))
# ---------- S ----------
seedsS=""
for (x,y) in [(30,46),(70,46),(40,64),(60,64),(50,80),(26,60),(74,60),(36,80),(64,80)]:
    seedsS+=f'<ellipse cx="{x}" cy="{y}" rx="1.6" ry="2.5" fill="#ffe36b"/>'
add("S","Strawberry","Red and sweet!", svg(
    P("M50 30C30 22 12 30 14 48C16 66 36 84 50 92C64 84 84 66 86 48C88 30 70 22 50 30Z","#e8273b"),
    seedsS,
    P("M50 34L36 38L40 30L28 26L42 24L44 16L50 22L56 16L58 24L72 26L60 30L64 38Z","#4caf50",O,2.5),
    L("M50 22L52 10",LEAFD,3.5),
    HL(28,44,3.5,6,30), face(50,52)))
# ---------- T ----------
add("T","Tomato","Red and juicy!", svg(
    E(50,58,38,32,"#f2412e"),
    P("M50 30L40 34L28 30L36 40L28 44L42 42L50 48L58 42L72 44L64 40L72 30L60 34Z","#3fa34d",O,2.5),
    L("M50 32L50 20",LEAFD,4),
    HL(28,52,4,8,20), face(50,64)))
# ---------- U ----------
pts=[]
random.seed(7)
for i in range(18):
    a=2*math.pi*i/18; r=34+ (3 if i%2 else -1) + random.uniform(-1.5,1.5)
    pts.append((50+r*math.cos(a), 54+r*0.92*math.sin(a)))
add("U","Ugli fruit","Bumpy and juicy!", svg(
    P(smooth_closed(pts),"#c9d64a"),
    F("M24 70Q30 80 40 82Q30 76 28 66Z","#93b52a"), F("M70 30Q80 36 82 48Q74 40 66 36Z","#93b52a"),
    F("M58 78Q70 76 76 66Q72 78 62 82Z","#e6c53a"), F("M30 32Q38 26 46 26Q38 30 34 38Z","#e6c53a"),
    P("M50 22Q48 16 52 14Q56 16 54 22Z","#6b8e23",O,2),
    dot(66,50,1.3,"#8aa02a"),dot(36,66,1.3,"#8aa02a"),dot(62,68,1.3,"#8aa02a"),
    HL(34,44,4,7,40), face(50,56)))
# ---------- V ----------
add("V","Vegetable soup","Warm and yummy!", svg(
    L("M36 26Q30 18 36 12Q42 6 36 2M50 24Q44 16 50 10Q56 4 50 0M64 26Q58 18 64 12Q70 6 64 2","#b0bec5",2.5),
    P("M10 46Q12 88 50 90Q88 88 90 46Z","#42a5f5"),
    E(50,46,40,9,"#f4a742"),
    C(32,46,4,"#ff7a1a",O,1.5), C(62,44,4,"#ff7a1a",O,1.5),
    dot(44,48,3,"#5cb85c"), dot(72,48,3,"#5cb85c"), dot(22,46,2.6,"#5cb85c"),
    P("M50 42h5v5h-5Z M76 42h5v5h-5Z","#ffe14d",O,1.2),
    L("M24 90L76 90",O,3),
    HL(24,62,3,7,-20), face(50,68)))
# ---------- W ----------
sd=""
for (x,y,r) in [(30,50,-30),(44,58,-10),(56,58,10),(70,50,30),(38,70,-20),(62,70,20)]:
    sd+=f'<ellipse cx="{x}" cy="{y}" rx="1.8" ry="3.2" fill="#2b1a12" transform="rotate({r} {x} {y})"/>'
add("W","Watermelon","Red, sweet and juicy!", svg(
    P("M8 36L92 36A42 42 0 0 1 8 36Z","#3a9a3f"),
    F("M14 36L86 36A36 36 0 0 1 14 36Z","#e9f7d2"),
    P("M18 36L82 36A32 32 0 0 1 18 36Z","#f2445a","#f2445a",1),
    sd.replace('38','38',1),
    L("M8 36L92 36A42 42 0 0 1 8 36Z"),
    HL(26,44,3,6,-40), face(50,46)))
# ---------- X ----------
stripes="M50 20Q42 36 50 52Q42 70 50 86 M32 26Q22 40 28 56Q22 70 30 80 M68 26Q78 40 72 56Q78 70 70 80 M18 40Q12 54 18 68 M82 40Q88 54 82 68"
add("X","Xigua","A big round melon!", svg(
    E(50,54,38,34,"#6cc04a"),
    L(stripes,"#2e7d32",5),
    E(50,54,38,34,"none"),
    L("M50 20Q50 14 54 12",BROWN,3),
    HL(34,36,4,7,50), face(50,56,1,"#1b1b1b")))
# ---------- Y ----------
yp=[(8,66),(16,56),(30,48),(46,42),(60,34),(74,28),(84,28),(90,36),(90,48),(82,54),(68,60),(54,68),(40,76),(26,78),(14,74)]
add("Y","Yam","Sweet and orange inside!", svg(
    L("M8 66L3 68M30 48L27 42M58 66L60 72M40 76L38 82","#5a2f38",2),
    P(smooth_closed(yp),"#9a566a"),
    E(84,41,7,12,"#ffa94d",O,3,rot=20), dot(84,41,3,"#ffc27a"),
    L("M20 66Q24 62 28 64M64 46Q68 42 72 44M30 72Q34 68 38 70","#6e3546",2),
    HL(30,58,3,7,60), face(48,55)))
# ---------- Z ----------
add("Z","Zucchini","Long and green!", svg(
    P("M80 14Q90 10 92 18Q90 24 84 22Z","#8bab4a",O,2.5),
    P("M20 88C10 84 10 72 16 66L74 16C80 12 88 18 86 26L36 82C30 88 26 90 20 88Z","#2f8a3a"),
    L("M24 74L70 28M34 76L78 32","#7bc47f",2),
    dot(30,66,1.2,"#c8e6c9"),dot(54,48,1.2,"#c8e6c9"),dot(62,34,1.2,"#c8e6c9"),
    HL(26,70,2.5,6,45), face(48,52,0.9,"#13331a")))

# Extra pictures from garden_more_*.py (each defines add_more(K) and calls K.add(...)).
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from svgkit import add_extensions
class _Shim:
    items = items
    add = staticmethod(add)
add_extensions(_Shim, "garden")
order=[chr(c) for c in range(65,91)]
out=["// ==GARDEN START==","// Garden world: fruit & vegetables A–Z, all hand-made SVG (viewBox 0 0 100 100).","const GARDEN_ITEMS = {"]
for i,k in enumerate(order):
    arr=items[k]
    out.append(f"  {k}: [")
    for j,it in enumerate(arr):
        s=it["svg"]; assert "`" not in s and "${" not in s
        comma = "," if j<len(arr)-1 else ""
        out.append(f'    {{ name: {json.dumps(it["name"])}, line: {json.dumps(it["line"])}, svg: `{s}` }}{comma}')
    out.append("  ]" + ("," if i<len(order)-1 else ""))
out.append("};"); out.append("// ==GARDEN END=="); out.append('if (typeof module !== "undefined") module.exports = GARDEN_ITEMS;')
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "garden.js"),"w",encoding="utf-8",newline="\n").write("\n".join(out)+"\n")
print("ok", sum(len(v) for v in items.values()))
