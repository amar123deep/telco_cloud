'''
This file is to check InitialPlacement 
'''
import simpy
import time
import logging
import Filters
import random

from Resource import Resource 
from Scheduler import Scheduler 
from optScheduler import optScheduler 
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
	workloadName = "workload_v1_6_a10_case5"
	nbrApps = 15

	logging.basicConfig(filename='activities.log', level=logging.DEBUG, filemode='w')
	logging.info("---- %s ----" % time.strftime("%d/%m/%Y - %H:%M:%S"))
	
	applications = {}
	applicationTypes = Application.TYPES.keys()
	for i in range(0, nbrApps-1):
		applications.update({'A%i'%i : Application('A%i'%i, Application.TYPES[random.choice(applicationTypes)])})

	env = simpy.Environment()

	topologyMaker = TopologyMaker(env, None, applications)

	datacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(	childStruct 	= [3,2,1], 
																				sizeStruct 		= [	Datacentre.RESOURCE_TYPES['L'],
																									Datacentre.RESOURCE_TYPES['M'],
																									Datacentre.RESOURCE_TYPES['S']], 
																				uplinkStruct 	= [100,100,100], 
																				downlinkStruct 	= [100,100,100], 
																				latencyStruct 	= [0,0,0] )
																				
	logging.info('Topology generated, with %i datacentres' % len(datacentres))
	
	topology = Topology(env, datacentres, links, leafnodes)
	

	scheduler = optScheduler(env, topology)
	logging.info('%s scheduler created' % type(scheduler).__name__)
	

		
	coordinator = Coordinator(env, topology, scheduler)
	

	workload = Workload(env,'workloads/'+workloadName+'.json', coordinator)
	monitor = SystemMonitor(env, 1, workloadName+'_continous_2', topology, coordinator, scheduler, 	
															[	("TOTAL_OVERLOAD", SystemMonitor.measureSystemOverloaFactor),
																("COMPONENT_OVERLOAD", SystemMonitor.measureComponentOverloadFactor),
																("RESOURCE_UTILISATION", SystemMonitor.measureComponentResourceUtilisation),
															], 
															[	("TOTAL_OVERLOAD", SystemMonitor.fileCSVOutput, None),
																("COMPONENT_OVERLOAD", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),
																("RESOURCE_UTILISATION", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),],
															[])
	
	#workload.produceWorkload()
	env.process(workload.produceWorkload())
	env.process(monitor.measure())
	
	logging.info("Contorller started")
	controller = PeriodicController(env, coordinator, 2, 0.1)
	
	logging.info("Simulation started")
	env.run(until=workload.getWorkloadTimeSpan())
	logging.info("Simulation Done")
	
	monitor.compose()
	logging.info("Composing results")
	
	monitor.produceOutput()
	#scheduler.output( "PLACEMENT" )
	
	print "DONE"
	
if __name__ == '__main__':
	main()