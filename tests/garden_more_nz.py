"""Extra Garden pictures N–Z (3–4 per letter in total)."""
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


def smooth_open(pts):
    """Catmull-Rom open curve through the points."""
    n = len(pts)
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for i in range(n - 1):
        p0 = pts[max(i - 1, 0)]; p1 = pts[i]; p2 = pts[i + 1]; p3 = pts[min(i + 2, n - 1)]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
    return d


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


def bean(x, y, rx, ry, rot, fill, w=2, eye=None):
    s = E(x, y, rx, ry, fill, O, w, rot=rot)
    if eye:
        s += dot(x, y - ry * 0.1, max(0.9, ry * 0.3), eye)
    return s


# ---------------------------------------------------------------- N
def napa_cabbage():
    def lf(rot, body, top):
        return T(f"rotate({rot} 50 92)",
                 P(wavy(50, 26, 19, 17, 9, 0.09), top),
                 P("M50 92C36 90 30 66 32 38Q50 30 68 38C70 66 64 90 50 92Z", body),
                 P("M50 92C44 84 42 62 44 38Q50 34 56 38C58 62 56 84 50 92Z", "#fbfdf0", O, 2.2),
                 L("M50 14L50 34M50 28L40 18M50 28L60 18", "#8fc24a", 1.8))
    return svg(
        lf(-12, "#e4f2b4", "#9fd05a"), lf(12, "#e4f2b4", "#9fd05a"),
        lf(0, "#eef8c8", "#b5dc6a"),
        HL(41, 50, 1.5, 6, 0), face(50, 62, 0.62))


def navy_beans():
    random.seed(3)
    beans = ""
    rows = [(52, 18, 82, 8), (45, 24, 76, 8.5), (38, 31, 69, 8.5), (31, 40, 60, 9)]
    for y, x0, x1, step in rows:
        n = int((x1 - x0) / step) + 1
        for i in range(n):
            x = x0 + i * (x1 - x0) / max(1, n - 1)
            beans += bean(round(x + random.uniform(-1, 1), 1), round(y + random.uniform(-1, 1), 1), 4.6, 3.3,
                          random.randint(-40, 40), "#f8f3e4")
    spill = bean(14, 90, 4.6, 3.3, 20, "#f8f3e4") + bean(86, 90, 4.6, 3.3, -25, "#f8f3e4") + bean(78, 93, 4.6, 3.3, 10, "#f8f3e4")
    return svg(
        P("M14 56Q18 34 50 25Q82 34 86 56Z", "#ece2c6", O, 2),
        beans,
        spill,
        P("M10 56L90 56Q88 88 50 90Q12 88 10 56Z", "#c98a4b"),
        L("M10 56L90 56", O, 3),
        L("M18 66Q50 72 82 66", "#e0aa70", 2.5),
        HL(20, 68, 2.5, 6, -20), face(50, 74))


def nutmeg():
    net = L("M22 36Q30 40 26 50Q24 58 30 66M34 22Q42 28 38 38M50 22Q56 28 52 36M58 40Q62 48 56 56M44 66Q50 70 48 76", "#c08a5a", 2.2)
    mace = ""
    marble = L("M58 66Q64 70 60 76Q58 80 64 84M66 60Q70 66 76 64Q82 64 80 72M70 76Q74 80 82 78M62 72Q68 74 70 70", "#9a5a30", 2.2)
    return svg(
        E(40, 46, 25, 31, "#8a5530", rot=-15),
        net, mace,
        HL(28, 38, 3, 7, 15), face(40, 50, 0.95),
        C(70, 72, 21, "#7a4626"),
        C(70, 72, 17, "#ecd2a4", "#a0683a", 2),
        marble,
        HL(60, 63, 2, 4, 30))


# ---------------------------------------------------------------- O
def okra():
    pod = T("rotate(-24 40 54)",
            L("M40 18L40 6", "#5a8f30", 6),
            P("M40 20C52 20 55 30 54 44C53 62 47 80 40 92C33 80 27 62 26 44C25 30 28 20 40 20Z", "#6bb54a"),
            L("M33 26Q31 56 39 86M47 26Q49 56 41 86", "#4e9a34", 2.2),
            P("M28 24Q40 14 52 24Q46 30 40 28Q34 30 28 24Z", "#4e8f2e", O, 2.5),
            HL(32, 40, 2, 7, 0), face(40, 50, 0.8))
    pts = []
    for i in range(10):
        a = math.radians(-90 + 36 * i)
        r = 19 if i % 2 == 0 else 15.5
        pts.append((74 + r * math.cos(a), 72 + r * math.sin(a)))
    seeds = ""
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        seeds += C(round(74 + 8.5 * math.cos(a), 1), round(72 + 8.5 * math.sin(a), 1), 3, "#f4fae6", "#8fc46a", 1.5)
    return svg(
        pod,
        P(smooth_closed(pts), "#6bb54a"),
        P(star_path(74, 72, 14, 0.75, 5), "#d9f0b4", "#8fc46a", 2),
        L("".join(f"M74 72L{74 + 13 * math.cos(math.radians(-54 + 72 * i)):.1f} {72 + 13 * math.sin(math.radians(-54 + 72 * i)):.1f}" for i in range(5)), "#a9d488", 1.5),
        seeds,
        HL(64, 62, 2, 4, 30))


