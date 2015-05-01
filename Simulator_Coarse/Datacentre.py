import simpy

from Resource import Resource,LinearCostFunc,NoCostFunc,BarrierFunc

class Datacentre(Resource):
	
	# Data centre sizes
	RESOURCE_TYPES = {
		"L":{ 
				"CPU":		{'CAPACITY':350.0, 'EXECOST': LinearCostFunc(1,0.0),'OVERLOADCOST': BarrierFunc(1,0),'MU':1},
				"NET_UP":	{'CAPACITY':350.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': BarrierFunc(1,0),'MU':1},
				"NET_DOWN":	{'CAPACITY':350.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': BarrierFunc(1,0),'MU':1}
			},
		"M":{ 
				"CPU":		{'CAPACITY':35.0, 'EXECOST': LinearCostFunc(2,0.0),'OVERLOADCOST': BarrierFunc(1,0),'MU':1},
				"NET_UP":	{'CAPACITY':35.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST':BarrierFunc(1,0),'MU':1},
				"NET_DOWN":	{'CAPACITY':35.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': BarrierFunc(),'MU':1}
			},
		"S":{ 
				"CPU":		{'CAPACITY':5.0, 'EXECOST': LinearCostFunc(4,0.0),'OVERLOADCOST': BarrierFunc(1,0),'MU':1},
				"NET_UP":	{'CAPACITY':5.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': BarrierFunc(),'MU':1},
				"NET_DOWN":	{'CAPACITY':5.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': BarrierFunc(),'MU':1}
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
		return self.computeTotalCost()