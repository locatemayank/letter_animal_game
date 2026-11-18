"""Dinosaurs A-D: Ankylosaurus, Allosaurus, Apatosaurus, Argentinosaurus, Brachiosaurus, Baryonyx,
Brontosaurus, Carnotaurus, Compsognathus, Corythosaurus, Diplodocus, Dilophosaurus, Deinonychus."""
from dinos_kit import *

PINKD = "#e0789f"
CLAW = "#fff8e1"


def _tri(x1, y1, x2, y2, x3, y3, fill, w=2.5):
    return P(f"M{x1} {y1}L{x2} {y2}L{x3} {y3}Z", fill, O, w)


def _bumps(fill, pts, w=1.8):
    return "".join(C(x, y, r, fill, O, w) for x, y, r in pts)


def _stripes(color, segs, w=3.2):
    return "".join(L(d, color, w) for d in segs)


def _feather(x, y, rot, s=1.0, fill=PURPLED):
    """Small leaf-shaped feather tuft pointing left at angle rot."""
    d = f"M0 0Q{-6 * s:g} {-4 * s:g} {-12 * s:g} 0Q{-6 * s:g} {4 * s:g} 0 0Z"
    return T(f"translate({x} {y}) rotate({rot})", P(d, fill, O, 2))


def add_more(K):
    # ---------------- A ----------------
    # Ankylosaurus: low armoured dome with bumps, club on the tail
    shell_spikes = "".join(_tri(x - 4, y + 3, x + dx, y - 8, x + 4, y + 3, SAND)
                           for x, y, dx in [(24, 52, -3), (36, 44, -1), (50, 41, 0), (64, 44, 1), (76, 52, 3)])
    K.add("A", "Ankylosaurus", "Ankylosaurus has a club on its tail!", svg(
        ground(50, 92, 42),
        shell_spikes,
        _tri(84, 63, 80, 56, 88, 61, SAND, 2.2),
        blob(BROWN,
             "M26 66Q16 64 11 60L11 68Q18 74 28 76Z",           # tail
             "M16 76Q16 46 50 44Q82 46 86 70Q86 79 76 79L26 79Q16 79 16 76Z",  # dome
             ell(84, 70, 8, 7),                               # neck
             ell(90, 69, 8, 7),                               # head
             ell(28, 82, 6.5, 8), ell(40, 83, 6.5, 8), ell(62, 83, 6.5, 8), ell(74, 82, 6.5, 8)),
        E(11, 64, 7.5, 6, BROWND),                             # club
        dot(9, 61.5, 1.8, "#fff", ".45"),
        L("M18 73Q50 70 84 73", BROWND, 2.4),                 # shell rim
        _bumps(SAND, [(26, 64, 3), (38, 58, 3.4), (51, 56, 3.6), (64, 58, 3.4), (75, 64, 3),
                      (32, 70, 2.4), (45, 66, 2.6), (58, 66, 2.6), (70, 70, 2.4), (40, 50, 2.2), (55, 49, 2.2)]),
        smile(92, 73, 5), eye(89, 66, 3.3), cheek(86, 73, 2), nostril(96, 67)))

    # Allosaurus: big hunter with little red brow horns and stripes
    K.add("A", "Allosaurus", "Allosaurus has little horns above its eyes!", svg(
        ground(46, 92, 36),
        _tri(64, 23, 66, 12, 72, 22, RED),
        blob(ORANGE,
             "M32 50Q16 50 3 60Q16 68 34 68Z",                # tail
             ell(43, 59, 22, 15, -8),                         # body
             ell(61, 46, 8, 12, 30),                          # neck
             "M56 30Q57 20 72 20Q92 20 96 32Q97 42 84 44L62 44Q55 42 56 30Z",  # head
             ell(36, 76, 7, 11), ell(53, 76, 7, 11),
             ell(39, 87, 10, 4.5), ell(57, 87, 10, 4.5)),
        belly(ell(48, 65, 13, 8, -8)),
        _stripes(ORANGED, ["M30 48Q32 54 30 58", "M40 45Q42 51 40 55", "M50 45Q52 51 50 55", "M18 54Q20 58 19 62"]),
        TL("M60 60Q68 62 70 68", ORANGE, 4),                  # arm
        P("M70 68L74 71L70 72Z", CLAW, O, 1.5), P("M67 70L70 74L66 73Z", CLAW, O, 1.5),
        L("M66 37Q80 41 94 35", O, 2.2),
        P("M74 39L76 42.5L78 39.5Z", "#fff", O, 1.2), P("M84 38.5L86 41.5L88 38Z", "#fff", O, 1.2),
        eye(70, 28, 4.4), nostril(92, 28), cheek(80, 34)))

    # Apatosaurus: long neck reaching forward, long tail
    K.add("A", "Apatosaurus", "Apatosaurus has a long, long neck!", svg(
        ground(46, 92, 38),
        blob(BLUE,
             "M24 56Q8 58 2 76Q14 74 28 72Z",                 # tail
             ell(44, 62, 24, 16),                             # body
             "M56 52Q70 42 80 22L90 26Q82 48 68 68Z",         # neck
             ell(86, 21, 9.5, 7, -10),                        # head
             ell(28, 80, 6.5, 11), ell(40, 81, 6.5, 11), ell(54, 81, 6.5, 11), ell(66, 80, 6.5, 11)),
        belly(ell(46, 70, 16, 5)),
        spots(BLUED, [(34, 56, 3), (46, 52, 3.5), (58, 56, 2.8), (22, 62, 2.2), (72, 46, 2.2)]),
        smile(89, 25, 6), eye(86, 18, 3.4), cheek(82, 25, 2.2), nostril(94, 19)))

    # Argentinosaurus: so big it barely fits - head up high, tiny tree for scale
    K.add("A", "Argentinosaurus", "Argentinosaurus is super, super big!", svg(
        ground(46, 93, 44),
        blob(TEAL,
             "M16 52Q4 56 2 72Q10 72 20 68Z",                 # tail
             ell(40, 57, 32, 23),                             # body
             "M58 46Q74 32 81 12L93 15Q88 38 72 66Z",          # neck
             ell(87, 13, 9, 6.5, -12),                         # head
             ell(20, 82, 8.5, 11), ell(35, 83, 8.5, 11), ell(51, 83, 8.5, 11), ell(65, 82, 8.5, 11)),
        belly(ell(42, 71, 21, 6)),
        spots(TEALD, [(26, 48, 3.5), (40, 44, 4), (54, 48, 3.5), (34, 56, 2.5), (48, 56, 2.5), (74, 36, 2.4), (79, 26, 2)]),
        smile(90, 17, 5.5), eye(87, 10.5, 3), cheek(84, 16.5, 2), nostril(94, 12),
        # tiny tree for scale
        R(85, 78, 3, 14, BROWN, 1, O, 1.8), C(86.5, 72, 5, GREEN, O, 1.8), C(82.5, 76, 4, GREEN, O, 1.8), C(90.5, 76, 4, GREEN, O, 1.8), C(86.5, 75.5, 4, GREEN, "none", 0)))

    # ---------------- B ----------------
    # Brachiosaurus: very tall neck, front legs longer than back legs
    K.add("B", "Brachiosaurus", "Brachiosaurus is so tall it eats from treetops!", svg(
        ground(46, 92, 36),
        blob(YELLOW,
             "M26 62Q10 66 3 82Q16 80 30 72Z",                # tail
             ell(44, 58, 23, 14, -18),                        # sloping body
             "M54 50Q62 32 64 16L77 16Q76 34 72 58Z",         # neck
             ell(74, 15, 10, 7),                              # head
             circ(70, 10, 4.5),                                # nose bump
             ell(30, 79, 6.5, 11), ell(40, 80, 6.5, 11),      # back legs
             ell(56, 76, 6.5, 16), ell(66, 75, 6.5, 16)),     # long front legs
        belly(ell(46, 66, 14, 5, -18)),
        spots(YELLOWD, [(34, 56, 3), (44, 50, 3.4), (54, 46, 2.6), (62, 36, 2.2), (68, 26, 2), (28, 62, 2.2)]),
        smile(78, 19, 6), eye(74, 13, 3.4), cheek(71, 19, 2.2), nostril(83, 13)))

    # Baryonyx: long crocodile snout, big thumb claw, catching a fish
    K.add("B", "Baryonyx", "Baryonyx loves to catch fish!", svg(
        ground(46, 92, 36),
        blob(GREY,
             "M30 52Q14 52 3 62Q16 70 32 68Z",                # tail
             ell(42, 60, 21, 14, -8),                         # body
             ell(58, 47, 8, 12, 40),                          # neck
             "M56 34Q58 26 68 26Q74 26 78 31L96 36Q99 42 93 44L66 46Q56 44 56 34Z",  # head + long snout
             ell(35, 76, 7, 11), ell(51, 76, 7, 11),
             ell(38, 87, 10, 4.5), ell(55, 87, 10, 4.5)),
        belly(ell(47, 65, 12, 8, -8)),
        _stripes(GREYD, ["M28 49Q30 54 28 58", "M38 46Q40 51 38 55", "M48 46Q50 51 48 55", "M18 56Q20 59 19 62"]),
        # fish
        P("M86 68L95 61L94 75Z", SEA, O, 2),
        P("M64 68Q76 57 88 68Q76 79 64 68Z", SEA, O, 2),
        L("M76 63Q78 68 76 73", BLUED, 1.6), dot(69, 66.5, 1.3, O),
        TL("M56 58Q64 60 70 63", GREY, 4.5),                 # arm
        P("M68 60Q80 54 80 66Q76 61 71 64Z", CLAW, O, 2),    # big thumb claw
        L("M66 40Q80 42 94 41", O, 2),
        P("M76 41.5L77.5 44.3L79 41.6Z", "#fff", O, 1.1), P("M86 41.3L87.5 44L89 41.3Z", "#fff", O, 1.1),
        eye(67, 32, 3.8), nostril(94, 37), cheek(72, 39, 2.4)))

    # Brontosaurus: chunky, long neck, long whip tail
    K.add("B", "Brontosaurus", "Brontosaurus has a long whippy tail!", svg(
        ground(48, 92, 38),
        blob(PINK,
             "M22 56Q10 58 6 48Q4 42 2 40Q2 50 6 58Q12 70 28 72Z",  # whip tail
             ell(44, 62, 26, 18),                             # chunky body
             "M58 54Q68 50 70 34Q72 22 78 18L88 22Q82 26 81 36Q80 58 66 72Z",  # neck
             ell(85, 20, 9, 6.5),                             # head
             ell(28, 81, 7.5, 10), ell(41, 82, 7.5, 10), ell(55, 82, 7.5, 10), ell(67, 81, 7.5, 10)),
        belly(ell(46, 71, 18, 6)),
        spots(PINKD, [(32, 54, 3.4), (45, 50, 3.8), (58, 55, 3), (22, 60, 2.4), (76, 36, 2)]),
        smile(88, 24, 6), eye(85, 17, 3.4), cheek(81, 24, 2.2), nostril(93, 18)))

    # ---------------- C ----------------
    # Carnotaurus: short bulldog head with two little horns, tiny arms
    K.add("C", "Carnotaurus", "Carnotaurus has two little horns!", svg(
        ground(46, 92, 36),
        _tri(64, 22, 58, 10, 72, 18, YELLOW), _tri(73, 19, 76, 7, 81, 19, YELLOW),
        blob(RED,
             "M32 50Q16 50 3 62Q16 70 34 68Z",                # tail
             ell(43, 59, 22, 16, -10),                        # body
             ell(60, 44, 9, 12, 25),                          # neck
             "M56 30Q56 18 72 18Q90 18 92 32Q92 44 80 46L62 46Q55 42 56 30Z",  # short deep head
             ell(36, 77, 7, 11), ell(53, 77, 7, 11),
             ell(39, 87, 10, 4.5), ell(57, 87, 10, 4.5)),
        belly(ell(48, 66, 13, 8, -10)),
        spots(REDD, [(26, 55, 2.4), (34, 49, 2.6), (44, 48, 2.6), (54, 52, 2.2), (18, 60, 1.8), (30, 60, 1.8), (40, 55, 1.8)]),
        TL("M62 60Q66 62 67 65", RED, 3.5),                   # tiny arm
        L("M64 38Q76 42 89 36", O, 2.2),
        P("M72 40L74 43L76 40.3Z", "#fff", O, 1.2), P("M80 39.5L82 42.5L84 39Z", "#fff", O, 1.2),
        eye(71, 28, 4.4), nostril(88, 27), cheek(80, 34)))

    # Compsognathus: tiny and quick, next to a big leaf
    K.add("C", "Compsognathus", "Compsognathus is tiny and very quick!", svg(
        ground(52, 92, 36),
        # big leaf (much bigger than the dino)
        TL("M16 91Q14 64 26 40", GREEND, 2.5),
        P("M22 64Q4 60 4 38Q20 42 22 64Z", GREEN, O, 2.5),
        L("M22 63Q12 52 6 41", GREEND, 1.6),
        P("M26 40Q28 6 94 8Q74 34 26 40Z", GREEN, O, 2.5),
        L("M27 39Q58 22 92 9", GREEND, 1.8),
        L("M44 31L42 20", GREEND, 1.4), L("M58 24L58 13", GREEND, 1.4), L("M72 18L74 9", GREEND, 1.4),
        L("M46 30L54 34", GREEND, 1.4), L("M62 22L70 26", GREEND, 1.4),
        # feather tufts on the back
        _feather(58, 58, -30, 0.8, ORANGE), _feather(64, 54, -40, 0.8, ORANGE),
        blob(YELLOW,
             "M52 62Q34 60 14 70Q30 72 52 70Z",               # long thin tail
             ell(58, 63, 11, 8, -15),                         # small body
             "M62 58Q68 52 70 44L76 46Q74 56 68 66Z",         # neck
             ell(76, 42, 8, 5.5, -8),                         # head
             "M54 66L46 82L50 84L60 70Z",                     # back leg
             "M62 66L68 80L72 78L66 66Z",                     # front leg
             ell(46, 85, 5, 2.5), ell(72, 81, 5, 2.5, -20)),
        belly(ell(60, 67, 7, 3.5, -15)),
        spots(YELLOWD, [(54, 60, 1.6), (60, 58, 1.6), (40, 66, 1.4)]),
        TL("M66 62L72 64", YELLOW, 2.2),                      # tiny arm
        L("M84 70L90 70", "#90a4ae", 1.6), L("M80 76L88 76", "#90a4ae", 1.6),  # speed lines
        smile(80, 45, 4.5), eye(77, 40, 2.8), cheek(75, 45, 1.6), nostril(83, 41)))

    # Corythosaurus: duckbill with a round helmet crest
    K.add("C", "Corythosaurus", "Corythosaurus has a round crest like a helmet!", svg(
        ground(46, 92, 38),
        P("M66 30Q62 10 79 9Q93 10 90 28Z", ORANGE, O, 2.5),   # helmet crest
        blob(GREEN,
             "M30 54Q14 56 3 70Q18 72 34 70Z",                # tail
             ell(44, 62, 24, 16, -10),                        # body
             ell(64, 46, 9, 13, 30),                          # neck
             ell(77, 33, 11, 8),                              # head
             "M82 30Q95 29 96 36Q95 42 84 41Z",               # duck bill
             ell(36, 79, 7.5, 11), ell(52, 79, 7, 11),
             ell(40, 88, 10, 4.5), ell(56, 88, 9, 4.5)),
        L("M70 22Q72 14 79 13Q86 14 87 22", ORANGED, 2), dot(76, 15, 1.8, "#fff", ".5"),
        belly(ell(50, 69, 14, 6, -10)),
        spots(GREEND, [(30, 56, 3), (40, 50, 3.4), (52, 50, 2.8), (22, 62, 2.2)]),
        TL("M64 62Q70 66 70 72", GREEN, 4),                   # arm
        smile(88, 38, 6), eye(77, 31, 3.6), cheek(74, 38, 2.2), nostril(92, 33)))

    # ---------------- D ----------------
    # Diplodocus: long and low, very long neck and very long tail
    K.add("D", "Diplodocus", "Diplodocus has a very, very long tail!", svg(
        ground(50, 92, 44),
        blob(LIME,
             "M32 58Q16 56 2 50Q10 60 30 72Z",                # very long tail
             ell(46, 64, 20, 13),                             # body
             "M58 56Q74 48 84 42L88 50Q76 60 62 72Z",         # long neck
             ell(88, 45, 8, 6, -15),                        # head
             ell(34, 80, 6, 10), ell(44, 81, 6, 10), ell(54, 81, 6, 10), ell(62, 80, 6, 10)),
        belly(ell(48, 71, 14, 4.5)),
        _stripes(GREEND, ["M36 53Q38 58 36 62", "M46 51Q48 56 46 60", "M56 53Q57 58 55 62",
                          "M22 57Q24 60 23 63", "M68 52Q70 55 70 58", "M78 47Q80 50 80 53"], 3),
        smile(90, 49, 5), eye(87, 42, 3.2), cheek(84, 48, 2), nostril(94.5, 43)))

    # Dilophosaurus: two crests on its head
    K.add("D", "Dilophosaurus", "Dilophosaurus has two crests on its head!", svg(
        ground(46, 92, 36),
        P("M62 26Q60 6 76 12Q72 18 72 26Z", RED, O, 2.5),
        P("M72 26Q72 4 88 12Q82 18 84 28Z", RED, O, 2.5),
        L("M66 22Q67 14 72 13", REDD, 1.8), L("M77 22Q78 13 84 12", REDD, 1.8),
        blob(SEA,
             "M32 52Q16 52 3 60Q16 68 34 68Z",                # tail
             ell(43, 60, 21, 14, -10),                        # body
             ell(60, 45, 7.5, 13, 25),                        # neck
             "M58 32Q58 24 72 24Q92 24 96 34Q96 42 86 43L64 43Q57 41 58 32Z",  # head
             ell(36, 76, 6.5, 11), ell(52, 76, 6.5, 11),
             ell(39, 87, 9.5, 4.5), ell(56, 87, 9.5, 4.5)),
        belly(ell(47, 66, 12, 7, -10)),
        spots(BLUED, [(26, 54, 2.6), (35, 50, 2.8), (45, 49, 2.4), (18, 58, 1.8)]),
        TL("M58 58Q65 62 67 67", SEA, 3.8),                   # arm
        P("M67 67L71 70L67 71Z", CLAW, O, 1.4),
        L("M66 37Q80 40 93 36", O, 2.2),
        eye(70, 31, 4), nostril(92, 30), cheek(79, 35, 2.5)))

    # Deinonychus: feathery, with a big sickle claw on its toe
    wing = P("M55 55L72 60L71 68L67 64L65 72L61 67L57 74L54 66Z", PURPLED, O, 2)
    K.add("D", "Deinonychus", "Deinonychus has a big hooked claw on its toe!", svg(
        ground(50, 92, 36),
        _feather(18, 46, 20, 1.3, PINK), _feather(18, 47, -12, 1.3, PINK), _feather(19, 48, 50, 1.1, PINK),  # tail fan
        _feather(38, 46, 40, 1.0, PINK), _feather(48, 43, 45, 1.0, PINK),                              # back fluff
        _feather(68, 25, 35, 1.1, PINK), _feather(74, 23, 55, 1.0, PINK),            # head crest
                                                       # far arm
        blob(PURPLE,
             "M36 48Q24 44 14 46Q22 56 38 60Z",               # stiff tail
             ell(46, 54, 17, 12, -15),                        # body
             ell(63, 42, 7, 12, 30),                          # neck
             "M62 30Q62 21 74 21Q86 21 96 30Q98 38 88 39L68 41Q61 39 62 30Z",  # head
             ell(42, 64, 9, 11, 10),                          # thigh
             "M38 70L40 85L47 85L46 70Z",                     # shin
             ell(48, 87, 8, 3.5),                             # foot
             ell(56, 64, 6, 9, -10),                          # far thigh
             "M54 70L60 85L65 84L60 70Z",
             ell(66, 87, 7, 3.2)),
        belly(ell(52, 60, 9, 5, -15)),
        wing,
        TL("M56 56Q64 60 71 62", PURPLE, 3.6),                # arm
        P("M71 60L76 62L71 64Z", CLAW, O, 1.3),
        # big sickle claws held up off the ground
        P("M46 85Q41 72 55 69Q49 77 51 85Z", CLAW, O, 2),
        P("M63 85Q60 74 71 72Q66 78 68 85Z", CLAW, O, 1.8),
        L("M68 34Q80 37 93 33", O, 2.2),
        P("M76 35.5L78 38.5L80 35.8Z", "#fff", O, 1.1),
        eye(73, 28, 3.8), nostril(93, 29), cheek(82, 33, 2.4)))
