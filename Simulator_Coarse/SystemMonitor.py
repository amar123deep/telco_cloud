import simpy
import logging
import time 
import os

class SystemMonitor(object):
	
	def __init__(self, env, time_delta, outputFolder, topology, coordinator, scheduler, inputs, outputs, filters):
		self.env = env
		self.topology = topology
		self.coordinator = coordinator
		self.time_delta = time_delta
		self.inputs = inputs
		self.outputs = outputs
		self.filters = filters 
		self.scheduler = scheduler
		self.outputFolder = outputFolder

		self.signals = {}

		self.dateAndTime = time.strftime("%d-%m-%Y_%H:%M:%S")
		self.separator = ","

		for (signalName, measPointFunc) in self.inputs:
			self.signals[signalName] = []

		for (inputSignalName, outputSignalName, filterFunc) in self.filters:
			self.signals[outputSignalName] = []

		# [DEPRICATED]
		self.bigBadness = {}
		self.bigUtilization = {}

	def measure(self):
		while True:
			#systemBadness,dcBadness,linkBadness, dcApp = self.measureSystemBadness()
			#self.bigBadness[self.env.now] = (systemBadness, dcBadness, linkBadness,dcApp)
			#l1,l2 = self.measureSystemUtilization()
			#self.bigUtilization[self.env.now] = (l1,l2)

			yield self.env.timeout(self.time_delta)

			for (signalName, measPointFunc) in self.inputs:
				self.signals[signalName].append((self.env.now, measPointFunc(self)))

			for (inputSignalName, outputSignalName, filterFunc) in self.filters:
				self.signals[outputSignalName].append((self.env.now, filterFunc(self.signals[inputSignalName][-1])))

	'''
	Measurements
	'''
	def measureComponentResourceUtilisation(self): 
		componentResourceUtilization = ''
		
		entities = self.topology.getAllDCs() + self.topology.getAllLinks()
		
		for entity in entities:
			for resourceName, resourceUtilisation in entity.getResourceUtilization().iteritems():
				componentResourceUtilization += "%s%s%f%s" % (resourceName, self.separator, resourceUtilisation, self.separator)

		return componentResourceUtilization

	def measureSystemUtilization(self): 
		dcUtilization = []
		linkUtilization = []
		def measureDCUtilization(): 
			dcList = self.topology.getAllDCs()
			for dc in sorted(dcList): 
				dcUtilization.append(dc.computeAppUtilization())
			return dcUtilization

		def measureLinkUtilization(): 
			linkList = self.topology.getAllLinks()
			for link in sorted(linkList): 
				linkUtilization.append(link.computeAppUtilization())
			return linkUtilization

		return measureDCUtilization(), measureLinkUtilization()
	
	def measureComponentOverloadFactor(self): 
		componentOverloadFactor = ''

		for entity in (self.topology.getAllDCs() + self.topology.getAllLinks()):
			componentOverloadFactor += "%f%s" % (entity.getCurrentCost(), self.separator)

		return componentOverloadFactor

	def measureSystemOverloaFactor(self):
		result = 0

		for entity in (self.topology.getAllLinks() + self.topology.getAllDCs()):
			result += entity.getCurrentCost()

		return result
	
	# [DEPRICATED]
	def measureSystemBadness(self):
		dcBadness = []
		linkBadness = []
		dcApp = []
		
		def listAllapp(): 
			dcList = self.topology.getAllDCs()
			for dc in sorted(dcList): 
				dcApp.append(dc.getAllapps())
			return dcApp
		def measureDCBadness():
			dcList = self.topology.getAllDCs()
			for dc in sorted(dcList): 
				dcBadness.append(dc.getBadness())
			return sum(dcBadness) 
		def measureLinkBadness():
			linkList = self.topology.getAllLinks()
			for link in sorted(linkList):
				linkBadness.append(link.getBadness())
			return sum(linkBadness)
		systemBadness = measureDCBadness()+ measureLinkBadness()
		# write to the files
		return systemBadness,dcBadness,linkBadness,listAllapp()

	'''
	Headers
	'''
	def composeDCLinkHeader(self):
		dcLinkHeader = "TIME%s" % self.separator
		
		for entitiy in (self.topology.getAllDCs() + self.topology.getAllLinks()):
			dcLinkHeader += "%s%s" % (entitiy.getName(), self.separator)
			
		dcLinkHeader+="\r"
		return dcLinkHeader

	def composePlacementsHeader(self):
		return "TIME, App, DC, Cost, Exe time\r"

	'''
	DEPRECATED
	'''
	def composeUtilization(self):
		fileD = open('sysLog2.txt','w')
		for key,(l1,l2) in self.bigUtilization.iteritems():
			fileD.write(str(key) + ':'+str(l1)+':'+str(l2)+'\r')
		fileD.close()
	
	'''
	Output
	'''
	def compose(self):
		fileDescr = open('sysLog1.txt','w')
		for key, (v1,v2,v3,v4) in self.bigBadness.iteritems(): 
			#print str(key), str(v1), str(v2), str(v3)
			fileDescr.write(str(key)+':'+str(v1)+':'+str(v2)+':'+str(v3) +':'+str(v4)+ "\r")
		fileDescr.close()

	def fileCSVOutput(self, signalName, headerMethod):
		assert signalName in self.signals , "%s is not a recorded signal" % signalName
		
		directory = "results"
		
		if not os.path.exists(directory):
			os.mkdir(directory)
		
		directory += "/%s" % self.outputFolder
		
		if not os.path.exists(directory):
			os.mkdir(directory)
			
		fileCSV = open('%s/%s%s'%(directory, signalName,'.csv'),'w')

		if headerMethod is not None:
			fileCSV.write(headerMethod(self))
		
		for (timeStamp, data) in self.signals[signalName]:
			fileCSV.write("%i%s%s\r" % (timeStamp, self.separator, data) )
		
		fileCSV.close()

	def produceOutput(self):
		for (signalName, outputMethod, headerMethod) in self.outputs:
			outputMethod(self, signalName, headerMethod)