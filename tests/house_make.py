"""House world: household things A-Z as hand-made SVG.  Writes tests/house.js.

Run:  python tests/house_make.py   then   python tests/pack_sheet.py tests/house.js house_sheet.png
"""
import math
import os
from svgkit import *

H = Pack()
WOOD = "#c58b5a"; WOODD = "#8d6e63"; RED = "#ef5350"; BLUE = "#42a5f5"; STEEL = "#b0bec5"

# A: alarm clock
H.add("A", "Alarm clock", "Ring, ring! Time to wake up!", svg(
    L("M30 84L22 94M70 84L78 94", O, 4),
    P("M14 30A14 14 0 0 1 36 14Z", "#ffca28"), P("M86 30A14 14 0 0 0 64 14Z", "#ffca28"),
    L("M44 10H56M50 10V18", O, 3),
    C(50, 54, 34, RED),
    C(50, 54, 26, "#fff"),
    L("M50 32V36M50 72V76M28 54H32M68 54H72", O, 2.5),
    L("M50 48L50 38M50 48L58 44", O, 2.5), dot(50, 48, 2, O),
    L("M8 44Q4 54 8 64M92 44Q96 54 92 64", "#90a4ae", 2.5),
    HL(30, 38, 3, 7, 40), face(50, 60, 0.75)))

# B: bed (sleepy face on the pillow)
H.add("B", "Bed", "Night night! Time for sleep!", svg(
    L("M14 80V92M86 80V92", O, 5),
    P("M8 34Q8 22 20 22Q32 22 32 34V82H8Z", WOOD),
    R(8, 58, 84, 22, "#fff", 4),
    P("M44 50H90V80H40Q36 64 44 50Z", "#5c6bc0"),
    L("M48 58H90", "#3949ab", 2.5),
    E(36, 50, 13, 8, "#fff"),
    sleepy(36, 48, 0.6),
    L("M64 14H72L64 22H72M78 6H84L78 12H84", "#5c6bc0", 2.5)))

# C: cup
H.add("C", "Cup", "A cup of warm milk!", svg(
    E(46, 90, 36, 6, "#fff"),
    TL("M70 44Q88 44 88 58Q88 72 70 72", "#29b6f6", 6),
    P("M22 30H70V72Q70 88 54 88H38Q22 88 22 72Z", "#29b6f6"),
    E(46, 30, 24, 5, "#fffaf0"),
    L("M36 22Q32 16 36 10M50 20Q46 14 50 6M62 22Q58 16 62 10", "#b0bec5", 2.5),
    HL(30, 48, 3, 9, 10), face(46, 58)))

# D: door
H.add("D", "Door", "Knock, knock! Who's there?", svg(
    R(14, 90, 72, 6, "#9e9e9e", 2),
    P("M24 90V20Q24 8 36 8H64Q76 8 76 20V90Z", "#a1887f"),
    R(32, 18, 36, 26, "none", 3, "#6d4c41", 2.5),
    R(32, 54, 36, 30, "none", 3, "#6d4c41", 2.5),
    C(68, 56, 4, "#ffd54f", O, 2),
    HL(30, 30, 2, 8, 0), face(50, 31, 0.8)))

# E: envelope
H.add("E", "Envelope", "A letter for you!", svg(
    R(10, 24, 80, 56, "#fff8e1", 4),
    L("M12 78L40 54M88 78L60 54", "#e0c9a6", 2.5),
    P("M10 26L50 58L90 26Z", "#ffecb3", O, 2.5),
    P(heart_path(50, 56, 0.9), "#e53935", O, 2),
    HL(22, 40, 2.5, 6, 40), face(50, 70, 0.75)))

# F: fridge
H.add("F", "Fridge", "Keeps our food cold!", svg(
    R(24, 6, 52, 88, "#e3f2fd", 6),
    L("M24 36H76", O, 3),
    L("M66 16V28M66 46V62", "#90a4ae", 4),
    P(star_path(36, 20, 5), "#ffca28", O, 1.5), P(heart_path(52, 22, 0.55), "#ec407a", O, 1.5),
    C(36, 80, 3.5, "#66bb6a", O, 1.5), C(64, 82, 3.5, "#ff7043", O, 1.5),
    L("M30 94V98M70 94V98", O, 3),
    HL(32, 50, 2, 8, 0), face(48, 62, 0.9)))

