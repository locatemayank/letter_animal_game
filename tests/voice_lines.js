// Lists every line the game can say, in recording/upload priority order.
// Writes ../tools/voice_script.tsv  (id <TAB> text <TAB> group)
//   id   = clip file name (voice/<id>.mp3); the game finds a clip with the same voiceId(text) rule.
//   text = exactly what the game passes to say(); the speechSynthesis fallback reads it as is.
// Run: node tests/voice_lines.js
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const here = __dirname;
const read = f => fs.readFileSync(path.join(here, f), "utf8");

// Same rule as voiceId() in voice.js.
const voiceId = text => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");

// ---- data from the game ----
const game = read("game.js");
const grab = (name) => {
  const start = game.indexOf(`const ${name} = {`);
  const end = game.indexOf("\n      };", start);
  return vm.runInNewContext(`(${game.slice(game.indexOf("{", start), end + 8)})`);
};
const animalVariants = grab("animalVariants");
const welcomes = [...game.matchAll(/welcome: "([^"]+)"/g)].map(m => m[1]);
const packs = {};
for (const [file, name] of [["garden.js", "GARDEN_ITEMS"], ["sports.js", "SPORTS_ITEMS"], ["house.js", "HOUSE_ITEMS"],
                            ["countries.js", "COUNTRY_ITEMS"], ["dinos.js", "DINO_ITEMS"]]) {
  const ctx = {};
  vm.runInNewContext(read(file).replace(new RegExp(`const ${name}\\b`), `this.${name}`).replace(/\bconst (\w+) =/g, "this.$1 ="), ctx);
  packs[name] = ctx[name];
}

const LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const spoken = l => (l === l.toLowerCase() ? `little ${l.toUpperCase()}` : l);
const BOTH = [...LETTERS, ...LETTERS.map(l => l.toLowerCase())];

const rows = [];
const seen = new Map();
function add(text, group) {
  const id = voiceId(text);
  if (seen.has(id)) {
    // Same words, different punctuation (e.g. "T-rex" and "T. rex"): they share one clip.
    if (seen.get(id) !== text) console.log(`shared clip: "${text}" uses "${seen.get(id)}"`);
    return;
  }
  seen.set(id, text);
  rows.push([id, text, group]);
}

// 1. prompts (most heard)
add("Where shall we play?", "prompts");
for (const w of welcomes) add(`${w}!`, "prompts");
add("Big letters!", "prompts");
add("Small letters!", "prompts");
add("Almost! Follow the pink dots.", "prompts");
for (const l of BOTH) add(`Can you trace ${spoken(l)}?`, "prompts");
for (const l of BOTH) add(`Let's follow the dots to make ${spoken(l)}.`, "prompts");
for (const l of BOTH) add(`Watch me make ${spoken(l)}. Then you try!`, "prompts");
for (const l of BOTH) add(`That looks like ${spoken(l)}!`, "prompts");

// 2. "A is for ..." per world
const worldItems = [
  ["zoo", animalVariants], ["garden", packs.GARDEN_ITEMS], ["sports", packs.SPORTS_ITEMS],
  ["house", packs.HOUSE_ITEMS], ["countries", packs.COUNTRY_ITEMS], ["dinos", packs.DINO_ITEMS]
];
for (const [w, items] of worldItems) {
  for (const L of LETTERS) for (const it of (items[L] || [])) add(`${L} is for ${it.name}`, w);
}

const out = path.join(here, "..", "tools");
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, "voice_script.tsv"), rows.map(r => r.join("\t")).join("\n") + "\n");
const counts = {};
rows.forEach(r => { counts[r[2]] = (counts[r[2]] || 0) + 1; });
console.log(rows.length, "lines", counts);
