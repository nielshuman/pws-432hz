import firebase_admin
from firebase_admin import credentials, firestore
from collections import Counter
import json

cred = credentials.Certificate("key.json")
app = firebase_admin.initialize_app(cred)

db = firestore.client()

out = {}

votes_ref = db.collection("votes")
votes = votes_ref.stream()
cats = {
    '440-432': [],
    '440-448': [],
}

genres = {
    'Jazz': cats.copy(),
    'Classical': cats.copy(),
}

for vote in votes:
    v = vote.to_dict()
    cats[v['cat']].append(v['vote'])
    genres[v['cat2']][v['cat']].append(v['vote'])

count_440_432 = Counter(cats['440-432'])
count_440_448 = Counter(cats['440-448'])

out['440-432'] = dict(count_440_432)
out['440-448'] = dict(count_440_448)

out['low-high'] = {
    'low': count_440_432['432'] + count_440_448['440'],
    'high': count_440_432['440'] + count_440_448['448'],
    'x': count_440_432['x'] + count_440_448['x']
}
for genre in genres:
    for cat in genres[genre]:
        out[f'{genre} ({cat})'] = dict(Counter(genres[genre][cat]))
    out[f'{genre} (low-high)'] = {
        'low': out[f'{genre} (440-432)']['432'] + out[f'{genre} (440-448)']['440'],
        'high': out[f'{genre} (440-432)']['440'] + out[f'{genre} (440-448)']['448'],
        'x': out[f'{genre} (440-432)']['x'] + out[f'{genre} (440-448)']['x']
    }

# export out as json
with open('data.json', 'w') as outfile:
    json.dump(out, outfile) 