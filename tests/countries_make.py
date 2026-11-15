"""Countries world: a country flag for every letter, as hand-made SVG.  Writes tests/countries.js.

Run:  python tests/countries_make.py   then   python tests/pack_sheet.py tests/countries.js countries_sheet.png

Each picture is the flag on a little flag pole.  Flags are drawn in their own "native"
units inside <g transform="translate scale"> so the geometry can follow the official
construction sheets.  There are no ids, so no <clipPath>: anything that a real flag
would clip (Union Jack diagonals, the South African Y, ...) is clipped here with plain
polygon maths (clip_convex) before it is written out.

Emblems with fine detail (Mexico, Egypt, Kenya, Lebanon, Oman, Zambia, Nepal) are
simplified so they still read at picture size; colours and layout follow the real flags.
X has no country, so X is a treasure map ("X marks the spot"), and W is the World.
"""
import math
import os
from svgkit import *

K = Pack()


# ---------------------------------------------------------------- geometry helpers
def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pd(pts):
    """Polygon -> path data."""
    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts) + "Z"


def clip_half(poly, nx, ny, c):
    """Keep the part of poly with nx*x + ny*y >= c (Sutherland-Hodgman, one edge)."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = nx * p[0] + ny * p[1] - c
        fq = nx * q[0] + ny * q[1] - c
        if fp >= 0:
            out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def area2(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def halfplanes(conv, inset=0.0):
    """Inward half-planes of a convex polygon (optionally moved inwards by `inset`)."""
    s = 1 if area2(conv) > 0 else -1
    hp = []
    for i in range(len(conv)):
        (x1, y1), (x2, y2) = conv[i], conv[(i + 1) % len(conv)]
        nx, ny = -(y2 - y1) * s, (x2 - x1) * s
        ln = math.hypot(nx, ny)
        nx, ny = nx / ln, ny / ln
        hp.append((nx, ny, nx * x1 + ny * y1 + inset))
    return hp


def clip_convex(poly, conv):
    for nx, ny, c in halfplanes(conv):
        poly = clip_half(poly, nx, ny, c)
        if not poly:
            break
    return poly


def rect_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def band(p, q, o1, o2, ext=0.0):
    """Strip along p->q between normal offsets o1..o2 (normal = direction rotated +90deg)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    a = (p[0] - ux * ext, p[1] - uy * ext)
    b = (q[0] + ux * ext, q[1] + uy * ext)
    return [(a[0] + nx * o1, a[1] + ny * o1), (b[0] + nx * o1, b[1] + ny * o1),
            (b[0] + nx * o2, b[1] + ny * o2), (a[0] + nx * o2, a[1] + ny * o2)]


def poly(pts, fill):
    return F(pd(pts), fill) if pts else ""


def star(x, y, r, fill, n=5, inner=0.382, rot=-90):
    return F(star_path(x, y, r, inner=inner, n=n, rot=rot), fill)


def circ(x, y, r, fill):
    return f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{fill}"/>'


def rect(x, y, w, h, fill):
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}"/>'


def hstripes(W, H, cols, weights=None):
    weights = weights or [1] * len(cols)
    tot, y, out = sum(weights), 0.0, []
    for c, w in zip(cols, weights):
        h = H * w / tot
        out.append(rect(0, y, W, h + 0.02, c))
        y += h
    return "".join(out)


def vstripes(W, H, cols, weights=None):
    weights = weights or [1] * len(cols)
    tot, x, out = sum(weights), 0.0, []
    for c, w in zip(cols, weights):
        ww = W * w / tot
        out.append(rect(x, 0, ww + 0.02, H, c))
        x += ww
    return "".join(out)


def lines(d, c, w, cap="round"):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{fmt(w)}" stroke-linecap="{cap}" stroke-linejoin="round"/>'


# ---------------------------------------------------------------- flag on a pole
POLE = "#8d6e63"
GOLDBALL = "#ffca28"
FX, FY, FW, FH = 15.0, 15.0, 80.0, 60.0     # flag area (left/top fixed; size follows ratio)


def on_pole(nw, nh, content, ratio=None, outline=None):
    """Draw flag `content` (native units nw x nh) on a pole.  `outline` = custom shape (native)."""
    ratio = ratio or nw / nh
    w = FW
    h = w / ratio
    if h > FH:
        h = FH
        w = h * ratio
    sx, sy = w / nw, h / nh
    g = f'<g transform="translate({fmt(FX)} {fmt(FY)}) scale({sx:.6g} {sy:.6g})">{content}</g>'
    if outline is None:
        frame = f'<rect x="{fmt(FX)}" y="{fmt(FY)}" width="{fmt(w)}" height="{fmt(h)}" rx="1.5" fill="none" {st()}/>'
    else:
        pts = [(FX + x * sx, FY + y * sy) for x, y in outline]
        frame = f'<path d="{pd(pts)}" fill="none" {st()}/>'
    pole = (R(8.5, 10, 5, 86, POLE, 2.5) + C(11, 9, 4.5, GOLDBALL)
            + E(11, 95, 9, 3, "#a1887f"))
    # little ties that hold the flag on the pole
    ties = (R(10, FY + 1.5, 7, 3.4, "#fff", 1.5, O, 2) + R(10, FY + h - 4.9, 7, 3.4, "#fff", 1.5, O, 2))
    return svg(pole, g, frame, ties)


