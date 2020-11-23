
//app Name
var CACHE_NAME = 'agyavart_app';

//file to cache
var staticAssets = [
'/./',
'/static/styles/fmt.css',
'/static/styles/login.css',
'/static/styles/mail.css',
'/static/styles/mainsetup.css',
'/static/styles/mesage.css',
'/static/styles/profile.css',
'/static/styles/register.css',
'/static/styles/side_nav.css',



];

self.addEventListener('install', function(event) {
	// Perform install steps
	event.waitUntil(
	  caches.open(CACHE_NAME)
		.then(function(cache) {
		  console.log('Opened cache');
		  return cache.addAll(staticAssets);
		})
	);
  });


  self.addEventListener('activate', function(event) {

	var cacheWhitelist = ['pages-cache-v1', 'blog-posts-cache-v1'];
  
	event.waitUntil(
	  caches.keys().then(function(cacheNames) {
		return Promise.all(
		  cacheNames.map(function(cacheName) {
			if (cacheWhitelist.indexOf(cacheName) === -1) {
			  return caches.delete(cacheName);
			}
		  })
		);
	  })
	);
  });

  self.addEventListener('fetch', function(event) {
	event.respondWith(
	  caches.match(event.request)
		.then(function(response) {
		  // Cache hit - return response
		  if (response) {
			return response;
		  }
  
		  return fetch(event.request).then(
			function(response) {
			  // Check if we received a valid response
			  if(!response || response.status !== 200 || response.type !== 'basic') {
				return response;
			  }
  
			  var responseToCache = response.clone();
  
			  caches.open(CACHE_NAME)
				.then(function(cache) {
				  cache.put(event.request, responseToCache);
				});
  
			  return response;
			}
		  );
		})
	  );
  });