# G: glasses (the eyes are behind the lenses)
H.add("G", "Glasses", "They help us see!", svg(
    L("M14 46L4 36M86 46L96 36", O, 5), L("M14 46L4 36M86 46L96 36", "#e53935", 2),
    C(30, 52, 17, "#e1f5fe", O, 0), C(70, 52, 17, "#e1f5fe", O, 0),
    dot(31, 54, 4, O), dot(69, 54, 4, O), dot(32.5, 52.5, 1.3, "#fff"), dot(70.5, 52.5, 1.3, "#fff"),
    C(30, 52, 17, "none", O, 9), C(30, 52, 17, "none", "#e53935", 5),
    C(70, 52, 17, "none", O, 9), C(70, 52, 17, "none", "#e53935", 5),
    L("M46 50Q50 44 54 50", O, 7), L("M46 50Q50 44 54 50", "#e53935", 3),
    HL(23, 45, 2.5, 5, 40), HL(63, 45, 2.5, 5, 40),
    L("M44 80Q50 86 56 80", O, 2.5)))

# H: hammer
H.add("H", "Hammer", "Tap, tap, tap!", svg(
    T("rotate(-24 50 50)",
      TL("M50 40V94", WOOD, 12),
      L("M44 80H56M44 86H56", "#8d5a2b", 2),
      P("M18 18H72Q80 18 80 26V32Q80 40 72 40H18Q12 40 12 34V24Q12 18 18 18Z", "#90a4ae"),
      P("M80 22Q92 14 94 26Q90 22 80 30Z", "#78909c", O, 2.5),
      HL(22, 24, 2, 5, 70), face(46, 28, 0.75))))

# I: iron
H.add("I", "Iron", "Makes clothes nice and smooth!", svg(
    L("M18 90Q22 84 18 78M30 92Q34 86 30 80", "#b0bec5", 2.5),
    TL("M42 32Q44 12 62 12H80Q86 12 86 20V32", "#26a69a", 7),
    P("M10 70Q14 34 56 30H80Q92 30 92 42V70Z", "#4dd0e1"),
    P("M8 70H94V78Q94 82 90 82H10Q6 82 8 70Z", STEEL),
    HL(28, 50, 3, 8, 40), face(62, 52, 0.9)))

# J: jug
H.add("J", "Jug", "Pour me a drink!", svg(
    TL("M70 34Q90 36 88 54Q86 70 70 72", "#7e57c2", 6),
    P("M32 16H66L70 28Q76 50 72 80Q70 90 60 90H36Q26 90 24 80Q20 50 30 28L16 16Z", "#b3e5fc"),
    F("M24 52Q48 46 74 52Q76 66 72 80Q70 88 60 88H36Q26 88 25 80Q22 66 24 52Z", "#fff"),
    P("M32 16H66L70 28Q76 50 72 80Q70 90 60 90H36Q26 90 24 80Q20 50 30 28L16 16Z", "none"),
    L("M24 52Q48 46 74 52", "#90caf9", 2),
    HL(34, 32, 2.5, 7, 10), face(48, 64, 0.9)))

# K: kettle
H.add("K", "Kettle", "Whistle! The water is hot!", svg(
    L("M88 30Q84 24 88 18M94 34Q90 28 94 22", "#b0bec5", 2.5),
    TL("M28 44Q32 14 50 14Q68 14 72 44", "#455a64", 5),
    P("M74 58L90 38L94 42L82 72Z", RED),
    P("M20 88Q14 44 50 40Q86 44 80 88Z", RED),
    E(50, 40, 16, 5, "#e57373"), C(50, 33, 4, "#455a64", O, 2),
    L("M20 88H80", O, 4),
    HL(30, 56, 3, 9, 20), face(50, 64)))

# L: lamp
H.add("L", "Lamp", "Click! The light is on!", svg(
    F("M22 50L10 80H90L78 50Z", "#fff59d", ".55"),
    TL("M50 50V86", "#78909c", 5),
    E(50, 88, 22, 6, WOODD),
    P("M30 12H70L84 50H16Z", "#ffd54f"),
    L("M24 30H76", "#ffb300", 2),
    HL(32, 22, 2, 6, 20), face(50, 36, 0.85)))

# M: mirror (the face is the reflection)
H.add("M", "Mirror", "Who can you see? It's you!", svg(
    L("M36 82L28 96M64 82L72 96", WOODD, 5),
    E(50, 46, 30, 38, "#ffca28"),
    E(50, 46, 22, 30, "#e1f5fe", O, 2),
    L("M34 30L44 20M34 40L52 22", "#fff", 3),
    face(50, 52), blush(50, 58, 11, 3)))

# N: night light
H.add("N", "Night light", "It glows all night long!", svg(
    C(48, 46, 40, "#fff59d", O, 0).replace('fill="#fff59d"', 'fill="#fff59d" opacity=".45"'),
    P(star_path(84, 16, 5), "#ffd54f", O, 1.5), P(star_path(16, 22, 4), "#ffd54f", O, 1.5), P(star_path(82, 66, 3.5), "#ffd54f", O, 1.5),
    R(30, 82, 40, 12, "#9575cd", 4),
    P("M58 10A36 36 0 1 0 82 70A28 28 0 1 1 58 10Z", "#ffe082"),
    HL(30, 36, 3, 8, 30), face(34, 56, 0.8)))

