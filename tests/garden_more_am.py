"""Extra Garden pictures A–M (3–4 per letter in total)."""
import math
import random
from svgkit import *

LEAF = "#5cb85c"
LEAFD = "#3f8f3f"
BROWN = "#7a4a2a"


def smooth_closed(pts):
    """Catmull-Rom closed curve through the points."""
    n = len(pts)
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n):
        p0 = pts[i - 1]; p1 = pts[i]; p2 = pts[(i + 1) % n]; p3 = pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d + "Z"


def wavy(cx, cy, rx, ry, n, amp, rot=0, phase=0.0):
    """Ellipse with a wavy (ruffled) edge."""
    pts = []
    m = n * 2
    r0 = math.radians(rot)
    for i in range(m):
        a = 2 * math.pi * i / m
        k = 1 + (amp if i % 2 == 0 else -amp)
        x = rx * k * math.cos(a + phase); y = ry * k * math.sin(a + phase)
        pts.append((cx + x * math.cos(r0) - y * math.sin(r0), cy + x * math.sin(r0) + y * math.cos(r0)))
    return smooth_closed(pts)


def leaf_path(bx, by, length, width, ang, teeth=0, tooth=0.0):
    """Leaf from base (bx,by) pointing at angle ang (degrees, 0 = right, -90 = up)."""
    pts = []
    N = max(10, teeth * 2) if teeth else 10
    up = []
    for i in range(1, N):
        t = i / N
        w = width / 2 * math.sin(math.pi * t) ** 0.8 * (1.15 - 0.3 * t)
        if teeth and i % 2 == 1:
            w += tooth
        up.append((t * length, -w))
    pts = [(0, 0)] + up + [(length, 0)] + [(x, -y) for (x, y) in reversed(up)]
    a = math.radians(ang)
    out = [(bx + x * math.cos(a) - y * math.sin(a), by + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    if teeth:
        return poly_path(out)
    return smooth_closed(out)


def leaf(bx, by, length, width, ang, fill=LEAF, vein=LEAFD, teeth=0, tooth=0.0, w=SW):
    a = math.radians(ang)
    ex = bx + length * 0.8 * math.cos(a); ey = by + length * 0.8 * math.sin(a)
    return P(leaf_path(bx, by, length, width, ang, teeth, tooth), fill, O, w) + L(f"M{bx:.1f} {by:.1f}L{ex:.1f} {ey:.1f}", vein, 1.8)


# ---------------------------------------------------------------- A
def apricot():
    return svg(
        L("M44 22L46 13", BROWN, 4),
        leaf(46, 15, 26, 12, -8),
        P("M44 22C28 16 10 28 12 50C14 72 30 80 46 78C64 78 78 66 76 46C74 26 60 16 44 22Z", "#ffa726"),
        F("M60 22C72 28 78 40 76 50C74 64 64 74 52 78C62 66 66 50 60 22Z", "#ff7043", ".55"),
        L("M44 24Q34 46 40 76", "#e0821a", 2.5),
        # cut half with stone
        C(72, 72, 19, "#ffa726"),
        C(72, 72, 15, "#ffcc5c", "#e0901a", 2),
        E(72, 72, 6.5, 8.5, "#a0522d", O, 2.5),
        L("M72 66L72 78", "#7a3d1e", 1.5),
        HL(24, 40, 4, 8, 20), face(38, 46))


def asparagus():
    def spear(x, rot, col, tip):
        body = (P(f"M{x-7} 90L{x-7} 32Q{x-8} 18 {x} 8Q{x+8} 18 {x+7} 32L{x+7} 90Z", col)
                + P(f"M{x-7} 34Q{x-8} 18 {x} 8Q{x+8} 18 {x+7} 34Q{x} 28 {x-7} 34Z", tip, O, 2.5)
                + L(f"M{x-7} 52L{x-2} 47M{x+7} 64L{x+2} 59M{x-7} 76L{x-2} 71", "#4f8a2a", 2.2))
        return T(f"rotate({rot} {x} 90)", body)
    return svg(
        spear(32, -16, "#8bc34a", "#7e57a8"),
        spear(68, 16, "#8bc34a", "#7e57a8"),
        spear(50, 0, "#9ccc65", "#8e63b8"),
        R(26, 64, 48, 13, "#e53935", rx=5),
        HL(46, 40, 2, 6, 0), face(50, 44, 0.55))


# ---------------------------------------------------------------- B
def beetroot():
    stems = L("M46 38Q40 30 32 26M50 36Q50 30 50 24M54 38Q60 30 68 26", "#b0225a", 4)
    return svg(
        leaf(32, 26, 24, 17, -130, "#43a047", "#b0225a"),
        leaf(68, 26, 24, 17, -50, "#43a047", "#b0225a"),
        leaf(50, 24, 19, 15, -90, "#5cb85c", "#b0225a"),
        stems,
        L("M50 84Q50 90 55 93", O, 2.5),
        P("M50 36C24 36 16 56 24 70C30 80 42 82 50 88C58 82 70 80 76 70C84 56 76 36 50 36Z", "#9c1f4f"),
        L("M30 68Q34 72 38 72M64 72Q68 72 70 68", "#6e1236", 2),
        HL(31, 50, 3.5, 7, 30), face(50, 58, 1, "#2a1010"))


# ---------------------------------------------------------------- C
def cucumber():
    seeds = ""
    for i in range(6):
        a = 2 * math.pi * i / 6 + 0.3
        x = 70 + 7 * math.cos(a); y = 70 + 7 * math.sin(a)
        seeds += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="1.4" ry="2.6" fill="#f4f8e0" stroke="#8fb85a" stroke-width="1" transform="rotate({math.degrees(a)+90:.0f} {x:.1f} {y:.1f})"/>'
    bumps = "".join(dot(x, y, 1.6, "#c5e8a0") for x, y in [(24, 30), (40, 26), (58, 26), (74, 30), (30, 50), (64, 50), (84, 40)])
    return svg(
        P("M88 36Q94 34 93 40Q91 44 87 42Z", "#b8d66a", O, 2),
        P("M10 42Q10 26 30 24L70 22Q88 22 88 38Q88 54 70 54L30 56Q10 58 10 42Z", "#3f9142"),
        L("M22 38Q50 34 80 34M26 47Q50 44 76 44", "#6fbf5a", 2.5),
        bumps,
        C(70, 70, 21, "#3f9142"),
        C(70, 70, 17, "#d9f0a8", "#9fcf6a", 2),
        C(70, 70, 10, "#eaf7c8", "#eaf7c8", 1),
        seeds,
        HL(22, 32, 2.5, 6, 70), HL(62, 63, 2.5, 4, 30), face(36, 40, 0.85))


# ---------------------------------------------------------------- D
def dates():
    def date(x, y, rot, col, s=1.0):
        d = (f"M{x-24*s:g} {y:g}C{x-24*s:g} {y-10*s:g} {x-12*s:g} {y-12*s:g} {x:g} {y-12*s:g}"
             f"C{x+12*s:g} {y-12*s:g} {x+24*s:g} {y-10*s:g} {x+25*s:g} {y:g}"
             f"C{x+24*s:g} {y+10*s:g} {x+12*s:g} {y+12*s:g} {x:g} {y+12*s:g}"
             f"C{x-12*s:g} {y+12*s:g} {x-24*s:g} {y+10*s:g} {x-24*s:g} {y:g}Z")
        return T(f"rotate({rot} {x} {y})",
                 P(d, col),
                 P(f"M{x+22*s:g} {y-4*s:g}Q{x+28*s:g} {y:g} {x+22*s:g} {y+4*s:g}Z", "#e0b060", O, 2),
                 L(f"M{x-16*s:g} {y-5*s:g}Q{x-11*s:g} {y:g} {x-15*s:g} {y+6*s:g}M{x+10*s:g} {y-7*s:g}Q{x+6*s:g} {y-1*s:g} {x+12*s:g} {y+5*s:g}", "#3e1a08", 2),
                 F(f"M{x-14*s:g} {y-7*s:g}Q{x:g} {y-11*s:g} {x+12*s:g} {y-7*s:g}Q{x:g} {y-8*s:g} {x-14*s:g} {y-7*s:g}Z", "#fff", ".45"))
    return svg(
        E(50, 82, 42, 10, "#8fd3f0"),
        E(50, 80, 30, 5, "#bfe8f8", "#bfe8f8", 1),
        date(30, 70, -8, "#6e3014", 0.9),
        date(70, 70, 8, "#6e3014", 0.9),
        date(50, 46, -4, "#8a4318", 1.35),
        face(50, 46, 0.9))


def durian():
    pts = []
    n = 26
    for i in range(2 * n):
        a = 2 * math.pi * i / (2 * n)
        r = 1.0 if i % 2 == 0 else 0.88
        pts.append((50 + 33 * r * math.cos(a), 56 + 35 * r * math.sin(a)))
    spikes = ""
    for (x, y) in [(32, 40), (50, 32), (68, 40), (26, 58), (74, 58), (34, 76), (50, 84), (66, 76), (40, 50), (60, 50)]:
        spikes += P(f"M{x-4} {y+3}L{x} {y-5}L{x+4} {y+3}Z", "#a8b83c", O, 1.8)
    return svg(
        P("M50 22Q50 12 46 6L52 4Q56 12 56 22Z", "#8a6a3a", O, 2.5),
        P(poly_path(pts), "#8fa02e"),
        spikes,
        HL(30, 46, 3, 7, 25), face(50, 62))


def daikon():
    return svg(
        leaf(44, 30, 24, 16, -122, "#4caf50", LEAFD),
        leaf(56, 30, 24, 16, -58, "#4caf50", LEAFD),
        leaf(50, 28, 21, 16, -90, LEAF, LEAFD),
        L("M50 88L51 93", O, 2.5),
        P("M34 30Q50 24 66 30Q66 62 56 84Q50 92 44 84Q34 62 34 30Z", "#fbf8ee"),
        F("M35 32Q50 26 65 32Q65 40 64 44Q50 40 36 44Q35 38 35 32Z", "#cfe8a0"),
        P("M34 30Q50 24 66 30Q66 62 56 84Q50 92 44 84Q34 62 34 30Z", "none"),
        L("M38 62L35 64M62 66L65 68M42 76L39 78", "#b9ad95", 2),
        HL(40, 50, 2.5, 7, 0), face(50, 52, 0.85))


# ---------------------------------------------------------------- E
def eggplant():
    return svg(
        P("M26 30C14 42 12 66 26 80C40 94 70 92 82 78C92 66 86 52 72 48C60 44 54 38 50 30C44 20 32 22 26 30Z", "#6a2c91"),
        P("M22 34L28 18L36 26L44 16L46 30L56 30L44 38L36 46L32 38Z", "#5fae3c", O, 2.5),
        P("M34 22L30 10L36 8L40 20Z", "#4f8f30", O, 2.5),
        F("M70 54C80 58 84 66 80 74C78 66 74 60 70 54Z", "#8e4cba"),
        HL(26, 56, 4, 9, 15), face(56, 66, 1, "#1e0a2a"))


def elderberries():
    berries = ""
    pos = [(22, 50), (36, 46), (50, 44), (64, 46), (78, 50),
           (28, 63), (72, 63), (34, 77), (66, 77), (50, 82)]
    stems = "".join(f"M50 28L{x} {y}" for x, y in pos[:5]) + "M36 46L28 63M64 46L72 63M42 60L34 77M58 60L66 77M50 62L50 82"
    for x, y in pos:
        berries += C(x, y, 7, "#3a1f52", O, 2.5) + dot(x - 2, y - 2, 1.6, "#9c84c4")
    return svg(
        leaf(48, 20, 30, 13, -165, LEAF, LEAFD),
        leaf(52, 20, 30, 13, -15, "#4caf50", LEAFD),
        L("M50 8L50 30", "#8e2d5a", 4),
        L(stems, "#8e2d5a", 2.5),
        berries,
        C(50, 62, 13, "#4a2a6a", O, 3),
        HL(45, 57, 2, 3.5, 30), face(50, 62, 0.6, "#fff"))


def endive():
    leafd = "M50 92C34 90 36 40 38 28Q42 14 50 14Q58 14 62 28C64 40 66 90 50 92Z"
    tipd = "M38 30Q42 14 50 14Q58 14 62 30Q50 24 38 30Z"
    def lf(rot, col):
        return T(f"rotate({rot} 50 92)", P(leafd, col), P(tipd, "#cddc39", O, 2.5), L("M50 30L50 86", "#e2d48a", 2))
    return svg(
        lf(-22, "#efe7a8"), lf(22, "#efe7a8"),
        lf(-10, "#f4eebc"), lf(10, "#f4eebc"),
        T("translate(0 2)", P(leafd, "#fbf7dc"), P(tipd, "#d4e157", O, 2.5)),
        HL(43, 48, 2.5, 8, 0), face(50, 60, 0.8))


# ---------------------------------------------------------------- F
def fennel():
    fronds = ""
    for x, y in [(26, 16), (50, 10), (74, 16)]:
        fronds += L(f"M{x} {y+8}L{x-9} {y-2}M{x} {y+8}L{x} {y-4}M{x} {y+8}L{x+9} {y-2}M{x} {y+16}L{x-11} {y+8}M{x} {y+16}L{x+11} {y+8}", "#4caf50", 3.5)
    return svg(
        TL("M42 52L28 22", "#a5d46a", 6), TL("M50 50L50 18", "#b5dc7a", 6), TL("M58 52L72 22", "#a5d46a", 6),
        fronds,
        P("M50 44C30 44 16 56 18 72C20 86 36 92 50 92C64 92 80 86 82 72C84 56 70 44 50 44Z", "#eef6d4"),
        L("M36 50Q26 68 36 88M64 50Q74 68 64 88", "#c4dc94", 2.2),
        F("M40 46Q50 42 60 46Q50 50 40 46Z", "#c8e494"),
        HL(26, 64, 3, 7, 20), face(50, 68))


def french_beans():
    def bean(d, col):
        return TL(d, col, 11)
    return svg(T("translate(50 50) scale(0.9) translate(-50 -50)",
        bean("M14 70Q40 74 86 30", "#5aaa36"),
        bean("M16 52Q36 48 76 14", "#4f9e30"),
        L("M86 30Q90 24 92 26M76 14Q80 8 84 8", LEAFD, 2.5),
        bean("M12 88Q50 92 88 54", "#6cbf44"),
        L("M88 54Q92 48 94 50", LEAFD, 2.5),
        L("M24 86Q50 88 76 66", "#a6dc80", 2.5),
        HL(20, 50, 2, 4, 60), face(50, 82, 0.65)))


def fruit_salad():
    return svg(
        C(67, 36, 13, "#7a5a2e"), C(67, 36, 10.5, "#7cc242", "#5f9a2c", 1.5),
        dot(67, 36, 3.2, "#f2f8d8"),
        "".join(dot(67 + 6.5 * math.cos(a), 36 + 6.5 * math.sin(a), 1.1, "#222") for a in [i * math.pi / 4 for i in range(8)]),
        P("M38 42C28 36 26 24 36 22Q42 20 46 24Q50 20 56 22C64 26 58 38 46 46Z", "#e8273b"),
        P("M38 24L42 16L46 22L52 16L52 24Z", "#4caf50", O, 2),
        dot(44, 30, 1.2, "#ffe36b"), dot(50, 34, 1.2, "#ffe36b"), dot(40, 34, 1.2, "#ffe36b"),
        C(26, 44, 11, "#fff3b0"), dot(26, 44, 3, "#e8d48a"),
        C(56, 48, 8, "#8e44ad"), HL(54, 45, 1.5, 3, 30),
        P("M72 50A10 10 0 0 1 92 50Z", "#ff9a1f"), F("M76 50A6 6 0 0 1 88 50Z", "#ffd27a"), L("M82 50L82 44M82 50L78 46M82 50L86 46", "#ff9a1f", 1.5),
        P("M12 50L88 50Q86 88 50 90Q14 88 12 50Z", "#ff8fb1"),
        L("M12 50L88 50", O, 3),
        L("M18 60Q50 66 82 60", "#ffc2d6", 3),
        HL(22, 66, 3, 7, -20), face(50, 72))


# ---------------------------------------------------------------- G
def grapefruit():
    segs = ""
    for i in range(10):
        a0 = i * 36
        segs += F(annulus_sector(62, 62, 3, 21, a0 + 3, a0 + 33), "#ff5c7a")
    return svg(
        C(32, 36, 25, "#ffb84d"),
        F("M14 48A25 25 0 0 0 46 58Q30 56 20 44Z", "#ff8a65", ".6"),
        dot(50, 26, 2.5, "#8a6a2a"),
        HL(20, 26, 3, 6, 30), face(28, 34, 0.85),
        C(62, 62, 29, "#ffb84d"),
        C(62, 62, 24, "#fff1e6", "#f0c090", 2),
        segs,
        dot(62, 62, 3, "#fff1e6"),
        HL(46, 48, 2.5, 5, 40))


def guava():
    seeds = "".join(dot(68 + x, 70 + y, 1.5, "#f6e7b8") for x, y in [(-6, -4), (0, -7), (6, -4), (-7, 3), (7, 3), (0, 6), (-3, 0), (3, 0)])
    return svg(
        L("M38 18L40 12", BROWN, 4),
        leaf(40, 13, 26, 12, -4),
        P(smooth_closed([(38, 18), (54, 22), (64, 38), (64, 58), (52, 72), (32, 74), (16, 62), (12, 42), (20, 24)]), "#a5d05a"),
        dot(22, 50, 1.4, "#7fa83a"), dot(50, 30, 1.4, "#7fa83a"), dot(30, 64, 1.4, "#7fa83a"),
        C(68, 70, 21, "#a5d05a"),
        C(68, 70, 17, "#ff7f93", "#e85a72", 2),
        C(68, 70, 10, "#ffa7b6", "#ffa7b6", 1),
        seeds,
        HL(22, 34, 3.5, 7, 30), face(38, 44))


# ---------------------------------------------------------------- H
def hazelnut():
    husk = []
    for i in range(14):
        a = math.pi + math.pi * i / 13
        r = 36 if i % 2 == 0 else 28
        husk.append((50 + r * math.cos(a), 52 + r * math.sin(a) * 1.05))
    husk_d = poly_path([(18, 66)] + husk + [(82, 66)])
    return svg(
        P(husk_d, "#8bc34a"),
        P("M50 18C46 26 26 36 24 58C22 78 36 90 50 90C64 90 78 78 76 58C74 36 54 26 50 18Z", "#b06a30"),
        P("M28 74Q50 66 72 74Q66 90 50 90Q34 90 28 74Z", "#e3c08e", O, 2.5),
        L("M40 36Q34 50 36 66M60 36Q66 50 64 66", "#8a4e20", 2),
        HL(34, 46, 3, 7, 20), face(50, 54))


def huckleberries():
    def berry(x, y, r, col="#6b2152"):
        return C(x, y, r, col) + dot(x, y + r * 0.6, r * 0.18, "#3a0f2a") + HL(x - r * 0.4, y - r * 0.4, r * 0.18, r * 0.35, 30)
    return svg(
        L("M10 24Q50 12 90 22", BROWN, 4),
        leaf(30, 19, 22, 13, -160, LEAF, LEAFD),
        leaf(66, 17, 22, 13, -20, "#4caf50", LEAFD),
        L("M26 22L24 40M50 17L50 34M76 21L78 40M40 19L38 58M62 18L64 58", "#5d7a2a", 2),
        berry(22, 46, 12, "#7b2a5c"),
        berry(78, 46, 12, "#7b2a5c"),
        berry(32, 72, 14),
        berry(68, 72, 14),
        C(50, 58, 17, "#8a2e66"),
        HL(42, 52, 2.5, 5, 30), face(50, 62, 0.8))


def herbs():
    lv = ""
    for (bx, by, ang, col) in [(50, 50, -150, "#4caf50"), (50, 50, -30, "#4caf50"), (46, 46, -118, "#66bb6a"),
                               (54, 46, -62, "#66bb6a"), (50, 44, -90, "#81c784")]:
        lv += leaf(bx, by, 30, 20, ang, col, LEAFD)
    return svg(
        L("M50 52L50 30M50 52L34 34M50 52L66 34", LEAFD, 3),
        lv,
        P("M24 60L76 60L70 90L30 90Z", "#d9773c"),
        R(18, 50, 64, 14, "#e88b4f", rx=4),
        HL(28, 56, 2, 5, 70), face(50, 74))


# ---------------------------------------------------------------- I
def indian_corn():
    random.seed(11)
    cols = ["#c62828", "#6a1b9a", "#fbc02d", "#ef6c00", "#3949ab", "#fff3c4", "#8d2a2a", "#ffb300"]
    kern = ""
    for row in range(11):
        y = 37 + row * 5.2
        w = 16 * math.sqrt(max(0.0, 1 - ((y - 62) / 30) ** 2))
        n = int((2 * w - 4) / 5.4) + 1
        for i in range(n):
            x = 50 + (i - (n - 1) / 2) * 5.4 + (1.3 if row % 2 else -1.3) * (n > 1)
            if (x - 50) ** 2 / 11 ** 2 + (y - 62) ** 2 / 8 ** 2 < 1 or abs(x - 50) > w - 3.2:
                continue
            kern += C(round(x, 1), round(y, 1), 2.7, cols[(row * 3 + i * 5 + random.randint(0, 2)) % len(cols)], "#5a3a1e", 0.8)
    return svg(
        P("M48 36Q28 26 22 6Q38 12 50 30Z", "#e8d4a2"),
        P("M52 36Q72 26 78 6Q62 12 50 30Z", "#dcc48a"),
        P("M50 36Q40 20 46 6Q56 18 54 36Z", "#f0e0b4"),
        L("M30 14Q38 22 46 30M70 14Q62 22 54 30", "#c2a66a", 1.6),
        P("M50 32C36 32 34 48 34 62C34 80 42 92 50 92C58 92 66 80 66 62C66 48 64 32 50 32Z", "#f3d27a"),
        kern,
        P("M50 32C36 32 34 48 34 62C34 80 42 92 50 92C58 92 66 80 66 62C66 48 64 32 50 32Z", "none"),
        HL(40, 44, 2, 5, 10), face(50, 61, 0.8))


def ice_cream_bean():
    fluff = ""
    for x, y, r in [(32, 60, 8), (42, 54, 9), (54, 48, 9), (66, 42, 9), (78, 36, 7), (38, 66, 6),
                    (48, 61, 8), (60, 55, 8), (72, 49, 8), (84, 40, 5)]:
        fluff += C(x, y, r, "#ffffff", "#c9c2b4", 1.5)
    return svg(
        P("M6 72Q6 54 22 50Q50 40 74 22Q90 12 93 26Q96 42 82 52Q54 70 26 82Q6 90 6 72Z", "#5f9e34"),
        P("M28 58Q52 42 84 26Q90 38 80 48Q56 64 32 72Q22 66 28 58Z", "#f6f1e4", O, 2.5),
        fluff,
        dot(46, 56, 2.2, "#2b1a12"), dot(66, 45, 2.2, "#2b1a12"), dot(56, 58, 2.2, "#2b1a12"),
        L("M14 82Q50 74 90 46", "#3f7f22", 2.5),
        HL(12, 62, 2, 5, 40), face(17, 70, 0.7))


def italian_plum():
    return svg(
        L("M40 18Q40 13 43 10", BROWN, 4),
        leaf(42, 12, 26, 12, -2),
        E(40, 48, 26, 32, "#4b3f9a", rot=-12),
        L("M36 18Q26 44 34 78", "#352a78", 2.5),
        F("M54 26Q64 36 62 52Q58 40 52 30Z", "#8f86d0", ".7"),
        E(72, 72, 16, 20, "#4b3f9a", rot=10),
        E(72, 72, 12, 16, "#f4c542", "#d8a62a", 2, rot=10),
        E(72, 72, 5, 8, "#a0522d", O, 2.5, rot=10),
        HL(26, 38, 3.5, 8, 20), face(38, 50, 1, "#14102e"))


# ---------------------------------------------------------------- J
def jalapeno():
    return svg(
        L("M24 30Q16 18 22 8", "#4f8f30", 6),
        P("M24 30C40 22 62 26 76 42C90 58 90 80 82 90Q74 84 70 74C62 60 46 56 30 54C16 52 12 36 24 30Z", "#3e9a35"),
        P("M14 38Q16 26 28 26Q38 28 36 34Q30 46 20 48Q14 46 14 38Z", "#5fb33a", O, 2.5),
        F("M62 34C74 42 82 54 84 70Q78 56 66 44Z", "#7cc858", ".8"),
        HL(52, 34, 2.5, 6, 70), face(52, 43, 0.85))


def jujube():
    return svg(
        L("M50 20Q50 14 54 11", BROWN, 3.5),
        leaf(53, 12, 26, 13, -8, LEAF, LEAFD),
        leaf(49, 13, 22, 11, -172, "#4caf50", LEAFD),
        E(30, 48, 17, 22, "#c8cc54", rot=-20),
        F("M26 28C38 28 46 40 44 56Q36 44 26 28Z", "#a8432a", ".75"),
        E(30, 48, 17, 22, "none", rot=-20),
        L("M30 26L44 18", BROWN, 2.5),
        E(60, 60, 23, 28, "#a8322a"),
        F("M40 66C42 80 52 88 62 88Q48 80 44 64Z", "#d9c95a", ".85"),
        E(60, 60, 23, 28, "none"),
        L("M60 32L54 20", BROWN, 2.5),
        HL(48, 48, 3, 7, 20), face(62, 60))


def jicama():
    return svg(
        P("M48 22Q46 12 42 8L50 6Q52 14 54 22Z", "#7a6a3a", O, 2.5),
        L("M50 88Q50 92 47 94", O, 2.5),
        P("M50 20C28 20 12 32 12 52C12 70 32 82 50 90C68 82 88 70 88 52C88 32 72 20 50 20Z", "#c9975a"),
        P("M52 52L88 52C88 68 72 80 58 87Z", "#fdf8ea", O, 2.5),
        F("M52 52L58 87", "#e7dcc0"),
        L("M24 40Q30 36 34 38M60 30Q66 28 70 32M22 64Q26 68 30 68", "#9c6d36", 2),
        HL(26, 34, 3, 7, 40), face(36, 50))


# ---------------------------------------------------------------- K
def kale():
    return svg(
        P(wavy(32, 44, 16, 30, 14, 0.08, rot=-28), "#2e6b3a"),
        P(wavy(68, 44, 16, 30, 14, 0.08, rot=28), "#2e6b3a"),
        TL("M50 66L50 90", "#9ccc65", 6),
        P(wavy(50, 44, 26, 36, 18, 0.07), "#3f8f4a"),
        L("M50 80L50 12M50 62L30 46M50 62L70 46M50 40L34 26M50 40L66 26", "#8fd18a", 2.2),
        HL(34, 30, 3, 7, 20), face(50, 50, 0.95))


def kumquat():
    def kq(x, y, s=1.0):
        return (E(x, y, 14 * s, 18 * s, "#ff9800") + dot(x, y - 18 * s + 3, 2, "#6b8e23")
                + dot(x + 6 * s, y + 4 * s, 1.1, "#e07b00") + dot(x - 5 * s, y + 9 * s, 1.1, "#e07b00"))
    return svg(
        L("M14 18Q50 6 86 18", BROWN, 4),
        leaf(26, 16, 18, 11, 160, "#2e7d32", LEAFD),
        leaf(74, 16, 18, 11, 20, "#2e7d32", LEAFD),
        L("M28 16L28 34M72 16L72 34M50 10L50 50", BROWN, 2.5),
        kq(28, 50), kq(72, 50), HL(22, 44, 2, 5, 25), HL(66, 44, 2, 5, 25),
        kq(50, 68, 1.25),
        HL(40, 58, 2.5, 6, 25), face(50, 70, 0.85))


def kohlrabi():
    stems = [((34, 50), (21, 30)), ((44, 40), (39, 21)), ((56, 40), (61, 21)), ((66, 50), (79, 30))]
    lv = ""
    for (sx, sy), (ex, ey) in stems:
        ang = math.degrees(math.atan2(ey - sy, ex - sx))
        lv += leaf(ex, ey, 17, 14, ang, "#43a047", "#2e7d32")
    return svg(
        "".join(TL(f"M{sx} {sy}L{ex} {ey}", "#a5d46a", 4) for (sx, sy), (ex, ey) in stems),
        lv,
        C(50, 64, 28, "#bfe07a"),
        E(28, 66, 3, 2, "#9ccc65", O, 2), E(72, 66, 3, 2, "#9ccc65", O, 2), E(36, 84, 3, 2, "#9ccc65", O, 2), E(64, 84, 3, 2, "#9ccc65", O, 2),
        HL(36, 50, 3.5, 7, 30), face(50, 66))


# ---------------------------------------------------------------- L
def lettuce():
    return svg(
        P(wavy(31, 50, 16, 30, 10, 0.07, rot=-30), "#5fb83c"),
        P(wavy(69, 50, 16, 30, 10, 0.07, rot=30), "#5fb83c"),
        P(wavy(50, 40, 22, 30, 11, 0.06), "#7ccd4a"),
        L("M28 74Q30 54 22 30M72 74Q70 54 78 30", "#c8ec9a", 2.2),
        L("M50 12L50 40", "#c8ec9a", 2.5),
        P("M40 84Q50 94 60 84L56 76L44 76Z", "#e6f5c4", O, 2.5),
        P(wavy(50, 64, 26, 22, 11, 0.06), "#a6dc66"),
        HL(34, 56, 3, 6, 30), face(50, 64))


def lychee():
    random.seed(5)
    pts = []
    n = 18
    for i in range(2 * n):
        a = 2 * math.pi * i / (2 * n)
        r = 31 if i % 2 == 0 else 28.5
        pts.append((40 + r * math.cos(a), 46 + r * math.sin(a)))
    tex = ""
    for x, y in [(26, 28), (40, 22), (54, 26), (20, 44), (60, 40), (24, 60), (36, 70), (52, 64), (32, 34), (48, 34)]:
        tex += L(f"M{x-3} {y+1}L{x} {y-2}L{x+3} {y+1}", "#a3203a", 1.8)
    return svg(
        L("M40 16Q40 12 44 10", BROWN, 3.5),
        leaf(43, 11, 22, 11, -4),
        P(smooth_closed(pts), "#e0405a"),
        tex,
        HL(22, 34, 3, 6, 30), face(38, 48, 0.9),
        P("M54 76Q54 92 72 92Q90 92 90 76Z", "#e0405a"),
        E(72, 68, 16, 18, "#f7f3ea", "#3b2a1e"),
        P("M54 76Q56 86 72 86Q88 86 90 76Q86 84 72 84Q58 84 54 76Z", "#e0405a", O, 2),
        HL(66, 62, 3, 6, 30))


# ---------------------------------------------------------------- M
def melon():
    random.seed(4)
    cx, cy, rr = 40, 42, 32
    grid = {}
    for i in range(-5, 6):
        for j in range(-5, 6):
            x = cx + i * 9 + (4.5 if j % 2 else 0) + random.uniform(-1.5, 1.5)
            y = cy + j * 8 + random.uniform(-1.5, 1.5)
            grid[(i, j)] = (x, y)
    segs = ""
    for (i, j), (x, y) in grid.items():
        for di, dj in [(1, 0), (0, 1), (-1 if j % 2 == 0 else 1, 1)]:
            k = (i + di, j + dj)
            if k in grid:
                x2, y2 = grid[k]
                if math.hypot(x - cx, y - cy) < rr - 4 and math.hypot(x2 - cx, y2 - cy) < rr - 4:
                    segs += f"M{x:.1f} {y:.1f}L{x2:.1f} {y2:.1f}"
    seeds = "".join(f'<ellipse cx="{x}" cy="{y}" rx="1.4" ry="2.6" fill="#fff3c4"/>'
                    for x, y in [(54, 70), (61, 72), (68, 73), (75, 72), (82, 70)])
    return svg(
        C(cx, cy, rr, "#e2c27a"),
        L(segs, "#f7ead0", 2.2),
        L("M40 11L42 6", BROWN, 3.5),
        HL(24, 28, 4, 7, 40), face(cx, cy + 2),
        P("M42 64L92 64Q90 92 67 92Q44 92 42 64Z", "#b5c76a"),
        F("M47 64L87 64Q85 86 67 86Q49 86 47 64Z", "#ffa040"),
        seeds,
        L("M42 64L92 64Q90 92 67 92Q44 92 42 64Z"))


def mint():
    lv = ""
    for (y, ln, w) in [(70, 28, 20), (48, 24, 17)]:
        lv += leaf(50, y, ln, w, -160, "#3ec26a", "#2a8a4a", teeth=7, tooth=1.8)
        lv += leaf(50, y, ln, w, -20, "#3ec26a", "#2a8a4a", teeth=7, tooth=1.8)
    return svg(
        TL("M50 90L50 26", "#6aa84f", 3),
        lv,
        leaf(50, 32, 18, 12, -125, "#52d07c", "#2a8a4a", teeth=5, tooth=1.4),
        leaf(50, 32, 18, 12, -55, "#52d07c", "#2a8a4a", teeth=5, tooth=1.4),
        P(leaf_path(50, 34, 28, 22, -90, 7, 1.6), "#5ad685"),
        HL(44, 18, 2, 4, 20), face(50, 20, 0.6))


def add_more(K):
    K.add("A", "Apricot", "Soft and sweet!", apricot())
    K.add("A", "Asparagus", "Long green spears!", asparagus())
    K.add("B", "Beetroot", "Deep purple and sweet!", beetroot())
    K.add("C", "Cucumber", "Cool and crunchy!", cucumber())
    K.add("D", "Dates", "Sticky and sweet!", dates())
    K.add("D", "Durian", "Spiky and smelly!", durian())
    K.add("D", "Daikon", "A long white radish!", daikon())
    K.add("E", "Eggplant", "Shiny and purple!", eggplant())
    K.add("E", "Elderberries", "Tiny dark berries!", elderberries())
    K.add("E", "Endive", "Crisp little leaves!", endive())
    K.add("F", "Fennel", "Crunchy with feathery leaves!", fennel())
    K.add("F", "French beans", "Long and green!", french_beans())
    K.add("F", "Fruit salad", "A bowl of yummy fruit!", fruit_salad())
    K.add("G", "Grapefruit", "Pink and juicy inside!", grapefruit())
    K.add("G", "Guava", "Green outside, pink inside!", guava())
    K.add("H", "Hazelnut", "A crunchy little nut!", hazelnut())
    K.add("H", "Huckleberries", "Small and juicy!", huckleberries())
    K.add("H", "Herbs", "Smell the green leaves!", herbs())
    K.add("I", "Indian corn", "So many colours!", indian_corn())
    K.add("I", "Ice-cream bean", "Soft and fluffy inside!", ice_cream_bean())
    K.add("I", "Italian plum", "Purple and juicy!", italian_plum())
    K.add("J", "Jalapeno", "Green and hot!", jalapeno())
    K.add("J", "Jujube", "Small and crunchy!", jujube())
    K.add("J", "Jicama", "Crunchy and white inside!", jicama())
    K.add("K", "Kale", "Curly green leaves!", kale())
    K.add("K", "Kumquat", "Tiny little oranges!", kumquat())
    K.add("K", "Kohlrabi", "A round green veggie!", kohlrabi())
    K.add("L", "Lettuce", "Crunchy green leaves!", lettuce())
    K.add("L", "Lychee", "Bumpy outside, sweet inside!", lychee())
    K.add("M", "Melon", "Orange and sweet!", melon())
    K.add("M", "Mint", "Fresh and yummy smell!", mint())
