# Magic Letter Zoo: review and improvement notes

Reviewed: https://locatemayank.github.io/letter_animal_game/ (index.html + sw.js v16), November 2026.
Audience: children aged 3 to 4 tracing uppercase letters on a phone or tablet.

The game is charming. It has a clear loop (trace, then meet an animal), good audio and confetti feedback, it installs as a PWA, and it cycles A to Z so every letter comes up. Most of the problems are in the parts a parent can't see: the letter check accepts almost anything, and the touch handling ignores real drawing or draws when it shouldn't. Both are fixed in the new `index.html`. Ideas for further work are at the end.

## 1. Bugs found in the current version

**The letter check always says yes.** Inside `recognizeLetter`, the target letter is "encouraged" whenever `drawingHasEnoughSignal` is true. That condition is just "at least 7 points and more than 18 px of ink", so a scribble, a half-traced letter or a completely different letter all count as the target. In a simulation of 780 attempts per case, the old check passed 100% of scribbles, 100% of half-traced letters and 100% of wrong letters. Children learn quickly that any wiggle wins, so the game stops teaching letter shapes.

**A resting hand blocks drawing.** A touch is rejected when `activeTouchPointers.size > 1`. This is the most common way small children hold a tablet: the other hand, a thumb on the bezel or the side of the palm stays on the glass. While that happens, the drawing finger does nothing, and to a 3-year-old the game looks broken.

**Touch tracking can get stuck.** Only the drawing pointer is captured, and `pointerup` is only listened for on the canvas. If a non-drawing finger lifts outside the canvas, its id stays in `activeTouchPointers`, and every later touch is rejected until a reload.

**Pinch and two-finger taps leave stray lines.** When a second finger lands just after the first, the first finger keeps drawing. A pinch therefore draws a line, which then gets "recognised".

**Taps and short strokes are thrown away.** Strokes with fewer than 2 points are dropped, and there is no automatic guess until more than 10 points in total have been drawn. A quick dab or a short bar of an E gives no visible feedback, which feels like the screen isn't working.

**`lostpointercapture` throws away a stroke in progress** instead of keeping it.

**A letter can be skipped.** After a correct letter, `setTimeout(nextTarget, 4200)` is scheduled, but the board isn't locked. Pressing "Guess" again, or adding a stroke that triggers the 2.2 s auto-guess, schedules a second `nextTarget`, so the game skips a letter.

**Resizing misaligns the ink.** On rotation, when the mobile URL bar hides, or in split screen, the canvases are re-laid out but the strokes aren't remapped. The ink then no longer sits on the guide letter.

**Drawing is slow on cheap tablets.** Every pointer move redraws all strokes with `shadowBlur`, which is very slow on budget Android tablets and Fire tablets. Lag makes fast child strokes come out as straight chords.

**Content issues:**

- N (Narwhal) uses 🦄, the same as U (Unicorn); 🐋 or 🦭 would read better.
- Q "Quail" uses the generic bird 🐦, which is also used for B "Bird".
- X "X-ray Fish" 🐟 is the same emoji as F "Fish".
- V "Vulture" 🦅 is the same as E "Eagle".
- Y "Yak" 🐂 is an ox.

These are left unchanged in the new build. Section 4 has ideas.

**The doctype is hidden, so the page renders in quirks mode.** The file in the repo starts with `<![CDATA[` and ends with `]]>`, probably left over from a copy-paste. In HTML, the browser treats `<![CDATA[<!DOCTYPE html>` as a bogus comment, so the doctype is swallowed and the page renders in quirks mode, and a stray `]]>` can show up at the end of the page. The new build removes the wrapper.

**Service worker:** the cache-first strategy for `index.html` means a fixed version only shows up one launch after it is deployed, and it caches error responses too.

## 2. What changed in the new `index.html`

### Letter recognition

The check now has two layers.

**Tracing check (main path).** Each letter has a stroke template drawn top-down in the usual preschool order. Guide dots are placed along it, and a dot counts as covered when ink passes within a finger-sized radius, R = 12% of the letter height (22 to 58 px). A letter passes when:

- enough of the dots are covered overall and on every stroke;
- most of the ink is actually on the letter (precision);
- the ink runs along the guide rather than across it (direction alignment);
- the total ink isn't much longer than the guide (zig-zags fail this).

Stroke order and direction don't matter, and overshoot and wobble are fine.

