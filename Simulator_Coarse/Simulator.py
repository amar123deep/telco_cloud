import simpy

from Monitor import Monitor
from TopologyMaker import TopologyMaker
from Workload import Workload
from Scheduler import Scheduler

SIM_DURATION = 100

applications = {}

env = simpy.Environment()

# Make topology
topologyMaker = TopologyMaker(env, None, applications)
datacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(	childStruct = [2,2,1], 
																			sizeStruct = ['S'], 
																			uplinkStruct = [1,1,1], 
																			downlinkStruct = [1,1,1], 
																			latencyStruct = [0,0,0] )

# Scheduler
scheduler = Scheduler(env, datacentres, leafnodes, links)

# Workload

workload = Workload('workfile.json', env, leafnodes, datacentres, [scheduler.notifyScheduler], applications)
workload.initWorkload()

# Run simulation
env.run(until=SIM_DURATION)