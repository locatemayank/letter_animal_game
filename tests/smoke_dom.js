const fs = require("fs");
const html = fs.readFileSync(require("path").join(__dirname, "..", "index.html"), "utf8");
const code = html.slice(html.lastIndexOf("<script>") + 8, html.lastIndexOf("</script>"));
const listeners = {};
const ctxProxy = new Proxy({}, { get: (t, k) => (k in t ? t[k] : () => ({ addColorStop() {} })), set: (t, k, v) => { t[k] = v; return true; } });
const els = {};
function mkEl(id) {
  const cls = new Set();
  return els[id] = {
    id, textContent: "", innerHTML: "", style: { setProperty() {} }, width: 0, height: 0, offsetWidth: 1,
    classList: { add: c => cls.add(c), remove: c => cls.delete(c), toggle: (c, on) => (on ? cls.add(c) : cls.delete(c)), contains: c => cls.has(c) },
    setAttribute() {}, appendChild() {}, remove() {},
    addEventListener(t, f) { (listeners[id + ":" + t] ||= []).push(f); },
    getContext: () => ctxProxy,
    getBoundingClientRect: () => ({ left: 0, top: 0, width: 640, height: 520 }),
    setPointerCapture() {}
  };
}
global.document = {
  getElementById: id => els[id] || mkEl(id),
  createElement: () => mkEl("anon" + Math.random()),
  body: { appendChild() {}, classList: { _c: new Set(), toggle(c, on) { on ? this._c.add(c) : this._c.delete(c); }, add(c) { this._c.add(c); }, remove(c) { this._c.delete(c); }, contains(c) { return this._c.has(c); } } },
  addEventListener(t, f) { (listeners["doc:" + t] ||= []).push(f); },
  querySelectorAll: sel => !/world-btn/.test(sel) ? [] : ["Zoo", "Garden", "Sports", "House"].map(W => {
    const b = els["world" + W] || mkEl("world" + W);
    b.dataset = { world: W.toLowerCase() };
    const prog = els["progress" + W] || mkEl("progress" + W), pic = els["pic" + W] || mkEl("pic" + W);
    b.querySelector = q => (q === ".world-progress" ? prog : q === ".world-pic" ? pic : null);
    return b;
  })
};
const store = {};
global.localStorage = { getItem: k => (k in store ? store[k] : null), setItem: (k, v) => { store[k] = String(v); }, removeItem: k => { delete store[k]; } };
global.window = global;
window.addEventListener = (t, f) => { (listeners["win:" + t] ||= []).push(f); };
global.navigator = {};
global.performance = performance;
let rafQ = [];
global.requestAnimationFrame = f => { rafQ.push(f); return rafQ.length; };
global.cancelAnimationFrame = () => {};
const flushRaf = () => { for (let i = 0; i < 400 && rafQ.length; i++) { const q = rafQ; rafQ = []; q.forEach(f => f(performance.now() + 1e5)); } };
eval(code);
flushRaf();
const E = require("./engine.js");
const fire = (k, e) => (listeners[k] || []).forEach(f => f({ preventDefault() {}, pointerType: "touch", button: 0, width: 20, height: 20, ...e }));
let pid = 10;
function trace(letter, opts = {}) {
  const strokes = E.layoutStrokes(letter, 640, 520);
  strokes.forEach(s => {
    const pts = E.densify(s, 6); const id = pid++;
    fire("drawCanvas:pointerdown", { pointerId: id, clientX: pts[0].x, clientY: pts[0].y });
    if (opts.secondFinger) fire("drawCanvas:pointerdown", { pointerId: 999, clientX: 300, clientY: 300 });
    pts.slice(1).forEach(p => fire("drawCanvas:pointermove", { pointerId: id, clientX: p.x, clientY: p.y }));
    fire("win:pointerup", { pointerId: id });
    if (opts.secondFinger) fire("win:pointerup", { pointerId: 999 });
    flushRaf();
  });
}
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const g = id => els[id].textContent;
  const click = id => (listeners[id + ":click"] || []).forEach(f => f());
  console.log("home shown on launch:", !els.home.classList.contains("hidden"), "| zoo progress:", g("progressZoo"));
  click("worldZoo"); flushRaf();
  console.log("start:", g("promptTitle"), "| home hidden:", els.home.classList.contains("hidden"), "| title:", g("appTitle"));
  trace("A");
  await sleep(400); flushRaf();
  console.log("after A trace:", g("recognized"), g("animalName"), "stars", g("stars"));
  await sleep(4800); flushRaf();
  console.log("next target:", g("promptTitle"));
  // two fingers at once -> should not draw anything
  trace("B", { secondFinger: true });
  console.log("toast after 2-finger:", g("toast"));
  await sleep(3200); flushRaf();
  console.log("after 2-finger (expect no reveal):", g("recognized"), "| msg:", g("message"));
  // half trace -> almost
  const s = E.layoutStrokes("B", 640, 520)[0]; const pts = E.densify(s, 6); const id = pid++;
  fire("drawCanvas:pointerdown", { pointerId: id, clientX: pts[0].x, clientY: pts[0].y });
  pts.slice(1).forEach(p => fire("drawCanvas:pointermove", { pointerId: id, clientX: p.x, clientY: p.y }));
  fire("win:pointerup", { pointerId: id });
  (listeners["tryButton:click"] || []).forEach(f => f());
  console.log("half B + Done:", g("message"));
  // finish B
  trace("B"); await sleep(400);
  console.log("after full B:", g("recognized"), "stars", g("stars"), "found", g("foundCount"));
  // resize
  els.canvasWrap.getBoundingClientRect = () => ({ left: 0, top: 0, width: 400, height: 380 });
  (listeners["win:resize"] || []).forEach(f => f()); flushRaf();
  console.log("resize ok");
  els.canvasWrap.getBoundingClientRect = () => ({ left: 0, top: 0, width: 640, height: 520 });
  (listeners["win:resize"] || []).forEach(f => f()); flushRaf();
  await sleep(4800); flushRaf();
  console.log("target now:", g("promptTitle"));
  // zigzag scribble then Done
  let id2 = pid++; fire("drawCanvas:pointerdown", { pointerId: id2, clientX: 150, clientY: 100 });
  for (let i = 0; i < 16; i++) fire("drawCanvas:pointermove", { pointerId: id2, clientX: i % 2 ? 480 : 150, clientY: 100 + i * 20 });
  fire("win:pointerup", { pointerId: id2 });
  (listeners["tryButton:click"] || []).forEach(f => f());
  console.log("scribble + Done:", g("message"));
  await sleep(3500); flushRaf();
  // draw an L freehand small in the corner while target is C
  trace("L"); // L traced on the full layout while target is C
  (listeners["tryButton:click"] || []).forEach(f => f());
  console.log("L while target C:", g("recognized"), "|", g("message"));
  // palm: big contact ignored
  const st = g("stars");
  fire("drawCanvas:pointerdown", { pointerId: 777, clientX: 300, clientY: 300, width: 90, height: 90 });
  for (let i = 0; i < 20; i++) fire("drawCanvas:pointermove", { pointerId: 777, clientX: 300 + i * 5, clientY: 300 });
  fire("win:pointerup", { pointerId: 777 });
  console.log("palm ignored, stars unchanged:", st === g("stars"));

  // ---- lowercase: ABC ⇄ abc keeps the same letter, other case ----
  await sleep(5200); flushRaf();
  const before = g("promptTitle");
  click("caseButton"); flushRaf();
  console.log("case toggle:", before, "->", g("promptTitle"), "| target svg:", /<svg/.test(els.targetLetter.innerHTML), "| ruled:", els.canvasWrap.classList.contains("ruled"));
  const lowTarget = g("promptTitle").match(/trace (\w)\?/)[1];
  const foundBefore = +g("foundCount");
  trace(lowTarget); await sleep(400); flushRaf();
  console.log(`after ${lowTarget} trace:`, g("recognized"), "|", g("animalName"), "| found", foundBefore, "->", g("foundCount"));
  await sleep(4800); flushRaf();
  console.log("next lowercase target:", g("promptTitle"));
  // i: stem + a tap on the dot
  click("newLetterButton"); flushRaf();
  while (!/trace i\?/.test(g("promptTitle"))) { click("newLetterButton"); flushRaf(); }
  trace("i"); await sleep(400); flushRaf();
  console.log("i (stem + dot tap):", g("recognized"), "|", g("animalName"));
  await sleep(4800); flushRaf();

  // ---- Garden world ----
  click("homeButton"); flushRaf();
  console.log("home again:", !els.home.classList.contains("hidden"), "| zoo progress:", g("progressZoo"));
  click("worldGarden"); flushRaf();
  console.log("garden:", g("appTitle"), "|", g("foundLabel"), g("foundCount"), "| body.world-garden:", document.body.classList.contains("world-garden"), "|", g("promptTitle"));
  click("caseButton"); flushRaf();
  const gt = g("promptTitle").match(/trace (\w)\?/)[1];
  trace(gt); await sleep(400); flushRaf();
  console.log(`garden ${gt}:`, g("animalName"), "| svg picture:", /<svg/.test(els.animalEmoji.innerHTML), "|", g("message"));
  await sleep(4800); flushRaf();

  // ---- Sports and House worlds ----
  for (const [W, key] of [["Sports", "sports"], ["House", "house"]]) {
    click("homeButton"); flushRaf();
    console.log(`home pic ${W} is svg:`, /<svg/.test(els["pic" + W].innerHTML));
    click("world" + W); flushRaf();
    const t = g("promptTitle").match(/trace (\w)\?/)[1];
    trace(t); await sleep(400); flushRaf();
    console.log(`${key}:`, g("appTitle"), "|", g("foundLabel"), g("foundCount"), "| body.world-" + key + ":", document.body.classList.contains("world-" + key),
      `| ${t}:`, g("animalName"), "| svg:", /<svg/.test(els.animalEmoji.innerHTML), "|", g("message"));
    await sleep(4800); flushRaf();
  }
  click("homeButton"); flushRaf();
  console.log("progress:", ["Zoo", "Garden", "Sports", "House"].map(W => W + " " + g("progress" + W)).join(", "));
  const saved = JSON.parse(store["magicLetterZoo.progress.v1"] || "{}");
  console.log("saved found:", JSON.stringify(saved.found), "| world:", saved.world);
  process.exit(0);
})().catch(e => { console.error("ERR", e); process.exit(1); });
