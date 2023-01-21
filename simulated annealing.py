import random 
import numpy as np 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


figure, ax = plt.subplots()

lower_bound = -1.5 
upper_bound = 1.5 
X = np.arange(lower_bound , upper_bound , .01)
def obj(x):
    return x**7 -3*x**3 + 2*x -x**5 + .2*x**6
    # return x**2

def visiting(dx,T):
    return np.exp(-(dx**2)/T)

temp = []
objective = []
iterations = 4000
k = 1.380649e-23
x_i  = random.choice(X)
# E is energy -> cost function 
def boltzmann_prob(dE,T):
    return np.exp(-dE/(k*T))

def get_neighbours(x):
    axis = list(X)
    idx = axis.index(x)
    pram = 4
    if (idx + pram <= len(axis)) and ( idx - pram >= 0):  
        return axis[idx-pram:idx+pram]
    elif idx + pram > len(axis):
        return axis[-2*pram:-1]
    else:
        return axis[0:2*pram+1]
v= []
def optimize():
    global temp , objective, x_i ,v 
    # parameters 
    alpha  = .9 # cooling rate (geometric reduction rule)
    T      =  500
    X_i=[]
   
    for i in range(iterations):
        neighbours = get_neighbours(x_i)
        random_neighbour = random.choice(neighbours)
        obj_i = obj(x_i)
        obj_neighbour = obj(random_neighbour)
        if(obj_neighbour <= obj_i):
            x_i = random_neighbour 
        else:
            dE = obj_neighbour - obj_i
            P = boltzmann_prob(dE , T)
            r = random.uniform(0,1)
            if (r < P):
                x_i = random_neighbour
        
        objective.append(obj_i)
        X_i.append(x_i)
        temp.append(T)
        T = alpha * T
    return X_i 
Xi = optimize()
def get_x(i):
    return Xi[i]

print(v)
ax.plot(x_i , obj(x_i) , marker="o")
ax.plot(X , obj(X))
plt.grid()


def update(i):
    x = get_x(i)
    y = obj(x)
    point.set_data([x],[y])
    return point , 


# ani = FuncAnimation(figure, update, interval=30, blit=True, repeat=True , frames = iterations)

# fig2, ax2 = plt.subplots()

plt.show()