def olives():
    def olive(x, y, rx, ry, col, hl="#fff"):
        return E(x, y, rx, ry, col, rot=-8) + HL(x - rx * 0.4, y - ry * 0.35, rx * 0.2, ry * 0.3, 20)
    return svg(
        L("M10 26Q50 16 90 24", BROWN, 4),
        leaf(22, 23, 22, 8, 165, "#8fae6a", "#5f7f40"),
        leaf(40, 20, 18, 8, -25, "#9cbc76", "#5f7f40"),
        leaf(62, 20, 18, 8, -155, "#8fae6a", "#5f7f40"),
        leaf(78, 22, 22, 8, 15, "#9cbc76", "#5f7f40"),
        L("M28 23L28 36M72 22L72 38M50 20L50 34", "#6a5a2a", 2.5),
        olive(26, 50, 14, 17, "#2e2838"),
        olive(74, 52, 14, 17, "#2e2838"),
        olive(50, 64, 20, 25, "#9cbf34"),
        dot(50, 39, 2, "#6a7a20"),
        face(50, 66, 0.9))


# ---------------------------------------------------------------- P
def peas():
    peas_ = ""
    for x, y, r in [(22, 47, 8), (36, 52, 9), (64, 52, 9), (78, 47, 8)]:
        peas_ += C(x, y, r, "#7cc444") + HL(x - r * 0.35, y - r * 0.35, r * 0.18, r * 0.3, 30)
    return svg(T("translate(50 52) scale(0.9) translate(-50 -52)",
        P("M10 46C18 26 38 18 56 20C72 22 86 28 92 40C78 38 64 36 50 38C34 40 20 42 10 46Z", "#5fb53c"),
        L("M20 40Q50 28 84 34", "#8fd06a", 2),
        P("M10 46C14 70 34 82 52 82C72 82 88 66 92 40C78 50 64 56 50 56C32 56 20 52 10 46Z", "#a8dc78"),
        peas_,
        C(50, 54, 11, "#86cf4c"), HL(45, 49, 2, 3.5, 30), face(50, 55, 0.6),
        P("M10 46C22 62 36 68 50 68C66 68 80 60 92 40C88 70 70 86 50 86C30 86 14 72 10 46Z", "#4caf50"),
        L("M22 72Q50 84 80 70", "#7fcf5a", 2.2),
        L("M10 46Q4 44 6 36", "#4f8f30", 4),
        L("M92 40Q98 34 94 28Q90 24 92 18", "#6aaa3a", 2.5)))


# ---------------------------------------------------------------- Q
def quinoa():
    random.seed(7)
    heads = ""
    for (x, y, col) in [(16, 20, "#e0703a"), (24, 13, "#e0703a"), (14, 32, "#d4582c"), (26, 26, "#ef8a4a"), (20, 42, "#d4582c"),
                        (84, 22, "#f2b33a"), (76, 15, "#f2b33a"), (86, 34, "#e6a020"), (74, 28, "#f7c55a"), (80, 44, "#e6a020")]:
        heads += C(x, y, 6, col, O, 2)
    grains = ""
    cols = ["#fff6dc", "#fff6dc", "#f3d9a4", "#d9573a", "#3b2a2a"]
    for _ in range(60):
        x = random.uniform(20, 80); y = random.uniform(36, 56)
        if y < 56 - 22 * (1 - ((x - 50) / 32) ** 2):
            continue
        grains += dot(round(x, 1), round(y, 1), 1.5, random.choice(cols))
    return svg(
        L("M22 58Q20 40 18 14M78 58Q80 40 82 16", "#6a9a3a", 3),
        heads,
        P("M14 58Q20 36 50 32Q80 36 86 58Z", "#f2e2bc", O, 2.5),
        grains,
        P("M10 58L90 58Q88 88 50 90Q12 88 10 58Z", "#26a69a"),
        L("M10 58L90 58", O, 3),
        L("M18 68Q50 74 82 68", "#6fd0c4", 2.5),
        HL(20, 70, 2.5, 6, -20), face(50, 76))


def quandong():
    pits = "".join(dot(x, y, 1.3, "#5a3418") for x, y in [(70, 70), (76, 72), (73, 77), (78, 78), (68, 76), (74, 67)])
    return svg(
        L("M12 20Q40 14 70 16", BROWN, 4),
        leaf(30, 17, 22, 9, -170, "#8fb08a", "#5f7f5a"),
        leaf(54, 16, 24, 9, -15, "#9cbc96", "#5f7f5a"),
        L("M40 16L40 24", BROWN, 3),
        C(40, 48, 26, "#e3263a"),
        F("M58 30C66 40 66 56 58 66Q62 50 56 34Z", "#ff6a78", ".7"),
        HL(26, 38, 3.5, 8, 25), face(40, 50),
        C(73, 73, 19, "#e3263a"),
        C(73, 73, 15, "#ffe7a8", "#f0b860", 2),
        C(73, 73, 9, "#c08a52", O, 2.5),
        pits)


def quenepa():
    def q(x, y, r):
        return C(x, y, r, "#7bb33a") + dot(x - r * 0.3, y + r * 0.3, 1.2, "#5a8f2a") + dot(x + r * 0.35, y, 1.2, "#5a8f2a") + HL(x - r * 0.4, y - r * 0.4, r * 0.16, r * 0.3, 30)
    return svg(
        L("M50 6L50 18M50 18L26 30M50 18L74 30M50 18L50 50M38 24L32 50M62 24L68 50", "#7a5a2a", 3),
        leaf(50, 11, 18, 9, -165, "#4caf50", LEAFD),
        leaf(50, 11, 18, 9, -15, LEAF, LEAFD),
        q(24, 34, 11), q(76, 34, 11), q(50, 30, 11),
        q(28, 56, 11), q(72, 56, 11),
        C(50, 66, 17, "#ffa77a"),
        P("M32 70L37 76L42 70L46 77L50 70L54 77L58 70L63 76L68 70Q70 90 50 90Q30 90 32 70Z", "#7bb33a"),
        dot(40, 84, 1.2, "#5a8f2a"), dot(58, 85, 1.2, "#5a8f2a"),
        HL(43, 57, 2.5, 5, 30), face(50, 63, 0.8))


