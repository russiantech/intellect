const CACHE_NAME = 'v1';
const CACHE_ASSETS = [
    '/',
    '/static/css/styles.css',
    '/static/js/vendor/jquery-3.5.1.min.js',
    '/static/js/vendor/bootstrap.bundle.min.js',
    '/static/js/vendor/OverlayScrollbars.min.js',
    '/static/js/common.js',
    '/static/img/favicon/favicon-192x192.png',
    '/static/img/favicon/favicon-512x512.png'
];

// Install the service worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(CACHE_ASSETS);
        })
    );
});

// Fetch assets from the cache
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});

// Activate the service worker
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});
