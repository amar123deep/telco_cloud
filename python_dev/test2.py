__author__ = 'amardeep'


from numpy import *

import numpy as np
#import matplotlib.axes3d as p3
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.pyplot as plt
import scipy.special as sps

from pylab import *
# u and v are parametric variables.
# u is an array from 0 to 2*pi, with 100 elements

# n = #application
N = 50
# m = #nodes
M = 10
# t = time
T= 60*24
# Total users
nbr_users = 10000


def distTotalUserApps(nbr_apps,nbr_users):
    a = 2. # parameter
    x = arange(1., nbr_apps+1)
    y = x**(-a)/sps.zetac(a)
    result = y/sum(y)*nbr_users
    print sum(result)
    return result

def distUsersNodes(usersPerApp, dist, nbr_leafs):
    result = []
    if (dist=="Uniform"):
        mu = usersPerApp
        sigma = 0.1
        result = np.random.normal(mu,sigma,nbr_leafs)
    elif(dist=="Zeta"):
        a = 2. # parameter
        x = arange(1., nbr_leafs+1)
        y= x**(-a)/sps.zetac(a)
        result = y/sum(y)*usersPerApp;
    else:
        print "Put correct distr function"
        return
    return result

def initialNormalDistr(nbr_leafs, nbr_users, mu=0, sigma=0.1):
    s = norm(mu, sigma, nbr_leafs)
    x = arange(1.,nbr_leafs)


delta = 0.025
x = arange(1,M+1,1)
y = arange(1,N+1,1)
X, Y = meshgrid(x, y)


usersPerApp = distTotalUserApps(N,nbr_users)
users = []
# distribute users per application into nodes as well
for m in range(M): #
    users.append(distUsersNodes(usersPerApp[m],"Uniform",N))

Z = asarray(users).transpose()

print 'z:',type(Z),Z.shape, Z.dtype,Z

fig = plt.figure(figsize=(14,6))

# `ax` is a 3D-aware axis instance because of the projection='3d' keyword argument to add_subplot
ax = fig.add_subplot(1, 2, 1, projection='3d')

p = ax.plot_surface(X, Y, Z, rstride=4, cstride=4, linewidth=0)

# surface_plot with color grading and color bar
ax = fig.add_subplot(1, 2, 2, projection='3d')
p = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
cb = fig.colorbar(p, shrink=0.5)
plt.show()