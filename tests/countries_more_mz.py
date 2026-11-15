"""Extra Countries flags M–Z (plus sailing letter flags for O, X, Y, Z).

Geometry follows the official construction sheets (Malaysia, Morocco, New Zealand, Pakistan,
Turkey, Tunisia, Quebec, Vanuatu, Zimbabwe and Zanzibar use the published coordinates).
Emblems with fine detail (Spain's arms, Uganda's crane, the Welsh dragon, Vanuatu's
namele fronds) are simplified so they still read at picture size.
"""
import math
from svgkit import *
from countries_kit import *

# signal flags are drawn 72 x 60 (a little longer than high, like real ones)
SIG_W, SIG_H = 72, 60
SIG_RED, SIG_YEL, SIG_BLUE = "#E4002B", "#FFD100", "#0033A0"


def arc_d(cx, cy, r, a0, a1):
    """Arc path from angle a0 to a1 (degrees, clockwise on screen)."""
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) % 360 > 180 else 0
    return f"M{fmt(p0[0])} {fmt(p0[1])}A{fmt(r)} {fmt(r)} 0 {large} 1 {fmt(p1[0])} {fmt(p1[1])}"


def ring_d(cx, cy, r):
    return (f"M{fmt(cx - r)} {fmt(cy)}A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx + r)} {fmt(cy)}"
            f"A{fmt(r)} {fmt(r)} 0 1 1 {fmt(cx - r)} {fmt(cy)}")


def stroke(d, c, w, cap="butt", join="miter"):
    return (f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{fmt(w)}" '
            f'stroke-linecap="{cap}" stroke-linejoin="{join}"/>')


# ================================================================ M
def madagascar():
    return rect(0, 0, 30, 60, "#fff") + rect(30, 0, 60, 30, "#FC3D32") + rect(30, 30, 60, 30.02, "#007E3A")


def malaysia():
    out = []
    for i in range(14):
        out.append(rect(0, i, 28, 1.02, "#CC0001" if i % 2 == 0 else "#fff"))
    out.append(rect(0, 0, 14, 8, "#010066"))
    # 14-point star and crescent (official coordinates, 480 units = 1 stripe)
    em = ("M4200 720l107 732 414-613-222 706 639-373-506 540 738-59-690 267 690 267-738-59 506 540-639-373"
          " 222 706-414-613-107 732-107-732-414 613 222-706-639 373 506-540-738 59 690-267-690-267 738 59"
          "-506-540 639 373-222-706 414 613zM3600 750a1280 1280 0 1 0 0 2340 1440 1440 0 1 1 0-2340z")
    out.append(T("scale(0.0020833)", F(em, "#FC0")))
    return "".join(out)


def morocco():
    d = "M45 17.31L52.46 40.27L32.93 26.08H57.07L37.54 40.27Z"
    return rect(0, 0, 90, 60, "#C1272D") + stroke(d, "#006233", 1.43)


# ================================================================ N
def new_zealand():
    out = [rect(0, 0, 120, 60, "#012169"), union_jack()]
    k = 1.0515          # circumradius of the official pentagram unit
    for x, y, rw, rr in ((90, 12, 45.4, 30), (101.88, 22.33, 40.4, 25), (76.14, 25.95, 45.4, 30), (90, 48, 50.4, 35)):
        out.append(star(x, y, rw * k / 10, "#fff") + star(x, y, rr * k / 10, "#C8102E"))
    return "".join(out)


# ================================================================ O
def olympic():
    cols = {"blue": "#0081C8", "yellow": "#FCB131", "black": "#000", "green": "#00A651", "red": "#EE334E"}
    r, sw, dx, dy = 8.6, 1.9, 19.8, 9.2
    cy0 = 30 - dy / 2 - 1
    top = [(45 - dx, cy0, cols["blue"]), (45, cy0, cols["black"]), (45 + dx, cy0, cols["red"])]
    bot = [(45 - dx / 2, cy0 + dy, cols["yellow"]), (45 + dx / 2, cy0 + dy, cols["green"])]
    out = [rect(0, 0, 90, 60, "#fff")]
    for x, y, c in top + bot:
        out.append(stroke(ring_d(x, y, r), c, sw))
    # interlace: the top-row ring passes over the lower-row ring at their upper crossing
    for (x1, y1, c1) in top:
        for (x2, y2, _) in bot:
            d = math.hypot(x2 - x1, y2 - y1)
            if d >= 2 * r:
                continue
            a = d / 2
            h = math.sqrt(r * r - a * a)
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            pts = [(mx + h * (y2 - y1) / d, my - h * (x2 - x1) / d), (mx - h * (y2 - y1) / d, my + h * (x2 - x1) / d)]
            px, py = min(pts, key=lambda p: p[1])
            phi = math.degrees(math.atan2(py - y1, px - x1))
            out.append(stroke(arc_d(x1, y1, r, phi - 22, phi + 22), c1, sw))
    return "".join(out)


