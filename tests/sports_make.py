"""Sports world: sports things A-Z as hand-made SVG.  Writes tests/sports.js.

Run:  python tests/sports_make.py   then   python tests/pack_sheet.py tests/sports.js sports_sheet.png
"""
import math
import os
from svgkit import *

K = Pack()
WOOD = "#d7a86e"; WOODD = "#a1887f"; GOLD = "#ffc107"; RED = "#e53935"; BLUE = "#1e88e5"; GRASS = "#66bb6a"

# A: archery target with an arrow
K.add("A", "Archery", "Aim for the middle!", svg(
    L("M30 80L20 96M62 80L72 96", WOODD, 5),
    C(46, 50, 36, "#fff"), C(46, 50, 27, RED, O, 2.5), C(46, 50, 18, "#fff", O, 2.5), C(46, 50, 10, GOLD, O, 2.5),
    TL("M60 36L86 10", WOOD, 4),
    P("M80 10L86 4L94 4L88 12Z M86 16L92 10L92 18L84 20Z", RED, O, 2),
    HL(28, 34, 4, 8, 40), face(46, 49, 0.75)))

# B: basketball
K.add("B", "Basketball", "Bounce, bounce, bounce!", svg(
    C(50, 52, 38, "#f57c20"),
    L("M12 52L88 52M50 14L50 90M22 26Q38 52 22 78M78 26Q62 52 78 78", O, 2.5),
    C(50, 52, 38, "none"),
    HL(30, 34, 4, 8, 40), face(36, 40, 0.85)))

# C: cricket bat and ball
K.add("C", "Cricket", "Hit it for six!", svg(
    T("rotate(32 46 48)",
      R(42, 2, 8, 30, "#37474f", 3),
      L("M42 10H50M42 18H50M42 26H50", "#90a4ae", 2),
      P("M33 32H59V82Q59 92 46 92Q33 92 33 82Z", "#f2d39b"),
      L("M46 40V84", "#d9b97a", 2),
      HL(38, 52, 2.5, 9, 0), face(46, 62, 0.85)),
    C(78, 78, 13, "#d32f2f"),
    L("M68 70Q78 78 88 86", "#fff", 2), L("M70 67Q80 75 90 82", "#fff", 1.5),
    HL(73, 72, 2.5, 4, 40)))

# D: dumbbell
K.add("D", "Dumbbell", "Lift it up! So strong!", svg(
    R(30, 44, 40, 20, "#ffb300", 6),
    R(8, 26, 14, 56, "#455a64", 5), R(20, 32, 12, 44, "#607d8b", 4),
    R(78, 26, 14, 56, "#455a64", 5), R(68, 32, 12, 44, "#607d8b", 4),
    HL(12, 40, 2, 7, 0), HL(82, 40, 2, 7, 0),
    face(50, 52, 0.75)))

# E: egg and spoon race
K.add("E", "Egg and spoon", "Walk slowly. Don't drop it!", svg(
    TL("M52 62L90 92", "#b0bec5", 7),
    E(38, 60, 28, 13, "#cfd8dc"),
    E(38, 40, 18, 23, "#fffaf0"),
    HL(30, 30, 3, 7, 20), face(38, 42, 0.85), blush(38, 49, 9, 2.5)))

# F: football (soccer ball)
pent = lambda x, y, r, rot=-90: star_path(x, y, r, inner=math.cos(math.pi / 5), n=5, rot=rot)
f_parts = [C(50, 52, 38, "#fff")]
for k in range(5):
    a = math.radians(-90 + 72 * k)
    x, y = 50 + 29 * math.cos(a), 52 + 29 * math.sin(a)
    x2, y2 = 50 + 15 * math.cos(a), 52 + 15 * math.sin(a)
    f_parts.append(L(f"M{x2:.1f} {y2:.1f}L{x:.1f} {y:.1f}", O, 2))
    f_parts.append(P(pent(x, y, 8, -90 + 72 * k + 180), "#263238", O, 2))
f_parts += [P(pent(50, 52, 15), "#263238", O, 2), HL(30, 32, 4, 8, 40), face(50, 52, 0.75, "#fff")]
K.add("F", "Football", "Kick it into the goal!", svg(*f_parts))

