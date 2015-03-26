import simpy

from Resource import Resource

class Leaf(Resource):

	def __init__(self, name, env):
		Resource.__init__(self, name, env, {}, {})
		
		self.paths = {}

	# Check if node hosts app
	def hosts(self, app):
		return False
	
	# Get the stored to a specific application
	def getPath(self, appName):
		return self.paths[appName]
		
	# Set path to a specific application
	def setPath(self, appName, path):
		self.paths[appName] = path

	# Update subscribe per leaf per app 
	def updateSubscriber(self, appName, leafName, nbrUsers):
		self.subscribers[appName] = nbrUsers

	# Override - Update resource usage
	def computeResourceUsage(self):
		pass

	def computeLatency(self, appName):
		path = self.findMinPath()
		
		dlLatency = 0
		ulLatency = 0
		
		for element in path:
			dlLatency += element.getLatency()
			ulLatency += element.getLatency()

	# Get total population
	def getTotalPopulation(self):
		result = 0
		for appSubscribers in self.subscribers.itervalues():
			result += appSubscribers['TOTAL']
		
		return result
		
	# Get population for an app
	def getAppPopulation(self, appName):
		return self.subscribers[appName]