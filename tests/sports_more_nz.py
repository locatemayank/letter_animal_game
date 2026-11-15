"""Extra Sports pictures N–Z (4 per letter in total; X has 3)."""
import math
from svgkit import *

WOOD = "#d7a86e"; WOODD = "#a1887f"; GOLD = "#ffc107"; RED = "#e53935"; BLUE = "#1e88e5"; GRASS = "#66bb6a"
SNOW = "#f4f9ff"; SKY = "#bbdefb"; WATER = "#4fc3f7"; GREY = "#90a4ae"; DARK = "#37474f"


def pt(cx, cy, r, deg):
    a = math.radians(deg)
    return cx + r * math.cos(a), cy + r * math.sin(a)


def arc(cx, cy, r, a0, a1):
    x0, y0 = pt(cx, cy, r, a0); x1, y1 = pt(cx, cy, r, a1)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{x0:.1f} {y0:.1f}A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}"


def ring(cx, cy, r, col, w=5):
    return C(cx, cy, r, "none", O, w + 4) + C(cx, cy, r, "none", col, w)


def waves(y, col="#42a5f5", w=3, x0=4, x1=96, amp=5, step=10):
    d = f"M{x0} {y}"
    x = x0
    up = True
    while x < x1:
        nx = min(x + step, x1)
        d += f"Q{(x + nx) / 2:g} {y - amp if up else y + amp} {nx:g} {y}"
        up = not up
        x = nx
    return L(d, col, w)


def num1(x, y, s, col, w=7):
    d = f"M{x - 6 * s:g} {y - 10 * s:g}L{x + 2 * s:g} {y - 16 * s:g}V{y + 16 * s:g}M{x - 7 * s:g} {y + 16 * s:g}H{x + 10 * s:g}"
    return TL(d, col, w)


def num2(x, y, s, col, w=6):
    d = (f"M{x - 8 * s:g} {y - 8 * s:g}Q{x - 6 * s:g} {y - 16 * s:g} {x:g} {y - 16 * s:g}"
         f"Q{x + 8 * s:g} {y - 16 * s:g} {x + 8 * s:g} {y - 8 * s:g}Q{x + 8 * s:g} {y - 2 * s:g} {x:g} {y + 4 * s:g}"
         f"L{x - 9 * s:g} {y + 16 * s:g}H{x + 9 * s:g}")
    return TL(d, col, w)


def num3(x, y, s, col, w=6):
    d = (f"M{x - 8 * s:g} {y - 12 * s:g}Q{x - 2 * s:g} {y - 18 * s:g} {x + 4 * s:g} {y - 15 * s:g}"
         f"Q{x + 10 * s:g} {y - 10 * s:g} {x + 5 * s:g} {y - 3 * s:g}Q{x + 2 * s:g} {y:g} {x - 3 * s:g} {y:g}"
         f"Q{x + 2 * s:g} {y:g} {x + 6 * s:g} {y + 4 * s:g}Q{x + 11 * s:g} {y + 12 * s:g} {x + 3 * s:g} {y + 16 * s:g}"
         f"Q{x - 4 * s:g} {y + 19 * s:g} {x - 9 * s:g} {y + 12 * s:g}")
    return TL(d, col, w)


def hubface(x, y, r, fc):
    return C(x, y, r * 0.42, "#ffca28", O, 2.5) + face(x, y - r * 0.06, fc)


def wheel(x, y, r, tyre="#37474f", hub="#cfd8dc", spokes=True, sw=None, fc=None):
    parts = [C(x, y, r, tyre), C(x, y, r * 0.62, hub, O, 2.5)]
    if spokes:
        d = ""
        for k in range(6):
            x1, y1 = pt(x, y, r * 0.62, 30 * k * 2 + 15)
            x2, y2 = pt(x, y, r * 0.62, 30 * k * 2 + 195)
            d += f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"
        parts.append(L(d, GREY, 1.5))
    if fc:
        parts.append(C(x, y, r * 0.42, "#ffca28", O, 2.5) + face(x, y - r * 0.06, fc))
    else:
        parts.append(C(x, y, r * 0.18, "#ffca28", O, 2))
    return "".join(parts)


# ---------------------------------------------------------------- N
def netball():
    net = "M44 26L48 50M52 27L54 50M60 27V50M68 27L66 50M76 26L72 50M46 38H74"
    return svg(
        R(14, 86, 34, 9, "#78909c", 4),
        TL("M31 88V12", "#cfd8dc", 6),
        TL("M31 16H44", "#cfd8dc", 4),
        L(net, "#eceff1", 2.2),
        E(60, 24, 17, 5, "none", O, 8), E(60, 24, 17, 5, "none", "#ff7043", 3.5),
        C(66, 70, 22, "#fff59d"),
        L("M46 58Q66 70 86 58M50 86Q66 70 82 86M66 48V92", "#ffb300", 2.5),
        C(66, 70, 22, "none"),
        HL(54, 58, 3, 6, 40), face(66, 72, 0.8))


