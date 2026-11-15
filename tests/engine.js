// ==ENGINE START==
// Pure (DOM-free) letter engine: guide layout, tracing check, free-draw recognizer.
const LetterEngine = (() => {
  "use strict";

  // Teaching strokes in a 0..100 box. Order + direction follow the usual
  // preschool rule: start at the top, big lines first, then the small ones.
  const TEMPLATES = {
    A: [[[50,8],[14,98]], [[50,8],[86,98]], [[28,66],[72,66]]],
    B: [[[18,8],[18,98]], [[18,8],[52,8],[68,14],[74,28],[68,44],[52,52],[18,52],[56,52],[74,60],[80,76],[72,92],[54,98],[18,98]]],
    C: [[[80,22],[66,11],[48,8],[30,13],[17,28],[11,50],[16,73],[30,90],[48,98],[66,95],[81,82]]],
    D: [[[18,8],[18,98]], [[18,8],[46,8],[66,17],[80,36],[82,56],[76,76],[62,92],[44,98],[18,98]]],
    E: [[[20,8],[20,98]], [[20,8],[78,8]], [[20,53],[68,53]], [[20,98],[80,98]]],
    F: [[[20,8],[20,98]], [[20,8],[78,8]], [[20,53],[68,53]]],
    G: [[[82,22],[68,11],[50,8],[32,13],[18,28],[12,50],[16,73],[30,90],[50,98],[68,94],[80,82],[84,62],[58,62]]],
    H: [[[16,8],[16,98]], [[82,8],[82,98]], [[16,53],[82,53]]],
    I: [[[50,8],[50,98]]],
    J: [[[66,8],[66,72],[60,88],[47,98],[31,96],[18,84]]],
    K: [[[18,8],[18,98]], [[78,8],[20,58],[80,98]]],
    L: [[[20,8],[20,98],[78,98]]],
    M: [[[14,8],[14,98]], [[14,8],[48,66],[82,8],[82,98]]],
    N: [[[16,8],[16,98]], [[16,8],[80,98],[80,8]]],
    O: [[[50,8],[32,12],[18,24],[11,42],[11,62],[18,80],[32,93],[50,98],[68,93],[82,80],[89,62],[89,42],[82,24],[68,12],[50,8]]],
    P: [[[18,8],[18,98]], [[18,8],[52,8],[70,15],[77,30],[70,46],[52,54],[18,54]]],
    Q: [[[50,8],[32,12],[18,24],[11,42],[11,62],[18,80],[32,93],[50,98],[68,93],[82,80],[89,62],[89,42],[82,24],[68,12],[50,8]], [[58,72],[88,100]]],
    R: [[[18,8],[18,98]], [[18,8],[52,8],[70,15],[77,30],[70,46],[52,54],[18,54],[42,54],[80,98]]],
    S: [[[78,20],[64,10],[46,8],[28,14],[20,28],[26,42],[46,50],[66,58],[78,72],[74,88],[56,98],[36,98],[18,88]]],
    T: [[[12,8],[88,8]], [[50,8],[50,98]]],
    U: [[[16,8],[16,68],[24,88],[40,98],[58,98],[74,88],[82,68],[82,8]]],
    V: [[[12,8],[50,98],[88,8]]],
    W: [[[6,8],[28,98],[50,40],[72,98],[94,8]]],
    X: [[[16,8],[84,98]], [[84,8],[16,98]]],
    Y: [[[14,8],[50,52]], [[86,8],[50,52],[50,98]]],
    Z: [[[14,8],[84,8],[14,98],[86,98]]]
  };

  // ---------- lowercase on school lines ----------
  // Lowercase letters sit on ruled lines: top line y=0, dashed midline y=45,
  // baseline y=100, descender line y=132. They keep their true size on the
  // lines (o is short, h is tall, p hangs below), so they are NOT stretched
  // to fill the board the way capitals are.
  const RULE = { top: 0, mid: 45, base: 100, desc: 132 };
  const TUNE = (k, d) => +(typeof process !== "undefined" && process.env && process.env[k] || d);   // test-only overrides
  const LOWER_R = TUNE("LOWER_R", 0.10); // finger tolerance as a fraction of the x-height-to-baseline line height (sim-calibrated)
  const XC = 72.5, RX = 24, RY = 27.5;     // centre/radii of an x-height "o"
  // Elliptical arc in template units. Angles in degrees, screen style
  // (0 = right, 90 = down): decreasing angles run anticlockwise on screen.
  function arc(cx, cy, rx, ry, a0, a1, step = 15) {
    const n = Math.max(2, Math.ceil(Math.abs(a1 - a0) / step));
    const out = [];
    for (let i = 0; i <= n; i++) {
      const a = (a0 + (a1 - a0) * i / n) * Math.PI / 180;
      out.push([Math.round((cx + rx * Math.cos(a)) * 10) / 10, Math.round((cy + ry * Math.sin(a)) * 10) / 10]);
    }
    return out;
  }
  const magicC = arc(48, XC, RX, RY, -30, -380);      // a d g q: "magic c" all the way round
  const bowlR = arc(52, XC, RX, RY, 200, 520);         // b p: bump on the right, clockwise
  const LOWER = {
    a: [magicC, [[72,45],[72,100]]],
    b: [[[28,0],[28,100]], bowlR],
    c: [arc(52, XC, RX, RY, -40, -320)],
    d: [magicC, [[72,0],[72,100]]],
    e: [[[28,72.5], ...arc(51, XC, 23, RY, 0, -320)]],
    f: [[[72,8],[66,2],[57,0],[49,3],[45,12],[44,24],[44,100]], [[28,45],[62,45]]],
    g: [magicC, [[72,45],[72,118],[67,127],[56,131],[42,130],[31,124]]],
    h: [[[28,0],[28,100]], [[28,64],[33,52],[43,46],[56,45],[67,50],[72,62],[72,100]]],
    i: [[[50,45],[50,100]], [[50,22],[50,23]]],
    j: [[[58,45],[58,116],[53,126],[43,131],[31,128],[24,120]], [[58,22],[58,23]]],
    k: [[[30,0],[30,100]], [[70,45],[31,76],[72,100]]],
    l: [[[50,0],[50,100]]],
    m: [[[18,45],[18,100]], [[18,60],[23,49],[32,45],[42,47],[48,56],[49,66],[49,100]], [[49,60],[54,49],[63,45],[73,47],[79,56],[80,66],[80,100]]],
    n: [[[28,45],[28,100]], [[28,62],[33,51],[43,45.5],[56,45],[67,50],[72,62],[72,100]]],
    o: [arc(50, XC, 25, RY, -90, -450)],
    p: [[[28,45],[28,132]], bowlR],
    q: [magicC, [[72,45],[72,132]]],
    r: [[[32,45],[32,100]], [[32,64],[37,52],[47,46],[59,45],[70,50]]],
    s: [[[70,52],[62,46],[50,45],[38,46.5],[31,53],[33,62],[43,68],[57,73],[67,79],[70,88],[65,96],[53,100],[40,100],[30,94]]],
    t: [[[46,12],[46,100]], [[28,45],[66,45]]],
    u: [[[28,45],[28,82],[33,94],[43,100],[57,100],[67,94],[72,82]], [[72,45],[72,100]]],
    v: [[[26,45],[50,100],[74,45]]],
    w: [[[14,45],[31,100],[50,55],[69,100],[86,45]]],
    x: [[[28,45],[72,100]], [[72,45],[28,100]]],
    y: [[[28,45],[50,100]], [[72,45],[36,132]]],
    z: [[[28,45],[72,45],[28,100],[74,100]]]
  };
  Object.assign(TEMPLATES, LOWER);

  const isLower = letter => typeof letter === "string" && letter !== letter.toUpperCase();
  const setOf = letter => (isLower(letter) ? "lower" : "upper");
  const LOWER_MAX_W = Math.max(...Object.values(LOWER).map(s => {
    const xs = s.flat().map(p => p[0]);
    return Math.max(...xs) - Math.min(...xs);
  }));

  // Extra shapes accepted by the free-draw recognizer (common kid variants).
  const VARIANTS = {
    a: [[[...magicC, [72,45], [72,100]]]],
    d: [[[...magicC, [72,0], [72,100]]]],
    g: [[[...magicC, [72,45], [72,118], [67,127], [56,131], [42,130], [31,124]]]],
    q: [[[...magicC, [72,45], [72,132]]]],
    b: [[[[28,0],[28,100],[28,63], ...bowlR.slice(1)]]],
    k: [[[[30,0],[30,100]], [[70,45],[31,76]], [[44,68],[72,100]]]],
    t: [[[[46,12],[46,90],[52,99],[62,100],[68,96]], [[28,45],[66,45]]]],
    y: [[[[28,45],[28,80],[34,94],[46,100],[60,96],[72,82]], [[72,45],[72,120],[64,130],[50,132],[38,128]]]],
    n: [[[[28,45],[28,100],[28,62],[33,51],[43,45.5],[56,45],[67,50],[72,62],[72,100]]]],
    h: [[[[28,0],[28,100],[28,64],[33,52],[43,46],[56,45],[67,50],[72,62],[72,100]]]],
    I: [[[[50,8],[50,98]], [[28,8],[72,8]], [[28,98],[72,98]]]],
    J: [[[[66,8],[66,72],[60,88],[47,98],[31,96],[18,84]], [[40,8],[86,8]]]],
    G: [[[[82,22],[68,11],[50,8],[32,13],[18,28],[12,50],[16,73],[30,90],[50,98],[68,94],[80,82],[82,62]]]],
    M: [[[[14,98],[14,8],[48,98],[82,8],[82,98]]]],
    K: [[[[18,8],[18,98]], [[78,8],[18,58]], [[40,44],[80,98]]]],
    Y: [[[[14,8],[50,52],[86,8]], [[50,52],[50,98]]]],
    B: [[[[18,8],[18,98]], [[18,8],[60,12],[64,48],[18,52]], [[18,52],[70,56],[72,94],[18,98]]]]
  };

  const LOOKALIKE = [
    ["C", "G", "O", "Q", "U"], ["B", "P", "R", "D"], ["E", "F"], ["I", "J", "L", "T"],
    ["M", "N", "W", "V"], ["K", "X", "Y"], ["S", "Z"], ["H", "N"],
    ["b", "d", "p", "q"], ["a", "d", "g", "q"], ["n", "h", "r", "m"], ["i", "j", "l", "t"],
    ["u", "v", "w", "y"], ["c", "e", "o", "a"], ["f", "t"], ["k", "x"]
  ];

  const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
  const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

  function polylineLength(pts) {
    let s = 0;
    for (let i = 1; i < pts.length; i++) s += dist(pts[i - 1], pts[i]);
    return s;
  }

  // Insert points so no gap is bigger than `step` (fast finger flicks leave gaps).
  function densify(pts, step) {
    if (pts.length < 2) return pts.slice();
    const out = [pts[0]];
    for (let i = 1; i < pts.length; i++) {
      const a = pts[i - 1], b = pts[i];
      const d = dist(a, b);
      const k = Math.ceil(d / step);
      for (let j = 1; j <= k; j++) {
        const t = j / k;
        out.push({ x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t });
      }
    }
    return out;
  }

  // Distance from p to segment ab, and the segment's unit direction.
  function segInfo(p, a, b) {
    const vx = b.x - a.x, vy = b.y - a.y;
    const len2 = vx * vx + vy * vy || 1e-9;
    const t = clamp(((p.x - a.x) * vx + (p.y - a.y) * vy) / len2, 0, 1);
    const cx = a.x + vx * t, cy = a.y + vy * t;
    const len = Math.sqrt(len2);
    return { d: Math.hypot(p.x - cx, p.y - cy), ux: vx / len, uy: vy / len };
  }

  // ---------- Guide layout (canvas coordinates) ----------
  function layoutTransform(letter, width, height) {
    const raw = TEMPLATES[letter] || TEMPLATES.A;
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    raw.flat().forEach(([x, y]) => {
      minX = Math.min(minX, x); minY = Math.min(minY, y);
      maxX = Math.max(maxX, x); maxY = Math.max(maxY, y);
    });
    if (isLower(letter)) {
      // Same scale + vertical position for every lowercase letter (school lines),
      // each glyph just centred horizontally.
      const span = RULE.desc - RULE.top;
      const padY = Math.max(16, height * 0.06);
      const padX = Math.max(24, width * 0.1);
      const scale = Math.min((height - padY * 2) / span, (width - padX * 2) / LOWER_MAX_W);
      const offY = (height - span * scale) / 2 - RULE.top * scale + height * 0.02;
      const offX = width / 2 - ((minX + maxX) / 2) * scale;
      return { scale, offX, offY };
    }
    const padding = Math.max(28, Math.min(width, height) * 0.14);
    const rawW = Math.max(1, maxX - minX), rawH = Math.max(1, maxY - minY);
    const scale = Math.min((width - padding * 2) / rawW, (height - padding * 2) / rawH);
    const offX = (width - rawW * scale) / 2 - minX * scale;
    const offY = (height - rawH * scale) / 2 - minY * scale + height * 0.03;
    return { scale, offX, offY };
  }

  function layoutStrokes(letter, width, height) {
    const { scale, offX, offY } = layoutTransform(letter, width, height);
    const raw = TEMPLATES[letter] || TEMPLATES.A;
    return raw.map(s => s.map(([x, y]) => ({ x: x * scale + offX, y: y * scale + offY })));
  }

  // Canvas y of the school lines (for drawing them under lowercase letters).
  function ruledLines(width, height) {
    const { scale, offY } = layoutTransform("o", width, height);
    const y = v => v * scale + offY;
    return { top: y(RULE.top), mid: y(RULE.mid), base: y(RULE.base), desc: y(RULE.desc), scale };
  }

  function buildGuide(letter, width, height) {
    const strokes = layoutStrokes(letter, width, height);
    const ys = strokes.flat().map(p => p.y);
    const lower = isLower(letter);
    // Lowercase: size tolerances by the line height (top line to baseline), not by the
    // glyph, so a short "o" keeps the same finger-sized tolerance as a tall "h".
    const letterH = lower ? (RULE.base - RULE.top) * layoutTransform(letter, width, height).scale
                          : Math.max(...ys) - Math.min(...ys);
    // Fat-finger tolerance: ~12% of letter height (≈ a preschooler's fingertip on a tablet).
    const R = lower ? clamp(letterH * LOWER_R, 20, 50) : clamp(letterH * 0.12, 22, 58);
    const spacing = lower ? clamp(letterH / 16, 10, 26) : clamp(letterH / 15, 12, 30);
    const dots = [];
    strokes.forEach((s, si) => {
      const len = polylineLength(s);
      const count = Math.max(2, Math.round(len / spacing) + 1);
      const dense = densify(s, 1.5);
      const step = polylineLength(dense) / (count - 1);
      let acc = 0, next = 0;
      dots.push({ x: dense[0].x, y: dense[0].y, stroke: si, covered: false });
      for (let i = 1; i < dense.length && dots.filter(d => d.stroke === si).length < count; i++) {
        acc += dist(dense[i - 1], dense[i]);
        if (acc >= step * (next + 1) - 0.01) {
          next++;
          dots.push({ x: dense[i].x, y: dense[i].y, stroke: si, covered: false });
        }
      }
      const last = s[s.length - 1];
      const mine = dots.filter(d => d.stroke === si);
      if (dist(mine[mine.length - 1], last) > spacing * 0.5) dots.push({ x: last.x, y: last.y, stroke: si, covered: false });
    });
    const segments = [];
    strokes.forEach(s => { for (let i = 1; i < s.length; i++) segments.push([s[i - 1], s[i]]); });
    const guideLength = strokes.reduce((acc, s) => acc + polylineLength(s), 0);
    // Tiny strokes are "dots" (the dot on i and j): the child taps them.
    const dotStrokes = strokes.map((s, i) => (polylineLength(s) < R * 0.5 ? i : -1)).filter(i => i >= 0);
    return { letter, strokes, dots, segments, R, letterH, guideLength, spacing, dotStrokes, lower };
  }

  function resetCoverage(guide) { guide.dots.forEach(d => { d.covered = false; }); }

  // Live feedback: light up guide dots near new ink. Returns how many lit up.
  function markCoverage(guide, points) {
    let lit = 0;
    const pts = densify(points, guide.R / 3);
    for (const d of guide.dots) {
      if (d.covered) continue;
      for (const p of pts) {
        if (dist(d, p) <= guide.R) { d.covered = true; lit++; break; }
      }
    }
    return lit;
  }

  // Thresholds get kinder each time the child is told "almost".
  const LENIENCY = [
    { overall: 0.78, perStroke: 0.55, precision: 0.72, align: 0.70, maxInk: 2.4, stray: TUNE("STRAY0", 0.12) },
    { overall: 0.66, perStroke: 0.40, precision: 0.62, align: 0.64, maxInk: 2.8, stray: TUNE("STRAY1", 0.16) },
    { overall: 0.55, perStroke: 0.25, precision: 0.55, align: 0.62, maxInk: 3.0, stray: TUNE("STRAY2", 0.22) }
  ];

  function traceReport(guide, inkStrokes, leniency = 0) {
    const L = LENIENCY[clamp(leniency, 0, LENIENCY.length - 1)];
    const R = guide.R;
    const strokes = inkStrokes.filter(s => s.length > 1 || s.length === 1);
    const ink = strokes.map(s => densify(s, R / 4));
    const flat = ink.flat();
    const inkLength = inkStrokes.reduce((a, s) => a + polylineLength(s), 0);

    // Coverage: guide dots that have ink within R.
    const perStrokeTotals = guide.strokes.map(() => 0);
    const perStrokeHit = guide.strokes.map(() => 0);
    let hit = 0;
    const uncovered = [];
    for (const d of guide.dots) {
      perStrokeTotals[d.stroke]++;
      let ok = false;
      for (const p of flat) { if (dist(d, p) <= R) { ok = true; break; } }
      if (ok) { hit++; perStrokeHit[d.stroke]++; } else uncovered.push(d);
    }
    const coverage = guide.dots.length ? hit / guide.dots.length : 0;
    const perStroke = perStrokeTotals.map((t, i) => (t ? perStrokeHit[i] / t : 0));

    // Precision + alignment: is the ink ON the letter and moving ALONG it?
    let near = 0, stray = 0, alignSum = 0, alignN = 0, segCount = 0;
    ink.forEach(s => {
      for (let i = 0; i < s.length; i++) {
        let best = { d: Infinity, ux: 0, uy: 0 };
        for (const [a, b] of guide.segments) {
          const info = segInfo(s[i], a, b);
          if (info.d < best.d) best = info;
        }
        segCount++;
        if (best.d > R * 1.5) stray++;
        if (best.d <= R * 1.3) {
          near++;
          if (i > 0) {
            const dx = s[i].x - s[i - 1].x, dy = s[i].y - s[i - 1].y;
            const l = Math.hypot(dx, dy);
            if (l > 0.5) { alignSum += Math.abs((dx * best.ux + dy * best.uy) / l); alignN++; }
          }
        }
      }
    });
    const precision = segCount ? near / segCount : 0;
    // Stray ink: share of ink clearly off the letter (an extra stick, a missing-letter part).
    const strayFrac = segCount ? stray / segCount : 0;
    const align = alignN ? alignSum / alignN : 0;
    const inkRatio = guide.guideLength ? inkLength / guide.guideLength : 0;

    const pass =
      coverage >= L.overall &&
      Math.min(...perStroke) >= L.perStroke &&
      precision >= L.precision &&
      align >= L.align &&
      inkRatio <= L.maxInk &&
      strayFrac <= L.stray;

    const onGuide = precision >= 0.45 && align >= 0.55 && inkRatio <= L.maxInk + 0.6;
    const almost = !pass && onGuide && coverage >= 0.22;
    // Clearly tracing the guide (ink sits on it and follows it) but not finished yet.
    const tracingEffort = !pass && precision >= 0.85 && align >= 0.7 && coverage >= 0.35;
    let weakest = 0;
    perStroke.forEach((c, i) => { if (c < perStroke[weakest]) weakest = i; });

    return { coverage, perStroke, precision, align, inkRatio, inkLength, strayFrac, pass, onGuide, almost, tracingEffort, weakestStroke: weakest, uncovered };
  }

  // ---------- $P point-cloud recognizer (order/direction independent) ----------
  const NP = 32;

  function cloudOf(strokes) {
    const pts = [];
    strokes.forEach((s, id) => s.forEach(p => pts.push({ x: p.x, y: p.y, id })));
    if (!pts.length) return [];
    let len = 0;
    for (let i = 1; i < pts.length; i++) if (pts[i].id === pts[i - 1].id) len += dist(pts[i - 1], pts[i]);
    let out;
    if (len < 1e-6) {
      out = Array.from({ length: NP }, () => ({ ...pts[0] }));
    } else {
      const I = len / (NP - 1);
      let D = 0;
      out = [{ ...pts[0] }];
      const src = pts.map(p => ({ ...p }));
      for (let i = 1; i < src.length; i++) {
        if (src[i].id !== src[i - 1].id) continue;
        const d = dist(src[i - 1], src[i]);
        if (D + d >= I && d > 0) {
          const t = (I - D) / d;
          const q = { x: src[i - 1].x + t * (src[i].x - src[i - 1].x), y: src[i - 1].y + t * (src[i].y - src[i - 1].y), id: src[i].id };
          out.push(q);
          src.splice(i, 0, q);
          D = 0;
        } else D += d;
        if (out.length >= NP) break;
      }
      while (out.length < NP) out.push({ ...src[src.length - 1] });
    }
    let minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    out.forEach(p => { minX = Math.min(minX, p.x); minY = Math.min(minY, p.y); maxX = Math.max(maxX, p.x); maxY = Math.max(maxY, p.y); });
    const size = Math.max(maxX - minX, maxY - minY) || 1;
    out = out.map(p => ({ x: (p.x - minX) / size, y: (p.y - minY) / size }));
    const cx = out.reduce((a, p) => a + p.x, 0) / NP, cy = out.reduce((a, p) => a + p.y, 0) / NP;
    return out.map(p => ({ x: p.x - cx, y: p.y - cy }));
  }

  function cloudDistance(a, b, start) {
    const n = a.length, matched = new Array(n).fill(false);
    let sum = 0, i = start;
    do {
      let idx = -1, min = Infinity;
      for (let j = 0; j < n; j++) {
        if (matched[j]) continue;
        const d = (a[i].x - b[j].x) ** 2 + (a[i].y - b[j].y) ** 2;
        if (d < min) { min = d; idx = j; }
      }
      matched[idx] = true;
      sum += (1 - ((i - start + n) % n) / n) * Math.sqrt(min);
      i = (i + 1) % n;
    } while (i !== start);
    return sum;
  }

  function greedyMatch(a, b) {
    const step = Math.floor(Math.pow(NP, 0.5));
    let min = Infinity;
    for (let i = 0; i < NP; i += step) min = Math.min(min, cloudDistance(a, b, i), cloudDistance(b, a, i));
    return min;
  }

  const toPts = strokes => strokes.map(s => s.map(([x, y]) => ({ x, y })));
  const CLOUDS = [];
  const addCloud = (letter, s) => CLOUDS.push({ letter, set: setOf(letter), cloud: cloudOf(toPts(s)), aspect: aspectOf(toPts(s)) });
  Object.entries(TEMPLATES).forEach(([letter, s]) => addCloud(letter, s));
  Object.entries(VARIANTS).forEach(([letter, list]) => list.forEach(s => addCloud(letter, s)));
  // How much ink a neat copy of each letter uses relative to its size (m, w, g are "busy").
  const INK_DENSITY = {};
  Object.entries(TEMPLATES).forEach(([letter, s]) => {
    const pts = toPts(s), f = pts.flat();
    const xs = f.map(p => p.x), ys = f.map(p => p.y);
    const diag = Math.hypot(Math.max(...xs) - Math.min(...xs), Math.max(...ys) - Math.min(...ys));
    INK_DENSITY[letter] = pts.reduce((a, st) => a + polylineLength(st), 0) / Math.max(1, diag);
  });

  function aspectOf(strokes) {
    const f = strokes.flat();
    const xs = f.map(p => p.x), ys = f.map(p => p.y);
    const w = Math.max(...xs) - Math.min(...xs), h = Math.max(...ys) - Math.min(...ys);
    return Math.max(0.05, w) / Math.max(0.05, h);
  }

  function freeRecognize(inkStrokes, targetLetter, leniency = 0) {
    const strokes = inkStrokes.filter(s => s.length > 1);
    if (!strokes.length) return null;
    const flat = strokes.flat();
    const xs = flat.map(p => p.x), ys = flat.map(p => p.y);
    const w = Math.max(...xs) - Math.min(...xs), h = Math.max(...ys) - Math.min(...ys);
    const diag = Math.hypot(w, h);
    const inkLength = strokes.reduce((a, s) => a + polylineLength(s), 0);
    if (diag < 30) return { tooSmall: true };
    // Scribble: lots of ink packed into a small box.
    const isScribble = inkLength / Math.max(1, diag) > Math.max(4.4, (INK_DENSITY[targetLetter] || 0) * 1.6);
    const set = setOf(targetLetter);

    const cloud = cloudOf(strokes);
    const userAspect = Math.max(4, w) / Math.max(4, h);
    const byLetter = {};
    CLOUDS.forEach(t => {
      if (t.set !== set) return;          // never compare "a" with "A"
      let d = greedyMatch(cloud, t.cloud);
      // Gentle aspect-ratio tie-breaker (helps I vs L vs T, O vs Q stays shape-driven).
      d += Math.min(1.2, Math.abs(Math.log(userAspect / t.aspect)) * 0.6);
      if (!(t.letter in byLetter) || d < byLetter[t.letter]) byLetter[t.letter] = d;
    });
    const ranked = Object.entries(byLetter).map(([letter, d]) => ({ letter, d })).sort((a, b) => a.d - b.d);
    const best = ranked[0], second = ranked[1];
    const target = ranked.find(r => r.letter === targetLetter);
    const sameGroup = LOOKALIKE.some(g => g.includes(targetLetter) && g.includes(best.letter));
    // $P distances: a fair kid letter is ~0.4-1.6, scribbles/blobs are >2.
    const maxD = [1.9, 2.15, 2.4][clamp(leniency, 0, 2)];
    const targetOk = !isScribble && !!target && target.d < maxD && (
      target === best ||
      target.d <= best.d * 1.12 + 0.08 ||
      (sameGroup && target.d <= best.d * 1.3 + 0.12)
    );
    const confident = !isScribble && best.d < 1.8 && best.d <= second.d * 0.88;
    return { ranked: ranked.slice(0, 5), best, target, targetOk, confident, isScribble, inkLength, diag };
  }

  // ---------- Top-level decision ----------
  // verdict: pass | almost | other | retry | scribble | wait | empty
  function evaluate(guide, inkStrokes, targetLetter, { final = false, leniency = 0 } = {}) {
    const minLen = Math.max(8, guide.R * 0.3);
    // Taps count when they land on a dot (i, j); other tiny marks are ignored.
    const onDot = s => (guide.dotStrokes || []).some(i => s.every(p => dist(p, guide.strokes[i][0]) <= guide.R * 1.6));
    const real = inkStrokes.filter(s => s.length && (polylineLength(s) >= minLen || onDot(s)));
    if (!real.length) return { verdict: final ? "empty" : "wait" };
    const trace = traceReport(guide, real, leniency);
    if (trace.pass) return { verdict: "pass", letter: targetLetter, mode: "trace", trace };
    if (!final) return { verdict: "wait", trace };
    const free = freeRecognize(real, targetLetter, leniency);
    const clearTarget = free && free.targetOk && free.target === free.best && free.target.d < 1.5;
    // Child is clearly tracing but stopped early -> point at the missing part
    // (unless the drawing on its own is already an unmistakable target letter).
    if (trace.tracingEffort && !clearTarget) return { verdict: "almost", letter: targetLetter, trace, free };
    if (!free || free.tooSmall) return { verdict: trace.almost ? "almost" : "retry", trace, free };
    if (free.isScribble) return { verdict: "scribble", trace, free };
    // Off the guide but clearly the target letter (e.g. written next to it): still a win.
    if (free.targetOk) return { verdict: "pass", letter: targetLetter, mode: "free", trace, free };
    if (free.confident && free.best.letter !== targetLetter) return { verdict: "other", letter: free.best.letter, trace, free };
    if (trace.almost) return { verdict: "almost", letter: targetLetter, trace, free };
    return { verdict: "retry", trace, free };
  }

  return { TEMPLATES, RULE, isLower, ruledLines, layoutTransform, layoutStrokes, buildGuide, resetCoverage, markCoverage, traceReport, freeRecognize, evaluate, polylineLength, densify };
})();
// ==ENGINE END==
if (typeof module !== "undefined") module.exports = LetterEngine;
