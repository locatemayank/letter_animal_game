"""Extra Countries flags A-L.

Drawn in each flag's own native units (see countries_kit.on_pole).  Colours and layout follow
the official flags; the coats of arms (Dominican Republic, Ecuador, Fiji, Haiti) and the
Dominica parrot / Kiribati bird are simplified so they read at picture size.
"""
import math
from svgkit import *
from countries_kit import *


# ---------------------------------------------------------------- small helpers
def ring_stars(cx, cy, R, r, n, fill, inner=0.382):
    """n five-pointed stars on a circle, each pointing outwards."""
    out = []
    for k in range(n):
        a = -90 + k * 360 / n
        x, y = cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))
        out.append(star(x, y, r, fill, inner=inner, rot=a))
    return "".join(out)


def wave_band(W, yc, amp, period, phase, half, x0=0.0, x1=None, step=None):
    """Horizontal wavy band (polygon) between x0..x1, centre line y = yc - amp*sin(...)."""
    x1 = W if x1 is None else x1
    step = step or (x1 - x0) / 60
    xs = []
    x = x0
    while x < x1:
        xs.append(x)
        x += step
    xs.append(x1)
    f = lambda x: yc - amp * math.sin(2 * math.pi * (x - phase) / period)
    top = [(x, f(x) - half) for x in xs]
    bot = [(x, f(x) + half) for x in reversed(xs)]
    return top + bot


# ================================================================ A
def algeria():
    out = [rect(0, 0, 900, 600, "#fff"), rect(0, 0, 450, 600, "#006233")]
    # crescent: outer circle r=150 at (450,300), cut by the circle r=120 at (487.5,300)
    out.append(F("M579.9 225A150 150 0 1 0 579.9 375A120 120 0 1 1 579.9 225Z", "#D21034"))
    out.append(star(510, 300, 75, "#D21034", rot=0))
    return "".join(out)


# ================================================================ B
def botswana():
    return hstripes(90, 60, ["#75AADB", "#fff", "#000", "#fff", "#75AADB"], [9, 1, 4, 1, 9])


# ================================================================ C
def chile():
    return "".join([rect(0, 0, 1500, 500, "#fff"), rect(0, 500, 1500, 500, "#D52B1E"),
                    rect(0, 0, 500, 500, "#0039A6"), star(250, 250, 125, "#fff")])


# ================================================================ D
def djibouti():
    tri = [(0, 0), (519.6, 300), (0, 600)]
    return "".join([rect(0, 0, 900, 300, "#6AB2E7"), rect(0, 300, 900, 300, "#12AD2B"),
                    poly(tri, "#fff"), star(173, 300, 72, "#D7141A")])


