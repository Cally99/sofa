import json
import requests

TARGET_SEQUENCES = [
                    # 1-0, 0-1
                    [['1-0', 1, 1]],
                    [['0-1', 1, 2]],
                    # 2-0, 0-2
                    [['1-0', 0, 1], ['2-0', 1, 1]],
                    [['0-1', 0, 2], ['0-2', 1, 2]],
                    # 2-1, 1-2
                    [['0-1', 0, 1], ['1-1', 0, 1], ['2-1', 1, 1]],
                    [['1-0', 0, 2], ['1-1', 0, 2], ['1-2', 1, 2]],
                    # 3-1, 1-3
                    [['1-0', 0, 1], ['1-1', 0, 1], ['2-1', 0, 1], ['3-1', 1, 1]],
                    [['0-1', 0, 2], ['1-1', 0, 2], ['1-2', 0, 2], ['1-3', 1, 2]],
                    ]

class Game:
    def __init__(self, id, first_score, second_score, current_first_score, current_away_score):
        self._id = id
        self._first_score = first_score
        self._second_score = second_score
        url = 'https://www.sofascore.com/event/%s/json' % self._id
        self._info = json.loads(requests.get(url, timeout=10).text)
        self._first_score = self._info.get('event').get('homeScore').get('period1')
        self._second_score = self._info.get('event').get('awayScore').get('period1')
        self._first_point = current_first_score
        self._second_point = current_away_score
        self._title = self._info.get('event').get('name')
        self._tournament = self._info.get('event').get('tournament').get('name')
        self._history = []
        self._fav = 1 if self._info.get('vote').get('vote1') > self._info.get('vote').get('vote2') else 2
        try:
            point_by_point = self._info.get('pointByPoint')[0]
        except Exception as e:
            print('Exception: %s %s-%s\n' % (self._title, self._first_score, self._second_score))
        else:
            self._hist_points = list(filter(None.__ne__, [g.get('score') for g in point_by_point.get('games')][::-1]))
            # print(self._hist_points)
            for p in self._hist_points:
                is_break = p.get('serving') != p.get('scoring')
                self._history.append(['%s-%s' % (p.get('homeScore'), p.get('awayScore')),
                                     int(is_break), self._fav])
            print(self._tournament)
            print(self._title)
            print('History: %s ' % self._history)
            print(self.is_target_game()) 
            print()
    


    def __repr__(self):
        return '*%s\n%s*\nСчёт: %s-%s\nФаворит: %s\n%s-%s' % (self._tournament, self._title, self._first_score, self._second_score, self._fav, self._first_point, self._second_point)

    def __str__(self):
        return '*%s\n%s*\nСчёт: %s-%s\nФаворит: %s\n%s-%s' % (self._tournament, self._title, self._first_score, self._second_score, self._fav, self._first_point, self._second_point)

    def get_id(self):
        return self._id

    def get_history(self):
        return self._history

    def get_title(self):
        return self._title

    def is_target_game(self):
        return self._history in TARGET_SEQUENCES

