import simpy

class Resource(object):
	
	def __init__(self, name, env, resources, applications):
		self.env = env
		self.name = name
		self.resources = resources 
		self.applications = applications

		# Append internal resource properties
		for resource in self.resources.itervalues():
			resource.update({'USAGE':0.0, 'BADNESS':0.0, 'APPS':{}})

		self.peers = {}

		self.subscribers = {}
		self.nbrSubscribers = 0

		self.badness = 0.0

	'''
	Attribute getters
	'''
	# Get peers
	def getPeers(self):
		return self.peers
	
	# Get peers as toubles, returns a dictionary
	def getOverloadFactor(self):
		overloadFactor = 1
		
		for resource in self.resources.itervalues():
			overloadFactor*= 1/(1-resource['USAGE'])
			
		return overloadFactor
	
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
		
	# Get badness
	def getBadness(self):
		return self.badness
	
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

	# [DEPRECATED] Compute the current badness
	def computeTotalBadness(self): 
		result = 0.0
		
		for resource in self.resources.itervalues():
			badness = self.computeBadness(
				resource['USAGE']
				/resource['CAPACITY'],
				resource['THRESHOLD'])

			resource['BADNESS'] = badness
			result += badness

		self.badness = result

	# [DEPRECATED] Compute badness for a resource
	def computeBadness(self, normAvailRes, thldRes):
		if normAvailRes >= 1:
			return float('inf')
		elif normAvailRes <= thldRes:
			return 0.0
		else:
			return abs(thldRes-normAvailRes)*1/(1-normAvailRes)

	'''
	Finding paths for workload propagation and scheduling
	'''
	# [Deprecated] Find paths to from this resource to application
	def findPaths(self, appName): # Caution! Only for trees
		# [Preliminary] Recursive search function
		def traverse(node, path, appName, paths):
			if node.hosts(appName): # If node hosts application
				#print "%s found in %s along path %s" % (appName, node.getName(), str(path))
				paths.append(path)
			else: # Keep looking ...
				peers = node.getPeers()
				for peerName in peers:
					if peers[peerName] not in path: 
						traverse(peers[peerName], path + [peers[peerName]], appName, paths)

		paths = [] # All the resulting paths
		path = [] # Iteratively constructed path

		traverse(self, path+[self], appName, paths)
		
		return paths
		
	# [Deprecated] Find paths to from this resource to application
	def findMinPath(self, appName): # Caution! Only for trees
		paths = self.findPaths(appName)
		
		assert len(paths)>0, 'App %s not found from %s' % (appName, leafName)

		minLen = sys.maxint
		minPath = None

		for path in paths:
			if len(path)<=minLen:
				minLen = len(path)
				minPath = path
		
		return minPath

	# [Deprecated] Find paths to from this resource to application
	def findPathsDC(self, fromNode, toNode): # Caution! Only for trees

		def traverse(node, path, toNodeName, paths):
			if node.getName is toNodeName:
				paths.append(path)
			else: # Keep looking ...
				peers = node.getPeers()
				for peerName in peers:
					if peers[peerName] not in path: 
						traverse(peers[peerName], path + [peers[peerName]], dcName, paths)

		paths = [] # All the resulting paths
		path = [] # Iteratively constructed path

		traverse(self, path+[self], toNode.getName(), paths)
		
		return paths

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

	# Evalutae hypothecital badness this consistillation
	def evaluateBadness(self, targetApps):
		# Input:    apps is a dictionary with application name and population
		# Output:   The badness for each resource, when taking into accound the 
		#           additional workload incurred by app and nbrUsers.
		badness = {}

		totalUsage = self.evaluateResourcesUsage(targetApps)

		exclude = targetApps.keys()
		
		# For all other apps
		for resourceName, resource in self.resources.iteritems():
			badness[resourceName] = self.computeBadness(totalUsage[resourceName]/resource['CAPACITY'], resource['THRESHOLD'])

		return badness

	# Evalutae hypothecital badness usage given the addition of targetApps
	def evaluateBadnessAdditive(self, targetApps):
		# Input:    apps is a dictionary with application name and population
		# Output:   The badness for each resource, when taking into accound the 
		#           additional workload incurred by app and nbrUsers.
		badness = {}

		totalUsage = self.evaluateResourcesUsage(targetApps)

		exclude = targetApps.keys()
		
		# For all other apps
		for resourceName, resource in self.resources.iteritems():
			badness[resourceName] = self.computeBadness(totalUsage[resourceName]/resource['CAPACITY'], resource['THRESHOLD'])

		return badness
		
	# Evalutae hypothecital badness usage given the addition of targetApps
	def evaluateResourceBadness(self, targetResources):
		badness = {}

		for resourceName, resourceUsage in targetResources.iteritems():
			badness[resourceName] = self.computeBadness(resourceUsage/self.resources[resourceName]['CAPACITY'], self.resources[resourceName]['THRESHOLD'])

		return badness
		
	# [DEPRECATED] Evalutae hypothecital badness usage given the addition of targetApps
	def evaluateAggregateBadness(self, targetResources):
		badness = 0.0

		for resourceName, resourceUsage in targetResources.iteritems():
			badness += self.computeBadness(resourceUsage/self.resources[resourceName]['CAPACITY'], self.resources[resourceName]['THRESHOLD'])

		return badness
		
	# Evalutae hypothecital badness usage given the addition of targetApps
	def evaluateAggregateOverload(self, targetResources):
		overload = 1

		for resourceName, resourceUsage in targetResources.iteritems():
			overload *= 1/(1+resourceUsage/self.resources[resourceName]['CAPACITY'])
			
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