# ---------------------------------------------------------------- Union Jack (native 60 x 30)
def union_jack(red="#C8102E", blue="#012169"):
    box = rect_pts(0, 0, 60, 30)
    out = [rect(0, 0, 60, 30, blue)]
    for p, q in (((0, 0), (60, 30)), ((0, 30), (60, 0))):
        out.append(poly(clip_convex(band(p, q, -3, 3, 5), box), "#fff"))
    # counterchanged red saltire: red sits below the diagonal in the hoist and above it in the fly
    regions = [[(0, 0), (0, 15), (30, 15)], [(30, 15), (60, 15), (60, 30)],      # for (0,0)-(60,30)
               [(60, 0), (30, 0), (30, 15)], [(30, 15), (0, 30), (30, 30)]]      # for (0,30)-(60,0)
    for i, reg in enumerate(regions):
        p, q = ((0, 0), (60, 30)) if i < 2 else ((0, 30), (60, 0))
        for o1, o2 in ((-2, 0), (0, 2)):
            out.append(poly(clip_convex(band(p, q, o1, o2, 5), reg), red))
    out.append(rect(25, 0, 10, 30, "#fff") + rect(0, 10, 60, 10, "#fff"))
    out.append(rect(27, 0, 6, 30, red) + rect(0, 12, 60, 6, red))
    return "".join(out)


STAR7 = dict(n=7, inner=0.444)


# ================================================================ A
K.add("A", "Australia", "G'day! Kangaroos hop here!", on_pole(120, 60, "".join([
    rect(0, 0, 120, 60, "#012169"),
    union_jack(red="#E4002B"),
    star(30, 45, 9, "#fff", **STAR7),
    star(90, 50, 4.3, "#fff", **STAR7), star(75, 26.25, 4.3, "#fff", **STAR7),
    star(90, 10, 4.3, "#fff", **STAR7), star(103.33, 22.25, 4.3, "#fff", **STAR7),
    star(96, 32.5, 2.5, "#fff", inner=0.444),
])))


def sun_of_may(cx, cy, s):
    out = []
    for k in range(32):
        a = math.radians(k * 360 / 32 - 90)
        r_out = (12.5 if k % 2 == 0 else 10.8) * s
        w = 0.07 if k % 2 == 0 else 0.06
        pts = [(cx + 5.4 * s * math.cos(a - w * 1.6), cy + 5.4 * s * math.sin(a - w * 1.6)),
               (cx + r_out * math.cos(a), cy + r_out * math.sin(a)),
               (cx + 5.4 * s * math.cos(a + w * 1.6), cy + 5.4 * s * math.sin(a + w * 1.6))]
        out.append(poly(pts, "#F6B40E"))
    out.append(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(5.6 * s)}" fill="#F6B40E" stroke="#85340A" stroke-width="{fmt(0.5 * s)}"/>')
    out.append(circ(cx - 1.9 * s, cy - 0.8 * s, 0.6 * s, "#85340A") + circ(cx + 1.9 * s, cy - 0.8 * s, 0.6 * s, "#85340A"))
    out.append(lines(f"M{fmt(cx - 1.6 * s)} {fmt(cy + 1.9 * s)}Q{fmt(cx)} {fmt(cy + 3 * s)} {fmt(cx + 1.6 * s)} {fmt(cy + 1.9 * s)}", "#85340A", 0.45 * s))
    return "".join(out)


K.add("A", "Argentina", "Hola! A happy sun on the flag!", on_pole(140, 90, "".join([
    hstripes(140, 90, ["#74ACDF", "#fff", "#74ACDF"]),
    sun_of_may(70, 45, 1.1),
])))

# ================================================================ B
def brazil():
    out = [rect(-2100, -1470, 4200, 2940, "#009440"),
           F("M-1743 0L0 1113L1743 0L0-1113Z", "#ffcb00"),
           circ(0, 0, 735, "#302681")]

    def inter(R):     # intersections of circle (centre (-420,1470), radius R) with the globe r=735
        cx, cy = -420.0, 1470.0
        d = math.hypot(cx, cy)
        a = (735 ** 2 - R ** 2 + d ** 2) / (2 * d)
        hh = math.sqrt(735 ** 2 - a ** 2)
        mx, my = a * cx / d, a * cy / d
        p1 = (mx + hh * cy / d, my - hh * cx / d)
        p2 = (mx - hh * cy / d, my + hh * cx / d)
        return sorted([p1, p2])          # left point first
    (ol, orr), (il, ir) = inter(1785), inter(1680)
    out.append(F(f"M{fmt(ol[0])} {fmt(ol[1])}A1785 1785 0 0 1 {fmt(orr[0])} {fmt(orr[1])}"
                 f"A735 735 0 0 1 {fmt(ir[0])} {fmt(ir[1])}A1680 1680 0 0 0 {fmt(il[0])} {fmt(il[1])}"
                 f"A735 735 0 0 1 {fmt(ol[0])} {fmt(ol[1])}Z", "#fff"))
    stars = [(-600, -132, 31.5), (-535, 177, 31.5), (-625, 243, 26.25), (-463, 132, 15), (-382, 250, 26.25),
             (-404, 323, 21), (228, -228, 31.5), (515, 258, 31.5), (617, 265, 21), (545, 323, 26.25),
             (368, 477, 26.25), (367, 551, 21), (441, 419, 21), (500, 382, 26.25), (365, 405, 21),
             (-280, 30, 26.25), (200, -37, 21), (0, 330, 31.5), (85, 184, 26.25), (0, 118, 26.25),
             (-74, 184, 21), (-37, 235, 15), (220, 495, 26.25), (283, 430, 21), (162, 412, 21),
             (-295, 390, 31.5), (0, 575, 10.5)]
    for x, y, r in stars:
        out.append(star(x, y, r * 1.6, "#fff"))     # a little bigger than real so they stay visible
    return f'<g transform="translate(2100 1470)">{"".join(out)}</g>'


