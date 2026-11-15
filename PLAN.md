# Magic Letter Zoo: plan for extending the game

Written November 2026. This builds on the current version (tracing check, touch arbiter, and the `tests/` sources with `build.py`).

These choices are already decided:

- **Worlds:** the child picks a "world" from a picture menu: 🦁 Zoo, 🍎 Garden, 🔢 Numbers.
- **Numbers reward:** tracing a number makes that many objects pop in, and they are counted aloud.
- **Age range:** the game starts at 3–4 years and grows to 3–6 years, adding lowercase, bigger numbers and short words.

**Status (15 Nov 2026):** the following are built:

- the home screen with world buttons and saved progress;
- the Garden world (all custom SVG);
- lowercase a–z on school lines, with an ABC ⇄ abc button;
- three extra picture worlds that were not in the original plan, ⚽ Sports, 🛋️ House and 🌍 Countries (custom SVG; Countries shows flags);
- a labelled "⬅️ Categories" button to go back to the home screen;
- about 4 pictures per letter in every world, picked at random each time;
- ◀ / ▶ letter buttons beside the letter tile (the Done and New Letter buttons are gone).
- Bigger picture panel with the words pinned under it; phones use the side-by-side layout when sideways and show a "Turn me sideways!" tip when upright.

That covers most of phase 1, all of phase 3 and the lowercase part of phase 5. Next up: Numbers 0–9.

## 1. The idea in one paragraph

Turn the game from "a letter game with animals" into a small platform with three worlds that share one tracing engine. Each world is just a content pack: a list of things to trace (letters or numbers), what each one rewards, and how the reward is shown. The engine, touch handling, celebration, sticker book and saved progress are written once and shared. Adding a fourth world later (vehicles, dinosaurs, colours) then means adding a data file, not new code. Inside every world, the child moves through stages as they get better. Stages 1–3 suit ages 3–4, and stages 4–6 add harder content for ages 4–6.

## 2. What the child sees

**Home screen.** Three huge picture buttons (🦁 Zoo, 🍎 Garden, 🔢 Numbers). There is no text the child needs to read. Each button shows a small progress ring (for example, 12 of 26 found). A small ⚙️ in the corner opens the parent area behind a press-and-hold gate.

**Play screen.** This is the current screen, with three changes:

- a 🏠 button to go back home;
- a 📖 button that opens the sticker book;
- the reward card follows the world's style: one big picture for Zoo and Garden, a counting tray for Numbers.

**Sticker book.** There is one book per world, in a grid layout. Items not found yet show as grey silhouettes. Tapping a found item replays its reveal ("B is for Banana!", or counting "1, 2, 3!"). Seeing the gaps is what makes a 3 to 5-year-old want to keep going.

**Parent area (behind the gate).** It contains:

- sound on/off;
- install;
- reset progress;
- the starting stage for each world;
- a left-handed option;
- a "bigger dots" option;
- a simple report: mastered items, items still being practised, and which strokes are usually missed. The engine already reports the weakest stroke.

## 3. The three worlds

### 🦁 Zoo (exists today)

This world keeps the current animals and fixes the duplicate pictures:

- N and U are both 🦄;
- X and F are both 🐟;
- Q and B are both 🐦;
- V and E are both 🦅.

### 🍎 Garden: fruits and vegetables A–Z

Some letters have more than one choice. The game rotates through them, like the animal variants do today.