def oscar():
    # diagonal from upper hoist to lower fly: red in the upper fly, yellow in the lower hoist
    return (poly([(0, 0), (SIG_W, 0), (SIG_W, SIG_H)], SIG_RED)
            + poly([(0, 0), (SIG_W, SIG_H), (0, SIG_H)], SIG_YEL))


# ================================================================ P
def pakistan():
    em = "".join([
        rect(-75, -40, 120, 80, "#fff"), rect(-45, -40, 90.02, 80, "#01411C"),
        circ(0, 0, 24, "#fff"), circ(6.14, -5.45, 22, "#01411C"),
        star(11.96, -10.63, 8, "#fff", inner=0.382, rot=-41.63),
    ])
    return T("translate(75 40)", em)


def quebec():
    fleur = ("M2309 1622v-129h-115c0-66 32-130 66-150 20-17 65-25 104-5 51 29 54 113 28 151 243-45 219-280 136-365"
             "-67-69-140-79-196-58-128 46-214 199-218 427h-67c0-207 36-273 130-534 48-123 19-275-65-415-31-50-69-95"
             "-112-144-43 49-81 94-112 144-84 140-113 292-65 415 94 261 130 327 130 534h-67c-4-228-90-381-218-427"
             "-56-21-129-11-196 58-83 85-107 320 136 365-26-38-23-122 28-151 39-20 84-12 104 5 34 20 66 84 66 150"
             "h-115v129h239c-3 67-39 119-106 148 8 28 49 85 105 81 11 60 21 94 71 149 50-55 60-89 71-149 56 4 97-53"
             " 105-81-67-29-103-81-106-148z")
    q = rect(0, 0, 4000, 2400, "#003DA5") + F(fleur, "#fff")
    return (rect(0, 0, 9600, 6400, "#fff") + q + T("translate(5600 0)", q)
            + T("translate(0 4000)", q) + T("translate(5600 4000)", q))


