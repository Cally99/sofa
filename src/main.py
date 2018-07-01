import os
import time
from collections import deque
from termcolor import colored

from get_data import get_target_games

if __name__=='__main__':
    sended = deque(maxlen=30)
    while True:
        """
        Finding games with breaks
        """
        try:
            target_games = get_target_games()
        except Exception as e:
            print('Connection aborted.')
            time.sleep(5)
            continue
        if target_games:
            print(f"Finds {len(target_games)} games")
            for g in target_games:
                if g.get_id() not in sended:
                    print(colored('Sending %s' % g, 'green'))
                    os.system('python3 send_to_channel.py "%s"' % g)
                    sended.append(g.get_id())
        else:
            time.sleep(5)
        
            

