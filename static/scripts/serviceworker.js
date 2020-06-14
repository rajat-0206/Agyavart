
// importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js');
// importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js');

//    var firebaseConfig = {
//     apiKey: "AIzaSyBp17YUm4uju7nqT5syTdGIUc_mJ253PH0",
//     authDomain: "agyavart-27f8b.firebaseapp.com",
//     databaseURL: "https://agyavart-27f8b.firebaseio.com",
//     projectId: "agyavart-27f8b",
//     storageBucket: "agyavart-27f8b.appspot.com",
//     messagingSenderId: "223304863434",
//     appId: "1:223304863434:web:585b9e9ace6b42ad51ee33",
//     measurementId: "G-7KW9B9M084"
//   };
//   // Initialize Firebase
//   firebase.initializeApp(firebaseConfig);
//   const messaging = firebase.messaging();

// messaging.usePublicVapidKey("BLVRpuCoOigGCotWJDI-3uQNNHVn-HOGxh9TSB0zgRriUZFDiAlrDWxVsqrcHpUhva7Aj20KsbP1vzSV9QU2Cps");
  



//   messaging.setBackgroundMessageHandler(function(payload) {
//   console.log('[firebase-messaging-sw.js] Received background message ', payload);
//   // Customize notification here
//   const notificationTitle = 'Background Message Title';
//   const notificationOptions = {
//     body: 'Background Message body.',
//     icon: '/firebase-logo.png'
//   };

//   return self.registration.showNotification(notificationTitle,
//     notificationOptions);
// });

// The rest of your Service Worker code goes here ...
/*
Copyright 2015, 2019 Google Inc. All Rights Reserved.
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/

// Incrementing OFFLINE_VERSION will kick off the install event and force
// previously cached resources to be updated from the network.
const OFFLINE_VERSION = 1;
const CACHE_NAME = 'offline';
// Customize this with a different URL if needed.
const OFFLINE_URL = '/offline.html';

self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function(cache) {
      return cache.addAll(
        [
          '/loader.html',
          '/404.html',
          '/offline.html',
        ]
      );
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    // Enable navigation preload if it's supported.
    // See https://developers.google.com/web/updates/2017/02/navigation-preload
    if ('navigationPreload' in self.registration) {
      await self.registration.navigationPreload.enable();
    }
  })());

  // Tell the active service worker to take control of the page immediately.
  self.clients.claim();
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    // Try the cache
    caches.match(event.request).then(function(response) {
      if (response) {
        return response;
      }
      return fetch(event.request).then(function(response) {
        if (response.status === 404) {
          return caches.match('/404.html');
        }
        return response
      });
    }).catch(function() {
      // If both fail, show a generic fallback:
      return caches.match('/offline.html');
    })
  );
});