def dr_arms(cx, cy, s):
    """Simplified coat of arms: laurel + palm branches, shield with flags, a little Bible and cross."""
    g, blue, red = "#2e8b3a", "#002D62", "#CE1126"
    out = []
    # branches around the shield
    out.append(lines(f"M{cx - 9} {cy - 7}Q{cx - 13} {cy + 3} {cx - 3} {cy + 11}", g, 2.2))
    out.append(lines(f"M{cx + 9} {cy - 7}Q{cx + 13} {cy + 3} {cx + 3} {cy + 11}", g, 2.2))
    for t in (0.2, 0.45, 0.7):
        for sgn in (-1, 1):
            x = cx + sgn * (11.5 - 2 * t)
            y = cy - 7 + 18 * t
            out.append(E(round(x, 2), round(y, 2), 2.4, 1.1, g, g, 0.1, rot=round(sgn * (40 + 30 * t), 1)))
    # ribbons: blue above, red below
    out.append(F(f"M{cx - 9} {cy - 13}Q{cx} {cy - 16} {cx + 9} {cy - 13}L{cx + 9} {cy - 10.6}Q{cx} {cy - 13.6} {cx - 9} {cy - 10.6}Z", blue))
    out.append(F(f"M{cx - 9} {cy + 12}Q{cx} {cy + 15} {cx + 9} {cy + 12}L{cx + 9} {cy + 14.4}Q{cx} {cy + 17.4} {cx - 9} {cy + 14.4}Z", red))
    # shield in the flag's colours
    sh = f"M{cx - 7} {cy - 9}H{cx + 7}V{cy + 2}C{cx + 7} {cy + 7} {cx + 2} {cy + 9} {cx} {cy + 10.5}C{cx - 2} {cy + 9} {cx - 7} {cy + 7} {cx - 7} {cy + 2}Z"
    out.append(F(sh, "#fff"))
    out.append(F(f"M{cx - 7} {cy - 9}H{cx - 1.3}V{cy - 1.3}H{cx - 7}Z", blue))
    out.append(F(f"M{cx + 1.3} {cy - 9}H{cx + 7}V{cy - 1.3}H{cx + 1.3}Z", red))
    out.append(F(f"M{cx - 7} {cy + 1.3}H{cx - 1.3}V{cy + 9.2}C{cx - 4} {cy + 7.5} {cx - 7} {cy + 6} {cx - 7} {cy + 2}Z", red))
    out.append(F(f"M{cx + 1.3} {cy + 1.3}H{cx + 7}V{cy + 2}C{cx + 7} {cy + 6} {cx + 4} {cy + 7.5} {cx + 1.3} {cy + 9.2}Z", blue))
    out.append(f'<path d="{sh}" fill="none" stroke="#b8860b" stroke-width="0.6"/>')
    # open Bible with a small gold cross above it
    out.append(F(f"M{cx - 3.4} {cy - 0.6}Q{cx - 1.7} {cy - 1.6} {cx} {cy - 0.6}Q{cx + 1.7} {cy - 1.6} {cx + 3.4} {cy - 0.6}"
                 f"V{cy + 2.6}Q{cx + 1.7} {cy + 1.6} {cx} {cy + 2.6}Q{cx - 1.7} {cy + 1.6} {cx - 3.4} {cy + 2.6}Z", "#fff")
               .replace('fill="#fff"', 'fill="#fff" stroke="#8a6a00" stroke-width="0.4" stroke-linejoin="round"'))
    out.append(f'<path d="M{cx} {cy - 0.6}V{cy + 2.6}" stroke="#8a6a00" stroke-width="0.4"/>')
    out.append(F(f"M{cx - 0.45} {cy - 6}H{cx + 0.45}V{cy - 4.6}H{cx + 1.5}V{cy - 3.7}H{cx + 0.45}V{cy - 1.4}H{cx - 0.45}V{cy - 3.7}H{cx - 1.5}V{cy - 4.6}H{cx - 0.45}Z", "#E0A800"))
    return "".join(out)


def dominican_republic():
    # 900 x 600, cross width 150 (one sixth of the length)
    blue, red = "#002D62", "#CE1126"
    out = [rect(0, 0, 900, 600, "#fff"),
           rect(0, 0, 375, 225, blue), rect(525, 0, 375, 225, red),
           rect(0, 375, 375, 225, red), rect(525, 375, 375, 225, blue)]
    out.append(T("translate(450 300) scale(9) translate(-50 -50)", dr_arms(50, 50, 1)))
    return "".join(out)


def dominica():
    green, yel, red = "#046A38", "#FFCD00", "#D50032"
    purple = "#9063CD"
    out = [rect(0, 0, 48, 24, green),
           rect(0, 9, 48, 3, yel), rect(21, 0, 3, 24, yel),
           rect(0, 12, 48, 3, "#fff"), rect(24, 0, 3, 24, "#fff"),
           rect(0, 11, 48, 2, "#000"), rect(23, 0, 2, 24, "#000"),
           circ(24, 12, 6, red)]
    out.append(ring_stars(24, 12, 4.5, 0.84, 10, green))
    # Sisserou parrot (simplified): on a branch, head turned to the hoist
    c = lambda x, y: (24 + x, 12 + y)
    px, py = 24, 12
    p = []
    p.append(F(f"M{px - 1.8} {py + 2.55}H{px + 1.6}V{py + 2.95}H{px - 1.8}Z", "#9C4A00"))                     # branch
    p.append(F(f"M{px + 0.6} {py + 0.6}L{px + 1.9} {py + 3.1}L{px + 1.2} {py + 3.2}L{px + 0.1} {py + 1.2}Z", green))  # tail
    p.append(F(f"M{px - 0.6} {py - 2.0}C{px - 1.4} {py - 1} {px - 1.3} {py + 1.2} {px + 0.2} {py + 2.2}"
               f"L{px + 0.9} {py + 2.2}C{px + 1.4} {py + 0.6} {px + 1.0} {py - 1.6} {px - 0.6} {py - 2.0}Z", purple))   # body
    p.append(F(f"M{px - 0.1} {py - 1.5}C{px + 1.3} {py - 1.2} {px + 1.6} {py + 0.6} {px + 1.1} {py + 2.0}"
               f"C{px + 0.5} {py + 1.0} {px} {py} {px - 0.1} {py - 1.5}Z", green))                                    # wing
    p.append(E(round(px - 0.7, 2), round(py - 2.45, 2), 0.9, 0.75, purple, purple, 0.05))                         # head
    p.append(F(f"M{px - 1.45} {py - 2.75}Q{px - 2.2} {py - 2.5} {px - 1.75} {py - 1.85}L{px - 1.35} {py - 2.2}Z", yel))  # beak
    p.append(circ(px - 0.95, py - 2.6, 0.22, "#000"))
    p.append(F(f"M{px - 0.4} {py + 2.2}l0.15 0.5h0.3l0.15-0.5ZM{px + 0.3} {py + 2.2}l0.15 0.5h0.3l0.15-0.5Z", yel))  # feet
    out.append("".join(p))
    return "".join(out)