def noodle():
    d = "M20 30Q24 96 50 80Q76 96 80 30"
    return svg(
        P("M4 60Q15 54 26 60T48 60T70 60T92 60T96 60V94H4Z", WATER),
        TL(d, "#ec407a", 14),
        L("M24 44Q28 82 46 76M76 44Q72 82 54 76", "#f48fb1", 3),
        E(20, 26, 10, 6, "#f06292"), E(20, 26, 3.5, 2, O, O, 1),
        E(80, 26, 10, 6, "#f06292"), E(80, 26, 3.5, 2, O, O, 1),
        L("M10 72Q16 68 22 72M70 90Q78 86 86 90M8 88Q14 84 20 88", "#e1f5fe", 2.5),
        face(50, 79, 0.65))


def number_bib():
    pin = lambda x, y, r: L(f"M{x - 5} {y + 3}L{x + 5} {y - 3}", "#78909c", 2.5) + C(x - 5, y + 3, 2.2, "#ffca28", O, 1.5)
    return svg(
        P("M8 26Q8 20 14 20H86Q92 20 92 26V80Q92 86 86 86H14Q8 86 8 80Z", "#fff"),
        F("M10 76H90V80Q90 84 86 84H14Q10 84 10 80Z", RED),
        L("M8 76H92", O, 2.5),
        L("M8 26Q8 20 14 20H86Q92 20 92 26V80Q92 86 86 86H14Q8 86 8 80Z"),
        pin(18, 28, 0), pin(82, 28, 0), pin(18, 68, 0), pin(82, 68, 0),
        num1(40, 48, 1.2, BLUE, 8),
        HL(18, 42, 2.5, 7, 0), face(66, 50, 0.75))


# ---------------------------------------------------------------- O
def olympic_rings():
    r = 9.5
    top = [(29, 42, "#1e88e5"), (51, 42, "#3d3d3d"), (73, 42, "#e53935")]
    bot = [(40, 52, "#fdd835"), (62, 52, "#43a047")]
    parts = [TL("M10 10V94", "#b0bec5", 4),
             P("M12 14Q36 6 56 14T92 14V70Q72 62 52 70T12 70Z", "#fff")]
    for x, y, c in top:
        parts.append(ring(x, y, r, c))
    for x, y, c in bot:
        parts.append(ring(x, y, r, c))
    # make them look linked: each top ring passes over the ring at its lower right
    for (x, y, c), (bx, by, _) in zip(top, bot):
        d = math.hypot(bx - x, by - y)
        ang = math.degrees(math.atan2(by - y, bx - x))
        a = ang + math.degrees(math.acos(d / (2 * r)))
        parts.append(F(annulus_sector(x, y, r - 2.5, r + 2.5, a - 14, a + 14), c))
    parts.append(C(10, 10, 4, GOLD, O, 2.5))
    parts.append(face(51, 80, 0.7))
    return svg(*parts)


def obstacle_course():
    tyre = lambda x, y: E(x, y, 14, 6, "#455a64") + E(x, y - 1, 6, 2.2, "#1a2a3a", O, 1.5) + L(f"M{x - 10} {y + 2}Q{x} {y + 6} {x + 10} {y + 2}", "#78909c", 1.5)
    return svg(
        E(50, 82, 47, 12, GRASS),
        P("M8 80V60A24 24 0 0 1 56 60V80Z", "#42a5f5"),
        F("M18 80V60A14 14 0 0 1 46 60V80Z", "#1a2a3a"),
        L("M13 48L20 53M32 36V46M51 48L44 53", "#ffeb3b", 4),
        L("M8 80V60A24 24 0 0 1 56 60V80Z"),
        L("M18 80V60A14 14 0 0 1 46 60V80", O, 2.5),
        TL("M68 82V54M90 82V54", "#eceff1", 4),
        R(62, 50, 34, 9, "#fff", 3),
        F("M68 51H74V58H68Z M80 51H86V58H80Z", RED),
        R(62, 50, 34, 9, "none", 3),
        tyre(42, 88), tyre(70, 87),
        HL(20, 44, 2.5, 6, -40), face(32, 70, 0.6, "#fff"))


def torch():
    return svg(
        P("M50 4Q72 20 70 36Q68 48 50 48Q32 48 30 36Q28 22 40 14Q40 24 46 26Q44 14 50 4Z", "#ff7043"),
        P("M50 22Q62 30 60 38Q58 44 50 44Q42 44 41 38Q40 30 50 22Z", "#ffeb3b", O, 2),
        P("M30 46H70L66 54H34Z", "#ffd54f"),
        P("M34 54H66L54 94H46Z", GOLD),
        L("M38 66H62M42 80H58", "#ffb300", 2.5),
        HL(40, 60, 2, 5, 10), face(50, 64, 0.6))


# ---------------------------------------------------------------- P
def ping_pong():
    return svg(
        L("M24 72V92M76 72V92", O, 4),
        P("M8 70L22 44H78L92 70Z", "#2e7d32"),
        P("M8 70H92V76H8Z", "#1b5e20", O, 2.5),
        L("M50 46V70", "#fff", 2), L("M12 68L24 46M88 68L76 46", "#fff", 1.6),
        R(14, 52, 72, 6, "#eceff1", 1, O, 2),
        L("M20 55H80", GREY, 1),
        T("rotate(-35 22 26)", TL("M22 34V46", WOOD, 6), C(22, 22, 13, RED)),
        T("rotate(35 78 26)", TL("M78 34V46", WOOD, 6), C(78, 22, 13, "#1e88e5")),
        C(50, 14, 6, "#fff", O, 2.5),
        L("M36 18Q42 10 44 14", "#b0bec5", 2),
        HL(18, 18, 2, 4, 40), face(36, 62, 0.6, "#fff"))


