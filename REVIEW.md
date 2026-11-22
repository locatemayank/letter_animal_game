# Magic Letter Zoo: review and improvement notes

Reviewed: https://locatemayank.github.io/letter_animal_game/ (index.html + sw.js v16), November 2026.
Audience: children aged 3 to 4 tracing uppercase letters on a phone or tablet.

The game is charming. It has a clear loop (trace, then meet an animal), good audio and confetti feedback, it installs as a PWA, and it cycles A to Z so every letter comes up. Most of the problems are in the parts a parent can't see: the letter check accepts almost anything, and the touch handling ignores real drawing or draws when it shouldn't. Both are fixed in the new `index.html`. Ideas for further work are at the end.

## Update 8: recorded voice (November 2026)

**A natural voice.** Every line the game speaks now has a recorded clip: 765 short MP3 files in the `voice/` folder (about 6.5 MB in total, each under 3 seconds). That covers "Where shall we play?", the six world welcomes, "Can you trace A?" and "Can you trace little A?", "Almost! Follow the pink dots.", the "Watch me make…" and "Let's follow the dots…" help lines, "That looks like…" and every "A is for Apple" line in all six worlds. The clips were made with the open Kokoro text-to-speech model (voice "af_heart", a warm, clear female voice, slightly slowed for small children). Hard names have their pronunciation set by hand (Xigua, Quetzalcoatlus, Pachycephalosaurus, Kiribati, Jalapeño and about 40 more), and letter names are read as letters ("A is for", not "uh is for"). Every clip was checked by running speech recognition on it.

**Upload a batch at a time.** Any line whose clip is missing is read by the browser voice as before, so the game works with none, some or all of the clips. A clip that is not uploaded yet, a slow network (more than 1.5 s) or an old browser all fall back to the browser voice. Lines that come in two parts ("Welcome to the Zoo!" then "Can you trace A?") play as two clips with a short pause between them.

**Offline.** Clips are kept by the service worker once they have been heard (in their own cache, so a game update does not download them again). Offline, a clip heard before still plays; a new line uses the browser voice. The current letter's clips are downloaded in advance, so they play without a delay.

**Your own voice.** `tools/voice_script.tsv` lists every line and its file name (for example `voice/can-you-trace-a.mp3`). A clip recorded by a parent with the same file name replaces the Kokoro one. `tools/record_kokoro.py` re-records clips, for example after new pictures are added (run `node tests/voice_lines.js` first to update the list).

**Fix.** The message bubble at the bottom stayed on top of the buttons after it faded out and could swallow taps on them. It no longer blocks taps.

The service worker cache is now v24.

## Update 7: Dinosaurs world (November 2026)

**🦖 Dinos.** A sixth world, Dinos, shows a cute cartoon dinosaur for each letter that has one: 45 hand-drawn SVG dinosaurs over 20 letters, picked at random like the other worlds. They include A Ankylosaurus / Allosaurus / Apatosaurus / Argentinosaurus, B Brachiosaurus / Baryonyx / Brontosaurus, D Diplodocus / Dilophosaurus / Deinonychus, P Parasaurolophus / Pachycephalosaurus, S Stegosaurus / Spinosaurus / Styracosaurus, T T. rex / Triceratops / Therizinosaurus / Troodon, U Utahraptor and V Velociraptor. The flying and swimming reptiles that children count as dinosaurs are in too: Pteranodon, Quetzalcoatlus and Rhamphorhynchus fly, and Elasmosaurus, Plesiosaurus, Ichthyosaurus and Mosasaurus swim. Each dinosaur has a short line that is read aloud, such as "Triceratops has three horns and a big frill!".

**Letters without a dinosaur are skipped.** F, J, W, X, Y and Z have no well-known dinosaur, so the Dinos world leaves them out. The letter row shows only the 20 dino letters, ◀ / ▶ jump straight over the gaps (E → G, and ◀ on A wraps to V), and the home button counts "⭐ 0 / 20". If a child draws one of the skipped letters anyway, the game says "That looks like X! Now can you trace V?" without a picture, and gives no stars. The other worlds still use all 26 letters.

**Home screen.** Six world buttons: one row of six on a sideways screen, 3 + 3 on an upright tablet and 2 + 2 + 2 on an upright phone. The Dinos world has its own warm sand-and-jungle colours.

The service worker cache is now v23.

