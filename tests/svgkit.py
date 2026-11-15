"""Shared drawing helpers for the picture packs (Sports, Home).

Same look as garden_make.py: chunky dark-brown outline, flat colours, a white
highlight and a small smiling face. Every picture is an SVG with viewBox 0 0 100 100
and no ids (several pictures can be on the page at once).
"""
import json
import os
import math

O = "#3b2a1e"
SW = 3


def st(c=O, w=SW):
    return f'stroke="{c}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"'


def P(d, fill, c=O, w=SW, extra=""):
    return f'<path d="{d}" fill="{fill}" {st(c, w)}{extra}/>'


def C(x, y, r, fill, c=O, w=SW):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" {st(c, w)}/>'


def E(x, y, rx, ry, fill, c=O, w=SW, rot=None):
    t = f' transform="rotate({rot} {x} {y})"' if rot is not None else ""
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="{fill}" {st(c, w)}{t}/>'


def R(x, y, w, h, fill, rx=4, c=O, sw=SW, rot=None):
    t = f' transform="rotate({rot} {x + w / 2:g} {y + h / 2:g})"' if rot is not None else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {st(c, sw)}{t}/>'


def L(d, c=O, w=SW):
    return f'<path d="{d}" fill="none" {st(c, w)}/>'


def TL(d, fill, w=8):
    """Thick outlined line: dark outline underneath, colour on top."""
    return L(d, O, w + 6) + L(d, fill, w)


def F(d, fill, op=None):
    o = f' opacity="{op}"' if op else ""
    return f'<path d="{d}" fill="{fill}"{o}/>'


def dot(x, y, r, fill, op=None):
    o = f' opacity="{op}"' if op else ""
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{o}/>'


def HL(x, y, rx, ry, rot=-30):
    return f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#fff" opacity=".55" transform="rotate({rot} {x} {y})"/>'


def face(x, y, s=1.0, eye=O):
    sp = 6 * s
    r = 2.5 * s if s >= 1 else max(2.0, 2.5 * s)
    return (f'<circle cx="{x - sp:g}" cy="{y}" r="{r:g}" fill="{eye}"/><circle cx="{x + sp:g}" cy="{y}" r="{r:g}" fill="{eye}"/>'
            f'<path d="M{x - 4 * s:g} {y + 5 * s:g}Q{x:g} {y + 9 * s:g} {x + 4 * s:g} {y + 5 * s:g}" fill="none" stroke="{eye}" stroke-width="2.2" stroke-linecap="round"/>')


def sleepy(x, y, s=1.0):
    sp = 6 * s
    return (L(f"M{x - sp - 3 * s:g} {y}Q{x - sp:g} {y + 3 * s:g} {x - sp + 3 * s:g} {y}", O, 2.2)
            + L(f"M{x + sp - 3 * s:g} {y}Q{x + sp:g} {y + 3 * s:g} {x + sp + 3 * s:g} {y}", O, 2.2)
            + L(f"M{x - 3 * s:g} {y + 6 * s:g}Q{x:g} {y + 9 * s:g} {x + 3 * s:g} {y + 6 * s:g}", O, 2.2))


def blush(x, y, sp=10, r=3):
    return dot(x - sp, y, r, "#ff8a80", ".6") + dot(x + sp, y, r, "#ff8a80", ".6")


def T(transform, *parts):
    return f'<g transform="{transform}">' + "".join(parts) + "</g>"


def svg(*parts):
    return '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


def poly_path(pts):
    return "M" + " ".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"


def star_path(x, y, r, inner=0.45, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        a = math.radians(rot + 180 * i / n)
        rr = r if i % 2 == 0 else r * inner
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    return poly_path(pts)


def heart_path(x, y, s):
    return (f"M{x:g} {y + 6 * s:g}C{x - 10 * s:g} {y - 1 * s:g} {x - 6 * s:g} {y - 9 * s:g} {x:g} {y - 4 * s:g}"
            f"C{x + 6 * s:g} {y - 9 * s:g} {x + 10 * s:g} {y - 1 * s:g} {x:g} {y + 6 * s:g}Z")


def annulus_sector(cx, cy, r1, r2, a0, a1):
    """Ring slice between radii r1<r2 from angle a0 to a1 (degrees, clockwise)."""
    def p(r, a):
        a = math.radians(a)
        return cx + r * math.cos(a), cy + r * math.sin(a)
    large = 1 if (a1 - a0) % 360 > 180 else 0
    x0, y0 = p(r2, a0); x1, y1 = p(r2, a1); x2, y2 = p(r1, a1); x3, y3 = p(r1, a0)
    return (f"M{x0:.1f} {y0:.1f}A{r2} {r2} 0 {large} 1 {x1:.1f} {y1:.1f}"
            f"L{x2:.1f} {y2:.1f}A{r1} {r1} 0 {large} 0 {x3:.1f} {y3:.1f}Z")


class Pack:
    def __init__(self):
        self.items = {}

    def add(self, letter, name, line, s):
        self.items.setdefault(letter, []).append({"name": name, "line": line, "svg": s})

    def write(self, path, const, marker, title):
        order = [chr(c) for c in range(65, 91)]
        missing = [k for k in order if k not in self.items]
        assert not missing, f"missing letters: {missing}"
        out = [f"// =={marker} START==", f"// {title}", f"const {const} = {{"]
        for i, k in enumerate(order):
            arr = self.items[k]
            out.append(f"  {k}: [")
            for j, it in enumerate(arr):
                s = it["svg"]
                assert "`" not in s and "${" not in s and " id=" not in s
                assert it["name"][0].upper() == k, (k, it["name"])
                comma = "," if j < len(arr) - 1 else ""
                out.append(f'    {{ name: {json.dumps(it["name"])}, line: {json.dumps(it["line"])}, svg: `{s}` }}{comma}')
            out.append("  ]" + ("," if i < len(order) - 1 else ""))
        out.append("};")
        out.append(f"// =={marker} END==")
        out.append(f'if (typeof module !== "undefined") module.exports = {const};')
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(out) + "\n")
        print("wrote", path, sum(len(v) for v in self.items.values()), "pictures")


def add_extensions(pack, prefix):
    """Append the pictures from every <prefix>_more_*.py next to this file (sorted by file name).

    Each extension module defines add_more(K) and calls K.add(letter, name, line, svg) for each
    extra picture.  Extra pictures come after the original ones for the same letter.
    """
    import glob
    import importlib
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    if here not in sys.path:
        sys.path.insert(0, here)
    for path in sorted(glob.glob(os.path.join(here, f"{prefix}_more_*.py"))):
        mod = importlib.import_module(os.path.splitext(os.path.basename(path))[0])
        before = sum(len(v) for v in pack.items.values())
        mod.add_more(pack)
        print(f"  + {os.path.basename(path)}: {sum(len(v) for v in pack.items.values()) - before} pictures")
