// Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCZ8HPRt6HzK3FDTL1dHOnKG3C6dVn96xo",  // Your Firebase Web API Key
    authDomain: "project-be8d3.firebaseapp.com",  // Your Firebase Auth Domain
    projectId: "project-be8d3",  // Your Firebase Project ID
    storageBucket: "project-be8d3.appspot.com",  // Your Firebase Storage Bucket
    messagingSenderId: "637894290222",  // Your Firebase Messaging Sender ID
    appId: "1:637894290222:web:4e9e92ef9c9b4f0b",  // Your Firebase App ID
    measurementId: "G-XXXXXXX"  // Your Firebase Measurement ID (optional)
  };
  
  // Initialize Firebase
  firebase.initializeApp(firebaseConfig);
  
  // Get elements for Google Sign-In
  const googleButton = document.getElementById("google-signin-btn");
  
  // Initialize Firebase Auth
  const auth = firebase.auth();

  gapi.load('auth2', function() {
    gapi.auth2.init({
      client_id: '637894290222-9u4c33jdsp97upr55a1jljkou4sb3g9h.apps.googleusercontent.com'
    });
  });
  
  // Google Sign-In Functionality
  googleButton.addEventListener("click", function () {
    const provider = new firebase.auth.GoogleAuthProvider();
    provider.setCustomParameters({
      // Customize the sign-in experience (optional)
      prompt: "select_account",
    });
  
    auth
      .signInWithPopup(provider)
      .then((result) => {
        // User is signed in, handle user info
        const user = result.user;
        console.log("Google Sign-In successful!", user);
  
        // Handle the user information or store it
        const userInfo = {
          uid: user.uid,
          displayName: user.displayName,
          email: user.email,
          photoURL: user.photoURL,
        };
  
        // Example: Redirect to a different page or use the user data
        window.location.href = "/dashboard";  // Redirect to your dashboard or desired page
      })
      .catch((error) => {
        // Handle Errors here.
        console.error("Error during Google Sign-In: ", error.message);
        alert(error.message);  // Display error message
      });
  });
  