from telegram.ext import Updater, InlineQueryHandler, CommandHandler
import requests
import re
import os

# ops

# MESSGAGE_FORMATS
ADD_STATION = u'add s (?P<param1>.*)'
RM_STATION = u'rm s (?P<param1>.*)'
ADD_GROUP = u'add g (?P<param1>.*)'
RM_GROUP = u'rm g (?P<param1>.*)'
BUSY_STATION = u'(?P<param1>.*) in (?P<param2>.*)'
FREE_STATION = u'(?P<param1>.*) free'
GROUP_GO_TO = u'(?P<param1>.*) go (?P<param2>.*)'


CURRENT_STATE = u"Free:\n{free}\nBusy:\n{busy}\n"
STATION_STATE = u"{name}: group:{group} waits:{waits}"

class Station(object):
    def __init__(self, name):
        self.name = name
        self.waits = []
        self.group = None

    def __repr__(self):
        return STATION_STATE.format(name=self.name, group=self.group, waits=', '.join(self.waits))

    def is_free(self):
        return (self.group == None) and (not len(self.waits))

stations = {}
groups = []

def add_station(station=None):
	assert station, "Missing station name"
	stations[station] = Station(station)

def rm_station(station=None):
	assert station, "Missing station name"
	stations.pop(station)

def add_group(group=None):
	assert group, "Missing group id"
	groups.append(group)

def rm_group(group=None):
	assert group, "Missing group id"
	groups.remove(group)

def busy_station(station=None, group=None):
	assert group, "Missing group id"
	assert station, "Missing station name"
	assert station in stations, "Wrong station name"
	assert groups.count(group) == 1, "Wrong group id"
	stations[station].group = group

def free_station(station=None):
	assert station, "Missing station name"
	assert station in stations, "Wrong station name"
	stations[station].group = None

def go_to_station(group=None, station=None):
	assert group, "Missing group id"
	assert station, "Missing station name"
	assert station in stations, "Wrong station name"
	assert groups.count(group) == 1, "Wrong group id"
	old_station = [stations[s] for s in stations if stations[s].group == group]
	if any(old_station):
		for s in old_station:
			s.group=None
	stations[station].waits.append(group)
# ops end

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

# Commands Wrappers
def start(update, context):    
  chat_id = update.message.chat.id
  context.bot.send_message(chat_id=chat_id, text=START_MESSAGE)
  context.bot.send_message(chat_id=chat_id, text="bla")
  update.message.reply_text("bla")


def add(update, context):
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

# Menu?
def main():    
  updater = Updater(TOKEN, use_context=True)    
  dp = updater.dispatcher  
  
  dp.add_handler(CommandHandler("start", start))
  #dp.add_handler(CommandHandler("add", add, pass_args=True))
  #dp.add_handler(CommandHandler("rm", rm, pass_args=True))   
  #dp.add_handler(CommandHandler("busy", busy, pass_args=True))   
  #dp.add_handler(CommandHandler("free", free, pass_args=True))   
  #dp.add_handler(CommandHandler("goto", goto, pass_args=True))
  dp.add_handler(CommandHandler("st", state))      
     
  updater.start_webhook(listen="0.0.0.0",        
                        port=int(PORT),                       
                        url_path=TOKEN) 
  updater.bot.setWebhook('https://activity-evening.herokuapp.com/' + TOKEN) 
  updater.idle()


if __name__ == '__main__':
	main()