# ================================================================ E
def ethiopia():
    out = [hstripes(1200, 600, ["#078930", "#FCDD09", "#DA121A"]), circ(600, 300, 200, "#0F47AF")]
    gold = "#FCDD09"
    R = 135
    pts = [(600 + R * math.cos(math.radians(-90 + 144 * k)), 300 + R * math.sin(math.radians(-90 + 144 * k))) for k in range(5)]
    d = "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts) + "Z"
    out.append(f'<path d="{d}" fill="none" stroke="{gold}" stroke-width="16" stroke-linejoin="miter"/>')
    rays = ""
    for k in range(5):
        a = math.radians(-90 + 36 + 72 * k)
        r1, r2 = 0.5 * R, 1.12 * R
        rays += f"M{fmt(600 + r1 * math.cos(a))} {fmt(300 + r1 * math.sin(a))}L{fmt(600 + r2 * math.cos(a))} {fmt(300 + r2 * math.sin(a))}"
    out.append(lines(rays, gold, 14, "butt"))
    return "".join(out)


def ecuador_arms(cx, cy):
    yel, blue, red = "#FFDD00", "#034EA2", "#ED1C24"
    gold, dark = "#C8A200", "#2b2b2b"
    out = []
    # draped flags on both sides
    for sgn in (-1, 1):
        x0 = cx + sgn * 6
        x1 = cx + sgn * 13
        for i, col in enumerate((yel, blue, red)):
            a = x0 + sgn * 2.3 * i
            b = x0 + sgn * 2.3 * (i + 1)
            out.append(F(f"M{fmt(a)} {cy - 9}L{fmt(b)} {cy - 9}Q{fmt(b + sgn * 2)} {cy + 2} {fmt(b - sgn * 2.5)} {cy + 12}"
                         f"L{fmt(a - sgn * 2.5)} {cy + 12}Q{fmt(a + sgn * 2)} {cy + 2} {fmt(a)} {cy - 9}Z", col))
        out.append(lines(f"M{fmt(x0)} {cy - 9.5}L{fmt(x1 - sgn * 1)} {cy - 10.5}", "#7a4a1a", 0.7))
    # oval with sky, sun, snowy mountain, river
    out.append(E(cx, cy, 7, 9, gold, gold, 0.1))
    out.append(E(cx, cy, 6, 8, "#8fd3f4", "#8fd3f4", 0.1))
    out.append(circ(cx, cy - 4.2, 1.8, "#FFC400"))
    out.append(F(f"M{cx - 6} {cy + 3.5}L{cx - 1.5} {cy - 2}L{cx + 1} {cy}L{cx + 6} {cy + 3.5}Z", "#2e8b3a"))
    out.append(F(f"M{cx - 3} {cy - 0.2}L{cx - 1.5} {cy - 2}L{cx - 0.2} {cy - 0.5}Z", "#fff"))
    out.append(F(f"M{cx - 5.8} {cy + 3.5}H{cx + 5.8}C{cx + 5.2} {cy + 6} {cx + 3} {cy + 8} {cx} {cy + 8}"
                 f"C{cx - 3} {cy + 8} {cx - 5.2} {cy + 6} {cx - 5.8} {cy + 3.5}Z", "#2a7fd4"))
    out.append(F(f"M{cx - 1.6} {cy + 4.6}H{cx + 1.8}L{cx + 1.1} {cy + 5.6}H{cx - 1}Z", "#7a4a1a"))
    # condor on top with spread wings
    out.append(F(f"M{cx} {cy - 8.5}C{cx - 4} {cy - 10} {cx - 9} {cy - 9.5} {cx - 13} {cy - 12.5}"
                 f"C{cx - 11} {cy - 13.6} {cx - 5} {cy - 13.5} {cx - 1.2} {cy - 11.6}"
                 f"L{cx} {cy - 13.5}L{cx + 1.2} {cy - 11.6}"
                 f"C{cx + 5} {cy - 13.5} {cx + 11} {cy - 13.6} {cx + 13} {cy - 12.5}"
                 f"C{cx + 9} {cy - 9.5} {cx + 4} {cy - 10} {cx} {cy - 8.5}Z", dark))
    out.append(lines(f"M{cx - 10.5} {cy - 12.2}Q{cx - 6} {cy - 11.4} {cx - 2.5} {cy - 10.6}"
                     f"M{cx + 10.5} {cy - 12.2}Q{cx + 6} {cy - 11.4} {cx + 2.5} {cy - 10.6}", "#fff", 0.45))
    out.append(circ(cx, cy - 13.6, 1.1, dark))
    out.append(circ(cx, cy - 12.4, 0.75, "#fff"))
    return "".join(out)