K.add("B", "Brazil", "Ola! Let's play football!", on_pole(4200, 2940, brazil()))

# ================================================================ C
LEAF = ("m4890 4430-45-863a95 95 0 0 1 111-98l859 151-116-320a65 65 0 0 1 20-73l941-762-212-99a65 65 0 0 1-34-79"
        "l186-572-542 115a65 65 0 0 1-73-38l-105-247-423 454a65 65 0 0 1-111-57l204-1052-327 189a65 65 0 0 1-91-27"
        "l-332-652-332 652a65 65 0 0 1-91 27l-327-189 204 1052a65 65 0 0 1-111 57l-423-454-105 247a65 65 0 0 1-73 38"
        "l-542-115 186 572a65 65 0 0 1-34 79l-212 99 941 762a65 65 0 0 1 20 73l-116 320 859-151a95 95 0 0 1 111 98l-45 863z")
K.add("C", "Canada", "Hello! Look, a maple leaf!", on_pole(9600, 4800, "".join([
    rect(0, 0, 9600, 4800, "#D52B1E"), rect(2400, 0, 4800, 4800, "#fff"), F(LEAF, "#D52B1E"),
])))


def china():
    out = [rect(0, 0, 30, 20, "#EE1C25"), star(5, 5, 3, "#FFFF00")]
    for x, y in ((10, 2), (12, 4), (12, 7), (10, 9)):
        rot = math.degrees(math.atan2(5 - y, 5 - x))
        out.append(star(x, y, 1, "#FFFF00", rot=rot))
    return "".join(out)


K.add("C", "China", "Ni hao! Pandas live here!", on_pole(30, 20, china()))

# ================================================================ D
K.add("D", "Denmark", "Hej! Lots of bikes here!", on_pole(37, 28, "".join([
    rect(0, 0, 37, 28, "#C8102E"), rect(12, 0, 4, 28, "#fff"), rect(0, 12, 37, 4, "#fff"),
])))

# ================================================================ E
def egypt_eagle(cx, cy, s):
    g = "#C09300"
    d = "#8a6a00"
    parts = [
        # wings raised up, feathers as scallops
        F(f"M{cx - 2} {cy - 4}C{cx - 6} {cy - 10} {cx - 11} {cy - 12} {cx - 12} {cy - 8}"
          f"C{cx - 13} {cy - 3} {cx - 10} {cy + 2} {cx - 6} {cy + 4}Z", g),
        F(f"M{cx + 2} {cy - 4}C{cx + 6} {cy - 10} {cx + 11} {cy - 12} {cx + 12} {cy - 8}"
          f"C{cx + 13} {cy - 3} {cx + 10} {cy + 2} {cx + 6} {cy + 4}Z", g),
        lines(f"M{cx - 10} {cy - 7}L{cx - 6} {cy - 1}M{cx - 8} {cy - 9}L{cx - 4} {cy - 3}"
              f"M{cx + 10} {cy - 7}L{cx + 6} {cy - 1}M{cx + 8} {cy - 9}L{cx + 4} {cy - 3}", d, 0.5),
        # tail and feet
        F(f"M{cx - 4} {cy + 6}L{cx} {cy + 11}L{cx + 4} {cy + 6}Z", g),
        # body
        F(f"M{cx - 5} {cy - 4}H{cx + 5}V{cy + 4}C{cx + 5} {cy + 7} {cx - 5} {cy + 7} {cx - 5} {cy + 4}Z", g),
        # shield on the chest (white with red and black stripes, like the flag)
        F(f"M{cx - 3.2} {cy - 2.6}H{cx + 3.2}V{cy + 2.6}C{cx + 3.2} {cy + 4.8} {cx - 3.2} {cy + 4.8} {cx - 3.2} {cy + 2.6}Z", "#fff"),
        F(f"M{cx - 3.2} {cy - 2.6}H{cx - 1.1}V{cy + 4.2}C{cx - 2} {cy + 3.8} {cx - 3.2} {cy + 3.4} {cx - 3.2} {cy + 2.6}Z", "#CE1126"),
        F(f"M{cx + 3.2} {cy - 2.6}H{cx + 1.1}V{cy + 4.2}C{cx + 2} {cy + 3.8} {cx + 3.2} {cy + 3.4} {cx + 3.2} {cy + 2.6}Z", "#000"),
        # neck + head looking to the hoist
        F(f"M{cx - 2.5} {cy - 4}C{cx - 3} {cy - 7} {cx - 2} {cy - 9} {cx} {cy - 9.5}"
          f"C{cx + 2} {cy - 9} {cx + 2.5} {cy - 7} {cx + 2.5} {cy - 4}Z", g),
        F(f"M{cx - 1} {cy - 9}L{cx - 4.2} {cy - 7.6}L{cx - 1} {cy - 6.8}Z", g),
        circ(cx - 0.6, cy - 8.1, 0.45, d),
        # scroll under the feet
        F(f"M{cx - 7} {cy + 10}H{cx + 7}V{cy + 12.5}H{cx - 7}Z", g),
    ]
    return T(f"translate({cx} {cy}) scale({s}) translate({-cx} {-cy})", *parts)


