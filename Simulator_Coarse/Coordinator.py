
import logging

class Coordinator(object):
	'''
	Descr : coordinates workload changes
	'''
	def __init__(self, env, topology, scheduler, depth):
		self.env = env
		self.topology = topology
		self.scheduler = scheduler
		self.depth = depth
		
		self.registry = {}
		
		self.appWorkloadCache = None

		#env.process(self.clearResources())

	def getAppPlacement(self, appName):
		return self.registry[appName]

	def revaluateAll(self):
		'''
		This function when called reevaluates the whole system
		'''
		appsNeedTobeReevaluated = {}
		logging.info("### Revaluating")
		
		totalDemand = {}
		
		for leaf in self.topology.getAllLeafs():
			for appName, demandDict in leaf.getAppDemands().iteritems():
				if appName not in totalDemand:
					totalDemand[appName] = {}
				totalDemand[appName].update(demandDict)
		
		for appName, nodeUser in totalDemand.iteritems():
				assert isinstance(demandDict, dict), "%s : demandDict is not a dict - %s" %(self.getName(), nodeUser)
				appsNeedTobeReevaluated[appName] = (nodeUser, self.topology.findNeighbours(self.registry[appName], self.depth))
		
		if len(appsNeedTobeReevaluated) > 0:
			self.callScheduler(appsNeedTobeReevaluated)
		
		self.updateDemand()
		
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
	def updateDemand(self):
		self.topology.clearDemand()
		for appName, nodeUser in self.appWorkloadCache.iteritems():
			# Update workload
			if appName in self.registry:
				dcName = self.registry[appName]
				for leafNodeName, demand in nodeUser.iteritems(): 
					if demand['PRODUCTION'] != 0:
						path = self.topology.getPath(appName, leafNodeName, dcName)
						#x_list = []
						#for x in path: 
						#	x_list.append(x.getName())
						#print "%s -> %s (%s) : %s" % (leafNodeName, dcName, x_list, demand)
						for entity in path:
							#print "%s + %s (%s)"%(entity.getName(), appName, demand)
							entity.updateDemand(appName, leafNodeName, demand)
							#print "\t %s - %f" % (entity.getName(), entity.getCurrentCost())
			else: 
				print "%s is not scheduled" % (appName)

	def processWorkload(self,appWorkload):
		'''
		This function receives workload from each time stamp from the workload generator,
		appWorkload has structure: {App:{node:user}}
		'''
		logging.debug('### Start workload processing')
		
		self.appWorkloadCache = appWorkload.copy()

		#print self.registry

		# All apps from workload at current time instant 
		currentAPPlist = self.appWorkloadCache.keys()
		# we store apps that's need to be scheduled and are absent in the registry
		appsWorkloadNotScheduled = {}
		for appName, nodeUser in self.appWorkloadCache.iteritems():  # appName , {leaf: nbrUsers}  

			if appName not in self.registry: # registry contains 
				#appsWorkloadNotScheduled[appName] = (nodeUser, self.topology.getAllDCsName()) 
				#print nodeUser
				#print self.topology.findNeighbours(self.topology.getRandomDCName(), self.depth)
				#print "------------"
				appsWorkloadNotScheduled[appName] = (nodeUser, self.topology.findNeighbours(self.topology.getRandomDCName(), self.depth))

		removeAppDClist = []
		for appName, dcName in self.registry.iteritems():
			if appName not in currentAPPlist:
				# remove from the registry
				removeAppDClist.append((appName,dcName))
				# ask scheduler to remove also from the topology table
		logging.info('\t %s - apps need to be removed: %s' % (type(self).__name__, str(removeAppDClist)))

		for (appName,dcName) in removeAppDClist: 
			del self.registry[appName]

		logging.info('\t %s - apps needs to be scheduled : %s ' % (type(self).__name__, str(appsWorkloadNotScheduled.keys())))
		if len(appsWorkloadNotScheduled) > 0:
			self.callScheduler(appsWorkloadNotScheduled)
			
		self.updateDemand()
		
		#print self.registry

	def callScheduler(self, appsWorkloadNotScheduled):
		'''
		This function calls the scheduler function
		'''
		for appName, dcName in self.scheduler.fnSchedule(appsWorkloadNotScheduled, self.registry):
			if dcName is not None:
				# Update app registry 
				self.registry[appName] = dcName

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
	
		logging.debug('%s - apps needs to be scheduled : %s ' % (type(self).__name__, str(appsNotScheduled.keys())))

		for (appName, dcLeafDict) in self.scheduler.fnSchedule(appsNotScheduled):
			for dcName in dcLeafDict:
				if dcName is not None:
					# Update app registry 
					self.registry[appName] = dcLeafDict  
					(nodeUser, placementOptions) = appsNotScheduled[appName]
					
					for leafNodeName, nbrUsrs in nodeUser.iteritems(): 
						yield (self.topology.getPath(appName, leafNodeName, dcName), appName, leafNodeName, nbrUsrs)