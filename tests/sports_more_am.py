"""Extra Sports pictures A–M (4 per letter in total)."""
import math
from svgkit import *

WOOD = "#d7a86e"; WOODD = "#a1887f"; GOLD = "#ffc107"; RED = "#e53935"; BLUE = "#1e88e5"
GRASS = "#66bb6a"; WATER = "#4fc3f7"; WAVE = "#42a5f5"; GREY = "#b0bec5"; DARK = "#37474f"


def waves(y, c=WAVE, x0=4, x1=96):
    d = f"M{x0} {y}"
    x = x0
    while x < x1:
        d += f"Q{x + 5} {y - 5} {x + 10} {y}"
        x += 10
    return L(d, c, 3)


def ring(cx, cy, rx, ry, col, w=6, rot=None):
    return E(cx, cy, rx, ry, "none", O, w + 6, rot) + E(cx, cy, rx, ry, "none", col, w, rot)


def seam(p0, p1, p2, n=6, tick=3.0, col="#e53935"):
    """Quadratic seam with little stitch ticks across it."""
    d = f"M{p0[0]} {p0[1]}Q{p1[0]} {p1[1]} {p2[0]} {p2[1]}"
    ticks = ""
    for i in range(1, n):
        t = i / n
        x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
        dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
        m = math.hypot(dx, dy)
        nx, ny = -dy / m * tick, dx / m * tick
        ticks += f"M{x - nx:.1f} {y - ny:.1f}L{x + nx:.1f} {y + ny:.1f}"
    return L(d, col, 2) + L(ticks, col, 1.8)


def ell_arc(cx, cy, rx, ry, a0, a1, rot=0):
    r = math.radians(rot)
    def p(a):
        a = math.radians(a)
        x, y = rx * math.cos(a), ry * math.sin(a)
        return cx + x * math.cos(r) - y * math.sin(r), cy + x * math.sin(r) + y * math.cos(r)
    x0, y0 = p(a0); x1, y1 = p(a1)
    return f"M{x0:.1f} {y0:.1f}A{rx} {ry} {rot} 0 1 {x1:.1f} {y1:.1f}"