K.add("E", "Egypt", "Marhaba! Look at the pyramids!", on_pole(90, 60, "".join([
    hstripes(90, 60, ["#CE1126", "#fff", "#000"]), egypt_eagle(45, 30, 0.82),
])))

# ================================================================ F
K.add("F", "France", "Bonjour! See the Eiffel Tower!", on_pole(90, 60, vstripes(90, 60, ["#002395", "#fff", "#ED2939"])))

# ================================================================ G
K.add("G", "Germany", "Hallo! Yummy pretzels!", on_pole(5, 3, hstripes(5, 3, ["#000", "#DD0000", "#FFCE00"])))


def greece():
    out = []
    for i in range(9):
        out.append(rect(0, i * 2, 27, 2.02, "#0D5EAF" if i % 2 == 0 else "#fff"))
    out.append(rect(0, 0, 10, 10, "#0D5EAF") + rect(4, 0, 2, 10, "#fff") + rect(0, 4, 10, 2, "#fff"))
    return "".join(out)


K.add("G", "Greece", "Yassou! Blue sea and white houses!", on_pole(27, 18, greece()))

# ================================================================ H
K.add("H", "Hungary", "Szia! Red, white and green!", on_pole(2, 1, hstripes(2, 1, ["#CE2939", "#fff", "#477050"])))

# ================================================================ I
def chakra(cx, cy, r):
    navy = "#000080"
    sp = "".join(f"M{fmt(cx)} {fmt(cy)}L{fmt(cx + r * 0.92 * math.cos(math.radians(k * 15)))} {fmt(cy + r * 0.92 * math.sin(math.radians(k * 15)))}"
                 for k in range(24))
    return (f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="{fmt(r * 0.94)}" fill="none" stroke="{navy}" stroke-width="{fmt(r * 0.12)}"/>'
            + lines(sp, navy, r * 0.06, "butt") + circ(cx, cy, r * 0.18, navy))


K.add("I", "India", "Namaste! Elephants and tigers!", on_pole(90, 60, hstripes(90, 60, ["#FF9933", "#fff", "#138808"]) + chakra(45, 30, 8.6)))
K.add("I", "Italy", "Ciao! Pizza and pasta!", on_pole(90, 60, vstripes(90, 60, ["#009246", "#fff", "#CE2B37"])))

# ================================================================ J
K.add("J", "Japan", "Konnichiwa! A big red sun!", on_pole(90, 60, rect(0, 0, 90, 60, "#fff") + circ(45, 30, 18, "#BC002D")))


def jamaica():
    box = rect_pts(0, 0, 120, 60)
    return "".join([rect(0, 0, 120, 60, "#000"),
                    poly([(0, 0), (120, 0), (60, 30)], "#009B3A"), poly([(0, 60), (120, 60), (60, 30)], "#009B3A"),
                    poly(clip_convex(band((0, 0), (120, 60), -5, 5, 8), box), "#FED100"),
                    poly(clip_convex(band((0, 60), (120, 0), -5, 5, 8), box), "#FED100")])


K.add("J", "Jamaica", "Sunny beaches and happy music!", on_pole(120, 60, jamaica()))

# ================================================================ K
def kenya():
    out = [hstripes(90, 60, ["#000", "#fff", "#BB0000", "#fff", "#006600"], [6, 1, 6, 1, 6])]
    # crossed white spears behind the shield
    for (x1, y1, x2, y2) in ((33, 7, 57, 53), (57, 7, 33, 53)):
        out.append(lines(f"M{x1} {y1}L{x2} {y2}", "#fff", 1.6))
        ux, uy = (x2 - x1), (y2 - y1)
        ln = math.hypot(ux, uy); ux, uy = ux / ln, uy / ln
        nx, ny = -uy, ux
        tip = (x1 - ux * 2, y1 - uy * 2)
        base = (x1 + ux * 6, y1 + uy * 6)
        mid = (x1 + ux * 2.5, y1 + uy * 2.5)
        out.append(poly([tip, (mid[0] + nx * 2.2, mid[1] + ny * 2.2), base, (mid[0] - nx * 2.2, mid[1] - ny * 2.2)], "#fff"))
    # Maasai shield: black edges, red middle, white marks
    out.append(F("M45 6C58 16 58 44 45 54C32 44 32 16 45 6Z", "#000"))
    out.append(F("M45 9C52 18 52 42 45 51C38 42 38 18 45 9Z", "#BB0000"))
    out.append(F("M45 22C47.6 25 47.6 35 45 38C42.4 35 42.4 25 45 22Z", "#fff"))
    out.append(lines("M40.5 19Q45 16.5 49.5 19M40.5 41Q45 43.5 49.5 41", "#fff", 1.4))
    out.append(F("M45 25.5C46.2 27.5 46.2 32.5 45 34.5C43.8 32.5 43.8 27.5 45 25.5Z", "#BB0000"))
    return "".join(out)


