import sys
from Link import Link
from Datacentre import Datacentre
class Topology: 
	'''
	Descr : traversing, finding path between any two nodes 
	'''
	
	def __init__(self, env, datacentres, links, leafs):
		self.env = env
		self.datacentres = datacentres
		self.leafs = leafs
		self.links = links
	
		self.pathRegistry = {}
	
	# Return all DCs
	def getAllDCs(self):
		result = []
		
		for dcName in sorted(self.datacentres, key=lambda x: str(x)):
			result.append(self.datacentres[dcName])
		
		return result
		
	# Return all Links 
	def getAllLinks(self):
		result = []
		
		for linkName in sorted(self.links, key=lambda x: str(x)):
			
			result.append(self.links[linkName])
		
		return result
		
	# Return all leafs
	def getAllLeafs(self):
		result = []
		
		for leafName in sorted(self.leafs, key=lambda x: str(x)):
			result.append(self.leafs[leafName])
		
		return result
		
	# Return all leafs
	def getAllLeafNames(self):
		return self.leafs.keys()
	
	def getPath(self, appName, fromNodeName, toNodeName):
		#assert type(appName) is str, "Topology.getPath : appName is not a string"
		#assert type(fromNodeName) is str, "Topology.getPath : fromNodeName is not a string"
		#assert type(toNodeName) is str, "Topology.getPath : toNodeName is not a string"
		
		key = (appName, fromNodeName, toNodeName)
		
		if key not in self.pathRegistry:
			self.updateTable( {key: self.findMinPath(fromNodeName, toNodeName)} )
		
		return self.pathRegistry[key]
	
	def updateTable(self, appPlacementPaths):
		
		for (appName, fromNodeName, toNodeName) , path in appPlacementPaths.iteritems():
			assert type(path) is list , "Provided path is not a list"
			assert len(path) > 2 , "Topology: Path has no length"
			self.pathRegistry[(appName, fromNodeName, toNodeName)] = path
	
	def removeFromTable(self, AppDCList): 
		'''
		This function removes all the entries related to application  
		'''
		keyList = []
		for (appName, fromNodeName, toNodeName) in self.pathRegistry:
			if (appName, toNodeName) in AppDCList: 
				keyList.append((appName, fromNodeName, toNodeName))
		for key in keyList:		
			del self.pathRegistry[key]
	
	'''
	Finding paths for workload propagation and scheduling
	[TO-DO] Do not include intermediate DCs
	'''
	# [Deprecated] Find paths to from this resource to application
	def findPaths(self, fromNodeName, toNodeName): # Caution! Only for trees

		def traverse(node, path):
			traversed_nodes.append(node)
			if node.getName() is toNodeName:
				result.append(path + [node])
				#print "Found node %s, path has %i elements - DONE \r" % (toNodeName, len(result))
			else: # Keep looking ...
				#print "%s Keep looking \r" % '\t'*len(path)
				if type(node) is Link: # Only add intermediate links
					path = path + [node]
					
				peers = node.getPeers()
				
				#print "%s %s has %i peers : %s \r" % ('\t'*len(path), node.getName(), len(peers), str(peers))
				for peer in peers.itervalues():
					if peer not in traversed_nodes: 
						traverse(peer, path)
		
		fromNode = self.getNode(fromNodeName)
		
		result = []
		traversed_nodes = [fromNode] # Traversed path
		path = [] # Iteratively constructed path

		#print "Looking for %s from %s" % (toNodeName, fromNodeName)
		
		traverse(fromNode, path+[fromNode])
		
		assert len(result) > 0, "Topology: No path from %s to %s found." % (fromNodeName, toNodeName)
		
		return result

	def findMinPath(self, fromNodeName, toNodeName):
		paths = self.findPaths(fromNodeName, toNodeName)
		
		min_length = sys.maxint
		min_path = None
		
		for path in paths:
			length = len(path) 
			if length < min_length:
				min_path = path
				min_length = length
			
		assert min_path is not None, "Topology: No min path found"

		return min_path
	def lookupNeighbour(self, nodeName, dist): 
		"""
		returns all the nodes along with edges (as tuple) at specific distance dist 
		
		"""
		node = self.getNode(nodeName)
		
		newDict = {node.getName():{'N_NODE':node,'EDGE':[]}}
		d = 0
		while d<= dist: 
			d = d+1
			print newDict
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
		
	def findAllNeighbour(self, nodeName,dist): 
		'''
		returns name of all the nodes at a distance
		'''
		node = self.getNode(nodeName)
		listNode = [node]
		listNodeName = []
		d = 0 
		while d < dist: 
			d = d+1 
			temp1 = []
			for n in listNode:
				tempNodeTuple = n.getPeersTouple()
				temp = []
				for (e,v) in tempNodeTuple:
					temp.append(v)
				temp1 = temp +temp1
				listNode = temp1
		s_list = set(listNode)
		l_lsit = list(s_list)

		if node in l_lsit:
			l_lsit.remove(node)
		for x in l_lsit:
			if isinstance(x, Datacentre):
				listNodeName.append(x.getName())
		return listNodeName
				
		
	def exploreNeighbour(self, nodeName, dist):
		"""
		compute all the possible neighbour at fixed distance h
		"""
		node = self.getNode(nodeName)
		
		newDict = {node.getName():{'N_NODE':node,'EDGE':[]}}
		d = 0
		while d< dist: 
			d = d+1
			#print newDict
			print "----------"
			_temp1 = {}
			for nodeAttributes in newDict.itervalues(): 
				#print nodeAttributes
				
				#print type(nodeAttributes['N_NODE'])
				tempListTuples = nodeAttributes['N_NODE'].getPeersTouple()
				print tempListTuples
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
		print newDict
		return newDict
	
		
	def getNode(self, nodeName):
		if nodeName in self.datacentres:
			return self.datacentres[nodeName]
		elif nodeName in self.leafs:
			return self.leafs[nodeName]
		elif nodeName in self.links:
			return self.links[nodeName]
		else:
			print "Topology: %s not found" % nodeName
			raise