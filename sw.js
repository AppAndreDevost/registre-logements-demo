self.addEventListener("install", event => {
  console.log("Service worker installé");
});

self.addEventListener("fetch", event => {
  event.respondWith(fetch(event.request));
});