def add_more(K):
    # ================= A =================
    K.add("A", "American football", "Throw it, catch it!", svg(
        T("rotate(-28 50 50)",
          P("M6 50Q50 4 94 50Q50 96 6 50Z", "#a0522d"),
          L("M25 39Q21 50 25 61M75 39Q79 50 75 61", "#fff", 3.5),
          L("M32 38H68", "#fff", 3.5),
          L("M38 33V43M45 33V43M52 33V43M59 33V43", "#fff", 3),
          HL(30, 46, 3, 7, 60),
          face(50, 57, 0.85))))

    def armband(cx, y, f=True):
        w, h = 18, 42
        body = (f"M{cx - w} {y}Q{cx - w - 5} {y + h * 0.25} {cx - w} {y + h * 0.5}Q{cx - w - 5} {y + h * 0.75} {cx - w} {y + h}"
                f"Q{cx} {y + h + 12} {cx + w} {y + h}Q{cx + w + 5} {y + h * 0.75} {cx + w} {y + h * 0.5}"
                f"Q{cx + w + 5} {y + h * 0.25} {cx + w} {y}Z")
        return [
            P(body, "#ff9800"),
            L(f"M{cx - w + 1} {y + h * 0.5}Q{cx} {y + h * 0.5 + 11} {cx + w - 1} {y + h * 0.5}", "#e65100", 3),
            E(cx, y, w, 9, "#ffb74d"),
            E(cx, y, 11, 4.5, "#6d4c41", O, 2),
            R(cx + 8, y + 26, 6, 8, "#fff", 2, O, 2),
            HL(cx - 11, y + 16, 2, 5, 0), HL(cx - 11, y + 36, 2, 4, 0),
            face(cx - 3, y + 36, 0.7) if f else ""]
    K.add("A", "Arm floats", "They help you float!", svg(
        waves(94), waves(86, "#81d4fa", 14, 86),
        T("rotate(-10 27 50)", *armband(27, 28, False)),
        T("rotate(10 73 50)", *armband(73, 28))))

    K.add("A", "Award ribbon", "First place! Well done!", svg(
        P("M38 52L22 92L32 86L38 96L50 58Z", BLUE),
        P("M62 52L78 92L68 86L62 96L50 58Z", BLUE),
        P(star_path(50, 42, 35, inner=0.86, n=16), "#1565c0"),
        P(star_path(50, 42, 27, inner=0.88, n=14, rot=-80), "#64b5f6", O, 2.5),
        C(50, 42, 17, GOLD),
        HL(42, 34, 2.5, 5, 40), face(50, 42, 0.75)))

    # ================= B =================
    K.add("B", "Baseball", "Swing the bat! Hit it!", svg(
        T("rotate(40 50 50)",
          P("M47 86L47 62Q47 52 41 42L41 16Q41 6 50 6Q59 6 59 16L59 42Q53 52 53 62L53 86Z", "#e0a96d"),
          E(50, 89, 8, 3.5, "#c48a4e"),
          L("M47 70H53M47 76H53M47 82H53", "#8d6e63", 1.5),
          HL(45, 22, 2, 8, 0)),
        C(70, 72, 20, "#fff"),
        seam((58, 57), (66, 72), (58, 87)),
        seam((82, 57), (74, 72), (82, 87)),
        HL(62, 62, 2.5, 4, 40), face(70, 70, 0.6)))

    feather = ("M-12 12L-24 -30Q-18 -36 -12 -32Q-6 -38 0 -33Q6 -38 12 -32Q18 -36 24 -30L12 12Z")
    K.add("B", "Badminton", "Hit the birdie up high!", svg(T("translate(50 52) scale(0.86) translate(-50 -50)",
        T("rotate(22 76 50)",
          TL("M76 52V92", "#90a4ae", 3),
          R(72, 76, 8, 18, "#5c6bc0", 3, O, 2.5),
          E(76, 30, 13, 18, "#f1f8e9"),
          L("M70 16V44M76 12V48M82 16V44M64 24H88M63 32H89M64 40H88", "#aaa", 1),
          E(76, 30, 13, 18, "none", O, 7), E(76, 30, 13, 18, "none", "#ec407a", 3)),
        T("translate(36 50) rotate(-24)",
          P(feather, "#fff"),
          L("M-8 10L-15 -30M0 12V-32M8 10L15 -30", "#cfd8dc", 1.8),
          L("M-18 -12H18", "#90caf9", 3),
          P("M-13 12Q-13 34 0 34Q13 34 13 12Z", "#ffb74d"),
          R(-14, 9, 28, 6, "#e53935", 2, O, 2.5),
          HL(-14, -18, 2.5, 6, 20), face(0, 23, 0.6)))))

    def wheel(x, y):
        sp = "".join(f"M{x}{y:+}" for _ in [])
        spokes = ""
        for k in range(6):
            a = math.radians(30 * k)
            spokes += f"M{x - 12 * math.cos(a):.1f} {y - 12 * math.sin(a):.1f}L{x + 12 * math.cos(a):.1f} {y + 12 * math.sin(a):.1f}"
        return C(x, y, 18, DARK) + C(x, y, 12, "#e1f5fe", O, 2) + L(spokes, "#90a4ae", 1.2) + C(x, y, 3, GREY, O, 2)
    K.add("B", "Bicycle", "Pedal, pedal, off we go!", svg(
        wheel(22, 70), wheel(78, 70),
        TL("M22 70L44 40L48 70Z M48 70L72 38M44 40H72M72 38L78 70", RED, 4),
        TL("M44 40L42 30M72 38L70 26", "#90a4ae", 3),
        P("M32 28Q32 24 40 24H50Q54 26 50 30H36Q32 30 32 28Z", DARK, O, 2.5),
        TL("M64 24Q70 20 80 24", "#90a4ae", 3), R(78, 20, 10, 7, DARK, 3, O, 2),
        C(48, 70, 6, GOLD, O, 2.5),
        HL(14, 60, 1.5, 4, 40)))

    # ================= C =================
    K.add("C", "Canoe", "Paddle down the river!", svg(
        waves(90), waves(80, "#81d4fa", 10, 90),
        P("M6 38Q12 48 24 52Q50 58 76 52Q88 48 94 38Q92 62 78 70Q50 80 22 70Q8 62 6 38Z", "#43a047"),
        P("M6 38Q12 48 24 52Q50 58 76 52Q88 48 94 38Q86 54 76 56Q50 62 24 56Q14 54 6 38Z", "#ffd54f", O, 2.5),
        TL("M66 8L50 70", WOOD, 4),
        P("M44 60L56 64L52 86Q48 92 44 88Z", WOOD),
        TL("M60 8H72", WOOD, 4),
        HL(16, 56, 2.5, 5, 40), face(32, 64, 0.8)))

    def cone(cx, top, bot, ht, hb, s):
        def xl(y): return cx - ht - (hb - ht) * (y - top) / (bot - top)
        def xr(y): return cx + ht + (hb - ht) * (y - top) / (bot - top)
        h = bot - top
        y1, y2 = top + 0.32 * h, top + 0.52 * h
        return [
            R(cx - hb - 6, bot, 2 * hb + 12, 9, "#ef6c00", 3),
            P(f"M{cx - ht} {top}Q{cx} {top - 5} {cx + ht} {top}L{cx + hb} {bot}H{cx - hb}Z", "#ff9800"),
            P(f"M{xl(y1):.1f} {y1:.1f}H{xr(y1):.1f}L{xr(y2):.1f} {y2:.1f}H{xl(y2):.1f}Z", "#fff", O, 2.5),
            HL(cx - ht - 2, top + 0.18 * h, 1.8, 0.1 * h, 15),
            face(cx, top + 0.72 * h, s) if s else ""]
    K.add("C", "Cones", "Run around the cones!", svg(
        *cone(24, 38, 84, 3, 14, 0),
        *cone(62, 10, 82, 4, 22, 0.85)))

    holds = [(28, 20, 7, RED), (56, 26, 6, "#43a047"), (24, 62, 6, "#ab47bc"), (56, 70, 7, "#1e88e5"), (34, 84, 6, "#ff9800")]
    hp = []
    for x, y, r, c in holds:
        hp.append(P(f"M{x - r} {y}Q{x - r} {y - r} {x} {y - r * 0.9}Q{x + r * 1.2} {y - r * 0.6} {x + r} {y + r * 0.3}Q{x + r * 0.4} {y + r} {x - r * 0.5} {y + r * 0.8}Q{x - r * 1.1} {y + r * 0.5} {x - r} {y}Z", c, O, 2.5))
        hp.append(dot(x, y, 1.4, O))
    K.add("C", "Climbing wall", "Climb up, up, up!", svg(
        R(8, 6, 66, 90, "#b3e5fc", 5),
        L("M8 36H74M8 66H74M30 6V96M52 6V96", "#81d4fa", 1.5),
        *hp,
        P("M30 46Q30 34 42 34Q56 34 54 46Q52 58 40 58Q30 58 30 46Z", GOLD),
        face(42, 45, 0.7),
        C(70, 12, 5, "#90a4ae", O, 2.5),
        TL("M70 17Q86 20 84 50Q82 76 90 94", "#ef5350", 3),
        HL(14, 16, 2, 6, 0)))

    # ================= D =================
    db = [C(44, 54, 40, "#263238")]
    n = 16
    for k in range(n):
        a0 = -90 - 360 / n / 2 + 360 / n * k; a1 = a0 + 360 / n
        db.append(P(annulus_sector(44, 54, 0.1, 30, a0, a1), "#263238" if k % 2 else "#fff3d6", O, 1.2))
        db.append(P(annulus_sector(44, 54, 26, 31, a0, a1), RED if k % 2 else "#43a047", O, 1.2))
        db.append(P(annulus_sector(44, 54, 15, 18, a0, a1), RED if k % 2 else "#43a047", O, 1.2))
    db += [C(44, 54, 10, "#43a047", O, 2), C(44, 54, 4, RED, O, 1.5), C(44, 54, 40, "none")]
    K.add("D", "Dartboard", "Throw the dart! Bullseye!", svg(
        *db,
        T("translate(-7 12) rotate(-40 66 34)",
          L("M60 34H66", "#90a4ae", 2.5),
          R(66, 30, 14, 8, "#eceff1", 3, O, 2.5),
          L("M80 34H86", O, 2.5),
          P("M84 34L92 24H98L94 34L98 44H92Z", "#ec407a", O, 2.5)),
        HL(20, 34, 3, 7, 40)))

    K.add("D", "Diving board", "Jump! Splash in the pool!", svg(
        R(4, 62, 92, 34, WATER, 4),
        waves(72, "#e1f5fe", 34, 94), waves(84, "#e1f5fe", 10, 70),
        R(6, 40, 20, 28, "#cfd8dc", 3),
        P("M6 30H76Q86 30 88 36L88 40H6Z", "#1e88e5"),
        L("M8 34H74", "#90caf9", 2),
        L("M10 18V40M20 18V40M10 24H20M10 32H20", "#90a4ae", 3),
        C(70, 56, 3, "#e1f5fe", O, 2), C(80, 52, 2.5, "#e1f5fe", O, 2), C(88, 58, 2, "#e1f5fe", O, 2),
        face(16, 52, 0.6)))

    K.add("D", "Discus", "Spin and throw it far!", svg(
        L("M2 40H14M4 52H14M2 64H14", "#90a4ae", 3),
        T("rotate(-18 54 52)",
          E(54, 58, 38, 30, "#78909c"),
          E(54, 52, 38, 30, "#cfd8dc"),
          E(54, 52, 27, 21, "#263238", O, 2.5),
          E(54, 52, 13, 10, GOLD, O, 2.5),
          HL(32, 38, 3, 7, 40)),
        face(54, 51, 0.6)))

    # ================= E =================
    K.add("E", "Exercise ball", "Bounce and stretch!", svg(
        R(8, 82, 84, 10, "#4db6ac", 4),
        E(50, 48, 40, 38, "#ab47bc"),
        L("M16 30Q50 46 84 30", "#ce93d8", 2.5), L("M12 58Q50 74 88 58", "#ce93d8", 2.5),
        C(84, 44, 2.5, "#fff", O, 1.5),
        HL(28, 26, 4, 10, 40), face(50, 46), blush(50, 52, 14, 3)))

    def pad(f):
        return [
            P("M-18 -36Q0 -42 18 -36L14 36Q0 40 -14 36Z", "#29b6f6"),
            R(-19, -28, 38, 9, "#263238", 3, O, 2.5), R(-16, 22, 32, 9, "#263238", 3, O, 2.5),
            P("M0 -18Q14 -18 14 0Q14 18 0 18Q-14 18 -14 0Q-14 -18 0 -18Z", "#455a64"),
            L("M-11 -9H11M-12 9H12", "#78909c", 2),
            HL(-8, -10, 1.8, 4, 20),
            face(0, -1, 0.6, "#fff") if f else ""]
    K.add("E", "Elbow pads", "Safe and ready to skate!", svg(
        T("translate(28 50) rotate(-8)", *pad(False)),
        T("translate(72 50) rotate(8)", *pad(True))))

    def pole(y, x0=14, x1=86):
        s = [R(x0, y - 4, x1 - x0, 8, "#fff", 4)]
        for x in range(x0 + 6, x1 - 6, 14):
            s.append(F(f"M{x} {y - 2.5}h7v5h-7Z", RED))
        s.append(R(x0, y - 4, x1 - x0, 8, "none", 4))
        return s
    K.add("E", "Equestrian jump", "Jump over, horsey!", svg(
        E(50, 90, 48, 8, GRASS),
        R(8, 18, 12, 72, "#fff", 3), R(80, 18, 12, 72, "#fff", 3),
        P("M6 18L14 8L22 18Z M78 18L86 8L94 18Z", "#1e88e5", O, 2.5),
        *pole(36), *pole(56),
        P("M38 92L34 72Q32 60 50 60Q68 60 66 72L62 92H52L56 74Q58 68 50 68Q42 68 44 74L48 92Z", GOLD),
        dot(38, 80, 1.5, O), dot(36, 70, 1.5, O), dot(62, 80, 1.5, O), dot(64, 70, 1.5, O),
        face(50, 86, 0.55)))

    # ================= F =================
    K.add("F", "Frisbee", "Fly, frisbee, fly! Catch it!", svg(
        L("M2 46H16M4 58H14M2 70H16", "#90a4ae", 3),
        T("rotate(-12 54 54)",
          E(56, 60, 40, 20, "#c2185b"),
          E(56, 52, 40, 20, "#ff4081"),
          E(56, 52, 28, 13, "none", "#f8bbd0", 3),
          HL(36, 44, 3, 6, 70)),
        face(56, 52, 0.75)))

    def flipper(col, dark, f):
        return [
            P("M-12 30Q-15 10 -14 0L-26 -38Q0 -50 26 -38L14 0Q15 10 12 30Q0 38 -12 30Z", col),
            L("M-8 -4L-14 -36M0 -4V-40M8 -4L14 -36", dark, 2.5),
            P("M-12 30Q-15 10 -14 0H14Q15 10 12 30Q0 38 -12 30Z", dark),
            E(0, 6, 8, 4, "#263238", O, 2),
            HL(-16, -26, 2, 6, 15),
            face(0, 20, 0.6, "#fff") if f else ""]
    K.add("F", "Flippers", "Kick, kick, swim fast!", svg(
        T("translate(30 58) rotate(-12) scale(0.8)", *flipper("#29b6f6", "#0277bd", False)),
        T("translate(70 58) rotate(12) scale(0.8)", *flipper("#ffca28", "#f57f17", True))))

    chk = [R(16, 14, 68, 22, "#fff", 2)]
    for r in range(2):
        for c in range(8):
            if (r + c) % 2 == 0:
                chk.append(F(f"M{16 + c * 8.5:.1f} {14 + r * 11}h8.5v11h-8.5Z", "#263238"))
    chk.append(R(16, 14, 68, 22, "none", 2))
    K.add("F", "Finish line", "You made it! Hooray!", svg(
        E(50, 92, 48, 6, "#ef8a65"),
        TL("M12 8V92", "#fff", 5), TL("M88 8V92", "#fff", 5),
        L("M12 30V40M12 56V66M12 80V88M88 30V40M88 56V66M88 80V88", RED, 5),
        *chk,
        TL("M12 62Q50 72 88 62", RED, 3),
        C(12, 8, 5, GOLD, O, 2.5), C(88, 8, 5, GOLD, O, 2.5),
        P(star_path(50, 58, 15), GOLD, O, 2.5), face(50, 60, 0.5)))

    # ================= G =================
    net = ""
    for x in range(22, 86, 8):
        net += f"M{x} 18V86"
    for y in range(26, 88, 8):
        net += f"M12 {y}H88"
    K.add("G", "Goal", "Score! Into the goal!", svg(
        E(50, 90, 48, 7, GRASS),
        F("M12 18H88V86H12Z", "#f1f8e9"),
        L(net, "#b0bec5", 1.6),
        TL("M12 88V16H88V88", "#fff", 5),
        C(54, 68, 16, "#fff"),
        P(star_path(54, 68, 7, inner=0.81, n=5), "#263238", O, 1.5),
        P("M40 60L45 58L46 63L42 66Z M68 60L63 58L62 63L66 66Z M48 82L52 79L56 79L60 82Z", "#263238", O, 1.5),
        C(54, 68, 16, "none"),
        HL(44, 60, 2, 4, 40), face(54, 69, 0.55, "#fff")))

    K.add("G", "Goggles", "See under the water!", svg(
        TL("M8 54Q8 30 50 30Q92 30 92 54", "#26a69a", 6),
        R(4, 46, 10, 16, "#26a69a", 4), R(86, 46, 10, 16, "#26a69a", 4),
        TL("M42 54Q50 46 58 54", "#ec407a", 4),
        E(29, 56, 17, 15, "#ec407a"), E(71, 56, 17, 15, "#ec407a"),
        E(29, 56, 12, 10, "#81d4fa", O, 2.5), E(71, 56, 12, 10, "#81d4fa", O, 2.5),
        HL(24, 51, 2, 4, 40), HL(66, 51, 2, 4, 40),
        dot(31, 57, 3.2, O), dot(69, 57, 3.2, O),
        L("M44 76Q50 81 56 76", O, 2.4)))

    K.add("G", "Gymnastics rings", "Hold on and swing!", svg(
        TL("M8 10H92", WOOD, 6),
        TL("M30 12L32 54M70 12L68 54", RED, 4),
        R(27, 50, 10, 10, GREY, 2, O, 2), R(63, 50, 10, 10, GREY, 2, O, 2),
        ring(32, 74, 15, 15, WOOD, 7), ring(68, 74, 15, 15, WOOD, 7),
        HL(22, 66, 1.5, 4, 40), HL(58, 66, 1.5, 4, 40)))

    # ================= H =================
    K.add("H", "Hockey stick", "Hit the ball to the goal!", svg(
        E(50, 90, 48, 7, GRASS),
        TL("M82 11L40 74Q34 86 22 84Q12 82 16 72", "#1e88e5", 7),
        TL("M82 11L71 27", "#263238", 7),
        L("M79 15L76 20M75 21L72.5 25", "#90a4ae", 1.5),
        C(68, 74, 14, "#ffca28"),
        dot(62, 70, 1.4, "#f9a825"), dot(74, 70, 1.4, "#f9a825"), dot(68, 82, 1.4, "#f9a825"),
        HL(62, 67, 2, 4, 40), face(68, 74, 0.6)))

    cols = ["#e53935", "#ffca28", "#43a047", "#1e88e5", "#ab47bc", "#ff9800"]
    hh = [L("M2 30Q8 22 14 28M86 74Q92 82 98 76", "#90a4ae", 2.5),
          f'<ellipse cx="50" cy="52" rx="42" ry="24" fill="none" stroke="{O}" stroke-width="14" transform="rotate(-14 50 52)"/>']
    for k in range(12):
        a0 = 30 * k; a1 = a0 + 30
        hh.append(f'<path d="{ell_arc(50, 52, 42, 24, a0, a1 + 0.5, -14)}" fill="none" stroke="{cols[k % 6]}" stroke-width="8"/>')
    hh.append(HL(22, 40, 1.5, 4, 40))
    K.add("H", "Hula hoop", "Wiggle, wiggle, spin!", svg(*hh))

    K.add("H", "Hurdle", "Run and jump over!", svg(
        P("M0 80H100V96H0Z", "#ef8a65", O, 0),
        L("M0 88H100", "#fff", 2.5),
        TL("M18 40V84M82 40V84", "#cfd8dc", 4),
        TL("M8 86H28M72 86H92", "#cfd8dc", 4),
        R(8, 20, 84, 22, "#fff", 4),
        F("M10 22H26V40H10Z M74 22H90V40H74Z", "#263238"),
        R(8, 20, 84, 22, "none", 4),
        HL(32, 26, 1.5, 4, 70), face(50, 29, 0.7)))

    # ================= I =================
    K.add("I", "Ice hockey", "Whoosh! Slide the puck!", svg(
        E(50, 84, 48, 13, "#e1f5fe"),
        L("M18 82H34M60 90H80", "#b3e5fc", 2.5),
        TL("M82 11L46 76", "#8d6e63", 6),
        TL("M82 11L74.5 24.5", "#263238", 6),
        P("M50 70L18 76Q10 78 12 84Q14 88 22 88L50 84Q54 78 50 70Z", "#8d6e63"),
        L("M26 78L28 86M32 77L34 85M38 76L40 84", "#263238", 2.5),
        P("M50 66V78A18 7 0 0 0 86 78V66Z", "#263238"),
        E(68, 66, 18, 7, "#455a64"),
        HL(60, 64, 1.5, 4, 80), face(68, 73, 0.5, "#fff")))

    K.add("I", "Inline skates", "Roll, roll, roll along!", svg(
        R(14, 72, 78, 8, GREY, 3),
        C(24, 86, 8, "#ffca28"), C(42, 86, 8, "#ffca28"), C(60, 86, 8, "#ffca28"), C(78, 86, 8, "#ffca28"),
        dot(24, 86, 2.5, O), dot(42, 86, 2.5, O), dot(60, 86, 2.5, O), dot(78, 86, 2.5, O),
        P("M24 8H56L58 44Q84 46 90 62V72H18Q16 40 24 8Z", "#26c6da"),
        P("M24 8H56V16H24Z", "#7e57c2", O, 2.5),
        R(20, 26, 40, 7, "#7e57c2", 3, O, 2.5),
        R(56, 50, 10, 16, "#7e57c2", 3, O, 2.5, rot=-30),
        P("M18 66H90V72H18Z", "#7e57c2", O, 2.5),
        HL(29, 40, 2.5, 7, 0), face(38, 52, 0.8)))

    K.add("I", "Inner tube", "Slide down the snowy hill!", svg(
        dot(16, 12, 2, "#90caf9"), dot(84, 10, 2, "#90caf9"), dot(60, 6, 1.5, "#90caf9"), dot(34, 20, 1.5, "#90caf9"),
        P("M0 56Q30 44 60 50Q82 54 100 46V100H0Z", "#e3f2fd", "#90caf9", 2.5),
        L("M6 90Q20 86 30 90M70 92Q82 88 94 92", "#90caf9", 2.5),
        E(50, 60, 40, 23, "#455a64"),
        E(50, 54, 15, 6, "#cfd8dc", O, 2.5),
        TL("M16 48Q12 36 24 34", GOLD, 4), TL("M84 48Q88 36 76 34", GOLD, 4),
        L("M22 46Q50 34 78 46", "#78909c", 2.5),
        HL(22, 54, 2.5, 6, 60), face(50, 72, 0.75, "#fff")))

    # ================= J =================
    K.add("J", "Javelin", "Throw it really far!", svg(
        L("M14 50L26 62M20 40L32 52M6 62L18 74", "#90a4ae", 2.5),
        TL("M10 90L80 20", "#ffca28", 4),
        P("M80 20L76 16L94 6L84 24Z", "#cfd8dc"),
        TL("M38 62L52 48", "#e53935", 9),
        L("M41 59L49 51", "#fff", 1),
        HL(30, 66, 1.5, 4, 45)))

    K.add("J", "Jet ski", "Zoom across the water!", svg(
        L("M2 54Q4 46 10 48M4 64Q0 58 6 56", "#90caf9", 2.5),
        TL("M58 44L52 24", "#90a4ae", 3),
        TL("M44 24H62", DARK, 3),
        P("M6 62H96Q92 76 76 80H18Q6 78 6 62Z", "#fff"),
        P("M6 62V54Q6 48 12 48H40L50 40H70L94 58L96 62Z", RED),
        P("M10 48Q10 40 18 40H40Q46 40 44 44L40 48Z", DARK),
        P("M62 40L72 30L76 32L72 44Z", "#81d4fa", O, 2.5),
        waves(86), waves(94, "#81d4fa", 14, 86),
        HL(20, 54, 1.5, 4, 70), face(48, 70, 0.7)))

    K.add("J", "Jockey cap", "Giddy up, horsey!", svg(
        P("M14 66Q14 18 50 18Q86 18 86 66Z", GOLD),
        P("M50 18Q30 22 31 66H50Z", "#7e57c2", O, 2.5),
        P("M50 18Q70 22 69 66H86Q86 18 50 18Z", "#7e57c2", O, 2.5),
        P("M14 66Q14 18 50 18Q86 18 86 66Z", "none"),
        P("M12 62Q50 54 88 62Q92 78 50 80Q8 78 12 62Z", "#5e35b1"),
        C(50, 15, 7, "#ec407a"),
        HL(22, 40, 3, 8, 20), face(41, 44, 0.7)))

    # ================= K =================
    K.add("K", "Kayak", "Paddle left, paddle right!", svg(
        waves(90), waves(80, "#81d4fa", 14, 86),
        TL("M12 26L88 44", "#455a64", 3),
        E(13, 26, 9, 5, RED, rot=13), E(87, 44, 9, 5, RED, rot=13),
        P("M4 58Q50 36 96 58Q50 82 4 58Z", "#ffca28"),
        L("M8 58Q50 52 92 58", "#f57f17", 2.5),
        E(56, 48, 13, 4.5, "#263238", O, 2.5),
        HL(20, 54, 1.5, 4, 70), face(32, 62, 0.7)))

    K.add("K", "Karate belt", "Hi-yah! Kick and chop!", svg(
        R(4, 36, 92, 16, "#263238", 6),
        L("M8 44H92", "#455a64", 1.5),
        P("M44 46L28 88L40 92L52 52Z", "#263238"),
        P("M56 46L72 88L60 92L48 52Z", "#263238"),
        L("M31 80L42 84M69 80L58 84", "#ffc107", 3),
        R(38, 30, 24, 26, "#37474f", 7),
        L("M44 32Q50 44 44 54", "#546e7a", 2),
        HL(10, 40, 1.5, 4, 80), face(50, 41, 0.6, "#fff")))

    K.add("K", "Kickboard", "Hold on and kick!", svg(
        T("rotate(-8 50 50)",
          P("M18 34Q18 8 50 8Q82 8 82 34V82Q82 90 74 90H26Q18 90 18 82Z", "#29b6f6"),
          P("M18 58H82V70H18Z", "#ffeb3b", O, 2.5),
          E(32, 22, 6, 4, "#fff", O, 2.5), E(68, 22, 6, 4, "#fff", O, 2.5),
          HL(26, 38, 2.5, 7, 0), face(50, 42, 0.85)),
        F("M0 80Q25 72 50 80T100 80V100H0Z", "#4fc3f7", ".8"),
        waves(80, WAVE, 0, 100)))

    # ================= L =================
    mesh = "M62 14L80 34M58 22L76 40M68 10L86 28M60 38L78 14M58 30L72 12M66 42L84 22"
    K.add("L", "Lacrosse stick", "Catch it in the net!", svg(
        TL("M12 92L58 44", "#90a4ae", 4),
        TL("M12 92L22 82", "#263238", 4),
        P("M56 46Q50 20 64 10Q80 2 92 14Q96 30 74 44Q64 50 56 46Z", "#f1f8e9", O, 0.1),
        L(mesh, "#90a4ae", 1.4),
        TL("M56 46Q50 20 64 10Q80 2 92 14Q96 30 74 44Q64 50 56 46Z", "none", 4),
        L("M56 46Q50 20 64 10Q80 2 92 14Q96 30 74 44Q64 50 56 46Z", "#1e88e5", 4),
        C(72, 28, 10, "#ff7043"),
        HL(68, 24, 1.5, 3, 40), face(72, 28, 0.5)))

    def foot(x, y, rot):
        return T(f"rotate({rot} {x} {y})", E(x, y, 3, 5, "#d4a64a", "#c49a3a", 0.1),
                 dot(x - 2, y - 6.5, 1.1, "#d4a64a"), dot(x, y - 7.2, 1.1, "#d4a64a"), dot(x + 2, y - 6.5, 1.1, "#d4a64a"))
    K.add("L", "Long jump", "Run, jump, land in the sand!", svg(
        P("M20 66H80L94 96H6Z", "#ef8a65"),
        L("M38 72L34 96M62 72L66 96", "#fff", 2.5),
        P("M14 10H86L96 62H4Z", "#8d6e63"),
        P("M18 14H82L90 58H10Z", "#ffe082", O, 2.5),
        P("M14 64H86V72H14Z", "#fff"),
        foot(44, 34, -5), foot(54, 34, 5), foot(26, 24, -5), foot(72, 22, 5),
        HL(20, 44, 2, 5, 20), face(50, 46, 0.75)))

    K.add("L", "Leotard", "Twirl and tumble!", svg(
        P("M30 10Q50 26 70 10L86 20L94 54L82 58L74 34L72 58Q60 68 56 92H44Q40 68 28 58L26 34L18 58L6 54L14 20Z", "#ec407a"),
        L("M14 20L20 22M86 20L80 22", "#f8bbd0", 3),
        L("M30 10Q50 26 70 10", "#f8bbd0", 3),
        P(star_path(38, 70, 4), "#fff", O, 1.5), P(star_path(62, 70, 4), "#fff", O, 1.5),
        P(star_path(50, 80, 3.5), "#fff", O, 1.5),
        HL(36, 30, 2.5, 6, 10), face(50, 42, 0.8), blush(50, 48, 12, 2.5)))

    # ================= M =================
    glove = ("M26 52V24Q26 14 34 14Q42 14 42 24V20Q42 8 50 8Q58 8 58 20V22Q58 12 66 12Q74 12 74 24V30"
             "Q74 22 81 22Q88 22 88 30V62Q88 92 56 92Q30 92 26 70Z")
    K.add("M", "Mitt", "Catch the ball in your mitt!", svg(
        P("M30 64Q8 58 8 40Q10 30 18 34L32 50Z", "#c47a3a"),
        P(glove, "#d68b45"),
        L("M42 24V52M58 22V52M74 30V54", "#a0612e", 2.5),
        L("M18 40L28 44M14 46L26 50", "#8d4b20", 2),
        L("M30 16L38 16M46 10L54 10M62 14L70 14M78 24L86 24", "#8d4b20", 2),
        R(30, 82, 50, 10, "#a0612e", 4),
        HL(34, 30, 2, 6, 0), face(57, 66, 0.85), blush(57, 72, 13, 2.5)))

    rungs = ["#e53935", "#ff9800", "#ffca28", "#43a047", "#1e88e5", "#ab47bc"]
    mb = [E(50, 92, 48, 6, GRASS),
          TL("M24 12V82M76 12V82", "#78909c", 4)]
    for i, c in enumerate(rungs):
        t = (i + 1) / 7
        xb = 24 + 52 * t; xf = 10 + 80 * t
        mb.append(TL(f"M{xb:.1f} 12L{xf:.1f} 42", c, 5))
    mb += [TL("M22 12H78", "#90a4ae", 4),
           TL("M10 42V90M90 42V90", "#90a4ae", 5),
           TL("M10 56H24M10 70H24M90 56H76M90 70H76", "#90a4ae", 3),
           TL("M8 42H92", "#90a4ae", 5)]
    K.add("M", "Monkey bars", "Swing across like a monkey!", svg(*mb))

    K.add("M", "Medicine ball", "Heavy! Lift it with two hands!", svg(
        E(50, 92, 34, 5, "#cfd8dc", "#cfd8dc", 0.1),
        C(50, 52, 38, "#5d4037"),
        P("M13 44Q50 66 87 44L88 58Q50 80 12 58Z", "#ffb300", O, 2.5),
        L("M50 14Q30 34 32 58M50 14Q70 34 68 58", "#3e2723", 2),
        L("M32 72Q34 82 42 88M68 72Q66 82 58 88", "#3e2723", 2),
        HL(30, 32, 3, 7, 40), face(50, 38, 0.8, "#fff")))
