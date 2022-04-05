import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

data = {
    'name': 'John Doe',
    'age': 25,
    'address': {
        'city': 'Elr',
        'state': 'AP',
        'country': 'IND'
    },
    'socials': ['linkedIn', 'youtube', 'instagram']
}

# CREATE

# Add document with auto ID's
db.collection('people').add(data)

# Set document with known ID like John Doe
db.collection('people').document('JohnDoe').set(data)

# Adding collection to the known document ID like John Doe
db.collection('people').document('JohnDoe').collection('movies').document('HP').set({'name': 'Harry Potter'})


# READ

# Get all documents from the collection
people = db.collection('people').get()
for person in people:
    print(person.to_dict())

# Getting a document with known ID
person = db.collection('people').document('JohnDoe').get()
if person.exists:
    print(person.to_dict())

# Querying based on where condition
people = db.collection('people').where('age','>=', 25).get()
for person in people:
    print(person.to_dict())

# Querying based on array value condition
people = db.collection('people').where('socials', 'array_contains', 'youtube').get()
for person in people:
    print(person.to_dict())

# Querying based on IN operator
people = db.collection('people').where('age', 'in', [25]).get()
for person in people:
    print(person.to_dict())


# UPDATE

# update document with known key
db.collection('people').document('JohnDoe').update({'age':50})

# update document by increment
db.collection('people').document('JohnDoe').update({'age':firestore.Increment(10)})

# update document by removing array value
db.collection('people').document('JohnDoe').update({'socials':firestore.ArrayRemove(['linkedIn'])})

# update document by adding array value
db.collection('people').document('JohnDoe').update({'socials':firestore.ArrayUnion(['linkedIn'])})

# updating document with unknown ID
people = db.collection('people').where('age', '==', 60).get()
for person in people:
    key = person.id
    db.collection('people').document(key).update({'age_group':'middle_aged'})


# DELETE

# delete field data inside the document using known id
db.collection('people').document('JohnDoe').update({'socials':firestore.DELETE_FIELD})

# delete collection associated with the document with known id
movies = db.collection('people').document('JohnDoe').collection('movies').get()
for movie in movies:
    key = movie.id
    db.collection('people').document('JohnDoe').collection('movies').document(key).delete()

# delete document with known id
db.collection('people').document('JohnDoe').delete()

# delete document with unknown id
people = db.collection('people').where('age', '==', 25).get()
for person in people:
    key = person.id
    db.collection('people').document(key).delete()