import math

class LinearAppResrFunc(object):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		
	def computeResourceUsage(self, demand):
		# linear function
		return self.a+self.b*demand

class ExpAppResrFunc(object):
	def __init__(self, a):
		self.a = a
		
	def computeResourceUsage(self, demand):
		# exponential function
		return self.a+math.exp(demand)
		
class LinearAppMigFuncLimited(object):
	def __init__(self, a):
		self.a = a
		
	def computeMigrationUsage(self, demand, maxAvailable):
		# linear function
		return self.a+math.exp(demand)

# Classes used to calculate migration incurred resource PRODUCTION
class MigrationScheme(object):
	def __init__(self, resources):
		self.resources = resources
		
	def computeMigrationUsage(self, demand, maxAvailable):
		# linear function
		return self.a + math.exp(demand)
		
class Constraint_MigrationScheme(MigrationScheme):
	def __init__(self, resources):
		MigrationScheme.__init__(self, resources)
		
	def computeMigrationUsage(self, maxAvailable):
		# linear function
		return self.a + math.exp(demand)

class Application(object):
	TYPES = {
		'CPU_INTENSIVE':{	
				'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.28), 'MIGRATION':None},
				'NET_UP': {'PRODUCTION':LinearAppResrFunc(0.0, 0.01), 'MIGRATION':None},
				'NET_DOWN': {'PRODUCTION':LinearAppResrFunc(0.0, 0.01), 'MIGRATION':None}
			},
		'NET_INTENSIVE':{
				'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.09), 'MIGRATION':None},
				'NET_UP': {'PRODUCTION':LinearAppResrFunc(0.0, 0.39*4/7), 'MIGRATION':None},
				'NET_DOWN': {'PRODUCTION':LinearAppResrFunc(0.0, 0.39*3/7), 'MIGRATION':None}
			},
		'SYMMETRIC':{
				'CPU': {'PRODUCTION':LinearAppResrFunc(1.0, 1.0), 'MIGRATION':None},
				'NET_UP': {'PRODUCTION':LinearAppResrFunc(0.0, 1.0), 'MIGRATION':None},
				'NET_DOWN': {'PRODUCTION':LinearAppResrFunc(0.0, 1.0), 'MIGRATION':None}
			}
		}
	
	def __init__(self, name, resourceFuncs):
		self.name = name
		self.resourceFuncs = resourceFuncs # Dictionary of resource PRODUCTION functiion
	
	# Compute resource usgae for a resource as according to the corresponding resourceFuncs
	def computeResourceUsage(self, resource, demand, demandType):
		return self.resourceFuncs[resource][demandType].computeResourceUsage(demand)
	
	# [DEPRECATED] Compute migration resource PRODUCTION for each resource
	def computeMigrationResourcePRODUCTION(self, demand):
		return self.resourceFuncs[resource]['MIGRATION'].computeResourceUsage(demand)
	
	# Get name
	def getName(self):
		return self.name
		