import simpy

from Scheduler import Scheduler
from Datacentre import Datacentre
from Link import Link

class DumbScheduler(Scheduler):
	
	def __init__(self, env, datacentres, leafs, links):
		Scheduler.__init__(self, env, datacentres, leafs, links)
		pass

	# Find paths to nearest available node
	def findFirstAvailableDC(self, targetLeaf, appName, nbrUsers): # Caution! Only for trees
		"""
		Descr  :    Find the paths to the nearest resource that can host application 'app'
		Input  :    leaf - The leafnode from which the search will originate from, actual node
					app - A struct with app name as key and number of users as value
		Output :    Paths of first placement options.
		"""
		def available(resAvailability):
			result = True
			for availability in resAvailability.itervalues():
				result *= availability
			return result
			
		def traverse(node, path, appName, nbrUsers, placementOptions):
			isAvailable = available(node.willAppFit({appName: nbrUsers['TOTAL']}))

			if type(node) is Datacentre:
				if isAvailable:
					placementOptions.append(node)
					return

			elif type(node) is Link:
				if not isAvailable:
					return
			
			peers = node.getPeers()
			
			for peer in peers.itervalues():
				if peer not in path: # [William] Not correct should be for all nodes or DCs
					traverse(peer, path + [peer], appName, nbrUsers, placementOptions)

		nodes = {}
	  
		placementOptions = [] # Possible places to host app
		path = [] # Iteratively constructed path
		
		traverse(targetLeaf, path+[self], appName, nbrUsers, placementOptions)

		return placementOptions

	def initPlacement(self):
		for leaf in self.leafs.itervalues():
			subscribers =  leaf.getSubscribers()
			#print "Leaf %s has the following apps : %s" % (leaf.getName(), str(subscribers.keys())) 
			for appName, nbrAppSubscribers in subscribers.iteritems():
				placementOptions = self.findFirstAvailableDC(leaf, appName, nbrAppSubscribers)
				
				assert (len(placementOptions) > 0),"No placement options found for %s from %s" % (appName, leaf.getName())

				placementOptions[0].registerApp(appName)