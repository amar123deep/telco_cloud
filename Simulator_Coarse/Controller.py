import simpy

class Controller(object):
	
	def __init__(self, env, coordinator):
		self.env = env
		self.coordinator = coordinator
		
		self.env.process(self.revaluate())
		
	def revaluate(self):
		raise NotImplementedError
		
class PeriodicController(Controller):
	
	def __init__(self, env, coordinator, period, offset):
		self.period = period
		self.offset = offset
		Controller.__init__(self, env, coordinator)
	
	def revaluate(self):
		yield self.env.timeout(self.offset)
		while True:
			yield self.env.timeout(self.period)
			print "%i - Revaluating all apps" % self.env.now
			self.coordinator.revaluateAll()