# ---------------------------------------------------------------- R
def rhubarb():
    def stalk(x, rot, col):
        return T(f"rotate({rot} {x} 92)",
                 R(x - 8, 38, 16, 54, col, rx=7),
                 L(f"M{x - 3} 44L{x - 3} 86M{x + 3} 44L{x + 3} 86", "#f58a9a", 2))
    return svg(
        P(wavy(26, 30, 20, 16, 10, 0.08, rot=-20), "#3f9a3f"),
        P(wavy(74, 30, 20, 16, 10, 0.08, rot=20), "#3f9a3f"),
        P(wavy(50, 22, 22, 15, 11, 0.08), "#56b54a"),
        L("M50 36L50 10M50 32L36 18M50 32L64 18M38 40L14 28M62 40L86 28", "#a8dc80", 2),
        stalk(34, -14, "#d23a55"),
        stalk(66, 14, "#d23a55"),
        stalk(50, 0, "#e04862"),
        R(26, 70, 48, 10, "#f2d36b", rx=4),
        HL(45, 48, 1.8, 6, 0), face(50, 54, 0.62))


def rice():
    random.seed(9)
    grains = ""
    for _ in range(40):
        x = random.uniform(20, 80); y = random.uniform(30, 54)
        if y < 54 - 24 * (1 - ((x - 50) / 33) ** 2) + 2:
            continue
        grains += E(round(x, 1), round(y, 1), 1.4, 2.6, "#ffffff", "#cfc6b0", 1, rot=random.randint(-60, 60))
    return svg(
        TL("M60 50L92 12", "#c98a4b", 3), TL("M66 52L94 22", "#c98a4b", 3),
        P(wavy(50, 54, 36, 24, 9, 0.05), "#fffdf6"),
        grains,
        P("M10 56L90 56Q88 86 50 88Q12 86 10 56Z", "#3d7fd6"),
        L("M10 56L90 56", O, 3),
        L("M16 66Q24 62 32 66Q40 70 48 66Q56 62 64 66Q72 70 80 66", "#ffffff", 2.5),
        P("M38 88L62 88L60 94L40 94Z", "#2f68b8", O, 2.5),
        HL(20, 68, 2, 5, -20), face(50, 76))


# ---------------------------------------------------------------- S
def spinach():
    lv = ""
    for ang, col in [(-148, "#2e7d32"), (-32, "#2e7d32"), (-118, "#388e3c"), (-62, "#388e3c")]:
        a = math.radians(ang)
        lv += TL(f"M50 86L{50 + 8 * math.cos(a):.1f} {62 + 8 * math.sin(a):.1f}", "#9ccc65", 4)
        lv += leaf(50 + 8 * math.cos(a), 62 + 8 * math.sin(a), 36, 28, ang, col, "#7fc26a")
    return svg(
        lv,
        TL("M50 86L50 60", "#9ccc65", 4),
        leaf(50, 62, 50, 36, -90, "#43a047", "#8fd18a"),
        R(38, 68, 24, 9, "#e53935", rx=4),
        L("M44 82L42 92M50 82L50 93M56 82L58 92", "#9ccc65", 3),
        HL(40, 30, 3, 7, 20), face(50, 40, 0.85))


def sweet_potato():
    body = smooth_closed([(10, 40), (20, 24), (44, 18), (68, 22), (86, 34), (88, 46), (70, 56), (42, 60), (20, 56)])
    return svg(
        L("M10 40Q4 40 4 34M88 40Q94 38 95 32", O, 2.5),
        P(body, "#c4524a"),
        L("M30 26Q34 30 38 28M60 22Q62 26 66 26M24 50Q28 52 32 50M74 48Q76 52 80 50", "#8e332e", 2),
        HL(26, 32, 3, 7, 60), face(48, 38),
        P("M36 70C36 58 52 56 66 58C82 60 92 66 90 78C88 90 72 94 58 92C42 90 36 82 36 70Z", "#c4524a"),
        E(52, 76, 13, 16, "#ff9a2e", rot=10),
        E(52, 76, 7, 9, "#ffb75e", "#ffb75e", 1, rot=10),
        HL(48, 70, 2, 4, 30))


def starfruit():
    whole = T("rotate(-28 34 28)",
              E(34, 28, 28, 13, "#e9cf2c"),
              L("M10 26Q34 18 58 26M12 32Q34 38 56 32", "#c8a818", 2),
              L("M62 28L66 26", "#6a8a2a", 3))
    pts = []
    for i in range(10):
        a = math.radians(-90 + 36 * i)
        r = 34 if i % 2 == 0 else 19
        pts.append((56 + r * math.cos(a), 60 + r * math.sin(a)))
    inner = []
    for x, y in pts:
        inner.append((56 + (x - 56) * 0.78, 60 + (y - 60) * 0.78))
    seeds = ""
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        x = 56 + 16 * math.cos(a); y = 60 + 16 * math.sin(a)
        seeds += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="1.6" ry="3" fill="#8a5a2a" transform="rotate({math.degrees(a) + 90:.0f} {x:.1f} {y:.1f})"/>'
    return svg(
        whole,
        P(smooth_closed(pts), "#ffd23a"),
        F(smooth_closed(inner), "#fff09a"),
        seeds,
        HL(46, 42, 2.5, 5, 30), face(56, 62, 0.8))


