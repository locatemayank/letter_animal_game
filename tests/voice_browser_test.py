"""Browser check of the recorded voice (needs: pip install playwright; playwright install chromium-headless-shell).

Serves the game folder, opens it in headless Chromium and checks that:
  1. with all clips, lines play as recorded clips (WebAudio) and the browser voice is not used;
  2. chained lines ("Welcome to the Zoo!" + "Can you trace A?") play as two clips in a row;
  3. a missing clip (404) falls back to the browser voice with the full sentence;
  4. without WebAudio, clips play through an <audio> element;
  5. the service worker keeps clips it has played, but never a 404;
  6. offline, a clip heard before still plays and a new line uses the browser voice.
Run from the repo root: python tests/voice_browser_test.py
"""
import functools
import http.server
import os
import sys
import threading

from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def handle(self):
        try:
            super().handle()
        except ConnectionError:
            pass   # the browser closed a clip download it no longer needs


def serve():
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=ROOT))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


SPY = """
window.__played = []; window.__tts = []; window.__el = [];
const st = AudioBufferSourceNode.prototype.start;
AudioBufferSourceNode.prototype.start = function (...a) { window.__played.push(+this.buffer.duration.toFixed(2)); return st.apply(this, a); };
speechSynthesis.speak = u => { if (u.text.trim()) window.__tts.push(u.text); };  // " " = iOS unlock
HTMLMediaElement.prototype.play = function () { window.__el.push(this.src.split('/').pop()); return Promise.resolve(); };
"""

fails = []


def check(name, ok, info=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  [{info}]" if info else ""), flush=True)
    if not ok:
        fails.append(name)


def main():
    httpd = serve()
    base = f"http://127.0.0.1:{httpd.server_port}/index.html"
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--autoplay-policy=no-user-gesture-required"])

        # 1-3: no service worker, so page.route sees every request.
        ctx = browser.new_context(service_workers="block", viewport={"width": 1280, "height": 720})
        missing = {"can-you-trace-b.mp3"}
        ctx.route("**/voice/*.mp3", lambda route: route.fulfill(status=404, body="<html>404</html>", content_type="text/html")
                  if route.request.url.split("/")[-1] in missing else route.continue_())
        page = ctx.new_page()
        page.add_init_script(SPY)
        page.goto(base)
        page.click("#worldZoo")
        page.wait_for_timeout(1500)
        played, tts = page.evaluate("[__played, __tts]")
        check("world welcome = 2 chained clips, no browser voice", len(played) == 2 and not tts, f"{played} {tts}")

        page.evaluate("__played.length = 0; __tts.length = 0")
        page.click("#nextLetterButton")          # A -> B, "Can you trace B?" has no clip here
        page.wait_for_timeout(1500)
        played, tts = page.evaluate("[__played, __tts]")
        check("missing clip -> browser voice says the sentence", tts == ["Can you trace B?"] and not played, f"{played} {tts}")

        page.evaluate("__played.length = 0; __tts.length = 0")
        page.click("#nextLetterButton")          # B -> C, has a clip
        page.wait_for_timeout(1500)
        played, tts = page.evaluate("[__played, __tts]")
        check("next letter plays its clip", len(played) == 1 and not tts, f"{played} {tts}")

        page.evaluate("__played.length = 0; __tts.length = 0")
        page.click("#caseButton")                # "Small letters!" + "Can you trace little C?"
        page.wait_for_timeout(1500)
        played, tts = page.evaluate("[__played, __tts]")
        check("abc button = 2 chained clips", len(played) == 2 and not tts, f"{played} {tts}")

        page.evaluate("__played.length = 0; __tts.length = 0")
        page.click("#soundButton")               # sound off
        page.click("#nextLetterButton")
        page.wait_for_timeout(1200)
        played, tts = page.evaluate("[__played, __tts]")
        check("sound off = silent", not played and not tts, f"{played} {tts}")
        ctx.close()

        # 4: no WebAudio -> <audio> element.
        ctx = browser.new_context(service_workers="block")
        page = ctx.new_page()
        page.add_init_script("delete window.AudioContext; delete window.webkitAudioContext;" + SPY.replace(
            "const st = AudioBufferSourceNode.prototype.start;", "const st = () => {};").replace(
            "AudioBufferSourceNode.prototype.start = function (...a) { window.__played.push(+this.buffer.duration.toFixed(2)); return st.apply(this, a); };", ""))
        page.goto(base)
        page.click("#worldGarden")
        page.wait_for_timeout(1500)
        el, tts = page.evaluate("[__el, __tts]")
        check("no WebAudio -> <audio> plays the first clip", el[:1] == ["welcome-to-the-garden.mp3"] and not tts, f"{el} {tts}")
        ctx.close()

        # 5: service worker caches played clips, not 404s.
        ctx = browser.new_context()
        page = ctx.new_page()
        page.goto(base)
        page.evaluate("navigator.serviceWorker.ready.then(() => true)")
        page.reload()                            # now the page is controlled by sw.js
        page.wait_for_function("navigator.serviceWorker.controller !== null", timeout=10000)
        page.wait_for_timeout(500)
        page.click("#worldDinos")
        page.wait_for_timeout(2000)
        page.evaluate("fetch('voice/not-a-real-clip.mp3')")
        page.wait_for_timeout(800)
        keys = page.evaluate("""(async () => { const c = await caches.open('magic-letter-zoo-voice-v1');
            return (await c.keys()).map(r => r.url.split('/').pop()); })()""")
        check("sw keeps played clips", "welcome-to-dino-land.mp3" in keys, f"{len(keys)} cached")
        check("sw never caches a 404", "not-a-real-clip.mp3" not in keys)

        # 6: offline - a clip heard before still plays, a new one uses the browser voice.
        page.add_init_script(SPY)
        page.reload()
        page.click("#worldDinos")                 # cached above
        page.wait_for_timeout(1500)
        ctx.set_offline(True)
        page.evaluate("__played.length = 0; __tts.length = 0")
        page.click("#nextLetterButton")           # A -> B: not heard yet
        page.wait_for_timeout(1800)
        played, tts = page.evaluate("[__played, __tts]")
        check("offline, clip not heard yet -> browser voice", tts == ["Can you trace B?"] and not played, f"{played} {tts}")
        page.evaluate("__played.length = 0; __tts.length = 0")
        page.click("#prevLetterButton")           # back to A: cached
        page.wait_for_timeout(1500)
        played, tts = page.evaluate("[__played, __tts]")
        check("offline, clip heard before -> clip", len(played) == 1 and not tts, f"{played} {tts}")
        ctx.close()
        browser.close()
    httpd.shutdown()
    print("ALL PASS" if not fails else f"{len(fails)} FAILED")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