K.add("K", "Kenya", "Jambo! Lions and zebras!", on_pole(90, 60, kenya()))

# ================================================================ L
def lebanon():
    g = "#00A651"
    out = [hstripes(90, 60, ["#ED1C24", "#fff", "#ED1C24"], [1, 2, 1])]
    tiers = [(15.6, 7), (19.5, 11), (24, 15.5), (28.8, 19.5), (33.6, 23.5)]
    for y, half in tiers:
        out.append(F(f"M45 {y - 5.2}C{45 + half * 0.35} {y - 2.6} {45 + half * 0.8} {y - 0.5} {45 + half} {y + 1.6}"
                     f"C{45 + half * 0.55} {y + 0.6} {45 + half * 0.3} {y + 1.8} 45 {y + 0.6}"
                     f"C{45 - half * 0.3} {y + 1.8} {45 - half * 0.55} {y + 0.6} {45 - half} {y + 1.6}"
                     f"C{45 - half * 0.8} {y - 0.5} {45 - half * 0.35} {y - 2.6} 45 {y - 5.2}Z", g))
    out.append(F("M43.3 33H46.7L47.5 44.9H42.5Z", g))
    out.append(F("M35 41.5C39 39.2 51 39.2 55 41.5C51 40.8 39 40.8 35 41.5Z", g))
    return "".join(out)


K.add("L", "Lebanon", "Marhaba! A big cedar tree!", on_pole(90, 60, lebanon()))

# ================================================================ M
def mexico_emblem(cx, cy):
    green, brown, dbrown = "#0c7a3d", "#8b5a2b", "#5d3a1a"
    out = [
        # oak and laurel wreath
        lines(f"M{cx - 9} {cy + 1}Q{cx - 9} {cy + 9} {cx} {cy + 10}Q{cx + 9} {cy + 9} {cx + 9} {cy + 1}", green, 1.6),
    ]
    for k in range(5):
        t = k / 4
        for sgn in (-1, 1):
            a = math.radians(180 - 70 * t) if sgn < 0 else math.radians(70 * t)
            x = cx + 9 * math.cos(a) * (1 if sgn > 0 else 1)
            y = cy + 1 + 8.5 * math.sin(math.radians(20 + 70 * t))
            out.append(E(round(x, 2), round(y, 2), 1.6, 0.9, green, green, 0.1, rot=(-40 if sgn < 0 else 40)))
    out += [
        # stone and lake base, cactus pads
        E(cx, cy + 7.6, 4.2, 1.3, "#1f6fb2", "#1f6fb2", 0.1),
        E(cx, cy + 5, 2.3, 2.6, green, green, 0.1), E(cx - 2.8, cy + 2.6, 2, 2.4, green, green, 0.1, rot=-25),
        E(cx + 2.8, cy + 2.6, 2, 2.4, green, green, 0.1, rot=25),
        circ(cx - 3.4, cy + 0.6, 0.7, "#CE1126"), circ(cx + 3.3, cy + 0.4, 0.7, "#CE1126"),
        # eagle: body, raised wing, tail, head facing the hoist with the snake
        F(f"M{cx - 1.5} {cy + 1.5}C{cx - 4.5} {cy - 1} {cx - 4} {cy - 6} {cx - 1} {cy - 7}"
          f"C{cx + 2} {cy - 7} {cx + 4} {cy - 3} {cx + 3} {cy + 1}Z", brown),
        F(f"M{cx + 0.5} {cy - 4}C{cx + 3} {cy - 11} {cx + 8} {cy - 12} {cx + 9.5} {cy - 9}"
          f"C{cx + 7} {cy - 8} {cx + 6} {cy - 5} {cx + 3} {cy - 1}Z", brown),
        lines(f"M{cx + 3} {cy - 6}L{cx + 7.5} {cy - 9.5}M{cx + 3.5} {cy - 4}L{cx + 8} {cy - 7.6}", dbrown, 0.4),
        F(f"M{cx + 1.5} {cy + 0.5}L{cx + 6} {cy + 3.5}L{cx + 2} {cy + 2.5}Z", dbrown),
        F(f"M{cx - 2.2} {cy - 6.2}C{cx - 3.4} {cy - 9} {cx - 1.4} {cy - 10.4} {cx + 0.4} {cy - 9.2}"
          f"C{cx + 1} {cy - 8} {cx} {cy - 6.4} {cx - 1} {cy - 6}Z", brown),
        F(f"M{cx - 2.3} {cy - 9}L{cx - 4.4} {cy - 8.2}L{cx - 2.4} {cy - 7.7}Z", "#e0a800"),
        circ(cx - 1.3, cy - 8.8, 0.35, "#000"),
        lines(f"M{cx - 4} {cy - 8}C{cx - 6} {cy - 7} {cx - 4} {cy - 5} {cx - 6} {cy - 3.6}C{cx - 7.4} {cy - 2.6} {cx - 5.6} {cy - 1} {cx - 7.2} {cy}", "#3f8f2f", 0.7),
    ]
    return "".join(out)


