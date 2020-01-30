from importlib import reload
def giveList(index):
	import appender
	myLists = []
	appender = reload(appender)
	myLists = appender.addData()
	return myLists[index]