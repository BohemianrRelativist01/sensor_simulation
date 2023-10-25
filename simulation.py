import numpy as np
from scipy.sparse import diags
import matplotlib.pyplot as plt
from math import sin,cos
import itertools

a=10 
r=1.6                #Initializing the inner radius of the spiral
angle=0.5           #Initialising the starting angle of the spiral
beta=0.25           #Angle update gain factor, changes the distance between the nodes 
gamma=0.0013        #Radius update factor, changes interlayer spacing
dis_threshold=3
arr=[]
plot_array=[]

class node:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.activation=0

    def draw_nodes(self,ax,radius):
        if self.activation:
            circle = plt.Circle((self.x, self.y), radius, color='red', ec='white')
        else:
            circle = plt.Circle((self.x, self.y), radius, color='blue', ec='white')
        ax.add_patch(circle)
        arr.append(circle)

def distance(ref_node,tar_node):
    return ((ref_node.center[0]-tar_node.center[0])**2 + (ref_node.center[1]-tar_node.center[1])**2)

def neighbour(ref_node):
    l=[]
    dic={}
    for i,cell in enumerate(arr):
        if distance(ref_node,cell)<dis_threshold:
            dic[distance(ref_node,cell)]=i
        #print(dic[distance(ref_node,cell)])
    dic=dict(sorted(dic.items()))
    l.append(dic)
    #l.append(dict(itertools.islice(dic.items(), 3)))
    return l


def update_matrix(ref_node):  
    act=neighbour(arr[ref_node])
    for count in list(act[0].values()):
        mat[ref_node][count]=1

def mouseover(event):
    if event.inaxes:
        for i in range(num_nodes):
          arr[i].set_color('blue')
        for j in range(num_nodes):
          if arr[j].contains(event)[0]:
            update_matrix(j)
            ones=mat[j].nonzero()[0]
            # print((j,plot_array[j].y,plot_array[j].x))
            for k in ones:
              arr[k].set_color('red')        
        plt.draw()

"""The diagonal matrix is going to represent the connections in the same layer of the spiral,
  since these are predefined, they can be represented by a sparse diagonal matrix."""
num_nodes=2000
#Intializing the sparse diagonal matrix, for the intra-layer connections
diag_0=np.squeeze(np.ones((1,num_nodes)))
diag_1=np.squeeze(np.ones((1,num_nodes-1)))
diag_2=np.squeeze(np.ones((1,num_nodes-2)))
diagonal=diags([diag_2,diag_1,diag_0,diag_1,diag_2],[-2,-1,0,1,2]).toarray()
mat=diagonal

for i in range(num_nodes):
    # Calculate the position of the next circle
    r = r+gamma
    x = (50+a*r* cos(angle))  
    y = (50+a*r* sin(angle))  
    angle = angle+ beta*(1/r)

    plot_array.append(node(x,y))
    
    

fig,ax=plt.subplots()
ax = plt.gca()
ax.set_xlim([0,100])
ax.set_ylim([0,100])

for z,nodes in enumerate(plot_array):
  nodes.draw_nodes(ax,0.0001*z)
fig.canvas.mpl_connect('motion_notify_event', mouseover)
plt.gca().set_aspect('equal', adjustable='box')
plt.show()