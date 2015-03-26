# here we test the badness for a specific node
# Input is the resources used in that specific node 

import simpy

from Monitor import Monitor
from TopologyMaker import TopologyMaker
from Workload import Workload
from Scheduler import Scheduler
from Application import Application
from Application import mapUsrAppResrFunc
from Datacentre import Datacentre

SIM_DURATION = 65

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

# Make topology
topologyMaker = TopologyMaker(env, None, applications)
datacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(	childStruct = [1], 
																			sizeStruct = ['S'], 
																			uplinkStruct = [100], 
																			downlinkStruct = [100], 
																			latencyStruct = [0] )

# Scheduler
scheduler = Scheduler(env, datacentres, leafnodes, links)

# Place applications - Temporary
for app in applications:
    datacentres[0].registerApp(app)

# Monitor instance
monitor = Monitor(env, {'BADNESS':{'FUNC': datacentres[0].getBadness, 'FILE_NAME':'badness.txt'}}, 5)

# Workload
# craete an instance of the root node and place the application there 
workload = Workload('workfile.json', env, leafnodes, datacentres, [scheduler.notifyScheduler], applications)
workload.initWorkload()

# Initial placement
#scheduler.initPlacement()

# Run simulation
env.run(until=workload.getWorkloadTimeSpan())

# Print results
monitor.composeResults()

print "DONE"