| Letter | Choices (emoji where one exists) |
|---|---|
| A | Apple 🍎, Avocado 🥑 |
| B | Banana 🍌, Broccoli 🥦, Blueberries 🫐 |
| C | Carrot 🥕, Cherries 🍒, Corn 🌽, Coconut 🥥 |
| D | Dragon fruit (needs art), Dates (needs art) |
| E | Edamame 🫛, Eggplant 🍆 (see note) |
| F | Fig (needs art) |
| G | Grapes 🍇, Garlic 🧄 |
| H | Honeydew 🍈 |
| I | Iceberg lettuce 🥬 |
| J | Jackfruit (needs art), Jalapeño 🌶️ |
| K | Kiwi 🥝 |
| L | Lemon 🍋, Lettuce 🥬 |
| M | Mango 🥭, Mushroom 🍄, Melon 🍈 |
| N | Nuts 🥜, Nectarine (needs art) |
| O | Orange 🍊, Onion 🧅, Olive 🫒 |
| P | Pear 🍐, Pineapple 🍍, Potato 🥔, Peas 🫛 |
| Q | Quince (needs art) |
| R | Radish (needs art), Raspberry (needs art) |
| S | Strawberry 🍓, Sweet potato 🍠 |
| T | Tomato 🍅 |
| U | Ugli fruit (needs art) |
| V | Vegetable soup 🥣 (stretch), or Vanilla pod (needs art) |
| W | Watermelon 🍉 |
| X | Xigua, a Chinese watermelon (needs art; X is hard in every theme) |
| Y | Yam 🍠 |
| Z | Zucchini 🥒 |

**Notes on the list:**

- Many parents read 🍆 and 🍑 as jokes; I'd skip both and use Edamame and Nectarine art instead.
- About 10 items have no emoji at all.
- Several newer emoji are missing on older Android tablets and Fire tablets, which show an empty box instead: 🫐, 🫒, 🫛, and on very old devices 🥥 and 🥭.

The fix for all three is the same: **bundle the pictures as SVG files instead of relying on the device's emoji.** Twemoji artwork (CC-BY 4.0, which needs a credit line in the parent area) covers most items and looks the same on every device. Draw about 10 simple custom SVGs for the gaps. The same switch also fixes the Zoo duplicates, and the service worker caches the files for offline play.

The Garden reveal line works the same way as the Zoo's: "B is for Banana! Bananas are yellow." A short colour or fact line adds vocabulary at no extra cost.

### 🔢 Numbers: trace a number, count the reward

**Stage 1 covers numbers 0–9.** After a pass, the matching number of objects pops into a **ten-frame**: a tray of 2 rows of 5 slots. They appear one by one with a "pop" and a spoken count ("one… two… three!"), and the tracing then finishes on "Three ducks!".

Ten-frames are the standard early-maths tool, because children start to *see* that 7 is "5 and 2 more" without counting. The objects rotate between ducks and fish from the Zoo and apples and carrots from the Garden, which ties the worlds together.

For **zero**, the tray stays empty: "Zero! The basket is empty!" Children find this funny, and it teaches the idea of zero.

**Numbers 10–20 (later stage, ages 5–6)** are traced as two digits side by side. The reward fills one full ten-frame plus a second one.

**Count-and-tap (later stage):** the objects appear all at once, and the child taps each one to count it themselves. Each tap lights up the object and says the next number. Getting this right is a great sign that the child understands counting, not just the order of the number words.

## 4. Engine changes

The tracing engine from the last update is data-driven, so most of this work is adding data.

### Template sets

`TEMPLATES` becomes several named sets:

