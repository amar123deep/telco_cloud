# This class implemenmts the round robin scheduler 

import simpy

from Scheduler import Scheduler
import logging

class rrScheduler(Scheduler):
		
	def __init__(self, env, topology):
		Scheduler.__init__(self, env, topology)

	def fnSchedule(self,temp): 
		
		'''
		Descr : A generator function that does the initial placement
		Input : dictionay where key is appname and value if tuples of nodeuser
				and list of DCs where the app is to be scheduled
		'''
		logging.debug('%s - attempting to schedule %s' % (type(self).__name__, str(temp.keys())))
		
		for appName, (nodeUsr,DClist) in temp.iteritems():
			currentNodeList = nodeUsr.keys()
			badnessList = []
			dcPathList = {}
			for dc in DClist:
				dcName = dc.getName()
				paths = []
				_temp = {}
				for leafNodeName, nbrUsers in nodeUsr.iteritems():
					paths.append( ( self.topology.getPath( appName, leafNodeName, dcName ), appName, nbrUsers ) ) # [findPathsDC]
					_temp[ (appName, leafNodeName, dcName) ] = self.topology.getPath(appName, leafNodeName, dcName)
				dcPathList[dcName] = _temp
				#badness for placing the application on the DC
				badnessList.append(self.evaluateAppPlacementBadness(paths))
			
			minBadness = min(badnessList)

			if minBadness < float('inf'):
				ind = badnessList.index(minBadness)
							
				dcName = DClist[ind].getName()
				
				logging.debug('%s - scheduled %s in %s with badness %f' % (type(self).__name__, appName, dcName, minBadness))
				
				DClist[ind].registerApp(appName)
				self.topology.updateTable(dcPathList[ dcName ]) #[Add all the paths for an application ]
				
				yield (appName, {dcName:currentNodeList})
			else: 
				logging.error('%s - failed to schedule %s, DC badness %s '%(type(self).__name__, appName, str(badnessList)))
				yield (appName, {})
				
		
		'''
		bigDict = {} 
		for appName, (nodeUsr,DClist) in temp.items():
			
			paths = {}

			for dc in DClist:
				for leafNode, Usr in nodeUsr:
					paths[(leafNode,dc)]= (self.topology.findPathsDC(leafNode,dc),Usr) # [findPathsDC]
					#allPaths[(leafNode,dc)] = (_tempPath,Usr)
			
			bigDict[appName] = paths
		return self.evaluatePath(bigDict)	
		
		
		#yield self.bestPathApp(appName,allPaths)
		'''