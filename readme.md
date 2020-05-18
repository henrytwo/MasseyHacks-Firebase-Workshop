# MasseyHacks Firebase Workshop
## By Henry Tu

## Introduction

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
If you followed the instructions properly, it should ask you to select Firebase CLI features. You can change your selection later on by running `firebase init` again, but let's select everything we need at once to save time.<br><br>
For this workshop, select:
- Hosting
- Firestore

(Notice that Authentication is missing here, and that's because it isn't something handled by the CLI)<br><br>
Next, it will ask you to select a project to link to. Go ahead and find the project you just created in the console.<br><br>
Finally, the CLI will ask to confirm the names of files to generate. If you hit enter a few times it'll use the default settings.

### Firebase Hosting
A cool feature of Firebase Hosting is their global CDN. This means that Firebase will automatically cache your website in multiple geographic location to ensure that it can be accessed quickly from anywhere. Additionally, Firebase handles all the scaling so any sudden spikes in usage are no problem.<br><br>
Here is a partial structure of your project so far:<br>
```
yourProject
  |-public
  | |- index.html
  | |- 404.html
  |-some other random firebase stuff...
```

If you used the default settings, everything under the `public`  folder will be accessible when your website is published. This is your website root.<br><br>
To host your own content, simply place it in this directory. After that's done, you can publish it by running `firebase deploy`. Notice that Firebase automatically generates a URL which can be immediately used to access your website. A custom domain can be configured via the Firebase console.<br><br>
Alternatively,  you can start the local development server by running `firebase serve`. This will come in handy when we need to test our website.

### Firebase Cloud Firestore
A really useful service that Firebase offers is Cloud Firestore. It's a realtime document based database. This means that Firestore will automatically propogate changes in the database to all connected apps in real time.<br><br>
First, we'll setup Firestore in the console. You'll receive a prompt asking whether you want to start in `production mode` or `test mode`. For now, let's select `test mode` so that we have unrestricted access to the DB. In practice, you'll want to lock this down so that people can't mess with your data.<br><br>
(Tip: For hackathons, it isn't a big priority to secure your DB. Focus on getting your hack working!)<br><br>

#### Writing data