# ================================================================ S
def spain_arms(cx, cy):
    gold, red, white, grey = "#F1BF00", "#AD1519", "#fff", "#c8c8c8"
    o = "#7a5a00"
    out = []
    # pillars of Hercules with crowns and red ribbons
    for px in (cx - 10.2, cx + 10.2):
        out.append(rect(px - 2.4, cy + 7.6, 4.8, 1.6, gold))          # base
        out.append(rect(px - 1.4, cy - 5.4, 2.8, 13.2, grey))         # shaft
        out.append(rect(px - 0.7, cy - 5.4, 0.9, 13.2, white))
        out.append(rect(px - 2.2, cy - 6.8, 4.4, 1.4, gold))          # capital
        out.append(F(f"M{px - 2} {cy - 6.8}V{cy - 9}L{px - 1} {cy - 8}L{px} {cy - 9.6}L{px + 1} {cy - 8}"
                     f"L{px + 2} {cy - 9}V{cy - 6.8}Z", gold))      # little crown
        out.append(F(f"M{px - 3.4} {cy - 1}C{px - 1} {cy - 2.6} {px + 1} {cy + 1.2} {px + 3.4} {cy - 0.4}"
                     f"V{cy + 1.4}C{px + 1} {cy + 3} {px - 1} {cy - 0.8} {px - 3.4} {cy + 0.8}Z", red))
    # royal crown above the shield
    out.append(F(f"M{cx - 5.6} {cy - 6.6}L{cx - 6.4} {cy - 10.6}L{cx - 3.4} {cy - 9}L{cx} {cy - 12.4}"
                 f"L{cx + 3.4} {cy - 9}L{cx + 6.4} {cy - 10.6}L{cx + 5.6} {cy - 6.6}Z", gold))
    out.append(rect(cx - 5.6, cy - 7.4, 11.2, 1.3, red))
    out.append(circ(cx, cy - 12.9, 0.9, gold))
    # shield (flat top, round bottom)
    x0, x1, y0, ym, y1 = cx - 6, cx + 6, cy - 5.6, cy + 2, cy + 9.4
    shield = f"M{x0} {y0}H{x1}V{ym}C{x1} {cy + 7} {cx + 3} {y1} {cx} {y1}C{cx - 3} {y1} {x0} {cy + 7} {x0} {ym}Z"
    out.append(F(shield, white))
    # quarters: Castile (castle on red), Leon (lion on white), Aragon (stripes), Navarre (chains)
    out.append(rect(x0, y0, 6, 6.4, red))
    out.append(F(f"M{cx - 4.6} {y0 + 5.2}V{y0 + 2.6}H{cx - 4}V{y0 + 1.6}H{cx - 3.4}V{y0 + 2.6}H{cx - 2.6}V{y0 + 1}"
                 f"H{cx - 2}V{y0 + 2.6}H{cx - 1.4}V{y0 + 1.6}H{cx - 0.8}V{y0 + 2.6}H{cx - 0.6}V{y0 + 5.2}Z", gold))
    out.append(F(f"M{cx + 1.6} {y0 + 5.4}C{cx + 1.8} {y0 + 3.4} {cx + 2.6} {y0 + 2.6} {cx + 3} {y0 + 1.4}"
                 f"C{cx + 3.6} {y0 + 0.6} {cx + 4.8} {y0 + 1} {cx + 4.4} {y0 + 2.2}L{cx + 4.2} {y0 + 3}"
                 f"C{cx + 5} {y0 + 3.4} {cx + 5} {y0 + 4.6} {cx + 4.6} {y0 + 5.4}Z", "#8A3D8E"))
    lo = f"M{x0} {cy + 0.8}H{cx}V{y1}C{cx - 3} {y1} {x0} {cy + 7} {x0} {ym}Z"
    out.append(F(lo, gold))
    for k in range(4):
        sx = x0 + 0.75 + k * 1.5
        out.append(poly(clip_convex(rect_pts(sx, cy + 0.8, 0.75, 9), [(x0, cy + 0.8), (cx, cy + 0.8), (cx, y1), (x0, cy + 6.5)]), red))
    ro = f"M{cx} {cy + 0.8}H{x1}V{ym}C{x1} {cy + 7} {cx + 3} {y1} {cx} {y1}Z"
    out.append(F(ro, red))
    out.append(lines(f"M{cx + 1} {cy + 2.6}H{cx + 5}M{cx + 1} {cy + 5}H{cx + 4.6}M{cx + 3} {cy + 1.4}V{cy + 8}"
                     f"M{cx + 1.2} {cy + 1.6}L{cx + 4.6} {cy + 6.4}M{cx + 4.8} {cy + 1.6}L{cx + 1.4} {cy + 6.4}", gold, 0.5))
    # Granada pomegranate at the point, Bourbon oval in the middle
    out.append(circ(cx, cy + 8, 1, "#e57373"))
    out.append(f'<ellipse cx="{fmt(cx)}" cy="{fmt(cy + 0.8)}" rx="2" ry="2.4" fill="#0039F0" stroke="{red}" stroke-width="0.6"/>')
    out.append(circ(cx, cy + 0.8, 0.55, gold))
    out.append(stroke(shield, o, 0.35))
    return "".join(out)


def spain():
    return (hstripes(90, 60, ["#AA151B", "#F1BF00", "#AA151B"], [1, 2, 1])
            + T("translate(30 30.5) scale(1.2) translate(-30 -30.5)", spain_arms(30, 30.5)))


def switzerland():
    return rect(0, 0, 32, 32, "#DA291C") + rect(13, 6, 6, 20, "#fff") + rect(6, 13, 20, 6, "#fff")


# ================================================================ T
def turkey():
    em = ("M41750 0l13568-4408-8386 11541V-7133l8386 11541zM42675 8021a15000 15000 0 1 1 0-16042"
          " 12000 12000 0 1 0 0 16042z")
    return rect(0, 0, 90, 60, "#E30A17") + T("translate(0 30) scale(0.001)", F(em, "#fff"))


