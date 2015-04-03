__author__ = 'amardeep'

from numpy import *

import numpy as np
#import matplotlib.axes3d as p3
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
import scipy.special as sps
import random as rdm1

from pylab import *
# u and v are parametric variables.
# u is an array from 0 to 2*pi, with 100 elements


import json

file_name = 'workfile.json'


# n = #Node
N = 5
# m = #Application
M = 4
# t = time
T= 60*24
# Total users
nbr_users = [100,110,120,130,140,150,160,170,180,190,200,210]

# Maybe we should pass the differntiable parameters
def distTotalUserApps(nbr_apps,nbr_users,rand1= False):
    """
    Input:
    """
    a = 2. # parameter
    x = arange(1, nbr_apps+1)
    y = x**(-a)/sps.zetac(a)
    x1 = ["A"+str(l) for l in range(0,nbr_apps)]
    result = y/sum(y)*nbr_users
    _result_dict_app = dict(zip(x1,result.astype(np.int64)))
    # print sum(result)

    if rand1:
        return fnRandApp(_result_dict_app)
    else:
        return _result_dict_app

def distUsersNodes(usersPerApp, dist, nbr_leafs):
    x = arange(1, nbr_leafs+1)
    x1 = [l for l in range(0,nbr_leafs)]
    if (dist=="Uniform"):
        mu = usersPerApp
        sigma = 0.1
        result = np.random.normal(mu,sigma,nbr_leafs)
        _result_dict_node = refineDictionary(dict(zip(x1,result.astype(np.int64))),5)
    elif(dist=="Zeta"):
        a = 2. # parameter
        y= x**(-a)/sps.zetac(a)
        result = y/sum(y)*usersPerApp
        _result_dict_node = refineDictionary(dict(zip(x1,result.astype(np.int64))),5)
    else:
        print "Put correct distribution function"
        return
    return _result_dict_node

"""
Remove applications that have 0 users or lets say bellow some threshold
"""
def refineDictionary(dictApp, thrld):
    return dict((k,v) for k,v in dictApp.items() if v>=thrld)

def initialNormalDistr(nbr_leafs, nbr_users, mu=0, sigma=0.1):
    s = norm(mu, sigma, nbr_leafs)
    x = arange(1,nbr_leafs)

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


# save all the data in dictionary, create a list of time instant
interval = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
# write what distribution you want at that specific time instant for (application,node)
# event = [("Zeta","Uniform"),("Zeta","Zeta"),("Zeta","Uniform"),("Zeta","Zeta")]
event = ["Zeta","Uniform","Zeta","Uniform","Zeta","Uniform","Zeta","Uniform","Zeta","Uniform","Zeta","Uniform"]

# generate the workload for the testing scenarios
# Scenarios: Application 1 is popular among all, 
_workload_dict = {}

for (i,j,k) in zip(interval,event,nbr_users):

    # we include also the initial distribution later on

    # distribute total users among the applications based on zipf, return is a dictionary
    # Pass True in case you wanna randomize the appliocation order
    rand1 = True
    usersPerApp = distTotalUserApps(M,k,rand1)
    _temp_dict =  {}
    for x in usersPerApp:
        # print x, usersPerApp[x]
        # distribute users per application among the node
        _temp = distUsersNodes(usersPerApp[x],j,N)
        if _temp:
            _temp_dict[x] =_temp
    if _temp_dict:
        _workload_dict[i] = _temp_dict

# Convert pyhton dictionary to JSON file
data_json = json.dumps(_workload_dict, sort_keys=True, indent=2)

# Wite JSON stucture to file
f = open(file_name, 'w')
f.write(data_json)
f.close()


    # users = []
    # for m in range(M): #
    #    users.append(distUsersNodes(usersPerApp[m],"Uniform",N))
    # Z = asarray(users).transpose()
    # print 'z:',type(Z),Z.shape, Z.dtype,Z

    # _workload_dict[x] =



# x = arange(1,M+1,1)
# y = arange(1,N+1,1)
# X, Y = meshgrid(x, y)

# fig = plt.figure(figsize=(14,6))

# `ax` is a 3D-aware axis instance because of the projection='3d' keyword argument to add_subplot
# ax = fig.add_subplot(1, 2, 1, projection='3d')

# p = ax.plot_surface(X, Y, Z, rstride=4, cstride=4, linewidth=0)

# surface_plot with color grading and color bar
# ax = fig.add_subplot(1, 2, 2, projection='3d')
# p = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
# cb = fig.colorbar(p, shrink=0.5)
# plt.show()