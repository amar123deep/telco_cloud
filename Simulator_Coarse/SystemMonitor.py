import simpy
import logging 

class SystemMonitor(object):
	
	def __init__(self, env, time_delta, topology, coordinator, inputs, outputs, filters):
		self.env = env
		self.topology = topology
		self.coordinator = coordinator
		self.time_delta = time_delta
		self.inputs = inputs
		self.outputs = outputs
		self.filters = filters 
		self.signals = {} # Amardeep! Have a look at this stuff! :)

		self.bigBadness = {}
		
		self.bigUtilization = {}
		
	def measure(self):
		while True:
			systemBadness,dcBadness,linkBadness, dcApp= self.measureSystemBadness()
			self.bigBadness[self.env.now] = (systemBadness, dcBadness, linkBadness,dcApp)
			l1,l2 = self.measureSystemUtilization()
			self.bigUtilization[self.env.now] = (l1,l2)
			yield self.env.timeout(self.time_delta)
	
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
		
		return measureDCUtilization(),measureLinkUtilization()
	
	def measureSystemBadness(self):
		dcBadness = []
		linkBadness = []
		dcApp = []
		
		def listAllapp(): 
			dcList = self.topology.getAllDCs()
			for dc in sorted(dcList): 
				dcApp.append(dc.getAllapps())
				# print dc.getAllapps()
			return dcApp
		def measureDCBadness():
			dcList = self.topology.getAllDCs()
			for dc in sorted(dcList): 
				#print dc.getName()
				dcBadness.append(dc.getBadness())
			return sum(dcBadness) 
		def measureLinkBadness():
			linkList = self.topology.getAllLinks()
			for link in sorted(linkList):
				#print link.getName()
				linkBadness.append(link.getBadness())
			return sum(linkBadness)
		systemBadness = measureDCBadness()+ measureLinkBadness()
		# write to the files
		return systemBadness,dcBadness,linkBadness,listAllapp()

	def composeUtilization(self):
		fileD = open('sysLog2.txt','w')
		for key,(l1,l2) in self.bigUtilization.iteritems():
			fileD.write(str(key) + ':'+str(l1)+':'+str(l2)+'\r')
		fileD.close()
		
	def compose(self):
		fileDescr = open('sysLog1.txt','w')
		for key, (v1,v2,v3,v4) in self.bigBadness.iteritems(): 
			#print str(key), str(v1), str(v2), str(v3)
			fileDescr.write(str(key)+':'+str(v1)+':'+str(v2)+':'+str(v3) +':'+str(v4)+ "\r")
		fileDescr.close()
		