{"filter":false,"title":"testScheduler.py","tooltip":"/Simulator_Coarse/testScheduler.py","undoManager":{"mark":86,"position":86,"stack":[[{"group":"doc","deltas":[{"start":{"row":27,"column":40},"end":{"row":27,"column":41},"action":"remove","lines":["p"]}]}],[{"group":"doc","deltas":[{"start":{"row":27,"column":39},"end":{"row":27,"column":40},"action":"remove","lines":["o"]}]}],[{"group":"doc","deltas":[{"start":{"row":27,"column":38},"end":{"row":27,"column":39},"action":"remove","lines":["c"]}]}],[{"group":"doc","deltas":[{"start":{"row":27,"column":37},"end":{"row":27,"column":38},"action":"remove","lines":["."]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":19},"end":{"row":19,"column":20},"action":"remove","lines":["]"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":18},"end":{"row":19,"column":19},"action":"remove","lines":["0"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":17},"end":{"row":19,"column":18},"action":"remove","lines":[","]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":16},"end":{"row":19,"column":17},"action":"remove","lines":["0"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":15},"end":{"row":19,"column":16},"action":"remove","lines":["["]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":14},"end":{"row":19,"column":15},"action":"remove","lines":["n"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":13},"end":{"row":19,"column":14},"action":"remove","lines":["o"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":12},"end":{"row":19,"column":13},"action":"remove","lines":["i"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":11},"end":{"row":19,"column":12},"action":"remove","lines":["t"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":10},"end":{"row":19,"column":11},"action":"remove","lines":["u"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":9},"end":{"row":19,"column":10},"action":"remove","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":8},"end":{"row":19,"column":9},"action":"remove","lines":["o"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":7},"end":{"row":19,"column":8},"action":"remove","lines":["s"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":6},"end":{"row":19,"column":7},"action":"remove","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":5},"end":{"row":19,"column":6},"action":"remove","lines":["t"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":4},"end":{"row":19,"column":5},"action":"remove","lines":["n"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":3},"end":{"row":19,"column":4},"action":"remove","lines":["i"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":2},"end":{"row":19,"column":3},"action":"remove","lines":["r"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":1},"end":{"row":19,"column":2},"action":"remove","lines":["p"]}]}],[{"group":"doc","deltas":[{"start":{"row":19,"column":0},"end":{"row":19,"column":1},"action":"remove","lines":["\t"]}]}],[{"group":"doc","deltas":[{"start":{"row":18,"column":19},"end":{"row":19,"column":0},"action":"remove","lines":["",""]}]}],[{"group":"doc","deltas":[{"start":{"row":0,"column":0},"end":{"row":36,"column":0},"action":"remove","lines":["","import math ","import numpy as np","","def nchoosek(n,k):","\tf = math.factorial","\treturn f(n) / f(k) / f(n-k)","\t\t","def getSolutions(n, m):","\t'''","\tn = numApp ","\tm = maxDist","\t'''","\tk = nchoosek(n+m-1,m)","\t# print k ","\t# initialize ","\tsolution = np.zeros((n,k))","\t","\tsolution[0,0] = m ","\tfor mu in np.arange(1,k):","\t\tq = n - 2  ","\t\twhile q >= 0: ","\t\t\tprint \"q:%f, mu-1:%f\" % (q, mu-1)","\t\t\tif solution[q,mu-1] > 0: ","","\t\t\t\tsolution[0:q,mu] = solution[0:q,mu-1]","\t\t\t\tsolution[q,mu]   = solution[q,mu] - 1 ","\t\t\t\tsolution[q+1,mu] = m - sum(solution[0:q,mu])","\t\t\t\tq = -1","\t\t\telse: ","\t\t\t\tq = q-1 ","\treturn solution","\t","solutions = getSolutions(4,2) ","# print the solution","print solutions",""]}]}],[{"group":"doc","deltas":[{"start":{"row":0,"column":0},"end":{"row":116,"column":7},"action":"insert","lines":["'''","This file is to check InitialPlacement ","'''","import simpy","import time","import logging","import Filters","","from Resource import Resource ","from Scheduler import Scheduler ","from RRMinOverloadScheduler import RRMinOverloadScheduler ","from TopologyMaker import TopologyMaker","from SystemMonitor import SystemMonitor","from Workload import Workload","from Application import Application","from Application import LinearAppResrFunc","from Datacentre import Datacentre","from Coordinator import Coordinator","from Topology import Topology","from Controller import PeriodicController","","applications = {\"A0\":Application(\"A0\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A1\":Application(\"A1\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A2\":Application(\"A2\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A3\":Application(\"A3\", Application.TYPES['SYMMETRIC']),","\t\t\t\t\"A4\":Application(\"A4\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A5\":Application(\"A5\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A6\":Application(\"A6\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A7\":Application(\"A7\", Application.TYPES['SYMMETRIC']),","\t\t\t\t\"A8\":Application(\"A8\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A9\":Application(\"A9\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A10\":Application(\"A10\", Application.TYPES['SYMMETRIC']),","\t\t\t\t\"A11\":Application(\"A11\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A12\":Application(\"A12\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A13\":Application(\"A13\", Application.TYPES['SYMMETRIC']),","\t\t\t\t\"A14\":Application(\"A14\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A15\":Application(\"A15\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A16\":Application(\"A16\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A17\":Application(\"A17\", Application.TYPES['SYMMETRIC']),","\t\t\t\t\"A18\":Application(\"A18\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A19\":Application(\"A19\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A20\":Application(\"A20\", Application.TYPES['SYMMETRIC']),","\t\t\t\t\"A21\":Application(\"A21\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A22\":Application(\"A22\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A23\":Application(\"A23\", Application.TYPES['SYMMETRIC']),","\t\t\t\t\"A24\":Application(\"A24\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A25\":Application(\"A25\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A26\":Application(\"A26\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t\"A27\":Application(\"A27\", Application.TYPES['SYMMETRIC']),","\t\t\t\t\"A28\":Application(\"A28\", Application.TYPES['CPU_INTENSIVE']),","\t\t\t\t\"A29\":Application(\"A29\", Application.TYPES['NET_INTENSIVE']),","\t\t\t\t}","","workloadName = \"workfile12\"","","def main():","\tlogging.basicConfig(filename='activities.log', level=logging.DEBUG, filemode='w')","\t","\tlogging.info(\"---- %s ----\" % time.strftime(\"%d/%m/%Y - %H:%M:%S\"))","\t","\tenv = simpy.Environment()","","\ttopologyMaker = TopologyMaker(env, None, applications)","","\tdatacentres, links, leafnodes = topologyMaker.GenerateTreeFromParameters(\tchildStruct = [3,3,1], ","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tsizeStruct = [\tDatacentre.RESOURCE_TYPES['S'],","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tDatacentre.RESOURCE_TYPES['L'],","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tDatacentre.RESOURCE_TYPES['S']], ","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tuplinkStruct = [100,100,100], ","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tdownlinkStruct = [100,100,100], ","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tlatencyStruct = [0,0,0] )","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t","\tlogging.info('Topology generated, with %i datacentres' % len(datacentres))","\t","\ttopology = Topology(env, datacentres, links, leafnodes)","\t","\tscheduler = RRMinOverloadScheduler(env, topology)","\tlogging.info('%s scheduler created' % type(scheduler).__name__)","\t","\tcoordinator = Coordinator(env, topology, scheduler)","\t","\tworkload = Workload(env,'workloads/'+workloadName+'.json', coordinator)","\tmonitor = SystemMonitor(env, 1, workloadName+'_continous_1continous_1', topology, coordinator, scheduler, \t","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t[\t(\"TOTAL_OVERLOAD\", SystemMonitor.measureSystemOverloaFactor),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"COMPONENT_OVERLOAD\", SystemMonitor.measureComponentOverloadFactor),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"PLACEMENTS\", SystemMonitor.getPlacementBuffer),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"RESOURCE_UTILISATION\", SystemMonitor.measureComponentResourceUtilisation),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"APPLICATION_LATENCY\", SystemMonitor.measureApplicationLatency)], ","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t[\t(\"TOTAL_OVERLOAD\", SystemMonitor.fileCSVOutput, None),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"COMPONENT_OVERLOAD\", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"PLACEMENTS\", SystemMonitor.fileCSVOutput, SystemMonitor.composePlacementsHeader),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"RESOURCE_UTILISATION\", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"MEAN_APPLICATION_LATENCY\", SystemMonitor.fileCSVOutput, None)],","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t[\t(\"APPLICATION_LATENCY\", \"MEAN_APPLICATION_LATENCY\", Filters.MeanFilter)])","\t","\tworkload.produceWorkload()","\t","\tenv.process(workload.produceWorkload())","\tenv.process(monitor.measure())","\t","\tlogging.info(\"Contorller started\")","\tcontroller = PeriodicController(env, coordinator, 1)","\t","\tlogging.info(\"Simulation started\")","\tenv.run(until=workload.getWorkloadTimeSpan())","\tlogging.info(\"Simulation Done\")","\t","\tmonitor.compose()","\tmonitor.composeUtilization()","\tlogging.info(\"Composing results\")","\t","\tmonitor.produceOutput()","\t","\tprint \"DONE\"","\t","if __name__ == '__main__':","\tmain()"]}]}],[{"group":"doc","deltas":[{"start":{"row":74,"column":56},"end":{"row":75,"column":0},"action":"insert","lines":["",""]},{"start":{"row":75,"column":0},"end":{"row":75,"column":1},"action":"insert","lines":["\t"]}]}],[{"group":"doc","deltas":[{"start":{"row":75,"column":1},"end":{"row":76,"column":0},"action":"insert","lines":["",""]},{"start":{"row":76,"column":0},"end":{"row":76,"column":1},"action":"insert","lines":["\t"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":1},"end":{"row":77,"column":0},"action":"insert","lines":["",""]},{"start":{"row":77,"column":0},"end":{"row":77,"column":1},"action":"insert","lines":["\t"]}]}],[{"group":"doc","deltas":[{"start":{"row":79,"column":2},"end":{"row":116,"column":13},"action":"remove","lines":["cheduler = RRMinOverloadScheduler(env, topology)","\tlogging.info('%s scheduler created' % type(scheduler).__name__)","\t","\tcoordinator = Coordinator(env, topology, scheduler)","\t","\tworkload = Workload(env,'workloads/'+workloadName+'.json', coordinator)","\tmonitor = SystemMonitor(env, 1, workloadName+'_continous_1continous_1', topology, coordinator, scheduler, \t","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t[\t(\"TOTAL_OVERLOAD\", SystemMonitor.measureSystemOverloaFactor),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"COMPONENT_OVERLOAD\", SystemMonitor.measureComponentOverloadFactor),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"PLACEMENTS\", SystemMonitor.getPlacementBuffer),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"RESOURCE_UTILISATION\", SystemMonitor.measureComponentResourceUtilisation),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"APPLICATION_LATENCY\", SystemMonitor.measureApplicationLatency)], ","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t[\t(\"TOTAL_OVERLOAD\", SystemMonitor.fileCSVOutput, None),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"COMPONENT_OVERLOAD\", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"PLACEMENTS\", SystemMonitor.fileCSVOutput, SystemMonitor.composePlacementsHeader),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"RESOURCE_UTILISATION\", SystemMonitor.fileCSVOutput, SystemMonitor.composeDCLinkHeader),","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t(\"MEAN_APPLICATION_LATENCY\", SystemMonitor.fileCSVOutput, None)],","\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t[\t(\"APPLICATION_LATENCY\", \"MEAN_APPLICATION_LATENCY\", Filters.MeanFilter)])","\t","\tworkload.produceWorkload()","\t","\tenv.process(workload.produceWorkload())","\tenv.process(monitor.measure())","\t","\tlogging.info(\"Contorller started\")","\tcontroller = PeriodicController(env, coordinator, 1)","\t","\tlogging.info(\"Simulation started\")","\tenv.run(until=workload.getWorkloadTimeSpan())","\tlogging.info(\"Simulation Done\")","\t","\tmonitor.compose()","\tmonitor.composeUtilization()","\tlogging.info(\"Composing results\")","\t","\tmonitor.produceOutput()","\t","\tprint \"DONE\""]}]}],[{"group":"doc","deltas":[{"start":{"row":79,"column":1},"end":{"row":79,"column":2},"action":"remove","lines":["s"]}]}],[{"group":"doc","deltas":[{"start":{"row":75,"column":1},"end":{"row":76,"column":0},"action":"insert","lines":["",""]},{"start":{"row":76,"column":0},"end":{"row":76,"column":1},"action":"insert","lines":["\t"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":1},"end":{"row":76,"column":17},"action":"insert","lines":["exploreNeighbour"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":1},"end":{"row":76,"column":2},"action":"insert","lines":["t"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":2},"end":{"row":76,"column":3},"action":"insert","lines":["o"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":3},"end":{"row":76,"column":4},"action":"insert","lines":["p"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":4},"end":{"row":76,"column":5},"action":"insert","lines":["o"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":5},"end":{"row":76,"column":6},"action":"insert","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":6},"end":{"row":76,"column":7},"action":"insert","lines":["o"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":7},"end":{"row":76,"column":8},"action":"insert","lines":["g"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":8},"end":{"row":76,"column":9},"action":"insert","lines":["y"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":9},"end":{"row":76,"column":10},"action":"insert","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":9},"end":{"row":76,"column":10},"action":"remove","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":9},"end":{"row":76,"column":10},"action":"insert","lines":["."]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":26},"end":{"row":76,"column":27},"action":"insert","lines":["("]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":27},"end":{"row":76,"column":28},"action":"insert","lines":[")"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":10},"end":{"row":76,"column":26},"action":"remove","lines":["exploreNeighbour"]},{"start":{"row":76,"column":10},"end":{"row":76,"column":26},"action":"insert","lines":["findAllNeighbour"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":27},"end":{"row":76,"column":28},"action":"insert","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":28},"end":{"row":76,"column":29},"action":"insert","lines":[","]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":29},"end":{"row":76,"column":30},"action":"insert","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":1},"end":{"row":76,"column":2},"action":"insert","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":2},"end":{"row":76,"column":3},"action":"insert","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":3},"end":{"row":76,"column":4},"action":"insert","lines":["="]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":4},"end":{"row":76,"column":5},"action":"insert","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":35},"end":{"row":77,"column":0},"action":"insert","lines":["",""]},{"start":{"row":77,"column":0},"end":{"row":77,"column":1},"action":"insert","lines":["\t"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":1},"end":{"row":77,"column":2},"action":"insert","lines":["p"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":2},"end":{"row":77,"column":3},"action":"insert","lines":["r"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":3},"end":{"row":77,"column":4},"action":"insert","lines":["i"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":4},"end":{"row":77,"column":5},"action":"insert","lines":["n"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":5},"end":{"row":77,"column":6},"action":"insert","lines":["t"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":6},"end":{"row":77,"column":7},"action":"insert","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":7},"end":{"row":77,"column":8},"action":"insert","lines":["l"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":31},"end":{"row":76,"column":32},"action":"remove","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":31},"end":{"row":76,"column":32},"action":"insert","lines":["D"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":32},"end":{"row":76,"column":33},"action":"insert","lines":["C"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":33},"end":{"row":76,"column":34},"action":"insert","lines":["6"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":34},"end":{"row":76,"column":35},"action":"insert","lines":["'"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":31},"end":{"row":76,"column":32},"action":"insert","lines":["'"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":14},"end":{"row":76,"column":30},"action":"remove","lines":["findAllNeighbour"]},{"start":{"row":76,"column":14},"end":{"row":76,"column":30},"action":"insert","lines":["exploreNeighbour"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":14},"end":{"row":76,"column":30},"action":"remove","lines":["exploreNeighbour"]},{"start":{"row":76,"column":14},"end":{"row":76,"column":30},"action":"insert","lines":["findAllNeighbour"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":34},"end":{"row":76,"column":35},"action":"remove","lines":["6"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":34},"end":{"row":76,"column":35},"action":"insert","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"remove","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"insert","lines":["2"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"remove","lines":["2"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"insert","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"remove","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"insert","lines":["2"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"remove","lines":["2"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"insert","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"remove","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"insert","lines":["2"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"remove","lines":["2"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":37},"end":{"row":76,"column":38},"action":"insert","lines":["3"]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":38},"end":{"row":76,"column":39},"action":"insert","lines":[","]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":38},"end":{"row":76,"column":39},"action":"remove","lines":[","]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":39},"end":{"row":77,"column":0},"action":"insert","lines":["",""]},{"start":{"row":77,"column":0},"end":{"row":77,"column":1},"action":"insert","lines":["\t"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":1},"end":{"row":77,"column":2},"action":"insert","lines":["s"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":2},"end":{"row":77,"column":3},"action":"insert","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":2},"end":{"row":77,"column":3},"action":"remove","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":1},"end":{"row":77,"column":2},"action":"remove","lines":["s"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":1},"end":{"row":77,"column":2},"action":"insert","lines":["c"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":2},"end":{"row":77,"column":3},"action":"insert","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":3},"end":{"row":77,"column":4},"action":"insert","lines":["="]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":4},"end":{"row":77,"column":5},"action":"insert","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":5},"end":{"row":77,"column":6},"action":"insert","lines":["c"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":6},"end":{"row":77,"column":7},"action":"insert","lines":["o"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":7},"end":{"row":77,"column":8},"action":"insert","lines":["o"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":5},"end":{"row":77,"column":8},"action":"remove","lines":["coo"]},{"start":{"row":77,"column":5},"end":{"row":77,"column":16},"action":"insert","lines":["coordinator"]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":16},"end":{"row":77,"column":17},"action":"insert","lines":["("]}]}],[{"group":"doc","deltas":[{"start":{"row":77,"column":0},"end":{"row":77,"column":17},"action":"remove","lines":["\tc = coordinator("]}]}],[{"group":"doc","deltas":[{"start":{"row":76,"column":39},"end":{"row":77,"column":0},"action":"remove","lines":["",""]}]}]]},"ace":{"folds":[],"scrolltop":96,"scrollleft":0,"selection":{"start":{"row":77,"column":8},"end":{"row":77,"column":8},"isBackwards":false},"options":{"tabSize":4,"useSoftTabs":false,"guessTabSize":false,"useWrapMode":false,"wrapToView":true},"firstLineState":{"row":5,"state":"start","mode":"ace/mode/python"}},"timestamp":1430377941909,"hash":"f8983e04078ba8bd26bbb733f30d27dc7457cc55"}