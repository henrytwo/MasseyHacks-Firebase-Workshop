# MasseyHacks Firebase Workshop
## By Henry Tu

## Introduction

### Starter code
Since this workshop will be focused on the Firebase services, I'm going to be working with some website code that I've already baked ahead of time.<br><br>
For the web portion of this workshop, check the `web-starter-code` directory. If you need to refer to the completed website, that's available in the `web-demo-finished` directory. Similarly, a small demo for the admin sdk  is available under `python-admin-sdk-demo`.

### What is Firebase?
Firebase is a development platform by Google that offers services such as Web Hosting, Database, Authentication, etc.

### Why Firebase?
With Firebase, you don't have to spend hours configuring a server and worrying about scaling. All of this is handled by Firebase behind the scenes so you can focus on writing awesome code.

### How do I use Firebase?
Here is the official Firebase guide: [https://firebase.google.com/docs/guides]
<br>
For this workshop, we'll be focusing on Firebase for Web and a bit on the Firebase Python Admin SDK.

### Firebase CLI Installation
For web, you'll need to install the Firebase CLI first. Follow the guide here for more details: [https://firebase.google.com/docs/cli]
<br><br>
Windows Install Executable: [https://firebase.tools/bin/win/instant/latest] (Note: You might need node installed first)<br>
macOS/Linux: Run `curl -sL https://firebase.tools | bash`
<br><br>
Now, open a console and type `firebase login` to authenticate. After that's setup, you're ready to create your first project!

### Creating a project
Go to the console at [https://console.firebase.google.com/] and create a new project. Go to the services that you want to use (i.e. Authentication, Cloud Firestore, etc.) and configure them. I'll go into more details when I discuss the individual services.

## Firebase on the web

### Setup
After you configure Firebase on the console, open your editor of choice and create a new directory to house your project. Navigate to this directory through your console and run `firebase init`.<br><br>
If you followed the instructions properly, it should ask you to select Firebase CLI features. You can change your selection later on by running `firebase init` again, but lets select everything we need at once to save time.<br><br>
For this workshop, select:
- Hosting
- Firestore

(Notice that Authentication is missing here, and that's because it isn't something handled by the CLI)<br><br>
Next, it will ask you to select a project to link to. Go ahead and find the project you just created in the console.<br><br>
Finally, the CLI will ask to confirm the names of files to generate. If you hit enter a few times it'll use the default settings.

### Firebase Hosting
A cool feature of Firebase Hosting is their global CDN. This means that Firebase will automatically cache your website in multiple geographic locations to ensure that it can be accessed quickly from anywhere. Additionally, Firebase handles all the scaling so any sudden spikes in usage are no problem.<br><br>
Here is a partial structure of your project so far:<br>
```
yourProject
  |-public
  | |- index.html
  | |- 404.html
  |-some other random firebase stuff...
```

If you used the default settings, everything under the `public`  folder will be accessible when your website is published. This is your website root.<br><br>
To host your own content, simply place it in this directory. After that's done, you can publish it by running `firebase deploy`. Notice that Firebase automatically generates an URL which can be immediately used to access your website. A custom domain can be configured via the Firebase console.<br><br>
Alternatively,  you can start the local development server by running `firebase serve`. This will come in handy when we need to test our website.

#### Setting up the libraries
Since we're using Firebase Hosting, we can use the integrated CDN to serve all our libraries. Place these imports in your HTML:

```html
<!-- update the version number as needed -->
<script defer src="/__/firebase/7.14.4/firebase-app.js"></script>
<script defer src="/__/firebase/7.14.4/firebase-auth.js"></script>
<script defer src="/__/firebase/7.14.4/firebase-firestore.js"></script>
<script defer src="/__/firebase/init.js"></script>
```
A full list can be found here: [https://firebase.google.com/docs/web/setup#available-libraries]<br><br>
Next, start a JS file and initialize Firebase by creating a Firebase app object:
```javascript
let app = firebase.app();
```

(Note: Usually you would have to configure your API key here, but since we're using Firebase Hosting your project will be automatically linked!)

### Firebase Cloud Firestore
A really useful service that Firebase offers is Cloud Firestore. It's a realtime document based database. This means that Firestore will automatically propogate changes in the database to all connected apps in real time.<br><br>
First, we'll setup Firestore in the console. You'll receive a prompt asking whether you want to start in `production mode` or `test mode`. For now, lets select `test mode` so that we have unrestricted access to the DB. In practice, you'll want to lock this down so that people can't mess with your data.<br><br>
(Tip: For hackathons, it isn't a big priority to secure your DB. Focus on getting your hack working!)<br><br>
If you open up the Firebase console to the Firestore tab, you'll be able to see changes pushed to the DB in real time.

#### Database structure
Firebase has a few different levels in its structure. At the highest level, there are collections which must be uniquely named. Collections contain documents which themselves can contain many fields. This is where you store your conventional data (i.e. strings, integers, or other collections!, etc.)<br><br>
Example:
```
 |-cats <- Collection
 |  |-cat1 <- Document
 |  | |- "location": "Toronto" <- Field
 |  | |- "social": "distance"
 |  |-cat2
 |    |- "meaningOfLife": 42
 |
 |-dogs
   |-woofer
   | |- "color": "purple"
   |-2020
     |- "status": "over" 
```

#### Setup
Create a Firestore object:
```javascript
var db = firebase.firestore();
```
(Note: Make sure you do this after creating the Firebase app object!)

#### Writing data
Here is a detailed guide: [https://firebase.google.com/docs/firestore/manage-data/add-data#add_a_document]<br><br>

To directly set data:
```javascript
db.collection("cities").doc("new-city-id").set({
    name: "Tokyo",
    country: "Japan"
});
```
This is useful if you know the exact document ID you want.<br><br>
To add data with an auto generated document ID:
```javascript
db.collection("cities").add({
    name: "Tokyo",
    country: "Japan"
})
```

#### Reading data
Detailed guide: [https://firebase.google.com/docs/firestore/query-data/get-data]<br><br>
We can read data directly if we know the path:
```javascript
db.collection("cities").doc("SF").get().then(function(doc) {
    if (doc.exists) {
        console.log("Document data:", doc.data());
    } else {
        // doc.data() will be undefined in this case
        console.log("No such document!");
    }
}).catch(function(error) {
    console.log("Error getting document:", error);
});
```

#### Listening for changes
Detailed guide: [https://firebase.google.com/docs/firestore/query-data/listen#web]<br><br>
We can also automatically listen for changes to the database:
```javascript
db.collection("cities").doc("SF")
    .onSnapshot(function(doc) {
        console.log("Current data: ", doc.data());
    });
```
This function will fire every time there is a change to the document.

#### Security
Detailed guide: [https://firebase.google.com/docs/firestore/security/get-started]<br><br>
Security rules are important because they keep your data safe. Without them, people can see all your secrets! Or even worse, they can use all of your quota! Since they are run at every database interaction, they can also be used to validate data.<br><br>
By default, these rules live in the `firestore.rules` file and are pushed automatically when `firebase deploy` is run.<br><br>
Due to limited time, we won't be focusing too much on this.<br><br>
Example security rule:
```
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read: if request.auth.uid != null;
      allow create: if request.auth.uid != null && request.resource.data.owner == request.auth.uid && request.resource.data.text.size() <= 128;
      allow update: if false;
      allow delete: if false;
      allow write: if false;
    }
  }
}
```
Breakdown:
- `request.auth.uid` is the `uid` of the user initiating request
- `request.resource.data` is the object being read/written (All sub attributes are the data itself)

#### Best practices for handling data
A good general rule of thumb is to never trust data that users provide. Let's say you're making a Twitter clone. Simple enough right? Just take whatever text they give you and add it to your HTML. Well... there's a bit of a problem with that. If you don't sanitize your input and treat it as HTML, a cleaver attacker could do something like submitting:
```html
<script>
  alert("Ahahaha, now I'm running JavaScript on your machine!")
</script>
```
How do you prevent an attack like this? Depending on what you're using to build your website, there are different approaches. Frameworks such as Vue.js and React already have features to escape text and prevent this sort of attack. If you're using jQuery, `$(yourElement).text(userText)` is generally safe. Just be careful to never use `$(yourElement).html(userText)` since this will cause the user input to be treated as HTML.

### Firebase Authentication
Detailed guide: [https://firebase.google.com/docs/auth]<br><br>
Firebase Authentication integrates nicely with other services such as Firestore. It allows users to sign in with Email/Password or through other services such as Google, Facebook, etc. No matter which method they choose to use, Firebase handles the complicated OAUTH and links all the authentication methods together. This means you only need to worry about writing one set of code and Firebase will handle the rest.

#### Setup
Go to the Firebase console and visit the Authentication section. Under the `Sign-In method` tab, enable the methods that you want users to be able to log in with.<br><br>
For this workshop, we'll focus on `Sign-In with Google` since it's basically set up out of the box.<br><br>
After enabling `Google`, complete the form annd enter a support email and save your settings. Now we'll setup the code.<br><br>
Create an auth provider object:
```javascript
var provider = new firebase.auth.GoogleAuthProvider();
```

Detailed guide: [https://firebase.google.com/docs/auth/web/google-signin]<br><br>
 
####  Trigger a login window
To trigger the  Google sign-in form, run:
```javascript
firebase.auth().signInWithPopup(provider).then(function (result) {
  // This gives you a Google Access Token. You can use it to access the Google API.
  var token = result.credential.accessToken;
  // The signed-in user info.
  var user = result.user;
  
  // This part will run if the login was successful

}).catch(function (error) {
  // Handle Errors here.
  var errorCode = error.code;
  var errorMessage = error.message;
  // The email of the user's account used.
  var email = error.email;
  // The firebase.auth.AuthCredential type that was used.
  var credential = error.credential;
  // ...
});
```
After logging in, other Firebase services such as Firestore will automatically be updated.
 
#### Trigger a sign out
To immediately sign the user out, run:
```javascript
firebase.auth().signOut().then(function() {
  // Sign-out successful.
  // This part will run if the user was signed out successfully

}, function(error) {
  // An error happened.
  console.log('Could\'t logout')
});
```

#### Listen for auth state change
If you want to run some code as soon as the user logs in/logs off:
```javascript
firebase.auth().onAuthStateChanged(function(user) {
  if (user) {
    // User is signed in.
    var displayName = user.displayName;
    var email = user.email;
    var emailVerified = user.emailVerified;
    var photoURL = user.photoURL;
    var isAnonymous = user.isAnonymous;
    var uid = user.uid;
    var providerData = user.providerData;
    // ...
  } else {
    // User is signed out.
    // ...
  }
});
```

### Firebase Python Admin SDK
Detailed guide: [https://firebase.google.com/docs/reference/admin]<br><br>
The Python Admin SDK is designed primarily for managing your Firebase app from your backend. Although you aren't supposed to use it for client applications, you can use it to quickly interface with Firebase services.

#### Installation
Using pip: `pip install firebase-admin` or `pip3 install firebase-admin` (Note: Might need to run as root)

#### About Service keys
Unlike using Firebase on the web, the Admin SDK uses service keys to link to your project. It is paramount that you do not publish these keys as anyone who has access to them can control your project.<br><br>
(During hackathon environments you might push them to version control for convenience, just be aware of the risks involved. Someone could mess with your stuff!)

#### Generating Service keys
To generate a service key, go to your Firebase console and click on the gear. Next, under `Service accounts`, find `Firebase Admin SDK` and click `Create service account`. Finally, click `Generate new private key`. This should start a download of a JSON file. This is the file you want to keep safe.

#### Setup
The first thing you should do is import the libraries and authenticate:
```python
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("path/to/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
```

#### Add data to Cloud Firestore
Detailed guide: [https://firebase.google.com/docs/firestore/quickstart] (Switch to Python tab)<br><br>

This is the same idea as using Firestore on the web.

```python
doc_ref = db.collection('users').document('alovelace')
doc_ref.set({
    'first': 'Ada',
    'last': 'Lovelace',
    'born': 1815
})
```

#### Get a single document from Cloud Firestore
Detailed guide: [https://firebase.google.com/docs/firestore/query-data/get-data] (Switch to Python tab)
```python
doc_ref = db.collection('cities').document('SF')

doc = doc_ref.get()
if doc.exists:
    print('Document data: {}'.format(doc.to_dict()))
else:
    print('No such document!')
```

#### Get multiple documenets from Cloud Firestore
Detailed guide: [https://firebase.google.com/docs/firestore/query-data/get-data] (Switch to Python tab)
```python
docs = db.collection('cities').stream()

for doc in docs:
    print('{} => {}'.format(doc.id, doc.to_dict()))
```

#### Getting realtime updates from Cloud Firestore
Detailed guide: [https://firebase.google.com/docs/firestore/query-data/listen] (Switch to Python Tab)<br><br>
For this, we'll need to import the `threading` library. 
```python
import threading

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print('Received document snapshot: {}'.format(doc.id))
    callback_done.set()

doc_ref = db.collection('cities').document('SF')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

```

## Wrapping up
There are plenty of useful resources online to get more information about Firebase. They even have a YouTube series to get you started: [https://www.youtube.com/user/Firebase].<br><br>
If you have any other questions, feel free to reach out to me on Discord (henrytwo#4997) or via email (henry (at) henrytu.me).<br><br>
Good luck!