# G: golf ball, hole and flag
K.add("G", "Golf", "Putt it in the hole!", svg(
    E(52, 82, 44, 12, GRASS),
    E(70, 82, 9, 3.5, "#2e5d32", O, 2),
    L("M70 82V12", "#eceff1", 4), L("M70 82V12", O, 1),
    P("M70 12L94 20L70 30Z", RED),
    C(32, 62, 16, "#fff"),
    dot(24, 56, 1.4, "#cfd8dc"), dot(40, 56, 1.4, "#cfd8dc"), dot(26, 70, 1.4, "#cfd8dc"), dot(38, 70, 1.4, "#cfd8dc"), dot(32, 52, 1.4, "#cfd8dc"),
    HL(25, 54, 2.5, 5, 40), face(32, 62, 0.8)))

# H: bike helmet
K.add("H", "Helmet", "Keep your head safe!", svg(
    L("M22 70Q30 92 50 92Q70 92 78 70", O, 3),
    R(44, 88, 12, 7, "#37474f", 2, O, 2),
    P("M12 66Q12 20 50 18Q88 20 88 66Z", "#42a5f5"),
    L("M34 30L38 42M50 24V38M66 30L62 42", "#1565c0", 5),
    P("M8 66H92Q94 74 86 74H14Q6 74 8 66Z", "#1565c0"),
    HL(26, 40, 4, 9, 30), face(50, 52, 0.9)))

# I: ice skate
K.add("I", "Ice skate", "Glide on the ice!", svg(
    L("M30 76V84M78 76V84", O, 4),
    P("M18 84H86Q94 84 92 90Q90 94 84 94H18Z", "#b0bec5"),
    P("M28 12H58L58 50Q82 52 88 64V76H24Q22 46 28 12Z", "#f5f5f5"),
    P("M28 12H58V18H28Z", "#ec407a", O, 2.5),
    L("M50 24L58 30M58 24L50 30M50 36L58 42M58 36L50 42", "#ec407a", 2.5),
    P("M24 70H88V76H24Z", "#ec407a", O, 2.5),
    HL(32, 30, 2.5, 8, 0), face(40, 56, 0.85)))

# J: jump rope with two handles
K.add("J", "Jump rope", "Jump, jump, jump!", svg(
    TL("M22 42Q14 98 50 94Q86 98 78 42", "#e53935", 2.5),
    T("rotate(-20 20 26)", R(12, 6, 16, 38, "#ffca28", 8), HL(16, 16, 2, 5, 0), face(20, 22, 0.55)),
    T("rotate(20 80 26)", R(72, 6, 16, 38, "#29b6f6", 8), HL(76, 16, 2, 5, 0), face(80, 22, 0.55))))

# K: kite
K.add("K", "Kite", "Fly high in the sky!", svg(
    L("M50 78Q36 86 46 92Q56 98 48 100", O, 2),
    P("M38 84L44 90L36 92Z M50 92L56 98L48 99Z", "#ab47bc", O, 1.5),
    P("M50 6L82 40L50 78L18 40Z", "#ff7043"),
    F("M50 9L21 40L50 40Z", "#ffca28"), F("M50 40L79 40L50 75Z", "#ffca28"),
    L("M50 6L82 40L50 78L18 40Z"),
    HL(38, 28, 3, 7, 40), face(50, 42, 0.9)))

# L: life ring
ring = [C(50, 50, 38, "#fff")]
for a0 in (0, 90, 180, 270):
    ring.append(P(annulus_sector(50, 50, 20, 38, a0 + 22.5, a0 + 67.5), RED, O, 2.5))
ring += [C(50, 50, 20, "#bbdefb"), C(50, 50, 38, "none"),
         HL(24, 30, 3, 7, 40), face(50, 79, 0.75)]
K.add("L", "Life ring", "It helps you float in the pool!", svg(*ring))

# M: medal
K.add("M", "Medal", "You are a winner!", svg(
    P("M28 4H44L58 46L46 50Z", BLUE), P("M72 4H56L42 46L54 50Z", RED),
    C(50, 66, 26, GOLD),
    C(50, 66, 19, "#ffd54f", O, 2),
    HL(36, 56, 3, 7, 40),
    face(50, 66, 0.85)))

# N: basketball net (hoop)
net = "M28 54L36 88M38 56L42 88M50 56V88M62 56L58 88M72 54L64 88M30 64H70M33 76H67"
K.add("N", "Net", "Swish! Into the net!", svg(
    R(16, 6, 68, 44, "#fff", 4),
    R(36, 22, 28, 22, "none", 1, RED, 3),
    L(net, "#90a4ae", 2.5),
    E(50, 54, 24, 6, "none", O, 7), E(50, 54, 24, 6, "#ff7043", "#ff7043", 3), E(50, 54, 24, 6, "none", "#ff7043", 3),
    face(50, 31, 0.7)))

