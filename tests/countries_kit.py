"""Flag-drawing helpers shared by countries_make.py and the countries_more_*.py extensions.

All flags: on_pole(native_w, native_h, content) where content is SVG drawn in native flag units
(0..native_w x 0..native_h). No ids, no clipPath: clip with clip_convex / clip_half.
"""
import math
import os
from svgkit import *



# ---------------------------------------------------------------- geometry helpers
def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def pd(pts):
    """Polygon -> path data."""
    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts) + "Z"


def clip_half(poly, nx, ny, c):
    """Keep the part of poly with nx*x + ny*y >= c (Sutherland-Hodgman, one edge)."""
    out = []
    n = len(poly)
    for i in range(n):
        p, q = poly[i], poly[(i + 1) % n]
        fp = nx * p[0] + ny * p[1] - c
        fq = nx * q[0] + ny * q[1] - c
        if fp >= 0:
            out.append(p)
        if (fp >= 0) != (fq >= 0):
            t = fp / (fp - fq)
            out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def area2(poly):
    return sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))


def halfplanes(conv, inset=0.0):
    """Inward half-planes of a convex polygon (optionally moved inwards by `inset`)."""
    s = 1 if area2(conv) > 0 else -1
    hp = []
    for i in range(len(conv)):
        (x1, y1), (x2, y2) = conv[i], conv[(i + 1) % len(conv)]
        nx, ny = -(y2 - y1) * s, (x2 - x1) * s
        ln = math.hypot(nx, ny)
        nx, ny = nx / ln, ny / ln
        hp.append((nx, ny, nx * x1 + ny * y1 + inset))
    return hp


def clip_convex(poly, conv):
    for nx, ny, c in halfplanes(conv):
        poly = clip_half(poly, nx, ny, c)
        if not poly:
            break
    return poly


def rect_pts(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def band(p, q, o1, o2, ext=0.0):
    """Strip along p->q between normal offsets o1..o2 (normal = direction rotated +90deg)."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    nx, ny = -uy, ux
    a = (p[0] - ux * ext, p[1] - uy * ext)
    b = (q[0] + ux * ext, q[1] + uy * ext)
    return [(a[0] + nx * o1, a[1] + ny * o1), (b[0] + nx * o1, b[1] + ny * o1),
            (b[0] + nx * o2, b[1] + ny * o2), (a[0] + nx * o2, a[1] + ny * o2)]


def poly(pts, fill):
    return F(pd(pts), fill) if pts else ""


def star(x, y, r, fill, n=5, inner=0.382, rot=-90):
    return F(star_path(x, y, r, inner=inner, n=n, rot=rot), fill)


def circ(x, y, r, fill):
    return f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{fmt(r)}" fill="{fill}"/>'


def rect(x, y, w, h, fill):
    return f'<rect x="{fmt(x)}" y="{fmt(y)}" width="{fmt(w)}" height="{fmt(h)}" fill="{fill}"/>'


def hstripes(W, H, cols, weights=None):
    weights = weights or [1] * len(cols)
    tot, y, out = sum(weights), 0.0, []
    for c, w in zip(cols, weights):
        h = H * w / tot
        out.append(rect(0, y, W, h + 0.02, c))
        y += h
    return "".join(out)


def vstripes(W, H, cols, weights=None):
    weights = weights or [1] * len(cols)
    tot, x, out = sum(weights), 0.0, []
    for c, w in zip(cols, weights):
        ww = W * w / tot
        out.append(rect(x, 0, ww + 0.02, H, c))
        x += ww
    return "".join(out)


def lines(d, c, w, cap="round"):
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{fmt(w)}" stroke-linecap="{cap}" stroke-linejoin="round"/>'


# ---------------------------------------------------------------- flag on a pole
POLE = "#8d6e63"
GOLDBALL = "#ffca28"
FX, FY, FW, FH = 15.0, 15.0, 80.0, 60.0     # flag area (left/top fixed; size follows ratio)


def on_pole(nw, nh, content, ratio=None, outline=None):
    """Draw flag `content` (native units nw x nh) on a pole.  `outline` = custom shape (native)."""
    ratio = ratio or nw / nh
    w = FW
    h = w / ratio
    if h > FH:
        h = FH
        w = h * ratio
    sx, sy = w / nw, h / nh
    g = f'<g transform="translate({fmt(FX)} {fmt(FY)}) scale({sx:.6g} {sy:.6g})">{content}</g>'
    if outline is None:
        frame = f'<rect x="{fmt(FX)}" y="{fmt(FY)}" width="{fmt(w)}" height="{fmt(h)}" rx="1.5" fill="none" {st()}/>'
    else:
        pts = [(FX + x * sx, FY + y * sy) for x, y in outline]
        frame = f'<path d="{pd(pts)}" fill="none" {st()}/>'
    pole = (R(8.5, 10, 5, 86, POLE, 2.5) + C(11, 9, 4.5, GOLDBALL)
            + E(11, 95, 9, 3, "#a1887f"))
    # little ties that hold the flag on the pole
    ties = (R(10, FY + 1.5, 7, 3.4, "#fff", 1.5, O, 2) + R(10, FY + h - 4.9, 7, 3.4, "#fff", 1.5, O, 2))
    return svg(pole, g, frame, ties)


# ---------------------------------------------------------------- Union Jack (native 60 x 30)
def union_jack(red="#C8102E", blue="#012169"):
    box = rect_pts(0, 0, 60, 30)
    out = [rect(0, 0, 60, 30, blue)]
    for p, q in (((0, 0), (60, 30)), ((0, 30), (60, 0))):
        out.append(poly(clip_convex(band(p, q, -3, 3, 5), box), "#fff"))
    # counterchanged red saltire: red sits below the diagonal in the hoist and above it in the fly
    regions = [[(0, 0), (0, 15), (30, 15)], [(30, 15), (60, 15), (60, 30)],      # for (0,0)-(60,30)
               [(60, 0), (30, 0), (30, 15)], [(30, 15), (0, 30), (30, 30)]]      # for (0,30)-(60,0)
    for i, reg in enumerate(regions):
        p, q = ((0, 0), (60, 30)) if i < 2 else ((0, 30), (60, 0))
        for o1, o2 in ((-2, 0), (0, 2)):
            out.append(poly(clip_convex(band(p, q, o1, o2, 5), reg), red))
    out.append(rect(25, 0, 10, 30, "#fff") + rect(0, 10, 60, 10, "#fff"))
    out.append(rect(27, 0, 6, 30, red) + rect(0, 12, 60, 6, red))
    return "".join(out)


STAR7 = dict(n=7, inner=0.444)


def offset_poly(pts, d):
    """Move every edge of a simple polygon inwards by d and re-intersect neighbours."""
    s = 1 if area2(pts) > 0 else -1
    n = len(pts)
    lines_ = []
    for i in range(n):
        (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
        nx, ny = -(y2 - y1) * s, (x2 - x1) * s
        ln = math.hypot(nx, ny); nx, ny = nx / ln, ny / ln
        lines_.append(((x1 + nx * d, y1 + ny * d), (x2 - x1, y2 - y1)))
    out = []
    for i in range(n):
        (p, r), (q, u) = lines_[i - 1], lines_[i]
        den = r[0] * u[1] - r[1] * u[0]
        t = ((q[0] - p[0]) * u[1] - (q[1] - p[1]) * u[0]) / den
        out.append((p[0] + t * r[0], p[1] + t * r[1]))
    return out
