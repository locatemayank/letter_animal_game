// ==ARBITER START==
// Pure (DOM-free) touch arbiter: decides which contact may draw.
//  - one finger draws, everything else is ignored
//  - two fingers landing together (pinch / two-finger tap) cancel the fresh stroke
//    and lock drawing until the fingers lift
//  - a palm / big contact, or a thumb gripping the canvas edge, never draws
//  - a hand resting on the screen does NOT block the drawing finger
//  - a stylus always wins over touch (palm rejection for pen users)
const createTouchArbiter = (opts = {}) => {
  const cfg = {
    palmPx: 64,          // contact width/height (CSS px) treated as a palm
    edgePx: 12,          // touches starting this close to the canvas edge are grip, not ink
    youngMs: 140,        // a stroke younger than this...
    youngTravelPx: 18,   // ...and shorter than this is cancelled if a 2nd finger lands
    pairMs: 350,
    pinchMs: 600,        // a 2nd finger that slides this early in a stroke = pinch, cancel
    pinchTravelPx: 30,         // two touches landing within this window = two-finger gesture
    lockMaxMs: 1500,     // safety: a lock never outlives this without new touches
    ...opts
  };
  const contacts = new Map(); // id -> { type, t0, x0, y0, travel, role }
  let activeId = null;
  let lockedAt = -1;
  let penDown = false;

  const isLocked = now => lockedAt >= 0 && now - lockedAt < cfg.lockMaxMs;

  function down(e) {
    // e: { id, type, x, y, w, h, cw, ch, t, button }
    const c = { type: e.type, t0: e.t, x0: e.x, y0: e.y, x: e.x, y: e.y, travel: 0, role: "idle" };
    contacts.set(e.id, c);

    if (e.type === "mouse") {
      if (e.button !== 0 || activeId !== null) { c.role = "ignored"; return { action: "ignore", reason: "mouse-busy" }; }
      c.role = "ink"; activeId = e.id; return { action: "start" };
    }

    if (e.type === "pen") {
      penDown = true;
      const prev = activeId;
      c.role = "ink"; activeId = e.id; lockedAt = -1;
      if (prev !== null && prev !== e.id) {
        const p = contacts.get(prev); if (p) p.role = "ignored";
        return { action: "restart", cancelId: prev, reason: "pen-wins" };
      }
      return { action: "start" };
    }

    // ---- touch ----
    if (penDown) { c.role = "ignored"; return { action: "ignore", reason: "pen-active" }; }
    if ((e.w || 0) >= cfg.palmPx || (e.h || 0) >= cfg.palmPx) { c.role = "palm"; return { action: "ignore", reason: "palm" }; }
    if (e.x < cfg.edgePx || e.y < cfg.edgePx || e.x > e.cw - cfg.edgePx || e.y > e.ch - cfg.edgePx) {
      c.role = "grip"; return { action: "ignore", reason: "edge" };
    }
    if (isLocked(e.t)) { c.role = "ignored"; lockedAt = e.t; return { action: "ignore", reason: "locked" }; }
    lockedAt = -1;

    if (activeId !== null) {
      const a = contacts.get(activeId);
      const young = a && e.t - a.t0 < cfg.youngMs && a.travel < cfg.youngTravelPx;
      if (young) {
        // Two fingers came down together: drop the fresh stroke, wait for lift.
        const cancelId = activeId;
        a.role = "ignored"; c.role = "ignored"; activeId = null; lockedAt = e.t;
        return { action: "cancel", cancelId, reason: "two-fingers" };
      }
      c.role = "ignored";
      return { action: "ignore", reason: "already-drawing" };
    }

    // Nobody is drawing. Another finger that landed *just* before = two-finger tap.
    for (const [id, o] of contacts) {
      if (id === e.id || o.type !== "touch") continue;
      if ((o.role === "idle" || o.role === "ignored") && e.t - o.t0 < cfg.pairMs) {
        c.role = "ignored"; lockedAt = e.t;
        return { action: "ignore", reason: "two-finger-tap" };
      }
    }
    // Older resting contacts (palm, other hand, thumb) do not block a new finger.
    c.role = "ink"; activeId = e.id;
    return { action: "start" };
  }

  function move(e) {
    const c = contacts.get(e.id);
    if (!c) return { action: "ignore" };
    c.travel += Math.hypot(e.x - c.x, e.y - c.y);
    c.x = e.x; c.y = e.y;
    if (e.id === activeId) return { action: "draw" };
    // A second finger that slides while the stroke is still fresh = pinch/zoom attempt.
    if (activeId !== null && c.type === "touch" && c.role === "ignored" && c.travel > cfg.pinchTravelPx) {
      const a = contacts.get(activeId);
      if (a && a.type === "touch" && e.t - a.t0 < cfg.pinchMs) {
        const cancelId = activeId;
        a.role = "ignored"; activeId = null; lockedAt = e.t;
        return { action: "cancel", cancelId, reason: "pinch" };
      }
    }
    return { action: "ignore" };
  }

  function up(e) {
    const c = contacts.get(e.id);
    contacts.delete(e.id);
    if (c && c.type === "pen") penDown = [...contacts.values()].some(o => o.type === "pen");
    if (![...contacts.values()].some(o => o.type === "touch")) lockedAt = -1;
    if (e.id === activeId) { activeId = null; return { action: "end" }; }
    return { action: "ignore" };
  }

  function reset() { contacts.clear(); activeId = null; lockedAt = -1; penDown = false; }

  return { down, move, up, reset, get activeId() { return activeId; }, get size() { return contacts.size; }, cfg };
};
// ==ARBITER END==
if (typeof module !== "undefined") module.exports = createTouchArbiter;
