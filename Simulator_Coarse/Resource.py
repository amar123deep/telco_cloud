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

		self.subscribers = {}
		self.nbrSubscribers = 0

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
	
	# Get subscribers
	def getSubscribers(self):
		return self.subscribers
	
	# Check if node has app
	def hosts(self, app):
		return False
	
	# Get  latency
	def getLatency(self, direction):
		return 0.0
	
	'''
	Propagate workload and compute resource usage
	'''
	# Update subscribe per leaf per app 
	def updateSubscriber(self, appName, leafName, nbrUsers):
		if appName not in self.subscribers:
			self.subscribers[appName] = {}
			self.subscribers[appName]['LEAFS'] = {}

		self.subscribers[appName]['LEAFS'][leafName] = nbrUsers

		self.computeTotalSubscribers()

		self.computeResourceUsage()
		
		self.computeTotalOverload()
		
	# Compute total number of subscribers
	def computeTotalSubscribers(self):
		self.nbrSubscribers = 0
		for appName in self.subscribers:
			nbrAppSubscribers = 0
			for leafName in self.subscribers[appName]['LEAFS']:
				nbrAppSubscribers += self.subscribers[appName]['LEAFS'][leafName]
			
			self.subscribers[appName]['TOTAL'] = nbrAppSubscribers
			self.nbrSubscribers += nbrAppSubscribers

	# [Asbstract] Update resource usage
	def computeResourceUsage(self):
		for appName in self.subscribers: # For every app
			for resourceName, resource in self.resources.iteritems(): # Calculate app usage for each resource usage each application's properties
				resource['APPS'][appName] = self.applications[appName].computeResourceUsage(resourceName, self.subscribers[appName]['TOTAL'])

		for resource in self.resources.itervalues(): # Update usage for each resource 
			totalSubsucribers = 0 # Total usage for each resource
			for nbrAppSubscribers in resource['APPS'].itervalues():
				totalSubsucribers += nbrAppSubscribers

			resource['USAGE'] = totalSubsucribers
		
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
		# Input:    app, nbrUsers
		# Output:   Total resource usgae for each resource
		
		totalUsage = {}
		
		for resourceName, resource in self.resources.iteritems():
			for appName, appResourceUsage in resource['APPS'].iteritems():
				if appName not in targetApps:
					totalUsage[resourceName] += appResourceUsage
				else:
					totalUsage[resourceName] += self.applications[appName].computeResourceUsage(resourceName, targetApps[appName])

		return totalUsage
		
	# Evalutae hypothecital resource usage excluding exludeApps
	def evaluateResourcesUsageExcluding(self, exludeApps):
		# Input:    app, nbrUsers
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
			for appName, nbrUsers in targetApps.iteritems():
				usage[resourceName] += self.applications[appName].computeResourceUsage(resourceName, targetApps[appName])

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