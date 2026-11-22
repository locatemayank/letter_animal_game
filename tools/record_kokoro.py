"""Record the game's voice clips with Kokoro-82M (voice af_heart).

Reads tools/voice_script.tsv (made by `node tests/voice_lines.js`) and writes voice/<id>.mp3.
Clips that already exist are skipped, so you can stop and re-run at any time.

    pip install kokoro-onnx soundfile         (and ffmpeg on the PATH)
    model files: kokoro-v1.0.int8.onnx + voices-v1.0.bin
      from https://github.com/thewh1teagle/kokoro-onnx/releases (model-files-v1.0)
    python tools/record_kokoro.py --model-dir path/to/model [--limit 50] [--only some-id]

You can also record your own voice instead: name each file voice/<id>.mp3 using the ids in
voice_script.tsv. Any clip that is missing is simply read by the browser voice.
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile
import time

import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

VOICE = "af_heart"
SPEED = 0.9

# Words the speech engine gets wrong: say them like this instead (the screen text is unchanged).
SAY_AS = {   # /.../ = phonemes (IPA as used by Kokoro)
    "Xiangqi": "/ʃjˈɑːŋtʃˈiː/",
    "Xare": "/ʃˈɑːɹeɪ/",
    "Xigua": "/ʃˈiːɡwɑː/",
    "Xiao bai cai": "/ʃjˈaʊ bˈaɪ tsˈaɪ/",
    "Xoconostle": "/ʃˌoʊkoʊnˈɑːstleɪ/",
    "Xolo dog": "/ʃˈoʊloʊ dˈɑːɡ/",
    "Xerus": "/zˈɪɹəs/",
    "Xenops": "/zˈiːnɑːps/",
    "Ube": "/ˈuːbeɪ/",
    "Ume plum": "/ˈuːmeɪ plˈʌm/",
    "Urad beans": "/ˈʊɹəd bˈiːnz/",
    "Quenepa": "/kᵻnˈɛpə/",
    "Uakari monkey": "/wɐkˈɑːɹi mˈʌŋki/",
    "Kiribati": "/kˈɪɹɪbæs/",
    "Jicama": "/hˈiːkəmə/",
    "Edamame": "/ˌɛdəmˈɑːmeɪ/",
    "Endive": "/ˈɛndaɪv/",
    "Vicuna": "/vɪkˈuːnjə/",
    "Quetzalcoatlus": "/kˌɛtsəlkoʊˈætləs/",
    "Quetzal": "/kɛtsˈɑːl/",
    "Maiasaura": "/mˌaɪəsˈɔːɹə/",
    "Euoplocephalus": "/jˌuːəplˌoʊsˈɛfələs/",
    "Utahraptor": "/jˈuːtɑːɹˌæptɚ/",
    "Ouranosaurus": "/ʊɹˌænəsˈɔːɹəs/",
    "Deinonychus": "/daɪnˈɑːnɪkəs/",
    "Rhamphorhynchus": "/ɹˌæmfəɹˈɪŋkəs/",
    "Therizinosaurus": "/θˌɛɹɪzˌiːnəsˈɔːɹəs/",
    "Compsognathus": "/kˌɑːmpsɑːɡnˈeɪθəs/",
    "Gallimimus": "/ɡˌælɪmˈaɪməs/",
    "Iguanodon": "/ɪɡwˈɑːnədˌɑːn/",
    "Parasaurolophus": "/pˌæɹəsɔːɹˈɑːləfəs/",
    "Pachycephalosaurus": "/pˌækisˌɛfələsˈɔːɹəs/",
    "Plesiosaurus": "/plˌiːziəsˈɔːɹəs/",
    "Diplodocus": "/dɪplˈɑːdəkəs/",
    "Edmontosaurus": "/ɛdmˌɑːntəsˈɔːɹəs/",
    "Mosasaurus": "/mˌoʊzəsˈɔːɹəs/",
    "Oviraptor": "/ˌoʊvɪɹˈæptɚ/",
    "Pteranodon": "/təɹˈænədˌɑːn/",
    "Nodosaurus": "/nˌoʊdəsˈɔːɹəs/",
    "Spinosaurus": "/spˌaɪnəsˈɔːɹəs/",
    "Styracosaurus": "/stɪɹˌækəsˈɔːɹəs/",
    "Troodon": "/tɹˈoʊədˌɑːn/",
    "Baryonyx": "/bˌæɹiˈɑːnɪks/",
    "Corythosaurus": "/kəɹˌɪθəsˈɔːɹəs/",
    "Dilophosaurus": "/daɪlˌoʊfəsˈɔːɹəs/",
    "Jalapeno": "/hˌɑːləpˈeɪnjoʊ/",
}

LONE_LETTER = re.compile(r"(?<![\w-])([A-Z])(?![\w-])|/([^/]+)/")


def load_rows():
    rows = []
    with open(os.path.join(HERE, "voice_script.tsv"), encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if line:
                rid, text, group = line.split("\t")
                rows.append((rid, text, group))
    return rows


def say_text(text, group):
    for word, how in SAY_AS.items():
        text = re.sub(rf"\b{re.escape(word)}\b", how, text)
    if group != "prompts" and not text.endswith(("!", "?", ".")):
        text += "!"           # "A is for Apple!" sounds brighter than a flat statement
    return text


def to_phonemes(k, text, letter_ph):
    # A lone capital letter is the letter's name ("A is for..." must not become "uh is for...");
    # /.../ is spliced in as phonemes.
    parts, last = [], 0

    def plain(chunk):
        chunk = chunk.strip()
        m = re.match(r"^[?!.,]+", chunk)
        if m and parts:                      # punctuation right after a letter stays with it
            punct = m.group(0)
            # A question ending on an "ee" letter (B C D E G P T V Z) gets a glide ("deer?",
            # "peer?") in Kokoro; "!" keeps the letter clean.
            if punct.startswith("?") and parts[-1].endswith("iː"):
                punct = "!" + punct[1:]
            parts[-1] += punct
            chunk = chunk[m.end():].strip()
        if chunk:
            parts.append(k.tokenizer.phonemize(chunk, "en-us"))

    for m in LONE_LETTER.finditer(text):
        plain(text[last:m.start()])
        parts.append(letter_ph[m.group(1)] if m.group(1) else m.group(2))
        last = m.end()
    plain(text[last:])
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", default=os.path.join(ROOT, ".kokoro"))
    ap.add_argument("--out", default=os.path.join(ROOT, "voice"))
    ap.add_argument("--limit", type=int, default=0, help="stop after this many new clips")
    ap.add_argument("--only", nargs="*", help="ids to (re)record")
    ap.add_argument("--seconds", type=float, default=0, help="stop after this much time")
    ap.add_argument("--shard", default="0/1", help="i/n: only every n-th line (run n copies in parallel)")
    ap.add_argument("--show", action="store_true", help="print phonemes only")
    args = ap.parse_args()

    k = Kokoro(os.path.join(args.model_dir, "kokoro-v1.0.int8.onnx"), os.path.join(args.model_dir, "voices-v1.0.bin"))
    letter_ph = {}
    for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        letter_ph[c] = k.tokenizer.phonemize(f"trace {c}", "en-us").split()[-1].strip("?!.,")

    os.makedirs(args.out, exist_ok=True)
    rows = load_rows()
    if args.only:
        rows = [r for r in rows if r[0] in args.only]
    si, sn = (int(x) for x in args.shard.split("/"))
    rows = [r for i, r in enumerate(rows) if i % sn == si]
    t0, made = time.time(), 0
    for rid, text, group in rows:
        mp3 = os.path.join(args.out, rid + ".mp3")
        if os.path.exists(mp3) and not args.only:
            continue
        ph = to_phonemes(k, say_text(text, group), letter_ph)
        if args.show:
            print(f"{rid}: {ph}")
            continue
        audio, sr = k.create(ph, voice=VOICE, speed=SPEED, lang="en-us", is_phonemes=True)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            wav = tmp.name
        sf.write(wav, audio, sr)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-af", "apad=pad_dur=0.06",
                        "-ac", "1", "-ar", "24000", "-codec:a", "libmp3lame", "-b:a", "40k", mp3 + ".part.mp3"], check=True)
        os.replace(mp3 + ".part.mp3", mp3)
        os.remove(wav)
        made += 1
        print(f"{made:4d} {time.time() - t0:6.1f}s {rid}", flush=True)
        if (args.limit and made >= args.limit) or (args.seconds and time.time() - t0 > args.seconds):
            break
    left = sum(1 for r in load_rows() if not os.path.exists(os.path.join(args.out, r[0] + ".mp3")))
    print(f"done: {made} new, {left} still missing", flush=True)


if __name__ == "__main__":
    sys.exit(main())
