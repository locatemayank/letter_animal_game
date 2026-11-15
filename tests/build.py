"""Rebuild the game script inside ../index.html from the modular sources.

Usage (from anywhere):  python tests/build.py

index.html keeps its markup and CSS; only the final <script> block is replaced with
engine.js (LetterEngine) + arbiter.js (createTouchArbiter) + the picture packs
garden.js (GARDEN_ITEMS), sports.js (SPORTS_ITEMS), house.js (HOUSE_ITEMS) + game.js (controller). Edit those files, run this, then run the tests (see tests/README.md).
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
INDEX = os.path.join(ROOT, "index.html")


def read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def between(text, start, end):
    i = text.index(start)
    j = text.index(end) + len(end)
    return text[i:j]


engine = between(read("engine.js"), "// ==ENGINE START==", "// ==ENGINE END==")
arbiter = between(read("arbiter.js"), "// ==ARBITER START==", "// ==ARBITER END==")
packs = "\n\n".join([
    between(read("garden.js"), "// ==GARDEN START==", "// ==GARDEN END=="),
    between(read("sports.js"), "// ==SPORTS START==", "// ==SPORTS END=="),
    between(read("house.js"), "// ==HOUSE START==", "// ==HOUSE END=="),
])
game = read("game.js").rstrip() + "\n"

with open(INDEX, encoding="utf-8") as f:
    html = f.read()

open_tag = "  <script>"
close_tag = "  </script>"
start = html.rindex(open_tag)
end = html.index(close_tag, start) + len(close_tag)

script = (
    open_tag + "\n    (() => {\n      \"use strict\";\n\n"
    + engine + "\n\n" + arbiter + "\n\n" + packs + "\n\n" + game
    + "    })();\n" + close_tag
)
html = html[:start] + script + html[end:]

with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print(f"rebuilt {INDEX} ({len(html.splitlines())} lines)")

# Quick syntax check if Node is available.
inline = os.path.join(HERE, ".build_check.js")
with open(inline, "w", encoding="utf-8") as f:
    f.write('(() => {"use strict";\n' + engine + "\n" + arbiter + "\n" + packs + "\n" + game + "\n})();")
try:
    result = subprocess.run(["node", "--check", inline], capture_output=True, text=True)
    print("syntax OK" if result.returncode == 0 else result.stderr)
    if result.returncode != 0:
        sys.exit(1)
except FileNotFoundError:
    print("node not found; skipped syntax check")
finally:
    os.remove(inline)
