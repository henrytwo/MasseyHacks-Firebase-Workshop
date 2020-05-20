import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("secret.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

""" Getting multiple items from a collection """
docs = db.collection('items').stream()

for doc in docs:
    print('{} => {}'.format(doc.id, doc.to_dict()))

""" Adding a document """
doc_ref = db.collection('users').document('2020')

doc_ref.set({
    'exists': False
})

""" Getting a single document """
doc_ref = db.collection('users').document('2020')

doc = doc_ref.get()
if doc.exists:
    print('Document data: {}'.format(doc.to_dict()))
else:
    print('No such document!')

""" Realtime updates """
import threading

# Create an Event for notifying main thread.
callback_done = threading.Event()

# Create a callback on_snapshot function to capture changes
def on_snapshot(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        print('Received document snapshot: {} {}'.format(doc.id, doc.to_dict()))
    callback_done.set()

doc_ref = db.collection('cities').document('SF')

# Watch the document
doc_watch = doc_ref.on_snapshot(on_snapshot)

input()
