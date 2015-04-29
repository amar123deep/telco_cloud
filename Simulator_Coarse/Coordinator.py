import logging

class Coordinator(object):
	'''
	Descr : coordinates workload changes
	'''
	def __init__(self, env, topology, scheduler):
		self.env = env
		self.topology = topology
		self.scheduler = scheduler
		self.registry = {}

		#env.process(self.clearResources())

	def getAppPlacement(self, appName):
		assert appName in self.registry, "Application not scheduled"
		return self.registry[appName].keys()[0]

	def revaluateAll(self):
		targetApps = {}

		for leaf in self.topology.getAllLeafs():
			leafName = leaf.getName()
			for appName, demandDict in leaf.getAppDemand().iteritems():
				if appName not in targetApps:
					targetApps[appName] = {}

				totalDemand = 0

				for demandType, demand in demandDict.iteritems():
					totalDemand += demand

				targetApps[appName].update( {leafName: totalDemand} ) 

		targetConstellations = {}
		
		for appName, totalAppDemand in targetApps.iteritems():
			targetConstellations[appName] = (totalAppDemand, self.topology.getAllDCs())

		for (appName, dcLeafDict) in self.scheduler.fnSchedule(targetConstellations):
			for dcName in dcLeafDict:
				if dcName is not None:
					for currentDC in dcLeafDict.keys():
						if currentDC not in self.registry[appName]:
							print "%s - %s migrated from %s to %s" % (self.env.now, appName, self.registry[appName].keys(), dcLeafDict.keys())
							for currentDCName in self.registry[appName]:
								self.clearPaths(appName, currentDCName)
							self.updateDemand(appName, dcName, targetApps[appName])
							self.registry[appName] = dcLeafDict # Update app registry 

	'''
	######## Migration ########
	'''
	def migrate(self, appName, fromNodeName, toNodenName):
		path = self.topology.findMinPath(fromNodeName, toNodenName)

		demand = path[0].getAppDemand(appName,'PRODUCTION')

		duration = 2

	'''
	Clear all previous paths
	'''
	def clearPaths(self, appName, dcName):
		leafNames = self.topology.getAllLeafNames()
		for leafName in leafNames:
			path = self.topology.getPath(appName, leafName, dcName)
			for entity in path:
				#print "%s overload Before : %s" % (entity.getName(), entity.getOverloadFactor())
				entity.clearDemand(appName)
				#print "%s overload After : %s" % (entity.getName(), entity.getOverloadFactor())

	'''
	Update demand
	'''
	def updateDemand(self, appName, dcName, leafDemand):
		for leafName, leafDemand in leafDemand.iteritems():
			path = self.topology.getPath(appName, leafName, dcName)
			for entity in path:
				entity.updateDemand(appName, leafName, {'PRODUCTION':leafDemand})

	
	
	def getPath(self,appWorkload):
		'''
		
		'''
		logging.debug('%s - Handling apps: %s, runnings apps: %s ' % (type(self).__name__, str(appWorkload.keys()), str(self.registry.keys())))
		# All apps from workload at current time instant 
		currentAPPlist = appWorkload.keys()
		# we store apps that's need to be scheduled and are absent in the registry
		appsNotScheduled = {}
		
		
		
		
	'''
	This can propbably be done more beutiful, but only necessary if we will publish the code. :)
	'''
	def getPath_v1(self, appWorkload): # { ... {appName: {leaf: nbrUsers}}...}
		logging.debug('%s - Handling apps: %s, runnings apps: %s ' % (type(self).__name__, str(appWorkload.keys()), str(self.registry.keys())))
		'''
		Descr : A generator function, yield results and resumes, so iterate over 
				this function when you use it. 
		'''
		# All apps from workload at current time instant 
		currentAPPlist = appWorkload.keys()
		# we store apps that's need to be scheduled and are absent in the registry
		appsNotScheduled = {}
		for appName, nodeUser in appWorkload.iteritems(): # appName , {leaf: nbrUsers}
			logging.debug('%s - Evaluating %s' % (type(self).__name__, appName))

			if appName not in self.registry: 
				appsNotScheduled[appName] = (nodeUser, self.topology.getAllDCs()) 
				logging.debug('%s - %s is NOT running : Net runnings apps %s' % (type(self).__name__, appName, str(appsNotScheduled.keys())))

			else:
				logging.debug('%s - %s is running' % (type(self).__name__, appName))
				# change here
				dcLeafDict = self.registry[appName]
				for dcName, prevLeafList in dcLeafDict.iteritems():
					currentLeafList = nodeUser.keys()
					# Leafs with workload 0 to be updated 
					diffLeaf = set(prevLeafList)-set(currentLeafList)
					for x in diffLeaf:
						nodeUser[x] = 0
					for leafNodeName, nbrUsrs in nodeUser.iteritems():
						path = self.topology.getPath( appName, leafNodeName, dcName )
						pathName = [] 
						for varPath in path: 
							pathName.append(varPath.getName())
						logging.debug('%s - Node: %s, User: %d'%(type(self).__name__, leafNodeName,nbrUsrs))
						logging.debug('%s - Returning path for %s from %s and %s with %i users: %s' % (type(self).__name__, appName, leafNodeName, dcName, nbrUsrs, str(pathName)))
						yield (path, appName, leafNodeName, nbrUsrs)

		logging.debug('%s - Current apps from workload: %s' % (type(self).__name__, str(currentAPPlist)))
		removeAppDClist = []
		for appName, dcLeafDict in self.registry.iteritems():
			for dcName in dcLeafDict.keys():
				if appName not in currentAPPlist:
					# remove from the registry
					removeAppDClist.append((appName,dcName) )
					# ask scheduler to remove also from the topology table
			logging.debug('%s - apps need to be removed: %s' % (type(self).__name__, str(removeAppDClist)))
		for (appName,name) in removeAppDClist: 
			del self.registry[appName]

		self.scheduler.removeDC(removeAppDClist)
	
		logging.debug('%s - apps needs to be scheduled : %s ' % (type(self).__name__, str(appsNotScheduled.keys())))

		for (appName, dcLeafDict) in self.scheduler.fnSchedule(appsNotScheduled):
			for dcName in dcLeafDict:
				if dcName is not None:
					# Update app registry 
					self.registry[appName] = dcLeafDict  
					(nodeUser, placementOptions) = appsNotScheduled[appName]
					
					for leafNodeName, nbrUsrs in nodeUser.iteritems(): 
						yield (self.topology.getPath(appName, leafNodeName, dcName), appName, leafNodeName, nbrUsrs)