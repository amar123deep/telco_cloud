__author__ = 'amardeep'
'''
The file generates the workload whose spike moves only to the nodes closer by and becomes popular among bunch of nodes
'''

from numpy import *

import numpy as np
#import matplotlib.axes3d as p3
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
import scipy.stats as sps
import scipy.special as sp
import random as rdm1
import json

file_name = 'workfile12.json'

def distTotalUserApps(nbr_apps,nbr_users,rand1 = False):
    a = 0.83 # parameter 0.83 to 0.83
    x = arange(1, nbr_apps+1)
    y = x**(-a)/sp.zetac(a)
    x1 = ["A"+str(l) for l in range(0,nbr_apps)]
    result = y/sum(y)*nbr_users
    _result_dict_app = dict(zip(x1,result.astype(np.int64)))
    if rand1:
        return fnRandApp(_result_dict_app)
    else:
        return _result_dict_app

def distTotalUserAmongNodes(nbr_users,nbrNodes,mu,sigma,rand2 = False):
    x = np.linspace(sps.norm.ppf(0.01),sps.norm.ppf(0.99), nbrNodes)
    y = np.exp(-(x-mu)**2/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)
    # x1 = ["N"+str(l) for l in range(0,nbrNodes)]
    result = y/sum(y)*nbr_users
    if rand2:
        return fnRandApp(dict(zip(np.arange(nbrNodes),result.astype(int))))
    else:
        return dict(zip(np.arange(nbrNodes),result.astype(int)))

def refineDictionary(dictApp, thrld):
    return dict((k,v) for k,v in dictApp.items() if v>=thrld)

def fnRandApp(d_in):
    """
    randomizes the application order so that not always the first application is popular
    :param d_in: The dictionary that contains the app and the corresponding number of users
    :return: returns the schuffled app in the dictionary
    """
    # print d_in
    keys = d_in.keys()
    rdm1.shuffle(keys)
    return dict(zip(keys,d_in.values()))


# First distribute the demand among applications
_workload_dict = {}
numApps = 15
rand1 = False
nbrNodes = 9
totalNbrUsers = 1000
T = 24
t = np.arange(T)
y = totalNbrUsers*(1+np.sin(2*t*np.pi/T))
t1 = np.arange(2*T)
y1 = np.tile(y.astype(int),2)
# print len(t1),len(y1)

for (tim,val) in zip(t1,y1):
    # distribute requests at that time instant among Apps
    usersPerAppDict = distTotalUserApps(numApps,val,True)
    appNodeDict = {}
    # print usersPerApp
    for app,usersPerApp in sorted(usersPerAppDict.iteritems(), key=lambda x: x[1],reverse=True):
        # print app,usersPerApp
        # Generate mid-day and mid-night distribution
        mu, sigma = 0, 2 # mean and standard deviation
        appNodeDict[app] = distTotalUserAmongNodes(usersPerApp,nbrNodes,mu,sigma,True)
    _workload_dict[tim] = appNodeDict


# Convert pyhton dictionary to JSON file
data_json = json.dumps(_workload_dict, sort_keys=True, indent=2)

# Wite JSON stucture to file
f = open(file_name, 'w')
f.write(data_json)
f.close()

# Plot the data



'''
x = np.linspace(0, 1, nbrNodes)
y = np.sin(x)

# You probably won't need this if you're embedding things in a tkinter plot...
plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x, y, 'r-') # Returns a tuple of line objects, thus the comma

for phase in np.linspace(0, 10*np.pi, 500):
    line1.set_ydata(np.sin(x + phase))
    fig.canvas.draw()
'''