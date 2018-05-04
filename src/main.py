import os
from collections import deque
from termcolor import colored

from get_data import get_target_games

if __name__=='__main__':
    sended = deque(maxlen=20)
    while True:
        target_games = get_target_games()
        for g in target_games:
            if g not in sended:
                print(colored('Sending %s' % g, 'green'))
                os.system('python3 send_to_channel.py %s' % g)
                sended.append(g.get_id())
            

