import simpy

class Monitor(object):

	def __init__(self, env, meas_points, interval):
		self.env = env
		self.meas_points = meas_points #Meas points are functions from other objects that you call to retreive the data.

	# Go through and read all measurement points
	def measure(self, env):
		for meas_point in meas_points:
			# Call the funton for each meas_point