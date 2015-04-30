
__author__ = 'amardeep'

'''
This file generates workload for each application running on a node
'''

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
from mpl_toolkits.mplot3d import Axes3D
import json
import matplotlib.animation as animation


lenNodes = 6
lenApps = 5
pAppsInit = np.sort(np.array([rnd.uniform(0.1,0.6) for x in np.arange(lenApps)]))[::-1]
# pAppsInit = np.array([rnd.uniform(0.1,0.6) for x in np.arange(15)])

# print 'probability: ',pAppsInit


def fnGauss(mu,sigma,lenNodes = 15):
    '''
    distribute a number among nodes on uniform distribution
    :param mu:
    :param sigma:
    :param lenNodes:
    :return:
    '''
    nodes = []
    while len(nodes) < lenNodes:
        value = rnd.gauss(mu, sigma)
        if mu-sigma < value < mu+sigma:
            nodes.append(int(value))
    return nodes

def fnConstructProb(idxApp, s, pApps):
    '''
    :param pApps: Input application probability
            s   : power (mist be between 0 and 1, 1 means same popularity, 0 means close to 1)
    :return: modified application probability
    '''

    if isinstance(idxApp,int):
        pApps[idxApp] = pApps[idxApp]**s
    else:
        assert 'error! fnConstructProb'
    return pApps


def fnUsersPerApp(nUsers,pa,pApps):
    '''
    :param nUsers: number of users on that particular node
    :param nApps: total number of apps
    :param pa: list of apps on the node that will be popular
    :return arrUsers: list of users on that node
    '''
    # arrUsers = []
    pApps =  pApps.copy()

    # case 1: Application m gets popular at one node
    for (idxApp,s) in pa:
        r_pApps = fnConstructProb(idxApp,s,pApps)

    arrUsers = (nUsers*r_pApps).astype(int)
    #for nn in np.arange(nApps):
    #    rr = [rnd.random() for x in np.arange(nUsers)]
    #    arrUsers.append(len(np.where(r_pApps[nn]>rr)[0]))
    return arrUsers

# create users on each node using gaussian distribution
def fnGenerateZ(pn,pa):
    '''
    generate demand node wise
    :param pn: node list where spike appear
    :param pa: for each node corresponding list of tuple of (app,spike coeff)
    :return:
    '''
    workload = np.zeros((lenNodes,lenApps))
    nodeList =  fnGauss(1000,100,lenNodes)
    for idx, val in enumerate(nodeList):
        if isinstance(pn,list):
            pApps = np.array([rnd.uniform(0.1,0.3) for x in np.arange(lenApps)])
            #pApps = pAppsInit.copy()

            if idx in pn:
                arrUsers = fnUsersPerApp(val,pa[pn.index(idx)],pApps)
                workload[idx,:] = np.array(arrUsers)
            else:
                arrUsers = (val*pApps).astype(int)
                workload[idx,:] = arrUsers
        else:
            arrUsers = (val*pAppsInit).astype(int)
            workload[idx,:] = arrUsers
    return workload

#def fnGenerateTimeVariation(t):
# Normal
workload_s = fnGenerateZ(1,1)
# print "progress"
# workload_s = fnGenerateZ([4,14],[[(2,0.5),(5,0.3)],[(5,0.5)]])
# one application gets popular on one node
workload_e = fnGenerateZ(2,1)

#nodeL = [2,3,4, 12,13,14]
#appL_pk = [[(10,0.2)],[(10,0.1)],[(10,0.3)],[(25,0.3)],[(10,0.1)],[(10,0.2)]]
#appL_afp = [[(10,0.5)],[(10,0.6)],[(10,0.7)],[(25,0.8)],[(10,0.4)],[(10,0.5)]]
#workload_e = fnGenerateZ([2,3,4, 12,13,14],[[(10,0.2)],[(10,0.1)],[(10,0.5)],[(10,0.3)],[(10,0.1)],[(10,0.1)]])
#workload_pk = fnGenerateZ( nodeL , appL_pk)
#workload_afp = fnGenerateZ( nodeL , appL_afp)

alpha = 0.05
t = 25

step = (workload_e-workload_s)/(t-1)
temp = workload_s.copy()

t_workload = np.zeros((t,lenNodes,lenApps))

for i in range(t):
    # t_workload[t_big+i,:,:] = temp
    t_workload[i,:,:] = np.multiply((1-alpha+2*alpha*np.random.random((lenNodes,lenApps))),temp)
    temp = temp + step


def fnRand(arrLen,workload):
    temp_workload = np.zeros((arrLen,lenNodes,lenApps))
    for i in np.arange(arrLen):
        temp_workload[i,:,:] = np.multiply((1-alpha+2*alpha*np.random.random((lenNodes,lenApps))),workload)
    return temp_workload



# write in a Json File, time, Application, node, demand
# print t_workload
workload_dict = {}
# appList = ['A'+str(i) for i in np.arange(lenApps)]
nodeList = np.arange(lenNodes).tolist()
for i in np.arange(t):
    temp = {}
    for j in np.arange(lenApps):
        temp1 = {}
        for k in np.arange(lenNodes):
            temp1[k] = {'PRODUCTION':t_workload[i,k,j]}
        #temp['A'+str(j)] = dict(zip (nodeList,dict(zip(lenNodes*['PRODUCTION'],t_workload[i,:,j]))))
        temp['A'+str(j)] = temp1
    workload_dict[i] = temp

# Convert pyhton dictionary to JSON file
data_json = json.dumps(workload_dict, sort_keys=True, indent=2)

file_name = 'workload_v1_'+str(lenNodes)+'_a'+str(lenApps)+'_case'+str(5)+'.json'
# Wite JSON stucture to file
f = open(file_name, 'w')
f.write(data_json)
