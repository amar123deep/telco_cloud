import scipy
import matplotlib.pyplot as plt

# Constants
SIM_TOTAL_TIME = 1000
SIM_TIME_INCREAMENT = 1
NBR_LEAFS = 100
APPLICATIONS = {
    'A1': {'data_rate':100, 'num_dist':None, 'loc_dist':None},
    'A2': {'data_rate':8,   'num_dist':None, 'loc_dist':None},
    'A3': {'data_rate':30,  'num_dist':None, 'loc_dist':None},
    'A4': {'data_rate':60,  'num_dist':None, 'loc_dist':None},
    'A5': {'data_rate':10,  'num_dist':None, 'loc_dist':None},
    'A6': {'data_rate':15,  'num_dist':None, 'loc_dist':None}}

# Init leafs
leafs = {}
for leaf in range(NBR_LEAFS):
    leafs[leaf] = {'pop_dist': None, 'users_per_app': [None] * 10, 'data': {'total_nbr_users': [None], 'app_population': [None],'data_volume': [None]}}

# Run simulation
for t in range(0,SIM_TIME,SIM_TIME_INCREAMENT):
    # This is where we reevaluta the distributions