from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import os
from contextlib import contextmanager
from operations import *

PORT = int(os.environ.get('PORT', 5000))
TOKEN = os.environ["TOKEN"]

START_MESSAGE = u"Welcome to Stations Manager bot.\n \
It will show which station is free and which is busy.\n \
In order to do so it will need your help in updating him on your station state changes :)\n \
The syntax is:\n \
To print the menu: \n\
/start \n\
To print the current stations state \n\
/st \n\
Adding|Removing groups|stations:\n \
/add s <station-name>\n \
/rm s <station-name>\n \
\n \
/add g <group-number>\n \
/rm g <group-number\n \
\n \
To announce a busy station:\n \
/busy <station-name> <group-number> \n \
\n \
To announce where you sent the group:\n \
/goto <group-number> <station-name> \n \
\n \
To announce a free station:\n\
/free <station-name>\n \
To add time to a group total mission's time:\n \
/time <group-number> <time>\n"


# Commands Wrappers
def start(update, context):
	chat_id = update.message.chat_id
	try:
		update.message.reply_text(START_MESSAGE)
	except AssertionError as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))
	except Exception as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))


def add(update, context):
	chat_id = update.message.chat_id
	try:
		add_type = context.args[0]
		if add_type == 's':
			add_station(context.args[1])
		elif add_type == 'g':
			add_group(context.args[1])
		else:
			assert False, "You have a typo, impossible addition type"
	except AssertionError as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))
	except Exception as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))



def rm(update, context):
	chat_id = update.message.chat_id
	try:
		rm_type = context.args[0]
		if rm_type == 's':
			rm_station(context.args[1])
		elif rm_type == 'g':
			rm_group(context.args[1])
		else:
			assert "You have a typo, impossible addition type"
	except AssertionError as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))
	except Exception as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))


def busy(update, context):
	chat_id = update.message.chat_id
	try:
		busy_station(context.args[0], context.args[1])
	except AssertionError as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))
	except Exception as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))


def free(update, context):
	chat_id = update.message.chat_id
	try:
		free_station(context.args[0])
	except AssertionError as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))
	except Exception as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))


def goto(update, context):
	chat_id = update.message.chat_id
	try:
		go_to_station(context.args[0], context.args[1])
	except AssertionError as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))
	except Exception as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))


def state(update, context):
	chat_id = update.message.chat_id
	try:
		update.message.reply_text(CURRENT_STATE.format(free="  "+ "\n  ".join(
			[str(station) for station in filter(lambda s: stations[s].is_free(), stations)]),
			busy="\n".join(
				[str(stations[station]) for station in filter(lambda s: not stations[s].is_free(), stations)])))
	except AssertionError as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))
	except Exception as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))


def time(update, context):
	chat_id = update.message.chat_id
	try:
		add_time(context.args[0], context.args[1])
	except AssertionError as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))
	except Exception as e:
		context.bot.send_message(chat_id=chat_id, text=str(e))


def clr():
	stations = {}
	groups = {}


def main():    
	updater = Updater(TOKEN, use_context=True)    
	dp = updater.dispatcher  
  
	dp.add_handler(CommandHandler("start", start, pass_args=True))
	dp.add_handler(CommandHandler("add", add, pass_args=True))
	dp.add_handler(CommandHandler("rm", rm, pass_args=True))   
	dp.add_handler(CommandHandler("busy", busy, pass_args=True))   
	dp.add_handler(CommandHandler("free", free, pass_args=True))   
	dp.add_handler(CommandHandler("goto", goto, pass_args=True))
	dp.add_handler(CommandHandler("st", state, pass_args=True))
	dp.add_handler(CommandHandler("time", time, pass_args=True))
	dp.add_handler(CommandHandler("clr", clr, pass_args=True))      
     
	updater.start_webhook(listen="0.0.0.0",        
							port=int(PORT),                       
							url_path=TOKEN) 
	updater.bot.setWebhook('https://activity-evening.herokuapp.com/' + TOKEN) 

	updater.idle()



if __name__ == '__main__':
	main()