'''
This file implements an scheduler for optimised placement algorithm 
'''
import simpy
import math
import time
import logging
import collections
import threading

import multiprocessing
from multiprocessing import Process, Queue
from Datacentre import Datacentre
from Link import Link
from Scheduler import Scheduler

class optScheduler_threaded(Scheduler):
	
	def __init__(self, env, topology):
		Scheduler.__init__(self, env, topology)
		self.max_thread_count = 8
		self.nbr_cpu = multiprocessing.cpu_count()
		print "System has %i cores" % self.nbr_cpu
		
	'''
		Descr : A generator function that does the initial placement
		Input : dictionay where key is appname and value if tuples of nodeuser
				and list of DCs where the app is to be scheduled
	'''
	def fnSchedule(self, appsNotScheduled, appPlacementRegistry):
		def threadCount(threads):
			count = 0
			for thread in threads:
				if thread.isAlive():
					count +=1
			return count
		
		t_start = time.time()
		
		appNeighborhoods = []
		appNames = []
		constellations = []
		constellationCosts = []
		
		for appName in sorted(appsNotScheduled):
			(appDemand, neighborhood) = appsNotScheduled[appName]
			appNeighborhoods.append(neighborhood)
			appNames.append(appName)

		nbrApps = len(appNames)
		assert len(appNeighborhoods) == nbrApps, "Number of neighborhoods is the same as the number of apps."
		
		resultQueue = multiprocessing.Queue()
		threads = []
		
		i = 0
		for constellation in self.getConstellation(appNeighborhoods):
			#assert len(constellation) == nbrApps, "Not all apps (%i) accounted for in constellation (%i) : %s" % (nbrApps, len(constellation), constellation)

			# Calculate cost for each constellation
			t = threading.Thread(target=self.evaluateAppPlacementCost_threaded, args=(i, appsNotScheduled, constellation, resultQueue))
			
			while threadCount(threads) >= self.max_thread_count:
				time.sleep(2)
			
			t.start()
			threads.append(t)
			# Save constellation
			constellations.append( constellation )
			i += 1

		for t in threads:
			t.join()
		
		temp_result = [resultQueue.get() for _ in xrange(len(constellations))]
		
		for (index, cost) in temp_result:
			constellationCosts.insert(index, cost)

		# Find constellation with min cost
		minIndex = constellationCosts.index(min(constellationCosts))
		proposedCost = constellationCosts[minIndex]

		if appPlacementRegistry is None or len(appPlacementRegistry) != nbrApps:
			currentCost = float('inf') 
		else:
			# Calculate cost current constellation
			sortedAppPlacementRegistry = collections.OrderedDict(sorted(appPlacementRegistry.items()))
			currentCost = self.evaluateAppPlacementCost( self.getPackagedPath(appsNotScheduled, sortedAppPlacementRegistry.values()) )

		if proposedCost < currentCost:
			print "NEW PLACEMENT: now: %f vs. before: %f ->" % (proposedCost, currentCost)
			for i in range(0, nbrApps):
				if appNames[i] not in appPlacementRegistry:
					prevDC = None
				else:
					prevDC = appPlacementRegistry[appNames[i]]
				print "%s: %s -> %s" % (appNames[i], prevDC, constellations[minIndex][i] )
				self.recordPlacement( appNames[i], constellations[minIndex][i], self.env.now )
				yield (appNames[i], constellations[minIndex][i])
		
		t_end = time.time()
		print "Evaluation took : %i ms" % (t_end-t_start)
		logging.debug("Evaluation took : %i ms" % (t_end-t_start))
		
		self.recordEvaluation(t_end-t_start, nbrApps)
		
	def getPackagedPath(self, appsNotScheduled, appDCs):
		result = []
		appNames = sorted(appsNotScheduled)
		nbrApps = len(appNames)
		
		# Generate path for each app in the constellation
		for i in range(0, nbrApps):
			appName = appNames[i]
			targetDC = appDCs[i]
			
			# Find path for each leaf dc pair
			(appDemand, neighborhood) = appsNotScheduled[appName]
			
			for leafNodeName, demand in appDemand.iteritems():
				result.append( ( self.topology.getPath( appName, leafNodeName, targetDC ), appName, demand) )
		
		return result
	
	def getConstellation(self, appNeighborhoods):
		for permutation in self.generatePermutations(appNeighborhoods, [], 0):
			yield permutation
	
	def generatePermutations(self, appNeighborhoods, combination, index):
		if index >= len(appNeighborhoods):
			yield combination
		else:
			for dcName in appNeighborhoods[index]:
				for perm in self.generatePermutations(appNeighborhoods, combination + [dcName] , index+1):
					yield perm
