import simpy

from Resource import Resource

class Datacentre(Resource):
	
	# Data centre sizes
	RESOURCE_TYPES = {
		"L":{ 
				"CPU":			{'CAPACITY':50.0,"THRESHOLD":0.5},
				"STORAGE":		{'CAPACITY':50.0,"THRESHOLD":0.5},
				"UPLINK_BW":	{'CAPACITY':50.0,"THRESHOLD":0.5}, 
				"DOWNLINK_BW":	{'CAPACITY':50.0,"THRESHOLD":0.5}
			},
		"M":{ 
				"CPU":			{'CAPACITY':50.0,"THRESHOLD":1.0},
				"STORAGE":		{'CAPACITY':50.0,"THRESHOLD":1.0},
				"UPLINK_BW":	{'CAPACITY':50.0,"THRESHOLD":1.0}, 
				"DOWNLINK_BW":	{'CAPACITY':50.0,"THRESHOLD":1.0}
			},
		"S":{ 
				"CPU":			{'CAPACITY':200.0,"THRESHOLD":0.5},
				"STORAGE":		{'CAPACITY':200.0,"THRESHOLD":0.5},
				"UPLINK_BW":	{'CAPACITY':200.0,"THRESHOLD":0.5},
				"DOWNLINK_BW":	{'CAPACITY':200.0,"THRESHOLD":0.5}
			}
		}
	
	def __init__(self, name, env, resources, applications):
		Resource.__init__(self, name, env, resources, applications)
		self.apps = {}

	# Method for scheduler to register application
	def registerApp(self, appName):
		if appName not in self.apps:
			self.apps[appName] = {}
			#print "[%s] Registeirng app %s" % (self.name, appName)

	# Method for scheduler to terminate application
	def terminateApp(self, appName):
		print appName
		assert appName in self.apps, 'App does not exist in the DC'
		del self.apps[appName]

	def getAllapps(self):
		return self.apps.keys()
		
	# Check if node has app
	def hosts(self, app):
		return app in self.apps
		
	# Method for scheduler to migrate application
	def migrateApp(self, app, destination):
		raise NotImplementedError

	# Compute how much resources an application cones and how much it 
	# contributes to the load of the DC
	def computeResourceUsage(self):
		Resource.computeResourceUsage(self)
		self.computeTotalBadness()