## Update 6: bigger picture, words always visible, phones sideways (November 2026)

**Wider picture.** The drawing area is a little narrower (about 59 % of the width instead of 67 % on a sideways screen) and the picture panel is wider, so the reward picture is bigger.

**Words always visible.** The words under the picture ("I see M!", "M is for Mammoth!" and the little message) are now pinned to the bottom of the picture card. The picture gets whatever space is left above them and shrinks to fit, so on short or older screens it can no longer push the words out of view. The page also uses the real visible screen height (`100dvh`) where the browser supports it, so the browser's address bar no longer hides the bottom of the game.

**Phones use the desktop layout.** On a phone held sideways the game now uses the side-by-side desktop layout (drawing on the left, picture on the right) instead of stacking them, by laying the page out 940 px wide and letting the phone shrink it to fit. On short screens the subtitle is hidden and the letter chips are smaller to save room. When the phone is held upright, a "Turn me sideways!" screen with a turning-phone picture covers the game (the category screen still works upright). A small "Keep it upright" button lets a grown-up dismiss it, for example if the phone's rotation lock is on; the game then uses the stacked layout as before. Tablets are unchanged.

The service worker cache is now v22.

## Update 5: more pictures, ◀ ▶ letter buttons, no Done button (November 2026)

**More pictures per letter.** Every world now has about four pictures per letter, and each time a letter comes up one is picked at random (never the same one twice in a row). The Zoo has 4 emoji animals per letter, for example A Alligator / Ant / Angelfish / Ape and P Penguin / Panda / Pig / Peacock. Garden has 104 fruit and veg (exactly 4 per letter) (new ones include Apricot, Beetroot, Kale, Starfruit and Yuzu). Sports has 103 (Bicycle, Frisbee, Surfboard, Trampoline …) and House has 103 (Bath, Teapot, Piano, Xmas tree …). Countries has 90 flags (Belgium, Ireland, Korea, New Zealand, Spain, Wales …, plus the sailors' signal flags for O, X, Y and Z). A few hard letters have 2–3: X in Sports and House, and F, H, J, O, Q, R, V, W, X, Y in Countries (there are only so many countries and flags for those letters). All new pictures are hand-drawn SVG in the existing style.

**◀ and ▶ beside the letter.** Two round orange arrow buttons sit either side of the big letter tile at the top. ▶ goes to the next letter and ◀ to the previous one (◀ on A wraps to Z). They also skip the celebration if a child wants to move on straight away.

**Done and New Letter are gone.** The game already checked the letter on its own: it passes as soon as the letter is complete, and otherwise it looks at the drawing 2.8 s after the last stroke. So the ✅ Done button was not needed, and 🎲 New Letter is replaced by ▶. The bottom row is now ⬅️ Categories, 🧽 Wipe, Install and Sound.

**Code.** Extra pictures live in their own files (`tests/<pack>_more_*.py`), which the pack scripts pick up automatically. The service worker cache is now v21.

## Update 4: Countries world and a Back button (November 2026)

**Countries.** A fifth world, 🌍 Countries, shows a flag on a little flagpole for each letter: A Australia / Argentina, B Brazil, C Canada / China, D Denmark, E Egypt, F France, G Germany / Greece, H Hungary, I India / Italy, J Japan / Jamaica, K Kenya, L Lebanon, M Mexico, N Nepal / the Netherlands, O Oman, P the Philippines / Peru, Q Qatar, R Rwanda, S South Africa / Sweden, T Thailand / Tanzania, U the United States / the United Kingdom, V Vietnam, W World (a smiling globe), X "X marks the spot" (a treasure map, because no country starts with X), Y Yemen, Z Zambia. Letters with two countries pick one at random. All 36 flags are drawn as SVG from the official proportions and simplified just enough for a small screen (for example Mexico's and Egypt's emblems). Each comes with a friendly hello and one fact, such as "Konnichiwa! A big red sun!" or "Hola! Llamas live here!".

**Back to the categories.** A green "⬅️ Categories" button is now the first button under the drawing area, so a parent can always find the way back. The small 🏠 button by the prompt still works too. Both go back to the "Where shall we play?" screen.

**Home screen.** Five buttons now sit in rows of 3 + 2 on tablets, 2 + 2 + 1 on phones held upright and one row of five when the screen is sideways. The service worker cache is now v20.

## Update 3: Sports and House worlds (November 2026)

**Two new worlds.** The home screen now has four picture buttons: 🦁 Zoo, 🍎 Garden, ⚽ Sports and 🛋️ House. They sit in a 2 × 2 grid when the screen is upright and in one row of four when it is sideways.

**Sports.** Each letter shows a sports thing a young child can name: A Archery, B Basketball, C Cricket, D Dumbbell, E Egg and spoon, F Football, G Golf, H Helmet, I Ice skate, J Jump rope, K Kite, L Life ring, M Medal, N Net, O Oar, P Paddle, Q Quoits, R Racket, S Skateboard, T Trophy, U Uniform, V Volleyball, W Whistle, X Xiangqi, Y Yo-yo, Z Zip line.

**House.** Each letter shows a household thing: A Alarm clock, B Bed, C Cup, D Door, E Envelope, F Fridge, G Glasses, H Hammer, I Iron, J Jug, K Kettle, L Lamp, M Mirror, N Night light, O Oven, P Pillow, Q Quilt, R Rubber duck, S Sofa, T Toothbrush, U Umbrella, V Vase, W Washing machine, X Xylophone, Y Yarn, Z Zipper.

All 52 pictures are hand-drawn SVG in the Garden style (dark outline, flat colours, a little smile). Each one comes with a short spoken line, such as "Roll and zoom!" or "Quack! Splash in the bath!". Each world has its own colours, praise words, found count and saved progress. Lowercase works in every world.

**Code.** The worlds are now a table: adding a world needs one entry in `WORLDS` plus one button on the home screen. The service worker cache is now v19.

## Update 2: lowercase letters and the Garden (November 2026)

**Home screen.** The game now opens on "Where shall we play?" with two big picture buttons, 🦁 Zoo and 🍎 Garden. Each shows how many of the 26 friends have been found. A 🏠 button (where the wiggling star was) goes back to it.

**Garden world.** Tracing a letter grows a fruit or vegetable: A Apple/Avocado, B Banana/Broccoli/Blueberries, C Carrot/Cherries/Corn … X Xigua, Y Yam, Z Zucchini (36 items). All are hand-drawn inline SVG in one friendly style (dark outline, little smile), so they look the same on every tablet with no emoji gaps. The voice says "A is for Apple" and the card adds a line such as "Crunchy and red!". The Garden has its own green tint and its own found count.

**Lowercase.** A big **ABC ⇄ abc** button next to the target letter switches case at any time. It keeps the same letter (A → a), and anything already found counts for both cases. Lowercase letters are traced on school lines (top line, dashed midline, baseline, descender line) at their real relative size, so "o" is short, "h" is tall and "p" hangs below the line. The strokes follow the usual preschool order: a, d, g and q start with a "magic c", and the dot on i and j is a single tap target. The voice says "Can you trace little A?", because text-to-speech reads a lone "a" as "uh". The target tile now draws the letter from the same strokes as the guide, because fonts disagree on shapes like "a" and "g".

**Recognition for lowercase.** It uses the same tracing-coverage check and free-draw fallback as uppercase. It never compares "a" with "A", and it has lowercase lookalike groups (b/d/p/q, n/h/r/m, i/j/l/t, u/v/w/y, …). A new "stray ink" limit stops a different letter from passing just because it happens to cover a short guide. That limit also improved uppercase: wrong letter on the guide is now rejected 94.4% of the time, up from 91.3%. Simulation results for both cases are in `tests/README.md`.

**Saved progress.** World, case, stars, found friends per world and the current letter are kept in `localStorage`, so closing the app no longer empties the zoo. The sound setting is saved too. If storage is blocked (private mode), the game still works and starts fresh.

**Service worker** cache is now v18.

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
- `sw.js` is the service worker, v20.
- `index_original.html` is the version reviewed, for diffing.
- `tests/` holds the standalone engine (`engine.js`), the touch arbiter (`arbiter.js`) and the game controller source (`game.js`), plus:
  - `build.py`, which builds `index.html` from these files;
  - `sim.js`, the handwriting simulation, run with `node sim.js` (environment variables `N`, `W`, `H` and `LEN`);
  - `test_arbiter.js`, the touch tests, run with `node test_arbiter.js`;
  - `smoke_dom.js`, a headless walk-through of the built `index.html` with stubbed browser objects (trace A, a two-finger touch, half a B, a scribble, a palm), run with `node smoke_dom.js`.
