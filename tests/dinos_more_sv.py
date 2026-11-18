"""Dinosaurs S T U V (Spinosaurus, Styracosaurus, Triceratops, Therizinosaurus, Troodon, Utahraptor, Velociraptor)."""
from dinos_kit import *

IVORY = "#fff3d6"


def _feather(x, y, ln, wd, rot, fill, w=2.2):
    """Leaf-shaped feather from (x, y) pointing along angle rot (degrees)."""
    t = math.radians(rot)
    ex, ey = x + ln * math.cos(t), y + ln * math.sin(t)
    nx, ny = -math.sin(t) * wd, math.cos(t) * wd
    mx, my = x + ln * 0.5 * math.cos(t), y + ln * 0.5 * math.sin(t)
    return P(f"M{x:.1f} {y:.1f}Q{mx + nx:.1f} {my + ny:.1f} {ex:.1f} {ey:.1f}Q{mx - nx:.1f} {my - ny:.1f} {x:.1f} {y:.1f}Z", fill, O, w)


def _spike(cx, cy, r0, r1, ang, half, fill, w=2.4):
    """Triangle spike sticking out of a circle centre (cx, cy): base at radius r0, tip at r1."""
    a = math.radians(ang); h = math.radians(half)
    bx1, by1 = cx + r0 * math.cos(a - h), cy + r0 * math.sin(a - h)
    bx2, by2 = cx + r0 * math.cos(a + h), cy + r0 * math.sin(a + h)
    tx, ty = cx + r1 * math.cos(a), cy + r1 * math.sin(a)
    return P(f"M{bx1:.1f} {by1:.1f}L{tx:.1f} {ty:.1f}L{bx2:.1f} {by2:.1f}Z", fill, O, w)