def pogo_stick():
    coil = "M44 66L56 69L44 72L56 75L44 78L56 81"
    return svg(
        L("M18 40Q12 50 18 60M82 40Q88 50 82 60", "#90a4ae", 2.5),
        L("M10 82H22M78 82H90", "#90a4ae", 2.5),
        TL("M50 64V88", "#b0bec5", 4),
        L(coil, O, 6), L(coil, "#cfd8dc", 3),
        R(44, 86, 12, 8, "#263238", 3),
        TL("M22 14H78", "#78909c", 4),
        R(12, 9, 16, 10, RED, 5), R(72, 9, 16, 10, RED, 5),
        R(40, 14, 20, 50, "#7e57c2", 8),
        TL("M24 62H76", "#78909c", 4),
        R(18, 58, 16, 8, "#ffca28", 3), R(66, 58, 16, 8, "#ffca28", 3),
        HL(45, 26, 2, 6, 0), face(50, 36, 0.6))


def parachute():
    cols = ["#e53935", "#ffca28", "#43a047", "#1e88e5"]
    parts = []
    # canopy split into 4 vertical gores
    xs = [8, 29, 50, 71, 92]
    for i in range(4):
        x0, x1 = xs[i], xs[i + 1]
        parts.append(F(f"M50 6L{x0} {40 if i == 0 else 40}Q{(x0 + x1) / 2} {46} {x1} 40Z", cols[i]))
    dome = "M8 40Q8 6 50 6Q92 6 92 40Q81 34 71 40Q60 34 50 40Q40 34 29 40Q19 34 8 40Z"
    # fill wedges approximated by drawing dome per colour band via vertical slices
    parts = [P(dome, "#fff")]
    bands = [("M8 40Q8 14 26 9L29 40Q19 34 8 40Z", "#e53935"),
             ("M50 6L50 40Q60 34 71 40L74 9Q62 6 50 6Z", "#1e88e5")]
    bands = [("M8 40Q8 14 28 8Q34 30 29 40Q19 34 8 40Z", "#e53935"),
             ("M50 6Q64 6 72 8Q76 30 71 40Q60 34 50 40Z", "#ffca28"),
             ("M28 8Q38 6 50 6V40Q40 34 29 40Q34 30 28 8Z", "#fff"),
             ("M72 8Q92 14 92 40Q81 34 71 40Q76 30 72 8Z", "#1e88e5")]
    for d, c in bands:
        parts.append(F(d, c))
    parts += [L("M28 8Q34 30 29 40M50 6V40M72 8Q76 30 71 40", O, 2), L(dome),
              L("M8 40L44 68M29 40L47 66M71 40L53 66M92 40L56 68", "#795548", 1.6),
              # teddy
              C(41, 60, 4, "#a1887f", O, 2.5), C(59, 60, 4, "#a1887f", O, 2.5),
              E(50, 84, 12, 10, "#a1887f"),
              E(50, 87, 6, 5, "#d7ccc8", O, 2),
              C(50, 68, 10, "#a1887f"),
              E(50, 72, 4.5, 3.5, "#d7ccc8", O, 1.5),
              HL(22, 22, 3, 7, 40), face(50, 67, 0.55)]
    return svg(*parts)


# ---------------------------------------------------------------- Q
def quiver():
    return svg(
        L("M30 30Q10 60 40 92", "#6d4c41", 4),
        T("rotate(18 52 56)",
          TL("M42 34V8M52 34V4M62 34V10", WOOD, 3),
          P("M42 8L37 2V14L42 18L47 14V2Z", RED, O, 2),
          P("M52 4L47 -2V10L52 14L57 10V-2Z", "#ffca28", O, 2),
          P("M62 10L57 4V16L62 20L67 16V4Z", "#1e88e5", O, 2),
          P("M34 28H70V86Q70 94 52 94Q34 94 34 86Z", "#8d6e63"),
          R(32, 26, 40, 9, "#6d4c41", 4),
          L("M34 78H70", "#6d4c41", 3),
          HL(40, 46, 2.5, 8, 0), face(52, 56, 0.75)))


def quad_bike():
    return svg(
        L("M4 78H12M2 66H10", GREY, 2.5),
        wheel(24, 74, 16, spokes=False), wheel(78, 74, 16, spokes=False),
        P("M10 58Q14 44 30 46H70Q86 44 92 58L86 62Q78 52 66 56L60 64H40L34 56Q22 52 14 62Z", RED),
        P("M38 46Q38 36 52 36H62Q66 36 66 42V46Z", "#263238", O, 2.5),
        TL("M74 46L70 26", "#78909c", 3),
        TL("M62 24H80", "#263238", 4),
        L("M84 50L92 50", "#ffeb3b", 4),
        HL(22, 52, 2, 5, 60), face(50, 53, 0.6, "#fff"))


