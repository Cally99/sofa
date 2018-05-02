import json
import requests


class Game:
    def __init__(self, id):
        self._id = id
        url = 'https://www.sofascore.com/event/%s/json' % self._id
        self._info = json.loads(requests.get(url).text)
        self._title = self._info.get('event').get('name')
        self._odds = []
        # self._odds = self._info.get('winningOdds')
        self._breaks = []
        # self._breaks = self._info.get('statistics').get('awayBreakPointsScored')
        self._hist_points = self._info.get('pointByPoint')


    def __repr__(self):
        return '%s\n%s\n%s\n' % (self._title, self._odds, self._breaks)

    def __str__(self):
        return '%s\n%s\n%s' % (self._title, self._odds, self._breaks)
    
    def is_target_game(self):
        url = 'https://www.sofascore.com/event/%s/json' % self._id
        info = json.loads(requests.get(url).text)
        self._title = info.get('event').get('name')
        self._odds = info.get('winningOdds')
        self._breaks = info.get('statistics').get('awayBreakPointsScored')



