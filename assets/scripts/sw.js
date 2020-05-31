
//app Name
var CACHE_NAME = 'agyavart_app';

//file to cache
var staticAssets = [
'./',
'./static/styles/fmt.css',
'./static/styles/login.css',
'./static/styles/mail.css',
'./static/styles/mainsetup.css',
'./static/styles/mesage.css',
'./static/styles/profile.css',
'./static/styles/register.css',
'./static/styles/side_nav.css',
'./templates/rmail.html',
'./templates/Login.html',
'./templates/signup.html',
'./templates/profile.html',	
'./templates/msg.html',
'./templates/setting.html',
'./templates/recieve.html',


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


  self.addEventListener('activate', function(event){

	self.ClientRectList.claim();
  });