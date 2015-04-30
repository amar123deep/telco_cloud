import simpy
import os
from Datacentre import Datacentre
from multiprocessing import Process, Queue
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
		self.measuredSystemOverload = float('inf')
		self.placementRegistry = []
		self.evaluationRegistry = []
		
	def recordPlacement(self, appName, dcName, time):
		self.placementRegistry.append( (time, appName, dcName) )
		
	def recordEvaluation(self, time, nodes):
		self.evaluationRegistry.append( (time, nodes) )
	
	'''
	######## Evaluation ########
	'''
	# Evalute if path can accomodate the placement option
	def evaluateAppPlacementCost(self, appPlacement):
		entities = self.evaluateAppPlacementResourcesUsage(appPlacement)
		
		overloadFactor = 0

		assert isinstance(entities, dict), "%s : entities is not a dict - %s" %(self.getName(), entities)

		for entity in entities.itervalues():
			entitiyOverload = entity['ENTITY'].evaluateAggregateCost(entity['USAGE'])
			
			overloadFactor += entitiyOverload
		
		return overloadFactor	
	
	# Evalute if path can accomodate the placement option (threaded)
	def evaluateAppPlacementCost_threaded(self, index, appPlacement, queue):
		entities = self.evaluateAppPlacementResourcesUsage(appPlacement)
		
		overloadFactor = 0

		assert isinstance(entities, dict), "%s : entities is not a dict - %s" %(self.getName(), entities)

		for entity in entities.itervalues():
			entitiyOverload = entity['ENTITY'].evaluateAggregateCost(entity['USAGE'])
			
			overloadFactor += entitiyOverload
		
		queue.put((index, overloadFactor))	
	
	# Compute total local resource usage for app in appNames and paths 
	def evaluateAppPlacementResourcesUsage(self, appPlacement): # appPaths ([PATH], appName, demand)
		enteties = {}
		for (path, appName, demand) in appPlacement:
			for entity in path:
				if entity.getName() not in enteties:
					enteties[entity.getName()] = {'USAGE':entity.evaluateResourcesUsageExcluding(appName), 'ENTITY':entity}
				
				usage = entity.evaluateAdditionalResourcesUsage({appName:demand})
				for resourceName, resourceUsage in usage.iteritems():
					enteties[entity.getName()]['USAGE'][resourceName] += resourceUsage
						
		return enteties
	
	# Evalute if path can accomodate the placement option
	def evaluatePath(self, appPlacement):
		entities = self.evaluateAppPlacementResourcesUsage(appPlacement)
		
		for entity in entities:
			entity['FITS'] = entity['ENTITY'].willAppFit({appName: entity['USAGE']})
	
	def getoverloadNodes(self,dictAppNode):
		"""
		Descr : compute the overload of the nodes where the application is 
				running 
		Input:  A dictionary with key as application and value as node on which
				the application is running
		Output: Dictionary, key: app, value: overload for the corresponding nodes
				where the app is running 
		"""
		overloadNodes = {}
		for app,node in dictAppNode:
			overloadNodes[node.getName()]=node.getOverload()
		return overloadNodes
	
	def overloadListNodes(self,lstNode):
		"""
		Descr : computes overload for a list of nodes  
		Input : List of Nodes whose overload we need to compute 
		Output: List containing overload for corresponding nodes
		"""
		lstoverloadNodes = []
		for node in lstNode:
			lstoverloadNodes.append(node.getOverload())
		return lstoverloadNodes
	
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
			overloadLocalNodes = {}
			for n in listNodes: 
				n.resource = n.resource + app.resource
				overloadLocalNodes[n] = n.getOverload()
			minNode = min(overloadLocalNodes,key = overloadLocalNodes.get) 
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
		# compute the overload of the node where the apps are running 
		dictAppNodeOverload = {}
		appToBeEvaluated = {}
		for app,node in dictAppNode:
			dictAppNodeOverload[app] = node.getOverload()
			if dictAppNodeoverload[app] > thldApp[app]:
				appToBeEvaluated[app] = node
			else: 
				# add the app to the node as constraint is fulfilled 
				node.resource = node.resource + app.resource
		possiblePlacementDict = self.evaluateNeighbour(appToBeEvaluated)
		return possiblePlacementDict

	def output(self, outputFolder):
		outputs = [self.writePlacementToFile, self.writeEvaluationsToFile]
		
		path = "results"
		
		if not os.path.exists(path):
			os.mkdir(path)
		
		path += "/%s" % outputFolder
		
		if not os.path.exists(path):
			os.mkdir(path)
		
		for output in outputs:
			output(path)
	
	def writePlacementToFile(self, filePath):
		file = open('%s/%s%s'%(filePath,'PLACEMENTS','.csv'),'w')
		file.write("%s%s%s%s%s\r" % ('Time', ',', 'App', ',', 'DC') )
		
		for (time, appName, dcName) in self.placementRegistry:
			file.write("%i%s%s%s%s\r" % (time, ',', appName, ',', dcName) )
		
		file.close()

	def writeEvaluationsToFile(self, filePath):
		file = open('%s/%s%s'%(filePath,'EVALUATIONS','.csv'),'w')
		file.write("%s%s%s\r" % ('Time', ',', 'Nbr nodes') )
		
		for (time, nodes) in self.evaluationRegistry:
			file.write("%i%s%s\r" % (time, ',', nodes) )
		
		file.close()
