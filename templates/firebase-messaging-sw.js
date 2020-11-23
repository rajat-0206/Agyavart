importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js');

   var firebaseConfig = {
    apiKey: "AIzaSyBp17YUm4uju7nqT5syTdGIUc_mJ253PH0",
    authDomain: "agyavart-27f8b.firebaseapp.com",
    databaseURL: "https://agyavart-27f8b.firebaseio.com",
    projectId: "agyavart-27f8b",
    storageBucket: "agyavart-27f8b.appspot.com",
    messagingSenderId: "223304863434",
    appId: "1:223304863434:web:585b9e9ace6b42ad51ee33",
    measurementId: "G-7KW9B9M084"
  };
  // Initialize Firebase
  const messaging = firebase.messaging();

  messaging.setBackgroundMessageHandler(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  // Customize notification here
  const notificationTitle = 'Background Message Title';
  const notificationOptions = {
    body: 'Background Message body.',
    icon: '/firebase-logo.png'
  };

  return self.registration.showNotification(notificationTitle,
    notificationOptions);
});
