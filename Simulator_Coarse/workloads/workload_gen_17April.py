__author__ = 'amardeep'

'''
This file generates workload for each application running on a node
'''

import numpy as np
import matplotlib.pyplot as plt
import random as rnd
from mpl_toolkits.mplot3d import Axes3D
import json

file_name = 'workfile_1_a.json'

import matplotlib.animation as animation

lenNodes = 10
lenApps = 15
pAppsInit = np.sort(np.array([rnd.uniform(0.1,0.6) for x in np.arange(15)]))[::-1]
# pAppsInit = np.array([rnd.uniform(0.1,0.6) for x in np.arange(15)])

# print 'probability: ',pAppsInit
t = 25

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

def fnConstructProb(pApps, idxApp, s):
    '''
    :param pApps: Input application probability
            s   : power (mist be between 0 and 1, 1 means same popularity, 0 means close to 1)
    :return: modified application probability
    '''

    if isinstance(idxApp,int):
        pApps[idxApp] = pApps[idxApp]**s
    if isinstance(idxApp,list):
        for idx,val in enumerate(idxApp):
            pApps[val] = pApps[val]**s[idx]
    else:
        assert 'error! fnConstructProb'
    return pApps


def fnUsersPerApp(nUsers,nApps,pa=1):
    '''
    :param nUsers: number of users on that particular node
    :param nApps: total number of apps
    :param k: case : how many apps on the node should be popular
    :return arrUsers: list of users on that node
    '''
    # arrUsers = []
    pApps =  pAppsInit.copy()
    # case 1: Application m gets popular at one node
    if pa == 1:
        m = 1
        s = 0 # close to 0 means probability equal to 1
        r_pApps = fnConstructProb(pApps,m,s)
    # case 2: App 1,2,3 becomes popular
    elif pa ==2:
        m = [1,2,3]
        s = [0.2,0.1,0.4]
        r_pApps = fnConstructProb(pApps,m,s)
    else:
        assert 'error! fnUsersPerApp not correct'

    arrUsers = (nUsers*r_pApps).astype(int)
    #for nn in np.arange(nApps):
    #    rr = [rnd.random() for x in np.arange(nUsers)]
    #    arrUsers.append(len(np.where(r_pApps[nn]>rr)[0]))
    return arrUsers

# create users on each node using gaussian distribution
def fnGenerateZ(pn,pa):
    # generate demand node wise
    workload = np.zeros((lenNodes,lenApps))
    nodeList =  fnGauss(1000,100,lenNodes)
    if pn == 1:
        for idx, val in enumerate(nodeList):
            # case 1: application becomes popular on one node
            if idx ==1:
                arrUsers = fnUsersPerApp(val,lenApps,pa)
                workload[idx,:] = np.array(arrUsers)
            else:
                arrUsers = (val*pAppsInit).astype(int)
                workload[idx,:] = arrUsers
    # case 2: application 1 becomes popular on all the nodes
    elif pn == 2:
        for idx, val in enumerate(nodeList):
            arrUsers = fnUsersPerApp(val,lenApps,pa)
            workload[idx,:] = np.array(arrUsers)
    # case 3: all application have equal probability
    elif pn == 3:
        for idx, val in enumerate(nodeList):
            arrUsers = (val*pAppsInit).astype(int)
            # print "bla",val,lenApps,arrUsers
            workload[idx,:] = np.array(arrUsers)
    else:
        assert "wrong case! fnGenerateZ"
    return workload

#def fnGenerateTimeVariation(t):
# Normal
workload_s = fnGenerateZ(3,1)
# one application gets popular on one node
workload_e = fnGenerateZ(1,1)
step = (workload_e-workload_s)/(t-1)
temp = workload_s.copy()
t_workload = np.zeros((t,lenNodes,lenApps))
for i in range(t):
    t_workload[i,:,:] = temp
    temp = temp + step

# write in a Json File, time, Application, node, demand
# print t_workload
workload_dict = {}
# appList = ['A'+str(i) for i in np.arange(lenApps)]
nodeList = np.arange(lenNodes).tolist()
for i in np.arange(t):
    temp = {}
    for j in np.arange(lenApps):
        temp['A'+str(j)] = dict(zip (nodeList,t_workload[i,:,j]))
    workload_dict[i] = temp

# Convert pyhton dictionary to JSON file
data_json = json.dumps(workload_dict, sort_keys=True, indent=2)

# Wite JSON stucture to file
f = open(file_name, 'w')
f.write(data_json)



'''

# fig = plt.figure()
fig = plt.figure()
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.set_xlabel('Apps')
ax1.set_ylabel('nodes')
ax1.set_zlabel('demand')
x = np.arange(lenApps)
y = np.arange(lenNodes)
ax1.set_zlim3d(0, 1200)
ax1.set_title('Before being popular, t = 0')
X,Y = np.meshgrid(x, y)
#print workload_s
#print X.shape,Y.shape,workload_s.shape
ax1.plot_surface(X, Y, workload_s, rstride=1, cstride=1, cmap='hot')

ax2 = fig.add_subplot(1, 2, 2, projection='3d')
ax2.set_xlabel('Apps')
ax2.set_ylabel('nodes')
ax2.set_zlabel('demand')
ax2.set_zlim3d(0, 1200)
ax2.set_title('after being popular at t= 25')
x = np.arange(lenApps)
y = np.arange(lenNodes)

X,Y = np.meshgrid(x, y)
#print workload_s
#print X.shape,Y.shape,workload_s.shape
ax2.plot_surface(X, Y, workload_e, rstride=1, cstride=1, cmap='hot')



# Creating the Animation object
# ani = animation.FuncAnimation(fig, updatefig, interval=100, blit=False)
plt.show()

'''