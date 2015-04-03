import simpy
from Datacentre import Datacentre
from Link import Link

class Scheduler(object):
	"""
	Declare global dictionary that will keep track of all the apps and the nodes 
	on which they are running. Later we plan to assign ID to each application. 
	"""
	appNodeDictGlobal = {}
		
	def __init__(self, env, topology):
		self.env = env
		self.topology = topology
		self.placements = []
		
		#self.monitor.registerSignal( "PLACEMENTS" )
		#self.monitor.registerOutput( [ ("PLACEMENTS", SystemMonitor.fileCSVOutput, self.composePlacementsHeader) ] )
	
	def addMeasurement(self, data):
		self.placements.append(data)
		
	def getPlacementBuffer(self):
		placementsBuffer = str()
		
		for placement in self.placements:
			placementsBuffer += "%s \r" % placement
			
		self.placements = []
		
		return placementsBuffer
		
	def removeDC(self,AppDCList):
		'''
		removes the list of DCs from the table of the topology
		'''
		for (appName, dcName) in AppDCList:
			dc = self.topology.getNode(dcName)
			dc.terminateApp(appName)
		self.topology.removeFromTable(AppDCList)
	
	
	def addAppLeafNode(self, appNodeDict): 
		"""
		Descr : This function should be called when new app appears in the 
				system
		Input : app and the leaf node where the app should run   
		Output: return 1 on success
		"""
		badness = self.getBadnessNodes(appNodeDict)
		
	def lookupDistH (self,nodeList,dist): 
		"""
		Descr : compute all the neighbour for distance less than and equal to dist
				
		Input : distance dist, node list
		
		"""
		newDict = {}
		for n in nodeList: 
			newDict[n] = self.lookupNeighbour(n,dist)
			
		return newDict    
	
	def generateSolutions(self, dist, numNodes): 
		_masterList = []
		baseList = [0]*numNodes 
		#while dist <=0:
		for i in range(dist):
			baseList[i] = dist -i 
			dist = dist -1
		pass
	
	# Method depricated 
	def exploreNeighbour(self, node, dist):
		"""
		compute all the possible neighbour at fixed distance h
		"""
		newDict = {node.getName():{'N_NODE':node,'EDGE':[]}}
		d = 0
		while d< dist: 
			d = d+1
			#print newDict
			print "----------"
			_temp1 = {}
			for nodeAttributes in newDict.itervalues(): 
				#print nodeAttributes
				tempListTuples = nodeAttributes['N_NODE'].getPeersTouple()
				_temp = {}
				for (e,v) in tempListTuples:
					_temp[v.getName()] = {'N_NODE':v,'EDGE':nodeAttributes['EDGE']+[e]}
					#_temp[v.getName()] = {'N_NODE':v,'EDGE':[nodeAttributes['EDGE'],e]}
				# to add the previous edges
				_temp1  = dict(_temp.items() + _temp1.items())
				newDict =  _temp1
		if node.getName() in newDict:
			del newDict[node.getName()]
		print "---result---"
		return newDict
	
	# Method depricated	
	def lookupNeighbour(self, node, dist): 
		"""
		returns all the nodes along with edges (as tuple) at specific distance dist 
		
		"""
		
		newDict = {node.getName():{'N_NODE':node,'EDGE':[]}}
		d = 0
		while d<= dist: 
			d = d+1
			print "----------"
			for nodeAttributes in newDict.itervalues(): 
				#print nodeAttributes
				tempListTuples = nodeAttributes['N_NODE'].getPeersTouple()
				_temp = {}
				for (e,v) in tempListTuples:
					_temp[v.getName()] = {'N_NODE':v,'EDGE':nodeAttributes['EDGE']+[e]}
				# to add the previous edges
				_temp1  = dict(_temp.items() + newDict.items())
				newDict =  _temp1
		return newDict
		
	
	def findNeighbourGlobal(self,dictAppNode):
		"""
		Descr:  Compute the neighbours if possible, node and link
		Input:  A dictionary with key as application and value as node on which
				the application is running 
		Output: dictionary, key: app, value: all the nodes corresponding to the 
				node where the app is running  
		"""
		dictAppNeighbour = {}
		for app,node in dictAppNode:
			dictAppNeighbour[app] = node.getChildNodes().append(node.getParentNode())
		return dictAppNeighbour
	
	def evaluateTotalBadness(self, appName, leafNodes, dc):
		"""
		Descr : Evaluates total badness from 
		Input : app and the leaf node where the app should run   
		Output: return 1 on success
		"""
		pass
	
	'''
	######## Measurements ########
	'''
	# [DEPRICATED] Sums badness in each resource entity
	def measureTotalBadness(self):
		badness = 0
		
		enteties = self.topology.getAllDCs() + self.topology.getAllLinks()
		
		for entity in enteties:
			badness += entity.getBadness()
			
		return badness
	
	# [DEPRICATED] Produce header for 
	def produceTotalBadnessHeader(self):
		return 'Total badness'
	
	# [DEPRICATED] Sums badness in each resource entity
	def measureBadness(self):
		badness = ''
		
		enteties = self.topology.getAllDCs() + self.topology.getAllLinks()
		
		for entity in enteties:
			badness += "%f ," % entity.getBadness()
			
		return badness
	
	# [DEPRICATED] Produce header for 
	def produceBadnessHeader(self):
		header = ''
		
		enteties = self.topology.getAllDCs() + self.topology.getAllLinks()
		
		for entity in enteties:
			header += entity.getName() + ','
			
		return header
	
	# [DEPRICATED] Compute total local resource usage for app in appNames and paths 
	def evaluateLocalResourcesUsage(self, appName, paths):
		enteties = {}
		
		for path in paths.iteritems():
			population = path[0].getAppPopulation(appName)
			for entity in path:
				if entity.getName() not in enteties:
					enteties[entity.getName()] = {'USAGE':entity.evaluateResourcesUsageExcluding(appName), 'ENTITY':entity}
				else:
					usage = entity.evaluateAdditionalResourcesUsage({appName:population})
					for resourceName, resourceUsage in usage.iteritems():
						enteties[entity.getName()]['USAGE'][resourceName] += resourceUsage[resourceName]
		return enteties
		
	# Compute total local resource usage for app in appNames and paths 
	def evaluateAppPlacementResourcesUsage(self, appPlacement): # appPaths ([PATH], appName, nbrUsers)
		enteties = {}
		
		for (path, appName, nbrUsers) in appPlacement:
			for entity in path:
				if entity.getName() not in enteties:
					enteties[entity.getName()] = {'USAGE':entity.evaluateResourcesUsageExcluding(appName), 'ENTITY':entity}
				else:
					usage = entity.evaluateAdditionalResourcesUsage({appName:nbrUsers})
					for resourceName, resourceUsage in usage.iteritems():
						enteties[entity.getName()]['USAGE'][resourceName] += resourceUsage
		return enteties
	
	# Evalute if path can accomodate the placement option
	def evaluatePath(self, appPlacement):
		entities = self.evaluateAppPlacementResourcesUsage(appPlacement)
		
		for entity in entities:
			entity['FITS'] = entity['ENTITY'].willAppFit({appName: entity['USAGE']})
	
	# [DEPRICATED] Evalute if path can accomodate the placement option
	def evaluateAppPlacementBadness(self, appPlacement):
		entities = self.evaluateAppPlacementResourcesUsage(appPlacement)
		
		badness = 0

		for entity in entities.itervalues():
			badness += entity['ENTITY'].evaluateAggregateBadness(entity['USAGE'])
			
		return badness
		
	# Evalute if path can accomodate the placement option
	def evaluateAppPlacementOverload(self, appPlacement):
		entities = self.evaluateAppPlacementResourcesUsage(appPlacement)
		
		overloadFactor = 0

		for entity in entities.itervalues():
			overloadFactor += entity['ENTITY'].evaluateAggregateOverload(entity['USAGE'])
			
		return overloadFactor	
	
	def findNeighbourLocal(self,node): 
		return node.getChildNodes().append(node.getParentNode())
		
	def getBadnessNodes(self,dictAppNode):
		"""
		Descr : compute the badness of the nodes where the application is 
				running 
		Input:  A dictionary with key as application and value as node on which
				the application is running
		Output: Dictionary, key: app, value: badness for the corresponding nodes
				where the app is running 
		"""
		badnessNodes = {}
		for app,node in dictAppNode:
			badnessNodes[node.getName()]=node.getBadness()
		return badnessNodes
	
	def badnessListNodes(self,lstNode):
		"""
		Descr : computes badness for a list of nodes  
		Input : List of Nodes whose badness we need to compute 
		Output: List containing badness for corresponding nodes
		"""
		lstbadnessNodes = []
		for node in lstNode:
			lstbadnessNodes.append(node.getBadness())
		return lstbadnessNodes
	
	def evaluateNeighbour(self,appToBeEvaluated):
		"""
		Descr  : This function evaluates the all the nodes where application 
				 violates the node constraints 
		Input  : dictionary of app, node 
		Output : dictionary of possible neighbour nodes for placement for 
				 corresponding application   
		"""
		res = {}
		for app,node in appToBeEvaluated:
			listNodes = node.findNeighbourLocal(node)
			badnessLocalNodes = {}
			for n in listNodes: 
				n.resource = n.resource + app.resource
				badnessLocalNodes[n] = n.getBadness()
			minNode = min(badnessLocalNodes,key = badnessLocalNodes.get) 
			# Node dictionary for placement 
			res[app] = minNode
		return res 
		
	# Schedule an application
	def schedule(self, dictAppNode,thldApp):
		"""
		Descr  : finds the node among the list of the nodes where the 
				 application is migrated based on certain threshold    
		Input  : dictAppNode: dictionary of (app,Node) to be placed, thldApp
		Output : node where the cost of running the app is minimum 
		"""
		# compute the badness of the node where the apps are running 
		dictAppNodeBadness = {}
		appToBeEvaluated = {}
		for app,node in dictAppNode:
			dictAppNodeBadness[app] = node.getBadness()
			if dictAppNodeBadness[app] > thldApp[app]:
				appToBeEvaluated[app] = node
			else: 
				# add the app to the node as constraint is fulfilled 
				node.resource = node.resource + app.resource
		possiblePlacementDict = self.evaluateNeighbour(appToBeEvaluated)
		return possiblePlacementDict
		
	
	# Notify scheduler of a change in the network
	def notifyScheduler(self): # this needs to contain more inotmation about the change, but for now, it is enough that we send a trigger now.
		pass