# O: rowing boat with an oar
K.add("O", "Oar", "Row, row, row your boat!", svg(
    L("M4 88Q14 82 24 88T44 88T64 88T84 88T100 88", "#42a5f5", 3),
    TL("M22 18L80 84", WOOD, 5),
    P("M70 72Q84 70 92 86Q90 94 82 92Q72 84 70 72Z", "#ffb74d"),
    P("M6 54H94Q86 82 50 82Q14 82 6 54Z", "#ef5350"),
    P("M6 54H94L92 60H8Z", "#fff", O, 2.5),
    HL(18, 64, 2.5, 6, 60), face(50, 66, 0.9)))

# P: ping-pong paddle and ball
K.add("P", "Paddle", "Ping, pong, ping!", svg(
    TL("M62 62L86 90", WOOD, 12),
    C(42, 42, 30, RED),
    C(84, 20, 9, "#fff"),
    L("M74 34Q78 30 80 30", "#90a4ae", 2),
    HL(26, 28, 4, 8, 40), face(42, 42)))

# Q: quoits (ring toss)
K.add("Q", "Quoits", "Toss the ring on the peg!", svg(
    E(72, 22, 15, 7, "none", O, 9, rot=-20), E(72, 22, 15, 7, "none", "#ab47bc", 5, rot=-20),
    TL("M40 86V26", WOOD, 8),
    E(40, 76, 20, 6, "none", O, 9), E(40, 76, 20, 6, "none", "#29b6f6", 5),
    E(40, 66, 20, 6, "none", O, 9), E(40, 66, 20, 6, "none", "#66bb6a", 5),
    R(10, 82, 74, 14, "#8d6e63", 5),
    face(48, 86, 0.6, "#fff")))

# R: tennis racket and ball
strings = []
rx, ry = 22, 28
for xx in range(-16, 17, 8):
    h = ry * math.sqrt(1 - (xx / rx) ** 2)
    strings.append(f"M{40 + xx} {38 - h:.1f}V{38 + h:.1f}")
for yy in range(-21, 22, 7):
    w = rx * math.sqrt(1 - (yy / ry) ** 2)
    strings.append(f"M{40 - w:.1f} {38 + yy}H{40 + w:.1f}")
K.add("R", "Racket", "Hit the ball over the net!", svg(
    T("rotate(-30 40 50)",
      TL("M40 66V96", "#455a64", 9),
      E(40, 38, 22, 28, "#e3f2fd"),
      L("".join(strings), "#90a4ae", 1.2),
      E(40, 38, 22, 28, "none", O, 9), E(40, 38, 22, 28, "none", "#7e57c2", 5)),
    C(76, 76, 15, "#d4e157"),
    L("M63 70Q72 78 66 88M89 70Q80 76 86 86", "#fff", 2.5),
    HL(70, 68, 2.5, 4, 40), face(76, 76, 0.75)))

# S: skateboard
K.add("S", "Skateboard", "Roll and zoom!", svg(
    L("M2 40H14M4 50H12M2 60H14", "#90a4ae", 3),
    T("rotate(-8 50 56)",
      L("M30 64V72M70 64V72", O, 4),
      C(28, 76, 8, "#ffca28"), C(72, 76, 8, "#ffca28"),
      dot(28, 76, 2.5, O), dot(72, 76, 2.5, O),
      P("M14 44Q14 40 20 42L80 42Q86 40 88 44Q92 54 86 62Q84 64 80 64H20Q16 64 14 62Q8 54 14 44Z", "#7e57c2"),
      P("M22 46L32 46L28 58L18 58Z M78 46L68 46L72 58L82 58Z", "#ff7043", O, 1.5),
      face(50, 51, 0.8))))

# T: trophy
K.add("T", "Trophy", "You did it! Hooray!", svg(
    TL("M28 22Q10 22 12 36Q14 48 30 50M72 22Q90 22 88 36Q86 48 70 50", GOLD, 5),
    P("M26 12H74V36Q74 64 50 66Q26 64 26 36Z", GOLD),
    P("M44 66H56L58 78H42Z", "#ffb300"),
    R(28, 78, 44, 14, "#8d6e63", 3),
    R(40, 82, 20, 6, "#ffd54f", 1, O, 1.5),
    HL(34, 26, 3, 9, 10), face(50, 38)))

