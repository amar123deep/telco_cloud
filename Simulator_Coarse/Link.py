import simpy

from Resource import Resource,LinearCostFunc,NoCostFunc,BarrierFunc
from Leaf import Leaf

class Link(Resource):
	RESOURCE_TYPES = {
		"M": {		
				'NET_UP':	{'CAPACITY':40000.0, 'EXECOST': NoCostFunc(), 'OVERLOADCOST': BarrierFunc(1,0.0), 'MU':1},
				'NET_DOWN':	{'CAPACITY':40000.0, 'EXECOST': NoCostFunc(), 'OVERLOADCOST': BarrierFunc(1,0.0), 'MU':1} 
			},
		"S": {	
				'NET_UP':	{'CAPACITY':4000.0, 'EXECOST': NoCostFunc(), 'OVERLOADCOST': BarrierFunc(1,0.0), 'MU':1},
				'NET_DOWN':	{'CAPACITY':4000.0, 'EXECOST': NoCostFunc(), 'OVERLOADCOST': BarrierFunc(1,0.0), 'MU':1} 
			}
		}

	def __init__(self, name, env, resources, length, applications):
		Resource.__init__(self, name, env, resources, applications)

		self.propagation_latency = length/200000000
		self.properties = {}
		self.properties.update({'NET_UP':{'LATENCY':0}, 'NET_DOWN':{'LATENCY':0}})

	# Latency calculation
	def computeLatency(self): # [TO-DO] Implement actual latency function
		for resourceName in self.properties:
			self.properties[resourceName]['LATENCY'] = self.propagation_latency + self.resources[resourceName]['USAGE']/self.resources[resourceName]['CAPACITY']

	# Get link latency
	def getLatency(self, resourceName):
		return self.properties[resourceName]['LATENCY']

	# (Resource) Compute resource usage
	def computeResourceUsage(self):
		Resource.computeResourceUsage(self)
		self.computeLatency()
		return self.computeTotalCost()