- `upper` (today's letters);
- `digits` (0–9);
- later, `lower` (a–z).

Each set has its own stroke templates in the usual preschool stroke order, its own `VARIANTS` and its own `LOOKALIKE` groups:

- digits: `[0, 6, 9]`, `[1, 7]`, `[2, Z]`, `[5, S]`, `[3, 8]`;
- lowercase: `[b, d, p, q]`, `[n, h, r]`, `[i, j, l]`, `[u, v, w]`.

### Recognizer scoped to the world

`freeRecognize` only compares against the active set. In the Numbers world, an "O" can't steal a "0". In the Zoo, a "5" can't be called an "S" and send the child to the wrong animal.

### Digit stroke order (top-down, the common preschool style)

| Digit | Strokes |
|---|---|
| 0 | One stroke, anticlockwise from the top |
| 1 | One stroke, down (the version with a small flag is accepted as a variant) |
| 2 | One stroke: curve round, slide down, then across |
| 3 | One stroke: two bumps |
| 4 | Two strokes: down and across, then a long line down |
| 5 | Two strokes: down and round, then the top flag |
| 6 | One stroke: curve down into a loop |
| 7 | One stroke: across, then down the slant |
| 8 | One stroke: an S, then back up |
| 9 | Two strokes: a circle, then a line down (the one-stroke version is accepted) |

### Layout modes

`layoutTransform` currently stretches each glyph to fill the board. That is fine for capital letters and digits, but wrong for lowercase, where the size of a letter is part of its identity: "h" is tall, "n" is short, and "p" goes below the line. Add a **ruled layout**: a fixed box with a top line, a dashed midline and a baseline, drawn on the guide canvas like school handwriting paper. Lowercase templates are defined against those lines. A **multi-box layout** places 2–3 glyph boxes side by side, for 10–20 and short words.

### Calibration

Extend `sim.js` to run every template set and both layouts. The same targets as for capital letters apply: at least 97% of good traces pass, at least 90% of scribbles and wrong glyphs are rejected, and "almost" is shown for at least 95% of half-traced glyphs. Digits will need the most tuning, because 1 and 7 are short, simple shapes, like I was for letters.

## 5. Shared features all worlds get

**Saved progress.** Today nothing is saved; closing the app wipes the zoo. Store this in `localStorage` with a version number:

- items found in each world;
- stars;
- the current stage;
- for each glyph: number of passes, number of "almosts", and the weakest stroke.

On iPhone and iPad, Safari deletes saved data for websites that haven't been opened for 7 days, but not for apps added to the home screen. So the parent area should encourage installing, and the "Install" prompt should explain this.

**Stages (progression)** for each world:

| Stage | What changes | Age |
|---|---|---|
| 1 | Full guide road and dots, start dot and arrow (today's game) | 3–4 |
| 2 | Dots only, no road | 3–4 |
| 3 | Start dot only, with a faint outline | 4 |
| 4 | Lowercase letters / numbers 10–20 | 4–5 |
| 5 | Free writing on ruled lines, no guide | 5–6 |
| 6 | Short words: C-A-T, D-O-G, one picture per word (Zoo/Garden); count-and-tap (Numbers) | 5–6 |

A glyph moves up a stage after 2 clean passes in a row and moves back after 2 "almosts" in a row. This uses the leniency system the engine already has.

**Easier letter order.** Within a stage, teach straight-line letters first (L F E H T I), then diagonals (A K M N V W X Y Z), then curves (C O Q G S U J D P R B). For digits, teach 1 4 7, then 0 6 9, then 2 3 5 8. Children succeed sooner and stay motivated. Free-choice play (tapping a sticker to practise that letter) stays open at any time.

## 6. Code structure

The current setup works well: the source files are kept separate and `build.py` assembles one `index.html`. Keep it, because a single file is simple to host and to cache offline. Reorganise the files like this:

```
index.html              ← built, deployed
sw.js                   ← cache list generated by build.py (includes assets/)
assets/
  zoo/*.svg  garden/*.svg  ui/*.svg
src/
  engine.js             ← template sets, layouts, tracing check, recognizer
  arbiter.js            ← touch handling (unchanged)
  content/zoo.js        ← { id, title, icon, set:'upper', reward:'single', items:{A:[…]} }
  content/garden.js
  content/numbers.js    ← { set:'digits', reward:'count', objects:['duck','apple',…] }
  progress.js           ← localStorage save/load, stages, mastery
  screens/home.js  screens/play.js  screens/book.js  screens/parent.js
  game.js               ← glue: routing between screens, celebration, sounds
tests/
  sim.js  test_arbiter.js  smoke_dom.js  test_progress.js
```

A world is just its content file. To add 🚗 Vehicles later, you write `content/vehicles.js` and add a few SVGs, with no code changes.

## 7. Delivery in phases

Each phase ends with a working, deployable game and its own commit and patch, like the last update. Sizes are rough:

- **S** = one working session;
- **M** = two or three sessions;
- **L** = a few days.

| Phase | Contents | Size | Done when |
|---|---|---|---|
| 1. Foundation | Move to `src/`; content-pack format; Zoo converted to a pack; home screen with world buttons; saved progress; parental gate; SVG assets for Zoo (fixes duplicates) | M | Zoo plays as today, progress survives a reload, all existing tests pass |
| 2. Numbers 0–9 | `digits` template set + recognizer scoping; ten-frame counting reward, including zero; number lookalikes; sim calibration | M | Sim targets met for digits; smoke test traces 0–9 |
| 3. Garden | `garden.js` content, Twemoji + about 10 custom SVGs, reveal lines | S–M | All 26 letters show art on an old Android tablet, with no empty boxes |
| 4. Sticker books + stages 1–3 | Book screen for each world, replay on tap; scaffold fading; easier order; mastery rules | M | A child's progress moves stages automatically; book shows silhouettes |
| 5. Growing to 4–6 | Ruled layout + `lower` set (a–z, with b/d/p/q care); multi-box layout; numbers 10–20 | L | Lowercase sim targets met; 10–20 traced as two digits |
| 6. Words + count-and-tap | Short CVC words (about 20, matching existing pictures: cat, dog, pig, fox, hen, bee, yak…); tap-to-count game | M | Word traced box by box shows its picture; tap counting works with one finger only |
| 7. Parent area | Report per glyph, weakest strokes, settings (left-handed, bigger dots, reduced motion), credits | S | — |

My suggested order is the one in the table. Numbers comes before Garden because it adds the bigger new engine feature (a new template set plus the counting reward). The Garden is mostly content, and it slots in easily once the content-pack format exists.

## 8. Testing on every phase

- **Automated:**
  - `sim.js` for every template set and layout;
  - `test_arbiter.js` (touch rules);
  - `smoke_dom.js` extended to switch worlds, trace, check the reward and reload to confirm progress was saved;
  - a new `test_progress.js` for the stage up/down rules and saved-data migration.
- **On real devices:** at least one cheap Android tablet, one iPad and one phone, both installed to the home screen and in a browser tab. Check:
  - tracing at the edges of the board;
  - a resting palm;
  - two-finger taps;
  - rotation mid-letter;
  - airplane mode, to confirm offline play;
  - that every picture renders.
- **With a child:** watch one real session per phase, without helping. Hesitations and mis-taps show what needs fixing better than any test.

## 9. Risks and how to handle them

**Too many choices for a 3-year-old.** Keep the home screen to three big buttons and remember the last world played. New worlds can go on a second page that a parent unlocks.

**Lookalikes once sets mix.** Never compare across sets. Each world has its own template set, so O and 0, S and 5, l and 1 can't be confused.

**Lowercase is much harder to recognise:**

- b/d/p/q differ only by direction or side;
- sizes relative to the ruled lines matter.

Lowercase is a phase-5 feature for older children, it gets its own calibration, and the tracing guide still does most of the work.

**Pictures look different on each device.** Bundled SVGs solve this. They add about 300–600 KB, which is cached once.

**Saved progress lost on iOS.** Encourage installing to the home screen, and offer an "export progress" code in the parent area if needed.

**One big file gets hard to change.** The `src/` split with `build.py` keeps editing modular while still deploying one file.

## 10. Decisions still open

- **Garden art style:** Twemoji-style, which matches the current look, or a custom illustrated style.
- **Number reward objects:** rotate between worlds, as proposed, or use one fixed object per number ("3 is three ducks", always).
- **Short words:** whether they also belong to the Garden (P-E-A, F-I-G, Y-A-M), which would make a nice bridge between worlds.
