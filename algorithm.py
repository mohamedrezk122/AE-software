from globals import * 
from plotting import *
import numpy as np 
import matplotlib.pyplot as plt 
from scipy.linalg import solve
from mpl_toolkits import mplot3d
from wave import Wave
import tikzplotlib as tk

time_matrix_lst =[]
dt_obs_lst = []
hit_lst = [1 , 14 , 16, 18 , 36]
hit_lst = [hit_lst[0]]
sensor_matrix = [S1,S2,S3,S4]
for hit in hit_lst:
    time_matrix = []
    for sensor in range(1,5):
        time_matrix.append(Wave(hit,sensor).arrival_time)
    dt_obs_lst.append([ti-time_matrix[0] for ti in [time_matrix[1],time_matrix[2],time_matrix[3]]]) 
    time_matrix_lst.append(time_matrix)

def objective(dt_clc , dt_obs):

    X_squared = 0
    for n in range(3):
        X_squared += ((dt_obs[n] - dt_clc[n])**2)
    return X_squared

def func_dt_clc (xs,ys):

    dt_clc_matrix = [] 
    for n in range(1,4):
        dt_n = (np.sqrt((sensor_matrix[n][0]-xs)**2 +(sensor_matrix[n][1]-ys)**2) - np.sqrt((sensor_matrix[0][0]-xs)**2 +(sensor_matrix[0][1]-ys)**2))/ velocity
        dt_clc_matrix.append(dt_n)
    return dt_clc_matrix

def brute_force_minimize(dt_obs):
    xs= np.arange(0,15, .05)
    ys = np.arange(0,15 , .05)
    lst = []
    xy = []
    for x in xs:
        for y in ys:
            lst.append(objective(func_dt_clc(x,y),dt_obs))
            xy.append((x ,y))
    min_point = min(lst)        
    return xy[lst.index(min_point)]  , min_point 

def DTOA():

    tau = [ti-t1 for ti in [t1,t2,t3,t4]] 

    A3 =    ((-2*S1[0]+2*S3[0])/(velocity*tau[2])) - ((-2*S1[0]+2*S2[0])/(velocity*tau[1]))  
            
    A4 =    ((-2*S1[0]+2*S4[0])/(velocity*tau[3])) - ((-2*S1[0]+2*S2[0])/(velocity*tau[1])) 

    B3 =    ((-2*S1[1]+2*S3[1])/(velocity*tau[2])) - ((-2*S1[1]+2*S2[1])/(velocity*tau[1])) 
            
    B4 =    ((-2*S1[1]+2*S4[1])/(velocity*tau[3])) - ((-2*S1[1]+2*S2[1])/(velocity*tau[1])) 

    D3 =    (velocity*tau[2])-(velocity*tau[1]) + ((S1[0]**2+S1[1]**2-S3[0]**2-S3[1]**2)/(velocity*tau[2]))- ((S1[0]**2+S1[1]**2-S2[0]**2-S2[1]**2)/(velocity*tau[1]))
            
    D4 =    (velocity*tau[3])-(velocity*tau[1]) + ((S1[0]**2+S1[1]**2-S4[0]**2-S4[1]**2)/(velocity*tau[3]))- ((S1[0]**2+S1[1]**2-S2[0]**2-S2[1]**2)/(velocity*tau[1]))
            
    # D_i + A_i x + B_i y = 0

    # C x = e 

    C_matrix = np.array(    [[ A3 , B3 ] , 
                            [  A4 , B4 ]] ) 

    D_matrix = np.array(    [[ -D3 ] ,  
                            [  -D4  ]])
    pos = solve(C_matrix, D_matrix)

    return pos


if __name__ == "__main__":
    
    ## General settings
    figure = plt.figure(figsize=(10,6) )
    ax =figure.add_subplot(1,2,1)
    ax.set_aspect(1)
    ax.set_title("Solution Demonstration" , fontsize =22)
    plt.grid()
    # ax.set_xlim(0,15)
    # ax.set_ylim(0,15)

    ## Solution plot
    source_lst = [brute_force_minimize(dt_obs_lst[i]) for i in range(len(hit_lst))] 
    for hit , source in zip(hit_lst,source_lst):
        plt.scatter(source[0][0] ,source[0][1], marker="x" ,s=100 )
        ax.annotate(f"{hit}", (source[0][0], source[0][1]+0.5) ,fontsize = 14)

    # solution two 
    # source2 = DTOA() 
    # ax.annotate("Solution 2", (source2[0]-1, source2[1]+1) ,fontsize = 18)
    # plt.scatter(source2[0] ,source2[1], marker="x" ,s=100 , color ='green')

    ## Sensors plot
    labels =["S1" ,"S2" , "S3", "S4"]
    sensor_pos_x = [sensor[0] for sensor in sensor_matrix]
    sensor_pos_y = [sensor[1] for sensor in sensor_matrix]
    plt.scatter(sensor_pos_x,sensor_pos_y , color="red" ,s=100)
    for i, txt in enumerate(labels):
        ax.annotate(txt, (sensor_pos_x[i]-0.3, sensor_pos_y[i]+0.3) ,fontsize = 18)

    ## objective function
    x = np.linspace(0,15,300)
    y = np.linspace(0,15,300)
    X,Y = np.meshgrid(x,y)
    Z = objective(func_dt_clc(X,Y),dt_obs_lst[0])
    ax2 = figure.add_subplot(1,2,2,projection='3d')
    ax2.plot_surface(X, Y, Z,
                cmap='jet')
    #ax2.scatter3D(source[0][0],source[0][1],source[1],s=70)
    ax2.set_title('Objective Function', fontsize =20 )


    plt.show()
