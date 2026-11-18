"""Dinosaurs: the two style examples (T. rex, Stegosaurus).  See dinos_kit.py for the style rules."""
from dinos_kit import *


def add_more(K):
    # T: Tyrannosaurus rex - big head, tiny arms
    K.add("T", "T. rex", "Tyrannosaurus rex! Big head, tiny arms. ROAR!", svg(
        ground(46, 92, 34),
        blob(GREEN,
             "M34 50Q16 52 3 70Q18 72 36 68Z",                  # tail
             ell(43, 60, 23, 17, -12),                          # body
             ell(60, 44, 9, 13, 25),                            # neck
             "M52 30Q54 16 72 16Q92 16 94 30Q95 42 82 44L60 44Q52 42 52 30Z",  # head
             ell(36, 78, 7, 11), ell(54, 77, 7, 11),            # legs
             ell(39, 88, 10, 4.5), ell(58, 87, 10, 4.5)),       # feet
        belly(ell(48, 66, 14, 9, -12)),
        TL("M64 56Q70 58 72 62", GREEN, 3.5),                   # tiny arm
        spots(GREEND, [(28, 56, 3), (36, 50, 2.4), (44, 52, 2), (20, 62, 2)]),
        L("M62 36Q76 40 92 34", O, 2.2),                        # big smile
        P("M70 38.5L72 42L74 39Z", "#fff", O, 1.2), P("M80 38.5L82 41.5L84 38Z", "#fff", O, 1.2),
        eye(68, 25, 4.6), nostril(90, 25), cheek(78, 33)))

    # S: Stegosaurus - plates on its back, spikes on its tail
    plates = "".join(P(f"M{x - w} {y + 6}L{x} {y - h}L{x + w} {y + 6}Z", ORANGE, O, 2.5)
                     for x, y, h, w in [(22, 52, 10, 6), (33, 43, 14, 7), (46, 39, 16, 8), (59, 42, 14, 7), (70, 50, 10, 6)])
    K.add("S", "Stegosaurus", "Stegosaurus has plates on its back and spikes on its tail!", svg(
        ground(50, 92, 38),
        plates,
        P("M8 66L3 46L15 63Z", YELLOW, O, 2.5), P("M15 65L16 45L24 63Z", YELLOW, O, 2.5),   # tail spikes
        blob(TEAL,
             "M28 60Q12 62 6 66Q16 74 32 72Z",                      # tail
             ell(47, 63, 26, 15),                                   # body
             ell(76, 66, 9, 7, -20),                                # neck
             ell(86, 62, 10, 8),                                    # head
             ell(32, 79, 6, 10), ell(42, 80, 6, 10), ell(56, 80, 6, 10), ell(66, 79, 6, 10)),
        belly(ell(50, 71, 15, 4.5)),
        spots(TEALD, [(36, 58, 3), (48, 55, 3.5), (60, 59, 3)]),
        smile(88, 66, 6), eye(87, 59, 3.4), cheek(82, 66, 2.2)))
