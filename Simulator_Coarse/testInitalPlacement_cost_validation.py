'''
This file is to check InitialPlacement 
'''
import simpy
import time
import logging
import random
import copy_reg

from Datacentre import LinearCostFunc, NoCostFunc
from Resource import Resource 
from Scheduler import Scheduler 
from optScheduler import optScheduler 
from optScheduler_threaded import optScheduler_threaded
from TopologyMaker import TopologyMaker
from SystemMonitor import SystemMonitor
from Workload import Workload
from Application import Application
from Application import LinearAppResrFunc
from Datacentre import Datacentre
from Coordinator import Coordinator
from Topology import Topology
from Controller import PeriodicController

def main():
	# Data centre sizes
	MY_RESOURCE_TYPES = {
		"L":{ 
				"CPU":		{'CAPACITY':100.0, 'EXECOST': LinearCostFunc(1.0,0.0),'OVERLOADCOST': NoCostFunc(),'MU':1},
				"NET_UP":	{'CAPACITY':100.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': NoCostFunc(),'MU':1},
				"NET_DOWN":	{'CAPACITY':100.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': NoCostFunc(),'MU':1}
			},
		"M":{ 
				"CPU":		{'CAPACITY':50.0, 'EXECOST': LinearCostFunc(1.0,0.0),'OVERLOADCOST': NoCostFunc(),'MU':1},
				"NET_UP":	{'CAPACITY':50.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST':NoCostFunc(),'MU':1},
				"NET_DOWN":	{'CAPACITY':50.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': NoCostFunc(),'MU':1}
			},
		"S":{ 
				"CPU":		{'CAPACITY':10.0, 'EXECOST': LinearCostFunc(1.0,0.0),'OVERLOADCOST': NoCostFunc(),'MU':1},
				"NET_UP":	{'CAPACITY':10.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': NoCostFunc(),'MU':1},
				"NET_DOWN":	{'CAPACITY':10.0, 'EXECOST': NoCostFunc(),'OVERLOADCOST': NoCostFunc(),'MU':1}
			}
		}
	
	#workloadName = "workload_v1_6_a5mini_1may"
	workloadName = "workfile_tripple_production"
	nbrApps = 5
	depth = 4
	mode = "_continuous"
	testCase  = "_cost_ver"

	logging.basicConfig(filename='activities.log', level=logging.DEBUG, filemode='w')
	logging.info("---- %s ----" % time.strftime("%d/%m/%Y - %H:%M:%S"))
	
	applications = {}
	applicationTypes = Application.TYPES.keys()
	for i in range(0, nbrApps):
		#applications.update({'A%i'%i : Application('A%i'%i, Application.TYPES[random.choice(applicationTypes)])})
		applications.update({'A%i'%i : Application('A%i'%i, Application.TYPES['SYMMETRIC'])})

	env = simpy.Environment()

	topologyMaker = TopologyMaker(env, None, applications)

	datacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(	childStruct 	= [2, 2, 1], 
																				sizeStruct 		= [	MY_RESOURCE_TYPES['L'],
																									MY_RESOURCE_TYPES['M'],
																									MY_RESOURCE_TYPES['S'] ], 
																				uplinkStruct 	= [10000,1000,1000], 
																				downlinkStruct 	= [10000,1000,1000], 
																				latencyStruct 	= [1,1,1] )
																				
	logging.info('Topology generated, with %i datacentres' % len(datacentres))
	
	topology = Topology(env, datacentres, links, leafnodes)
	
	scheduler = optScheduler(env, topology, applications)
	logging.info('%s scheduler created' % type(scheduler).__name__)
	
	coordinator = Coordinator(env, topology, scheduler, depth)
	
	workload = Workload(env,'workloads/'+workloadName+'.json', coordinator)
	monitor = SystemMonitor(env, 1, 0.2, workloadName+mode+testCase, topology, coordinator, scheduler, 	
															[	("TOTAL_OVERLOAD", SystemMonitor.measureSystemOverloaFactor),
																("COMPONENT_OVERLOAD", SystemMonitor.measureComponentOverloadFactor),
																("RESOURCE_UTILISATION", SystemMonitor.measureComponentResourceUtilisation),
																("APP_RESOURCE_UTILISATION", SystemMonitor.measureUtilisationPerApp),
															], 
															[	("TOTAL_OVERLOAD", SystemMonitor.fileCSVOutput, None),
																("COMPONENT_OVERLOAD", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),
																("RESOURCE_UTILISATION", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),
																("APP_RESOURCE_UTILISATION", SystemMonitor.fileCSVOutput, None),
															],
															[])
	
	#workload.produceWorkload()
	env.process(workload.produceWorkload())
	env.process(monitor.measure())
	
	logging.info("Controller started")
	controller = PeriodicController(env, coordinator, 1, 0.1)
	
	logging.info("Simulation started")
	env.run(until=workload.getWorkloadTimeSpan())
	logging.info("Simulation Done")
	
	monitor.compose()
	logging.info("Composing results")
	
	monitor.produceOutput()
	scheduler.output(workloadName+mode+testCase)
	
	print "DONE"
	
if __name__ == '__main__':
	main()
	