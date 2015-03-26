import simpy

from Resource import Resource
from Datacentre import Datacentre
from Leaf import Leaf

class Link(Resource):
	RESOURCE_TYPES = {
		"100Mbit": {	
						'UPLINK_BW':	{'CAPACITY':100.0, "THRESHOLD":0.5}, 
						'DOWNLINK_BW':	{'CAPACITY':100.0, "THRESHOLD":0.5}
					},
		"1Gbit": {		
						'UPLINK_BW':	{'CAPACITY':1000.0, "THRESHOLD":0.5}, 
						'DOWNLINK_BW':	{'CAPACITY':1000.0, "THRESHOLD":0.5}
					},
			}

	def __init__(self, name, env, resources, length, applications):
		Resource.__init__(self, name, env, resources, applications)

		self.propagation_latency = length/200000000
		self.properties = {}
		self.properties.update({'UPLINK':{'LATENCY':0},'DOWNLINK':{'LATENCY':0}})

	# Latency calculation
	def computeLatency(self): # [TO-DO] Implement actual latency function
		for resourceName in self.properties:
			self.properties[resourceName]['LATENCY'] = self.propagation_latency + self.resources[resourceName+'_BW']['USAGE']/self.resources[resourceName+'_BW']['CAPACITY']

	# Get link latency
	def getLatency(self, direction):
		return self.latency[direction]
	
	# (Resource) Compute resource usage
	def computeResourceUsage(self):
		Resource.computeResourceUsage(self)
		self.computeLatency()
		self.computeTotalBadness()