"""Dinosaurs E, G, H, I, K, L, M."""
from dinos_kit import *

WAVE = "#90caf9"
BILL = "#ffe9a8"


def _seg(x1, y1, r1, x2, y2, r2):
    """Tapered limb segment as blob pieces (two circles + joining quad)."""
    dx, dy = x2 - x1, y2 - y1
    ln = math.hypot(dx, dy) or 1
    nx, ny = -dy / ln, dx / ln
    pts = [(x1 + nx * r1, y1 + ny * r1), (x2 + nx * r2, y2 + ny * r2),
           (x2 - nx * r2, y2 - ny * r2), (x1 - nx * r1, y1 - ny * r1)]
    return [circ(x1, y1, r1), circ(x2, y2, r2), poly_path(pts)]


def _waves(pts):
    out = ""
    for x, y in pts:
        out += L(f"M{x} {y}Q{x + 4} {y - 3} {x + 8} {y}Q{x + 12} {y + 3} {x + 16} {y}", WAVE, 2.4)
    return out


def _bubbles(pts):
    return "".join(C(x, y, r, "#e3f2fd", WAVE, 1.6) for x, y, r in pts)


def _tri(x, y, ang, h, w, fill, sw=2.2):
    """Spike with base centre (x, y), pointing at angle ang (deg), height h, base width w."""
    a = math.radians(ang)
    ux, uy = math.cos(a), math.sin(a)
    px, py = -uy, ux
    pts = [(x + px * w / 2, y + py * w / 2), (x + ux * h, y + uy * h), (x - px * w / 2, y - py * w / 2)]
    return P(poly_path(pts), fill, O, sw)


def _cloud(x, y):
    parts = [(x - 8, y + 1, 5), (x - 1, y - 3, 7), (x + 7, y, 5.5), (x, y + 3, 6)]
    return ("".join(C(a, b, r, "#e3eef5", "#e3eef5", 4) for a, b, r in parts)
            + "".join(dot(a, b, r, "#fff") for a, b, r in parts))