def ecuador():
    return hstripes(90, 60, ["#FFDD00", "#034EA2", "#ED1C24"], [2, 1, 1]) + \
        T("translate(45 30) scale(1.3) translate(-45 -30)", ecuador_arms(45, 30))


# ================================================================ F
def fiji_shield(cx, top):
    red, gold, green = "#CE1126", "#FFD100", "#2e7d32"
    w, h = 12.0, 32.0
    x0, x1 = cx - w, cx + w
    bot = top + h
    sh = f"M{x0} {top}H{x1}V{top + 16}C{x1} {top + 25} {cx + 5} {bot - 2} {cx} {bot}C{cx - 5} {bot - 2} {x0} {top + 25} {x0} {top + 16}Z"
    out = [F(sh, "#fff")]
    chief = top + 8
    out.append(rect(x0, top, 2 * w, 8, red))
    # gold lion holding a cocoa pod
    ly = top + 4.6
    out.append(F(f"M{cx - 7} {ly + 1.5}C{cx - 7} {ly - 1.5} {cx + 2} {ly - 1.8} {cx + 3} {ly - 0.5}"
                 f"L{cx + 4} {ly - 2.6}C{cx + 6} {ly - 3.2} {cx + 7} {ly - 1} {cx + 6} {ly + 0.6}"
                 f"L{cx + 5} {ly + 2.5}H{cx + 3.6}L{cx + 3} {ly + 0.8}H{cx - 4}L{cx - 4.6} {ly + 2.5}H{cx - 6}Z", gold))
    out.append(lines(f"M{cx - 7} {ly + 0.6}Q{cx - 9} {ly - 1} {cx - 8.4} {ly - 2.8}", gold, 0.8))
    out.append(E(cx + 7.6, ly - 1.2, 0.9, 1.4, "#8d5524", "#8d5524", 0.1))
    # red cross
    cy = chief + 10
    out.append(rect(cx - 1.4, chief, 2.8, bot - chief - 0.2, red))
    out.append(rect(x0, cy - 1.4, 2 * w, 2.8, red))
    # quarters: sugar cane, coconut palm, dove, bananas
    ax, ay = cx - 6, chief + 5
    out.append(lines(f"M{ax - 2} {ay + 4}L{ax - 2} {ay - 4}M{ax} {ay + 4}L{ax} {ay - 4.4}M{ax + 2} {ay + 4}L{ax + 2} {ay - 4}", green, 1))
    out.append(lines(f"M{ax - 2} {ay - 1}h0.01M{ax} {ay}h0.01M{ax + 2} {ay - 1}h0.01", "#1b5e20", 1.2))
    bx, by = cx + 6, chief + 5
    out.append(lines(f"M{bx + 0.5} {by + 4}Q{bx} {by} {bx} {by - 2.5}", "#8d5524", 1))
    out.append(lines(f"M{bx} {by - 2.5}Q{bx - 2.5} {by - 4} {bx - 4} {by - 1.5}M{bx} {by - 2.5}Q{bx + 2.5} {by - 4} {bx + 4} {by - 1.5}"
                     f"M{bx} {by - 2.5}Q{bx - 1} {by - 4.6} {bx - 2.6} {by - 4.6}M{bx} {by - 2.5}Q{bx + 1} {by - 4.6} {bx + 2.6} {by - 4.6}", green, 1))
    dx_, dy_ = cx - 5.8, cy + 5
    out.append(F(f"M{dx_ - 3} {dy_}C{dx_ - 1.5} {dy_ - 2.2} {dx_ + 1} {dy_ - 2} {dx_ + 2} {dy_ - 0.6}L{dx_ + 3.4} {dy_ - 1.4}"
                 f"L{dx_ + 2.6} {dy_ + 0.2}C{dx_ + 1.6} {dy_ + 1.8} {dx_ - 1} {dy_ + 1.8} {dx_ - 3} {dy_}Z", "#cfd8dc"))
    out.append(lines(f"M{dx_ - 1} {dy_ - 1}L{dx_ + 1.2} {dy_ - 3}", "#cfd8dc", 0.9))
    out.append(lines(f"M{dx_ + 3.4} {dy_ - 1.2}L{dx_ + 4.4} {dy_ - 1.8}", green, 0.6))
    ex, ey = cx + 5.6, cy + 4.6
    for k in range(4):
        out.append(E(round(ex - 2.4 + 1.6 * k, 2), ey, 0.7, 2, "#f9c80e", "#c99a00", 0.25, rot=round(-20 + 13 * k, 1)))
    out.append(lines(f"M{ex - 3} {ey - 2.4}Q{ex} {ey - 3.6} {ex + 3} {ey - 2.4}", "#2e7d32", 0.7))
    out.append(f'<path d="{sh}" fill="none" stroke="#444" stroke-width="0.5"/>')
    return "".join(out)


