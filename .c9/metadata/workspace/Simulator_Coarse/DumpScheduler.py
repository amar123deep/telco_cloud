{"changed":true,"filter":false,"title":"DumpScheduler.py","tooltip":"/Simulator_Coarse/DumpScheduler.py","value":"import simpy\n\nfrom Scheduler import Scheduler\n\nclass DumbScheduler(Scheduler):\n    def __init__(self, env, datacentres, leafs, links):\n        Scheduler.__init__(self, env, datacentres, leafs, links)\n    \n    # Find paths to nearest available node\n\tdef findFirstAvailableDC(self, leaf, appName, nbrUsers): # Caution! Only for trees\n\t\t\"\"\"\n        Descr  :    Find the paths to the nearest resource that can host application 'app'\n        Input  :    leaf - The leafnode from which the search will originate from, actual node\n                    app - A struct with app name as key and number of users as value\n        Output :    Paths of first placement options.\n        \"\"\"\n        def available(resAvailability):\n            result = True\n            for availability in resAvailability.itervalues():\n                result *= availability\n            return result\n            \n        def traverse(node, path, appName, nbrUsers, placementOptions):\n\t\t    isAvailable = available(node.willAppFit({appName: nbrUsers}))\n\t\t    \n\t\t    if type(node) is Datacentre:\n\t\t        if isAvailable:\n\t\t            placementOptions.append(node) # Candidate DC found\n\t\t            return # No reason to proceed down this path as we are only looking for first available DC\n\n\t\t    elif type(node) is Link:\n\t\t        if not isAvailable:\n\t\t            return # If link is saturated, no reason to proceed down this path.\n\n            # Keep looking ...\n\t\t\tpeers = node.getPeers()\n\t\t\tfor peer in peers.iteritems():\n\t\t\t\tif peer not in path: # [William] Not correct should be for all nodes or DCs\n\t\t\t\t\ttraverse(peer, path + [peer], appName, nbrUsers, placementOptions)\n\n        nodes = {}\n      \n        placementOptions = [] # Possible places to host app\n        path = [] # Iteratively constructed path\n        \n        traverse(leaf, path+[self], appName, nbrUsers, placementOptions)\n\n        return placementOptions\n\n    \n    def initPlacement(self):\n        for leaf in self.leafs.itervalues():\n            subscribers =  leaf.getSubscribers()\n            print subscribers\n            for appName, nbrAppSubscribers in subscribers.iteritems():\n                placementOptions = self.findFirstAvailableDC(leaf, appName, nbrAppSubscribers)\n                \n                assert (len(placementOptions) > 0),\"No placement options found for %s from %s\" % (appName, leaf.getName())\n                \n                placementOptions[0].registerApp(appName)","undoManager":{"mark":14,"position":15,"stack":[[{"group":"doc","deltas":[{"start":{"row":0,"column":0},"end":{"row":55,"column":56},"action":"insert","lines":["class DumbScheduler(Scheduler):","    def __init__(self, env, datacentres, leafs, links):","        Scheduler.__init__(self, env, datacentres, leafs, links)","    ","    # Find paths to nearest available node","\tdef findFirstAvailableDC(self, leaf, appName, nbrUsers): # Caution! Only for trees","\t\t\"\"\"","        Descr  :    Find the paths to the nearest resource that can host application 'app'","        Input  :    leaf - The leafnode from which the search will originate from, actual node","                    app - A struct with app name as key and number of users as value","        Output :    Paths of first placement options.","        \"\"\"","        def available(resAvailability):","            result = True","            for availability in resAvailability.itervalues():","                result *= availability","            return result","            ","        def traverse(node, path, appName, nbrUsers, placementOptions):","\t\t    isAvailable = available(node.willAppFit({appName: nbrUsers}))","\t\t    ","\t\t    if type(node) is Datacentre:","\t\t        if isAvailable:","\t\t            placementOptions.append(node) # Candidate DC found","\t\t            return # No reason to proceed down this path as we are only looking for first available DC","","\t\t    elif type(node) is Link:","\t\t        if not isAvailable:","\t\t            return # If link is saturated, no reason to proceed down this path.","","            # Keep looking ...","\t\t\tpeers = node.getPeers()","\t\t\tfor peer in peers.iteritems():","\t\t\t\tif peer not in path: # [William] Not correct should be for all nodes or DCs","\t\t\t\t\ttraverse(peer, path + [peer], appName, nbrUsers, placementOptions)","","        nodes = {}","      ","        placementOptions = [] # Possible places to host app","        path = [] # Iteratively constructed path","        ","        traverse(leaf, path+[self], appName, nbrUsers, placementOptions)","","        return placementOptions","","    ","    def initPlacement(self):","        for leaf in self.leafs.itervalues():","            subscribers =  leaf.getSubscribers()","            print subscribers","            for appName, nbrAppSubscribers in subscribers.iteritems():","                placementOptions = self.findFirstAvailableDC(leaf, appName, nbrAppSubscribers)","                ","                assert (len(placementOptions) > 0),\"No placement options found for %s from %s\" % (appName, leaf.getName())","                ","                placementOptions[0].registerApp(appName)"]}]}],[{"group":"doc","deltas":[{"start":{"row":0,"column":6},"end":{"row":0,"column":19},"action":"remove","lines":["DumbScheduler"]},{"start":{"row":0,"column":6},"end":{"row":0,"column":19},"action":"insert","lines":["DumpScheduler"]}]}],[{"group":"doc","deltas":[{"start":{"row":0,"column":0},"end":{"row":1,"column":0},"action":"insert","lines":["",""]}]}],[{"group":"doc","deltas":[{"start":{"row":1,"column":0},"end":{"row":2,"column":0},"action":"insert","lines":["",""]}]}],[{"group":"doc","deltas":[{"start":{"row":0,"column":0},"end":{"row":2,"column":29},"action":"insert","lines":["import simpy","","from Resource import Resource"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":5},"end":{"row":2,"column":13},"action":"remove","lines":["Resource"]},{"start":{"row":2,"column":5},"end":{"row":2,"column":6},"action":"insert","lines":["A"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":6},"end":{"row":2,"column":7},"action":"insert","lines":["S"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":6},"end":{"row":2,"column":7},"action":"remove","lines":["S"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":5},"end":{"row":2,"column":6},"action":"remove","lines":["A"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":5},"end":{"row":2,"column":6},"action":"insert","lines":["S"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":6},"end":{"row":2,"column":7},"action":"insert","lines":["c"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":5},"end":{"row":2,"column":7},"action":"remove","lines":["Sc"]},{"start":{"row":2,"column":5},"end":{"row":2,"column":16},"action":"insert","lines":["Scheduler()"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":14},"end":{"row":2,"column":15},"action":"remove","lines":["("]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":14},"end":{"row":2,"column":15},"action":"remove","lines":[")"]}]}],[{"group":"doc","deltas":[{"start":{"row":2,"column":22},"end":{"row":2,"column":30},"action":"remove","lines":["Resource"]},{"start":{"row":2,"column":22},"end":{"row":2,"column":31},"action":"insert","lines":["Scheduler"]}]}],[{"group":"doc","deltas":[{"start":{"row":4,"column":9},"end":{"row":4,"column":10},"action":"remove","lines":["p"]},{"start":{"row":4,"column":9},"end":{"row":4,"column":10},"action":"insert","lines":["b"]}]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":4,"column":6},"end":{"row":4,"column":19},"isBackwards":true},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1426756355069}