def quarter_pipe():
    curve = "M6 88Q74 88 74 18"
    bt, nx, ny = -45, -0.707, -0.707
    bx, by = 59 + 7 * nx, 71 + 7 * ny
    return svg(
        L("M76 18V6M92 18V6M76 8H92", GREY, 3),
        P("M6 88Q74 88 74 18H92V88Z", "#4dd0e1"),
        P("M6 88Q74 88 74 18H80Q80 92 6 92Z", "#d7a86e", O, 2.5),
        L("M74 18H92", "#b0bec5", 5), L("M74 18H92", O, 1.2),
        L("M84 30V80", "#26c6da", 2.5),
        R(4, 88, 92, 7, "#a1887f", 3),
        T(f"rotate({bt} {bx:.1f} {by:.1f})",
          R(bx - 14, by - 6, 28, 6, "#ffca28", 3, O, 2.5),
          C(bx - 8, by + 3, 3, RED, O, 2), C(bx + 8, by + 3, 3, RED, O, 2)),
        L("M30 66Q36 58 42 54M24 60Q30 52 36 48", GREY, 2),
        HL(88, 34, 1.5, 5, 0), face(84, 64, 0.55))


# ---------------------------------------------------------------- R
def rugby_ball():
    rx, ry = 42, 27

    def band(a, b, col):
        ha = ry * math.sqrt(1 - (a / rx) ** 2); hb = ry * math.sqrt(1 - (b / rx) ** 2)
        k = 6 if a < 0 else -6
        return P(f"M{a} {-ha:.1f}A{rx} {ry} 0 0 {1 if a < b else 0} {b} {-hb:.1f}"
                 f"Q{b + k} 0 {b} {hb:.1f}A{rx} {ry} 0 0 {1 if a < b else 0} {a} {ha:.1f}"
                 f"Q{a + k} 0 {a} {-ha:.1f}Z".replace("A", "A").replace("0 0 1 " + str(b) + " " + f"{hb:.1f}", "0 0 0 " + str(b) + " " + f"{hb:.1f}"), col, O, 2.5)

    def band2(a, b, col):
        ha = ry * math.sqrt(1 - (a / rx) ** 2); hb = ry * math.sqrt(1 - (b / rx) ** 2)
        ka = 7 if a < 0 else -7
        return P(f"M{a} {-ha:.1f}L{b} {-hb:.1f}Q{b + ka} 0 {b} {hb:.1f}L{a} {ha:.1f}Q{a + ka} 0 {a} {-ha:.1f}Z", col, O, 2.5)

    return svg(T("translate(50 52) rotate(-22)",
                 E(0, 0, rx, ry, "#fff"),
                 band2(-28, -22, "#1e88e5"), band2(28, 22, "#1e88e5"),
                 band2(-34, -30, RED), band2(34, 30, RED),
                 E(0, 0, rx, ry, "none"),
                 HL(-14, -16, 3, 7, 70), face(0, 0, 0.85)))


def roller_skate():
    return svg(
        L("M2 50H14M4 60H12", GREY, 2.5),
        L("M34 76V82M74 76V82", O, 4),
        C(28, 84, 9, "#ffeb3b"), C(38, 84, 9, "#ffeb3b"), C(70, 84, 9, "#ffeb3b"), C(80, 84, 9, "#ffeb3b"),
        dot(38, 84, 2.5, O), dot(80, 84, 2.5, O),
        R(18, 72, 70, 8, "#b0bec5", 3),
        C(90, 72, 5, "#ec407a", O, 2.5),
        P("M24 8H56L56 46Q82 48 88 62V72H20Q18 40 24 8Z", "#26c6da"),
        P("M24 8H56V15H24Z", "#fff", O, 2.5),
        L("M48 22L56 28M56 22L48 28M48 34L56 40M56 34L48 40", "#fff", 2.5),
        P("M20 66H88V72H20Z", "#fff", O, 2.5),
        HL(28, 26, 2.5, 8, 0), face(38, 52, 0.85))


def relay_baton():
    return svg(
        P("M2 92L30 70H70L98 92Z", "#ef6c4a"),
        L("M22 92L38 70M50 92V70M78 92L62 70", "#fff", 2.5),
        L("M4 34H22M8 44H24M4 54H18", GREY, 2.5),
        T("rotate(-28 56 44)",
          R(22, 32, 68, 24, RED, 12),
          E(80, 44, 6, 11, "#c62828", O, 3),
          E(80, 44, 3, 6, "#7f1d1d", O, 1.5),
          L("M40 33V55", "#ffca28", 4),
          HL(30, 38, 2, 5, 70), face(56, 44, 0.75)))


# ---------------------------------------------------------------- S
def surfboard():
    return svg(
        P("M2 94V52Q12 24 46 16Q78 10 92 30Q98 44 86 48Q74 50 74 40Q76 32 66 32Q48 32 40 52Q36 70 40 94Z", "#1e88e5"),
        P("M46 16Q78 10 92 30Q98 44 86 48Q78 48 76 42Q86 40 84 32Q74 22 52 22Z", "#e3f2fd", O, 2.5),
        L("M14 50Q20 36 34 30M10 70Q14 60 22 54", "#64b5f6", 3),
        T("rotate(-24 56 66)",
          P("M14 66Q34 54 66 56Q94 58 98 66Q94 74 66 76Q34 78 14 66Z", "#ffca28"),
          L("M22 66Q56 64 92 66", "#ff7043", 4),
          P("M30 74L24 84L38 76Z", "#ff7043", O, 2),
          HL(42, 60, 2, 6, 80), face(60, 67, 0.75)),
        P("M2 94Q24 82 48 88T98 84V96H2Z", "#42a5f5"))


