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
/free <station-name>"

@contextmanager
def respond_error(update):
	try:
		yield
	except AssertionError as e:
		update.message.reply_text(e.__repr__())
	finally:
		pass

# Commands Wrappers
def start(update, context):
	update.message.reply_text(START_MESSAGE)

def add(update, context):
	with respond_error(update):
		add_type = context.args[0]
		if add_type == 's':
			add_station(context.args[1])
		elif add_type == 'g':
			add_group(context.args[1])
		else:
			assert "You have a typo, impossible addition type"



def rm(update, context):
	rm_type = context.args[0]
	if rm_type == 's':
		rm_station(context.args[1])
	elif rm_type == 'g':
		rm_group(context.args[1])
	else:
		assert "You have a typo, impossible addition type"


def busy(update, context):
	busy_station(context.args[0], context.args[1])


def free(update, context):
	free_station(context.args[0])


def goto(update, context):
	go_to_station(context.args[0], context.args[1])


def state(update, context):
	chat_id = update.message.reply_text(CURRENT_STATE.format(free="\n".join(
		[station.__repr__() for station in filter(lambda s: stations[s].is_free(), stations)]),
        busy="\n".join(
        	[stations[station].__repr__() for station in filter(lambda s: not stations[s].is_free(), stations)])))


def time(update, context):
	add_time(context.args[0], context.args[1])


def main():    
  	updater = Updater(TOKEN, use_context=True)    
  	dp = updater.dispatcher  
  
  	dp.add_handler(CommandHandler("start", start))
  	dp.add_handler(CommandHandler("add", add, pass_args=True))
  	dp.add_handler(CommandHandler("rm", rm, pass_args=True))   
  	dp.add_handler(CommandHandler("busy", busy, pass_args=True))   
  	dp.add_handler(CommandHandler("free", free, pass_args=True))   
  	dp.add_handler(CommandHandler("goto", goto, pass_args=True))
  	dp.add_handler(CommandHandler("st", state))
  	dp.add_handler(CommandHandler("time", time, pass_args=True))      
     
  	updater.start_webhook(listen="0.0.0.0",        
                        	port=int(PORT),                       
                        	url_path=TOKEN) 
  	updater.bot.setWebhook('https://activity-evening.herokuapp.com/' + TOKEN) 

	updater.idle()



if __name__ == '__main__':
	main()