def tunisia():
    em = "".join([rect(-60, -40, 120, 80, "#E70013"), circ(0, 0, 20, "#fff"), circ(0, 0, 15, "#E70013"),
                  circ(4, 0, 12, "#fff"),
                  F("M-5 0L11.28-5.29L1.22 8.56V-8.56L11.28 5.29Z", "#E70013")])
    return T("translate(60 40)", em)


# ================================================================ U
def uganda_crane(cx, cy):
    grey, dark, gold, red = "#8f9496", "#3a3a3a", "#E8B800", "#D90000"
    out = [
        # legs: one standing, one raised and bent forward
        lines(f"M{cx + 2.6} {cy + 3}L{cx + 2.2} {cy + 12}M{cx + 2.2} {cy + 12}L{cx - 0.2} {cy + 12.6}M{cx + 2.2} {cy + 12}L{cx + 4} {cy + 12.6}", dark, 0.9),
        lines(f"M{cx + 0.4} {cy + 3}L{cx - 4.6} {cy + 6.4}L{cx - 3.4} {cy + 10.4}M{cx - 3.4} {cy + 10.4}L{cx - 5.4} {cy + 11}M{cx - 3.4} {cy + 10.4}L{cx - 2} {cy + 11.4}", dark, 0.9),
        # drooping tail plumes
        F(f"M{cx + 6} {cy - 1.6}C{cx + 9.6} {cy + 0.4} {cx + 10.4} {cy + 4.2} {cx + 9.6} {cy + 7.4}"
          f"C{cx + 8} {cy + 4.6} {cx + 6} {cy + 3.4} {cx + 4} {cy + 2.6}Z", dark),
        # body
        F(f"M{cx - 3.6} {cy - 1}C{cx - 2.4} {cy - 4} {cx + 4} {cy - 4.4} {cx + 7} {cy - 2}"
          f"C{cx + 8.4} {cy} {cx + 6.4} {cy + 3.6} {cx + 2} {cy + 3.8}C{cx - 1.4} {cy + 4} {cx - 4.4} {cy + 1.6} {cx - 3.6} {cy - 1}Z", grey),
        # white and golden wing feathers
        F(f"M{cx - 0.6} {cy - 2}C{cx + 2} {cy - 3.6} {cx + 5.6} {cy - 3} {cx + 7.4} {cy - 1.2}"
          f"C{cx + 5} {cy - 0.2} {cx + 2} {cy + 0.2} {cx - 0.6} {cy - 2}Z", "#fff"),
        F(f"M{cx + 1} {cy - 0.4}C{cx + 3} {cy + 0.4} {cx + 5.6} {cy + 0.2} {cx + 7.2} {cy - 0.8}"
          f"C{cx + 6.4} {cy + 1.6} {cx + 3} {cy + 2} {cx + 1} {cy - 0.4}Z", "#c9a24a"),
        # neck
        lines(f"M{cx - 2.4} {cy - 1}C{cx - 4.6} {cy - 4} {cx - 3} {cy - 6.6} {cx - 4} {cy - 9.4}", grey, 2.2),
        # head: black crown cap, white cheek, red wattle, grey beak
        F(f"M{cx - 6.2} {cy - 10.4}L{cx - 9.6} {cy - 9.4}L{cx - 6} {cy - 9.4}Z", dark),
        circ(cx - 4.8, cy - 10.2, 1.7, "#111"),
        circ(cx - 4.3, cy - 9.8, 0.9, "#fff"),
        F(f"M{cx - 5.6} {cy - 9}C{cx - 6} {cy - 7.6} {cx - 5.2} {cy - 7.2} {cx - 4.8} {cy - 8.4}Z", red),
        # golden crown of stiff feathers
        lines("".join(f"M{fmt(cx - 4.4)} {fmt(cy - 11.4)}L{fmt(cx - 4.4 + 3.4 * math.cos(math.radians(a)))} {fmt(cy - 11.4 + 3.4 * math.sin(math.radians(a)))}"
                      for a in (-150, -125, -100, -75, -50, -25)), gold, 0.7),
    ]
    return "".join(out)


def uganda():
    cols = ["#000", "#FCDC04", "#D90000", "#000", "#FCDC04", "#D90000"]
    return (hstripes(90, 60, cols) + circ(45, 30, 15, "#fff") + uganda_crane(45, 29.5))