def skis():
    return svg(
        P("M-4 104V72Q30 56 56 66Q78 74 104 58V104Z", SNOW),
        L("M8 96L60 8", GREY, 3), L("M92 96L40 8", GREY, 3),
        E(14, 86, 6, 2, "#78909c", O, 2), E(86, 86, 6, 2, "#78909c", O, 2),
        C(60, 8, 3, "#263238", O, 1.5), C(40, 8, 3, "#263238", O, 1.5),
        T("rotate(-24 50 54)",
          P("M42 92V22Q42 10 48 8Q54 8 54 22V92Q54 96 48 96Q42 96 42 92Z", RED),
          R(40, 54, 16, 10, "#455a64", 2, O, 2)),
        T("rotate(24 50 54)",
          P("M42 92V22Q42 10 48 8Q54 8 54 22V92Q54 96 48 96Q42 96 42 92Z", "#1e88e5"),
          R(40, 54, 16, 10, "#455a64", 2, O, 2)),
        L("M20 74Q24 78 28 74M72 80Q76 84 80 80", "#cfd8dc", 2),
        face(50, 86, 0.6))


def stopwatch():
    ticks = ""
    for k in range(12):
        x1, y1 = pt(50, 56, 26, 30 * k); x2, y2 = pt(50, 56, 22 if k % 3 == 0 else 24, 30 * k)
        ticks += f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"
    return svg(
        R(42, 6, 16, 8, "#b0bec5", 3), R(44, 12, 12, 8, "#78909c", 2),
        T("rotate(40 78 26)", R(72, 20, 12, 8, RED, 3)),
        C(50, 56, 38, "#43a047"),
        C(50, 56, 30, "#fff", O, 2.5),
        L(ticks, O, 2),
        L("M50 56L64 36", RED, 3), dot(50, 56, 3, O),
        HL(26, 36, 3, 8, 40), face(44, 66, 0.65))


# ---------------------------------------------------------------- T
def tennis_ball():
    fuzz = ""
    for k in range(24):
        x1, y1 = pt(50, 50, 38, 15 * k + 7); x2, y2 = pt(50, 50, 41, 15 * k + 7)
        fuzz += f"M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}"
    return svg(
        L(fuzz, "#c0ca33", 2.5),
        C(50, 50, 38, "#d4e157"),
        L("M22 24Q42 50 22 76M78 24Q58 50 78 76", "#fff", 4),
        C(50, 50, 38, "none"),
        HL(32, 30, 4, 8, 40), face(50, 52, 0.95))


def trampoline():
    springs = ""
    for k in range(14):
        a = 360 * k / 14
        x1, y1 = pt(0, 0, 1, a)
        springs += f"M{50 + 30 * x1:.1f} {44 + 8 * y1:.1f}L{50 + 40 * x1:.1f} {44 + 12 * y1:.1f}"
    return svg(
        L("M24 10Q20 16 24 22M76 10Q80 16 76 22M50 6V18", GREY, 2.5),
        TL("M18 52L12 90M82 52L88 90M36 56L32 92M64 56L68 92", "#546e7a", 3),
        TL("M14 80H34M66 80H86", "#546e7a", 2),
        E(50, 44, 44, 15, "#1e88e5"),
        E(50, 44, 30, 8, "#263238", O, 2.5),
        L(springs, "#cfd8dc", 1.5),
        P("M6 44Q8 60 50 60Q92 60 94 44Q92 54 50 54Q8 54 6 44Z", "#1565c0", O, 2.5),
        HL(20, 38, 2, 6, -70),
        C(50, 22, 9, "#ffca28"), face(50, 22, 0.5))


def tricycle():
    return svg(
        wheel(34, 80, 11, spokes=False),
        TL("M60 40L66 66", "#e53935", 5),
        wheel(66, 66, 24),
        TL("M18 82L40 58L62 44", "#e53935", 5),
        TL("M18 82H36", "#e53935", 4),
        wheel(18, 82, 11, spokes=False),
        TL("M40 58L36 48", "#e53935", 4),
        E(34, 46, 12, 5, "#263238", O, 2.5),
        TL("M57 26L62 44", "#e53935", 5),
        TL("M57 26L54 12H70", "#78909c", 3),
        R(64, 8, 16, 8, "#ffca28", 4, O, 2.5),
        TL("M66 66L80 84", "#455a64", 2), R(74, 82, 14, 6, "#263238", 2, O, 2),
        hubface(66, 66, 24, 0.55),
        HL(46, 54, 1.5, 4, 40))


# ---------------------------------------------------------------- U
def unicycle():
    return svg(
        L("M14 86H26M76 86H88", GREY, 2.5),
        TL("M50 68L40 56", "#78909c", 3), R(30, 51, 14, 6, "#263238", 2, O, 2),
        TL("M50 20V64", "#ab47bc", 6),
        wheel(50, 68, 24),
        TL("M50 68L62 82", "#78909c", 3), R(56, 80, 14, 6, "#263238", 2, O, 2),
        hubface(50, 68, 24, 0.55),
        P("M30 10Q50 4 70 10Q74 18 60 20H40Q26 18 30 10Z", "#263238", O, 3),
        HL(40, 12, 3, 2, 0))


