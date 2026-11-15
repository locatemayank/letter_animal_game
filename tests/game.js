      const animals = {
        A: { name: "Alligator", emoji: "🐊", sound: "snap snap!" },
        B: { name: "Bear", emoji: "🐻", sound: "grrr!" },
        C: { name: "Cat", emoji: "🐱", sound: "meow!" },
        D: { name: "Dog", emoji: "🐶", sound: "woof!" },
        E: { name: "Elephant", emoji: "🐘", sound: "toot toot!" },
        F: { name: "Fox", emoji: "🦊", sound: "ring-ding!" },
        G: { name: "Giraffe", emoji: "🦒", sound: "munch munch!" },
        H: { name: "Hippo", emoji: "🦛", sound: "splash!" },
        I: { name: "Iguana", emoji: "🦎", sound: "scurry!" },
        J: { name: "Jaguar", emoji: "🐆", sound: "roar!" },
        K: { name: "Koala", emoji: "🐨", sound: "sleepy munch!" },
        L: { name: "Lion", emoji: "🦁", sound: "roar!" },
        M: { name: "Monkey", emoji: "🐵", sound: "ooh ooh!" },
        N: { name: "Narwhal", emoji: "🦄", sound: "splash sparkle!" },
        O: { name: "Owl", emoji: "🦉", sound: "hoot hoot!" },
        P: { name: "Penguin", emoji: "🐧", sound: "waddle waddle!" },
        Q: { name: "Quail", emoji: "🐦", sound: "tweet!" },
        R: { name: "Rabbit", emoji: "🐰", sound: "hop hop!" },
        S: { name: "Snake", emoji: "🐍", sound: "ssss!" },
        T: { name: "Tiger", emoji: "🐯", sound: "rawr!" },
        U: { name: "Unicorn", emoji: "🦄", sound: "sparkle!" },
        V: { name: "Vulture", emoji: "🦅", sound: "whoosh!" },
        W: { name: "Whale", emoji: "🐳", sound: "whoooo!" },
        X: { name: "X-ray Fish", emoji: "🐟", sound: "bubble bubble!" },
        Y: { name: "Yak", emoji: "🐂", sound: "moo!" },
        Z: { name: "Zebra", emoji: "🦓", sound: "neigh!" }
      };

      // Four zoo friends per letter; one is picked at random each time a letter comes up.
      const animalVariants = {
        A: [{ name: "Alligator", emoji: "🐊", sound: "snap snap!" }, { name: "Ant", emoji: "🐜", sound: "tiny steps!" }, { name: "Angelfish", emoji: "🐠", sound: "blub blub!" }, { name: "Ape", emoji: "🦍", sound: "ooh ooh ah ah!" }],
        B: [{ name: "Bear", emoji: "🐻", sound: "grrr!" }, { name: "Bee", emoji: "🐝", sound: "buzz buzz!" }, { name: "Butterfly", emoji: "🦋", sound: "flutter flutter!" }, { name: "Beaver", emoji: "🦫", sound: "chomp chomp!" }],
        C: [{ name: "Cat", emoji: "🐱", sound: "meow!" }, { name: "Cow", emoji: "🐮", sound: "moo!" }, { name: "Chick", emoji: "🐤", sound: "cheep cheep!" }, { name: "Crab", emoji: "🦀", sound: "snip snip!" }],
        D: [{ name: "Dog", emoji: "🐶", sound: "woof!" }, { name: "Duck", emoji: "🦆", sound: "quack!" }, { name: "Dolphin", emoji: "🐬", sound: "click click!" }, { name: "Dinosaur", emoji: "🦕", sound: "stomp stomp!" }],
        E: [{ name: "Elephant", emoji: "🐘", sound: "toot toot!" }, { name: "Eagle", emoji: "🦅", sound: "screech!" }, { name: "Ewe", emoji: "🐑", sound: "baa baa!" }, { name: "Earthworm", emoji: "🪱", sound: "wiggle wiggle!" }],
        F: [{ name: "Fox", emoji: "🦊", sound: "ring-ding!" }, { name: "Frog", emoji: "🐸", sound: "ribbit!" }, { name: "Fish", emoji: "🐟", sound: "bubble bubble!" }, { name: "Flamingo", emoji: "🦩", sound: "honk honk!" }],
        G: [{ name: "Giraffe", emoji: "🦒", sound: "munch munch!" }, { name: "Goat", emoji: "🐐", sound: "maa maa!" }, { name: "Grasshopper", emoji: "🦗", sound: "chirp chirp!" }, { name: "Guinea pig", emoji: "🐹", sound: "squeak squeak!" }],
        H: [{ name: "Hippo", emoji: "🦛", sound: "splash!" }, { name: "Horse", emoji: "🐴", sound: "neigh!" }, { name: "Hedgehog", emoji: "🦔", sound: "sniff sniff!" }, { name: "Hen", emoji: "🐔", sound: "cluck cluck!" }],
        I: [{ name: "Iguana", emoji: "🦎", sound: "scurry!" }, { name: "Inchworm", emoji: "🐛", sound: "inch, inch!" }, { name: "Impala", emoji: "🦌", sound: "boing boing!" }, { name: "Ice bear", emoji: "🐻‍❄️", sound: "brrr!" }],
        J: [{ name: "Jaguar", emoji: "🐆", sound: "roar!" }, { name: "Jackrabbit", emoji: "🐇", sound: "hop hop!" }, { name: "June bug", emoji: "🪲", sound: "buzz!" }, { name: "Jersey cow", emoji: "🐄", sound: "moo moo!" }],
        K: [{ name: "Koala", emoji: "🐨", sound: "sleepy munch!" }, { name: "Kangaroo", emoji: "🦘", sound: "boing boing!" }, { name: "Kitten", emoji: "🐈", sound: "mew mew!" }, { name: "Komodo dragon", emoji: "🐉", sound: "hiss!" }],
        L: [{ name: "Lion", emoji: "🦁", sound: "roar!" }, { name: "Ladybug", emoji: "🐞", sound: "fly away!" }, { name: "Lobster", emoji: "🦞", sound: "click click!" }, { name: "Llama", emoji: "🦙", sound: "hum hum!" }],
        M: [{ name: "Monkey", emoji: "🐵", sound: "ooh ooh!" }, { name: "Mouse", emoji: "🐭", sound: "squeak!" }, { name: "Mammoth", emoji: "🦣", sound: "trumpet!" }, { name: "Macaw", emoji: "🦜", sound: "squawk!" }],
        N: [{ name: "Narwhal", emoji: "🐋", sound: "splash sparkle!" }, { name: "Nurse shark", emoji: "🦈", sound: "swish swish!" }, { name: "Nautilus", emoji: "🐚", sound: "bloop!" }, { name: "Newt", emoji: "🦎", sound: "splish!" }],
        O: [{ name: "Owl", emoji: "🦉", sound: "hoot hoot!" }, { name: "Octopus", emoji: "🐙", sound: "wiggle wiggle!" }, { name: "Otter", emoji: "🦦", sound: "splish splash!" }, { name: "Orangutan", emoji: "🦧", sound: "ooh ooh!" }],
        P: [{ name: "Penguin", emoji: "🐧", sound: "waddle waddle!" }, { name: "Panda", emoji: "🐼", sound: "munch munch!" }, { name: "Pig", emoji: "🐷", sound: "oink oink!" }, { name: "Peacock", emoji: "🦚", sound: "ta-da!" }],
        Q: [{ name: "Quail", emoji: "🐦", sound: "tweet!" }, { name: "Queen bee", emoji: "🐝", sound: "buzz buzz!" }, { name: "Quarter horse", emoji: "🐎", sound: "gallop gallop!" }, { name: "Quetzal", emoji: "🦜", sound: "whistle!" }],
        R: [{ name: "Rabbit", emoji: "🐰", sound: "hop hop!" }, { name: "Rooster", emoji: "🐓", sound: "cock-a-doodle-doo!" }, { name: "Raccoon", emoji: "🦝", sound: "sniff sniff!" }, { name: "Rhino", emoji: "🦏", sound: "stomp stomp!" }],
        S: [{ name: "Snake", emoji: "🐍", sound: "ssss!" }, { name: "Squirrel", emoji: "🐿️", sound: "nibble nibble!" }, { name: "Snail", emoji: "🐌", sound: "slowly, slowly!" }, { name: "Swan", emoji: "🦢", sound: "honk!" }],
        T: [{ name: "Tiger", emoji: "🐯", sound: "rawr!" }, { name: "Turtle", emoji: "🐢", sound: "slow steps!" }, { name: "Turkey", emoji: "🦃", sound: "gobble gobble!" }, { name: "T-rex", emoji: "🦖", sound: "roar!" }],
        U: [{ name: "Unicorn", emoji: "🦄", sound: "sparkle!" }, { name: "Uakari monkey", emoji: "🐒", sound: "ooh ooh!" }, { name: "Upside-down sloth", emoji: "🦥", sound: "sleepy yawn!" }, { name: "Urchin", emoji: "🦔", sound: "snuffle snuffle!" }],
        V: [{ name: "Vulture", emoji: "🦅", sound: "whoosh!" }, { name: "Vampire bat", emoji: "🦇", sound: "flap flap!" }, { name: "Vicuna", emoji: "🦙", sound: "hum hum!" }, { name: "Viper", emoji: "🐍", sound: "hiss hiss!" }],
        W: [{ name: "Whale", emoji: "🐳", sound: "whoooo!" }, { name: "Wolf", emoji: "🐺", sound: "awooo!" }, { name: "Walrus", emoji: "🦭", sound: "arf arf!" }, { name: "Wild boar", emoji: "🐗", sound: "oink oink!" }],
        X: [{ name: "X-ray Fish", emoji: "🐟", sound: "bubble bubble!" }, { name: "Xerus", emoji: "🐿️", sound: "chitter chitter!" }, { name: "Xolo dog", emoji: "🐕", sound: "woof woof!" }, { name: "Xenops", emoji: "🐦", sound: "tweet tweet!" }],
        Y: [{ name: "Yak", emoji: "🐂", sound: "moo!" }, { name: "Yellow chick", emoji: "🐥", sound: "peep peep!" }, { name: "Yeti crab", emoji: "🦀", sound: "snip snip!" }, { name: "Yellowfin tuna", emoji: "🐟", sound: "zoom zoom!" }],
        Z: [{ name: "Zebra", emoji: "🦓", sound: "neigh!" }, { name: "Zebu", emoji: "🐃", sound: "moo moo!" }, { name: "Zebrafish", emoji: "🐠", sound: "swish swish!" }, { name: "Zebra finch", emoji: "🐦", sound: "cheep cheep!" }]
      };

      // ---------- worlds (content packs) ----------
      // Each world maps an uppercase letter to one or more items. Items have a name plus
      // either an emoji or an inline SVG picture; `cheer` is what the stage says on success.
      const WORLDS = {
        zoo: {
          icon: "🦁", title: "Magic Letter Zoo", subtitle: "✏️ Trace a letter. Meet an animal friend! 🐾",
          foundLabel: "Zoo friends", welcome: "Welcome to the Zoo", hello: "🦁",
          intro: "Follow the dots to make the letter. An animal friend will come!",
          praise: ["Amazing!", "Wow!", "Super writing!", "Zoo-rific!", "You did it!", "Fantastic!"],
          items: L => animalVariants[L] || [animals[L] || animals.A],
          cheer: item => `${item.name} says "${item.sound}"`
        },
        garden: {
          icon: "🍎", title: "Magic Letter Garden", subtitle: "✏️ Trace a letter. Pick something yummy! 🥕",
          foundLabel: "Garden friends", welcome: "Welcome to the Garden", hello: null,
          intro: "Follow the dots to make the letter. Something yummy will grow!",
          praise: ["Yummy!", "Wow!", "Berry good!", "Super writing!", "You did it!", "Fantastic!"],
          items: L => (typeof GARDEN_ITEMS !== "undefined" && GARDEN_ITEMS[L]) || [{ name: "Apple", emoji: "🍎", line: "Crunchy and red!" }],
          cheer: item => item.line || "Yum yum!", homePic: "A"
        },
        sports: {
          icon: "⚽", title: "Magic Letter Sports", subtitle: "✏️ Trace a letter. Get ready to play! 🏆",
          foundLabel: "Sports things", welcome: "Welcome to Sports Day", hello: null,
          intro: "Follow the dots to make the letter. Let's play!",
          praise: ["Goal!", "Wow!", "Champion!", "Super writing!", "You did it!", "High five!"],
          items: L => (typeof SPORTS_ITEMS !== "undefined" && SPORTS_ITEMS[L]) || [{ name: "Ball", emoji: "⚽", line: "Kick it!" }],
          cheer: item => item.line || "Hooray!", homePic: "F"
        },
        house: {
          icon: "🛋️", title: "Magic Letter House", subtitle: "✏️ Trace a letter. Find things at home! 🧸",
          foundLabel: "House things", welcome: "Welcome to the House", hello: null,
          intro: "Follow the dots to make the letter. Let's find something at home!",
          praise: ["Wonderful!", "Wow!", "Super writing!", "You did it!", "Fantastic!", "Hooray!"],
          items: L => (typeof HOUSE_ITEMS !== "undefined" && HOUSE_ITEMS[L]) || [{ name: "Sofa", emoji: "🛋️", line: "Sit down!" }],
          cheer: item => item.line || "Hooray!", homePic: "S"
        },
        countries: {
          icon: "🌍", title: "Magic Letter Countries", subtitle: "✏️ Trace a letter. Find a flag! 🚩",
          foundLabel: "Flags", welcome: "Welcome to Countries", hello: null,
          intro: "Follow the dots to make the letter. A flag will wave!",
          praise: ["Wonderful!", "Wow!", "World champion!", "Super writing!", "You did it!", "Fantastic!"],
          items: L => (typeof COUNTRY_ITEMS !== "undefined" && COUNTRY_ITEMS[L]) || [{ name: "World", emoji: "🌍", line: "Our big world!" }],
          cheer: item => item.line || "Hooray!",
          homeSvg: () => (typeof COUNTRY_HOME_SVG !== "undefined" ? COUNTRY_HOME_SVG : null)
        }
      };
      const WORLD_KEYS = Object.keys(WORLDS);

      const targetLetters = Object.keys(animals);
      const $ = id => document.getElementById(id);
      const canvasWrap = $("canvasWrap");
      const drawCanvas = $("drawCanvas");
      const guideCanvas = $("guideCanvas");
      const dctx = drawCanvas.getContext("2d");
      const gctx = guideCanvas.getContext("2d");
      const inkCanvas = document.createElement("canvas"); // cache of finished strokes
      const ictx = inkCanvas.getContext("2d");

      const hint = $("hint"), targetLetterEl = $("targetLetter"), promptTitle = $("promptTitle"), promptSubtitle = $("promptSubtitle");
      const animalCard = $("animalCard"), animalEmoji = $("animalEmoji"), recognized = $("recognized"), animalName = $("animalName");
      const message = $("message"), starsEl = $("stars"), foundCountEl = $("foundCount"), alphabetEl = $("alphabet"), toast = $("toast");
      const clearButton = $("clearButton"), prevLetterButton = $("prevLetterButton"), nextLetterButton = $("nextLetterButton");
      const installButton = $("installButton"), soundButton = $("soundButton");
      const homeEl = $("home"), homeButton = $("homeButton"), caseButton = $("caseButton");
      const worldButtons = Array.from(document.querySelectorAll(".world-btn[data-world]"));
      const appTitle = $("appTitle"), appSubtitle = $("appSubtitle"), foundLabelEl = $("foundLabel"), foundIconEl = $("foundIcon");

      // ---------- state ----------
      let width = 0, height = 0, ratio = 1;
      let strokes = [];           // finished strokes (CSS px)
      let currentStroke = [];
      let drawing = false;
      let guide = null;           // LetterEngine guide for the current target + canvas size
      let glowDots = null;        // guide dots to highlight after an "almost"
      let targetLetter = "A", targetIndex = 0, stars = 0;
      let phase = "home";         // "home" | "play" | "celebrate"
      let world = "zoo";          // key of WORLDS
      let letterCase = "upper";   // "upper" | "lower"
      const perWorld = make => Object.fromEntries(WORLD_KEYS.map(k => [k, make()]));
      const pos = perWorld(() => 0);      // next letter index per world
      let leniency = 0;           // 0..2, grows each time the child is told "almost"
      let idleTimer = null, wipeTimer = null, nextTimer = null, celebrateTimer = null;
      let renderQueued = false, guideQueued = false;
      let audioEnabled = true, audioCtx = null, speechUnlocked = false, preferredVoice = null;
      let deferredInstallPrompt = null;
      let teachingAnimationId = null, teachingAnimationToken = 0, teaching = false;
      let lastPling = 0, lastOneFingerNudge = 0;
      // Found items per world, keyed by UPPERCASE letter (shared by A and a).
      const foundBy = perWorld(() => new Set());
      const foundSet = () => foundBy[world];
      const lastPick = perWorld(() => ({}));   // index of the picture shown last time, per letter
      const alphabetChips = new Map();
      const arbiter = createTouchArbiter();

      const IDLE_CHECK_MS = 2800;   // pause after the last stroke before we "look" at it
      const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
      const lerp = (a, b, t) => a + (b - a) * t;

      // ---------- small helpers ----------
      function clearTimers() {
        clearTimeout(idleTimer); idleTimer = null;
        clearTimeout(wipeTimer); wipeTimer = null;
      }

      function lineWidthInk() { return Math.max(13, Math.min(26, width / 32)); }

      const isLowerCase = () => letterCase === "lower";
      const inCase = L => (isLowerCase() ? L.toLowerCase() : L.toUpperCase());
      // What the voice says: "little A" reads better than a bare "a" (which TTS says as "uh").
      const spoken = letter => (letter === letter.toLowerCase() ? `little ${letter.toUpperCase()}` : letter);

      function setupAlphabet() {
        alphabetEl.innerHTML = "";
        alphabetChips.clear();
        targetLetters.forEach(letter => {
          const chip = document.createElement("div");
          chip.className = "letter-chip";
          chip.textContent = inCase(letter);
          chip.setAttribute("aria-label", `${letter} not discovered yet`);
          alphabetEl.appendChild(chip);
          alphabetChips.set(letter, chip);
        });
      }

      function getItemForLetter(letter) {
        const L = letter.toUpperCase();
        const variants = WORLDS[world].items(L);
        // Random pick each time, but never the same picture twice in a row for a letter.
        const last = lastPick[world][L];
        let index = Math.floor(Math.random() * variants.length);
        if (variants.length > 1 && index === last) index = (index + 1 + Math.floor(Math.random() * (variants.length - 1))) % variants.length;
        lastPick[world][L] = index;
        return variants[index];
      }

      // Show an emoji or an inline SVG picture on the big stage.
      function setPicture(item) {
        if (item && item.svg) { animalEmoji.innerHTML = item.svg; animalEmoji.classList.add("is-svg"); }
        else { animalEmoji.textContent = (item && item.emoji) || "✏️"; animalEmoji.classList.remove("is-svg"); }
        fitPicture();
      }

      // Shrink the picture so it always fits the space above the words (short or old screens).
      const picArea = $("picArea");
      function fitPicture() {
        if (!picArea || typeof getComputedStyle !== "function") return;
        animalEmoji.style.fontSize = "";
        const h = picArea.clientHeight, w = picArea.clientWidth;
        if (!h || !w) return;
        const cssSize = parseFloat(getComputedStyle(animalEmoji).fontSize) || 0;
        const fit = Math.max(40, Math.floor(Math.min((h - 10) / 1.06, (w - 10) / 1.1)));
        if (cssSize && fit < cssSize) animalEmoji.style.fontSize = fit + "px";
      }

      // The big target tile draws the letter from the same strokes the child traces,
      // so the shape always matches the guide (fonts disagree on "a", "g", "t", ...).
      function letterSVG(letter) {
        const lower = LetterEngine.isLower(letter);
        const R = LetterEngine.RULE;
        const strokesRaw = LetterEngine.TEMPLATES[letter] || LetterEngine.TEMPLATES.A;
        const lines = lower ? [
          [R.top, 0.45, 3, ""], [R.mid, 0.6, 3, ' stroke-dasharray="9 7"'],
          [R.base, 0.85, 4.5, ""], [R.desc, 0.35, 3, ' stroke-dasharray="9 7"']
        ].map(([y, o, w, dash]) => `<line x1="-10" x2="110" y1="${y}" y2="${y}" stroke="rgba(255,255,255,${o})" stroke-width="${w}"${dash}/>`).join("") : "";
        const paths = strokesRaw.map(s => {
          const len = s.reduce((acc, p, i) => acc + (i ? Math.hypot(p[0] - s[i - 1][0], p[1] - s[i - 1][1]) : 0), 0);
          return `<polyline points="${s.map(p => p.join(",")).join(" ")}"${len < 6 ? ' stroke-width="18"' : ""}/>`;
        }).join("");
        const vb = lower ? "-12 -8 124 148" : "-6 -1 112 108";
        return `<svg viewBox="${vb}" aria-hidden="true" focusable="false">${lines}<g fill="none" stroke="#fff" stroke-width="13" stroke-linecap="round" stroke-linejoin="round">${paths}</g></svg>`;
      }

      // ---------- saved progress (best effort; private mode may block storage) ----------
      const STORE_KEY = "magicLetterZoo.progress.v1";
      function loadProgress() {
        try {
          const d = JSON.parse(window.localStorage.getItem(STORE_KEY) || "null");
          if (!d || d.v !== 1) return;
          if (WORLDS[d.world]) world = d.world;
          if (d.letterCase === "lower" || d.letterCase === "upper") letterCase = d.letterCase;
          if (Number.isFinite(d.stars) && d.stars >= 0) stars = Math.floor(d.stars);
          WORLD_KEYS.forEach(w => {
            (d.found && Array.isArray(d.found[w]) ? d.found[w] : []).forEach(L => { if (targetLetters.includes(L)) foundBy[w].add(L); });
            const p = d.pos && d.pos[w];
            if (Number.isInteger(p) && p >= 0 && p < targetLetters.length) pos[w] = p;
          });
          audioEnabled = d.sound !== false;
        } catch (err) { /* start fresh */ }
      }
      function saveProgress() {
        try {
          window.localStorage.setItem(STORE_KEY, JSON.stringify({
            v: 1, world, letterCase, stars, pos, sound: audioEnabled,
            found: Object.fromEntries(WORLD_KEYS.map(k => [k, [...foundBy[k]]]))
          }));
        } catch (err) { /* storage is optional */ }
      }

      // ---------- canvas sizing ----------
      function resizeCanvases() {
        const rect = canvasWrap.getBoundingClientRect();
        const newW = Math.max(1, rect.width), newH = Math.max(1, rect.height);
        const newRatio = window.devicePixelRatio || 1;
        if (Math.abs(newW - width) < 0.5 && Math.abs(newH - height) < 0.5 && newRatio === ratio && guide) return;

        // Keep the child's ink glued to the letter when the canvas changes size
        // (mobile URL bar hiding, rotation, split screen...).
        if (width > 1 && height > 1 && strokes.length) {
          const a = LetterEngine.layoutTransform(targetLetter, width, height);
          const b = LetterEngine.layoutTransform(targetLetter, newW, newH);
          const map = p => ({ x: (p.x - a.offX) / a.scale * b.scale + b.offX, y: (p.y - a.offY) / a.scale * b.scale + b.offY });
          strokes = strokes.map(s => s.map(map));
          currentStroke = currentStroke.map(map);
        }

        width = newW; height = newH; ratio = newRatio;
        [drawCanvas, guideCanvas, inkCanvas].forEach(canvas => {
          canvas.width = Math.floor(width * ratio);
          canvas.height = Math.floor(height * ratio);
          if (canvas !== inkCanvas) { canvas.style.width = `${width}px`; canvas.style.height = `${height}px`; }
          canvas.getContext("2d").setTransform(ratio, 0, 0, ratio, 0, 0);
        });

        guide = LetterEngine.buildGuide(targetLetter, width, height);
        recomputeCoverage();
        rebuildInkCache();
        cancelTeachingAnimation();
        drawGuide();
        render();
      }

      function recomputeCoverage() {
        if (!guide) return;
        LetterEngine.resetCoverage(guide);
        strokes.forEach(s => LetterEngine.markCoverage(guide, s));
        if (currentStroke.length) LetterEngine.markCoverage(guide, currentStroke);
      }

      // ---------- ink rendering ----------
      function strokePath(ctx, stroke) {
        ctx.beginPath();
        ctx.moveTo(stroke[0].x, stroke[0].y);
        for (let i = 1; i < stroke.length; i++) {
          const midX = (stroke[i - 1].x + stroke[i].x) / 2;
          const midY = (stroke[i - 1].y + stroke[i].y) / 2;
          ctx.quadraticCurveTo(stroke[i - 1].x, stroke[i - 1].y, midX, midY);
        }
        const last = stroke[stroke.length - 1];
        ctx.lineTo(last.x, last.y);
      }

      function drawInkStroke(ctx, stroke) {
        if (!stroke.length) return;
        const lw = lineWidthInk();
        ctx.save();
        ctx.lineCap = "round";
        ctx.lineJoin = "round";
        if (stroke.length === 1) {
          // A tap still leaves a visible dot, so little fingers always get feedback.
          ctx.fillStyle = "#4f7cff";
          ctx.beginPath(); ctx.arc(stroke[0].x, stroke[0].y, lw / 2, 0, Math.PI * 2); ctx.fill();
          ctx.restore();
          return;
        }
        strokePath(ctx, stroke);
        // Cheap glow instead of shadowBlur (shadowBlur is very slow on budget tablets).
        ctx.lineWidth = lw + 9; ctx.strokeStyle = "rgba(79, 124, 255, 0.16)"; ctx.stroke();
        ctx.lineWidth = lw; ctx.strokeStyle = "#4f7cff"; ctx.stroke();
        ctx.lineWidth = Math.max(5, Math.min(10, width / 74)); ctx.strokeStyle = "rgba(255,255,255,0.75)"; ctx.stroke();
        ctx.restore();
      }

      function rebuildInkCache() {
        ictx.clearRect(0, 0, width, height);
        strokes.forEach(s => drawInkStroke(ictx, s));
      }

      function render() {
        renderQueued = false;
        dctx.clearRect(0, 0, width, height);
        dctx.drawImage(inkCanvas, 0, 0, width, height);
        if (currentStroke.length) drawInkStroke(dctx, currentStroke);
      }

      function queueRender() {
        if (renderQueued) return;
        renderQueued = true;
        requestAnimationFrame(render);
      }

      // ---------- guide rendering (dots that light up as you trace) ----------
      function queueGuide() {
        if (guideQueued) return;
        guideQueued = true;
        requestAnimationFrame(() => { guideQueued = false; drawGuide(); });
      }

      function nextStrokeToTrace() {
        if (!guide) return 0;
        for (let i = 0; i < guide.strokes.length; i++) {
          const dots = guide.dots.filter(d => d.stroke === i);
          const lit = dots.filter(d => d.covered).length;
          if (lit / dots.length < 0.6) return i;
        }
        return -1;
      }

      // School lines for lowercase: top line, dashed midline, strong baseline, faint
      // descender line. Letters sit on them at their true size (o short, h tall, p hangs).
      function drawRuledLines(ctx) {
        const L = LetterEngine.ruledLines(width, height);
        const x0 = Math.max(10, width * 0.04), x1 = width - x0;
        const line = (y, color, lw, dash) => {
          ctx.save();
          ctx.strokeStyle = color; ctx.lineWidth = lw; ctx.lineCap = "round";
          ctx.setLineDash(dash || []);
          ctx.beginPath(); ctx.moveTo(x0, y); ctx.lineTo(x1, y); ctx.stroke();
          ctx.restore();
        };
        line(L.top, "rgba(79, 124, 255, 0.45)", 3);
        line(L.mid, "rgba(255, 111, 177, 0.70)", 3, [16, 12]);
        line(L.base, "rgba(36, 59, 107, 0.65)", 5);
        line(L.desc, "rgba(79, 124, 255, 0.28)", 3, [10, 12]);
      }

      function drawGuide() {
        if (teaching || !guide) return;
        gctx.clearRect(0, 0, width, height);
        if (guide.lower) drawRuledLines(gctx);
        const roadW = Math.max(18, guide.R * 1.1);

        // Soft "road" so the letter shape is obvious even before tracing.
        gctx.save();
        gctx.lineCap = "round"; gctx.lineJoin = "round";
        gctx.lineWidth = roadW;
        gctx.strokeStyle = "rgba(124, 92, 255, 0.10)";
        guide.strokes.forEach(s => {
          gctx.beginPath(); gctx.moveTo(s[0].x, s[0].y);
          for (let i = 1; i < s.length; i++) gctx.lineTo(s[i].x, s[i].y);
          gctx.stroke();
        });
        gctx.restore();

        const r = Math.max(5, Math.min(11, guide.spacing * 0.32));
        const glowing = new Set(glowDots || []);
        guide.dots.forEach(d => {
          gctx.beginPath();
          if (d.covered) {
            gctx.fillStyle = "#ffc93c";
            gctx.arc(d.x, d.y, r * 1.25, 0, Math.PI * 2);
          } else if (glowing.has(d)) {
            gctx.fillStyle = "#ff4fa3";
            gctx.arc(d.x, d.y, r * 1.45, 0, Math.PI * 2);
          } else {
            gctx.fillStyle = "rgba(124, 92, 255, 0.55)";
            gctx.arc(d.x, d.y, r, 0, Math.PI * 2);
          }
          gctx.fill();
          if (glowing.has(d) && !d.covered) {
            gctx.strokeStyle = "rgba(255, 79, 163, 0.35)";
            gctx.lineWidth = 6;
            gctx.beginPath(); gctx.arc(d.x, d.y, r * 2.4, 0, Math.PI * 2); gctx.stroke();
          }
        });

        // The dot on i / j: one big tap target instead of two tiny guide dots.
        (guide.dotStrokes || []).forEach(si => {
          const mine = guide.dots.filter(d => d.stroke === si);
          const lit = mine.some(d => d.covered);
          const p = guide.strokes[si][0];
          gctx.beginPath();
          gctx.fillStyle = lit ? "#ffc93c" : "rgba(124, 92, 255, 0.55)";
          gctx.arc(p.x, p.y, Math.max(r * 2, guide.R * 0.5), 0, Math.PI * 2);
          gctx.fill();
        });

        // Green numbered start dot + arrow on the next stroke to trace.
        const next = nextStrokeToTrace();
        if (next >= 0 && !drawing) {
          const s = guide.strokes[next];
          drawStartDot(s[0], next + 1, "#4bd269", "#1f9e45");
          // The dot on i / j is a tap, not a line: no arrow for it.
          if (!(guide.dotStrokes || []).includes(next)) drawArrow(s[0], s[1]);
        }
      }

      function drawArrow(a, b) {
        const ang = Math.atan2(b.y - a.y, b.x - a.x);
        const len = Math.min(dist(a, b) * 0.5, Math.max(34, guide.R * 1.4));
        const sx = a.x + Math.cos(ang) * guide.R * 0.9, sy = a.y + Math.sin(ang) * guide.R * 0.9;
        const ex = sx + Math.cos(ang) * len, ey = sy + Math.sin(ang) * len;
        gctx.save();
        gctx.strokeStyle = "#1f9e45"; gctx.fillStyle = "#1f9e45";
        gctx.lineWidth = 5; gctx.lineCap = "round";
        gctx.beginPath(); gctx.moveTo(sx, sy); gctx.lineTo(ex, ey); gctx.stroke();
        const h = 13;
        gctx.beginPath();
        gctx.moveTo(ex + Math.cos(ang) * 4, ey + Math.sin(ang) * 4);
        gctx.lineTo(ex - Math.cos(ang - 0.6) * h, ey - Math.sin(ang - 0.6) * h);
        gctx.lineTo(ex - Math.cos(ang + 0.6) * h, ey - Math.sin(ang + 0.6) * h);
        gctx.closePath(); gctx.fill();
        gctx.restore();
      }

      function drawStartDot(point, number, fill = "#ffd85a", ring = "#ff9f43") {
        gctx.save();
        gctx.fillStyle = fill;
        gctx.strokeStyle = ring;
        gctx.lineWidth = 4;
        gctx.beginPath();
        gctx.arc(point.x, point.y, Math.max(15, Math.min(width, height) / 30), 0, Math.PI * 2);
        gctx.fill();
        gctx.stroke();
        gctx.fillStyle = "#ffffff";
        gctx.font = `900 ${Math.max(16, Math.min(width, height) / 22)}px "Comic Sans MS", system-ui, sans-serif`;
        gctx.textAlign = "center";
        gctx.textBaseline = "middle";
        gctx.fillText(String(number), point.x, point.y + 1);
        gctx.restore();
      }

      // ---------- teaching animation ("this is how we write X") ----------
      function cancelTeachingAnimation() {
        teachingAnimationToken += 1;
        teaching = false;
        if (teachingAnimationId) { cancelAnimationFrame(teachingAnimationId); teachingAnimationId = null; }
      }

      function polyLen(points) { let s = 0; for (let i = 1; i < points.length; i++) s += dist(points[i - 1], points[i]); return s; }

      function pointAt(points, frac) {
        const target = polyLen(points) * frac;
        let acc = 0;
        for (let i = 1; i < points.length; i++) {
          const seg = dist(points[i - 1], points[i]);
          if (acc + seg >= target) { const t = seg ? (target - acc) / seg : 0; return { x: lerp(points[i - 1].x, points[i].x, t), y: lerp(points[i - 1].y, points[i].y, t) }; }
          acc += seg;
        }
        return points[points.length - 1];
      }

      function drawTeachingStroke(points, progress, color, lw) {
        if (points.length < 2 || progress <= 0) return;
        const total = polyLen(points), target = total * Math.min(1, progress);
        let travelled = 0;
        gctx.save();
        gctx.lineCap = "round"; gctx.lineJoin = "round";
        gctx.lineWidth = lw; gctx.strokeStyle = color;
        gctx.beginPath(); gctx.moveTo(points[0].x, points[0].y);
        for (let i = 1; i < points.length; i++) {
          const seg = dist(points[i - 1], points[i]);
          if (travelled + seg <= target) { gctx.lineTo(points[i].x, points[i].y); travelled += seg; }
          else { const t = Math.max(0, Math.min(1, (target - travelled) / seg)); gctx.lineTo(lerp(points[i - 1].x, points[i].x, t), lerp(points[i - 1].y, points[i].y, t)); break; }
        }
        gctx.stroke();
        gctx.lineWidth = Math.max(4, lw * 0.36); gctx.strokeStyle = "rgba(255,255,255,0.78)"; gctx.stroke();
        gctx.restore();
      }

      function animateLetter(letter, onDone) {
        cancelTeachingAnimation();
        teaching = true;
        const token = teachingAnimationToken;
        const tStrokes = LetterEngine.layoutStrokes(letter, width, height);
        const duration = Math.max(2300, tStrokes.length * 900 + 700);
        const lw = Math.max(16, Math.min(34, width / 26));
        const start = performance.now();

        function frame(now) {
          if (token !== teachingAnimationToken) return;
          const progress = Math.min(1, (now - start) / duration);
          const active = progress * tStrokes.length;
          gctx.clearRect(0, 0, width, height);
          if (LetterEngine.isLower(letter)) drawRuledLines(gctx);
          gctx.save();
          gctx.fillStyle = "#4f3cc9";
          gctx.font = `900 ${Math.max(22, Math.min(width, height) / 18)}px "Comic Sans MS", system-ui, sans-serif`;
          gctx.textAlign = "center"; gctx.textBaseline = "top";
          gctx.fillText(`This is how we write ${letter}!`, width / 2, 12);
          gctx.restore();
          tStrokes.forEach((s, i) => {
            const p = Math.max(0, Math.min(1, active - i));
            drawTeachingStroke(s, p, i % 2 ? "#ff6fb1" : "#00b894", lw);
            drawStartDot(s[0], i + 1);
            if (p > 0 && p < 1) {
              const q = pointAt(s, p);
              gctx.save();
              gctx.font = `${Math.max(24, Math.min(width, height) / 13)}px system-ui, sans-serif`;
              gctx.textAlign = "center"; gctx.textBaseline = "middle";
              gctx.fillText("⭐", q.x, q.y);
              gctx.restore();
            }
          });
          if (progress < 1) teachingAnimationId = requestAnimationFrame(frame);
          else {
            teachingAnimationId = null;
            setTimeout(() => {
              if (token !== teachingAnimationToken) return;
              teaching = false;
              if (onDone) onDone(); else drawGuide();
            }, 700);
          }
        }
        teachingAnimationId = requestAnimationFrame(frame);
      }

      // ---------- input (one finger draws; multi-touch rejected) ----------
      function toArb(e) {
        const r = drawCanvas.getBoundingClientRect();
        return {
          id: e.pointerId, type: e.pointerType || "mouse", button: e.button,
          x: e.clientX - r.left, y: e.clientY - r.top,
          w: e.width || 0, h: e.height || 0, cw: r.width, ch: r.height,
          t: performance.now()
        };
      }

      function canvasPoint(ev) {
        const r = drawCanvas.getBoundingClientRect();
        return {
          x: Math.max(0, Math.min(width, ev.clientX - r.left)),
          y: Math.max(0, Math.min(height, ev.clientY - r.top))
        };
      }

      function onPointerDown(e) {
        e.preventDefault();
        if (phase !== "play") return;
        const res = arbiter.down(toArb(e));
        if (res.action === "cancel" || res.action === "restart") cancelCurrentStroke(res.reason);
        if (res.action === "start" || res.action === "restart") beginStroke(e);
      }

      function onPointerMove(e) {
        const res = arbiter.move(toArb(e));
        if (res.action === "cancel") { cancelCurrentStroke(res.reason); return; }
        if (res.action !== "draw" || !drawing) return;
        e.preventDefault();
        const events = typeof e.getCoalescedEvents === "function" ? e.getCoalescedEvents() : [];
        const list = events.length ? events : [e];
        const added = [];
        for (const ev of list) {
          const p = canvasPoint(ev);
          const last = currentStroke[currentStroke.length - 1];
          if (!last || dist(last, p) >= 0.75) { currentStroke.push(p); added.push(p); }
        }
        if (!added.length) return;
        const before = currentStroke[currentStroke.length - added.length - 1];
        const lit = LetterEngine.markCoverage(guide, before ? [before, ...added] : added);
        if (lit) { queueGuide(); pling(); }
        queueRender();
      }

      function onPointerUp(e) {
        const res = arbiter.up({ id: e.pointerId, t: performance.now() });
        if (res.action === "end" && drawing) endStroke();
      }

      function beginStroke(e) {
        // If old ink was waiting to be wiped (after a wrong letter), wipe it now so
        // the new attempt starts clean; otherwise just stop the "are you done?" timer.
        if (wipeTimer) clearDrawing(true); else clearTimers();
        unlockSpeech();
        ensureAudio();
        if (teaching) cancelTeachingAnimation();
        try { drawCanvas.setPointerCapture(e.pointerId); } catch (err) { /* ignore */ }
        drawing = true;
        hint.classList.add("hidden");
        currentStroke = [canvasPoint(e)];
        LetterEngine.markCoverage(guide, currentStroke);
        drawGuide();
        queueRender();
        playTinyTap();
      }

      function endStroke() {
        drawing = false;
        if (currentStroke.length) {
          const s = simplifyStroke(currentStroke);
          strokes.push(s);
          drawInkStroke(ictx, s);
          if (s.length > 1) sparkleAt(s[s.length - 1]);
        }
        currentStroke = [];
        queueRender();
        drawGuide();
        afterStroke();
      }

      function cancelCurrentStroke(reason) {
        if (drawing) {
          drawing = false;
          currentStroke = [];
          recomputeCoverage();
          queueRender();
          drawGuide();
        }
        const now = performance.now();
        if (now - lastOneFingerNudge > 4000) {
          lastOneFingerNudge = now;
          showToast("☝️ One finger, please!");
        }
      }

      function simplifyStroke(stroke) {
        const out = [];
        stroke.forEach(p => { if (!out.length || dist(out[out.length - 1], p) > 2) out.push(p); });
        const last = stroke[stroke.length - 1];
        if (out.length && out[out.length - 1] !== last && dist(out[out.length - 1], last) > 0.5) out.push(last);
        return out;
      }

      // ---------- checking the letter ----------
      function afterStroke() {
        if (phase !== "play") return;
        const res = LetterEngine.evaluate(guide, strokes, targetLetter, { final: false, leniency });
        if (res.verdict === "pass") {
          phase = "celebrate";
          clearTimers();
          celebrateTimer = setTimeout(() => succeed(res), 260);
          return;
        }
        clearTimeout(idleTimer);
        idleTimer = setTimeout(finalCheck, IDLE_CHECK_MS);
      }

      // Runs by itself once the child pauses (there is no Done button).
      function finalCheck() {
        clearTimeout(idleTimer); idleTimer = null;
        if (phase !== "play" || drawing) return;
        let res = LetterEngine.evaluate(guide, strokes, targetLetter, { final: true, leniency });

        // Never let a 3-year-old get stuck: third "almost" with real effort counts.
        if (res.verdict === "almost" && leniency >= 2 && res.trace && res.trace.coverage >= 0.45) {
          res = { ...res, verdict: "pass" };
        }

        switch (res.verdict) {
          case "pass":
            phase = "celebrate";
            succeed(res);
            break;
          case "almost":
            leniency = Math.min(2, leniency + 1);
            glowDots = res.trace.uncovered;
            drawGuide();
            message.textContent = "Almost! Trace the pink dots ✨";
            showToast("Almost! Follow the pink dots ✨");
            say("Almost! Follow the pink dots.");
            boop(true);
            break;
          case "other":
            revealOther(res.letter);
            break;
          case "scribble":
            clearDrawing(true);
            message.textContent = "Wow, lots of lines! Let's follow the dots.";
            say(`Let's follow the dots to make ${spoken(targetLetter)}.`);
            boop(true);
            animateLetter(targetLetter);
            break;
          case "retry":
            leniency = Math.min(2, leniency + 1);
            clearDrawing(true);
            message.textContent = `Watch! Then start at the green dot.`;
            say(`Watch me make ${spoken(targetLetter)}. Then you try!`);
            boop(true);
            animateLetter(targetLetter);
            break;
          default: // empty
            if (strokes.length) clearDrawing(true);
        }
      }

      function succeed() {
        clearTimers();
        // Remember progress right away, so leaving mid-celebration still moves on.
        pos[world] = (targetIndex + 1) % targetLetters.length;
        revealItem(targetLetter, true);
        clearTimeout(nextTimer);
        nextTimer = setTimeout(nextTarget, 4600);
      }

      function revealOther(letter) {
        revealItem(letter, false);
        message.textContent = `That looks like ${letter}! Now can you trace ${targetLetter}?`;
        wipeTimer = setTimeout(() => clearDrawing(true), 5200);
      }

      function revealItem(letter, isTarget) {
        const W = WORLDS[world];
        const L = letter.toUpperCase();
        const item = getItemForLetter(letter);
        const alreadyFound = foundSet().has(L);
        setPicture(item);
        recognized.textContent = `I see ${letter}!`;
        animalName.textContent = `${letter} is for ${item.name}!`;
        const praise = W.praise[Math.floor(Math.random() * W.praise.length)];

        if (isTarget) {
          message.textContent = `${praise} ${W.cheer(item)}`;
          stars += alreadyFound ? 1 : 3;
          animateLetter(letter, () => {});
          promptSubtitle.textContent = "Great job! A new letter is coming...";
        } else {
          stars += alreadyFound ? 0 : 1;
        }

        foundSet().add(L);
        saveProgress();
        updateScore();
        markLetter();
        animalCard.classList.remove("pop");
        void animalCard.offsetWidth;
        animalCard.classList.add("pop");
        burstConfetti(isTarget ? 70 : 36);
        cheer(L, isTarget);
        speakItem(L, item);
        showToast(isTarget ? `You did ${letter}! ⭐⭐⭐` : `${letter} is for ${item.name}!`);
      }

      function updateScore() {
        starsEl.textContent = stars;
        foundCountEl.textContent = foundSet().size;
      }

      function markLetter() {
        const base = targetLetter.toUpperCase();
        alphabetChips.forEach((chip, l) => {
          const has = foundSet().has(l);
          chip.textContent = inCase(l);
          chip.classList.toggle("found", has);
          chip.classList.toggle("target", l === base);
          chip.setAttribute("aria-label", `${inCase(l)}${has ? " discovered" : " not discovered yet"}${l === base ? ", current target" : ""}`);
        });
      }

      function clearDrawing(keepMessage = false) {
        clearTimers();
        strokes = [];
        currentStroke = [];
        glowDots = null;
        ictx.clearRect(0, 0, width, height);
        if (guide) LetterEngine.resetCoverage(guide);
        hint.classList.remove("hidden");
        if (!keepMessage) message.textContent = "Start at the green dot and follow the dots!";
        if (!teaching) drawGuide();
        render();
      }

      function resetAnimalStageForTracing() {
        if ("speechSynthesis" in window) window.speechSynthesis.cancel();
        animalCard.classList.remove("pop");
        setPicture({ emoji: "✏️" });
        recognized.textContent = "";
        animalName.textContent = "Trace the letter";
        message.textContent = "Start at the green dot and follow the dots!";
      }

      // letter: any case; it is shown in the current case (ABC / abc).
      function setTarget(letter) {
        targetLetter = inCase(letter);
        targetIndex = targetLetters.indexOf(letter.toUpperCase());
        pos[world] = targetIndex;
        targetLetterEl.innerHTML = letterSVG(targetLetter);
        targetLetterEl.setAttribute("aria-label", `Target letter ${targetLetter}`);
        promptTitle.textContent = `Can you trace ${targetLetter}?`;
        promptSubtitle.textContent = "Start at the green dot. Follow the dots!";
        canvasWrap.classList.toggle("ruled", isLowerCase());
        leniency = 0;
        glowDots = null;
        guide = LetterEngine.buildGuide(targetLetter, width, height);
      }

      function stopEverything() {
        clearTimers();
        clearTimeout(nextTimer); nextTimer = null;
        clearTimeout(celebrateTimer); celebrateTimer = null;
        cancelTeachingAnimation();
        drawing = false;
        currentStroke = [];
        arbiter.reset();
      }

      // Start (or restart) tracing `letter` with a clean page.
      function startLetter(letter, speak = true) {
        stopEverything();
        setTarget(letter);
        resetAnimalStageForTracing();
        markLetter();
        clearDrawing(true);
        phase = "play";
        saveProgress();
        if (speak) say(`Can you trace ${spoken(targetLetter)}?`, 350);
      }

      function nextTarget() {
        startLetter(targetLetters[(targetIndex + 1) % targetLetters.length]);
      }

      function prevTarget() {
        const n = targetLetters.length;
        startLetter(targetLetters[(targetIndex - 1 + n) % n]);
      }

      // ---------- ABC ⇄ abc ----------
      function updateCaseButton() {
        caseButton.classList.toggle("lower", isLowerCase());
        caseButton.setAttribute("aria-pressed", String(isLowerCase()));
        caseButton.setAttribute("aria-label", isLowerCase() ? "Small letters. Tap for big letters" : "Big letters. Tap for small letters");
      }

      function toggleCase() {
        letterCase = isLowerCase() ? "upper" : "lower";
        updateCaseButton();
        // Same letter, other case: A -> a -> A. Found items are shared between cases.
        startLetter(targetLetter.toUpperCase(), false);
        say(isLowerCase() ? `Small letters! Can you trace ${spoken(targetLetter)}?` : `Big letters! Can you trace ${spoken(targetLetter)}?`, 200);
        showToast(isLowerCase() ? "abc  small letters" : "ABC  big letters");
      }

      // ---------- worlds + home screen ----------
      function applyWorld() {
        const W = WORLDS[world];
        WORLD_KEYS.forEach(k => document.body.classList.toggle(`world-${k}`, k === world));
        appTitle.textContent = W.title;
        appSubtitle.textContent = W.subtitle;
        foundLabelEl.textContent = W.foundLabel;
        foundIconEl.textContent = W.icon;
        updateScore();
      }

      function updateHomeProgress() {
        const n = targetLetters.length;
        worldButtons.forEach(btn => {
          const k = btn.dataset.world;
          const prog = btn.querySelector(".world-progress");
          if (prog && foundBy[k]) prog.textContent = `⭐ ${foundBy[k].size} / ${n}`;
          btn.classList.toggle("last", k === world);
        });
      }

      function showHome(speak) {
        stopEverything();
        if ("speechSynthesis" in window) window.speechSynthesis.cancel();
        phase = "home";
        updateHomeProgress();
        homeEl.classList.remove("hidden");
        homeEl.setAttribute("aria-hidden", "false");
        if (speak) say("Where shall we play?", 120);
      }

      function chooseWorld(key) {
        ensureAudio(); unlockSpeech();
        world = WORLDS[key] ? key : "zoo";
        homeEl.classList.add("hidden");
        homeEl.setAttribute("aria-hidden", "true");
        applyWorld();
        startLetter(targetLetters[pos[world]] || "A", false);
        const W = WORLDS[world];
        if (W.hello) setPicture({ emoji: W.hello });
        else { const pics = W.items("A"); setPicture(pics[Math.floor(Math.random() * pics.length)]); }
        recognized.textContent = "Hello, little writer!";
        animalName.textContent = W.welcome;
        message.textContent = W.intro;
        say(`${W.welcome}! Can you trace ${spoken(targetLetter)}?`, 200);
        boop();
      }

      // ---------- effects ----------
      function showToast(text) {
        toast.textContent = text;
        toast.classList.add("show");
        clearTimeout(showToast.timer);
        showToast.timer = setTimeout(() => toast.classList.remove("show"), 1600);
      }

      function burstConfetti(count) {
        const colors = ["#ff6fb1", "#ffd85a", "#4bd269", "#7c5cff", "#00cec9", "#ff9f43"];
        for (let i = 0; i < count; i++) {
          const piece = document.createElement("div");
          piece.className = "confetti";
          piece.style.left = `${Math.random() * 100}vw`;
          piece.style.top = `${-8 - Math.random() * 20}vh`;
          piece.style.background = colors[i % colors.length];
          piece.style.setProperty("--dur", `${1.6 + Math.random() * 1.6}s`);
          piece.style.setProperty("--drift", `${-80 + Math.random() * 160}px`);
          piece.style.setProperty("--spin", `${360 + Math.random() * 720}deg`);
          piece.style.setProperty("--rot", `${Math.random() * 180}deg`);
          document.body.appendChild(piece);
          piece.addEventListener("animationend", () => piece.remove(), { once: true });
        }
      }

      function sparkleAt(point) {
        if (!point) return;
        const icons = ["✨", "⭐", "💫", "🌟"];
        const rect = drawCanvas.getBoundingClientRect();
        for (let i = 0; i < 5; i++) {
          const sp = document.createElement("div");
          sp.className = "sparkle";
          sp.textContent = icons[Math.floor(Math.random() * icons.length)];
          sp.style.left = `${rect.left + point.x}px`;
          sp.style.top = `${rect.top + point.y}px`;
          sp.style.setProperty("--dx", `${-45 + Math.random() * 90}px`);
          sp.style.setProperty("--dy", `${-55 + Math.random() * 60}px`);
          document.body.appendChild(sp);
          sp.addEventListener("animationend", () => sp.remove(), { once: true });
        }
      }

      // ---------- audio ----------
      function ensureAudio() {
        if (!audioEnabled) return null;
        if (!audioCtx) {
          const Context = window.AudioContext || window.webkitAudioContext;
          if (!Context) return null;
          audioCtx = new Context();
        }
        if (audioCtx.state === "suspended") audioCtx.resume();
        return audioCtx;
      }

      function tone(freq, duration, type = "sine", delay = 0, gainValue = 0.06) {
        const ctx = ensureAudio();
        if (!ctx) return;
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, ctx.currentTime + delay);
        gain.gain.setValueAtTime(0.0001, ctx.currentTime + delay);
        gain.gain.exponentialRampToValueAtTime(gainValue, ctx.currentTime + delay + 0.018);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + delay + duration);
        osc.connect(gain).connect(ctx.destination);
        osc.start(ctx.currentTime + delay);
        osc.stop(ctx.currentTime + delay + duration + 0.02);
      }

      function cheer(letter, big) {
        if (!audioEnabled) return;
        const base = 240 + (letter.toUpperCase().charCodeAt(0) - 65) * 9;
        tone(base, 0.14, "triangle", 0, 0.055);
        tone(base * 1.25, 0.14, "triangle", 0.13, 0.065);
        tone(base * 1.5, 0.18, "triangle", 0.26, 0.075);
        if (big) tone(base * 2, 0.22, "sine", 0.43, 0.055);
      }

      // Only happy sounds: no "wrong" buzzer for preschoolers.
      function boop() { if (audioEnabled) tone(540, 0.15, "triangle", 0, 0.04); }
      function playTinyTap() { if (audioEnabled) tone(640, 0.035, "sine", 0, 0.015); }

      // Rising "pling" as dots light up: progress you can hear.
      function pling() {
        if (!audioEnabled || !guide) return;
        const now = performance.now();
        if (now - lastPling < 70) return;
        lastPling = now;
        const frac = guide.dots.filter(d => d.covered).length / guide.dots.length;
        tone(520 + 520 * frac, 0.06, "sine", 0, 0.025);
      }

      function chooseVoice() {
        if (!("speechSynthesis" in window)) return null;
        const voices = window.speechSynthesis.getVoices();
        preferredVoice =
          voices.find(v => /^en(-|_)?/i.test(v.lang) && /female|samantha|victoria|karen|zira|google/i.test(v.name)) ||
          voices.find(v => /^en(-|_)?/i.test(v.lang)) || voices[0] || null;
        return preferredVoice;
      }

      function unlockSpeech() {
        if (speechUnlocked || !audioEnabled || !("speechSynthesis" in window)) return;
        speechUnlocked = true;
        chooseVoice();
        try {
          const warmup = new SpeechSynthesisUtterance(" ");
          warmup.volume = 0;
          if (preferredVoice) warmup.voice = preferredVoice;
          window.speechSynthesis.speak(warmup);
          window.speechSynthesis.cancel();
        } catch (error) { /* speech is optional */ }
      }

      function say(text, delay = 60) {
        if (!audioEnabled || !speechUnlocked || !("speechSynthesis" in window)) return;
        const speak = () => {
          const u = new SpeechSynthesisUtterance(text);
          u.lang = "en-US"; u.rate = 0.8; u.pitch = 1.18; u.volume = 1;
          const voice = chooseVoice();
          if (voice) u.voice = voice;
          window.speechSynthesis.cancel();
          setTimeout(() => window.speechSynthesis.speak(u), delay);
        };
        if (window.speechSynthesis.getVoices().length === 0) {
          window.speechSynthesis.onvoiceschanged = () => { window.speechSynthesis.onvoiceschanged = null; speak(); };
          setTimeout(speak, 250);
        } else speak();
      }

      function speakItem(letter, item) {
        speechUnlocked = speechUnlocked || audioEnabled;
        say(`${letter} is for ${item.name}`);
      }

      function updateSoundButton() { soundButton.textContent = audioEnabled ? "🔊 Sound On" : "🔇 Sound Off"; }

      function toggleSound() {
        audioEnabled = !audioEnabled;
        updateSoundButton();
        saveProgress();
        if (audioEnabled) { ensureAudio(); boop(); showToast("Sound on!"); }
        else { if ("speechSynthesis" in window) window.speechSynthesis.cancel(); showToast("Sound off"); }
      }

      // ---------- install ----------
      async function installWebApp() {
        if (!deferredInstallPrompt) { showToast("Use your browser menu to add this game to the home screen."); return; }
        deferredInstallPrompt.prompt();
        await deferredInstallPrompt.userChoice;
        deferredInstallPrompt = null;
        installButton.classList.remove("show");
      }

      function setupWebAppInstall() {
        if ("serviceWorker" in navigator) {
          window.addEventListener("load", () => { navigator.serviceWorker.register("./sw.js").catch(() => {}); });
        }
        window.addEventListener("beforeinstallprompt", event => {
          event.preventDefault();
          deferredInstallPrompt = event;
          installButton.classList.add("show");
        });
        window.addEventListener("appinstalled", () => {
          deferredInstallPrompt = null;
          installButton.classList.remove("show");
          showToast("Magic Letter Zoo installed!");
        });
      }

      // ---------- wiring ----------
      function initEvents() {
        drawCanvas.addEventListener("pointerdown", onPointerDown);
        drawCanvas.addEventListener("pointermove", onPointerMove);
        // Listen on window so a finger lifted outside the canvas is never "stuck down".
        window.addEventListener("pointerup", onPointerUp);
        window.addEventListener("pointercancel", onPointerUp);
        drawCanvas.addEventListener("lostpointercapture", e => {
          if (drawing && e.pointerId === arbiter.activeId) onPointerUp(e);
        });

        // Stop the browser from hijacking little fingers: no pinch-zoom, no
        // long-press menus, no text-selection magnifier, no pull-to-refresh.
        canvasWrap.addEventListener("touchmove", e => e.preventDefault(), { passive: false });
        canvasWrap.addEventListener("contextmenu", e => e.preventDefault());
        document.addEventListener("gesturestart", e => e.preventDefault());
        document.addEventListener("dblclick", e => e.preventDefault());

        caseButton.addEventListener("click", () => { ensureAudio(); unlockSpeech(); toggleCase(); boop(); });
        // Every "back to the categories" button (the labelled pill by the prompt and the one in the controls row).
        document.querySelectorAll("[data-go-home]").forEach(b => b.addEventListener("click", () => {
          ensureAudio(); unlockSpeech(); showHome(true); boop();
        }));
        worldButtons.forEach(btn => btn.addEventListener("click", () => chooseWorld(btn.dataset.world)));
        clearButton.addEventListener("click", () => {
          ensureAudio(); unlockSpeech();
          if (phase !== "play") return;
          cancelTeachingAnimation();
          clearDrawing();
          boop();
        });
        // ◀ / ▶ beside the big letter: step through the alphabet (also skips a celebration).
        prevLetterButton.addEventListener("click", () => {
          ensureAudio(); unlockSpeech();
          if (phase === "home") return;
          prevTarget();
          boop();
        });
        nextLetterButton.addEventListener("click", () => {
          ensureAudio(); unlockSpeech();
          if (phase === "home") return;
          nextTarget();
          boop();
        });
        installButton.addEventListener("click", installWebApp);
        soundButton.addEventListener("click", () => { unlockSpeech(); toggleSound(); });

        if ("ResizeObserver" in window) {
          new ResizeObserver(() => resizeCanvases()).observe(canvasWrap);
          if (picArea) new ResizeObserver(() => fitPicture()).observe(picArea);
        }
        window.addEventListener("resize", () => { resizeCanvases(); fitPicture(); });
        window.addEventListener("orientationchange", () => setTimeout(() => { resizeCanvases(); fitPicture(); }, 180));
        // Upright phone: "turn me sideways" tip, with a grown-up button to keep playing upright.
        const uprightButton = $("uprightButton");
        if (uprightButton) uprightButton.addEventListener("click", () => {
          document.documentElement.classList.add("upright-ok");
          setTimeout(() => { resizeCanvases(); fitPicture(); }, 50);
        });
      }

      function welcome() {
        loadProgress();
        updateSoundButton();
        updateCaseButton();
        applyWorld();
        setTarget(targetLetters[pos[world]] || "A");
        markLetter();
        // Picture-pack worlds show one of their own SVG pictures on the home screen.
        worldButtons.forEach(btn => {
          const W = WORLDS[btn.dataset.world], pic = btn.querySelector(".world-pic");
          const custom = W && W.homeSvg ? W.homeSvg() : null;
          const item = W && W.homePic ? W.items(W.homePic)[0] : null;
          if (pic && custom) pic.innerHTML = custom;
          else if (pic && item && item.svg) pic.innerHTML = item.svg;
        });
        showHome(false);
      }

      setupAlphabet();
      setupWebAppInstall();
      initEvents();
      welcome();
      requestAnimationFrame(() => { resizeCanvases(); fitPicture(); });
