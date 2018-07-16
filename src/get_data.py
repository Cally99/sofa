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


    ids = []
    for t in tournaments:
        events = t.get('events')
        season = t.get('season').get('name')
        # Checks that not womens and not wimbledon
        if 'imbledon' in season or 'Women' in season:
            continue

        for e in events:
            if e.get('statusDescription') == '1. set' and '/' not in e.get('name'):
                id = e.get('id')
                home_score = e.get('homeScore').get('period1')
                away_score = e.get('awayScore').get('period1')
                current_home_score = e.get('homeScore').get('point', 0)
                current_away_score = e.get('awayScore').get('point', 0)
                if [home_score, away_score] in DICT_OF_SCORES:
                    ids.append([id, home_score, away_score, current_home_score, current_away_score])
    
    print(ids)
    
    target_games = []
    for g in ids:
        try:
            with timeout(10):
                new_game = Game(g[0], g[1], g[2], g[3], g[4])
        except Exception as e:
            print('Timeout exception.')
            continue
        game_str = '%s %s\n' % (new_game.get_title(), new_game.get_history())
        if game_str not in watched:
                watched.append(game_str)
        if new_game.is_target_game():
            target_games.append(new_game)
    
    return target_games
