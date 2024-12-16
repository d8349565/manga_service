const CACHE_NAME = 'manga-reader-v1';
const ASSETS_TO_CACHE = [
  '/static/comics.html',
  '/static/chapters.html',
  '/static/reader.html',
  '/static/history.html',
  '/static/login.html',
  '/static/admin.html',
  '/static/manifest.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(ASSETS_TO_CACHE))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    fetch(event.request)
      .catch(() => {
        return caches.match(event.request);
      })
  );
}); 