def fiji():
    return rect(0, 0, 120, 60, "#68BFE5") + union_jack() + fiji_shield(90, 14.5)


# ================================================================ G
def georgia():
    red = "#FF0000"
    out = [rect(0, 0, 300, 200, "#fff"), rect(130, 0, 40, 200, red), rect(0, 80, 300, 40, red)]

    def bolnur(x, y):
        """Bolnur-katskhuri cross: four arms that flare out with concave sides."""
        s, w, c = 26.0, 9.0, 3.5     # half span, half width at the tips, half width at the centre
        d = f"M{fmt(x - c)} {fmt(y - c)}"
        for k in range(4):
            # rotate the top arm (drawn for k=0) by k*90 degrees
            co, si = [(1, 0), (0, 1), (-1, 0), (0, -1)][k]
            rot = lambda px, py: (x + px * co - py * si, y + px * si + py * co)
            pts = [(-c * 1.1, -s * 0.6), (-w, -s), (w, -s), (c * 1.1, -s * 0.6), (c, -c)]
            (q1, a, b, q2, e) = [rot(*p) for p in pts]
            d += (f"Q{fmt(q1[0])} {fmt(q1[1])} {fmt(a[0])} {fmt(a[1])}L{fmt(b[0])} {fmt(b[1])}"
                  f"Q{fmt(q2[0])} {fmt(q2[1])} {fmt(e[0])} {fmt(e[1])}")
        return F(d + "Z", red)
    for x, y in ((65, 40), (235, 40), (65, 160), (235, 160)):
        out.append(bolnur(x, y))
    return "".join(out)


# ================================================================ H
def honduras():
    blue = "#00BCE4"
    out = [hstripes(72, 36, [blue, "#fff", blue])]
    for x, y in ((36, 18), (28, 14.6), (28, 21.4), (44, 14.6), (44, 21.4)):
        out.append(star(x, y, 2.1, blue))
    return "".join(out)


