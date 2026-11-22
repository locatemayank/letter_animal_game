// ==VOICE START==
// Recorded voice. Every line the game says can have a clip: voice/<id>.mp3, where
// id = voiceId(text) ("Can you trace A?" -> voice/can-you-trace-a.mp3).
// A line whose clip is missing (not uploaded yet, offline, old browser) is read by the
// browser's speech voice instead, so the clips can be added a batch at a time.
// Clips are fetched by XHR (works on old Safari too), decoded for WebAudio, or played
// with an <audio> element when there is no WebAudio.
const voiceId = text => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  .toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "");

// Clips that sit in another folder of the site than voice/ (e.g. uploaded as stage01/voice/...):
// { "stage01/": "id id ...", ... }. build.py fills this in from the clips it finds next to index.html.
const VOICE_FOLDERS = {}; // ==VOICE FOLDERS==

const Voice = (() => {
  const DIR = "voice/";
  const GAP = 0.14;          // seconds between chained parts ("Welcome to the Zoo!" + "Can you trace A?")
  const WAIT_MS = 1500;      // longest wait for a clip before using the speech voice instead
  const raw = new Map();     // id -> Promise<ArrayBuffer|null>   (null = no clip)
  const decoded = new Map(); // id -> Promise<AudioBuffer|null>
  let getContext = () => null;
  let playing = [];          // WebAudio sources or <audio> elements of the current line
  let token = 0;

  const folderOf = new Map();
  Object.keys(VOICE_FOLDERS).forEach(folder => VOICE_FOLDERS[folder].split(" ").forEach(id => folderOf.set(id, folder)));
  const url = id => (folderOf.get(id) || "") + DIR + id + ".mp3";

  function fetchRaw(id) {
    if (raw.has(id)) return raw.get(id);
    const p = new Promise(resolve => {
      if (typeof XMLHttpRequest === "undefined") { resolve(null); return; }
      try {
        const xhr = new XMLHttpRequest();
        xhr.open("GET", url(id), true);
        xhr.responseType = "arraybuffer";
        xhr.onload = () => {
          const ok = (xhr.status === 200 || xhr.status === 0) && xhr.response && xhr.response.byteLength > 200;
          // A missing clip may come back as a page (404 page or the offline index.html): not audio.
          const type = (xhr.getResponseHeader && xhr.getResponseHeader("Content-Type")) || "";
          resolve(ok && !/text\/html/i.test(type) ? xhr.response : null);
        };
        xhr.onerror = xhr.ontimeout = xhr.onabort = () => resolve(null);
        xhr.timeout = 15000;
        xhr.send();
      } catch (error) { resolve(null); }
    });
    raw.set(id, p);
    return p;
  }

  function decode(id) {
    const ctx = getContext();
    if (!ctx || !ctx.decodeAudioData) return fetchRaw(id).then(buf => (buf ? "element" : null));
    if (decoded.has(id)) return decoded.get(id);
    const p = fetchRaw(id).then(buf => new Promise(resolve => {
      if (!buf) { resolve(null); return; }
      try {
        // Callback form: old Safari has no promise-returning decodeAudioData. slice(0) keeps
        // the cached ArrayBuffer usable (decoding detaches it).
        const maybe = ctx.decodeAudioData(buf.slice(0), b => resolve(b), () => resolve(null));
        if (maybe && maybe.catch) maybe.catch(() => resolve(null));
      } catch (error) { resolve(null); }
    }));
    decoded.set(id, p);
    // Don't keep a failed decode forever (e.g. the context was not ready yet).
    p.then(b => { if (!b) decoded.delete(id); });
    return p;
  }

  function stop() {
    token++;
    playing.forEach(s => {
      try { if (s.stop) s.stop(); else { s.pause(); s.src = ""; } } catch (error) { /* already ended */ }
    });
    playing = [];
  }

  function playBuffers(ctx, buffers) {
    let t = ctx.currentTime + 0.03;
    buffers.forEach(b => {
      const src = ctx.createBufferSource();
      src.buffer = b;
      src.connect(ctx.destination);
      src.start(t);
      playing.push(src);
      t += b.duration + GAP;
    });
  }

  function playElements(ids, my) {
    let i = 0;
    const next = () => {
      if (my !== token || i >= ids.length) return;
      const a = new Audio(url(ids[i++]));
      playing.push(a);
      a.onended = () => setTimeout(next, GAP * 1000);
      a.onerror = next;
      const p = a.play();
      if (p && p.catch) p.catch(() => {});
    };
    next();
  }

  return {
    setContext(fn) { getContext = fn; },
    // Start downloading clips we will probably need soon, so they play without a pause.
    preload(texts) { texts.forEach(t => fetchRaw(voiceId(t))); },
    stop,
    // Say the parts one after another with recorded clips. Calls fallback(fullText) if any
    // part has no clip (then the whole line uses the same voice).
    say(parts, delay, fallback) {
      stop();
      const my = token;
      const ids = parts.map(voiceId);
      setTimeout(() => {
        if (my !== token) return;
        let done = false;
        const timer = setTimeout(() => { if (!done && my === token) { done = true; fallback(parts.join(" ")); } }, WAIT_MS);
        Promise.all(ids.map(decode)).then(got => {
          if (done || my !== token) return;
          done = true;
          clearTimeout(timer);
          if (got.some(g => !g)) { fallback(parts.join(" ")); return; }
          const ctx = getContext();
          if (got[0] === "element" || !ctx) playElements(ids, my);
          else playBuffers(ctx, got);
        });
      }, delay);
    },
    has(text) { return fetchRaw(voiceId(text)).then(Boolean); }
  };
})();
// ==VOICE END==