**Free-draw fallback.** If the child draws the letter freehand somewhere else on the board, a $P point-cloud recogniser (independent of stroke order and direction, and better suited to children's writing than the old fixed-direction template match) checks it against all 26 letters plus common variants (I with serifs, J with a top bar, single-stroke M and so on). It is biased towards the target letter and lenient within lookalike groups, but it rejects scribbles (ink length far longer than the drawing size).

**Leniency increases.** After each "almost", the thresholds relax (three levels). On the third try, any real effort with at least 45% coverage counts as a pass, so no child gets stuck on a letter.

**Responses are always kind.** There is no buzzer:

| Response | What it means | What the game does |
|---|---|---|
| Pass | The letter is right | Animal, stars and confetti |
| Almost | Close, but not finished | The missing dots glow pink and a voice says "Almost! Follow the pink dots." |
| Other letter | A clearly different letter | That letter's animal is shown, then "Now can you trace B?" |
| Scribble or nothing like a letter | — | The board is wiped and the stroke-order animation plays: "Watch me make B. Then you try!" |

Simulated preschool handwriting, 780 attempts per row at 640×520 (`tests/sim.js`):

| Scenario | Old | New |
|---|---|---|
| Good trace passes | 100% | 99.6% |
| Sloppy trace passes | 100% | 97.2% |
| Multi-stroke letter missing a stroke is not passed | 42% | 92.3% |
| Half-traced letter is not passed (gets "almost") | 0% | 99.4% (98.7%) |
| Zig-zag scribble is not passed | 0% | 95.5% |
| Loop scribble is not passed | 0% | 100% |
| Random scribble is not passed | 0% | 99.1% |
| Wrong letter traced over the guide is not passed | 0% | 91.3% |
| Target letter drawn freehand off the guide passes | 100% | 96.5% |
| Wrong letter drawn freehand is named correctly | no (always called the target) | 99.1% of the time when the game names one |

Results are similar at 360×330 (phone) and 900×650 (tablet). Each check takes about 2 ms.

**Known soft spots:**

- **I**: a zig-zag down the single guide line can pass about 1 time in 25.
- **A/R/B/E**: the most common cause of a pass with a missing stroke is that the middle bar is short.
- **Partial tracing**: if a child traces a different letter that lies entirely on the guide (an L on the C guide, for example), it is treated as partial tracing ("almost") rather than "that's an L". This is deliberate.

### Touch handling (single finger is more sensitive, multi-touch is rejected)

All pointer input now goes through a small, separately tested "touch arbiter" (17 scenario tests in `tests/test_arbiter.js`):

- **One finger draws**, even while the other hand, a thumb or a palm rests on the screen. A resting hand no longer blocks drawing.
- **Two fingers landing together** (within 140 ms, before the first finger has moved 18 px) cancel the fresh stroke and lock drawing until the fingers lift. A gentle "☝️ One finger, please!" message appears, at most once every 4 s.
- **A two-finger tap** (fingers within 350 ms of each other) draws nothing.
- **Pinches** (a second finger sliding more than 30 px early in a stroke) cancel the stroke instead of leaving a line.
- **Large contacts** (64 px or more, i.e. a palm or the side of a hand) never draw.
- **Grip touches** that start within 12 px of the canvas edge never draw.
- **A stylus always wins** over touch.
- **No more stuck state:** `pointerup` and `pointercancel` are handled on `window`, and the lock expires as soon as no fingers are down.
- **More sensitive to light, quick touches:**
  - every coalesced pointer sample is used;
  - a tap leaves a visible dot;
  - short strokes count;
  - points are clamped to the board;
  - `lostpointercapture` keeps the stroke instead of dropping it;
  - the coverage radius is finger-sized.
- **Faster drawing:** finished ink is cached on an offscreen canvas, so each move only draws the live stroke. A layered stroke replaces `shadowBlur`, and frames are batched with `requestAnimationFrame`.
- **Browser gestures are blocked:** no long-press menu, text-selection magnifier, double-tap zoom, iOS pinch gesture or pull-to-refresh (`user-select`, `touch-callout`, `overscroll-behavior`, and a non-passive `touchmove` handler on the board).

### Game flow and teaching

- **The guide now teaches:**
  - a soft "road" shows the letter's shape;
  - dots light up gold as the child covers them, with a rising "pling" so progress can be heard;
  - a green numbered start dot and an arrow show where to begin the next stroke.
- **Spoken prompts:** each letter is announced ("Can you trace B?"). "Guess My Letter" is now "✅ Done". A pass is detected automatically about 0.25 s after the stroke that completes the letter. Otherwise the game waits 2.8 s after the last stroke before responding, so slow multi-stroke letters aren't interrupted mid-way.
- **Celebration is a locked phase,** so a reveal can't happen twice and letters can't be skipped.
- **Resizing keeps the ink on the letter:** the ink is remapped when the board size changes.
- **Service worker:** `sw.js` moves to cache v17. The page is fetched network-first (offline still works), so updates appear on the next launch, and error responses are never cached.

## 3. How to deploy

Replace `index.html` and `sw.js` in the repo. No other files changed (manifest and icons are as before). The old version stays in the service-worker cache until the new `sw.js` installs, so after deploying open the page once while online, then relaunch. To test on a device, try tracing slowly, scribbling, resting your other palm on the screen, and pinching.

## 4. Ideas, in rough priority order

These are ordered by how much they help a 3 to 4-year-old learn, and by effort.

1. **Introduce letters in an easier order.** A to Z order puts hard letters (B, G, K, M, Q, R) early. Handwriting programmes for this age usually start with straight-line letters (L, F, E, H, T, I), then diagonals (A, K, M, N, V, W, X, Y, Z), then curves (C, O, Q, G, S, U, J, D, P, R, B). A child succeeds sooner and keeps playing.

2. **Fade the scaffolding.** Each letter could progress through three stages:
   - full road and dots (now);
   - dots only;
   - just a small start dot.
   
   Move up a stage after two clean passes and back down after two "almosts". The leniency system already in the engine slots straight into this.

3. **Phonics, not just letter names.** Say "B says /b/, /b/, bear!" alongside "B is for Bear". Phonemic awareness is the strongest predictor of later reading at this age, and the speech code is already there. Record real voice clips for the 26 sounds; browser text-to-speech mispronounces isolated phonemes.

4. **Mystery animal.** Show a dark silhouette or a peeking animal before tracing starts, then reveal it in full colour on a pass. Anticipation is very motivating for 3 to 4-year-olds and makes the reward feel earned.

5. **Real animal sounds** (short recorded clips) instead of spoken "grrr!". Children this age love them, and the sound acts as a reward in itself.

6. **Sticker-book zoo with saved progress.** Save found animals, stars and the current letter in `localStorage`, so closing the app doesn't wipe the zoo. Make the alphabet chips tappable so a child can revisit an animal they've earned. A full page of animals at Z is a nice long-term goal.

7. **Interface for children who can't read yet:**
   - make the buttons icons only (✅ 🧽 ⏭️), large (at least 64 px), and away from the drawing area;
   - put Sound, Install and New Letter behind a simple parental gate (for example, press and hold for 2 s), because small children tap everything and skip letters by accident;
   - turn on fullscreen (`requestFullscreen`) after the first tap.

8. **Haptics:** `navigator.vibrate(15)` when a stroke starts and a short pattern on a pass (Android only; iOS ignores it).

9. **Lowercase and numbers.** The engine is data-driven: adding `a` to `z` or `0` to `9` means adding entries to `TEMPLATES`. Lowercase matters, because most of what children will read is lowercase.

10. **Fix the content collisions** listed in section 1 (N and U both 🦄; F, X and Q reusing fish and bird emoji; V and E both 🦅). Some options:
    - N: Newt 🦎 or Narwhal 🐋;
    - Q: Quokka (no emoji, use an image);
    - X: X-ray fish (use an image) or "foX" as an end sound;
    - V: Vampire bat 🦇;
    - Y: Yak (use an image).
    
    Custom SVG animals would also make the game look distinctive.

11. **A tiny parent view** (behind the gate): letters mastered, letters needing practice, and which strokes are usually missed. `traceReport.weakestStroke` already reports this.

12. **Accessibility and settings:**
    - a left-handed option (mirror the start-arrow side);
    - a "bigger dots" setting for children with motor delays;
    - respect `prefers-reduced-motion` for the confetti.

## 5. Files

- `index.html` is the new game, as a single file.
- `sw.js` is the service worker, v17.
- `index_original.html` is the version reviewed, for diffing.
- `tests/` holds the standalone engine (`engine.js`), the touch arbiter (`arbiter.js`) and the game controller source (`game.js`), plus:
  - `build.py`, which builds `index.html` from these files;
  - `sim.js`, the handwriting simulation, run with `node sim.js` (environment variables `N`, `W`, `H` and `LEN`);
  - `test_arbiter.js`, the touch tests, run with `node test_arbiter.js`;
  - `smoke_dom.js`, a headless walk-through of the built `index.html` with stubbed browser objects (trace A, a two-finger touch, half a B, a scribble, a palm), run with `node smoke_dom.js`.
