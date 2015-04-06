'''
This file is to check InitialPlacement 
'''
import simpy
import time
import logging
import Filters

from Resource import Resource 
from Scheduler import Scheduler 
from rrScheduler import rrScheduler 
from TopologyMaker import TopologyMaker
from SystemMonitor import SystemMonitor
from Workload import Workload
from Application import Application
from Application import LinearAppResrFunc
from Datacentre import Datacentre
from Coordinator import Coordinator
from Topology import Topology

applications = {"A0":Application("A0",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.28),'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.01),'MIGRATION':None}
							}
						),
				"A1":Application("A1",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.09), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.39), 'MIGRATION':None}
							},
						),
				"A2":Application("A2",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.28),'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.01),'MIGRATION':None}
							}
						),
				"A3":Application("A3",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None}
							},
						),
				"A4":Application("A4",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.09), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.39), 'MIGRATION':None}
							},
						),
				"A5":Application("A5",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.28),'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.01),'MIGRATION':None}
							}
						),
				"A6":Application("A0",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None}
							},
						),
				"A7":Application("A1",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.28),'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.01),'MIGRATION':None}
							}
						),
				"A8":Application("A2",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.09), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.39), 'MIGRATION':None}
							},
						),
				"A9":Application("A3",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.28),'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.01),'MIGRATION':None}
							}
						),
				"A10":Application("A4",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None}
							},
						),
				"A11":Application("A5",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.28),'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.01),'MIGRATION':None}
							}
						),
				"A12":Application("A0",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None}
							},
						),
				"A13":Application("A1",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 0.09), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 0.39), 'MIGRATION':None}
							},
						),
				"A14":Application("A2",{
					'CPU': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None},
					'NET': {'PRODUCTION':LinearAppResrFunc(0.0, 1), 'MIGRATION':None}
							},
						),
				}

def main():
	logging.basicConfig(filename='activities.log', level=logging.DEBUG, filemode='w')
	
	logging.info("---- %s ----" % time.strftime("%d/%m/%Y - %H:%M:%S"))
	
	env = simpy.Environment()

	topologyMaker = TopologyMaker(env, None, applications)

	datacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(	childStruct = [3,3,1], 
																				sizeStruct = [	Datacentre.RESOURCE_TYPES['L'],
																								Datacentre.RESOURCE_TYPES['M'],
																								Datacentre.RESOURCE_TYPES['S']], 
																				uplinkStruct = [100,100,100], 
																				downlinkStruct = [100,100,100], 
																				latencyStruct = [0,0,0] )
																				
	logging.info('Topology generated, with %i datacentres' % len(datacentres))
	
	topology = Topology(env, datacentres, links, leafnodes)
	
	scheduler = rrScheduler(env,topology)
	logging.info('%s scheduler created' % type(scheduler).__name__)
	
	coordinator = Coordinator(topology, scheduler)
	
	workload = Workload(env,'workloads/workfile_single.json', coordinator)
	monitor = SystemMonitor(env, 1, topology, coordinator, scheduler, 	
															[	("TOTAL_OVERLOAD", SystemMonitor.measureSystemOverloaFactor),
																("COMPONENT_OVERLOAD", SystemMonitor.measureComponentOverloadFactor),
																("PLACEMENTS", SystemMonitor.getPlacementBuffer),
																("RESOURCE_UTILISATION", SystemMonitor.measureComponentResourceUtilisation),
																("APPLICATION_LATENCY", SystemMonitor.measureApplicationLatency)], 
															[	("TOTAL_OVERLOAD", SystemMonitor.fileCSVOutput, None),
																("COMPONENT_OVERLOAD", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),
																("PLACEMENTS", SystemMonitor.fileCSVOutput, SystemMonitor.composePlacementsHeader),
																("RESOURCE_UTILISATION", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),
																("MEAN_APPLICATION_LATENCY", SystemMonitor.fileCSVOutput, None)],
															[	("APPLICATION_LATENCY", "MEAN_APPLICATION_LATENCY", Filters.MeanFilter)])
	
	workload.produceWorkload()
	
	env.process(workload.produceWorkload())
	env.process(monitor.measure())
	
	logging.info("Simulation started")
	env.run(until=workload.getWorkloadTimeSpan())
	logging.info("Simulation Done")
	
	monitor.compose()
	monitor.composeUtilization()
	logging.info("Composing results")
	
	monitor.produceOutput()
	
	print "DONE"
	
if __name__ == '__main__':
	main()