# O: oven
H.add("O", "Oven", "Bake a yummy cake!", svg(
    R(14, 10, 72, 84, "#eceff1", 6),
    L("M14 28H86", O, 3),
    C(28, 19, 4, "#90a4ae", O, 2), C(42, 19, 4, "#90a4ae", O, 2), R(58, 15, 20, 8, "#263238", 2, O, 2),
    L("M30 36H70", O, 4),
    R(24, 42, 52, 30, "#455a64", 4),
    F("M28 70H72V64Q50 58 28 64Z", "#ff9800", ".5"),
    P("M38 66Q38 54 50 54Q62 54 62 66Z", "#ffcc80", O, 2),
    face(50, 81, 0.75)))

# P: pillow
H.add("P", "Pillow", "Soft and fluffy!", svg(
    P("M12 22Q50 12 88 22Q96 50 88 80Q50 90 12 80Q4 50 12 22Z", "#f8bbd0"),
    L("M22 30Q50 24 78 30M22 72Q50 78 78 72", "#f48fb1", 2),
    HL(24, 40, 3, 8, 20), face(50, 50), blush(50, 57, 13, 3)))

# Q: quilt (patchwork)
qc = ["#ef9a9a", "#fff59d", "#90caf9", "#a5d6a7", "#ffcc80", "#ce93d8", "#80deea", "#f48fb1", "#c5e1a5"]
quilt = []
for i in range(3):
    for j in range(3):
        quilt.append(R(14 + 24 * j, 14 + 24 * i, 24, 24, qc[i * 3 + j], 0, O, 2))
quilt += [L("M18 18H82V82H18Z", "#fff", 1.2).replace('stroke-linecap="round"', 'stroke-dasharray="3 3"'),
          R(14, 14, 72, 72, "none", 4), HL(22, 22, 2, 4, 40), face(50, 50, 0.8)]
H.add("Q", "Quilt", "Warm and cozy!", svg(*quilt))

# R: rubber duck
H.add("R", "Rubber duck", "Quack! Splash in the bath!", svg(
    L("M4 90Q14 84 24 90T44 90T64 90T84 90T100 90", "#4fc3f7", 3),
    P("M12 62Q12 88 46 88Q80 88 86 64Q88 50 76 52Q66 54 60 50Q72 40 70 26Q66 10 50 10Q32 12 32 30Q32 40 40 48Q20 46 12 62Z", "#ffd600"),
    P("M70 28Q84 26 88 32Q84 38 70 36Z", "#ff9800"),
    L("M32 66Q46 76 62 64", "#f9a825", 2.5),
    dot(56, 26, 3.5, O), dot(57, 25, 1.2, "#fff"), dot(50, 36, 3, "#ff8a80", ".6"),
    HL(40, 22, 3, 6, 30)))

# S: sofa
H.add("S", "Sofa", "Sit down and snuggle!", svg(
    L("M18 82V92M82 82V92", O, 5),
    R(16, 24, 68, 40, "#26a69a", 10),
    R(4, 44, 20, 40, "#00897b", 8), R(76, 44, 20, 40, "#00897b", 8),
    R(20, 60, 60, 22, "#4db6ac", 6),
    L("M50 62V80", "#00897b", 2),
    HL(26, 34, 2.5, 6, 40), face(50, 42)))

# T: toothbrush
H.add("T", "Toothbrush", "Brush, brush, brush your teeth!", svg(
    P("M8 56Q8 48 16 48H70L90 52V62L70 66H16Q8 66 8 56Z", "#42a5f5"),
    R(60, 30, 32, 18, "#fff", 2),
    L("M66 32V46M72 32V46M78 32V46M84 32V46", "#b0bec5", 2),
    P("M60 30Q58 18 70 20Q74 10 84 16Q96 14 92 30Z", "#80cbc4", O, 2.5),
    L("M66 24Q76 18 86 24", "#fff", 2.5),
    HL(18, 52, 1.5, 4, 90), face(36, 56, 0.7)))

# U: umbrella
H.add("U", "Umbrella", "It keeps us dry in the rain!", svg(
    L("M14 70L12 76M86 66L84 72M24 84L22 90", "#4fc3f7", 3),
    TL("M50 50V82Q50 92 41 92Q34 92 34 85", "#6d4c41", 4),
    P("M8 52Q10 14 50 12Q90 14 92 52Q82 44 71 52Q61 44 50 52Q39 44 29 52Q18 44 8 52Z", "#7e57c2"),
    L("M50 12Q38 30 29 52M50 12Q62 30 71 52", "#5e35b1", 2),
    L("M50 6V12", O, 3),
    HL(24, 32, 3, 8, 40), face(50, 34, 0.85)))

