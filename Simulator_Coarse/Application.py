import math

class LinearAppResrFunc(object):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		
	def computeResourceUsage(self, nbrUsers):
		# linear function
		return self.a+self.b*nbrUsers

class ExpAppResrFunc(object):
	def __init__(self, a):
		self.a = a
		
	def computeResourceUsage(self, nbrUsers):
		# linear function
		return self.a+math.exp(nbrUsers)

class Application(object):
	
	TYPES = {
		'CPU_INTENSIVE':{	
				'CPU':LinearAppResrFunc(0.0, 0.28),
				'NET':LinearAppResrFunc(0.0, 0.01),
			},
		'NET_INTENSIVE':{	
				'CPU':LinearAppResrFunc(0.0, 0.09),
				'NET':LinearAppResrFunc(0.0, 0.39),
			},
		'NORMAL':{	
				'CPU':LinearAppResrFunc(1.0, 1.0),
				'NET':LinearAppResrFunc(1.0, 1.0),
			}
		}
	
	def __init__(self, name, resourceFuncs):
		self.name = name
		self.resourceFuncs = resourceFuncs # Dictionary of resource usage functiion
	
	# Compute resource usgae for a resource as according to the corresponding resourceFuncs
	def computeResourceUsage(self, resource, nbrUsers):
		return self.resourceFuncs[resource].computeResourceUsage(nbrUsers)
	
	# Compute migration resource usage for each resource
	def computeMigrationResourceUsage(self):
		raise NotImplementedError
	
	# Get name
	def getName(self):
		return self.name
		