# ================================================================ V
def venezuela():
    out = [hstripes(90, 60, ["#FFCC00", "#00247D", "#CF142B"])]
    for th in (-70, -50, -30, -10, 10, 30, 50, 70):
        a = math.radians(th)
        out.append(star(45 + 18 * math.sin(a), 42 - 18 * math.cos(a), 2.6, "#fff", rot=-90 + th))
    return "".join(out)


def frond(p, q, w, side_cut=6):
    """Serrated yellow leaf from p (stalk) to q (tip), half-width w (native Vanuatu units)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    left, right = [], []
    n = 8
    for i in range(n + 1):
        t = 0.12 + 0.88 * i / n
        ww = w * math.sin(math.pi * min(1, t * 1.15)) ** 0.6
        for side, arr in ((1, left), (-1, right)):
            tip_t = t + 0.06
            arr.append((p[0] + ux * ln * t + nx * ww * side * 0.35, p[1] + uy * ln * t + ny * ww * side * 0.35))
            arr.append((p[0] + ux * ln * tip_t + nx * ww * side, p[1] + uy * ln * tip_t + ny * ww * side))
    stalk = [(p[0] + nx * 3, p[1] + ny * 3)]
    return poly(stalk + left + [q] + right[::-1] + [(p[0] - nx * 3, p[1] - ny * 3)], "#FDCE12")


def vanuatu():
    y = "#FDCE12"
    tusk = ("M115.48 339.52V372C143.73 372 199.18 350.35 199.18 280.64C199.18 210.94 140.04 198 122.35 198"
            "C104.66 198 50 210.67 50 267.71C50 324.74 103.6 330.02 114.16 330.02C124.72 330.02 164.33 320.51 159.84 277.74"
            "C159.84 289.89 146.11 315.5 117.33 315.5C88.55 315.5 70.6 294.11 70.6 272.99C70.6 251.86 88.02 223.61 118.39 223.61"
            "C148.75 223.61 170.93 250.54 170.93 277.74C170.93 304.94 149.54 339.52 115.48 339.52Z")
    return "".join([
        rect(0, 0, 950, 285, "#D21034"), rect(0, 285, 950, 285, "#009543"),
        poly([(0, 0), (552.81, 285), (0, 570)], "#000"), rect(0, 234, 950, 102, "#000"),
        poly([(0, 40.5), (474.25, 285), (0, 529.5)], y), rect(0, 270, 950, 30, y),
        poly([(0, 74.25), (408.78, 285), (0, 495.75)], "#000"),
        F(tusk, y),
        frond((91, 298), (145, 242), 12), frond((147.5, 298), (93.5, 242), 12),
    ])


# ================================================================ W
def welsh_dragon():
    red = "#C8102E"
    parts = [
        # tail: from the rump down, round and up over the back, ending in an arrow point
        lines("M66 33C74 36 80 36 82 30C84 23 79 17 72 17C67 17 64 20 63 23", red, 2.6),
        poly([(60.4, 21.6), (62.2, 26.8), (66.2, 22.6)], red),
        # wings (raised, scalloped trailing edge)
        F("M40 27C38 20 41 12 48 7C52 4.5 58 4 63 3.5C60 6 58.5 8 58.5 10.5C56 10 54 11.4 54.6 14"
          "C52 13.6 50.4 15.4 51.4 18C49 18 47.6 20 48.6 22.6C47 22.8 46 24.6 47 27Z", red),
        F("M44 27C45 19 51 12 58 9.6C62 8.2 67 8.6 71 8.6C68 10.4 66.8 12.4 67.2 14.4C64.6 14 62.6 15.4 63.2 18"
          "C60.6 17.8 59 19.6 59.6 22.2C57.2 22.2 55.6 24 56.6 27Z", red),
        # body
        F("M34 30C36 25 44 24.6 52 25.4C58 26 64 25 67.4 28C70 30.4 68.6 35.6 64 37.4C58 39.4 48 39.6 42 38.8"
          "C37 38 33 35 34 30Z", red),
        # neck and head (facing the hoist), open mouth with tongue
        F("M34 32C31 28 30 23 28.6 19.6L33.6 17.6C35 21.4 37.6 25 40 27.6Z", red),
        F("M26 13.6C28.6 12 32.4 12.6 34.4 15.2C35.6 17 34.6 20.2 32.4 20.8C30 21.4 28 20 26.4 19.4"
          "L19 20.6L22.2 18.6L18.6 17L23.6 16.4L20.6 14.2Z", red),
        lines("M23 18.2L16 19.4", red, 0.8),
        poly([(14.6, 19.6), (16.8, 18.2), (16.6, 20.6)], red),
        poly([(28.8, 13.2), (30.4, 9), (31.4, 13.4)], red), poly([(31.6, 13.8), (34.6, 10.6), (34, 15)], red),
        circ(29.4, 15.6, 0.75, "#fff"),
        # legs: front leg raised forward, the others standing
        lines("M38 33.6L31 33.4L27.6 36.2", red, 3),
        lines("M27.6 36.2L25.4 38.4M27.6 36.2L25.6 36.4M27.6 36.2L27 39", red, 1),
        lines("M42 36L41 43.6L37.2 46.4", red, 3.2),
        lines("M37.2 46.4L34.6 47.6M37.2 46.4L35.4 49M37.2 46.4L38 49.4", red, 1.1),
        lines("M60 35.6L63.8 41.6L59.6 46.6", red, 3.4),
        lines("M59.6 46.6L57 47.8M59.6 46.6L58 49.4M59.6 46.6L60.6 49.6", red, 1.1),
        lines("M66 34L71.6 39L68.6 45", red, 3),
        lines("M68.6 45L66.4 46.6M68.6 45L67.6 47.8M68.6 45L69.8 47.8", red, 1),
        # spikes along the back
        poly([(42, 25.2), (44, 22.6), (46, 25)], red), poly([(48, 25), (50, 22.6), (52, 25.2)], red),
    ]
    return "".join(parts)


def wales():
    return rect(0, 0, 100, 30, "#fff") + rect(0, 30, 100, 30, "#00B140") + welsh_dragon()


# ================================================================ X / Y
def xray():
    return (rect(0, 0, SIG_W, SIG_H, "#fff") + rect(SIG_W / 2 - 6, 0, 12, SIG_H, SIG_BLUE)
            + rect(0, SIG_H / 2 - 6, SIG_W, 12, SIG_BLUE))


def yankee():
    box = rect_pts(0, 0, SIG_W, SIG_H)
    n = 10
    step = (SIG_W + SIG_H) / n
    out = []
    for i in range(n):
        piece = clip_half(clip_half(box, 1, 1, i * step), -1, -1, -(i + 1) * step - 0.05)
        out.append(poly(piece, SIG_YEL if i % 2 == 0 else SIG_RED))
    return "".join(out)


# ================================================================ Z
ZIM_BIRD = ("M2290 4580c-18-45-15-95 8-138 23-42 65-72 113-80 51-9 102-12 154-11 49-76 131-125 221-132 90-6 178 30 238 98"
            " 71 81 113 183 122 290l37 464 1412 1105a86 86 0 0 1-76 150l-59-17c-227 141-395 387-428 651l-85 672H2454"
            "l-198-769c-71-86-81-207-25-303 73-125 161-241 262-345 66-66 96-160 83-253-14-92-21-185-22-278-1-77 16-154"
            " 49-223l-19-694c-3-82-48-157-119-197z")


def zimbabwe():
    box = rect_pts(0, 0, 126, 63)
    tri = [(0, 0), (42, 31.5), (0, 63)]
    out = [hstripes(126, 63, ["#319208", "#FFD200", "#DE2010", "#000", "#DE2010", "#FFD200", "#319208"]),
           poly(clip_convex(offset_poly(tri, -1.5), box), "#000"), poly(tri, "#fff"),
           star(16, 29.85, 14, "#DE2010", inner=0.382),
           T("scale(0.005)", P(ZIM_BIRD, "#FFD200", "#000", 40)),
           T("scale(0.005)", circ(2799, 4459, 70, "#000"))]
    return "".join(out)


def zanzibar():
    canton = rect_pts(0, 0, 9, 6)
    return "".join([
        rect(0, 0, 27, 6, "#0093CD"), rect(0, 6, 27, 6, "#000"), rect(0, 12, 27, 6, "#1EB53A"),
        rect(0, 0, 9, 6, "#1EB53A"), poly([(0, 6), (9, 0), (9, 6)], "#00A3DD"),
        poly(clip_convex(band((0, 6), (9, 0), -1.19, 1.19, 1), canton), "#FCD116"),
        poly(clip_convex(band((0, 6), (9, 0), -0.81, 0.81, 1), canton), "#000"),
    ])


def zulu():
    c = (SIG_W / 2, SIG_H / 2)
    return "".join([
        poly([(0, 0), c, (0, SIG_H)], "#000"),
        poly([(0, 0), (SIG_W, 0), c], SIG_YEL),
        poly([(SIG_W, 0), (SIG_W, SIG_H), c], SIG_BLUE),
        poly([(0, SIG_H), c, (SIG_W, SIG_H)], SIG_RED),
    ])


def add_more(K):
    sig = dict(ratio=SIG_W / SIG_H)
    K.add("M", "Madagascar", "Salama! Funny lemurs live here!", on_pole(90, 60, madagascar()))
    K.add("M", "Malaysia", "Apa khabar! Orangutans swing in the trees!", on_pole(28, 14, malaysia()))
    K.add("M", "Morocco", "Salam! Camels and yummy mint tea!", on_pole(90, 60, morocco()))

    K.add("N", "New Zealand", "Kia ora! Kiwi birds live here!", on_pole(120, 60, new_zealand()))
    K.add("N", "Nigeria", "Sannu! Yummy jollof rice!", on_pole(120, 60, vstripes(120, 60, ["#008751", "#fff", "#008751"])))

    K.add("O", "Olympic flag", "Five rings for sports friends!", on_pole(90, 60, olympic()))
    K.add("O", "Oscar flag", "Sailors wave this flag for O!", on_pole(SIG_W, SIG_H, oscar(), **sig))

    K.add("P", "Poland", "Hello! Yummy pierogi dumplings!", on_pole(8, 5, hstripes(8, 5, ["#fff", "#DC143C"])))
    K.add("P", "Pakistan", "Salaam! Very tall snowy mountains!", on_pole(120, 80, pakistan()))

    K.add("Q", "Quebec", "Bonjour! Snowy winters and maple syrup!", on_pole(9600, 6400, quebec()))

    K.add("R", "Russia", "Privet! Big brown bears live here!", on_pole(90, 60, hstripes(90, 60, ["#fff", "#0039A6", "#D52B1E"])))
    K.add("R", "Romania", "Salut! Castles in the mountains!", on_pole(90, 60, vstripes(90, 60, ["#002B7F", "#FCD116", "#CE1126"])))

    K.add("S", "Spain", "Hola! Yummy oranges and paella!", on_pole(90, 60, spain()))
    K.add("S", "Switzerland", "Gruezi! Mountains and yummy cheese!", on_pole(32, 32, switzerland(), ratio=1))

    K.add("T", "Turkey", "Merhaba! Hot air balloons fly here!", on_pole(90, 60, turkey()))
    K.add("T", "Tunisia", "Aslema! Camels in the sandy desert!", on_pole(120, 80, tunisia()))

    K.add("U", "Ukraine", "Pryvit! Big fields of sunflowers!", on_pole(90, 60, hstripes(90, 60, ["#0057B7", "#FFD700"])))
    K.add("U", "Uganda", "Oli otya! Gorillas live in the forest!", on_pole(90, 60, uganda()))

    K.add("V", "Venezuela", "Hola! The tallest waterfall in the world!", on_pole(90, 60, venezuela()))
    K.add("V", "Vanuatu", "Halo! Sunny islands and coconuts!", on_pole(950, 570, vanuatu()))

    K.add("W", "Wales", "Shwmae! A big red dragon!", on_pole(100, 60, wales()))

    K.add("X", "X-ray flag", "Sailors wave this flag for X!", on_pole(SIG_W, SIG_H, xray(), **sig))
    K.add("Y", "Yankee flag", "Sailors wave this flag for Y!", on_pole(SIG_W, SIG_H, yankee(), **sig))

    K.add("Z", "Zimbabwe", "Mhoro! Big elephants live here!", on_pole(126, 63, zimbabwe()))
    K.add("Z", "Zanzibar", "Jambo! Sunny beaches and spices!", on_pole(27, 18, zanzibar()))
    K.add("Z", "Zulu flag", "Sailors wave this flag for Z!", on_pole(SIG_W, SIG_H, zulu(), **sig))
