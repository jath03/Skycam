var urlsToCache = [
  '/',
  './',
  '/index.html',
  '/manifest.json',
  '/style.css',
  '/scripts/main.js',
  '/scripts/jquery-3.2.1.min.js',
  '/sw.js',
  '/page.html',
  '/offline.html',
  '/icons/testing-30x30.png',
  '/icons/testing-60x60.png',
  '/icons/testing-90x90.png',
  '/icons/testing-180x180.png',
  '/icons/testing-200x200.png'
];

var cacheName = "test-webapp-v1";

self.addEventListener("install", function(event) {
  event.waitUntil(caches.open(cacheName).then(function(cache) {
    console.log('opened cache');
    return cache.addAll(urlsToCache);
  }));
});

self.addEventListener("fetch", function(event) {
  event.respondWith(caches.match(event.request).then(function(response) {
    if (response) {
      return response;
    }
    return fetch(event.request).catch(function(error) {
      console.log("Responding with offline page for request of " + event.request.url + " because of error: \"" + error + "\"");
      return caches.match("/offline.html");
    });
  }));
});

self.addEventListener("activate", function(event) {
  event.waitUntil(caches.keys().then(function(cacheNames) {
    console.log(cacheNames);
    Promise.all(cacheNames.filter(function(cN) {
      if (cN === cacheName) {
        return false;
      }
      return true;
    }).map(function(cN) {
      return caches.delete(cN);
    }));
  }));
});