def umpire_chair():
    return svg(
        TL("M24 92L32 44M76 92L68 44", "#2e7d32", 5),
        TL("M28 80H72M30 66H70M32 54H68", "#2e7d32", 4),
        P("M26 30H74V44Q74 48 70 48H30Q26 48 26 44Z", "#43a047"),
        P("M30 6H70Q74 6 74 10V32H26V10Q26 6 30 6Z", "#66bb6a"),
        TL("M18 30H28M72 30H82", "#2e7d32", 4),
        R(12, 86, 20, 8, "#795548", 3), R(68, 86, 20, 8, "#795548", 3),
        HL(32, 14, 2, 6, 0), face(50, 19, 0.8))


def uneven_bars():
    return svg(
        R(4, 82, 92, 12, "#42a5f5", 4),
        L("M28 82V88M72 82V88", "#1e88e5", 2),
        TL("M20 82V16M80 82V16", "#90a4ae", 4),
        TL("M18 84L30 66M82 84L70 66", "#90a4ae", 3),
        TL("M38 82V50M62 82V50", "#90a4ae", 4),
        TL("M14 16H86", "#ffca28", 4),
        TL("M32 50H68", "#ffca28", 4),
        HL(12, 86, 2, 4, 90), face(50, 88, 0.55, "#fff"))


# ---------------------------------------------------------------- V
def visor():
    G1, G2, G3 = "#ec407a", "#ad1457", "#f48fb1"
    cx, cy, rx, ry, h = 36, 36, 28, 12, 12
    back = f"M{cx - rx} {cy}A{rx} {ry} 0 0 1 {cx + rx} {cy}V{cy + h}A{rx} {ry} 0 0 0 {cx - rx} {cy + h}Z"
    front = f"M{cx - rx} {cy}A{rx} {ry} 0 0 0 {cx + rx} {cy}V{cy + h}A{rx} {ry} 0 0 1 {cx - rx} {cy + h}Z"
    p = lambda t: (cx + rx * math.cos(math.radians(t)), cy + h - 3 + ry * math.sin(math.radians(t)))
    a = p(120); b = p(-5)
    brim = f"M{a[0]:.1f} {a[1]:.1f}C30 96 92 98 96 70C98 56 80 46 {b[0]:.1f} {b[1]:.1f}Z"
    return svg(
        C(84, 16, 7, "#ffca28", O, 2), L("M84 2V4M98 16H96M74 6L76 8M94 6L92 8", "#ffb300", 2.5),
        P(brim, G3),
        L("M38 74Q70 92 90 66", "#fff", 2),
        P(back, G2),
        P(front, G1),
        L(f"M{cx - rx} {cy}A{rx} {ry} 0 0 1 {cx + rx} {cy}"),
        HL(14, 46, 2, 4, 20), face(66, 72, 0.75))


def vaulting_horse():
    return svg(
        TL("M28 52L16 88M72 52L84 88M38 56L34 88M62 56L66 88", "#78909c", 4),
        TL("M22 72H78", "#78909c", 3),
        R(12, 26, 76, 28, "#8d6e63", 14),
        L("M20 30H80", "#a1887f", 2),
        R(8, 86, 18, 8, "#455a64", 3), R(74, 86, 18, 8, "#455a64", 3),
        HL(22, 34, 2.5, 5, 70), face(50, 40, 0.85))


def podium():
    return svg(
        P(star_path(50, 14, 10), GOLD, O, 2.5),
        R(34, 30, 32, 62, "#ffd54f", 3),
        R(6, 50, 30, 42, "#e0e0e0", 3),
        R(64, 62, 30, 30, "#ffab91", 3),
        num1(50, 46, 0.7, "#e65100", 5),
        num2(21, 66, 0.55, "#546e7a", 4.5),
        num3(79, 76, 0.5, "#bf360c", 4.5),
        HL(40, 36, 2, 5, 0), face(50, 74, 0.7))


# ---------------------------------------------------------------- W
def water_bottle():
    return svg(
        L("M66 10Q72 4 78 8M68 18Q76 16 80 20", "#4fc3f7", 2.5),
        R(44, 6, 12, 12, "#ffca28", 3),
        R(34, 16, 32, 12, "#ffca28", 4),
        P("M30 28H70Q74 28 74 34V50Q68 56 68 62Q74 68 74 74V88Q74 94 68 94H32Q26 94 26 88V74Q32 68 32 62Q26 56 26 50V34Q26 28 30 28Z", "#29b6f6"),
        P("M28 66H72V74H28Z", "#e1f5fe", O, 2),
        HL(34, 40, 2.5, 7, 0), face(50, 44, 0.8))


def wetsuit():
    return svg(
        P("M38 6H62L84 18L94 52L84 56L72 30V58L76 92H56L50 64L44 92H24L28 58V30L16 56L6 52L16 18Z", "#263238"),
        P("M16 18L38 6H42L36 30L28 30V22Z", "#26c6da", O, 2.5),
        P("M84 18L62 6H58L64 30L72 30V22Z", "#26c6da", O, 2.5),
        F("M8 50L16 52M84 52L92 50", "none"),
        R(4, 48, 12, 8, "#26c6da", 3, O, 2.5, rot=22), R(84, 48, 12, 8, "#26c6da", 3, O, 2.5, rot=-22),
        R(24, 84, 20, 8, "#26c6da", 3, O, 2.5), R(56, 84, 20, 8, "#26c6da", 3, O, 2.5),
        L("M50 8V46", "#90a4ae", 2.5),
        HL(36, 40, 2, 6, 0), face(50, 34, 0.7, "#fff"))


