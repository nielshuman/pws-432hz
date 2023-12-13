import firebase_admin
from firebase_admin import credentials, firestore
from collections import Counter
from copy import deepcopy
import json

cred = credentials.Certificate("key.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

out = {}

votes_ref = db.collection("votes")
votes_stream = votes_ref.stream()
votes = []
cats = {
    '440-432': [],
    '440-448': [],
}

genres = {
    'Jazz': deepcopy(cats),
    'Classical': deepcopy(cats),
}

for vote in votes_stream:
    v = vote.to_dict()
    votes.append(v)
    cats[v['cat']].append(v['vote'])
    genres[v['cat2']][v['cat']].append(v['vote'])

print(f'Total votes: {len(votes)}')
print(f'Votes in 440-432: {len(cats["440-432"])}')
print(f'Votes in 440-448: {len(cats["440-448"])}')
print(f'Votes in Jazz: {len(genres["Jazz"]["440-432"]) + len(genres["Jazz"]["440-448"])}')
print(f'Votes in Classical: {len(genres["Classical"]["440-432"]) + len(genres["Classical"]["440-448"])}')

# print(genres)
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
        'low': out[f'{genre} (440-432)'].get('432', 0) + out[f'{genre} (440-448)'].get('440', 0),
        'high': out[f'{genre} (440-432)'].get('440', 0) + out[f'{genre} (440-448)'].get('448', 0),
        'x': out[f'{genre} (440-432)'].get('x', 0) + out[f'{genre} (440-448)'].get('x', 0)
    }
# export out as json
with open('data.json', 'w') as outfile:
    json.dump(out, outfile) 