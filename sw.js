const CACHE_NAME = 'price-app-v2';
const ASSETS = [
  './',
  './index.html',
  './manifest.json'
];

// インストール
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  // 古いキャッシュをすぐに有効化
  self.skipWaiting();
});

// アクティベート時の古いキャッシュ削除
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter((n) => n !== CACHE_NAME).map((n) => caches.delete(n)))
    )
  );
  self.clients.claim();
});

// フェッチ（ネットワーク優先、失敗時キャッシュ）
self.addEventListener('fetch', (e) => {
  e.respondWith(
    fetch(e.request).then((response) => {
      const clone = response.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
      return response;
    }).catch(() => caches.match(e.request))
  );
});
