
# This file is to check the neighbour 
import simpy

from Resource import Resource 
from Scheduler import Scheduler 
from TopologyMaker import TopologyMaker
from Monitor import Monitor
from Workload import Workload
from Application import Application
from Application import mapUsrAppResrFunc
from Datacentre import Datacentre

applications = {"A1":Application("A1",{
                    'CPU':mapUsrAppResrFunc(1.0,1.0),
                    'STORAGE':mapUsrAppResrFunc(1.0,1.0),
                    'UPLINK_BW':mapUsrAppResrFunc(1.0,1.0),
                    'DOWNLINK_BW':mapUsrAppResrFunc(1.0,1.0) }
                                ),
                "A2":Application("A2",{
                    'CPU':mapUsrAppResrFunc(1.0,1.0),
                    'STORAGE':mapUsrAppResrFunc(1.0,1.0),
                    'UPLINK_BW':mapUsrAppResrFunc(1.0,1.0),
                    'DOWNLINK_BW':mapUsrAppResrFunc(1.0,1.0) }
                                ),
                "A3":Application("A3",{
                    'CPU':mapUsrAppResrFunc(1.0,1.0),
                    'STORAGE':mapUsrAppResrFunc(1.0,1.0),
                    'UPLINK_BW':mapUsrAppResrFunc(1.0,1.0),
                    'DOWNLINK_BW':mapUsrAppResrFunc(1.0,1.0) }
                                ),
                "A4":Application("A4",{
                    'CPU':mapUsrAppResrFunc(1.0,1.0),
                    'STORAGE':mapUsrAppResrFunc(1.0,1.0),
                    'UPLINK_BW':mapUsrAppResrFunc(1.0,1.0),
                    'DOWNLINK_BW':mapUsrAppResrFunc(1.0,1.0) }
                                ),
                "A0":Application("A5",{
                    'CPU':mapUsrAppResrFunc(1.0,1.0),
                    'STORAGE':mapUsrAppResrFunc(1.0,1.0),
                    'UPLINK_BW':mapUsrAppResrFunc(1.0,1.0),
                    'DOWNLINK_BW':mapUsrAppResrFunc(1.0,1.0) }
                                ),
                "DUMMY":Application("DUMMY",{
                    'CPU':mapUsrAppResrFunc(1.0,0.0),
                    'STORAGE':mapUsrAppResrFunc(1.0,0.0),
                    'UPLINK_BW':mapUsrAppResrFunc(1.0,0.0),
                    'DOWNLINK_BW':mapUsrAppResrFunc(1.0,0.0) }
                                )
                }

env = simpy.Environment()

#aScheduler = Scheduler() 


topologyMaker = TopologyMaker(env, None, applications)
datacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(	childStruct = [2,3,1], 
																			sizeStruct = ['S','S','S'], 
																			uplinkStruct = [100,100,100], 
																			downlinkStruct = [100,100,100], 
																			latencyStruct = [0,0,0] )
'''
for (v0,e0) in datacentres[0].getPeersTouple():
    print v.getName()
    print e.getName()
    print '---------'
    for (v1,e1) in e0.getPeersTouple():
        print v1.getName()
        print e.getName()
'''


#(env, datacentres, leafs, links9
aScheduler = Scheduler(env, datacentres, links, leafnodes) 
l0  = datacentres[0]

#print type(l0)
print l0.getName()
print "---call function---"
dictNodes = aScheduler.lookupNeighbour(l0,2)

#dNodes = aScheduler.exploreNeighbour(l0,1)
