"""Extra House pictures N–Z (4 per letter in total; X has 3)."""
import math
from svgkit import *

WOOD = "#c58b5a"; WOODD = "#8d6e63"; WOODL = "#deb887"; RED = "#ef5350"; BLUE = "#42a5f5"; STEEL = "#b0bec5"
GOLD = "#ffca28"; GREEN = "#66bb6a"; PINK = "#f48fb1"; GLASS = "#e1f5fe"


def note(x, y, s=1.0, col=O):
    """Single music note (stroked, filled head)."""
    return (E(x, y, 3.2 * s, 2.4 * s, col, O, 1.2, rot=-20)
            + L(f"M{x + 3 * s:g} {y:g}V{y - 12 * s:g}Q{x + 6 * s:g} {y - 9 * s:g} {x + 9 * s:g} {y - 7 * s:g}", O, 2))


def bubble(x, y, r):
    return C(x, y, r, "#e1f5fe", O, 1.8) + dot(x - r * 0.35, y - r * 0.35, r * 0.25, "#fff")


def fringe(x0, x1, y, dy, step=5, col=O):
    d = "".join(f"M{x:g} {y:g}V{y + dy:g}" for x in range(int(x0), int(x1) + 1, step))
    return L(d, col, 2.2)


def add_more(K):
    # ---------------------------------------------------------------- N
    # Napkin: fan-folded napkin through a gold ring
    band = "".join(F(f"M{x} 14H{x + 9}V86H{x}Z", "#ef5350", ".4") + F(f"M14 {x}H86V{x + 9}H14Z", "#ef5350", ".4")
                   for x in (14, 32, 50, 68))
    K.add("N", "Napkin", "Wipe your mouth!", svg(
        T("rotate(-8 50 50)",
          R(14, 14, 72, 72, "#fff", 4),
          band,
          P("M86 52V82Q86 86 82 86H52Z", "#ffcdd2", O, 2.5),
          R(14, 14, 72, 72, "none", 4),
          L("M20 22H24", "#fff", 0)),
        HL(22, 22, 2, 5, 40), face(50, 48, 0.95), blush(50, 55, 12, 3)))

    # Notebook: spiral notebook with a pencil
    rings = "".join(L(f"M{x} 10V22", "#90a4ae", 3) + dot(x, 22, 2, O) for x in range(26, 72, 9))
    K.add("N", "Notebook", "Let's draw a picture!", svg(
        R(14, 16, 60, 78, "#7e57c2", 5),
        R(20, 16, 54, 72, "#fffde7", 3, O, 2.5),
        L("M26 40H66M26 50H66M26 60H66M26 70H66", "#90caf9", 2),
        L("M30 24V84", "#ef9a9a", 1.5),
        rings,
        T("translate(-8 2) rotate(28 74 56)",
          R(70, 26, 12, 48, "#ffd54f", 2),
          L("M74 28V72M78 28V72", "#f9a825", 1.5),
          R(70, 20, 12, 8, "#f48fb1", 2, O, 2.5),
          P("M70 74H82L76 90Z", "#ffe0b2"),
          P("M74.5 84H77.5L76 90Z", O, O, 1)),
        HL(24, 34, 2, 5, 30), face(44, 46, 0.8)))

    # Nightstand: bedside table with a drawer, a book and a glass of water
    K.add("N", "Nightstand", "Right next to my bed!", svg(
        L("M24 82V94M76 82V94", O, 6), L("M24 82V93M76 82V93", WOODD, 2.5),
        R(14, 30, 72, 10, WOODD, 3),
        R(18, 38, 64, 46, WOOD, 4),
        R(24, 44, 52, 14, "#d7a26f", 3, O, 2.5),
        C(50, 51, 3, GOLD, O, 2),
        R(24, 62, 52, 16, "#d7a26f", 3, O, 2.5),
        R(22, 20, 32, 10, "#42a5f5", 2), L("M26 25H50", "#fff", 2),
        R(26, 12, 26, 8, "#ef5350", 2), L("M30 16H48", "#fff", 2),
        P("M62 6H76L74 30H64Z", GLASS), F("M63.2 16H74.8L74 29H64Z", "#81d4fa", ".8"),
        P("M62 6H76L74 30H64Z", "none", O, 2.5),
        HL(28, 48, 1.5, 3, 60), face(50, 67, 0.75)))

    # ---------------------------------------------------------------- O
    # Oven mitt
    K.add("O", "Oven mitt", "Ouch, hot! Use a mitt!", svg(
        L("M58 6Q66 2 66 12", O, 3),
        P("M36 86V40Q36 14 56 12Q76 12 76 36V58Q84 48 90 52Q94 58 86 68L74 86Z", "#ef5350"),
        R(30, 80, 50, 14, "#fff", 5),
        L("M42 84V90M50 84V90M58 84V90M66 84V90", "#ef9a9a", 2),
        L("M44 30L68 54M44 46L66 68M52 22L74 44", "#e57373", 1.8),
        L("M44 54L60 30M44 70L72 34", "#e57373", 1.8),
        HL(44, 26, 2.5, 7, 20), face(56, 52, 0.85)))

    # Ottoman: round padded footstool
    K.add("O", "Ottoman", "Put your feet up!", svg(
        L("M24 82L22 94M76 82L78 94M50 86V94", O, 6), L("M24 82L22 93M76 82L78 93M50 86V93", WOODD, 2.5),
        P("M10 38V70Q10 88 50 88Q90 88 90 70V38Z", "#26a69a"),
        L("M10 70Q10 80 50 80Q90 80 90 70", "#00897b", 2.5),
        E(50, 38, 40, 16, "#4db6ac"),
        dot(36, 34, 2, O), dot(64, 34, 2, O), dot(50, 42, 2, O), dot(50, 29, 2, O), dot(30, 42, 2, O), dot(70, 42, 2, O),
        L("M36 34L50 42L64 34L50 29Z", "#00897b", 1.5),
        HL(22, 54, 2.5, 7, 10), face(50, 62, 0.9)))

    # Orange juicer: glass juicer with half an orange on the cone
    K.add("O", "Orange juicer", "Squeeze! Yummy orange juice!", svg(
        P("M14 46H86Q86 58 76 62H24Q14 58 14 46Z", GLASS),
        P("M24 60H76L72 86Q70 94 60 94H40Q30 94 28 86Z", GLASS),
        F("M26.5 72H73.5L72 86Q70 92 60 92H40Q30 92 28.4 86Z", "#ffb74d"),
        P("M24 60H76L72 86Q70 94 60 94H40Q30 94 28 86Z", "none"),
        TL("M76 66Q90 66 88 78Q86 88 72 86", GLASS, 4),
        P("M40 48L50 34L60 48Z", "#e1f5fe", O, 2.5),
        P("M22 30Q22 4 50 4Q78 4 78 30Z", "#ff9800"),
        E(50, 31, 28, 11, "#fff3e0"),
        E(50, 31, 23, 8, "#ffb74d", "#ffe0b2", 1),
        L("M50 23V39M34 26L66 36M66 26L34 36M28 31H72", "#fff3e0", 1.8),
        E(50, 31, 28, 11, "none"),
        HL(32, 14, 2.5, 5, 60), HL(30, 72, 2, 6, 10), face(50, 78, 0.8)))

    # ---------------------------------------------------------------- P
    # Plate with a stack of pancakes
    K.add("P", "Plate", "Pancakes on my plate!", svg(
        E(50, 76, 44, 16, "#fff"),
        E(50, 76, 32, 10, "none", "#cfd8dc", 2),
        P("M18 66V56Q18 50 50 50Q82 50 82 56V66Q82 74 50 74Q18 74 18 66Z", "#ffcc80"),
        L("M18 60Q18 66 50 66Q82 66 82 60", "#e6a057", 2),
        P("M18 46V36Q18 30 50 30Q82 30 82 36V46Q82 54 50 54Q18 54 18 46Z", "#ffcc80"),
        P("M24 36Q22 28 50 26Q80 28 76 36Q78 44 70 42Q66 50 62 42Q50 46 40 42Q34 48 32 40Q22 42 24 36Z", "#d84315", O, 2.5),
        R(40, 22, 18, 10, "#fff59d", 3, O, 2.5),
        HL(26, 40, 2, 4, 70), face(50, 60, 0.8)))

    # Pan with a fried egg
    K.add("P", "Pan", "Sizzle! Fry an egg!", svg(
        TL("M76 66L91 81", "#5d4037", 6),
        C(44, 52, 36, "#455a64"),
        C(44, 52, 28, "#607d8b", O, 2),
        P("M24 50Q20 34 36 32Q44 22 56 32Q70 34 66 50Q70 66 52 68Q40 76 30 66Q16 62 24 50Z", "#fff", O, 2.5),
        C(46, 50, 11, "#ffb300", O, 2.5),
        L("M14 18Q10 12 14 6M22 16Q18 10 22 4", "#b0bec5", 2.5),
        HL(40, 44, 2, 4, 40), face(46, 50, 0.6)))

    # Piano: small upright piano
    keys = "".join(R(14 + 8 * i, 46, 8, 18, "#fff", 1, O, 1.8) for i in range(9))
    blacks = "".join(R(19.5 + 8 * i, 46, 5, 11, "#263238", 1, O, 1.2) for i in (0, 1, 3, 4, 5, 7))
    K.add("P", "Piano", "Plink, plonk! Play a tune!", svg(
        L("M18 88V95M82 88V95", O, 5),
        R(12, 14, 76, 76, "#8d4f3a", 5),
        R(8, 40, 84, 8, "#a1624a", 3),
        keys, blacks,
        R(8, 64, 84, 6, "#a1624a", 2),
        R(32, 20, 36, 16, "#fff8e1", 2, O, 2),
        L("M36 26H64M36 30H64", "#bcaaa4", 1.2),
        note(44, 32, 0.55), note(56, 30, 0.55),
        R(30, 84, 10, 4, GOLD, 1, O, 1.5), R(60, 84, 10, 4, GOLD, 1, O, 1.5),
        note(88, 10, 0.7), note(8, 10, 0.6),
        HL(18, 22, 2, 5, 20), face(50, 75, 0.75)))

    # ---------------------------------------------------------------- Q
    # Quill in an ink pot
    K.add("Q", "Quill", "Write with a feather pen!", svg(
        L("M50 66L78 8", O, 2.5),
        P("M50 64Q48 40 62 22Q72 8 84 4Q86 20 78 34Q68 52 50 64Z", "#fff"),
        L("M50 64Q64 36 82 8", "#bdbdbd", 2),
        L("M60 46L70 42M64 36L74 32M70 26L80 22M58 52L66 50", "#bdbdbd", 1.6),
        P("M26 62H74V82Q74 92 64 92H36Q26 92 26 82Z", "#3949ab"),
        R(32, 54, 36, 10, "#283593", 3),
        E(50, 55, 16, 3, "#1a237e", O, 1.5),
        HL(32, 72, 2, 6, 10), face(50, 76, 0.8)))

    # Quiche in a fluted dish with a slice cut out
    def fluted(cx, cy, rx, ry, n, amp, a0, a1):
        pts = []
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            k = 1 + (amp if i % 2 == 0 else -amp)
            pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
        return pts
    cx, cy = 50, 54
    rim = fluted(cx, cy, 42, 32, 40, 0.045, 30, 330)
    d_dish = "M" + f"{cx} {cy}L" + "L".join(f"{x:.1f} {y:.1f}" for x, y in rim) + "Z"
    fill_pts = [(cx + 34 * math.cos(math.radians(a)), cy + 25 * math.sin(math.radians(a))) for a in range(30, 331, 10)]
    d_fill = f"M{cx} {cy}L" + "L".join(f"{x:.1f} {y:.1f}" for x, y in fill_pts) + "Z"
    K.add("Q", "Quiche", "A warm slice of quiche!", svg(
        E(50, 62, 44, 32, "#90a4ae", O, 3),
        P(d_dish, "#e0a458"),
        P(d_fill, "#ffe082", O, 2.5),
        dot(36, 44, 3, GREEN), dot(58, 66, 3, GREEN), dot(30, 64, 3, "#ef5350"), dot(48, 36, 2.5, "#ef5350"),
        dot(64, 38, 2.5, GREEN), dot(42, 70, 2.5, "#ef5350"),
        P("M70 50L92 58L92 70L74 64Z", "#ffe082"),
        HL(26, 50, 2, 5, 30), face(44, 54, 0.75)))

    # Quiz book: book with a big question mark
    K.add("Q", "Quiz book", "What is it? Let's guess!", svg(
        P("M20 10H80Q86 10 86 16V84Q86 90 80 90H20Z", "#fff", O, 3),
        R(14, 8, 68, 84, "#ab47bc", 5),
        R(14, 8, 12, 84, "#8e24aa", 4),
        L("M44 34Q44 20 56 20Q68 20 68 32Q68 40 58 44Q56 46 56 54", O, 12),
        L("M44 34Q44 20 56 20Q68 20 68 32Q68 40 58 44Q56 46 56 54", GOLD, 6),
        C(56, 68, 5, GOLD, O, 3),
        HL(32, 20, 2, 6, 20), face(56, 82, 0.6)))

    # ---------------------------------------------------------------- R
    # Rug: oval patterned rug with fringe
    K.add("R", "Rug", "A soft rug on the floor!", svg(
        L("M8 30H2M8 38H2M8 46H2M8 54H2M8 62H2M8 70H2", O, 2.2),
        L("M92 30H98M92 38H98M92 46H98M92 54H98M92 62H98M92 70H98", O, 2.2),
        R(8, 24, 84, 52, "#ef5350", 6),
        P("M14 50L19 40L24 50L19 60ZM76 50L81 40L86 50L81 60Z", "#fff59d", O, 2),
        R(28, 31, 44, 38, "#42a5f5", 4, O, 2.5),
        P("M50 33L68 50L50 67L32 50Z", "#ffca28", O, 2.5),
        HL(14, 32, 1.5, 3, 40), face(50, 48, 0.7)))

    # Radio: retro radio with music notes
    K.add("R", "Radio", "La la la! Music time!", svg(
        L("M66 30L84 8", O, 3), dot(84, 8, 3, O),
        R(10, 30, 80, 58, "#ff7043", 10),
        TL("M30 30Q30 18 50 18Q70 18 70 30", "#6d4c41", 4),
        C(34, 60, 18, "#ffe0b2"),
        L("M22 52H46M20 60H48M22 68H46", "#bf8a5a", 2.5),
        R(58, 44, 24, 12, "#fff8e1", 2, O, 2), L("M70 44V56", RED, 2),
        C(64, 72, 5, "#455a64", O, 2), C(77, 72, 5, "#455a64", O, 2),
        L("M14 88V94M86 88V94", O, 4),
        note(14, 22, 0.7), note(24, 12, 0.55),
        HL(18, 40, 2, 5, 30), face(34, 60, 0.7)))

    # Remote control
    btn = "".join(C(42 + 8 * (i % 3) - 8, 56 + 9 * (i // 3), 3, c, O, 1.8)
                  for i, c in enumerate(["#90caf9", "#90caf9", "#90caf9", "#a5d6a7", "#a5d6a7", "#a5d6a7"]))
    K.add("R", "Remote control", "Click! Change the show!", svg(
        L("M66 14Q74 10 74 2M72 20Q84 16 86 6", "#ffb300", 2.5),
        R(30, 10, 36, 84, "#455a64", 14),
        C(48, 22, 5, "#ef5350", O, 2.5), L("M48 18V22", "#fff", 1.6),
        C(48, 40, 9, "#90a4ae", O, 2.5), C(48, 40, 3, "#cfd8dc", O, 1.5),
        L("M48 31.5V34M48 46V48.5M39.5 40H42M54 40H56.5", "#fff", 1.6),
        btn,
        HL(36, 22, 1.5, 6, 10), face(48, 80, 0.75, "#fff")))

    # ---------------------------------------------------------------- S
    # Spoon
    K.add("S", "Spoon", "Yum! Eat with a spoon!", svg(
        T("rotate(35 50 50)",
          P("M45 48Q41 78 45 96Q50 101 55 96Q59 78 55 48Z", "#b0bec5"),
          E(50, 28, 22, 27, "#cfd8dc"),
          E(50, 30, 16, 20, "#eceff1", "#90a4ae", 2),
          HL(41, 20, 2.5, 7, 0)),
        face(62, 34, 0.8), blush(62, 40, 9, 2.5)))

    # Sink with tap and bubbles
    K.add("S", "Sink", "Wash, wash, splash!", svg(
        R(6, 46, 88, 12, "#bcaaa4", 3),
        P("M12 58H88V84Q88 92 80 92H20Q12 92 12 84Z", "#e0e0e0"),
        P("M18 52H82V66Q82 76 72 76H28Q18 76 18 66Z", "#b3e5fc", O, 2.5),
        TL("M50 46V20Q50 12 58 12Q66 12 66 20V26", "#90a4ae", 4),
        R(62, 26, 8, 6, "#78909c", 2, O, 2),
        L("M66 34V44", "#4fc3f7", 3),
        bubble(26, 40, 6), bubble(36, 30, 4.5), bubble(80, 36, 5), bubble(86, 24, 3.5), bubble(30, 20, 3),
        HL(20, 72, 2, 4, 30), face(50, 82, 0.75)))

    # Soap bar with bubbles
    K.add("S", "Soap", "Bubbles! Clean hands!", svg(
        P("M10 70Q10 56 24 54H76Q90 56 90 70V78Q90 90 76 90H24Q10 90 10 78Z", "#f48fb1"),
        P("M14 64Q16 46 30 46H70Q84 46 86 64Q84 74 70 74H30Q16 74 14 64Z", "#f8bbd0"),
        bubble(26, 30, 10), bubble(52, 18, 8), bubble(74, 28, 12), bubble(42, 36, 5), bubble(88, 10, 4), bubble(12, 12, 4),
        HL(26, 56, 2, 5, 70), face(50, 76, 0.85)))

    # ---------------------------------------------------------------- T
    # Teapot
    K.add("T", "Teapot", "Pour a cup of tea!", svg(
        TL("M76 44Q94 40 92 58Q90 72 76 74", "#4fc3f7", 5),
        P("M24 58Q14 52 8 34L14 32Q20 44 28 46Z", "#4fc3f7"),
        P("M20 66Q20 36 50 34Q80 36 80 66Q80 88 50 88Q20 88 20 66Z", "#4fc3f7"),
        E(50, 35, 22, 6, "#81d4fa"),
        P("M36 34Q36 22 50 22Q64 22 64 34Z", "#81d4fa"),
        C(50, 18, 4, GOLD, O, 2.5),
        L("M22 70Q50 80 78 70", "#fff", 3),
        dot(32, 76, 2.5, "#fff"), dot(68, 76, 2.5, "#fff"), dot(50, 79, 2.5, "#fff"),
        L("M8 22Q4 16 8 10M14 20Q10 14 14 8", "#b0bec5", 2.2),
        E(50, 90, 26, 3, "none", O, 0),
        HL(30, 52, 3, 8, 20), face(50, 58, 0.9)))

    # Table: dining table with tablecloth and fruit bowl
    K.add("T", "Table", "Dinner time at the table!", svg(
        L("M18 62V94M82 62V94M30 62V90M70 62V90", O, 7), L("M18 62V93M82 62V93M30 62V89M70 62V89", WOOD, 3),
        R(8, 50, 84, 8, WOOD, 3),
        P("M14 50H86L84 70L78 64L72 70L66 64L60 70L54 64L48 70L42 64L36 70L30 64L24 70L18 64L16 70Z", "#fff"),
        L("M20 50V66M32 50V66M44 50V66M56 50V66M68 50V66M80 50V66", "#ef9a9a", 2.5),
        L("M14 58H86", "#ef9a9a", 2.5),
        C(36, 30, 9, RED), L("M36 21Q36 16 40 14", O, 2.5),
        C(62, 30, 9, "#ff9800"), P("M62 20Q68 14 72 18Q66 22 62 20Z", GREEN, O, 2),
        C(49, 26, 8, "#fdd835"),
        P("M26 36H74Q72 50 50 50Q28 50 26 36Z", "#4fc3f7"),
        HL(32, 40, 1.5, 3, 60), face(50, 41, 0.6)))

    # Television with a cartoon picture
    K.add("T", "Television", "Time for a cartoon!", svg(
        L("M40 22L28 6M60 22L72 6", O, 3), dot(28, 6, 3, O), dot(72, 6, 3, O),
        L("M28 84L22 94M72 84L78 94", O, 5),
        R(8, 20, 84, 66, "#7e57c2", 10),
        R(16, 28, 56, 50, "#81d4fa", 6, O, 2.5),
        P("M17.5 64Q30 52 44 62Q56 54 70.5 62V72Q70.5 76.5 66 76.5H22Q17.5 76.5 17.5 72Z", "#81c784", O, 0),
        C(54, 44, 8, "#ffeb3b", O, 2),
        L("M54 32V30M66 44H68M62 36L64 34M46 36L44 34", "#f9a825", 2),
        R(16, 28, 56, 50, "none", 6, O, 2.5),
        C(82, 40, 4, GOLD, O, 2), C(82, 54, 4, GOLD, O, 2),
        L("M78 66H86M78 72H86", O, 2),
        HL(22, 36, 2, 5, 40), face(34, 48, 0.7)))

    # ---------------------------------------------------------------- U
    # Ukulele
    K.add("U", "Ukulele", "Strum, strum! Sing a song!", svg(
        T("rotate(35 50 50) translate(50 50) scale(0.88) translate(-50 -48)",
          R(44, 2, 12, 46, WOODD, 3),
          P("M42 -6H58V8H42Z", "#6d4c41"),
          dot(40, -2, 2.5, O), dot(40, 5, 2.5, O), dot(60, -2, 2.5, O), dot(60, 5, 2.5, O),
          P("M50 40Q30 38 30 56Q30 64 34 68Q24 74 26 88Q30 102 50 102Q70 102 74 88Q76 74 66 68Q70 64 70 56Q70 38 50 40Z", "#ffb74d"),
          C(50, 66, 7, "#5d4037", O, 2.5),
          R(42, 84, 16, 5, "#6d4c41", 2, O, 2),
          L("M47 6V84M50 6V84M53 6V84", "#fff8e1", 1),
          HL(36, 52, 2, 5, 0), face(50, 92, 0.6)),
        note(14, 22, 0.8), note(88, 70, 0.7)))

    # Utensils: pot with a wooden spoon, whisk and spatula
    K.add("U", "Utensils", "Stir, whisk and flip!", svg(
        TL("M30 52L18 18", WOOD, 4), E(17, 14, 6, 9, WOOD, O, 3, rot=-20),
        TL("M50 52V24", "#90a4ae", 3),
        P("M50 26Q38 16 42 6Q46 -2 50 6Q54 -2 58 6Q62 16 50 26Z", "none", O, 2.5),
        L("M50 26Q44 14 50 4Q56 14 50 26", O, 2),
        TL("M70 52L80 26", "#455a64", 3),
        R(74, 6, 16, 22, "#ef5350", 3, O, 2.5, rot=20),
        L("M80 12L78 20M85 14L83 22", "#fff", 1.5),
        P("M18 50H82L78 88Q76 94 68 94H32Q24 94 22 88Z", "#4dd0e1"),
        R(14, 46, 72, 10, "#26a69a", 4),
        HL(28, 64, 2.5, 7, 10), face(50, 72, 0.9)))

    # Unicorn toy: plush unicorn sitting
    K.add("U", "Unicorn toy", "My soft cuddly unicorn!", svg(
        P("M22 70Q4 66 6 84Q10 80 14 84Q14 78 20 80Z", "#ce93d8"),
        E(44, 74, 26, 17, "#fce4ec"),
        E(34, 88, 9, 6, "#fce4ec"), E(62, 88, 10, 6, "#fce4ec"),
        dot(30, 91, 2.5, "#ce93d8"), dot(67, 91, 2.5, "#ce93d8"),
        C(34, 26, 8, "#ce93d8", O, 2.5), C(28, 38, 8, "#80deea", O, 2.5), C(28, 51, 8, "#f48fb1", O, 2.5), C(33, 62, 7, "#fff176", O, 2.5),
        P("M34 44Q32 20 52 18Q66 18 72 32Q82 42 80 52Q78 62 66 60Q58 58 50 64Q36 66 34 44Z", "#fce4ec"),
        P("M42 22L40 8L52 18Z", "#fce4ec", O, 2.5),
        P("M54 20L72 4L64 26Z", GOLD, O, 2.5),
        L("M58 18L66 16M62 13L68 10", "#f9a825", 2),
        P("M36 30Q40 16 54 18Q50 26 40 32Z", "#ce93d8", O, 2.5),
        dot(74, 48, 1.8, O),
        face(58, 38, 0.75), dot(68, 50, 3, "#ff8a80", ".6"),
        HL(42, 34, 2, 5, 20), HL(30, 70, 2, 5, 40)))

    # ---------------------------------------------------------------- V
    # Vacuum cleaner: canister vacuum with hose
    K.add("V", "Vacuum cleaner", "Vroom! Clean the floor!", svg(
        TL("M62 52Q70 30 56 22Q44 16 38 24", "#7e57c2", 5),
        TL("M38 24L22 78", "#90a4ae", 4),
        P("M8 78H36Q40 78 40 84V88H8Q4 88 4 84Q4 78 8 78Z", "#455a64"),
        P("M44 82Q40 50 68 46Q94 46 94 72Q94 84 84 86H52Q44 86 44 82Z", "#ef5350"),
        C(56, 86, 6, "#455a64", O, 2.5), C(84, 86, 6, "#455a64", O, 2.5),
        C(76, 58, 3, GOLD, O, 2),
        L("M26 94Q20 92 14 94", "#bdbdbd", 2), dot(12, 94, 1.5, "#bdbdbd"),
        HL(56, 56, 2, 5, 40), face(68, 70, 0.8)))

    # Violin with bow
    K.add("V", "Violin", "Play a pretty song!", svg(
        T("rotate(-30 50 54)",
          R(45, 0, 10, 40, "#5d4037", 3),
          P("M44 -6Q50 -12 56 -6Q56 2 50 2Q44 2 44 -6Z", "#5d4037"),
          P("M50 30Q32 30 34 46Q36 54 40 58Q30 62 30 78Q32 96 50 96Q68 96 70 78Q70 62 60 58Q64 54 66 46Q68 30 50 30Z", "#d84315"),
          P("M40 60Q42 64 40 70M60 60Q58 64 60 70", "none", O, 2.5),
          R(44, 76, 12, 4, "#3e2723", 1, O, 1.5),
          P("M44 86H56L54 94H46Z", "#3e2723", O, 1.5),
          L("M48 2V86M52 2V86", "#fff8e1", 0.8),
          HL(40, 42, 2, 5, 0)),
        L("M8 72L88 30", O, 5), L("M8 72L88 30", "#a1887f", 2),
        L("M12 64L88 26", "#fff8e1", 1.2),
        face(62, 72, 0.7)))

    # Valentine card
    K.add("V", "Valentine card", "I love you! Here's a card!", svg(
        R(14, 14, 72, 76, "#fff", 5, rot=-6),
        R(18, 10, 68, 76, "#f8bbd0", 5, rot=6),
        P(heart_path(52, 46, 3.0), "#e53935"),
        P(heart_path(24, 20, 0.7), "#f06292", O, 2), P(heart_path(82, 80, 0.8), "#f06292", O, 2),
        P(heart_path(80, 18, 0.5), "#e53935", O, 1.5),
        L("M28 74Q50 84 74 78", "#ec407a", 2.5),
        HL(40, 36, 3, 6, 40), face(52, 48, 0.85)))

    # ---------------------------------------------------------------- W
    # Watering can
    K.add("W", "Watering can", "Water the flowers!", svg(
        P("M60 72L82 34L88 38L68 82Z", "#66bb6a"),
        P("M78 30L92 18L98 30L86 40Z", "#43a047", O, 2.5),
        dot(84, 28, 1.2, O), dot(90, 26, 1.2, O), dot(89, 32, 1.2, O),
        L("M96 40V46M91 44L89 50M97 52V56", "#4fc3f7", 2.5),
        TL("M42 42Q40 14 20 18Q4 24 14 66", "#388e3c", 5),
        P("M14 48Q14 40 22 40H60Q68 40 68 48V84Q68 92 60 92H22Q14 92 14 84Z", "#66bb6a"),
        E(41, 41, 22, 4, "#81c784", O, 2.5),
        L("M14 56H68", "#43a047", 2.5),
        HL(22, 66, 2.5, 7, 10), face(41, 70, 0.9)))

    # Window with sky and a flower box
    def flower(x, y, col):
        return (L(f"M{x} {y}V{y + 12}", "#43a047", 2.5)
                + "".join(C(x + 4 * math.cos(math.radians(a)), y + 4 * math.sin(math.radians(a)), 3, col, O, 1.5) for a in range(0, 360, 72))
                + C(x, y, 2.5, GOLD, O, 1.5))
    K.add("W", "Window", "Look outside! It's sunny!", svg(
        R(14, 8, 72, 66, "#81d4fa", 4, "#fff", 0),
        C(68, 26, 9, "#ffeb3b", O, 2),
        P("M22 32Q20 24 26 24Q28 18 34 21Q40 19 40 25Q44 27 42 32Z", "#fff", O, 2),
        R(14, 8, 72, 66, "none", 4, O, 0),
        L("M50 10V72M16 41H84", "#fff", 8), L("M50 10V72M16 41H84", O, 0),
        R(14, 8, 72, 66, "none", 4, "#fff", 8),
        R(10, 4, 80, 74, "none", 6, O, 3),
        R(18, 12, 64, 58, "none", 2, O, 2.5),
        L("M46 12V70M54 12V70M18 37H82M18 45H82", O, 2),
        flower(26, 70, "#f06292"), flower(42, 72, "#ffb74d"), flower(58, 70, "#ba68c8"), flower(74, 72, "#f06292"),
        R(8, 78, 84, 14, "#a1887f", 4),
        HL(26, 20, 2, 6, 40), face(50, 85, 0.6)))

    # Wardrobe
    K.add("W", "Wardrobe", "My clothes live inside!", svg(
        L("M22 90V96M78 90V96", O, 5),
        P("M14 14Q14 6 22 6H78Q86 6 86 14V90H14Z", WOOD),
        R(10, 4, 80, 8, WOODD, 3),
        R(20, 16, 28, 48, "#d7a26f", 3, O, 2.5), R(52, 16, 28, 48, "#d7a26f", 3, O, 2.5),
        R(20, 68, 60, 18, "#d7a26f", 3, O, 2.5),
        C(44, 40, 3, GOLD, O, 2), C(56, 40, 3, GOLD, O, 2),
        HL(26, 26, 2, 7, 10), face(50, 74, 0.75)))

    # ---------------------------------------------------------------- X
    # Xmas tree
    K.add("X", "Xmas tree", "Twinkle, twinkle! Merry Christmas!", svg(
        R(42, 80, 16, 12, WOODD, 2),
        P("M50 14L74 40H64L82 62H70L90 82H10L30 62H18L36 40H26Z", "#43a047"),
        L("M30 50Q50 58 70 48M22 72Q50 80 80 68", "#ffca28", 2.5),
        C(38, 44, 3.5, RED, O, 1.8), C(62, 58, 3.5, BLUE, O, 1.8), C(30, 76, 3.5, "#ab47bc", O, 1.8),
        C(70, 76, 3.5, RED, O, 1.8), C(44, 64, 3.5, GOLD, O, 1.8),
        P(star_path(50, 13, 11), "#ffd600", O, 2.5),
        R(30, 86, 12, 10, RED, 2, O, 2), L("M36 86V96", GOLD, 2),
        R(60, 84, 14, 12, BLUE, 2, O, 2), L("M67 84V96", GOLD, 2),
        HL(42, 36, 1.5, 4, 40), face(50, 50, 0.75)))

    # Xmas stocking
    K.add("X", "Xmas stocking", "What's inside? Presents!", svg(
        L("M26 14Q20 2 30 4Q36 6 32 14", O, 2.5),
        TL("M58 24V10Q58 4 64 4Q70 4 70 10", "#fff", 4),
        L("M58 20L58 16M58 12L60 8M66 4L70 8", "#e53935", 3),
        P("M28 22H66V58Q76 66 80 74Q84 88 70 92Q56 96 42 86Q26 76 28 58Z", "#e53935"),
        R(22, 12, 50, 16, "#fff", 7),
        P("M52 82Q60 90 72 86Q80 82 78 74Q72 66 64 66Q60 76 52 82Z", "#43a047", O, 2.5),
        HL(36, 40, 2, 6, 10), face(46, 52, 0.85)))

    # ---------------------------------------------------------------- Y
    # Yogurt pot with a spoon and berries
    K.add("Y", "Yogurt pot", "Yummy yogurt with berries!", svg(
        TL("M60 34L84 4", "#90a4ae", 4),
        P("M18 34H82L74 86Q72 92 64 92H36Q28 92 26 86Z", "#fff"),
        F("M20.5 50H79.5L77.4 64H22.6Z", "#f48fb1"),
        P("M18 34H82L74 86Q72 92 64 92H36Q28 92 26 86Z", "none"),
        E(50, 34, 32, 8, "#fff3f6"),
        C(36, 30, 5, "#e53935", O, 2), C(48, 26, 5, "#5c6bc0", O, 2), C(66, 30, 5, "#e53935", O, 2), C(56, 34, 4.5, "#5c6bc0", O, 2),
        dot(35, 28, 1.2, "#fff"), dot(65, 28, 1.2, "#fff"),
        HL(28, 72, 2, 6, 10), face(50, 76, 0.85)))

    # Yardstick: long wooden ruler
    marks = "".join(L(f"M{x} 40V{50 if i % 2 == 0 else 46}", O, 2) for i, x in enumerate(range(10, 92, 6)))
    K.add("Y", "Yardstick", "Measure how tall you are!", svg(
        T("rotate(-30 50 50)",
          R(0, 38, 100, 24, "#ffd54f", 4),
          L(" ".join(f"M{x} 38V{48 if i % 2 == 0 else 44}" for i, x in enumerate(range(8, 96, 6))), O, 2),
          C(92, 54, 2.5, "#fff", O, 2),
          HL(8, 56, 1.5, 4, 90),
          face(50, 52, 0.7))))

    # Yellow raincoat on a hook
    K.add("Y", "Yellow raincoat", "Splash in the rain!", svg(
        R(10, 4, 80, 8, WOOD, 3), C(50, 8, 3, "#90a4ae", O, 2),
        L("M14 74L12 80M88 64L86 70M90 84L88 90", "#4fc3f7", 3),
        P("M30 30Q22 34 18 50L12 76Q16 82 24 80L28 64V92H72V64L76 80Q84 82 88 76L82 50Q78 34 70 30Z", "#ffd600"),
        P("M34 32Q30 8 50 10Q70 8 66 32Q58 40 50 40Q42 40 34 32Z", "#ffca28"),
        P("M40 30Q40 18 50 18Q60 18 60 30Q56 34 50 34Q44 34 40 30Z", "#f9a825", O, 2.5),
        L("M50 40V92", O, 2.5),
        C(56, 54, 2.5, "#1e88e5", O, 1.5), C(56, 66, 2.5, "#1e88e5", O, 1.5), C(56, 78, 2.5, "#1e88e5", O, 1.5),
        R(32, 70, 12, 10, "#ffeb3b", 2, O, 2),
        HL(26, 48, 2, 7, 15), face(40, 56, 0.6)))

    # ---------------------------------------------------------------- Z
    # Zip bag with snacks
    K.add("Z", "Zip bag", "Snacks in my zip bag!", svg(
        P("M12 22H88V84Q88 92 80 92H20Q12 92 12 84Z", "#e1f5fe"),
        R(18, 56, 20, 20, "#ffb74d", 3, O, 2.5, rot=-15), dot(24, 62, 1.5, "#bf6f1f"), dot(32, 64, 1.5, "#bf6f1f"), dot(28, 70, 1.5, "#bf6f1f"),
        R(44, 62, 22, 20, "#ffb74d", 3, O, 2.5, rot=10), dot(50, 68, 1.5, "#bf6f1f"), dot(60, 70, 1.5, "#bf6f1f"), dot(55, 76, 1.5, "#bf6f1f"),
        P("M68 50L82 82L76 84Z", "#ff9800", O, 2.5), P("M68 50Q62 42 66 40Q72 44 70 50Z", GREEN, O, 2),
        C(32, 82, 4, "#e53935", O, 2), C(42, 84, 4, "#e53935", O, 2),
        P("M12 22H88V84Q88 92 80 92H20Q12 92 12 84Z", "none"),
        R(10, 14, 80, 10, "#ef5350", 3),
        L("M14 19H86", "#ffcdd2", 2),
        HL(20, 40, 2, 7, 10), face(50, 40, 0.85)))

    # Zebra rug: striped rug with a zebra face
    K.add("Z", "Zebra rug", "Stripy, just like a zebra!", svg(
        L("M8 32H2M8 40H2M8 48H2M8 56H2M8 64H2M8 72H2", O, 2.2),
        L("M92 32H98M92 40H98M92 48H98M92 56H98M92 64H98M92 72H98", O, 2.2),
        R(8, 26, 84, 52, "#fff", 8),
        P("M18 26Q24 40 16 52Q22 64 20 78H28Q32 64 26 52Q32 40 28 26Z", "#263238", O, 0),
        P("M72 26Q68 40 74 52Q68 64 72 78H80Q78 64 82 52Q76 40 82 26Z", "#263238", O, 0),
        P("M36 26Q40 32 36 38H44Q48 32 44 26Z", "#263238", O, 0),
        P("M56 26Q52 32 56 38H64Q60 32 64 26Z", "#263238", O, 0),
        P("M36 78Q40 72 36 66H44Q48 72 44 78Z", "#263238", O, 0),
        P("M56 78Q52 72 56 66H64Q60 72 64 78Z", "#263238", O, 0),
        R(8, 26, 84, 52, "none", 8),
        HL(14, 34, 1.5, 3, 40), blush(50, 56, 10, 3), face(50, 51, 0.8)))

    # Zoo blocks: toy blocks with a lion, a paw and a snake
    def block(x, y, s, col, inner):
        return (P(f"M{x} {y}L{x + s * 0.25} {y - s * 0.2}H{x + s * 1.25}L{x + s} {y}Z", col, O, 2.5)
                + P(f"M{x + s} {y}L{x + s * 1.25} {y - s * 0.2}V{y + s * 0.8}L{x + s} {y + s}Z", col, O, 2.5)
                + F(f"M{x + s} {y}L{x + s * 1.25} {y - s * 0.2}V{y + s * 0.8}L{x + s} {y + s}Z", "#000", ".18")
                + R(x, y, s, s, col, 3, O, 2.5) + inner)
    lion = (C(29, 74, 10, "#ff9800", O, 2) + C(29, 74, 6.5, GOLD, O, 2)
            + dot(27, 73, 1.3, O) + dot(31, 73, 1.3, O) + L("M27.5 77Q29 78.5 30.5 77", O, 1.3))
    paw = (E(71, 77, 6, 5, "#6d4c41", O, 0) + dot(64, 70, 2.4, "#6d4c41") + dot(69, 66, 2.4, "#6d4c41")
           + dot(74, 66, 2.4, "#6d4c41") + dot(79, 70, 2.4, "#6d4c41"))
    snake = (L("M38 40Q42 32 48 38Q54 44 60 36", "#43a047", 5) + dot(61, 35, 3.2, "#43a047") + dot(62, 34, 1, O))
    K.add("Z", "Zoo blocks", "Stack the zoo animals!", svg(
        block(12, 58, 34, "#ef5350", lion),
        block(54, 58, 34, "#42a5f5", paw),
        block(32, 22, 34, GOLD, snake),
        HL(16, 64, 1.5, 4, 0)))