# V: vase with flowers
def daisy(x, y, col, r=7):
    petals = "".join(E(x + r * math.cos(math.radians(a)), y + r * math.sin(math.radians(a)), 4, 2.6, "#fff", O, 1.5, rot=a)
                     for a in range(0, 360, 60))
    return petals + C(x, y, 4, col, O, 1.5)
H.add("V", "Vase", "Pretty flowers!", svg(
    L("M44 44Q38 30 28 20M50 44V14M56 44Q64 30 74 22", "#43a047", 3),
    daisy(28, 20, "#ffca28"), daisy(50, 14, "#ff7043"), daisy(74, 22, "#ffca28"),
    P("M38 40Q20 54 26 78Q30 92 50 92Q70 92 74 78Q80 54 62 40V34H38Z", "#4db6ac"),
    HL(32, 58, 3, 9, 15), face(50, 68)))

# W: washing machine
H.add("W", "Washing machine", "Round and round, wash the clothes!", svg(
    R(16, 8, 68, 86, "#f5f5f5", 6),
    L("M16 24H84", O, 3),
    C(28, 16, 3.5, "#90a4ae", O, 2), R(54, 13, 22, 6, "#263238", 2, O, 1.5),
    C(50, 58, 25, STEEL),
    C(50, 58, 18, "#4fc3f7", O, 2.5),
    F("M33 62Q50 54 67 62Q66 74 50 76Q34 74 33 62Z", "#0288d1", ".45"),
    C(40, 48, 2, "#fff", O, 1), C(60, 50, 2.6, "#fff", O, 1), C(56, 44, 1.6, "#fff", O, 1),
    face(50, 58, 0.75)))

# X: xylophone (toy)
bars = ["#ef5350", "#ff9800", "#ffd54f", "#66bb6a", "#42a5f5", "#ab47bc"]
xy = [L("M12 34L88 46M12 74L88 64", WOODD, 5)]
for i, col in enumerate(bars):
    x = 14 + i * 12.5; top = 24 + i * 3.5; h = 60 - i * 7
    xy.append(R(x, top, 10, h, col, 3, O, 2.5))
    xy.append(dot(x + 5, top + 6, 1.6, O))
    xy.append(dot(x + 5, top + h - 6, 1.6, O))
xy += [TL("M64 8L92 30", WOOD, 3), C(62, 6, 5, "#e53935", O, 2.5),
       L("M88 82V92M88 82L96 80V90", O, 2.5), dot(86, 92, 3, O), dot(94, 90, 3, O),
       face(26, 54, 0.6)]
H.add("X", "Xylophone", "Ding, ding, dong!", svg(*xy))

# Y: ball of yarn with knitting needles
H.add("Y", "Yarn", "Knit a cozy scarf!", svg(
    TL("M18 18L72 78", "#90a4ae", 3), TL("M84 20L28 76", "#90a4ae", 3),
    dot(16, 16, 4, "#ffca28"), dot(86, 18, 4, "#ffca28"),
    L("M76 76Q90 82 86 92Q82 98 92 98", "#ec407a", 3),
    C(50, 54, 30, "#ec407a"),
    L("M24 44Q44 34 62 28M22 58Q48 44 74 36M30 76Q54 58 78 52M42 82Q64 70 80 66", "#ad1457", 2.2),
    C(50, 54, 30, "none"),
    HL(36, 38, 3, 7, 40), face(50, 58, 0.85)))

# Z: zipper on a pencil case
teeth = "".join(R(18 + 5 * i, 36 if i % 2 else 40, 4, 4, "#cfd8dc", 0.8, O, 1) for i in range(13))
H.add("Z", "Zipper", "Zip it up! Zzzip!", svg(
    P("M10 40Q10 30 20 30H80Q90 30 90 40V78Q90 88 80 88H20Q10 88 10 78Z", "#29b6f6"),
    teeth,
    R(76, 33, 10, 12, "#ffca28", 2, O, 2),
    TL("M81 45V58", "#ffca28", 3),
    C(81, 61, 4, "#ffca28", O, 2),
    HL(20, 54, 2.5, 7, 15), face(48, 64)))

H.write(os.path.join(os.path.dirname(os.path.abspath(__file__)), "house.js"),
        "HOUSE_ITEMS", "HOUSE", "House world: household things A-Z, hand-made SVG (viewBox 0 0 100 100). Generated by house_make.py.")
