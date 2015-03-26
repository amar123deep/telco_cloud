'''
This file is to check InitialPlacement 
'''
import simpy
import time
import logging

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
					'CPU':LinearAppResrFunc(1.0,1.0),
					'STORAGE':LinearAppResrFunc(1.0,1.0),
					'UPLINK_BW':LinearAppResrFunc(1.0,1.0),
					'DOWNLINK_BW':LinearAppResrFunc(1.0,1.0) }
								),
				"A1":Application("A1",{
					'CPU':LinearAppResrFunc(1.0,1.0),
					'STORAGE':LinearAppResrFunc(1.0,1.0),
					'UPLINK_BW':LinearAppResrFunc(1.0,1.0),
					'DOWNLINK_BW':LinearAppResrFunc(1.0,1.0) }
								),
				"A2":Application("A2",{
					'CPU':LinearAppResrFunc(1.0,1.0),
					'STORAGE':LinearAppResrFunc(1.0,1.0),
					'UPLINK_BW':LinearAppResrFunc(1.0,1.0),
					'DOWNLINK_BW':LinearAppResrFunc(1.0,1.0) }
								),
				"A3":Application("A3",{
					'CPU':LinearAppResrFunc(1.0,1.0),
					'STORAGE':LinearAppResrFunc(1.0,1.0),
					'UPLINK_BW':LinearAppResrFunc(1.0,1.0),
					'DOWNLINK_BW':LinearAppResrFunc(1.0,1.0) }
								),
				"A4":Application("A4",{
					'CPU':LinearAppResrFunc(1.0,1.0),
					'STORAGE':LinearAppResrFunc(1.0,1.0),
					'UPLINK_BW':LinearAppResrFunc(1.0,1.0),
					'DOWNLINK_BW':LinearAppResrFunc(1.0,1.0) }
								),
				"DUMMY":Application("DUMMY",{
					'CPU':LinearAppResrFunc(1.0,0.0),
					'STORAGE':LinearAppResrFunc(1.0,0.0),
					'UPLINK_BW':LinearAppResrFunc(1.0,0.0),
					'DOWNLINK_BW':LinearAppResrFunc(1.0,0.0) }
								)
				}

def main():
	logging.basicConfig(filename='activities.log', level=logging.DEBUG, filemode='w')
	
	logging.info("---- %s ----" % time.strftime("%d/%m/%Y - %H:%M:%S"))
	
	env = simpy.Environment()

	topologyMaker = TopologyMaker(env, None, applications)

	datacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(	childStruct = [2,3,1], 
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
	
	workload = Workload(env,'workfile.json', coordinator)
	#monitor = Monitor(env, {'BADNESS': {'FUNC': scheduler.measureBadness,'HEADER': scheduler.produceBadnessHeader, 'OUTPUT':Monitor.composeCSV}}, 5)
	
	# time_delta, topology, coordinator, inputs, outputs, filters
	monitor = SystemMonitor(env, 1, topology, coordinator, None, None, None)
	#monitor.measure()
	#workload.produceWorkload()
	
	env.process(workload.produceWorkload())
	env.process(monitor.measure())
	
	logging.info("Simulation started")
	env.run(until=workload.getWorkloadTimeSpan())
	logging.info("Simulation Done")
	
	monitor.compose()
	logging.info("Composing results")
	
	monitor.composeUtilization()
	
	print "DONE"
	
if __name__ == '__main__':
	main()