import firebase_admin
from firebase_admin import credentials, firestore
from collections import Counter

cred = credentials.Certificate("key.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

users_ref = db.collection("pilot")
docs = users_ref.stream()
cats = {
    '440-432': [],
    '440-448': []
}

for doc in docs:
    v = doc.to_dict()
    cats[v['cat']].append(v['vote'])

count_440_432 = Counter(cats['440-432'])
count_440_448 = Counter(cats['440-448'])

print(count_440_432)
print(count_440_448)