# ---------------------------------------------------------------- T
def tangerine():
    def seg(x, y, rot):
        return T(f"rotate({rot} {x} {y})",
                 P(f"M{x - 16} {y}A16 15 0 0 1 {x + 16} {y}Q{x} {y + 4} {x - 16} {y}Z", "#ffb347", O, 2.8),
                 L(f"M{x - 9} {y - 4}Q{x} {y - 13} {x + 9} {y - 4}", "#ffe0b0", 2),
                 L(f"M{x} {y - 1}L{x} {y - 6}", "#ffe0b0", 1.6))
    dimples = "".join(dot(x, y, 1.2, "#e06a00") for x, y in [(22, 44), (34, 30), (60, 30), (70, 46), (28, 60), (62, 60)])
    return svg(
        L("M46 22L48 12", BROWN, 4),
        leaf(48, 14, 26, 12, -15, "#2e7d32", LEAFD),
        P("M46 22C66 18 84 30 84 46C84 62 66 70 46 70C26 70 8 62 8 46C8 30 26 18 46 22Z", "#ff8a1f"),
        dot(46, 24, 2.2, "#6b8e23"),
        dimples,
        HL(20, 36, 3, 7, 50), face(46, 46),
        seg(30, 90, -10), seg(68, 90, 10))


def turnip():
    bulb = "M50 32C24 32 14 46 16 60C18 74 36 82 50 90C64 82 82 74 84 60C86 46 76 32 50 32Z"
    return svg(
        leaf(44, 32, 26, 17, -118, "#43a047", LEAFD),
        leaf(56, 32, 26, 17, -62, "#43a047", LEAFD),
        leaf(50, 30, 22, 16, -90, LEAF, LEAFD),
        L("M50 88Q50 92 54 95", O, 2.5),
        P(bulb, "#fbf6ee"),
        F("M17 52C18 40 30 32 50 32C70 32 82 40 83 52Q72 58 62 54Q50 50 40 56Q28 60 17 52Z", "#9c3fa0"),
        P(bulb, "none"),
        L("M34 74L32 76M66 74L68 76", "#c8bba8", 2),
        HL(28, 44, 3, 6, 40), face(50, 66))


def tamarind():
    def pod_pts(p0, p1, p2, w0, nb, t0=0.0, t1=1.0):
        up, dn = [], []
        N = 40
        for i in range(N + 1):
            t = t0 + (t1 - t0) * i / N
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
            dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
            dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
            ln = math.hypot(dx, dy)
            nx, ny = -dy / ln, dx / ln
            w = w0 * (0.72 + 0.28 * abs(math.sin(nb * math.pi * t))) * min(1, (t / 0.14 + 0.02) ** 0.5, ((1 - t) / 0.14 + 0.02) ** 0.5)
            up.append((x + nx * w, y + ny * w)); dn.append((x - nx * w, y - ny * w))
        return up, dn
    def pod(p0, p1, p2, w0, nb, col):
        up, dn = pod_pts(p0, p1, p2, w0, nb)
        return P(smooth_closed(up + dn[::-1]), col)
    up, dn = pod_pts((12, 52), (50, 22), (90, 44), 11, 4, 0.8, 1.0)
    pulp = P(smooth_closed(up + dn[::-1]), "#6b3414")
    strings = L("M80 34Q84 40 86 46M76 40Q80 44 82 50", "#c08040", 1.6)
    return svg(
        L("M14 30L6 26M14 80L6 78", BROWN, 3),
        pod((12, 30), (50, 4), (90, 22), 8, 4, "#b98a52"),
        pod((12, 80), (50, 56), (90, 86), 9, 4, "#a8743e"),
        pod((12, 52), (50, 22), (90, 44), 11, 4, "#c4925a"),
        pulp, strings,
        HL(26, 42, 2, 5, 60), face(46, 40, 0.85))


# ---------------------------------------------------------------- U
def ube():
    body = smooth_closed([(12, 30), (22, 14), (44, 12), (62, 26), (74, 44), (64, 70), (42, 70), (24, 54)])
    return svg(
        L("M14 26Q6 20 8 12", O, 2.5),
        P(body, "#6b4a52"),
        L("M24 24Q28 28 32 26M40 18Q44 22 48 20M22 44Q26 48 30 46M46 60Q50 62 54 58", "#46303a", 2),
        HL(24, 30, 2.5, 6, 40),
        E(64, 64, 25, 27, "#6b4a52"),
        E(64, 64, 21, 23, "#8e3fd1", "#5a2a8a", 2),
        E(64, 64, 13, 15, "#b06ae8", "#b06ae8", 1),
        HL(52, 52, 2.5, 5, 30), face(64, 64))


def ume():
    def plum(x, y, r):
        return (C(x, y, r, "#cddc4a")
                + F(f"M{x + r * 0.2:.1f} {y - r * 0.95:.1f}A{r} {r} 0 0 1 {x + r * 0.9:.1f} {y + r * 0.45:.1f}Q{x + r * 0.2:.1f} {y:.1f} {x + r * 0.2:.1f} {y - r * 0.95:.1f}Z", "#ff8a65", ".8")
                + C(x, y, r, "none")
                + L(f"M{x:.1f} {y - r + 2:.1f}Q{x - r * 0.35:.1f} {y:.1f} {x - r * 0.1:.1f} {y + r - 3:.1f}", "#a8b830", 2))
    petals = ""
    for i in range(5):
        a = math.radians(-90 + 72 * i)
        petals += C(round(20 + 7 * math.cos(a), 1), round(22 + 7 * math.sin(a), 1), 6.5, "#ffc2d4", O, 2.2)
    return svg(
        L("M6 30Q40 14 92 14", BROWN, 4),
        leaf(66, 15, 22, 11, -30, LEAF, LEAFD),
        L("M44 20L44 32M78 15L78 26", BROWN, 2.5),
        petals, C(20, 22, 3.5, "#ffd54f", O, 1.5),
        plum(78, 38, 14),
        plum(46, 62, 27),
        HL(32, 52, 3.5, 7, 25), face(44, 64))