def racing_wheelchair():
    return svg(
        L("M2 94H98", "#ef6c4a", 3),
        TL("M50 50L86 82", "#78909c", 4),
        wheel(86, 84, 8, spokes=False),
        C(36, 62, 30, "none", O, 3),
        C(36, 62, 28, "#e3f2fd", "#37474f", 5),
        C(36, 62, 22, "none", "#ffca28", 3),
        L("M36 34V90M8 62H64M16 42L56 82M56 42L16 82", GREY, 1.5),
        R(10, 6, 16, 36, "#1e88e5", 6),
        R(10, 30, 50, 12, "#1e88e5", 6),
        hubface(36, 62, 30, 0.6),
        HL(15, 14, 1.5, 6, 0))


# ---------------------------------------------------------------- X
def xc_skis():
    ski = lambda y, col: P(f"M6 {y}H84Q92 {y} 94 {y - 8}Q98 {y - 6} 96 {y - 2}Q92 {y + 6} 84 {y + 6}H6Z", col, O, 2.5)
    return svg(
        P("M-4 104V46Q50 36 104 46V104Z", SNOW),
        L("M2 70H98M2 76H98M2 86H98M2 92H98", "#90caf9", 2),
        L("M10 52Q14 56 18 52M80 48Q84 52 88 48", "#cfd8dc", 2),
        TL("M36 72L28 12", GREY, 2), TL("M64 72L72 12", GREY, 2),
        E(35, 66, 6, 2, "#78909c", O, 2), E(65, 66, 6, 2, "#78909c", O, 2),
        P("M26 8L30 8L31 18L27 18Z", RED, O, 2), P("M70 8L74 8L73 18L69 18Z", RED, O, 2),
        ski(73, "#ff7043"), ski(88, "#29b6f6"),
        R(40, 68, 14, 5, "#455a64", 2, O, 2), R(40, 83, 14, 5, "#455a64", 2, O, 2),
        HL(14, 75, 1, 4, 90), HL(14, 90, 1, 4, 90))


def xare():
    # hoop seen at an angle, loose net bag sagging below it
    bag = "M20 30Q18 66 42 70Q66 66 64 30"
    mesh = ("M26 34Q28 58 42 66M34 36Q34 56 42 68M50 36Q50 56 42 68M58 34Q56 58 42 66"
            "M22 44Q42 52 63 44M24 54Q42 62 61 54")
    return svg(
        T("rotate(-24 42 40)",
          TL("M42 66V98", WOOD, 7),
          P(bag + "Z", "#fffde7", O, 2.5),
          L(mesh, "#bdbdbd", 1.6),
          L(bag, O, 2.5),
          E(42, 30, 23, 11, "none", O, 10), E(42, 30, 23, 11, "none", "#a1683a", 6)),
        C(78, 78, 12, "#f5f5f5"),
        L("M68 74Q78 78 72 88M88 72Q80 78 86 86", "#8d6e63", 2),
        HL(72, 72, 2, 4, 40), face(78, 79, 0.55))


# ---------------------------------------------------------------- Y
def yacht():
    return svg(
        TL("M50 8V68", WOOD, 4),
        P("M54 10Q80 38 88 64H54Z", "#fff"),
        P("M46 16Q32 40 14 62H46Z", "#ffca28"),
        P("M50 8L62 12L50 16Z", RED, O, 2),
        P("M8 66H92Q86 84 50 84Q14 84 8 66Z", RED),
        P("M8 66H92L90 71H10Z", "#fff", O, 2.5),
        waves(88, "#42a5f5", 3, 2, 98, 4, 8),
        HL(62, 40, 2, 6, -30), face(50, 76, 0.7))


def yoga_mat():
    return svg(
        P("M24 60H78L70 90H8Z", "#ab47bc"),
        L("M22 66L14 86M74 66L66 86", "#ce93d8", 2.5),
        R(22, 34, 56, 28, "#ba68c8", 14),
        E(78, 48, 9, 14, "#ce93d8"),
        L("M78 48m-2 0a2 3 0 1 0 4 0a4 6 0 1 0 -8 0a6 9 0 1 0 12 0", "#7b1fa2", 1.8),
        HL(34, 40, 2, 6, 70), face(42, 76, 0.75, "#fff"))


def yellow_card():
    return svg(
        T("rotate(-14 42 48)",
          R(18, 10, 48, 70, "#ffeb3b", 6),
          HL(26, 22, 2.5, 8, 0), face(42, 46, 0.9)),
        L("M78 60Q90 50 86 34", O, 2.2),
        P("M64 86A12 12 0 1 1 82 72H94V82H78Q74 90 64 86Z", "#b0bec5"),
        E(86, 72, 4, 1.5, "#263238", O, 1.5),
        HL(62, 74, 2, 4, 40))


# ---------------------------------------------------------------- Z
def zorb():
    return svg(
        E(50, 88, 44, 10, GRASS),
        C(50, 48, 40, "#e1f5fe"),
        C(50, 48, 22, "#fff", "#4fc3f7", 3),
        L("M50 8V26M50 70V88M10 48H28M72 48H90M22 20L34 32M78 20L66 32M22 76L34 64M78 76L66 64", "#81d4fa", 1.6),
        C(50, 48, 40, "none"),
        HL(26, 26, 5, 11, 40), HL(42, 36, 2, 4, 40), face(50, 50, 0.8))


