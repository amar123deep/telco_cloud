'''
This file is to check InitialPlacement 
'''
import simpy
import time
import logging
import Filters

from Resource import Resource 
from Scheduler import Scheduler 
from RRMinOverloadScheduler import RRMinOverloadScheduler 
from TopologyMaker import TopologyMaker
from SystemMonitor import SystemMonitor
from Workload import Workload
from Application import Application
from Application import LinearAppResrFunc
from Datacentre import Datacentre
from Coordinator import Coordinator
from Topology import Topology
from Controller import PeriodicController

applications = {"A0":Application("A0", Application.TYPES['CPU_INTENSIVE']),
				"A1":Application("A1", Application.TYPES['NET_INTENSIVE']),
				"A2":Application("A2", Application.TYPES['NET_INTENSIVE']),
				"A3":Application("A3", Application.TYPES['SYMMETRIC']),
				"A4":Application("A4", Application.TYPES['NET_INTENSIVE']),
				"A5":Application("A5", Application.TYPES['CPU_INTENSIVE']),
				"A6":Application("A6", Application.TYPES['NET_INTENSIVE']),
				"A7":Application("A7", Application.TYPES['SYMMETRIC']),
				"A8":Application("A8", Application.TYPES['CPU_INTENSIVE']),
				"A9":Application("A9", Application.TYPES['NET_INTENSIVE']),
				"A10":Application("A10", Application.TYPES['SYMMETRIC']),
				"A11":Application("A11", Application.TYPES['NET_INTENSIVE']),
				"A12":Application("A12", Application.TYPES['CPU_INTENSIVE']),
				"A13":Application("A13", Application.TYPES['SYMMETRIC']),
				"A14":Application("A14", Application.TYPES['CPU_INTENSIVE']),
				"A15":Application("A15", Application.TYPES['CPU_INTENSIVE']),
				"A16":Application("A16", Application.TYPES['NET_INTENSIVE']),
				"A17":Application("A17", Application.TYPES['SYMMETRIC']),
				"A18":Application("A18", Application.TYPES['CPU_INTENSIVE']),
				"A19":Application("A19", Application.TYPES['NET_INTENSIVE']),
				"A20":Application("A20", Application.TYPES['SYMMETRIC']),
				"A21":Application("A21", Application.TYPES['NET_INTENSIVE']),
				"A22":Application("A22", Application.TYPES['NET_INTENSIVE']),
				"A23":Application("A23", Application.TYPES['SYMMETRIC']),
				"A24":Application("A24", Application.TYPES['NET_INTENSIVE']),
				"A25":Application("A25", Application.TYPES['CPU_INTENSIVE']),
				"A26":Application("A26", Application.TYPES['NET_INTENSIVE']),
				"A27":Application("A27", Application.TYPES['SYMMETRIC']),
				"A28":Application("A28", Application.TYPES['CPU_INTENSIVE']),
				"A29":Application("A29", Application.TYPES['NET_INTENSIVE']),
				}

workloadName = "workfile12"

def main():
	logging.basicConfig(filename='activities.log', level=logging.DEBUG, filemode='w')
	
	logging.info("---- %s ----" % time.strftime("%d/%m/%Y - %H:%M:%S"))
	
	env = simpy.Environment()

	topologyMaker = TopologyMaker(env, None, applications)

	datacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(	childStruct = [3,3,1], 
																				sizeStruct = [	Datacentre.RESOURCE_TYPES['S'],
																								Datacentre.RESOURCE_TYPES['L'],
																								Datacentre.RESOURCE_TYPES['S']], 
																				uplinkStruct = [100,100,100], 
																				downlinkStruct = [100,100,100], 
																				latencyStruct = [0,0,0] )
																				
	logging.info('Topology generated, with %i datacentres' % len(datacentres))
	
	topology = Topology(env, datacentres, links, leafnodes)
	
	l = topology.findNeighbours('DC1',3)
	print l
	
	
if __name__ == '__main__':
	main()