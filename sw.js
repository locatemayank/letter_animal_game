const CACHE_NAME = "magic-letter-zoo-v17";
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
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

function putInCache(request, response) {
  // Only cache good, same-origin responses (never cache a 404 or an opaque error).
  if (response && response.ok && response.type === "basic") {
    const copy = response.clone();
    caches.open(CACHE_NAME).then(cache => cache.put(request, copy));
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

  // Everything else (icons, manifest): cache first.
  event.respondWith(
    caches.match(request)
      .then(cached => cached || fetch(request).then(response => putInCache(request, response)))
      .catch(() => caches.match("./index.html"))
  );
});