K.add("M", "Mexico", "Hola! Yummy tacos!", on_pole(70, 40, vstripes(70, 40, ["#006847", "#fff", "#CE1126"]) + mexico_emblem(35, 20.5)))

# ================================================================ N
def offset_poly(pts, d):
    """Move every edge of a simple polygon inwards by d and re-intersect neighbours."""
    s = 1 if area2(pts) > 0 else -1
    n = len(pts)
    lines_ = []
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        nx, ny = -(y2 - y1) * s, (x2 - x1) * s
        ln = math.hypot(nx, ny); nx, ny = nx / ln, ny / ln
        lines_.append(((x1 + nx * d, y1 + ny * d), (x2 - x1, y2 - y1)))
    out = []
    for i in range(n):
        (p, r), (q, u) = lines_[i - 1], lines_[i]
        den = r[0] * u[1] - r[1] * u[0]
        t = ((q[0] - p[0]) * u[1] - (q[1] - p[1]) * u[0]) / den
        out.append((p[0] + t * r[0], p[1] + t * r[1]))
    return out


NEPAL = [(0, 0), (74, 46), (27, 46), (80, 100), (0, 100)]


def nepal():
    inner = offset_poly(NEPAL, 5)
    out = [poly(NEPAL, "#003893"), poly(inner, "#DC143C")]
    # moon: crescent bowl with a rayed half-disc rising out of it
    mx, my = 19, 33
    rays = []
    for k in range(9):
        a = math.radians(180 + k * 22.5)
        rays.append(poly([(mx + 5.5 * math.cos(a - 0.17), my - 1 + 5.5 * math.sin(a - 0.17)),
                          (mx + 8.6 * math.cos(a), my - 1 + 8.6 * math.sin(a)),
                          (mx + 5.5 * math.cos(a + 0.17), my - 1 + 5.5 * math.sin(a + 0.17))], "#fff"))
    out += rays
    out.append(F(f"M{mx - 6.2} {my - 1}A6.2 6.2 0 0 1 {mx + 6.2} {my - 1}Z", "#fff"))
    out.append(F(f"M{mx - 11} {my - 1.5}A11 9 0 0 0 {mx + 11} {my - 1.5}A11 6.2 0 0 1 {mx - 11} {my - 1.5}Z", "#fff"))
    # sun: 12-pointed
    out.append(star(22, 76, 12.5, "#fff", n=12, inner=0.68))
    return "".join(out)


K.add("N", "Nepal", "Namaste! The tallest mountain in the world!", on_pole(80, 100, nepal(), outline=NEPAL))
K.add("N", "Netherlands", "Hallo! Windmills and tulips!", on_pole(90, 60, hstripes(90, 60, ["#AE1C28", "#fff", "#21468B"])))

# ================================================================ O
def oman_emblem(cx, cy):
    w = "#fff"
    return "".join([
        # two crossed curved swords
        lines(f"M{cx - 7} {cy - 7}Q{cx - 1} {cy - 2} {cx + 6} {cy + 7}", w, 1.1),
        lines(f"M{cx + 7} {cy - 7}Q{cx + 1} {cy - 2} {cx - 6} {cy + 7}", w, 1.1),
        lines(f"M{cx - 6.6} {cy - 4.6}L{cx - 4.6} {cy - 6.6}M{cx + 6.6} {cy - 4.6}L{cx + 4.6} {cy - 6.6}", w, 1.1),
        # belt
        lines(f"M{cx - 6} {cy - 0.8}Q{cx} {cy + 1.4} {cx + 6} {cy - 0.8}", w, 1.2),
        # khanjar (curved dagger) in the middle
        F(f"M{cx - 1.3} {cy - 7.5}H{cx + 1.3}L{cx + 1.6} {cy - 4.5}H{cx - 1.6}Z", w),
        F(f"M{cx - 2.4} {cy - 4.5}H{cx + 2.4}V{cy - 3.2}H{cx - 2.4}Z", w),
        F(f"M{cx - 1.5} {cy - 3.2}H{cx + 1.5}C{cx + 1.8} {cy + 1} {cx + 2.5} {cy + 4} {cx + 5} {cy + 6}"
          f"C{cx + 1.5} {cy + 6} {cx - 1.3} {cy + 2} {cx - 1.5} {cy - 3.2}Z", w),
    ])


K.add("O", "Oman", "Marhaba! Camels in the desert!", on_pole(120, 60, "".join([
    rect(0, 0, 120, 20, "#fff"), rect(0, 20, 120, 20, "#DB161B"), rect(0, 40, 120, 20, "#008000"),
    rect(0, 0, 30, 60, "#DB161B"), T("translate(15 12) scale(1.3) translate(-15 -12)", oman_emblem(15, 12)),
])))

# ================================================================ P
def philippines():
    out = [rect(0, 0, 120, 30, "#0038A8"), rect(0, 30, 120, 30, "#CE1126"),
           poly([(0, 0), (51.96, 30), (0, 60)], "#fff")]
    sx, sy, gold = 17.3, 30, "#FCD116"
    for k in range(8):
        a = math.radians(k * 45)
        for da, ln_, wd in ((-0.2, 10.5, 0.05), (0, 12.6, 0.06), (0.2, 10.5, 0.05)):
            b = a + da
            out.append(poly([(sx + 6 * math.cos(b - wd), sy + 6 * math.sin(b - wd)),
                             (sx + ln_ * math.cos(b), sy + ln_ * math.sin(b)),
                             (sx + 6 * math.cos(b + wd), sy + 6 * math.sin(b + wd))], gold))
    out.append(circ(sx, sy, 5.6, gold))
    for x, y, rot in ((5.4, 6, -90 + 30), (5.4, 54, -90 - 30), (44.5, 30, 0)):
        out.append(star(x, y, 3, gold, rot=rot))
    return "".join(out)