def urad_beans():
    random.seed(13)
    beans = ""
    for y, x0, x1, step in [(54, 14, 66, 7), (48, 18, 62, 7), (42, 24, 56, 7), (36, 32, 48, 8)]:
        n = int((x1 - x0) / step) + 1
        for i in range(n):
            x = x0 + i * (x1 - x0) / max(1, n - 1)
            beans += bean(round(x + random.uniform(-1, 1), 1), round(y + random.uniform(-1, 1), 1), 3.8, 3, random.randint(-40, 40), "#2b2530", 1.8, "#f2efe6")
    spill = "".join(bean(x, y, 3.8, 3, r, "#2b2530", 1.8, "#f2efe6") for x, y, r in [(22, 90, 15), (34, 92, -20), (86, 86, 30), (78, 92, -10)])
    return svg(
        TL("M66 60L92 34", "#c98a4b", 7),
        P("M10 56Q18 38 40 32Q62 38 70 56Z", "#4a4250", O, 2),
        beans,
        P("M8 56L72 56Q70 84 40 86Q10 84 8 56Z", "#d9a05a"),
        L("M8 56L72 56", O, 3),
        L("M14 66Q40 72 66 66", "#efc488", 2.5),
        spill,
        HL(16, 68, 2, 5, -20), face(40, 72))


# ---------------------------------------------------------------- V
def vanilla():
    pods = ""
    for d in ["M14 90Q30 56 52 30", "M24 92Q44 64 70 44", "M8 78Q22 52 36 36"]:
        pods += TL(d, "#4a2c1a", 5)
    petals = ""
    for i in range(5):
        a = -90 + 72 * i
        petals += leaf(68, 30, 24, 11, a, "#fff2b0", "#f2d36b", w=2.5)
    return svg(
        leaf(40, 64, 30, 14, -10, "#4caf50", LEAFD),
        pods,
        L("M20 82Q30 62 46 40", "#7a5232", 1.6),
        petals,
        P("M60 30Q60 46 68 48Q76 46 76 30Q68 26 60 30Z", "#f7c94a", O, 2.5),
        C(68, 30, 9, "#fff7cc", O, 2.5),
        face(68, 29, 0.6))


def veggie_basket():
    weave = L("M18 64L82 64M20 74L80 74M24 84L76 84M30 56L34 90M42 56L44 92M54 56L54 92M66 56L64 90", "#b07a3a", 2)
    return svg(
        L("M16 56Q50 0 84 56", O, 9), L("M16 56Q50 0 84 56", "#d9a25a", 4),
        P(wavy(32, 42, 18, 14, 9, 0.1), "#5cb85c"),
        L("M24 46Q32 36 40 34", "#a6dc80", 2),
        TL("M58 50L70 18", "#ff8a1f", 8),
        P("M70 18L64 6M70 18L72 4M70 18L80 8", "none", "#4caf50", 4),
        L("M64 34L67 33M60 42L63 41", "#c45a00", 2),
        C(48, 46, 13, "#e53935"),
        P("M42 36L48 40L54 36L52 42L44 42Z", "#4caf50", O, 2),
        HL(42, 46, 2, 4, 30),
        P("M10 54L90 54L80 92L20 92Z", "#d9a25a"),
        weave,
        R(8, 50, 84, 10, "#c48a42", rx=4),
        face(50, 74))


def violet_carrot():
    carrot = T("rotate(-14 42 56)",
               P("M36 26Q26 12 30 4Q40 12 42 24Z", LEAF), P("M46 24Q48 8 56 4Q58 16 50 26Z", LEAF), P("M42 24Q40 10 42 2Q50 10 48 24Z", "#4caf50"),
               P("M24 26Q42 20 60 26Q58 50 46 86Q42 92 38 86Q26 50 24 26Z", "#6a2a8a"),
               L("M30 40L36 40M48 52L54 52M34 62L39 62M44 72L48 72", "#4a1a62", 2.5),
               HL(32, 34, 2.5, 6, 10), face(42, 40, 0.85, O))
    return svg(
        carrot,
        C(72, 72, 19, "#6a2a8a"),
        C(72, 72, 14, "#b05ad0", "#4a1a62", 2),
        C(72, 72, 8, "#ffb030", "#e08a10", 2),
        HL(64, 64, 2, 4, 30))


# ---------------------------------------------------------------- W
def walnut():
    wr = L("M26 40Q32 44 28 50Q24 56 30 60M34 30Q40 36 36 42M38 58Q32 64 36 70M62 30Q56 36 60 42M70 40Q64 44 68 50Q72 56 66 60M58 58Q64 64 60 70", "#9a6a34", 2.2)
    return svg(
        C(46, 48, 30, "#c99a5c"),
        P("M46 14Q42 18 46 22Q50 18 46 14Z", "#b08048", O, 2),
        L("M46 20Q40 48 46 78", "#9a6a34", 3),
        wr,
        HL(28, 34, 3.5, 7, 30), face(46, 50),
        P("M56 74Q56 92 74 92Q92 92 92 74Z", "#c99a5c"),
        P(wavy(74, 72, 15, 10, 6, 0.12), "#efd29a"),
        L("M74 64L74 80M66 70Q70 74 66 78M82 70Q78 74 82 78", "#c09a5a", 2))


