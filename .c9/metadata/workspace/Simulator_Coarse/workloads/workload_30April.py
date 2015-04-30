{"filter":false,"title":"workload_30April.py","tooltip":"/Simulator_Coarse/workloads/workload_30April.py","undoManager":{"mark":11,"position":11,"stack":[[{"group":"doc","deltas":[{"start":{"row":0,"column":0},"end":{"row":1,"column":0},"action":"remove","lines":["__author__ = 'amardeep'",""]}]}],[{"group":"doc","deltas":[{"start":{"row":0,"column":0},"end":{"row":1,"column":0},"action":"remove","lines":["",""]}]}],[{"group":"doc","deltas":[{"start":{"row":161,"column":0},"end":{"row":211,"column":3},"action":"remove","lines":["","# fig = plt.figure()","fig = plt.figure()","ax1 = fig.add_subplot(1, 1, 1, projection='3d')","ax1.set_xlabel('Apps')","ax1.set_ylabel('nodes')","ax1.set_zlabel('demand')","x = np.arange(lenApps)","y = np.arange(lenNodes)","ax1.set_zlim3d(0, 1200)","ax1.set_title('Before being popular, t = 0')","X,Y = np.meshgrid(x, y)","#print workload_s","#print X.shape,Y.shape,workload_s.shape","obj1 = ax1.plot_surface(X,Y,workload_s, rstride=1, cstride=1, cmap='hot')","#wframe = ax1.plot_wireframe(X, Y, workload_s, rstride=2, cstride=2)","","","def update(i, ax, fig):","    ax.cla()","    # Z = np.multiply((1-alpha+2*alpha*np.random.random((lenNodes,lenApps))),t_workload[i])","    obj1 = ax.plot_surface(X,Y,t_workload[i], rstride=1, cstride=1, cmap='hot')","    #wframe = ax.plot_wireframe(X, Y, Z, rstride=2, cstride=2)","    ax.set_zlim(0,1200)","    #return wframe,","    return obj1,","","ani = animation.FuncAnimation(fig, update,frames=xrange(t),fargs=(ax1, fig ), interval=50)","plt.show()","","#ani.save('im.mp4', writer=writer)","# Creating the Animation object","#anim = animation.FuncAnimation(fig, update, init_func=init, frames = 25,interval=100, blit=False)","'''","","ax2 = fig.add_subplot(1, 2, 2, projection='3d')","ax2.set_xlabel('Apps')","ax2.set_ylabel('nodes')","ax2.set_zlabel('demand')","ax2.set_zlim3d(0, 1200)","ax2.set_title('App 10 popular on nodes 2,3,4 and 12,13,14 after t= 25')","x = np.arange(lenApps)","y = np.arange(lenNodes)","","X,Y = np.meshgrid(x, y)","#print workload_s","#print X.shape,Y.shape,workload_s.shape","ax2.plot_surface(X, Y, workload_pk, rstride=1, cstride=1, cmap='hot')","","plt.show()","'''"]}]}],[{"group":"doc","deltas":[{"start":{"row":158,"column":0},"end":{"row":161,"column":0},"action":"remove","lines":["# Set up formatting for the movie files","# Writer = animation.writers['ffmpeg']","# writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)",""]}]}],[{"group":"doc","deltas":[{"start":{"row":157,"column":0},"end":{"row":158,"column":0},"action":"remove","lines":["",""]}]}],[{"group":"doc","deltas":[{"start":{"row":16,"column":11},"end":{"row":16,"column":12},"action":"remove","lines":["0"]}]}],[{"group":"doc","deltas":[{"start":{"row":16,"column":10},"end":{"row":16,"column":11},"action":"remove","lines":["1"]}]}],[{"group":"doc","deltas":[{"start":{"row":16,"column":10},"end":{"row":16,"column":11},"action":"insert","lines":["5"]}]}],[{"group":"doc","deltas":[{"start":{"row":101,"column":0},"end":{"row":101,"column":1},"action":"insert","lines":["#"]}]}],[{"group":"doc","deltas":[{"start":{"row":101,"column":1},"end":{"row":101,"column":2},"action":"insert","lines":[" "]}]}],[{"group":"doc","deltas":[{"start":{"row":102,"column":0},"end":{"row":102,"column":1},"action":"insert","lines":["#"]}]}],[{"group":"doc","deltas":[{"start":{"row":102,"column":1},"end":{"row":102,"column":2},"action":"insert","lines":[" "]}]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":16,"column":11},"end":{"row":16,"column":11},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1430401460115,"hash":"824bdecbda5586a9dd643d3147c06c7c9096aa92"}