K.add("P", "Philippines", "Kumusta! Thousands of islands!", on_pole(120, 60, philippines()))
K.add("P", "Peru", "Hola! Llamas live here!", on_pole(90, 60, vstripes(90, 60, ["#D91023", "#fff", "#D91023"])))

# ================================================================ Q
def qatar():
    out = [rect(0, 0, 28, 11, "#8A1538")]
    pts = [(0, 0)]
    for i in range(9):
        y0 = 11 * i / 9
        pts += [(8, y0), (10.6, y0 + 11 / 18)]
    pts += [(8, 11), (0, 11)]
    out.append(poly(pts, "#fff"))
    return "".join(out)


K.add("Q", "Qatar", "Marhaba! A hot sunny desert!", on_pole(28, 11, qatar(), ratio=2.2))

# ================================================================ R
def rwanda():
    out = [hstripes(90, 60, ["#00A1DE", "#FAD201", "#20603D"], [2, 1, 1])]
    sx, sy, gold = 72, 15.5, "#E5BE01"
    out.append(star(sx, sy, 10.5, gold, n=24, inner=0.62))
    out.append(circ(sx, sy, 5.9, "#00A1DE") + circ(sx, sy, 4.9, gold))
    return "".join(out)


K.add("R", "Rwanda", "Muraho! Gorillas in the green hills!", on_pole(90, 60, rwanda()))

# ================================================================ S
def south_africa():
    box = rect_pts(0, 0, 90, 60)
    out = [poly([(0, 0), (90, 0), (90, 30), (45, 30)], "#E03C31"), poly([(0, 60), (90, 60), (90, 30), (45, 30)], "#001489")]

    def Y(hw, col):
        return "".join(poly(clip_convex(band(p, q, -hw, hw, e), box), col)
                       for p, q, e in (((45, 30), (90, 30), 0), ((0, 0), (45, 30), 0), ((0, 60), (45, 30), 0)))
    out.append(Y(10, "#fff"))
    tri = [(0, 0), (45, 30), (0, 60)]
    out.append(poly(tri, "#FFB81C"))
    black = tri
    for nx, ny, c in halfplanes(tri, 10)[:2]:       # inset from the two slanted edges only
        black = clip_half(black, nx, ny, c)
    out.append(poly(black, "#000"))
    out.append(Y(6, "#007749"))
    return "".join(out)


K.add("S", "South Africa", "Sawubona! Penguins on the beach!", on_pole(90, 60, south_africa()))
K.add("S", "Sweden", "Hej! Snow and reindeer!", on_pole(16, 10, rect(0, 0, 16, 10, "#006AA7") + rect(5, 0, 2, 10, "#FECC02") + rect(0, 4, 16, 2, "#FECC02")))

# ================================================================ T
K.add("T", "Thailand", "Sawasdee! Elephants live here!", on_pole(9, 6, hstripes(9, 6, ["#A51931", "#fff", "#2D2A4A", "#fff", "#A51931"], [1, 1, 2, 1, 1])))


def tanzania():
    box = rect_pts(0, 0, 90, 60)
    return "".join([poly([(0, 0), (90, 0), (0, 60)], "#1EB53A"), poly([(90, 0), (90, 60), (0, 60)], "#00A3DD"),
                    poly(clip_convex(band((0, 60), (90, 0), -9.6, 9.6, 10), box), "#FCD116"),
                    poly(clip_convex(band((0, 60), (90, 0), -6.6, 6.6, 10), box), "#000")])


K.add("T", "Tanzania", "Jambo! Big Mount Kilimanjaro!", on_pole(90, 60, tanzania()))

# ================================================================ U
def usa():
    W, H = 190, 100
    out = []
    for i in range(13):
        out.append(rect(0, i * H / 13, W, H / 13 + 0.05, "#B22234" if i % 2 == 0 else "#fff"))
    out.append(rect(0, 0, 76, H * 7 / 13, "#3C3B6E"))
    for row in range(9):
        for col in range(6 if row % 2 == 0 else 5):
            x = 6.3 + col * 12.6 + (6.3 if row % 2 else 0)
            y = 5.4 + row * 5.4
            out.append(star(x, y, 3.08, "#fff"))
    return "".join(out)


K.add("U", "United States", "Hello! The Statue of Liberty!", on_pole(190, 100, usa()))
K.add("U", "United Kingdom", "Hello! Big Ben goes dong, dong!", on_pole(60, 30, union_jack()))

# ================================================================ V
K.add("V", "Vietnam", "Xin chao! Lots of rice fields!", on_pole(90, 60, rect(0, 0, 90, 60, "#DA251D") + star(45, 30, 18, "#FFFF00")))