def zumba():
    return svg(
        P("M66 8V30", "none"),
        L("M70 10V32M70 10L86 6V26", O, 3), C(66, 32, 4.5, "#ec407a", O, 2.5), C(82, 27, 4.5, "#ec407a", O, 2.5),
        L("M20 10V28", O, 3), L("M20 10Q26 12 28 18", O, 3), C(16, 28, 4.5, "#7e57c2", O, 2.5),
        P("M8 80Q8 64 16 56L36 52Q46 58 56 54L74 60Q92 66 92 78Q92 86 82 86H14Q8 86 8 80Z", "#ec407a"),
        P("M8 80H92Q92 90 84 90H14Q8 90 8 80Z", "#ffeb3b", O, 2.5),
        P("M36 52Q46 58 56 54L60 64Q46 68 34 62Z", "#fff", O, 2),
        L("M38 58L42 64M46 58L48 66M54 58L54 64", "#26c6da", 2),
        P(star_path(24, 72, 6), "#ffeb3b", O, 1.8),
        HL(20, 62, 2, 4, 40), face(74, 74, 0.7))


def zigzag_run():
    pts = [(22, 86), (76, 72), (26, 56), (72, 42), (32, 28)]
    cols = [RED, "#ffca28", "#1e88e5", "#ff7043", "#ab47bc"]
    d = "M" + "L".join(f"{x} {y}" for x, y in pts)
    parts = [P("M2 96V22Q50 14 98 22V96Z", GRASS),
             f'<path d="{d}" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="1 7"/>']
    for (x, y), c in reversed(list(zip(pts, cols))):
        s = 0.75 + 0.55 * (y - 28) / 58
        h = 20 * s
        parts.append(E(x, y, 4 * s, 1.6 * s, "#2e7d32", O, 1.5))
        parts.append(L(f"M{x} {y}V{y - h:.1f}", O, 2.5))
        parts.append(P(f"M{x} {y - h:.1f}L{x + 15 * s:.1f} {y - h + 5.5 * s:.1f}L{x} {y - h + 11 * s:.1f}Z", c, O, 2))
    return svg(*parts)


def add_more(K):
    K.add("N", "Netball", "Shoot it in the ring!", netball())
    K.add("N", "Noodle", "Float with a bendy noodle!", noodle())
    K.add("N", "Number bib", "Number one! Ready, go!", number_bib())
    K.add("O", "Olympic rings", "Five rings for the big games!", olympic_rings())
    K.add("O", "Obstacle course", "Over, under and through!", obstacle_course())
    K.add("O", "Olympic torch", "The flame shines bright!", torch())
    K.add("P", "Ping-pong", "Ping! Pong! Over the net!", ping_pong())
    K.add("P", "Pogo stick", "Boing, boing, boing!", pogo_stick())
    K.add("P", "Parachute", "Float down, slow and soft!", parachute())
    K.add("Q", "Quiver", "A bag full of arrows!", quiver())
    K.add("Q", "Quad bike", "Vroom! Four big wheels!", quad_bike())
    K.add("Q", "Quarter pipe", "Roll up the ramp! Whee!", quarter_pipe())
    K.add("R", "Rugby ball", "Run with the ball!", rugby_ball())
    K.add("R", "Roller skates", "Roll, roll, roll along!", roller_skate())
    K.add("R", "Relay baton", "Pass the baton, quick!", relay_baton())
    K.add("S", "Surfboard", "Ride the big wave!", surfboard())
    K.add("S", "Skis", "Swoosh down the snowy hill!", skis())
    K.add("S", "Stopwatch", "Click! How fast are you?", stopwatch())
    K.add("T", "Tennis ball", "A fuzzy ball! Bounce it!", tennis_ball())
    K.add("T", "Trampoline", "Jump up high! Boing!", trampoline())
    K.add("T", "Tricycle", "Pedal, pedal, three wheels!", tricycle())
    K.add("U", "Unicycle", "Just one wheel! Wobble!", unicycle())
    K.add("U", "Umpire chair", "Sit up high and watch!", umpire_chair())
    K.add("U", "Uneven bars", "Swing on the bars!", uneven_bars())
    K.add("V", "Visor", "Keep the sun away!", visor())
    K.add("V", "Vaulting horse", "Run, jump and fly over!", vaulting_horse())
    K.add("V", "Victory podium", "First, second, third! Hooray!", podium())
    K.add("W", "Water bottle", "Drink water! Glug, glug!", water_bottle())
    K.add("W", "Wetsuit", "Stay warm when you swim!", wetsuit())
    K.add("W", "Wheelchair racing", "Push fast to the finish!", racing_wheelchair())
    K.add("X", "X-country skis", "Glide along the snowy track!", xc_skis())
    K.add("X", "Xare", "Catch and throw the ball!", xare())
    K.add("Y", "Yacht", "Sail across the sea!", yacht())
    K.add("Y", "Yoga mat", "Stretch like a cat!", yoga_mat())
    K.add("Y", "Yellow card", "Yellow card! Play nicely!", yellow_card())
    K.add("Z", "Zorb ball", "Roll inside a giant ball!", zorb())
    K.add("Z", "Zumba", "Dance and move to music!", zumba())
    K.add("Z", "Zig-zag run", "Zig, zag, run around!", zigzag_run())
