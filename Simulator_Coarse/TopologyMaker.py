import json

from Datacentre import Datacentre
from Link import Link
from Leaf import Leaf 

class TopologyMaker(object):

	def __init__(self, env, scheduler, applications):
		self.env = env
		self.scheduler = scheduler
		self.applications = applications

	# From JSON
	def GenerateFromJSON(self, file):
		raise NotImplementedError
	
	# From BRITE
	def GenerateFromBRITE(self, file):
		raise NotImplementedError
	
	# From parameters
	def GenerateTreeFromParameters(self, childStruct, sizeStruct, uplinkStruct, downlinkStruct, latencyStruct): 
		# Redursive method to add children
		def addChild(parent, depth):
			if(depth < DEPTH):
				print "%s () [%s]" % ('\t'*depth,'DC'+str(len(datacentres)))
				child = Datacentre('DC'+str(len(datacentres)), self.env, sizeStruct[depth], self.applications)
				datacentres[child.getName()] = child
				
				for childNbr in range(childStruct[depth]):
					addChild(child, depth+1)

			else:
				child = Leaf(str(len(leafs)), self.env) # Change workload to LEAF#
				leafs[child.getName()] = child
				print "%s X [%s]" % ('\t'*depth, child.getName())

			link = Link('LINK'+str(len(links)), self.env, Link.RESOURCE_TYPES['M'], 100, self.applications)
			links[link.getName()] = link
			link.addPeer(child)
			link.addPeer(parent)
			
			parent.addPeer(link)
			child.addPeer(link)

		print '-- Generating topology --'

		DEPTH = len(childStruct)
		
		datacentres = {}
		links = {}
		leafs = {}

		root = Datacentre('DC'+str(len(datacentres)), self.env, Datacentre.RESOURCE_TYPES['L'], self.applications)
		datacentres[root.getName()] = root
		
		print "() [%s]" % ('DC0')
		
		for childNbr in range(childStruct[0]):
			addChild(root, 1)

		print '-------------------------'
		
		return (datacentres, links, leafs)