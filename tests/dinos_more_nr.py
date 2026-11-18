"""Dinosaurs N O P Q R."""
from dinos_kit import *

WATER = "#b3e5fc"
WING_PINK = "#fcd3e1"


def _top(cx, cy, rx, ry, x):
    """y of the top edge of an axis-aligned ellipse at x."""
    t = max(0.0, 1 - ((x - cx) / rx) ** 2)
    return cy - ry * math.sqrt(t)


def _waves(rows):
    out = ""
    for x0, y, n in rows:
        d = f"M{x0} {y}" + "".join(f"q4 -3 8 0" for _ in range(n))
        out += L(d, SEA, 2.2)
    return out


def _bubbles(pts):
    return "".join(C(x, y, r, "#fff", SEA, 1.6) for x, y, r in pts)


def _cloud(cx, cy, s=1.0):
    return blob("#fff", ell(cx, cy, 14 * s, 6 * s), circ(cx - 6 * s, cy - 4 * s, 6 * s),
                circ(cx + 5 * s, cy - 5 * s, 7 * s), w=2)


def add_more(K):
    # N: Nodosaurus - armoured, bumpy back, side spikes, no tail club
    bx, by, brx, bry = 48, 63, 29, 16
    bumps = [circ(x, _top(bx, by, brx, bry, x) + 1.5, 3.6) for x in (25, 33, 41, 49, 57, 65, 72)]
    side_spikes = "".join(P(f"M{x - 3.8} {y - 1}L{x + dx} {y + dy}L{x + 3.8} {y + 1}Z", SAND, O, 2.2)
                          for x, y, dx, dy in [(20, 69, -10, 5), (36, 75, 0, 10), (50, 76.5, 0, 10), (63, 75, 0, 10), (72, 58, 7, -9)])
    armour = "".join(C(x, y, r, BROWND, O, 1.6) for x, y, r in
                     [(28, 62, 2.6), (37, 57, 2.8), (47, 55, 2.8), (57, 56, 2.8), (66, 61, 2.6),
                      (32, 69, 2.2), (42, 65, 2.4), (52, 64, 2.4), (62, 67, 2.2)])
    K.add("N", "Nodosaurus", "Nodosaurus is bumpy like a turtle!", svg(
        ground(50, 92, 40),
        blob(BROWN,
             "M24 60Q10 64 3 74Q14 77 28 72Z",                 # tail, no club
             ell(bx, by, brx, bry), *bumps,                    # armoured body
             ell(76, 67, 9, 7, -10),                            # neck
             ell(86, 69, 10, 7.5),                              # head
             ell(30, 81, 6, 8), ell(42, 82, 6, 8), ell(58, 82, 6, 8), ell(68, 81, 6, 8),
             ell(31, 88, 8, 3.5), ell(43, 88.5, 8, 3.5), ell(59, 88.5, 8, 3.5), ell(69, 88, 8, 3.5)),
        armour,
        L("M21 72Q48 80 75 71", O, 2),                          # edge of the shell
        side_spikes,
        smile(90, 72, 6), eye(86, 66, 3.4), cheek(83, 72, 2.2), nostril(94, 67)))

    # O: Oviraptor - parrot beak, round crest, feathers, holding an egg
    tail_feathers = "".join(E(x, y, 9, 4, PURPLED, O, 2.2, rot=r) for x, y, r in
                            [(10, 40, -30), (8, 50, 0), (12, 58, 25)])
    K.add("O", "Oviraptor", "Oviraptor hugs its egg!", svg(
        ground(48, 92, 34),
        tail_feathers,
        P("M66 24Q65 9 76 10Q86 12 83 26Z", ORANGE, O, 2.5),     # round head crest
        blob(PURPLE,
             "M32 50Q20 46 10 48Q14 58 34 64Z",                 # feathery tail
             ell(42, 60, 19, 15, -12),                          # body
             ell(60, 44, 8, 14, 28),                            # neck
             ell(72, 30, 10, 9),                                # head
             ell(38, 76, 5, 10), ell(50, 77, 5, 10),            # legs
             ell(41, 88, 8, 3.5), ell(54, 88, 8, 3.5)),
        P("M79 24Q92 22 92 34Q91 40 84 39Q86 33 80 33Z", YELLOW, O, 2.5),   # parrot beak
        belly(ell(46, 66, 11, 7, -12), "#d1c4e9"),
        L("M24 52l3 3 3 -3M32 48l3 3 3 -3M40 46l3 3 3 -3", PURPLED, 2),     # feathers
        E(68, 69, 8.5, 11, "#fff8e1", O, 2.5),                  # egg
        spots(SEA, [(65, 65, 1.6), (71, 72, 1.8), (66, 75, 1.3)]),
        TL("M54 55Q56 68 64 76", PURPLE, 4.5),                  # arm hugging the egg
        P("M54 56l-2 5 5 -2Z", PURPLED, O, 1.5),
        HL(65, 64, 2, 3.5),
        eye(71, 28, 3.8), cheek(75, 35, 2.4), nostril(88, 28)))

    # O: Ouranosaurus - duckbill-ish plant eater with a low sail
    ribs = "".join(L(f"M{x} {_top(45, 63, 25, 14, x) + 2:.1f}L{x + d} {y}", REDD, 1.8)
                   for x, y, d in [(30, 46, -2), (38, 40, -1), (46, 38, 0), (54, 40, 1), (61, 46, 2)])
    K.add("O", "Ouranosaurus", "Ouranosaurus has a sail on its back!", svg(
        ground(50, 92, 40),
        P("M20 60Q20 40 44 36Q64 36 68 56Z", RED, O, 2.5),     # low sail
        ribs,
        blob(GREEN,
             "M26 58Q10 60 3 70Q14 74 30 70Z",                  # tail
             ell(45, 64, 25, 14),                               # body
             ell(70, 56, 11, 8, -35),                           # neck
             ell(80, 47, 9, 7.5, -10),                          # head
             ell(89, 51, 8, 5, 10),                             # flat duck snout
             ell(33, 79, 7, 10), ell(46, 80, 6, 10), ell(60, 80, 5, 9), ell(68, 79, 5, 9),
             ell(34, 88, 9, 3.5), ell(47, 88.5, 8, 3.5), ell(61, 88, 7, 3), ell(70, 87.5, 7, 3)),
        belly(ell(48, 71, 16, 5)),
        spots(GREEND, [(30, 62, 2.6), (40, 58, 3), (52, 58, 2.6), (24, 66, 2)]),
        smile(90, 54, 6), eye(79, 45, 3.6), cheek(84, 52, 2.2), nostril(95, 49)))

    # P: Parasaurolophus - long tube crest curving back
    K.add("P", "Parasaurolophus", "Parasaurolophus can toot with its long head crest!", svg(
        ground(46, 92, 34),
        TL("M74 30Q62 14 44 11", RED, 7),                       # long tube crest
        blob(ORANGE,
             "M28 56Q12 54 3 62Q12 72 32 68Z",                  # tail
             ell(42, 62, 21, 15, -12),                          # body
             ell(62, 46, 8, 13, 32),                            # neck
             ell(75, 34, 10, 8),                                # head
             ell(86, 38, 8, 5, 10),                             # duck snout
             ell(36, 78, 7, 10), ell(50, 78, 6, 10),            # legs
             ell(39, 88, 9, 3.8), ell(53, 88, 8, 3.5)),
        TL("M58 60Q64 66 66 72", ORANGE, 4),                    # arm
        belly(ell(46, 68, 12, 7, -12)),
        L("M30 50l4 6M38 47l4 6M46 46l3 6M24 55l3 5", ORANGED, 3),           # stripes
        smile(88, 41, 6), eye(74, 31, 3.8), cheek(80, 39, 2.4), nostril(92, 36)))

    # P: Pachycephalosaurus - thick dome head with little knobs
    knobs = "".join(C(x, y, 2, BLUED, O, 1.6) for x, y in [(58, 36), (59, 42), (63, 47), (90, 37), (91, 42)])
    K.add("P", "Pachycephalosaurus", "Pachycephalosaurus has a big hard dome head!", svg(
        ground(46, 92, 34),
        knobs,
        blob(BLUE,
             "M30 56Q14 52 3 54Q10 68 34 68Z",                  # tail
             ell(44, 62, 19, 15, -15),                          # body
             ell(62, 50, 8, 12, 30),                            # neck
             ell(75, 41, 14, 9),                                # head
             ell(72, 31, 14, 12),                               # big dome
             ell(38, 77, 7, 10), ell(52, 77, 6, 10),
             ell(41, 88, 9, 3.8), ell(55, 88, 8, 3.5)),
        P("M58.5 34A14 12 0 1 1 85.5 34Q72 29 58.5 34Z", SAND, O, 3),   # thick bony dome
        HL(67, 24, 4.5, 2.6),
        TL("M58 60Q64 66 64 72", BLUE, 4),                      # arm
        belly(ell(48, 68, 11, 7, -15)),
        spots(BLUED, [(32, 56, 2.6), (40, 52, 2.4), (26, 60, 2), (70, 37, 1.6), (64, 38, 1.6)]),
        smile(83, 46, 6), eye(79, 39, 3.4), cheek(80, 45, 2.2), nostril(88, 41)))

    # P: Pteranodon - big wings, long backward crest, long beak
    K.add("P", "Pteranodon", "Pteranodon flies high in the sky!", svg(
        _cloud(50, 88, 1.0),
        P("M47 46Q28 32 3 50Q12 52 16 58Q24 56 30 62Q38 60 46 64Z", WING_PINK, O, 3),   # left wing
        P("M53 46Q72 32 97 50Q88 52 84 58Q76 56 70 62Q62 60 54 64Z", WING_PINK, O, 3),  # right wing
        L("M14 50Q30 46 46 52M86 50Q70 46 54 52", PINK, 2),
        P("M48 22L12 10L46 30Z", ORANGE, O, 2.5),              # long backward crest
        P("M56 23L93 31L56 33Z", YELLOW, O, 2.5),              # long beak
        blob(PINK,
             ell(50, 54, 7, 11),                                # body
             ell(50, 38, 4.5, 8),                               # neck
             ell(52, 28, 8, 7),                                 # head
             ell(46, 68, 2.5, 4), ell(54, 68, 2.5, 4)),         # little feet
        L("M58 32Q72 34 86 32", O, 1.6),
        eye(52, 26, 3.4), cheek(56, 32, 2)))

    # P: Plesiosaurus - swimmer, medium neck, 4 flippers
    K.add("P", "Plesiosaurus", "Plesiosaurus swims with four flippers!", svg(
        _waves([(6, 10, 5), (58, 8, 5)]),
        _bubbles([(90, 18, 2.4), (86, 10, 1.6), (12, 30, 2), (16, 22, 1.4)]),
        E(66, 74, 11, 4, TEALD, O, 2.5, rot=-50),              # far flippers
        E(34, 74, 10, 4, TEALD, O, 2.5, rot=-50),
        blob(TEAL,
             "M22 56Q8 60 3 70Q14 70 26 66Z",                   # short tail
             ell(42, 60, 24, 13, -5),                           # body
             "M56 54Q66 42 70 30L84 30Q80 48 66 64Z",           # neck
             ell(80, 27, 10, 7.5),                              # small head
             ell(56, 78, 13, 4.5, -45),                         # front flipper
             ell(24, 76, 12, 4.5, -45)),                        # back flipper
        belly(ell(44, 66, 15, 4.5, -5), "#b2dfdb"),
        spots(TEALD, [(34, 54, 2.6), (44, 52, 3), (54, 54, 2.4), (24, 58, 2)]),
        smile(85, 31, 6), eye(80, 25, 3.4), cheek(80, 31, 2), nostril(88, 26),
        _waves([(20, 94, 4), (62, 92, 4)])))

    # Q: Quetzalcoatlus - giant flyer with huge wings and a very long beak
    K.add("Q", "Quetzalcoatlus", "Quetzalcoatlus is a giant flyer with a long, long beak!", svg(
        _cloud(26, 86, 0.9),
        P("M50 50Q58 26 76 6Q74 30 60 56Z", REDD, O, 3),        # far wing
        P("M50 50Q30 28 3 10Q10 26 12 38Q22 40 24 50Q32 52 36 60Z", RED, O, 3),   # near wing (huge)
        L("M10 22Q30 34 46 50", REDD, 2),
        P("M76 36L70 20L82 32Z", ORANGE, O, 2.5),               # little crest
        TL("M36 60Q28 66 20 66M40 61Q34 70 26 72", GREY, 3),    # legs trailing behind
        blob(GREY,
             ell(45, 57, 13, 8, -15),                           # body
             "M52 52Q66 40 74 36L80 42Q70 52 56 62Z",           # long neck
             ell(79, 38, 7, 6)),                                # head
        P("M83 35L96 64L80 44Z", YELLOW, O, 2.5),               # very long beak
        belly(ell(46, 61, 8, 3.5, -15), "#cfd8dc"),
        eye(78, 37, 3.2), cheek(81, 42, 1.8)))

    # R: Rhamphorhynchus - small flyer, long tail with a diamond vane
    K.add("R", "Rhamphorhynchus", "Rhamphorhynchus has a long tail with a diamond on the end!", svg(
        _cloud(70, 88, 0.8),
        P("M58 46Q70 24 86 6Q86 28 66 54Z", ORANGED, O, 3),     # far wing
        TL("M46 56Q30 64 26 76Q22 84 14 84", YELLOW, 2.6),       # long tail
        P("M14 76L22 84L14 94L6 84Z", RED, O, 2.5),             # diamond vane
        blob(YELLOW,
             ell(54, 52, 12, 8, -15),                           # body
             ell(66, 44, 5, 6, 30),                             # neck
             ell(74, 38, 9, 8)),                                # head
        P("M58 48Q40 24 10 10Q16 26 20 34Q30 34 34 42Q42 42 46 54Z", ORANGE, O, 3),  # near wing
        L("M18 18Q36 30 52 48", ORANGED, 2),
        P("M81 35L97 42L81 44Z", YELLOW, O, 2.5),               # pointy beak
        P("M85 42.5l1.5 2.5 1.5 -2Z", "#fff", O, 1), P("M90 42l1.2 2 1.2 -1.6Z", "#fff", O, 1),
        TL("M52 58L50 64M58 58L58 64", YELLOW, 2),             # little feet
        belly(ell(56, 56, 7, 3, -15)),
        eye(74, 35, 3.6), cheek(76, 42, 2.2)))
