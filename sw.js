const CACHE_NAME = "magic-letter-zoo-v25";
// Voice clips live in their own cache so a game update does not download them all again.
// Change this name only if clips are re-recorded under the same file names.
const VOICE_CACHE = "magic-letter-zoo-voice-v1";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icons/icon.svg"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys
          .filter(key => key !== CACHE_NAME && key !== VOICE_CACHE)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

function putInCache(request, response, cacheName = CACHE_NAME) {
  // Only cache good, same-origin responses (never cache a 404 or an opaque error).
  if (response && response.ok && response.type === "basic") {
    const copy = response.clone();
    caches.open(cacheName).then(cache => cache.put(request, copy));
  }
  return response;
}

self.addEventListener("fetch", event => {
  const request = event.request;
  if (request.method !== "GET") return;

  // The page itself: network first, so a new version shows up on the next
  // launch instead of one launch later. Falls back to the cache when offline.
  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request)
        .then(response => putInCache(request, response))
        .catch(() => caches.match(request).then(cached => cached || caches.match("./index.html")))
    );
    return;
  }

  // Voice clips: cache first, kept once heard. A clip that is not uploaded yet (404) or
  // can't be fetched offline is not cached; the game then uses the browser voice.
  if (new URL(request.url).pathname.includes("/voice/")) {
    event.respondWith(
      caches.match(request)
        .then(cached => cached || fetch(request).then(response => putInCache(request, response, VOICE_CACHE)))
        .catch(() => new Response("", { status: 504, statusText: "offline" }))
    );
    return;
  }

  // Everything else (icons, manifest): cache first.
  event.respondWith(
    caches.match(request)
      .then(cached => cached || fetch(request).then(response => putInCache(request, response)))
      .catch(() => caches.match("./index.html"))
  );
});
