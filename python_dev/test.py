# Produce the user distribution based on the application popularity

import matplotlib.pyplot as plt
import scipy.special as sps
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

# for 3D plot, import 
from mpl_toolkits.mplot3d.axes3d import Axes3D

# step 1: compute the user distribution per application based on global popularity
# step 2: distribute the user among nodes
# step 2a: Uniform
# step 2b: Non-uniform
# step 3: shape changes with time baased on some scenario (use-cases)

#s = np.random.zipf(a, n)


# Truncate s values at n so plot is interesting
# count, bins, ignored = plt.hist(s, n, normed=True)

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
    x = np.arange(1., nbr_apps+1)
    y = x**(-a)/sps.zetac(a)
    result = y/sum(y)*nbr_users
    print sum(result)
    return result

def distUsersNodes(usersPerApp, dist, nbr_leafs):
    result = []
    if (dist=="Uniform"):
        mu = 0
        sigma = 0.1 
        result = np.random.normal(mu, sigma, nbr_leafs)
    elif(dist=="Zeta"):
        a = 2. # parameter
        x = np.arange(1., nbr_leafs+1)
        y= x**(-a)/sps.zetac(a)
        result = y/sum(y)*usersPerApp;
    else:
        print "Put correct distr function" 
        return
    return result

def initialNormalDistr(nbr_leafs, nbr_users, mu=0, sigma=0.1): 
    s = np.random.normal(mu, sigma, nbr_leafs)
    x = np.arrange(1.,nbr_leafs)
    s/sum(s)*nbr_users
    

    
# we want to make a 3d array for user distr 
usersPerApp = distTotalUserApps(N,nbr_users)
# plot to see the application popularity 
x1 = np.arange(1., N)
#plt.plot(x1,usersPerApp, linewidth=2, color='r')
#plt.show()

users = []

# distribute users per application into nodes as well 
for m in range(M): # 
    users.append(distUsersNodes(usersPerApp[m],"Zeta",N))

# 3d plot for users, x axis= node, y-axis= application, z-axis= # users  
fig = plt.figure()
ax = fig.gca(projection='3d')
X = np.arange(1., M+1)
Y = np.arange(1., N+1)
#X, Y = np.meshgrid(X, Y)

print X.size
print Y.size


ax = fig.add_subplot(1, 2, 1, projection='3d')
p = ax.plot_surface(X, Y, Z, rstride=4, cstride=4, linewidth=0)

# surface_plot with color grading and color bar
ax = fig.add_subplot(1, 2, 2, projection='3d')
p = ax.plot_surface(X, Y, np.array(users), rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
cb = fig.colorbar(p, shrink=0.5)


#surf = ax.plot_surface(Y, X, np.array(users), rstride=1, cstride=1, cmap=cm.coolwarm,
#        linewidth=0, antialiased=True)
#ax.set_zlim(-1.01, 1.01)

#ax.zaxis.set_major_locator(LinearLocator(10))
#ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

#fig.colorbar(surf, shrink=0.5, aspect=5)
#fig.show()