def wheat():
    def ear(x0, y0, x1, y1, n, col, s=1.0):
        out = TL(f"M{x0} {y0}L{x1} {y1}", "#d8a830", 2.5)
        ang = math.degrees(math.atan2(y1 - y0, x1 - x0))
        ln = math.hypot(x1 - x0, y1 - y0)
        ux, uy = (x1 - x0) / ln, (y1 - y0) / ln
        awn = ""
        for i in range(n):
            t = 0.42 + 0.58 * i / (n - 1)
            cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for side in (-1, 1):
                gx = cx + side * (-uy) * 4.2 * s; gy = cy + side * ux * 4.2 * s
                ex, ey = gx + (ux + side * -uy * 0.8) * 12, gy + (uy + side * ux * 0.8) * 12
                awn += f"M{gx:.1f} {gy:.1f}L{ex:.1f} {ey:.1f}"
        out += L(awn, "#c8962a", 1.4)
        for i in range(n):
            t = 0.42 + 0.58 * i / (n - 1)
            cx, cy = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            for side in (-1, 1):
                gx = cx + side * (-uy) * 4.2 * s; gy = cy + side * ux * 4.2 * s
                out += E(round(gx, 1), round(gy, 1), 3.4 * s, 5.6 * s, col, O, 2, rot=round(ang + 90 - side * 25))
        tx, ty = x1 + ux * 3, y1 + uy * 3
        out += E(round(tx, 1), round(ty, 1), 3.2 * s, 5 * s, col, O, 2, rot=round(ang + 90))
        return out
    return svg(T("translate(50 56) scale(0.88) translate(-50 -56)",
        ear(50, 92, 22, 22, 5, "#f2c14e"),
        ear(50, 92, 78, 22, 5, "#f2c14e"),
        ear(50, 92, 50, 14, 6, "#f7d066", 1.15),
        P("M40 74Q50 68 60 74L58 82Q50 78 42 82Z", "#e53935", O, 2.5),
        HL(46, 34, 1.5, 4, 0)))


