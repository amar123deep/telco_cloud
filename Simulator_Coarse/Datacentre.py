import simpy

from Resource import Resource

class Datacentre(Resource):
	
	# Data centre sizes
	RESOURCE_TYPES = {
		"L":{ 
				"CPU":		{'CAPACITY':2000.0},
				"NET_UP":	{'CAPACITY':2000.0},
				"NET_DOWN":	{'CAPACITY':2000.0}
			},
		"M":{ 
				"CPU":		{'CAPACITY':200.0},
				"NET_UP":	{'CAPACITY':200.0},
				"NET_DOWN":	{'CAPACITY':200.0}
			},
		"S":{ 
				"CPU":		{'CAPACITY':20.0},
				"NET_UP":	{'CAPACITY':20.0},
				"NET_DOWN":	{'CAPACITY':20.0}
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

	# Compute how much resources an application cones and how much it 
	# contributes to the load of the DC
	def computeResourceUsage(self):
		Resource.computeResourceUsage(self)
		return self.computeTotalOverload()