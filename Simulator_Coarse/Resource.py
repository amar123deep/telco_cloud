import simpy

class Resource(object):
	
	def __init__(self, name, env, resources, applications):
		self.env = env
		self.name = name
		self.resources = resources 
		self.applications = applications

		# Append internal resource properties
		for resource in self.resources.itervalues():
			resource.update({'USAGE':0.0, 'OVERLOAD':0.0, 'APPS':{}})

		self.peers = {}

		self.appDemand = {}
		self.totalDemand = 0.0

		self.overload = 0.0

	'''
	Attribute getters
	'''
	# Get peers
	def getPeers(self):
		return self.peers
	
	# Get overload factor 
	def getOverloadFactor(self):
		return self.overload
	
	# Get list subscribing applications
	def getAppList(self):
		return self.appDemand.keys()
	
	# Get demand for each application, returns a dictionary with demand type as key
	def getAppDemand(self, appName, demandType):
		return self.appDemand[appName]['TOTAL'][demandType]
	
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
	def getappDemand(self):
		return self.appDemand
	
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
		if appName not in self.appDemand:
			self.appDemand[appName] = {}
			self.appDemand[appName]['SOURCE'] = {}

		self.appDemand[appName]['SOURCE'][sourceNodeName] = demand
		self.computeTotalappDemand()
		self.computeResourceUsage()
		self.computeTotalOverload()
		
		if demand is 0:
			del self.appDemand[appName]['SOURCE'][sourceNodeName]
		
		if len(self.appDemand[appName]['SOURCE']) is 0:
			del self.appDemand[appName]
	
	def incurrTempDemand(self, appName, sourceNodeName, demand, duration):
		self.updateDemand(appName, sourceNodeName, demand)
		env.process(self.removeTempDemand(appName, sourceNodeName, duration))
		
	def removeTempDemand(self, appName, sourceNodeName, duration):
		yield self.env.timeout(duration)
		self.updateDemand(appName, sourceNodeName, 0.0)
	
	# Compute total number of appDemand
	def computeTotalappDemand(self):
		self.totalDemand = 0.0
		for appName, appDemand in self.appDemand.iteritems():
			totalAppDemand = {}
			for sourceNodeName, sourceDemand in appDemand['SOURCE'].iteritems():
				for demandType, demand in sourceDemand.iteritems():
					if demandType not in totalAppDemand:
						totalAppDemand[demandType] = 0.0
					totalAppDemand[demandType] += demand
					self.totalDemand += demand
			
			appDemand['TOTAL'] = totalAppDemand

	# [Asbstract] Update resource usage
	def computeResourceUsage(self):
		for resourceName, resource in self.resources.iteritems(): # Calculate app usage for each resource usage each application's properties
			for appName, appDemand in self.appDemand.iteritems(): # For every app
				resource['APPS'][appName] = 0.0
				for demandType, demand in appDemand['TOTAL'].iteritems():
					resource['APPS'][appName] += self.applications[appName].computeResourceUsage(resourceName, demand, demandType)
					
		for resource in self.resources.itervalues(): # Update usage for each resource 
			totalDemand = 0.0 # Total usage for each resource
			for totalAppDemand in resource['APPS'].itervalues():
				totalDemand += totalAppDemand

			resource['USAGE'] = totalDemand
			
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
		for resourceName, resource in self.resources.iteritems():
			result[resourceName] = resource['USAGE']/resource['CAPACITY']
			
		return result

	# Compute the current overload factor
	def computeTotalOverload(self): 
		result = 0.0
		
		for resource in self.resources.itervalues():
			overload = self.computeOverload(
				resource['USAGE']
				/resource['CAPACITY'])

			resource['OVERLOAD'] = overload
			result += overload

		self.overload = result

	# Compute overload for a resource
	def computeOverload(self, normAvailRes):
		if normAvailRes >= 1:
			return float('inf')
		else:
			return 1/(1-normAvailRes)
			
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
					
		return totalUsage

	# Evalutae hypothecital resource usage given the addition of targetApps
	def evaluateAdditionalResourcesUsage(self, targetApps):
		usage = {}
		
		for resourceName in self.resources:
			usage[resourceName] = 0.0
			for appName, demand in targetApps.iteritems():
				for demandType, demandVolume in demand.iteritems():
					usage[resourceName] += self.applications[appName].computeResourceUsage(resourceName, demandVolume, demandType)

		return usage

	# Evalutae hypothecital badness usage given the addition of targetApps
	def evaluateAggregateOverload(self, targetResources):
		overload = 1

		for resourceName, resourceUsage in targetResources.iteritems():
			overload *= self.computeOverload(resourceUsage/self.resources[resourceName]['CAPACITY'])
		
			#print "%s, %s, %s/%s=%s" % (self.getName(), resourceName, resourceUsage, self.resources[resourceName]['CAPACITY'], overload)
		
		return overload
	
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