import simpy

# [DEPRICATED]
class Monitor(object):

	def __init__(self, env, measrPoints, interval):
		self.env = env
		self.measrPoints = measrPoints #Meas points are functions from other objects that you call to retreive the data.
		self.interval = interval
		
		assert isinstance(self.measrPoints, dict), "%s : measrPoints is not a dict - %s" %(self.getName(), self.measrPoints)
		
		for measrPoint in self.measrPoints.itervalues():
			measrPoint['DATA'] = {}
		
		env.process(self.measure())
		
	# Go through and read all measurement points
	def measure(self):
		while True:
			yield self.env.timeout(self.interval)
			
			for measrPoint in self.measrPoints.itervalues():
				measrPoint['DATA'][self.env.now] = measrPoint['FUNC']()
	
	# Report measurement
	def report(self, identifier, data):
		self.measrPoints[identifier].update({self.env.now:data})

	# Compose results
	def composeResults(self):
		for mpName, mp in self.measrPoints.iteritems():
			mp['OUTPUT'](self, mpName)
	
	# Compose CSV file
	def composeCSV(self, mpName):
		separator = ','
		
		f = open('%s.csv' % mpName,'w')
			
		f.write('Time%s%s \n' % (separator, self.measrPoints[mpName]['HEADER']()))
			
		for time in sorted(self.measrPoints[mpName]['DATA'], key=lambda x: float(x)):
			f.write("%i%s%s \n" % (time, separator, self.measrPoints[mpName]['DATA'][time]))
			
		f.close()