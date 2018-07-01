import json
import requests
from timeoutcontext import timeout

from Game import Game


watched = []

DICT_OF_SCORES = [
                   [1, 0], [0, 1],
                   [2, 0], [0, 2],
                   [2, 1], [1, 2],
                   [3, 1], [1, 3]
                 ]

def get_target_games():
    url = 'https://www.sofascore.com/tennis/livescore/json'
    response = json.loads(requests.get(url, timeout=10).text)
    try:
        tournaments = response.get('sportItem').get('tournaments')
    except Exception as e:
        print('No live games')
        return []

    itf_tournaments = list(filter(lambda t: 'ITF' in t.get('category').get('name'), tournaments))

    itf_ids = []
    for t in itf_tournaments:
        events = t.get('events')
        for e in events:
            if e.get('statusDescription') == '1. set' and '/' not in e.get('name'):
                id = e.get('id')
                home_score = e.get('homeScore').get('period1')
                away_score = e.get('awayScore').get('period1')
                if [home_score, away_score] in DICT_OF_SCORES:
                    itf_ids.append([id, home_score, away_score])
    
    print(itf_ids)
    
    target_games = []
    for g in itf_ids:
        print("I'm in.")
        
        try:
            with timeout(10):
                new_game = Game(g[0], g[1], g[2])
        except Exception as e:
            print('Timeout exception.')
            continue
        print("I'm here.")
        game_str = '%s %s\n' % (new_game.get_title(), new_game.get_history())
        if game_str not in watched:
                watched.append(game_str)
        if new_game.is_target_game():
            target_games.append(new_game)
    
    return target_games
