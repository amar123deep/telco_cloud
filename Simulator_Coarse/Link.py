import simpy

class Link(Resource):

    def __init__(self, env, scheduler):
        Resource.__init__(self, name, id)
        self.env = env
        self.scheduler = scheduler
        self.applications = []

        self.uplink = uplink
        self.downlink = downlink

    # Add appliction to its list of applications
    def add_Application(self, application):
        applications.append({application.id : {'compute_need'}})

    # Remove appliction to its list of applications
    def remove_Application(self, application):
        applications.remove(application)

    # Update number of users for an application
    def update_nbr_users(self, application, nbr_users):

    # Evaluate how much resources an application consumes and how much it contributes to the load of the DC
    def evaluate_resource_usage(self, application, nbr_users):