# This class implemenmts the round robin scheduler 
import time
import simpy

from Scheduler import Scheduler
import logging

class RRMinOverloadScheduler(Scheduler):
		
	def __init__(self, env, topology):
		Scheduler.__init__(self, env, topology)

	def fnSchedule(self, data): 
		t_start = time.time()

		'''
		Descr : A generator function that does the initial placement
		Input : dictionay where key is appname and value if tuples of nodeuser
				and list of DCs where the app is to be scheduled
		'''
		logging.debug('%s - atdatating to schedule %s' % (type(self).__name__, str(data.keys())))
		
		for appName, (nodeUsr, DClist) in data.iteritems():
			currentNodeList = nodeUsr.keys()
			overloadList = []
			dcPathList = {}
			for dc in DClist:
				dcName = dc.getName()
				paths = []
				_data = {}
				for leafNodeName, demand in nodeUsr.iteritems():
					paths.append( ( self.topology.getPath( appName, leafNodeName, dcName ), appName, {'PRODUCTION':demand}) ) # [findPathsDC]
					_data[ (appName, leafNodeName, dcName) ] = self.topology.getPath(appName, leafNodeName, dcName)
				dcPathList[dcName] = _data
				#overload for placing the application on the DC
				overloadList.append(self.evaluateAppPlacementOverload(paths))
			
			minoverload = min(overloadList)

			(currentDCName, prevOverload) = self.getPlacementHistory(appName)

			currentPlacementOverload = float('inf')
				
			if currentDCName is not None:
				for leafNodeName, demand in nodeUsr.iteritems():
					paths.append( ( self.topology.getPath( appName, leafNodeName, currentDCName ), appName, {'PRODUCTION':demand}) ) # [findPathsDC]
		
				currentPlacementOverload = self.evaluateAppPlacementOverload(paths)

			#print "%s is currently placed in %s with incurred overhead %f proposed overhead" % (appName, currentDCName, currentPlacementOverload)

			if minoverload < currentPlacementOverload:
				print "%s - curr: %f , new: %f , delta: %f" % (appName, currentPlacementOverload, minoverload, currentPlacementOverload-minoverload)
				ind = overloadList.index(minoverload)

				dcName = DClist[ind].getName() 

				DClist[ind].registerApp(appName) # [TO-DO] This should be done by the coordinator
				self.topology.updateTable(dcPathList[ dcName ]) # Add all the paths for an application

				t_end = time.time()
				logging.debug('%s - scheduled %s in %s with overload %f previous overload %f, %s' % (type(self).__name__, appName, dcName, minoverload, prevOverload, overloadList))
				self.addMeasurement("SUCCESSFUL,%s,%s,%f,%i"%(appName, dcName, minoverload, (t_end-t_start)))
				
				self.recordPlacement(appName, dcName, minoverload)
				
				yield (appName, {dcName:currentNodeList})
			else: 
				logging.error('%s - failed to schedule %s, DC overload %s '%(type(self).__name__, appName, str(overloadList)))
				print '%s - failed to schedule %s'%(type(self).__name__, appName)
				t_end = time.time()
				self.addMeasurement("FAILED,%s,%s,%f,%i"%(appName, "-", minoverload, (t_end-t_start)))
				yield (appName, {})
				
		
		'''
		bigDict = {} 
		for appName, (nodeUsr,DClist) in data.items():
			
			paths = {}

			for dc in DClist:
				for leafNode, Usr in nodeUsr:
					paths[(leafNode,dc)]= (self.topology.findPathsDC(leafNode,dc),Usr) # [findPathsDC]
					#allPaths[(leafNode,dc)] = (_dataPath,Usr)
			
			bigDict[appName] = paths
		return self.evaluatePath(bigDict)	
		
		
		#yield self.bestPathApp(appName,allPaths)
		'''