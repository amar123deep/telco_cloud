import simpy
import json
import sys
import yaml
import logging

class Workload(object):

	def __init__(self, env, file_name, coordinator):
		self.env = env
		self.coordinator = coordinator
		self.data_new = yaml.load(open(file_name))
		self.apps = []

	# Produce workload
	def produceWorkload(self):
		prev_time = self.env.now

		for time in sorted(self.data_new, key=lambda x: int(x)): # Time progresses whenever there is a change
			yield self.env.timeout(int(time)-prev_time) # Needed in runtime
			logging.debug("----- [%s]-----" % time)

			prev_time = self.env.now

			for (path, appName, leafName, demand) in self.coordinator.getPath(self.data_new[time]):
				for element in path:
					element.updateSubscriber(appName, leafName, demand)

	# Get the last time stamp in the workload
	def getWorkloadTimeSpan(self):
		return sorted(self.data_new, key=lambda x: int(x))[-1]