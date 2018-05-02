import json
import requests
from Game import Game

url = 'https://www.sofascore.com/tennis/livescore/json'

response = json.loads(requests.get(url).text)

tournaments = response.get('sportItem').get('tournaments')

itf_tournaments = list(
        filter(lambda t: 'ITF' in t.get('category').get('name'), tournaments)
                     )
itf_ids = []
for t in itf_tournaments:
    events = t.get('events')
    for e in events:
        if e.get('statusDescription') == '1. set':
            itf_ids.append(e.get('id'))

print(itf_ids)

games = []
for id in itf_ids:
    new_game = Game(id)
    print(new_game)
    games.append(new_game)

# print(games)
