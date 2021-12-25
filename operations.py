CURRENT_STATE = u"Free Stations:\n{free}\nBusy Stations:\n{busy}\n"
STATION_STATE = u"  {name}:\n    current group:{group}\n    waiting groups: {waits}"

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
groups = {}

def add_station(station=None):
	assert station, "Missing station name"
	stations[station] = Station(station)

def rm_station(station=None):
	assert station, "Missing station name"
	stations.pop(station)

def add_group(group=None):
	assert group, "Missing group id"
	groups[group] = 0

def rm_group(group=None):
	assert group, "Missing group id"
	groups.pop(group)

def busy_station(station=None, group=None):
	assert group, "Missing group id"
	assert station, "Missing station name"
	assert station in stations, "Station doesn't exist"
	assert group in groups, "Group doesn't exist"
	if group in stations[station].waits:
		stations[station].waits.remove(group)
	stations[station].group = group

def free_station(station=None):
	assert station, "Missing station name"
	assert station in stations, "Station doesn't exist"
	stations[station].group = None

def go_to_station(group=None, station=None):
	assert group, "Missing group id"
	assert station, "Missing station name"
	assert station in stations, "Station doesn't exist"
	assert group in groups, "Group doesn't exist"
	old_station = [stations[s] for s in stations if stations[s].group == group]
	if any(old_station):
		for s in old_station:
			s.group=None
	stations[station].waits.append(group)

def add_time(group=None, time=0):
	time_f = float(time)
	assert group, "Missing group id"
	assert 0 < time_f, "Time is zero or less"
	assert group in groups, "Group doesn't exist"
	groups[group] += time