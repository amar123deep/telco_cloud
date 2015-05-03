import math

class LinearAppResrFunc(object):
	def __init__(self, a, b):
		self.a = a
		self.b = b
		
	def computeResourceUsage(self, demand):
		# linear function
		assert isinstance(demand, float) or isinstance(demand, int), "%s : Demand is not a number - %s" % demand
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

# SLO/SLA
class Threshold(object):
	def __init__(self, threshold):
		self.threshold = threshold
		
	def compute(self, value):
		if value >= self.threshold:
			return False
		else:
			return True

class Application(object):
	TYPES = {
		'CPU_INTENSIVE':{	
				'CPU': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 0.28), 'MIGRATION':None },
					'SLO_FUNC': Threshold(float('inf')),
					},
				'NET_UP': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 0.01), 'MIGRATION':None},
					'SLO_FUNC': Threshold(20.0),
					},
				'NET_DOWN': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 0.01), 'MIGRATION':None},
					'SLO_FUNC': Threshold(20.0),
					},
			},
		'NET_INTENSIVE':{
				'CPU': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 0.09), 'MIGRATION':None},
					'SLO_FUNC': Threshold(float('inf')),
					},
				'NET_UP': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 0.39*4/7), 'MIGRATION':None},
					'SLO_FUNC': Threshold(20.0),
					},
				'NET_DOWN': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 0.39*3/7), 'MIGRATION':None},
					'SLO_FUNC': Threshold(20.0),
					},
			},
		'SYMMETRIC':{
				'CPU': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 1.0), 'MIGRATION':None},
					'SLO_FUNC': Threshold(float('inf')),
					},
				'NET_UP': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 1.0), 'MIGRATION':None},
					'SLO_FUNC': Threshold(20.0),
					},
				'NET_DOWN': {
					'RESOURCE_FUNCS':{
						'PRODUCTION':LinearAppResrFunc(0.0, 1.0), 'MIGRATION':None},
					'SLO_FUNC': Threshold(20.0),
					},
			}
		}
	
	def __init__(self, name, resourceFuncs):
		self.name = name
		self.resourceFuncs = resourceFuncs # Dictionary of resource PRODUCTION functiion
	
	# Compute resource usgae for a resource as according to the corresponding resourceFuncs
	def computeResourceUsage(self, resource, demand, demandType):
		return self.resourceFuncs[resource]['RESOURCE_FUNCS'][demandType].computeResourceUsage(demand)
		
	# Evaluate SLO
	def evaluateSLO(self, latency=0, cpu=0, memory=0):
		result = True
		
		result *= self.resourceFuncs['CPU']['SLO_FUNC'].compute(cpu)
		result *= self.resourceFuncs['NET_UP']['SLO_FUNC'].compute(latency)
		result *= self.resourceFuncs['NET_DOWN']['SLO_FUNC'].compute(latency)
		
		return result

	# Get name
	def getName(self):
		return self.name
		