# U: team uniform (jersey)
K.add("U", "Uniform", "Ready to play for the team!", svg(
    P("M32 12L42 10Q50 20 58 10L68 12L90 30L78 44L70 38V90H30V38L22 44L10 30Z", "#43a047"),
    L("M16 36L26 26M84 36L74 26", "#fff", 4),
    L("M42 10Q50 20 58 10", "#fff", 3),
    P(star_path(50, 70, 9), "#fff", O, 2),
    HL(38, 30, 3, 7, 10), face(50, 46, 0.9)))

# V: volleyball: three swirled panels (yellow, blue, white)
def vb_panels():
    cx, cy, r = 50, 52, 38
    def pt(rad, deg):
        a = math.radians(deg)
        return cx + rad * math.cos(a), cy + rad * math.sin(a)
    parts = []
    for k, col in enumerate(("#ffca28", BLUE, "#fff")):
        t0 = -90 + 120 * k; t1 = t0 + 120
        e0 = pt(r, t0); e1 = pt(r, t1); c0 = pt(24, t0 - 40); c1 = pt(24, t1 - 40)
        parts.append(P(f"M{cx} {cy}Q{c0[0]:.1f} {c0[1]:.1f} {e0[0]:.1f} {e0[1]:.1f}"
                       f"A{r} {r} 0 0 1 {e1[0]:.1f} {e1[1]:.1f}Q{c1[0]:.1f} {c1[1]:.1f} {cx} {cy}Z", col, O, 2.5))
        m0 = pt(10, t0 + 60); mc = pt(28, t0 + 20); me = pt(r - 1, t0 + 52)
        parts.append(L(f"M{m0[0]:.1f} {m0[1]:.1f}Q{mc[0]:.1f} {mc[1]:.1f} {me[0]:.1f} {me[1]:.1f}", O, 1.6))
    return parts
K.add("V", "Volleyball", "Bump it up high!", svg(
    *vb_panels(),
    C(50, 52, 38, "none"),
    HL(66, 26, 3, 6, 50), face(33, 46, 0.75)))

# W: whistle
K.add("W", "Whistle", "Tweet! Time to play!", svg(
    L("M84 24Q92 18 96 24M86 34Q94 32 98 36M80 16Q84 8 90 10", "#90a4ae", 2.5),
    C(14, 38, 7, "none", O, 3),
    P("M18 62A26 26 0 1 0 66 50V48H88V30H44Q18 32 18 62Z", "#e53935"),
    E(58, 30, 6, 2, "#263238", O, 1.5),
    HL(30, 50, 3, 7, 40), face(42, 62, 0.85)))

# X: xiangqi (Chinese chess) piece
K.add("X", "Xiangqi", "A chess game from China!", svg(
    E(50, 62, 36, 30, "#c69c62"),
    E(50, 54, 36, 30, "#f3d9a4"),
    E(50, 54, 28, 22, "none", "#c62828", 2.5),
    L("M40 38H60M50 32V48M43 48H57", "#c62828", 4),
    HL(28, 44, 3, 6, 40), face(50, 61, 0.75)))

# Y: yo-yo
K.add("Y", "Yo-yo", "Up and down, up and down!", svg(
    L("M50 2V20", O, 2.5), C(50, 6, 4, "none", O, 2),
    C(50, 54, 36, "#ab47bc"),
    C(50, 54, 25, "#ce93d8", O, 2),
    L("M14 54H24M76 54H86", "#7b1fa2", 3),
    HL(30, 38, 3, 7, 40), face(50, 54)))

# Z: zip line
K.add("Z", "Zip line", "Wheee! Zoom down the line!", svg(
    TL("M8 12V96", WOOD, 6), TL("M92 52V96", WOOD, 6),
    L("M8 16L92 56", O, 3),
    C(46, 34, 6, "#90a4ae", O, 2.5),
    L("M46 34V68", O, 2.5),
    E(46, 74, 20, 8, "#ff7043"),
    L("M60 24L72 30M62 18L74 24", "#90a4ae", 2.5),
    face(46, 72, 0.6)))

add_extensions(K, "sports")

K.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "sports.js"),
        "SPORTS_ITEMS", "SPORTS", "Sports world: sports things A-Z, hand-made SVG (viewBox 0 0 100 100). Generated by sports_make.py.")