def haiti():
    out = [rect(0, 0, 100, 30, "#00209F"), rect(0, 30, 100, 30, "#D21034")]
    px, py, pw, ph = 35.5, 18.5, 29, 23
    out.append(rect(px, py, pw, ph, "#fff"))
    cx = 50
    g = "#2e8b3a"
    # flags on both sides (blue over red), on little poles
    for sgn in (-1, 1):
        for k, ang in enumerate((26, 44)):
            a = math.radians(ang)
            bx, by = cx + sgn * 2.5, py + 18.5
            tx, ty = bx + sgn * 11 * math.sin(a), by - 11 * math.cos(a)
            out.append(lines(f"M{fmt(bx)} {fmt(by)}L{fmt(tx)} {fmt(ty)}", "#7a4a1a", 0.5))
            fx = tx - sgn * 0.2
            out.append(poly([(fx, ty), (fx - sgn * 4.4, ty + 0.8), (fx - sgn * 4.4, ty + 2.6), (fx, ty + 1.8)], "#00209F"))
            out.append(poly([(fx, ty + 1.8), (fx - sgn * 4.4, ty + 2.6), (fx - sgn * 4.4, ty + 4.4), (fx, ty + 3.6)], "#D21034"))
    # palm tree with the cap of liberty
    out.append(F(f"M{cx - 0.8} {py + 19}L{cx - 0.45} {py + 6}H{cx + 0.45}L{cx + 0.8} {py + 19}Z", "#8d5524"))
    fr = ""
    for ang in (-150, -120, -60, -30, -170, -10):
        a = math.radians(ang)
        ex, ey = cx + 6 * math.cos(a), py + 6 + 4 * math.sin(a) + 2.2
        mx, my = cx + 3.2 * math.cos(a), py + 6 + 3.2 * math.sin(a) - 0.6
        fr += f"M{cx} {py + 6}Q{fmt(mx)} {fmt(my)} {fmt(ex)} {fmt(ey)}"
    out.append(lines(fr, "#1b7a2b", 1.1))
    out.append(F(f"M{cx - 1.2} {py + 5.3}Q{cx - 1} {py + 2.4} {cx + 1} {py + 2.6}L{cx + 1.4} {py + 3.6}L{cx + 1.2} {py + 5.3}Z", "#D21034"))
    # cannon balls / drum and the green lawn
    out.append(F(f"M{px + 1} {py + 19.3}Q{cx} {py + 16.6} {px + pw - 1} {py + 19.3}V{py + 21}H{px + 1}Z", g))
    out.append(rect(cx - 1.6, py + 16.4, 3.2, 2.2, "#D21034"))
    out.append(lines(f"M{cx - 9} {py + 18.3}L{cx - 4.5} {py + 17.4}M{cx + 9} {py + 18.3}L{cx + 4.5} {py + 17.4}", "#333", 1.1))
    out.append(F(f"M{cx - 9} {py + 20.4}Q{cx} {py + 22.4} {cx + 9} {py + 20.4}V{py + 21.6}Q{cx} {py + 23.4} {cx - 9} {py + 21.6}Z", "#fff"))
    return "".join(out)


# ================================================================ I
def iceland():
    return "".join([rect(0, 0, 25, 18, "#02529C"), rect(7, 0, 4, 18, "#fff"), rect(0, 7, 25, 4, "#fff"),
                    rect(8, 0, 2, 18, "#DC1E35"), rect(0, 8, 25, 2, "#DC1E35")])


# ================================================================ J
def jordan():
    out = [hstripes(120, 60, ["#000", "#fff", "#007A3D"]), poly([(0, 0), (60, 30), (0, 60)], "#CE1126")]
    out.append(star(19, 30, 6, "#fff", n=7, inner=0.5))
    return "".join(out)