# ================================================================ W  (the whole world)
def world():
    sea, land = "#4fc3f7", "#7cc576"
    return svg(
        C(50, 52, 40, sea),
        P("M24 30C30 22 42 22 44 30C46 36 40 38 40 44C40 50 34 52 32 60C30 66 24 62 22 56C18 48 16 38 24 30Z", land, O, 2.5),
        P("M54 20C62 16 74 20 78 28C82 34 74 36 70 34C64 32 60 36 56 32C52 28 50 24 54 20Z", land, O, 2.5),
        P("M58 50C64 46 74 48 76 56C78 64 72 74 64 76C58 78 56 70 58 64C60 58 54 54 58 50Z", land, O, 2.5),
        P("M30 80C36 78 44 80 46 84C40 88 34 88 30 84Z", "#fff", O, 2),
        C(50, 52, 40, "none"),
        HL(30, 30, 4, 9, 40), face(50, 46, 0.9), blush(50, 53, 12, 2.6),
        # a tiny flag on top of the world
        L("M50 12V2", O, 2.2), P("M50 2L62 5L50 8Z", "#e53935", O, 1.6))


K.add("W", "World", "Our big, round, beautiful world!", world())

# ================================================================ X  (no country starts with X)
K.add("X", "X marks the spot", "A treasure map! Let's go and explore!", svg(
    P("M12 22C24 18 32 26 44 22C56 18 66 26 80 20L90 22L88 80C76 86 66 78 54 82C42 86 32 78 20 82L10 80Z", "#f3d9a4"),
    P("M28 34C34 28 46 30 48 38C50 46 42 50 34 48C26 46 24 40 28 34Z", "#9ccc65", O, 2),
    P("M58 54C64 50 76 52 76 60C76 68 66 70 60 66C54 62 54 58 58 54Z", "#9ccc65", O, 2),
    L("M22 70C30 64 34 72 42 64C48 58 52 52 60 52", "#8d6e63", 2.5).replace('stroke-linecap="round"', 'stroke-linecap="round" stroke-dasharray="3 4"'),
    L("M62 34L72 44M72 34L62 44", "#e53935", 5),
    F(star_path(78, 70, 6, inner=0.45, n=4, rot=-90), "#3b2a1e"),
    HL(22, 30, 2.5, 5, 30)))

# ================================================================ Y
K.add("Y", "Yemen", "Marhaba! Very tall mud houses!", on_pole(90, 60, hstripes(90, 60, ["#CE1126", "#fff", "#000"])))

# ================================================================ Z
def zambia():
    out = [rect(0, 0, 90, 60, "#198A00"),
           rect(63, 22.5, 9, 37.5, "#DE2010"), rect(72, 22.5, 9, 37.5, "#000"), rect(81, 22.5, 9, 37.5, "#EF7D00")]
    cx, cy, o = 76.5, 12, "#EF7D00"
    out.append(F(f"M{cx - 1.5} {cy}C{cx - 5} {cy - 3} {cx - 9} {cy - 3.5} {cx - 12} {cy - 6.5}"
                 f"C{cx - 11} {cy - 2} {cx - 7} {cy + 1.5} {cx - 2} {cy + 3}Z", o))
    out.append(F(f"M{cx + 1.5} {cy}C{cx + 5} {cy - 3} {cx + 9} {cy - 3.5} {cx + 12} {cy - 6.5}"
                 f"C{cx + 11} {cy - 2} {cx + 7} {cy + 1.5} {cx + 2} {cy + 3}Z", o))
    out.append(F(f"M{cx - 2.2} {cy - 1.5}C{cx - 2.2} {cy - 5} {cx + 2.2} {cy - 5} {cx + 2.2} {cy - 1.5}"
                 f"L{cx + 1.5} {cy + 4}L{cx + 3} {cy + 7}H{cx - 3}L{cx - 1.5} {cy + 4}Z", o))
    out.append(F(f"M{cx - 1.6} {cy - 4.2}L{cx - 4} {cy - 3.2}L{cx - 1.4} {cy - 2.6}Z", o))
    return "".join(out)


K.add("Z", "Zambia", "Muli shani! The giant Victoria Falls!", on_pole(90, 60, zambia()))

K.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "countries.js"),
        "COUNTRY_ITEMS", "COUNTRIES",
        "Countries world: a flag for every letter (W = World, X = treasure map), hand-made SVG (viewBox 0 0 100 100). Generated by countries_make.py.")


# ---------------------------------------------------------------- home-screen picture: a bunch of flags
def inner(s):
    return s[s.index(">") + 1:s.rindex("</svg>")]


def flag_of(name):
    return next(it["svg"] for arr in K.items.values() for it in arr if it["name"] == name)


HOME = svg(
    T("translate(5 46) scale(0.5) rotate(-8 11 96)", inner(flag_of("Brazil"))),
    T("translate(46 47) scale(0.5) rotate(7 11 96)", inner(flag_of("India"))),
    T("translate(20 3) scale(0.56)", inner(flag_of("Japan"))),
)
js_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "countries.js")
src = open(js_path, encoding="utf-8").read()
assert "`" not in HOME and " id=" not in HOME
src = src.replace("// ==COUNTRIES END==", f"const COUNTRY_HOME_SVG = `{HOME}`;\n// ==COUNTRIES END==")
open(js_path, "w", encoding="utf-8", newline="\n").write(src)
print("added COUNTRY_HOME_SVG")
