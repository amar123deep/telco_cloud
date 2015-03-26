import simpy

from Resource import Resource

class DatacentreDiscrete(Resource):
	
	# Data centre sizes
	VM_TYPES = {
		"L":{ 
				"CPU":			{'CAPACITY':50.0,"THRESHOLD":0.6},
				"STORAGE":		{'CAPACITY':50.0,"THRESHOLD":0.6},
				"UPLINK_BW":	{'CAPACITY':50.0,"THRESHOLD":0.6}, 
				"DOWNLINK_BW":	{'CAPACITY':50.0,"THRESHOLD":0.6}
			},
		"M":{ 
				"CPU":			{'CAPACITY':50.0,"THRESHOLD":0.6},
				"STORAGE":		{'CAPACITY':50.0,"THRESHOLD":0.6},
				"UPLINK_BW":	{'CAPACITY':50.0,"THRESHOLD":0.6}, 
				"DOWNLINK_BW":	{'CAPACITY':50.0,"THRESHOLD":0.6}
			},
		"S":{ 
				"CPU":			{'CAPACITY':200.0,"THRESHOLD":0.6},
				"STORAGE":		{'CAPACITY':200.0,"THRESHOLD":0.6},
				"UPLINK_BW":	{'CAPACITY':200.0,"THRESHOLD":0.6},
				"DOWNLINK_BW":	{'CAPACITY':200.0,"THRESHOLD":0.6}
			}
		}
		
	RESOURCE_TYPES = {
		"L":{ 
				"VMS":	{'CAPACITY':50.0,"THRESHOLD":0.6},
			},
		"M":{ 
				"VMS":	{'CAPACITY':50.0,"THRESHOLD":0.6},
			},
		"S":{ 
				"VMS":	{'CAPACITY':200.0,"THRESHOLD":0.6},
			}
		}
	
	def __init__(self, resources, name, env, scheduler, monitor, applications):
		Resource.__init__(self, name, env, {}, applications, monitor)

		self.scheduler = scheduler
	
		self.resources = resources
		
		# Append internal resource properties
		for resource in self.resources.itervalues():
			resource.update({'USAGE':0, 'BADNESS':0 , 'APPS':{}})

		self.apps = {}
	
	# Method for scheduler to register application
	def registerApp(self, appName):
		if appName not in self.apps:
			self.apps[appName] = {}
			#print "[%s] Registeirng app %s" % (self.name, appName)
			
	# Method for scheduler to terminate application
	def terminateApp(self, app):
		del self.apps[app]

	# Check if node has app
	def hosts(self, app):
		return app in self.apps
		
	# Method for scheduler to migrate application
	def migrateApp(self, app, destination):
		raise NotImplementedError

	# [Asbstract] Update resource usage
	def computeResourceUsage(self):
		for appName in self.subscribers: # For every app
			for resourceName, resource in self.resources.iteritems(): # Calculate app usage for each resource usage each application's properties
				resource['APPS'][appName] = self.applications[appName].computeResourceUsage(resourceName, self.subscribers[appName]['TOTAL'])

		for resource in self.resources.itervalues(): # Update usage for each resource 
			totalSubsucribers = 0 # Total usage for each resource
			for nbrAppSubscribers in resource['APPS'].itervalues():
				totalSubsucribers += nbrAppSubscribers

			resource['USAGE'] = totalSubsucribers

	# Compute how much resources an application cones and how much it 
	# contributes to the load of the DC
	def computeResourceUsage(self):
		Resource.computeResourceUsage(self)
		self.computeTotalBadness()