# ================================================================ K
def korea():
    red, blue, blk = "#CD2E3A", "#0047A0", "#000"
    ang = math.degrees(math.atan2(2, 3))           # 33.69: the diagonal of a 3:2 flag
    tg = "".join([F("M0-12A12 12 0 0 1 0 12Z", red), F("M0-12A12 12 0 0 0 0 12Z", blue),
                  circ(0, -6, 6, red), circ(0, 6, 6, blue)])

    def tri(y0, pattern):
        """Trigram: three bars at y0, y0+3, y0+6 (bar 2 thick, 12 long); pattern 1 = solid, 0 = broken."""
        o = ""
        for i, solid in enumerate(pattern):
            y = y0 + 3 * i - 1
            o += rect(-6, y, 12, 2, blk) if solid else rect(-6, y, 5.5, 2, blk) + rect(0.5, y, 5.5, 2, blk)
        return o
    a1 = -(90 - ang)        # axis "up" points to the upper hoist corner
    a2 = 90 - ang           # axis "up" points to the upper fly corner
    body = (T(f"rotate({fmt(a1)})", tg, tri(-25, (1, 1, 1)), tri(19, (0, 0, 0)))
            + T(f"rotate({fmt(a2)})", tri(-25, (0, 1, 0)), tri(19, (1, 0, 1))))
    return rect(0, 0, 72, 48, "#fff") + T("translate(36 24)", body)


def kuwait():
    return hstripes(12, 6, ["#007A3D", "#fff", "#CE1126"]) + poly([(0, 0), (3, 2), (3, 4), (0, 6)], "#000")


def kiribati():
    red, gold, blue, ink = "#C81010", "#F8D000", "#183070", "#3b2a1e"
    out = [rect(0, 0, 600, 300, red)]
    # rising sun: 17 rays (alternately straight and wavy) and the disc
    rays = []
    for k in range(17):
        a = -84.706 + k * 21.176
        base = 9.37
        if k % 2 == 0:
            pts = [(-base, 50.1), (0, 93), (base, 50.1)]
            d = pd([(300 + x * math.cos(math.radians(a)) - (-y) * math.sin(math.radians(a)),
                     156 + x * math.sin(math.radians(a)) + (-y) * math.cos(math.radians(a))) for x, y in pts])
            rays.append(f'<path d="{d}" fill="{gold}" stroke="{ink}" stroke-width="1.2" stroke-linejoin="round"/>')
        else:
            rays.append(T(f"rotate({fmt(a + 13.4)} 300 156)",
                          f'<path d="M290.63 105.87A50 50 0 0 1 300 66A50 50 0 0 0 309.37 105.87Z" fill="{gold}" stroke="{ink}" stroke-width="1.2" stroke-linejoin="round" transform="rotate(-13.4 300 156)"/>'))
    out += rays
    out.append(f'<circle cx="300" cy="156" r="51" fill="{gold}" stroke="{ink}" stroke-width="1.2"/>')
    # frigate bird (official outline)
    bird = ("M305.75 27.34c-19.08-7.89-30.76-9.34-43.81-9.47-18.9 0.13-27.92 8.25-45.94 9 7.14 7.69 33.02 9.57 43.93-0.53 "
            "16.22 1.69 19.9 6.07 24.25 11.52-6.77-1.07-14.57-3.02-21.04 4.14-5.46 1.1-7.99 0-17.33 0-4.36 0-5.87 2.14-5.81 6 "
            "2.82-3.9 22.31-1.6 27.09 0 3.67 1.23 7.57 6.32 12.22 7.15 12.19 2.17 29.68-4.2 45.81-8.54l34.88-4.61-23.93 0 29.93-6"
            "c-13.93 0-23.11 0-32.54 0-0.69-0.79-2.34-1.81-3.66-2.68 8.37-5.39 15.77-15.19 17.66-19.92 15.09-0.15 24.83-1.55 "
            "36.54-4.29-77.18-8.54-59.61 0.67-78.25 18.23z")
    out.append(f'<path d="{bird}" fill="{gold}" stroke="{ink}" stroke-width="1.2" stroke-linejoin="round"/>')
    out.append(circ(270.06, 41.39, 2.2, ink))
    # sea: blue with three white waves
    out.append(rect(0, 162, 600, 138, blue))
    for yc in (168, 216, 264):
        out.append(poly(wave_band(600, yc, 6, 120, -36, 12, step=5), "#fff"))
    return "".join(out)


# ================================================================ L
# (stripes only - see add_more)