def add_more(K):
    # ---------------------------------------------------------------- E
    # Edmontosaurus - big duck-billed plant eater with a long flat bill
    K.add("E", "Edmontosaurus", "Edmontosaurus has a flat bill like a duck!", svg(
        ground(50, 92, 40),
        blob(GREEN,
             "M30 52Q14 50 2 58Q14 68 32 66Z",
             ell(44, 60, 22, 15, -8),
             ell(66, 46, 8, 12, 40),
             ell(76, 35, 11, 8.5, -8),
             ell(37, 75, 8, 12), ell(51, 77, 6.5, 10),
             *_seg(63, 62, 4.5, 67, 84, 3.2),
             ell(40, 87, 10, 4.5), ell(54, 88, 8, 3.5), ell(70, 87, 6, 3)),
        P("M81 29Q97 26 98 34Q98 42 83 42Q80 36 81 29Z", BILL),
        belly(ell(46, 67, 15, 7, -8)),
        spots(GREEND, [(30, 56, 3), (40, 50, 2.6), (50, 52, 2.2), (18, 58, 2), (60, 54, 2)]),
        smile(90, 38, 8), eye(74, 31, 4), nostril(94, 31), cheek(76, 39, 2.6)))

    # Euoplocephalus - armoured tank: spike rows, eyelid armour, club tail
    top = []
    for i in range(9):
        a = math.radians(200 + i * 17.5)
        x, y = 52 + 26 * math.cos(a), 63 + 17 * math.sin(a)
        top.append(_tri(x, y, math.degrees(math.atan2(math.sin(a) * 26, math.cos(a) * 17)), 9.5, 6.5, YELLOW))
    studs = ""
    for row, (ry, n, x0, dx) in enumerate([(54, 4, 40, 9), (64, 5, 34, 9)]):
        for k in range(n):
            x = x0 + k * dx
            yy = ry + 0.01 * (x - 52) ** 2
            studs += E(f"{x:g}", f"{yy:.1f}", 3.2, 2.4, PURPLED, O, 1.6) + dot(f"{x - 0.8:g}", f"{yy - 0.8:.1f}", 0.9, "#fff", ".6")
    K.add("E", "Euoplocephalus", "Euoplocephalus has spiky armour and a club tail!", svg(
        ground(50, 92, 42),
        "".join(top),
        _tri(80, 59, -120, 6, 5, YELLOW), _tri(86, 58, -70, 5, 4.5, YELLOW),
        blob(PURPLE,
             "M32 60Q20 61 12 60L13 67Q22 70 34 70Z",
             ell(52, 63, 26, 17),
             ell(76, 67, 8, 7),
             ell(85, 66, 10, 8),
             ell(34, 79, 6, 9), ell(45, 81, 6, 9), ell(59, 81, 6, 9), ell(70, 79, 6, 9)),
        blob(PURPLED, ell(10, 59.5, 6.5, 5.2), ell(10, 66.5, 6.5, 5.2)),
        HL(8, 58, 2.4, 1.3), HL(8, 65, 2.4, 1.3),
        belly(ell(52, 73, 17, 4)),
        studs,
        smile(90, 70, 6), eye(86, 63, 3.4),
        P("M82 61.8Q86 55.5 90.2 61.5Q86 59.6 82 61.8Z", PURPLED, O, 1.8),
        nostril(93.5, 64), cheek(85, 70, 2.2)))

    # Elasmosaurus - super long neck, four flippers, swimming
    K.add("E", "Elasmosaurus", "Elasmosaurus has a super long neck!", svg(
        _waves([(2, 40), (22, 32), (44, 92), (66, 88), (6, 92)]),
        _bubbles([(70, 6, 2), (64, 12, 1.5), (50, 46, 2.2), (56, 40, 1.4)]),
        P("M48 70Q60 72 66 80Q58 82 46 76Z", TEALD),
        P("M24 74Q30 82 30 90Q24 88 18 78Z", TEALD),
        blob(TEAL,
             "M16 64Q6 63 2 70Q10 74 18 74Z",
             ell(32, 68, 20, 12),
             "M40 59Q56 54 64 40Q71 27 80 18L87 24Q79 32 73 44Q65 62 48 72Z",
             ell(87, 18, 9, 6.5, -5)),
        P("M40 74Q50 76 56 86Q48 88 36 78Z", TEAL),
        P("M16 74Q20 82 18 92Q12 88 10 76Z", TEAL),
        belly(ell(32, 74, 14, 4)),
        spots(TEALD, [(24, 62, 2.6), (34, 60, 3), (44, 64, 2.2), (66, 42, 1.8), (74, 30, 1.6)]),
        smile(91, 21, 5), eye(87, 15.5, 3.2), nostril(94.5, 16), cheek(85, 21, 2)))

    # ---------------------------------------------------------------- G
    # Gallimimus - fast ostrich-like runner
    K.add("G", "Gallimimus", "Gallimimus runs super fast like an ostrich!", svg(
        ground(50, 92, 32),
        L("M3 62L16 62", GREY, 2.5), L("M6 70L20 70", GREY, 2.5), L("M2 78L12 78", GREY, 2.5),
        blob(YELLOW,
             "M36 38Q18 32 2 28Q12 44 36 52Z",
             ell(46, 45, 17, 11, -12),
             "M54 37Q66 30 71 17L80 19Q77 34 62 48Z",
             ell(79, 15, 8, 5.8, -5),
             "M84 11Q97 14 96 17Q90 21 82 20Z",
             *_seg(50, 50, 7, 59, 64, 4), *_seg(59, 64, 3.6, 61, 78, 2.6), *_seg(61, 78, 2.6, 71, 86, 2),
             *_seg(41, 52, 7, 40, 66, 4), *_seg(40, 66, 3.6, 28, 74, 2.6), *_seg(28, 74, 2.6, 22, 82, 2)),
        TL("M60 46Q66 50 66 55", YELLOW, 3),
        L("M65.5 56L64 59M66.5 56L67 59.5", O, 1.6),
        belly(ell(48, 51, 11, 4.5, -12)),
        spots(YELLOWD, [(36, 42, 2.4), (44, 39, 2.6), (52, 39, 2), (22, 38, 1.8)]),
        smile(89, 17, 5), eye(78, 13, 3.2), cheek(81, 18, 2)))

    # Giganotosaurus - giant (friendly) meat-eater with stripes
    stripes = "".join(F(d, REDD) for d in [
        "M24 50Q26 54 22 58L19 56Q22 53 21 50Z", "M33 44Q36 49 32 54L29 52Q32 48 30 45Z",
        "M43 42Q46 47 42 52L39 50Q42 46 40 43Z", "M53 42Q56 47 52 52L49 50Q52 46 50 43Z",
        "M13 54Q15 57 12 60L9 59Q12 56 10 54Z"])
    K.add("G", "Giganotosaurus", "Giganotosaurus is a giant dinosaur with a big smile!", svg(
        ground(48, 92, 38),
        blob(RED,
             "M32 46Q14 44 2 56Q16 62 36 62Z",
             ell(44, 57, 22, 15, -8),
             ell(63, 45, 9, 12, 40),
             "M57 31Q59 18 76 18Q93 18 97 30Q98 41 86 43L64 43Q57 41 57 31Z",
             ell(36, 75, 8, 12), ell(53, 75, 8, 12),
             ell(39, 87, 10, 4.5), ell(57, 87, 10, 4.5)),
        P("M66 21Q71 16 77 20Q71 20 66 23Z", REDD, O, 1.8),
        belly(ell(49, 64, 14, 8, -10)),
        stripes,
        TL("M64 57Q71 58 73 63", RED, 3.5),
        L("M66 37Q80 41 95 35", O, 2.2),
        P("M74 39.5L76 43L78 40Z", "#fff", O, 1.2), P("M84 39.3L86 42.3L88 38.6Z", "#fff", O, 1.2),
        eye(71, 26, 4.4), nostril(93, 26), cheek(80, 33)))

    # ---------------------------------------------------------------- H
    # Hadrosaurus - duck-billed plant eater munching leaves
    leaves = "".join(E(x, y, 6, 3.2, c, O, 2, rot=r) for x, y, c, r in [
        (64, 14, GREEN, -25), (76, 13.5, LIME, 20), (87, 14, GREEN, -15), (82, 5, LIME, -30), (95, 6, GREEN, 30)])
    K.add("H", "Hadrosaurus", "Hadrosaurus loves to munch on leaves!", svg(
        ground(42, 92, 36),
        TL("M56 11Q76 8 99 11", BROWND, 3.5),
        leaves,
        blob(PINK,
             "M28 62Q12 70 2 86Q18 84 34 74Z",
             ell(42, 60, 19, 15, -25),
             ell(56, 42, 8, 13, 25),
             ell(66, 28, 10.5, 8, -15),
             ell(40, 76, 9, 12), ell(50, 78, 6, 10),
             ell(44, 88, 10, 4), ell(55, 88, 7, 3)),
        P("M71 22Q86 16 89 23Q91 30 77 33Q72 28 71 22Z", BILL),
        E(91, 25, 6, 3, GREEN, O, 2, rot=-35), L("M86 28L95 22", GREEND, 1.4),
        belly(ell(46, 66, 11, 9, -25)),
        TL("M57 57Q62 59 64 63", PINK, 3.5),
        spots("#e57fa5", [(30, 56, 2.6), (38, 48, 2.4), (24, 66, 2), (46, 50, 1.8)]),
        smile(81, 29, 6), eye(64, 25, 3.8), nostril(85, 22), cheek(67, 32, 2.4)))

    # ---------------------------------------------------------------- I
    # Iguanodon - big thumb spike
    K.add("I", "Iguanodon", "Iguanodon has a spiky thumb!", svg(
        ground(44, 92, 36),
        blob(ORANGE,
             "M28 60Q12 68 2 84Q18 84 34 72Z",
             ell(42, 60, 19, 15, -20),
             ell(58, 44, 8, 13, 30),
             ell(70, 31, 13, 8.5, -8),
             ell(38, 76, 8, 12), ell(50, 78, 6, 10),
             ell(42, 88, 10, 4), ell(55, 88, 7, 3)),
        TL("M56 60Q64 63 71 60", ORANGE, 4.5),
        P("M70 55Q71 46 74.5 38Q78.5 46 79.5 55Z", "#fff8e1", O, 2.6),
        C(74.5, 58, 5.5, ORANGE, O, 2.6),
        L("M79 60L82.5 61.5M78 63L81 65.5", O, 1.8),
        belly(ell(46, 66, 11, 9, -20)),
        spots(ORANGED, [(30, 56, 2.6), (38, 48, 2.4), (24, 66, 2), (46, 50, 1.8)]),
        smile(78, 35, 7), eye(69, 28, 3.8), nostril(80, 27), cheek(70, 35, 2.4)))

    # Ichthyosaurus - dolphin-shaped swimmer with a big eye
    K.add("I", "Ichthyosaurus", "Ichthyosaurus swims like a dolphin!", svg(
        _waves([(4, 14), (60, 8), (50, 90), (10, 88)]),
        _bubbles([(92, 34, 2.2), (88, 28, 1.5), (95, 24, 1.2)]),
        P("M40 62Q38 74 30 80Q28 70 32 62Z", GREYD),
        blob(GREY,
             "M40 41Q46 24 58 39Z",
             "M26 46Q16 49 10 52Q16 55 26 60Z",
             "M13 52Q7 40 3 28Q16 36 18 50Q17 64 4 76Q8 62 13 52Z",
             ell(46, 52, 28, 14, -3),
             "M68 44Q88 44 98 49Q90 56 70 59Z"),
        P("M56 60Q60 74 52 82Q48 74 50 62Z", GREY),
        belly("M24 57Q46 66 72 58Q60 64 46 65Q32 64 24 57Z", "#e8eef2"),
        spots(GREYD, [(30, 48, 2), (38, 44, 2.4), (48, 42, 2)]),
        L("M78 53Q88 54 94 50.5", O, 2), cheek(70, 55, 2.6),
        eye(66, 47, 6.2)))

    # ---------------------------------------------------------------- K
    # Kentrosaurus - plates in front turning into long spikes at the back
    kp = ""
    for x, h, w, kind in [(65, 11, 5.5, 0), (57, 13, 6, 0), (49, 14, 6, 0), (41, 15, 4.4, 1),
                          (33, 17, 4, 1), (25, 16, 3.6, 1), (17, 14, 3.4, 1)]:
        if x > 28:
            yb = 64 - 14 * math.sqrt(max(0.0, 1 - ((x - 46) / 24) ** 2)) + 2.5
        else:
            yb = 59 - (28 - x) * 6 / 26 + 2
        if kind == 0:
            kp += P(f"M{x - w} {yb:.1f}Q{x - w} {yb - h:.1f} {x} {yb - h:.1f}Q{x + w} {yb - h * 0.6:.1f} {x + w} {yb:.1f}Z", ORANGE, O, 2.4)
        else:
            kp += _tri(x, yb, -100 - (40 - x) * 1.0 if x < 40 else -100, h, w * 2, ORANGE, 2.4)
    K.add("K", "Kentrosaurus", "Kentrosaurus has lots and lots of spikes!", svg(
        ground(50, 92, 40),
        kp,
        blob(LIME,
             "M28 59Q12 57 2 53Q10 70 30 72Z",
             ell(46, 64, 24, 14),
             ell(76, 66, 8, 6.5, -15),
             ell(86, 63, 9, 7),
             ell(31, 79, 6, 10), ell(41, 80, 6, 10), ell(55, 80, 6, 10), ell(65, 79, 6, 10)),
        belly(ell(48, 72, 15, 4)),
        _tri(36, 66, 160, 15, 7, ORANGE, 2.4),
        spots(GREEND, [(38, 58, 2.6), (48, 55, 3), (58, 58, 2.6), (20, 61, 2)]),
        smile(89, 67, 6), eye(87, 60, 3.3), nostril(93.5, 61), cheek(83, 66, 2.2)))

    # ---------------------------------------------------------------- L
    # Lambeosaurus - duckbill with a hatchet-shaped head crest
    K.add("L", "Lambeosaurus", "Lambeosaurus has a crest on its head like an axe!", svg(
        ground(46, 92, 38),
        P("M66 28L64 11Q65 4 73 4L84 7Q89 10 86 17L79 28Z", ORANGE, O, 2.6),
        P("M66 24L53 19L60 30Z", ORANGE, O, 2.4),
        blob(PURPLE,
             "M28 60Q12 66 2 80Q18 80 34 72Z",
             ell(42, 60, 19, 15, -20),
             ell(58, 44, 8, 13, 30),
             ell(71, 32, 10, 8, -8),
             ell(38, 76, 8, 12), ell(50, 78, 6, 10),
             ell(42, 88, 10, 4), ell(55, 88, 7, 3)),
        P("M76 27Q91 23 93 30Q94 37 79 38Q75 33 76 27Z", BILL),
        F("M68 10Q70 7 76 7.5Q72 9 69 13Z", "#fff", ".5"),
        TL("M57 59Q62 61 64 65", PURPLE, 3.5),
        belly(ell(46, 66, 11, 9, -20)),
        spots(PURPLED, [(30, 56, 2.6), (38, 48, 2.4), (24, 66, 2), (46, 50, 1.8)]),
        smile(85, 34, 6), eye(70, 29, 3.8), nostril(89, 28), cheek(72, 36, 2.4)))

    # ---------------------------------------------------------------- M
    # Maiasaura - mother duckbill with a baby hatching in the nest
    K.add("M", "Maiasaura", "Maiasaura is a good mummy who looks after her babies!", svg(
        ground(46, 92, 44),
        blob(YELLOW,
             "M22 52Q8 52 2 62Q12 68 24 66Z",
             ell(34, 58, 19, 14, -10),
             ell(50, 44, 7.5, 12, 35),
             ell(59, 33, 9.5, 7.5, 15),
             ell(28, 74, 7, 11), ell(40, 76, 6, 10),
             *_seg(48, 64, 4, 51, 84, 3),
             ell(31, 87, 9, 4), ell(43, 88, 7, 3), ell(54, 87, 5.5, 3)),
        P("M62 31Q73 31 75 38Q75 44 66 41Q61 37 62 31Z", BILL),
        P("M55 27Q58 22 62 26Z", YELLOWD, O, 1.8),
        belly(ell(38, 65, 12, 6, -10)),
        spots(YELLOWD, [(24, 54, 2.6), (32, 48, 2.4), (14, 58, 2), (40, 52, 2)]),
        smile(70, 39, 5), eye(58, 30, 3.5), nostril(72, 34), cheek(59, 36, 2.2),
        E(69, 79, 4.5, 6, "#fff", O, 2.2), E(91, 79, 4.5, 6, "#fff", O, 2.2),
        blob(LIME, circ(80, 70, 6), ell(80, 78, 5, 5)),
        eye(81.5, 68.5, 2.4), smile(84, 73, 3.5), cheek(78, 73, 1.6),
        P("M74 76L76 79L78 76L80 79L82 76L84 79L86 76Q87 88 80 88Q73 88 74 76Z", "#fff", O, 2.2),
        P("M60 84Q60 92 80 92Q100 92 99 84Q90 80 80 85Q70 80 60 84Z", BROWN, O, 2.4),
        L("M63 87L72 86M76 89L86 88M88 86L96 87", BROWND, 1.6)))

    # Mosasaurus - huge sea lizard with a tail fin and paddles
    K.add("M", "Mosasaurus", "Mosasaurus is a giant sea lizard!", svg(
        _waves([(6, 12), (52, 8), (40, 92), (72, 88)]),
        _bubbles([(96, 38, 2), (92, 32, 1.4)]),
        P("M64 60Q72 70 72 80Q64 76 58 64Z", GREEND),
        P("M30 60Q32 70 28 78Q22 72 24 62Z", GREEND),
        blob(GREEN,
             "M26 48Q14 50 6 54Q14 60 26 62Z",
             "M9 55Q4 44 3 34Q12 42 14 54Z",
             "M9 55Q6 70 2 80Q16 72 16 57Z",
             ell(46, 54, 25, 13, -3),
             "M64 44Q80 39 95 46Q99 52 95 57Q80 61 64 61Z"),
        P("M56 62Q64 74 62 84Q54 80 50 64Z", GREEN),
        P("M24 62Q24 72 18 80Q14 72 18 62Z", GREEN),
        belly("M24 59Q46 68 70 60Q86 59 94 56Q80 62 64 63Q40 70 24 59Z", LIME),
        spots(GREEND, [(28, 48, 2.4), (38, 44, 3), (50, 43, 3), (60, 44, 2.4), (16, 52, 1.8)]),
        L("M72 54Q84 56 96 51", O, 2.2),
        P("M78 54.5L80 58L82 55Z", "#fff", O, 1.2), P("M87 54.3L89 57.3L91 53.6Z", "#fff", O, 1.2),
        eye(78, 47, 3.8), nostril(94, 48), cheek(74, 55, 2.4)))

    # Microraptor - little gliding dino with feathered wings on arms and legs
    def wing(d, fill, w=2.4):
        return P(d, fill, O, w)
    fwing = "M58 46Q54 26 36 12Q34 18 39 21Q31 22 35 27Q27 28 32 33Q25 35 31 39Q28 44 36 46Q44 50 54 50Z"
    hwing = "M42 54Q36 66 20 78Q22 72 26 70Q18 70 22 66Q15 64 21 61Q16 57 24 56Q32 52 42 52Z"
    K.add("M", "Microraptor", "Microraptor has four feathery wings and can glide!", svg(
        _cloud(84, 84),
        T("translate(8 -4)", wing(fwing, PURPLED)),
        T("translate(8 4)", wing(hwing, PURPLED)),
        blob(BLUE,
             "M34 47Q18 50 4 56Q18 58 36 56Z",
             ell(48, 50, 15, 8, -8),
             ell(62, 44, 6, 6, -30),
             ell(71, 39, 8, 6.5, -10),
             "M75 37Q86 37 88 40Q84 44 75 43Z"),
        P("M14 52Q4 50 2 54Q4 60 14 58Q8 55 14 52Z", BLUED, O, 2.2),
        P("M66 34Q64 28 68 30Q68 26 72 31Z", BLUED, O, 1.8),
        wing(fwing, BLUED),
        wing(hwing, BLUED),
        L("M50 44Q44 32 38 24M46 46Q38 38 32 32", "#90caf9", 1.6),
        L("M38 55Q32 62 26 66", "#90caf9", 1.6),
        belly(ell(50, 54, 9, 2.6, -8)),
        smile(80, 42, 4.5), eye(71, 37, 3.2), cheek(73, 42, 1.8)))

    # Megalosaurus - classic two-legged meat-eater with a long snout and 3-fingered arms
    K.add("M", "Megalosaurus", "Megalosaurus walks on two big legs!", svg(
        ground(48, 92, 38),
        TL("M58 56Q66 64 72 64", ORANGED, 3.5),
        blob(ORANGE,
             "M30 44Q14 40 2 46Q14 58 34 58Z",
             ell(44, 54, 20, 13, -6),
             ell(61, 44, 8, 10, 45),
             "M60 34Q61 24 72 24Q86 24 97 32Q99 40 90 41L68 43Q60 41 60 34Z",
             ell(38, 70, 8, 11, 15), *_seg(36, 76, 5, 30, 86, 3.6),
             ell(52, 70, 8, 11, -15), *_seg(55, 76, 5, 60, 86, 3.6),
             ell(28, 87, 7, 3.5), ell(63, 87, 8, 3.5)),
        belly(ell(48, 60, 12, 6, -6)),
        TL("M60 58Q68 66 75 64", ORANGE, 3.5),
        L("M75 61L80 59M76 64L81 64M75 67L79 69", O, 2),
        spots(ORANGED, [(30, 48, 2.6), (40, 44, 2.6), (50, 44, 2.2), (16, 46, 2)]),
        L("M68 37Q82 40 96 36", O, 2.2),
        P("M78 38.8L80 42L82 38.5Z", "#fff", O, 1.2),
        eye(70, 30, 4), nostril(95, 31), cheek(76, 34, 2.4)))
