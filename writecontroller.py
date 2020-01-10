from importlib import reload
def giveList(index):
	import appender
	myLists = []
	appender = reload(appender)
	myLists = appender.addData()
	print("MY SIZEEE", myLists[index])
	return myLists[index]