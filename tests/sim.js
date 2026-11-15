// Synthetic "preschooler" handwriting simulator to calibrate the recognizer.
const E = require(process.env.ENGINE || "./engine.js");
let seed = 12345;
const rnd = () => { seed = (seed * 1664525 + 1013904223) % 4294967296; return seed / 4294967296; };
const U = (a, b) => a + (b - a) * rnd();
const SET = process.env.SET || "upper";
const LETTERS = Object.keys(E.TEMPLATES).filter(l => (SET === "lower") === (E.isLower ? E.isLower(l) : false));
const W = +(process.env.W || 640), H = +(process.env.H || 520);

function wobbleStroke(pts, amp, sampleStep) {
  const dense = E.densify(pts, 1);
  const L = E.polylineLength(dense);
  const f1 = U(0.5, 2.2) / Math.max(1, L) * 2 * Math.PI, f2 = U(2, 5) / Math.max(1, L) * 2 * Math.PI;
  const p1 = U(0, 6.28), p2 = U(0, 6.28);
  const out = [];
  let acc = 0, nextAt = 0;
  for (let i = 0; i < dense.length; i++) {
    if (i) acc += Math.hypot(dense[i].x - dense[i - 1].x, dense[i].y - dense[i - 1].y);
    if (acc + 1e-9 < nextAt && i !== dense.length - 1) continue;
    nextAt = acc + U(sampleStep * 0.5, sampleStep * 1.5);
    const a = dense[Math.max(0, i - 1)], b = dense[Math.min(dense.length - 1, i + 1)];
    const l = Math.hypot(b.x - a.x, b.y - a.y) || 1;
    const nx = -(b.y - a.y) / l, ny = (b.x - a.x) / l;
    const off = amp * (0.7 * Math.sin(f1 * acc + p1) + 0.3 * Math.sin(f2 * acc + p2)) + U(-amp, amp) * 0.25;
    out.push({ x: dense[i].x + nx * off, y: dense[i].y + ny * off });
  }
  return out;
}

function trimExtend(s, frac) {
  // frac < 0 trims ends, > 0 overshoots
  if (s.length < 2) return s;
  const a = s[0], b = s[1], y = s[s.length - 1], z = s[s.length - 2];
  const L = E.polylineLength(s);
  const ext = (p, q, d) => { const l = Math.hypot(p.x - q.x, p.y - q.y) || 1; return { x: p.x + (p.x - q.x) / l * d, y: p.y + (p.y - q.y) / l * d }; };
  if (frac >= 0) return [ext(a, b, L * frac * rnd()), ...s, ext(y, z, L * frac * rnd())];
  const dense = E.densify(s, 2); const k = Math.floor(dense.length * -frac * rnd());
  return dense.slice(k, dense.length - Math.floor(dense.length * -frac * rnd()));
}

function kidStrokes(letter, { onGuide = true, quality = 1, dropStroke = false, partial = 0, shuffle = true } = {}) {
  let strokes = E.layoutStrokes(letter, W, H);
  const guide = E.buildGuide(letter, W, H);
  const R = guide.R;
  const cx = W / 2, cy = H / 2;
  // global transform
  const s = onGuide ? U(0.88, 1.12) : U(0.35, 0.7);
  const sx = s * U(0.85, 1.15), sy = s;
  const rot = U(-0.14, 0.14) * quality, shear = U(-0.15, 0.15) * quality;
  const tx = onGuide ? U(-0.35, 0.35) * R : U(-W * 0.2, W * 0.2), ty = onGuide ? U(-0.35, 0.35) * R : U(-H * 0.15, H * 0.15);
  strokes = strokes.map(st => {
    const dx = U(-0.3, 0.3) * R * quality, dy = U(-0.3, 0.3) * R * quality; // strokes not meeting
    return st.map(p => {
      let x = (p.x - cx) * sx, y = (p.y - cy) * sy;
      x += shear * y;
      const xr = x * Math.cos(rot) - y * Math.sin(rot), yr = x * Math.sin(rot) + y * Math.cos(rot);
      return { x: xr + cx + tx + dx, y: yr + cy + ty + dy };
    });
  });
  if (dropStroke && strokes.length > 1) strokes.splice(Math.floor(rnd() * strokes.length), 1);
  if (partial) {
    // keep only first `partial` fraction of total ink
    const dense = strokes.map(st => E.densify(st, 2));
    const total = dense.reduce((a, d) => a + d.length, 0);
    let keep = Math.floor(total * partial);
    strokes = [];
    for (const d of dense) { if (keep <= 0) break; strokes.push(d.slice(0, Math.min(d.length, keep))); keep -= d.length; }
    strokes = strokes.filter(x => x.length > 1);
  }
  const amp = U(0.12, 0.42) * R * quality * (onGuide ? 1 : s);
  strokes = strokes.map(st => wobbleStroke(trimExtend(st, U(-0.08, 0.1)), amp, U(3, 9)));
  if (shuffle) {
    strokes = strokes.map(st => (rnd() < 0.35 ? st.slice().reverse() : st));
    strokes.sort(() => rnd() - 0.5);
  }
  return { strokes, guide };
}

