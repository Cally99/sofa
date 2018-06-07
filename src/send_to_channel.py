import os
import logging
import telebot
import time
import sys

BOT_TOKEN = os.environ.get('TOKEN')
CHANNEL_ID = -1001336404624
bot = telebot.TeleBot(BOT_TOKEN)

def send_msg(msg):
	try:
		bot.send_message(CHANNEL_ID, msg, parse_mode="Markdown") 
	except Exception as ex:
		logging.error('Exception of type {!s} in send_new_fight(): {!s}'.format(type(ex).__name__, str(ex)))
	finally:
		logging.info('Finished sending.')


if __name__ == '__main__':
	logging.basicConfig(format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s', level=logging.INFO,
                        filename='bot_log.log', datefmt='%d.%m.%Y %H:%M:%S')
	msg = sys.argv[1]
	send_msg(msg)
