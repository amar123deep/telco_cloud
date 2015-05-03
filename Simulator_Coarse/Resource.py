import simpy
import logging 

class LinearCostFunc(object):
	def __init__(self, a= 1, b= 0):
		self.a = a
		self.b = b
		
	def compute(self, usage):
		return  self.a*usage + self.b

class BarrierFunc(object):# Compute overload for a resource
	def __init__(self, a= -1, b= -1):
		self.a = a
		self.b = b
	
	def compute(self, normAvailRes):
		'''
		 ax +b + 1/(1-x)
		'''
		if normAvailRes >= 1:
			return float('inf')
		else:
			return self.a*normAvailRes+self.b+1/(1-normAvailRes)

class NoCostFunc(object):
	def compute(self, usage):
		return 0

class Resource(object):
	def __init__(self, name, env, resources, applications):
		self.env = env
		self.name = name
		self.resources = resources 
		self.applications = applications

		assert isinstance(resources, dict), "%s : resources is not a dict - %s" %(self.getName(), resources)
		
		# Append internal resource properties
		for resource in self.resources.itervalues():
			resource.update({'USAGE':0.0, 'COST':1.0, 'APPS':{}})

		self.peers = {}
		self.appDemands = {}

		self.cost = 0.0
		
	'''
	Attribute getters
	'''
	# Get peers
	def getPeers(self):
		return self.peers

	# Get overload factor 
	def getCurrentCost(self):
		return self.cost
		
	# Get current resource usage 
	def getCurrentResourcesUsage(self):
		result = ''
		#print "----- %s" % (self.getName())
		#print self.resources
		#print "-------------"
		for resourceName, resource in self.resources.iteritems():
			if len(resource['APPS']) != 0:

				result += '\t\t' + resourceName + "\r"
				for appName, appUsage in resource['APPS'].iteritems():
					if appUsage != 0:
						util = appUsage/self.resources[resourceName]['CAPACITY']
						result += "\t\t\t %s - %f \r" % (appName, util)
		
		return result 

	# Get list subscribing applications
	def getAppList(self):
		return self.appDemands.keys()

	# Get demand for each application, returns a dictionary with demand type as key
	def getAppDemand(self, appName, demandType):
		return self.appDemands[appName]['TOTAL'][demandType]

	# Get peers as toubles, returns a dictionary
	def getPeersTouple(self):
		result = []
		for peerName, peer in self.peers.iteritems():
			itsPeers = peer.getPeers()
			for itsPeerName, itsPeer in itsPeers.iteritems():
				if self is not itsPeer:
					result.append((peer, itsPeer))
		return result

	# Add peer
	def addPeer(self, peer):
		self.peers[peer.getName()] = peer

	# Get name of the node
	def getName(self):
		return self.name

	# Get appDemand
	def getappDemands(self):
		return self.appDemands

	# Check if node has app
	def hosts(self, app):
		return False

	# Get  latency
	def getLatency(self, direction):
		return 0.0

	'''
	Propagate workload and compute resource usage
	'''
	# Update demand per source per app 
	def updateDemand(self, appName, sourceNodeName, demand):
		if appName not in self.appDemands:
			self.appDemands[appName] = {}
			self.appDemands[appName]['SOURCE'] = {}

		self.appDemands[appName]['SOURCE'][sourceNodeName] = demand
		
		self.computeTotalappDemand()
		self.computeResourceUsage()
		self.cost = self.computeTotalCost()

	def clearDemand(self, appName):
		
		if appName in self.appDemands:
			del self.appDemands[appName]
		
		self.computeTotalappDemand()
		self.computeResourceUsage()
		self.cost = self.computeTotalCost()
		
	def clearAllDemand(self):
		self.appDemands = {}
		
		#print "%s - Cost before : %f " % (self.getName(), self.getCurrentCost()) 
		self.computeTotalappDemand()
		self.computeResourceUsage()
		self.cost = self.computeTotalCost()
		#print "%s - Cost after : %f " % (self.getName(), self.getCurrentCost())

	def incurrTempDemand(self, appName, sourceNodeName, demand, duration):
		self.updateDemand(appName, sourceNodeName, demand)
		env.process(self.removeTempDemand(appName, sourceNodeName, duration))

	def removeTempDemand(self, appName, sourceNodeName, duration):
		yield self.env.timeout(duration)
		self.updateDemand(appName, sourceNodeName, 0.0)

	# Compute total number of appDemand
	def computeTotalappDemand(self):
		self.totalDemand = 0.0
		
		for appName, appDemand in self.appDemands.iteritems():
			totalAppDemand = {}

			for sourceDemand in appDemand['SOURCE'].itervalues():
				for demandType, demand in sourceDemand.iteritems():
					if demandType not in totalAppDemand:
						totalAppDemand[demandType] = 0.0
					totalAppDemand[demandType] += demand
					self.totalDemand += demand
			
			appDemand['TOTAL'] = totalAppDemand

	# [Asbstract] Update resource usage
	def computeResourceUsage(self):
		#logging.info("\t %s - App resource utilisation:" % self.getName() )
		for resourceName, resource in self.resources.iteritems(): # Calculate app usage for each resource usage each application's properties
			resource['APPS'] = {}
			for appName, appDemand in self.appDemands.iteritems(): # For every app
				resource['APPS'][appName] = 0.0

				for demandType, demand in appDemand['TOTAL'].iteritems():
					resource['APPS'][appName] += self.applications[appName].computeResourceUsage(resourceName, demand, demandType)
				
				#logging.info("\t\t %s in %s - %f percent" % (appName, resourceName, resource['APPS'][appName]/resource['CAPACITY']) )
					
		assert isinstance(self.resources, dict), "%s : resources is not a dict - %s" %(self.getName(), self.resources)

		for resourceName, resource in self.resources.iteritems(): # Update usage for each resource 
			totalDemand = 0.0 # Total usage for each resource
			assert isinstance(resource['APPS'], dict), "%s : resource['APPS'] is not a dict - %s" %(self.getName(), resource['APPS'])
			for totalAppDemand in resource['APPS'].itervalues():
				totalDemand += totalAppDemand

			resource['USAGE'] = totalDemand

			#print "%s - resource %s - usage %s" % (self.getName(), resourceName, resource['USAGE'])

	# compute app utilization
	def computeAppUtilization(self):
		# we want usage of all the applications running in that particular resource
		bigDict = {}
		for resourceName,resource in self.resources.iteritems():
			bigDict[resourceName] = {}
			for appName, demand in resource['APPS'].iteritems():
				bigDict[resourceName][appName] = demand
		return bigDict

	# compute resource utilization
	def getResourceUtilization(self):
		# we want usage of all the applications running in that particular resource
		result = {}
		#logging.info("\t %s - Resource utilisation:" % self.getName() )
		for resourceName, resource in self.resources.iteritems():
			result[resourceName] = resource['USAGE']/resource['CAPACITY']
			#logging.info("\t\t %s - %f percent" % (resourceName, result[resourceName]) )
		return result

	'''
	Evaluation of resource usage when scheduling
	'''
	# Evalutae hypothecital resource usage
	def evaluateResourcesUsage(self, targetApps):
		# Input:    app, demand
		# Output:   Total resource usgae for each resource
		
		totalUsage = {}
		
		for resourceName, resource in self.resources.iteritems():
			for appName, appResourceUsage in resource['APPS'].iteritems():
				if appName not in targetApps:
					totalUsage[resourceName] += appResourceUsage
				else:

					totalUsage[resourceName] += self.applications[appName].computeResourceUsage(resourceName, targetApps[appName], 'PRODUCTION')
		
		return totalUsage

	# Evalutae hypothecital resource usage excluding exludeApps
	def evaluateResourcesUsageExcluding(self, exludeApps):
		# Input:    app, demand
		# Output:   Total resource usgae for each resource
		
		totalUsage = {}
		
		for resourceName, resource in self.resources.iteritems():
			totalUsage[resourceName] = 0.0
			for appName, appResourceUsage in resource['APPS'].iteritems():
				if appName not in exludeApps:
					totalUsage[resourceName] += appResourceUsage
		#logging.info("\t %s - Total resource consumed: %s " % (self.getName(), totalUsage) )
		return totalUsage

	# Evalutae hypothecital resource usage given the addition of targetApps
	def evaluateAdditionalResourcesUsage(self, targetApps):
		usage = {}

		for resourceName in self.resources:
			usage[resourceName] = 0.0
			for appName, demand in targetApps.iteritems():
				for demandType, demandVolume in demand.iteritems():
					#print "%s: %s - %s for %s = %f" %(appName, demandType, demandVolume, resourceName, self.applications[appName].computeResourceUsage(resourceName, demandVolume, demandType))
					usage[resourceName] += self.applications[appName].computeResourceUsage(resourceName, demandVolume, demandType)
	
		#print "%s - %s -> %s" % (self.getName(), targetApps, usage)
	
		return usage
		
	'''
	Evalutae hypothecital badness usage given the addition of targetApps
	'''
	def evaluateAggregateCost(self, targetResources):
		result = 0.0
		# compute the app + overload cost
		for resourceName, resourceUsage in targetResources.iteritems():
			resource = self.resources[resourceName]
			#print "%s - resource %s - usage %s" % (self.getName(), resourceName, resource['USAGE'])
			overload = resource['OVERLOADCOST'].compute(resourceUsage/resource['CAPACITY'])
			cost = resource['EXECOST'].compute(resourceUsage)
			
			result += resource['MU']*overload + cost
	
		return result
	
		# Compute the current overload factor
	def computeTotalCost(self):
		'''
		Total = app_execution + mu*overload_cost
		param mu:  
		'''
		result = 0.0
		# compute the app + overload cost
		for resourceName, resource in self.resources.iteritems():
			#print "%s - resource %s - usage %s" % (self.getName(), resourceName, resource['USAGE'])
			overload = resource['OVERLOADCOST'].compute(resource['USAGE'])/resource['CAPACITY']
			cost = resource['EXECOST'].compute(resource['USAGE'])
			
			resource['COST'] = resource['MU']*overload + cost
			result += resource['COST']
			if resourceName is "CPU": 
				print "%s - overload %s - cost %s- usage %s- capacity %s" % (self.getName(), overload, cost, resource['USAGE'], resource['CAPACITY'])
		return result
	
	# Evalutae if an application can be accomodated in the infrastucture
	def willAppFit(self, targetApps):
		result = {}
		usage = self.evaluateResourcesUsage(targetApps)
		
		for resourceName, resourceUsage in usage.iteritems():
			result[resourceName] = resourceUsage < self.resources[resourceName]['CAPACITY']
			
		return result
		
	# Evalutae if an application can be accomodated in the infrastucture
	def willResourceUsageFit(self, targetResources):
		result = {}
		
		for resourceName, resourceUsage in resourceUsage.iteritems():
			result[resourceName] = resourceUsage < self.resources[resourceName]['CAPACITY']
			
		return result
	
	def evaluateLatency(self, resourceUsage):
		return 0