function scribble(letter, kind) {
  const guide = E.buildGuide(letter, W, H);
  const xs = guide.strokes.flat().map(p => p.x), ys = guide.strokes.flat().map(p => p.y);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  const pts = [];
  if (kind === "zigzag") {
    const n = Math.floor(U(8, 22));
    for (let i = 0; i <= n; i++) pts.push({ x: i % 2 ? x1 + U(-20, 20) : x0 + U(-20, 20), y: y0 + (y1 - y0) * i / n });
  } else if (kind === "loops") {
    const n = Math.floor(U(3, 7)) * 40;
    for (let i = 0; i < n; i++) {
      const t = i / 40 * 2 * Math.PI;
      pts.push({ x: (x0 + x1) / 2 + Math.cos(t) * (x1 - x0) * U(0.3, 0.55) + i * 0.3, y: (y0 + y1) / 2 + Math.sin(t) * (y1 - y0) * U(0.3, 0.5) });
    }
  } else { // random walk
    let x = (x0 + x1) / 2, y = (y0 + y1) / 2, a = U(0, 6.28);
    for (let i = 0; i < 260; i++) { a += U(-0.9, 0.9); x += Math.cos(a) * 6; y += Math.sin(a) * 6; x = Math.max(x0 - 30, Math.min(x1 + 30, x)); y = Math.max(y0 - 30, Math.min(y1 + 30, y)); pts.push({ x, y }); }
  }
  return { strokes: [E.densify(pts, 6)], guide };
}

function run(name, gen, n, check) {
  let ok = 0; const verdicts = {}; const fails = {};
  for (let i = 0; i < n; i++) {
    const letter = LETTERS[i % LETTERS.length];
    const { strokes, guide, target } = gen(letter);
    const r = E.evaluate(guide, strokes, target || letter, { final: true, leniency: +(process.env.LEN || 0) });
    verdicts[r.verdict] = (verdicts[r.verdict] || 0) + 1;
    if (check(r, letter)) ok++; else fails[letter] = (fails[letter] || 0) + 1;
  }
  console.log(`${name.padEnd(34)} ${(100 * ok / n).toFixed(1).padStart(5)}%  ${JSON.stringify(verdicts)}  fails:${JSON.stringify(fails)}`);
}

const N = +(process.env.N || 780);
run("good trace -> pass", L => kidStrokes(L), N, r => r.verdict === "pass");
run("sloppy trace(q=1.5) -> pass", L => kidStrokes(L, { quality: 1.5 }), N, r => r.verdict === "pass");
run("missing stroke -> NOT pass", L => kidStrokes(L, { dropStroke: true }), N, (r, L) => E.TEMPLATES[L].length === 1 || r.verdict !== "pass");
run("half traced -> NOT pass", L => kidStrokes(L, { partial: 0.5 }), N, r => r.verdict !== "pass");
run("half traced -> almost", L => kidStrokes(L, { partial: 0.5 }), N, r => r.verdict === "almost");
run("scribble zigzag -> NOT pass", L => scribble(L, "zigzag"), N, r => r.verdict !== "pass");
run("scribble loops -> NOT pass", L => scribble(L, "loops"), N, r => r.verdict !== "pass");
run("scribble walk -> NOT pass", L => scribble(L, "walk"), N, r => r.verdict !== "pass");
run("wrong letter on guide -> NOT pass", L => {
  let other = LETTERS[Math.floor(rnd() * LETTERS.length)]; while (other === L) other = LETTERS[Math.floor(rnd() * LETTERS.length)];
  const k = kidStrokes(other); return { strokes: k.strokes, guide: E.buildGuide(L, W, H), target: L };
}, N, r => r.verdict !== "pass");
run("free draw target (off guide) -> pass", L => kidStrokes(L, { onGuide: false }), N, r => r.verdict === "pass");
run("free draw other -> recognized", L => {
  let other = LETTERS[Math.floor(rnd() * LETTERS.length)]; while (other === L) other = LETTERS[Math.floor(rnd() * LETTERS.length)];
  const k = kidStrokes(other, { onGuide: false }); k.target = L; k.other = other; global.__o = other; return k;
}, N, r => r.verdict === "other" ? r.letter === global.__o : true);
