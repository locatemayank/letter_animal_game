"""Helpers for the Dinosaurs pack (dinos_make.py and dinos_more_*.py).

Style: side view, head on the RIGHT, chunky dark outline (O from svgkit), flat colours,
one big friendly eye, a small smile, pink cheek, soft ground shadow. viewBox 0 0 100 100.

The trick for clean silhouettes: blob(fill, d1, d2, ...) draws every shape's thick outline
first and then all the fills on top, so overlapping parts merge into one outlined body
without seams.  Use ell()/circ() to turn ellipses into path data for blob().
"""
import math
from svgkit import *

GREEN = "#7cc95a"; GREEND = "#4f9a3a"; BELLY = "#f6eab0"; ORANGE = "#ffa94d"; ORANGED = "#e07b1f"
PURPLE = "#b39ddb"; PURPLED = "#7e57c2"; BLUE = "#64b5f6"; BLUED = "#1e88e5"; TEAL = "#4db6ac"; TEALD = "#00897b"
RED = "#ef6c5a"; REDD = "#c62828"; YELLOW = "#ffd54f"; YELLOWD = "#f9a825"; BROWN = "#c49a6c"; BROWND = "#8d6e63"
PINK = "#f8a5c2"; GREY = "#a7b6c2"; GREYD = "#78909c"; LIME = "#c5e1a5"; SEA = "#4fc3f7"; SAND = "#ffe0a3"


def ell(cx, cy, rx, ry, rot=0):
    """Ellipse as path data (for blob)."""
    t = math.radians(rot)
    ax, ay = cx - rx * math.cos(t), cy - rx * math.sin(t)
    bx, by = cx + rx * math.cos(t), cy + rx * math.sin(t)
    return (f"M{ax:.1f} {ay:.1f}A{rx} {ry} {rot} 1 1 {bx:.1f} {by:.1f}"
            f"A{rx} {ry} {rot} 1 1 {ax:.1f} {ay:.1f}Z")


def circ(cx, cy, r):
    return ell(cx, cy, r, r)


def blob(fill, *ds, w=SW):
    """One merged outlined shape made of several path-data pieces."""
    under = "".join(f'<path d="{d}" fill="{O}" stroke="{O}" stroke-width="{2 * w}" stroke-linejoin="round" stroke-linecap="round"/>' for d in ds)
    over = "".join(f'<path d="{d}" fill="{fill}"/>' for d in ds)
    return under + over


def ground(cx=50, cy=92, rx=36, ry=4.5):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000" opacity=".1"/>'


def eye(x, y, r=4.4):
    """Side-view eye looking right: white, big pupil, shine."""
    return (C(x, y, r, "#fff", O, 2) + dot(f"{x + r * 0.22:.1f}", f"{y + r * 0.08:.1f}", f"{r * 0.58:.1f}", O)
            + dot(f"{x + r * 0.02:.1f}", f"{y - r * 0.28:.1f}", f"{r * 0.24:.1f}", "#fff"))


def smile(x, y, w=8, c=O):
    """Small smile, ends at (x - w/2, y) and (x + w/2, y)."""
    return L(f"M{x - w / 2:g} {y:g}Q{x:g} {y + w * 0.45:g} {x + w / 2:g} {y - 0.6:g}", c, 2.2)


def cheek(x, y, r=2.8):
    return dot(x, y, r, "#ff8a80", ".55")


def nostril(x, y):
    return dot(x, y, 1.1, O)


def spots(color, pts, op=None):
    """Flat spots, pts = [(x, y, r), ...]."""
    return "".join(dot(x, y, r, color, op) for x, y, r in pts)


def belly(d, color=BELLY):
    """Lighter belly patch (fill only, no outline) - draw it after the body blob."""
    return F(d, color)