# ================================================================ add them
def add_more(K):
    # A
    K.add("A", "Austria", "Servus! Snowy mountains for skiing!", on_pole(90, 60, hstripes(90, 60, ["#C8102E", "#fff", "#C8102E"])))
    K.add("A", "Algeria", "Marhaba! Camels in the big Sahara!", on_pole(900, 600, algeria()))
    # B
    K.add("B", "Belgium", "Bonjour! Yummy waffles and chocolate!", on_pole(15, 13, vstripes(15, 13, ["#000", "#FDDA24", "#EF3340"])))
    K.add("B", "Bangladesh", "Nomoshkar! Bengal tigers live here!", on_pole(10, 6, rect(0, 0, 10, 6, "#006A4E") + circ(4.5, 3, 2, "#F42A41")))
    K.add("B", "Botswana", "Dumela! So many elephants live here!", on_pole(90, 60, botswana()))
    # C
    K.add("C", "Chile", "Hola! Penguins and tall mountains!", on_pole(1500, 1000, chile()))
    K.add("C", "Colombia", "Hola! Lots of colourful birds!", on_pole(90, 60, hstripes(90, 60, ["#FCD116", "#003893", "#CE1126"], [2, 1, 1])))
    # D
    K.add("D", "Djibouti", "Salaam! Big whale sharks swim here!", on_pole(900, 600, djibouti()))
    K.add("D", "Dominican Republic", "Hola! Sunny beaches and baseball!", on_pole(900, 600, dominican_republic()))
    K.add("D", "Dominica", "Hello! A purple parrot on the flag!", on_pole(48, 24, dominica()))
    # E
    K.add("E", "Estonia", "Tere! Big green forests!", on_pole(33, 21, hstripes(33, 21, ["#0072CE", "#000", "#fff"])))
    K.add("E", "Ethiopia", "Selam! Funny gelada monkeys live here!", on_pole(1200, 600, ethiopia()))
    K.add("E", "Ecuador", "Hola! Giant tortoises live here!", on_pole(90, 60, ecuador()))
    # F
    K.add("F", "Finland", "Hei! Santa Claus lives in Lapland!", on_pole(18, 11, rect(0, 0, 18, 11, "#fff") + rect(5, 0, 3, 11, "#002F6C") + rect(0, 4, 18, 3, "#002F6C")))
    K.add("F", "Fiji", "Bula! Sunny islands and coral reefs!", on_pole(120, 60, fiji()))
    # G
    K.add("G", "Ghana", "Akwaaba! Yummy chocolate from cocoa!", on_pole(90, 60, hstripes(90, 60, ["#CE1126", "#FCD116", "#006B3F"]) + star(45, 30, 10, "#000")))
    K.add("G", "Georgia", "Gamarjoba! Big snowy mountains!", on_pole(300, 200, georgia()))
    # H
    K.add("H", "Honduras", "Hola! Colourful macaws fly here!", on_pole(72, 36, honduras()))
    K.add("H", "Haiti", "Bonjou! Mangoes and sunny beaches!", on_pole(100, 60, haiti()))
    # I
    K.add("I", "Ireland", "Dia duit! Green fields and sheep!", on_pole(120, 60, vstripes(120, 60, ["#169B62", "#fff", "#FF883E"])))
    K.add("I", "Iceland", "Halló! Puffins and hot springs!", on_pole(25, 18, iceland()))
    # J
    K.add("J", "Jordan", "Marhaba! A city carved in pink rock!", on_pole(120, 60, jordan()))
    # K
    K.add("K", "Korea", "Annyeong! Yummy rice and kimchi!", on_pole(72, 48, korea()))
    K.add("K", "Kuwait", "Marhaba! Tall round towers by the sea!", on_pole(12, 6, kuwait()))
    K.add("K", "Kiribati", "Mauri! Sunny islands in the ocean!", on_pole(600, 300, kiribati()))
    # L
    K.add("L", "Latvia", "Sveiki! White storks build nests here!", on_pole(20, 10, hstripes(20, 10, ["#9E3039", "#fff", "#9E3039"], [2, 1, 2])))
    K.add("L", "Lithuania", "Labas! Sandy dunes by the sea!", on_pole(5, 3, hstripes(5, 3, ["#FDB913", "#006A44", "#C1272D"])))
    K.add("L", "Luxembourg", "Moien! Castles on green hills!", on_pole(5, 3, hstripes(5, 3, ["#EF3340", "#fff", "#00A3E0"])))