def watercress():
    tips = [(24, 32, -150), (34, 20, -120), (50, 14, -90), (66, 20, -60), (76, 32, -30), (36, 38, -140), (64, 38, -40), (50, 32, -90)]
    stems = "".join(f"M50 70L{x} {y}" for x, y, a in tips)
    lv = ""
    cols = ["#3fa34d", "#4cb85a", "#5cc46a"]
    for k, (x, y, a) in enumerate(tips):
        for da in (-55, 55, 0):
            lv += leaf(x, y, 12, 10, a + da, cols[(k + da // 55) % 3], "#2e7d32", w=2.2)
    return svg(
        L(stems, "#5a9a3a", 2.5),
        lv,
        P("M28 50L72 50L68 90Q50 94 32 90Z", "#cfeefb"),
        F("M30 62L70 62L68 88Q50 92 32 88Z", "#8fd3f0"),
        L("M30 62L70 62", "#5ab0dc", 2),
        L("M40 50L42 88M50 50L50 90M58 50L58 88", "#5a9a3a", 2.5),
        P("M28 50L72 50L68 90Q50 94 32 90Z", "none"),
        R(26, 46, 48, 8, "#e6f6fd", rx=3),
        HL(34, 70, 1.8, 7, 0), face(50, 74, 0.9))


# ---------------------------------------------------------------- X
def ximenia():
    def fr(x, y, rx, ry, rot):
        return T(f"rotate({rot} {x} {y})",
                 E(x, y, rx, ry, "#f45a28"),
                 dot(x, y + ry - 2, 1.6, "#8a2a10"),
                 HL(x - rx * 0.4, y - ry * 0.35, rx * 0.18, ry * 0.3, 20))
    return svg(
        L("M8 20Q50 8 92 18", "#6a4a2a", 4),
        L("M20 16L17 10M62 12L65 7M84 16L88 12", "#6a4a2a", 2),
        leaf(30, 15, 20, 9, 175, "#6aaa5a", LEAFD),
        leaf(42, 13, 18, 8, -25, "#7cbc6a", LEAFD),
        leaf(74, 14, 22, 9, -10, "#6aaa5a", LEAFD),
        L("M28 15L26 34M76 16L78 36M52 12L50 36", "#6a4a2a", 2.5),
        fr(24, 50, 13, 17, 10),
        fr(78, 52, 13, 17, -10),
        E(50, 64, 21, 26, "#ff6a2a"),
        dot(50, 88, 1.8, "#8a2a10"),
        F("M62 48C70 58 70 72 62 82Q66 66 60 50Z", "#ff9a5a", ".8"),
        HL(38, 54, 3, 7, 20), face(50, 66))


def xoconostle():
    spines = ""
    for x, y in [(26, 56), (40, 50), (56, 54), (30, 72), (46, 70), (62, 70), (38, 86), (54, 86), (68, 58)]:
        spines += dot(x, y, 1.6, "#f2e6a0") + L(f"M{x - 2.5} {y - 2.5}L{x - 4.5} {y - 4.5}M{x + 2.5} {y - 2.5}L{x + 4.5} {y - 4.5}", "#f2e6a0", 1.2)
    def fruit(x, y, rot):
        return T(f"rotate({rot} {x} {y + 14})",
                 P(f"M{x - 11} {y + 12}C{x - 14} {y - 2} {x - 12} {y - 14} {x} {y - 14}C{x + 12} {y - 14} {x + 14} {y - 2} {x + 11} {y + 12}Q{x} {y + 18} {x - 11} {y + 12}Z", "#a5d06a"),
                 F(f"M{x - 12} {y - 2}C{x - 12} {y - 12} {x - 6} {y - 13} {x} {y - 13}C{x + 6} {y - 13} {x + 12} {y - 12} {x + 12} {y - 2}Q{x} {y + 4} {x - 12} {y - 2}Z", "#f06292"),
                 P(f"M{x - 11} {y + 12}C{x - 14} {y - 2} {x - 12} {y - 14} {x} {y - 14}C{x + 12} {y - 14} {x + 14} {y - 2} {x + 11} {y + 12}Q{x} {y + 18} {x - 11} {y + 12}Z", "none"),
                 P(f"M{x - 6} {y - 13}Q{x} {y - 9} {x + 6} {y - 13}Q{x} {y - 17} {x - 6} {y - 13}Z", "#c2185b", O, 1.8),
                 dot(x - 5, y + 2, 1.2, "#f8f0b0"), dot(x + 5, y + 4, 1.2, "#f8f0b0"), dot(x, y - 4, 1.2, "#f8f0b0"))
    return svg(
        fruit(30, 26, -20), fruit(70, 26, 20), fruit(50, 20, 0),
        P(wavy(48, 68, 30, 24, 8, 0.02), "#5fae4a"),
        spines,
        HL(28, 60, 3, 6, 40), face(48, 70))


def xiao_bai_cai():
    def stalk(rot):
        return T(f"rotate({rot} 50 90)",
                 P("M50 16C34 16 30 34 32 50C33 58 38 62 42 64L44 88L56 88L58 64C62 62 67 58 68 50C70 34 66 16 50 16Z", "#3f9a3f"),
                 L("M50 22L50 62", "#9fd880", 2.2),
                 L("M50 40L40 32M50 50L40 44M50 40L60 32M50 50L60 44", "#7cc26a", 1.6))
    return svg(
        stalk(-30), stalk(30), stalk(-14), stalk(14), stalk(0),
        P("M34 62Q50 54 66 62Q70 80 62 90Q50 94 38 90Q30 80 34 62Z", "#e4f4c4"),
        L("M42 64Q40 78 44 90M58 64Q60 78 56 90", "#b8dc8a", 2),
        HL(40, 30, 2.5, 7, 10), face(50, 74, 0.85))


# ---------------------------------------------------------------- Y
def yuzu():
    seeds = "".join(E(70 + x, 72 + y, 1.6, 2.6, "#fffbe0", "#c8a830", 1) for x, y in [(-5, -5), (5, -5), (0, 6)])
    segs = ""
    for i in range(9):
        a0 = i * 40
        segs += F(annulus_sector(70, 72, 3, 15, a0 + 3, a0 + 37), "#ffe680")
    dimples = "".join(dot(x, y, 1.1, "#e0b000") for x, y in [(22, 50), (34, 30), (52, 40), (30, 62), (52, 64), (60, 28)])
    return svg(
        L("M42 20L44 11", BROWN, 4),
        leaf(44, 12, 24, 11, -10, "#3f9a3f", LEAFD),
        P(wavy(40, 46, 30, 27, 13, 0.035), "#ffd21f"),
        dimples,
        HL(24, 38, 3.5, 7, 30), face(40, 48),
        C(70, 72, 22, "#ffd21f"),
        C(70, 72, 18, "#fff7c8", "#e8c040", 2),
        segs, seeds,
        HL(56, 60, 2, 4, 40))


def yardlong_beans():
    loops = ""
    for k, col in [(0, "#5aaa36"), (1, "#6cbf44"), (2, "#4f9e30")]:
        rx, ry = 34 - k * 5, 30 - k * 5
        pts = []
        for i in range(37):
            a = math.radians(100 + i * 9.6)
            pts.append((50 + rx * math.cos(a), 40 + ry * math.sin(a) + (k * 2)))
        d = smooth_open(pts)
        loops += TL(d, col, 5)
    ends = TL("M44 74Q38 84 30 90", "#5aaa36", 5) + TL("M50 74Q52 86 46 94", "#6cbf44", 5) + TL("M56 74Q64 84 72 88", "#4f9e30", 5)
    return svg(
        loops, ends,
        R(36, 60, 28, 16, "#e8c26a", rx=6),
        L("M40 64L60 64M40 72L60 72", "#c89a40", 1.6),
        face(50, 66, 0.7),
        HL(22, 26, 1.5, 5, 30))


def yellow_squash():
    body = smooth_closed([(36, 20), (30, 28), (36, 42), (40, 52), (32, 66), (36, 84), (56, 92), (78, 86), (86, 68),
                          (78, 52), (62, 44), (52, 34), (46, 22)])
    bumps = "".join(dot(x, y, 1.4, "#f0b000") for x, y in [(52, 54), (66, 60), (74, 74), (44, 80), (60, 82), (40, 34)])
    return svg(
        P("M38 22Q30 14 32 6L40 6Q40 14 44 20Z", "#6a9a3a", O, 2.5),
        P(body, "#ffd133"),
        L("M38 30Q42 44 50 50M70 52Q80 62 78 78", "#f0b000", 2),
        bumps,
        HL(42, 64, 3, 7, 20), face(58, 70))


# ---------------------------------------------------------------- Z
def zante_currants():
    berries = ""
    rows = [(36, 5), (46, 5), (56, 4), (65, 4), (74, 3), (82, 2), (89, 1)]
    for j, (y, n) in enumerate(rows):
        for i in range(n):
            x = 50 + (i - (n - 1) / 2) * 11
            berries += C(round(x, 1), y, 6, "#3e1f50", O, 2.2) + dot(round(x - 2, 1), y - 2, 1.4, "#9a7ab8")
    lobes = P("M58 14C60 6 70 4 74 10C80 6 90 10 86 18C92 22 88 30 80 28C78 34 68 32 66 26C58 28 54 20 58 14Z", "#5cb85c")
    return svg(
        L("M50 30L50 8Q52 4 56 4", BROWN, 4),
        lobes, L("M60 18L76 18M68 14L70 24", LEAFD, 1.8),
        berries,
        C(50, 56, 12, "#4a2a66", O, 2.5),
        HL(45, 51, 2, 3.5, 30), face(50, 56, 0.6, "#fff"))


def zucchini_flower():
    petals = ""
    for i in range(5):
        a = -90 + 72 * i + 10
        petals += leaf(60, 40, 30, 22, a, "#ffb300", "#ff8f00", w=3)
    inner = ""
    for i in range(5):
        a = -90 + 72 * i + 46
        inner += leaf(60, 40, 18, 14, a, "#ffd54f", "#ffb300", w=2)
    return svg(
        T("rotate(-38 30 72)",
          P("M6 72Q6 62 18 62L50 62Q58 62 58 72Q58 82 50 82L18 82Q6 82 6 72Z", "#3f9142"),
          L("M14 68L48 68M14 76L48 76", "#6fbf5a", 2),
          P("M4 72Q0 72 1 76L6 76Z", "#b8d66a", O, 2)),
        petals, inner,
        C(60, 40, 8, "#ff8f00", O, 2.5),
        face(60, 39, 0.55))


def zebra_tomato():
    body = "M42 26C30 20 10 28 9 48C8 68 24 80 42 80C60 80 76 68 75 48C74 28 54 20 42 26Z"
    streaks = ""
    for d in ["M24 30Q16 46 20 64Q22 48 28 32Z", "M36 28Q30 44 33 58Q35 44 40 28Z", "M50 28Q56 42 54 56Q50 42 46 28Z",
              "M62 32Q70 44 68 60Q64 46 58 32Z", "M14 52Q16 66 26 74Q18 64 16 50Z", "M70 54Q66 68 58 76Q66 66 72 52Z",
              "M40 64Q42 72 46 78Q40 74 38 66Z"]:
        streaks += F(d, "#3f7f2a")
    seeds = "".join(E(x, y, 1.3, 2.2, "#fff6b0", "#b8a840", 0.8, rot=r) for x, y, r in
                    [(64, 66, 30), (62, 74, -20), (80, 66, -30), (82, 74, 20), (72, 84, 90), (70, 62, 0)])
    return svg(
        P(body, "#c6dc48"),
        streaks,
        P(body, "none"),
        L("M42 26L42 10", "#2e7d32", 4),
        P(star_path(42, 27, 13, 0.32, 6), "#2e9a3a", O, 2.5),
        HL(22, 40, 3, 7, 25), face(42, 52),
        C(72, 72, 21, "#b5d94a"),
        C(72, 72, 17, "#cfe87a", "#8fbf3a", 2),
        E(64, 70, 6, 8, "#eef8b8", "#a8cc5a", 1.5), E(80, 70, 6, 8, "#eef8b8", "#a8cc5a", 1.5), E(72, 82, 8, 5, "#eef8b8", "#a8cc5a", 1.5),
        seeds,
        HL(60, 60, 2, 4, 40))


def add_more(K):
    K.add("N", "Napa cabbage", "Crunchy cabbage leaves!", napa_cabbage())
    K.add("N", "Navy beans", "Little white beans!", navy_beans())
    K.add("N", "Nutmeg", "A nut that smells yummy!", nutmeg())
    K.add("O", "Okra", "A green pod with a star inside!", okra())
    K.add("O", "Olives", "Green and black olives!", olives())
    K.add("P", "Peas", "Pop open the pod!", peas())
    K.add("Q", "Quinoa", "Tiny little grains!", quinoa())
    K.add("Q", "Quandong", "A little red fruit!", quandong())
    K.add("Q", "Quenepa", "Peel it and suck it!", quenepa())
    K.add("R", "Rhubarb", "Pink stalks, big leaves!", rhubarb())
    K.add("R", "Rice", "A bowl of white rice!", rice())
    K.add("S", "Spinach", "Green leaves make you strong!", spinach())
    K.add("S", "Sweet potato", "Orange and sweet inside!", sweet_potato())
    K.add("S", "Starfruit", "Cut it and see a star!", starfruit())
    K.add("T", "Tangerine", "Peel it and share it!", tangerine())
    K.add("T", "Turnip", "Purple and white!", turnip())
    K.add("T", "Tamarind", "Sticky and sour!", tamarind())
    K.add("U", "Ube", "Purple inside!", ube())
    K.add("U", "Ume plum", "A little green plum!", ume())
    K.add("U", "Urad beans", "Tiny black beans!", urad_beans())
    K.add("V", "Vanilla", "Smells so sweet!", vanilla())
    K.add("V", "Veggie basket", "A basket full of veggies!", veggie_basket())
    K.add("V", "Violet carrot", "A purple carrot!", violet_carrot())
    K.add("W", "Walnut", "Crack the shell!", walnut())
    K.add("W", "Wheat", "Golden wheat makes bread!", wheat())
    K.add("W", "Watercress", "Little leaves that love water!", watercress())
    K.add("X", "Ximenia", "Little orange fruits!", ximenia())
    K.add("X", "Xoconostle", "A pink cactus fruit!", xoconostle())
    K.add("X", "Xiao bai cai", "Baby bok choy!", xiao_bai_cai())
    K.add("Y", "Yuzu", "Bumpy and yellow!", yuzu())
    K.add("Y", "Yardlong beans", "Long, long beans!", yardlong_beans())
    K.add("Y", "Yellow squash", "A yellow squash with a bent neck!", yellow_squash())
    K.add("Z", "Zante currants", "Teeny tiny grapes!", zante_currants())
    K.add("Z", "Zucchini flower", "A yellow flower!", zucchini_flower())
    K.add("Z", "Zebra tomato", "A tomato with stripes!", zebra_tomato())
