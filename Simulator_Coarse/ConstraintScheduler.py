# This class implemenmts the round robin scheduler 
import time
import simpy

from Scheduler import Scheduler
import logging

class ConstraintScheduler(Scheduler):

	def __init__(self, env, topology):
		Scheduler.__init__(self, env, topology)

	def fnSchedule(self, temp): 
		t_start = time.time()
		'''
		Descr : A generator function that does the initial placement
		Input : dictionay where key is appname and value if tuples of nodeuser
				and list of DCs where the app is to be scheduled
		'''
		logging.debug('%s - attempting to schedule %s' % (type(self).__name__, str(temp.keys())))

		for appName, (nodeUsr, DClist) in temp.iteritems():
			currentNodeList = nodeUsr.keys()
			overloadList = []
			dcPathList = {}
			for dc in DClist:
				dcName = dc.getName()
				paths = []
				_temp = {}
				for leafNodeName, demand in nodeUsr.iteritems():
					paths.append( ( self.topology.getPath( appName, leafNodeName, dcName ), appName, {'PRODUCTION':demand}) ) # [findPathsDC]
					_temp[ (appName, leafNodeName, dcName) ] = self.topology.getPath(appName, leafNodeName, dcName)
				dcPathList[dcName] = _temp
				#overload for placing the application on the DC
				overloadList.append(self.evaluateAppPlacementOverload(paths))

			minoverload = min(overloadList)

			if minoverload < float('inf'):
				ind = overloadList.index(minoverload)

				dcName = DClist[ind].getName()

				DClist[ind].registerApp(appName) # [TO-DO] This should be done by the coordinator
				self.topology.updateTable(dcPathList[ dcName ]) # Add all the paths for an application

				t_end = time.time()
				logging.debug('%s - scheduled %s in %s with overload %f, %s' % (type(self).__name__, appName, dcName, minoverload, overloadList))
				self.addMeasurement("SUCCESSFUL,%s,%s,%f,%i"%(appName, dcName, minoverload, (t_end-t_start)))

				yield (appName, {dcName:currentNodeList})
			else: 
				logging.error('%s - failed to schedule %s, DC overload %s '%(type(self).__name__, appName, str(overloadList)))
				print '%s - failed to schedule %s'%(type(self).__name__, appName)
				t_end = time.time()
				self.addMeasurement("FAILED,%s,%s,%f,%i"%(appName, "-", minoverload, (t_end-t_start)))
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