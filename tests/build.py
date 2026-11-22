"""Rebuild the game script inside ../index.html from the modular sources.

Usage (from anywhere):  python tests/build.py

index.html keeps its markup and CSS; only the final <script> block is replaced with
engine.js (LetterEngine) + arbiter.js (createTouchArbiter) + voice.js (Voice: recorded clips) + the picture packs
garden.js (GARDEN_ITEMS), sports.js (SPORTS_ITEMS), house.js (HOUSE_ITEMS),
countries.js (COUNTRY_ITEMS, COUNTRY_HOME_SVG), dinos.js (DINO_ITEMS) + game.js (controller). Edit those files, run this, then run the tests (see tests/README.md).
It also lists voice clips that sit in <folder>/voice/ rather than voice/ (VOICE_FOLDERS), so run it after
uploading clips to another folder.
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
voice = between(read("voice.js"), "// ==VOICE START==", "// ==VOICE END==")


def voice_folders():
    """Clips in <folder>/voice/ instead of voice/ (e.g. uploaded in stages as stage01/voice/...).
    A clip in the top-level voice/ folder always wins."""
    top = set(os.listdir(os.path.join(ROOT, "voice"))) if os.path.isdir(os.path.join(ROOT, "voice")) else set()
    found = {}
    for folder in sorted(os.listdir(ROOT)):
        d = os.path.join(ROOT, folder, "voice")
        if folder.startswith(".") or not os.path.isdir(d):
            continue
        ids = sorted(f[:-4] for f in os.listdir(d) if f.endswith(".mp3") and f not in top)
        ids = [i for i in ids if not any(i in v for v in found.values())]
        if ids:
            found[folder + "/"] = ids
    lines = ",\n".join(f'  "{k}": "{" ".join(v)}"' for k, v in found.items())
    print("voice clips: %d in voice/, %s" % (len(top), ", ".join(f"{len(v)} in {k}voice/" for k, v in found.items()) or "none elsewhere"))
    return "const VOICE_FOLDERS = {\n" + lines + "\n}; // ==VOICE FOLDERS==" if found else "const VOICE_FOLDERS = {}; // ==VOICE FOLDERS=="


_vf_start = voice.index("const VOICE_FOLDERS = {")
_vf_end = voice.index("// ==VOICE FOLDERS==") + len("// ==VOICE FOLDERS==")
voice = voice[:_vf_start] + voice_folders() + voice[_vf_end:]
packs = "\n\n".join([
    between(read("garden.js"), "// ==GARDEN START==", "// ==GARDEN END=="),
    between(read("sports.js"), "// ==SPORTS START==", "// ==SPORTS END=="),
    between(read("house.js"), "// ==HOUSE START==", "// ==HOUSE END=="),
    between(read("countries.js"), "// ==COUNTRIES START==", "// ==COUNTRIES END=="),
    between(read("dinos.js"), "// ==DINOS START==", "// ==DINOS END=="),
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
    + engine + "\n\n" + arbiter + "\n\n" + voice + "\n\n" + packs + "\n\n" + game
    + "    })();\n" + close_tag
)
html = html[:start] + script + html[end:]

with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
    f.write(html)
print(f"rebuilt {INDEX} ({len(html.splitlines())} lines)")

# Quick syntax check if Node is available.
inline = os.path.join(HERE, ".build_check.js")
with open(inline, "w", encoding="utf-8") as f:
    f.write('(() => {"use strict";\n' + engine + "\n" + arbiter + "\n" + voice + "\n" + packs + "\n" + game + "\n})();")
try:
    result = subprocess.run(["node", "--check", inline], capture_output=True, text=True)
    print("syntax OK" if result.returncode == 0 else result.stderr)
    if result.returncode != 0:
        sys.exit(1)
except FileNotFoundError:
    print("node not found; skipped syntax check")
finally:
    os.remove(inline)
