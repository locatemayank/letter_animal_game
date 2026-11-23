"""Browser check: the game must not stop on a lowercase k after the stem and the arm.
Draws | then the arm, checks there is no win on the finger lift, an "Almost" after the pause,
then draws the leg and checks the win. Run from the repo root: python tests/k_browser_test.py
"""
import functools, http.server, os, threading, json, subprocess, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Q, directory=ROOT))
threading.Thread(target=httpd.serve_forever, daemon=True).start()
def strokes(letter, w, h):
    js = f"const E=require({json.dumps(os.path.join(ROOT, 'tests', 'engine.js'))});console.log(JSON.stringify(E.layoutStrokes('{letter}',{w},{h})))"
    return json.loads(subprocess.check_output(["node", "-e", js]))
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.add_init_script("speechSynthesis.speak = () => {};")
    pg.goto(f"http://127.0.0.1:{httpd.server_port}/index.html", wait_until="networkidle")
    pg.click("#worldZoo"); pg.wait_for_timeout(300)
    pg.click("#caseButton"); pg.wait_for_timeout(300)
    for _ in range(10): pg.click("#nextLetterButton"); pg.wait_for_timeout(120)
    pg.wait_for_timeout(4500)   # let the teaching animation finish
    r = pg.eval_on_selector("#drawCanvas", "c => { const r = c.getBoundingClientRect(); return [r.left, r.top, r.width, r.height]; }")
    L, T, W, H = r
    S = strokes("k", W, H)
    msg = lambda: pg.inner_text("#message")
    start = msg()
    print("before:", start)
    def line(a, b, n=25):
        pg.mouse.move(L + a["x"], T + a["y"]); pg.mouse.down()
        for i in range(1, n + 1):
            t = i / n; pg.mouse.move(L + a["x"] + (b["x"] - a["x"]) * t, T + a["y"] + (b["y"] - a["y"]) * t)
        pg.mouse.up()
    line(S[0][0], S[0][1]); pg.wait_for_timeout(300)
    line(S[1][0], S[1][1]); pg.wait_for_timeout(600)
    m1 = msg(); print("0.6 s after stem+arm:", m1)
    pg.wait_for_timeout(3000)
    m2 = msg(); print("3.6 s after stem+arm:", m2)
    line(S[1][1], S[1][2]); pg.wait_for_timeout(800)
    m3 = msg(); print("after the leg:", m3)
    ok = m1 == start and "Almost" in m2 and "Almost" not in m3 and m3 != start
    print("PASS" if ok else "FAIL")
    b.close()
httpd.shutdown()
sys.exit(0 if ok else 1)
