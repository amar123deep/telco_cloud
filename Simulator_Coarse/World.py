import simpy

# Class wich manages all applications and users, loops through at a certain rate and updates users.
class World(object):

    def __init__(self, env, scheduler, nbr_applications, user_population_model):
    	self.env = env
    	self.scheduler = scheduler
    	self.applications = {}
    	
    	# Instanciate users and applications
    	for i in range(nbr_applications):
    		self.applications.update() # Add applicta

    # Revaluate all user placements
	def revaluate(self):

	# Send data
	def notify_listeners(self, data):
		pass

	# Perhaps all scheduling shall be done by trigger box
	def schedule_application(self, application)
		scheduler.schedule(application)