def add_more(K):
    # ---------------- S: Spinosaurus - big sail, long crocodile snout, a fish
    ribs = "".join(L(f"M{x0} {y0}L{x1} {y1}", ORANGED, 2) for x0, y0, x1, y1 in
                   [(26, 54, 24, 36), (33, 50, 32, 26), (41, 49, 42, 19), (49, 49, 51, 20), (56, 50, 59, 30)])
    K.add("S", "Spinosaurus", "Spinosaurus has a big sail on its back!", svg(
        ground(44, 92, 36),
        P("M18 60Q16 34 32 20Q46 10 58 20Q68 30 66 54Z", ORANGE, O, 2.8),     # sail
        ribs,
        blob(BLUE,
             "M28 58Q12 58 2 74Q18 78 34 70Z",                # tail
             ell(42, 63, 23, 14, -8),                          # body
             ell(62, 50, 8, 12, 40),                           # neck
             "M56 41Q58 31 69 31L92 38Q98 41 96 46L72 50Q57 51 56 41Z",  # long croc head
             ell(36, 79, 6.5, 10), ell(52, 78, 6.5, 10),
             ell(38, 88, 9.5, 4), ell(55, 87, 9.5, 4)),
        belly(ell(46, 70, 14, 6, -8)),
        TL("M60 64Q67 66 69 71", BLUE, 3.5),                   # arm
        spots(BLUED, [(26, 62, 2.6), (34, 57, 2.2), (14, 68, 2)]),
        # fish in its mouth
        P("M88 64L81 75L96 74Z", YELLOW, O, 2.2),
        E(89, 57, 10, 5.8, YELLOW, O, 2.2, rot=80),
        L("M85.5 61Q89 59 93 61.5", YELLOWD, 1.8), L("M86 56Q89 54.5 92.5 56.5", YELLOWD, 1.8),
        dot(90.6, 50.8, 1.2, O),
        L("M70 46Q82 47 95 43", O, 2.2),
        P("M76 46.5L77.5 49.5L79 46.5Z", "#fff", O, 1.1),
        eye(67, 38, 4.2), nostril(92, 40), cheek(70, 44, 2.4)))

    # ---------------- S: Styracosaurus - frill crowned with long spikes, one big nose horn
    spikes = "".join(_spike(62, 43, 13.5, 30, a, 19, IVORY, 2.2) for a in (185, 211, 237, 263, 289))
    K.add("S", "Styracosaurus", "Styracosaurus has spikes on its frill and a big horn!", svg(
        ground(48, 92, 38),
        blob(ORANGE,
             "M22 58Q8 60 3 72Q14 75 26 70Z",                  # tail
             ell(42, 64, 25, 15),                              # body
             ell(28, 80, 6.5, 9.5), ell(40, 81, 6.5, 9.5), ell(55, 81, 6.5, 9.5), ell(66, 80, 6.5, 9.5)),
        belly(ell(44, 73, 15, 4.5)),
        spots(ORANGED, [(24, 60, 2.6), (34, 56, 3), (46, 56, 2.6), (40, 63, 2)]),
        spikes,
        C(62, 43, 14, RED, O, 2.8),                            # frill
        dot(62, 43, 8.5, "#ff8a80", ".7"),
        P("M83 46Q83 28 91 12Q97 30 94 47Z", IVORY, O, 2.6),  # big nose horn
        blob(ORANGE,
             ell(76, 52, 14, 11, 10),                          # head
             "M84 44Q97 47 97 56Q95 62 86 62Z"),               # beak
        F("M90 55L97 56Q95 62 88 61Z", BROWN),                 # beak tip
        smile(83, 58, 7), eye(76, 48, 4), nostril(92, 50), cheek(76, 56, 2.4)))

    # ---------------- T: Triceratops - three horns and a big frill
    K.add("T", "Triceratops", "Triceratops has three horns and a big frill!", svg(
        ground(48, 92, 38),
        blob(PURPLE,
             "M22 56Q8 60 3 72Q14 75 26 70Z",                  # tail
             ell(42, 64, 25, 15),
             ell(28, 80, 6.5, 9.5), ell(40, 81, 6.5, 9.5), ell(55, 81, 6.5, 9.5), ell(66, 80, 6.5, 9.5)),
        belly(ell(44, 73, 15, 4.5)),
        spots(PURPLED, [(22, 62, 2.4), (32, 56, 3), (44, 54, 2.6), (36, 63, 2)]),
        blob(ORANGE, circ(61, 42, 18),
             *[circ(61 + 18 * math.cos(math.radians(a)), 42 + 18 * math.sin(math.radians(a)), 3.6)
               for a in range(130, 400, 27)]),
        F(ell(61, 42, 12, 12), YELLOW),
        spots(ORANGE, [(55, 36, 2.2), (61, 33, 2.2), (54, 45, 2), (67, 37, 2)]),
        P("M68 42Q73 22 86 11Q81 26 75 45Z", "#f1e3c2", O, 2.4),       # far brow horn
        blob(PURPLE,
             ell(73, 52, 14, 11, 10),
             "M81 44Q93 47 93 56Q91 62 82 62Z"),
        P("M72 43Q79 23 93 13Q88 29 79 46Z", IVORY, O, 2.6),          # near brow horn
        P("M84 48Q85 40 89 34Q92 42 90 49Z", IVORY, O, 2.2),          # nose horn
        smile(79, 58, 7), eye(72, 49, 4.2), nostril(88, 51), cheek(72, 57, 2.5)))

    # ---------------- T: Therizinosaurus - giant claws, pot belly, fluffy
    tufts = "".join(_feather(x, y, ln, 6, r, PURPLE) for x, y, ln, r in
                    [(10, 78, 10, 190), (12, 75, 10, 215), (26, 50, 10, 215), (34, 44, 10, 235), (44, 41, 10, 255),
                     (52, 38, 10, 215), (56, 30, 10, 215), (63, 20, 9, 240)])
    claws = "".join(P(d, IVORY, O, 2.3) for d in [
        "M61 66Q84 60 90 80Q82 70 63 70Z",
        "M61 67Q80 68 82 88Q76 76 61 71Z",
        "M60 68Q71 76 71 91Q66 80 58 71Z"])
    K.add("T", "Therizinosaurus", "Therizinosaurus has very long claws!", svg(
        ground(44, 92, 36),
        tufts,
        blob(PINK,
             "M28 66Q16 66 7 78Q20 84 34 76Z",                 # tail
             ell(40, 62, 20, 21),                               # pot belly
             ell(58, 40, 8, 16, 30),                            # neck
             ell(70, 25, 11, 9, 10),                            # head
             "M76 19Q91 21 91 28Q89 32 78 32Z",                 # beak
             ell(34, 82, 7, 7), ell(48, 82, 7, 7),
             ell(35, 88, 9.5, 4), ell(50, 88, 9.5, 4)),
        belly(ell(42, 68, 13, 13)),
        _feather(52, 52, 17, 6.5, 100, PURPLE),                 # arm feathers
        TL("M52 50Q53 62 62 67", PINK, 6),                      # arm
        claws,
        C(61.5, 67.5, 3.6, PINK, O, 2.2),                       # hand
        L("M78 28Q84 30 90 28", O, 2), eye(70, 22, 3.8), nostril(88, 23), cheek(74, 29, 2.2)))

    # ---------------- T: Troodon - small clever dinosaur with big eyes
    K.add("T", "Troodon", "Troodon has big eyes to see in the dark!", svg(
        ground(48, 92, 34),
        _feather(12, 48, 10, 3.5, 200, TEALD), _feather(13, 52, 10, 3.5, 172, TEALD),
        blob(TEAL,
             "M38 52Q22 46 10 46Q12 58 38 66Z",                 # tail
             ell(46, 59, 17, 12, -15),                          # body
             ell(62, 46, 6, 11, 35),                            # neck
             ell(74, 34, 14, 12),                               # big head
             "M80 30Q96 32 96 38Q95 43 82 43Z",                 # snout
             ell(46, 70, 7, 9),                                 # thigh
             ell(40, 80, 3.6, 8, -10), ell(50, 80, 3.6, 8, 10),
             ell(38, 88, 7.5, 3), ell(54, 88, 7.5, 3)),
        belly(ell(52, 64, 9, 5, -15), LIME),
        _feather(58, 58, 11, 3.5, 75, TEALD),                   # arm feathers
        TL("M57 56Q63 60 65 65", TEAL, 3),                      # little arm
        spots(TEALD, [(36, 56, 2.4), (44, 51, 2.2), (26, 54, 2)]),
        L("M82 40Q88 41 94 39", O, 2),
        eye(76, 31, 6.6), nostril(93, 34), cheek(83, 38, 2.4)))

    # ---------------- U: Utahraptor - big feathered raptor, sickle toe claw
    K.add("U", "Utahraptor", "Utahraptor has a big claw on its toe!", svg(
        ground(46, 92, 36),
        _feather(11, 45, 10, 3.5, 195, ORANGE), _feather(12, 49, 10, 3.5, 168, ORANGE),
        _feather(62, 20, 10, 3.5, 210, ORANGE), _feather(64, 24, 10, 3.5, 185, ORANGE),
        blob(BROWN,
             "M36 48Q20 42 9 42Q10 54 34 62Z",                   # tail
             ell(44, 56, 18, 13, -15),                          # body
             ell(62, 42, 7, 12, 30),                            # neck
             "M60 30Q61 18 74 18Q91 19 95 28Q96 35 86 36L67 37Q60 36 60 30Z",  # head
             ell(42, 66, 9, 11),                                # thigh
             ell(36, 80, 4.5, 9, -10), ell(48, 80, 4.5, 9, 10),
             ell(34, 88, 8, 3.5), ell(54, 88, 8, 3.5)),
        belly(ell(50, 62, 10, 6, -15), SAND),
        P("M52 86Q51 73 63 73Q66 75 65 80Q61 76 58 78Q56 81 57 86Z", IVORY, O, 2.2),   # sickle claw
        _feather(55, 47, 19, 6, 58, ORANGE),                    # feathery arm
        P("M64 62L68 67L64.5 66Z", IVORY, O, 1.6),
        spots(BROWND, [(34, 50, 2.6), (42, 46, 2.4), (24, 48, 2), (50, 50, 2)]),
        L("M70 33Q82 34 94 30", O, 2.2),
        P("M78 33.5L79.5 36.5L81 33.5Z", "#fff", O, 1.1),
        eye(71, 25, 4.4), nostril(91, 25), cheek(74, 31, 2.4)))

    # ---------------- V: Velociraptor - small feathered raptor, running
    K.add("V", "Velociraptor", "Velociraptor can run very fast!", svg(
        ground(48, 92, 34),
        L("M6 60L16 60", GREY, 2.4), L("M3 68L13 68", GREY, 2.4), L("M8 84L16 84", GREY, 2.4),   # speed lines
        _feather(14, 41, 10, 3.5, 200, YELLOW), _feather(15, 45, 10, 3.5, 172, YELLOW),
        _feather(68, 28, 9, 3, 215, YELLOW),
        blob(RED,
             "M34 46Q22 41 12 39Q12 51 34 58Z",                   # tail
             ell(48, 52, 17, 11, -8),                           # body
             ell(65, 43, 6.5, 10, 55),                          # neck
             "M66 34Q68 26 78 26Q92 27 96 34Q96 40 88 41L72 42Q66 41 66 34Z",  # head
             ell(50, 61, 8.5, 9),                               # thigh
             ell(59, 73, 4, 10, -32), ell(66, 86, 8, 3.2),    # front leg (forward)
             ell(38, 72, 3.8, 10, 50), ell(28, 76, 7, 3, -30)),  # back leg (kicked back)
        belly(ell(54, 57, 10, 5, -8), YELLOW),
        P("M29 75Q22 64 32 59Q29 66 34 73Z", IVORY, O, 2.2),     # sickle claw
        _feather(58, 50, 13, 4, 35, YELLOW),                    # feathery arm
        spots(REDD, [(40, 47, 2.4), (48, 45, 2.2), (28, 46, 2), (56, 47, 1.8)]),
        L("M74 38Q84 39 94 36", O, 2.2),
        eye(76, 32, 4), nostril(93, 31), cheek(78, 37, 2.2)))
