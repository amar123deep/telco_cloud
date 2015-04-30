__author__ = 'amardeep'
'''
The file generates the workload whose spike moves from one node to another in the round robin way
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


file_name = 'workfile11.json'

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

def distTotalUserAmongNodes(nbr_users,nbrNodes,mu,sigma):
    x = np.linspace(sps.norm.ppf(0.01),sps.norm.ppf(0.99), nbrNodes)
    y = np.exp(-(x-mu)**2/(2*sigma**2))/np.sqrt(2*np.pi*sigma**2)
    #x1 = ["N"+str(l) for l in range(0,nbrNodes)]
    result = y/sum(y)*nbr_users
    return result

def refineDictionary(dictApp, thrld):
    return dict((k,v) for k,v in dictApp.items() if v>=thrld)

def fnRandApp(d_in):
    """
    randomizes the application order so that not always the first application is popular
    :param d_in: The dictionary that contains the app and the corresponding number of users
    :return: returns the schuffled app in the dictionary
    """
    print d_in
    keys = d_in.keys()
    rdm1.shuffle(keys)
    return dict(zip(keys,d_in.values()))

# First distribute the demand among applications
_workload_dict = {}
# n = #Node
N = 5
# m = #Application
numApps = 15
rand1 = False
nbrUsers = 1000
nbrNodes = 9
t_inc = 24

usersPerAppDict = distTotalUserApps(numApps,nbrUsers)
timeNodeDict = {}
# print usersPerApp
k = 0
for app,usersPerApp in sorted(usersPerAppDict.iteritems(), key=lambda x: x[1],reverse=True):
    # print app,usersPerApp
    # Generate mid-day and mid-night distribution
    mu, sigma = 0, 2 # mean and standard deviation
    result = distTotalUserAmongNodes(usersPerApp,nbrNodes,mu,sigma)

    for i in range(t_inc):
        # print 't'+str(i),':',(np.roll(result,i)).astype(int)
        if i in timeNodeDict:
            timeNodeDict[i].extend([(app,(np.roll(result,i)).astype(int).tolist())])
        else:
            timeNodeDict[i] = [(app,(np.roll(result,i)).astype(int).tolist())]

    # location of the next application as it increases the counter
    k = k+1

# print timeNodeDict
newDict =  {}
alist = range(nbrNodes)
for key, value in timeNodeDict.iteritems():
    # print key,':',value
    tempDict = {}
    for (app,nList) in value:
        
        tempDict[app] = dict(zip(alist,nList))
    newDict[key] = tempDict

# Convert pyhton dictionary to JSON file
data_json = json.dumps(newDict, sort_keys=True, indent=2)

# Wite JSON stucture to file
f = open(file_name, 'w')
f.write(data_json)
f.close()
