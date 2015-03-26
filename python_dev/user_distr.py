# [TO-DO : WILLIAM] Make application generation dynamic
# [TO-DO] What distribution to use for data rate?
# [TO-DO] How do we specify the seed? Can we do it for all distributions in one place?

#[To-DO : AMARDEEP] Implement user workload distribution for testing purpose 

#import pkg_resources
#pkg_resources.require("matplotlib")

import numpy as np
import scipy.special as sps
import matplotlib.pyplot as plt

# Constants
TOTAL_USER = 10000
SIM_TOTAL_TIME = 1000
SIM_TIME_INCREAMENT = 1
NBR_LEAFS = 20
APPLICATIONS = {
    'A1': {'data_rate':100, 'users':0, 'data': {'total_nbr_users': [None], 'data_volume': [None]}},
    'A2': {'data_rate':8,   'users':0, 'data': {'total_nbr_users': [None], 'data_volume': [None]}},
    'A3': {'data_rate':30,  'users':0, 'data': {'total_nbr_users': [None], 'data_volume': [None]}},
    'A4': {'data_rate':60,  'users':0, 'data': {'total_nbr_users': [None], 'data_volume': [None]}},
    'A5': {'data_rate':10,  'users':0, 'data': {'total_nbr_users': [None], 'data_volume': [None]}},
    'A6': {'data_rate':15,  'users':0, 'data': {'total_nbr_users': [None], 'data_volume': [None]}}}

# Zipf Distribution
a = 2 # [TO-DO] Find reasonable value
s = np.random.zipf(a, len(APPLICATIONS))
total_popularity = sum(s)
print(total_popularity)

for num in s:
    print(num)

# Init leafs
leafs = {}
for leaf in range(NBR_LEAFS):
    leafs[leaf] = {'pop_dist': None, 'users_per_app': [None], 'data': {'total_nbr_users': [None], 'app_population': [None],'data_volume': [None]}}
    # assign mean, median for each node

    
# Run simulation
#for t in range(0,SIM_TIME,SIM_TIME_INCREAMENT):
#    for leaf_nbr in leafs:
#        leafs[leaf_nbr]
#        # compute user distribution baswed on mean and mediaun assigned to each node
        

# This is where we reevaluta the distributions
    