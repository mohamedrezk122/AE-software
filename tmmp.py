import numpy as np 
import random
import matplotlib.pyplot as plt
from pso_optimization import *
from simplex_optimization import *
from globals import * 
from mpl_toolkits import mplot3d
from wave import Wave
from  matplotlib.animation import FuncAnimation
from matplotlib import animation ,  gridspec
import matplotlib

matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.style.use('seaborn-talk')
matplotlib.rcParams['xtick.major.pad']='2'
matplotlib.rcParams['ytick.major.pad']='2'
matplotlib.rcParams["figure.autolayout"] = True
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})
X = np.arange(grid_min , grid_max , 0.5)
Y = np.arange(grid_min , grid_max , 0.5)
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

def func_dt_clc (xs,ys):

    dt_clc_matrix = [] 
    for n in range(1,4):
        dt_n = (np.sqrt((sensor_matrix[n][0]-xs)**2 +(sensor_matrix[n][1]-ys)**2) -\
        np.sqrt((sensor_matrix[0][0]-xs)**2 +(sensor_matrix[0][1]-ys)**2))/ velocity
        dt_clc_matrix.append(dt_n)
    return dt_clc_matrix


def objective(X):
    dt_clc = func_dt_clc(X[0],X[1])
    X_squared = 0
    for n in range(3):
        X_squared += ((dt_obs_lst[0][n] - dt_clc[n])**2)
    return X_squared

def brute_force_minimize():
    xs= np.arange(0,15, .05)
    ys = np.arange(0,15 , .05)
    lst = []
    xy = []
    for x in xs:
        for y in ys:
            lst.append(objective([x,y]))
            xy.append((x ,y))
    min_point = min(lst)        
    return xy[lst.index(min_point)]  
    # , min_point 


if __name__ == "__main__":
    
    ## General settings
    figure = plt.figure()
    # figure.set_tight_layout(True)   
    ax =figure.add_subplot(111)
    ax.set_aspect(1)
    # ax.set_title("Solution Demonstration" , fontsize =18)
    plt.grid()
    # ax.set_xlim(grid_min-1,grid_max+1)
    # ax.set_ylim(grid_min-1,grid_max+1)
    plots = []
    ## Solution plot
    # source_lst = [brute_force_minimize() for i in range(len(hit_lst))] 
    # for hit , source in zip(hit_lst,source_lst):
    #     p = ax.scatter(source[0][0] ,source[0][1], marker="*",s=100 , label =f"Brute force {hit}")
    #     # ax.annotate(f"{hit}", (source[0][0], source[0][1]+0.5) ,fontsize = 14)
    #     plots.append(p)

    

    # solution two 
    # so= PSOptimize(objective)
    # sol = so.x
    # p2  = ax.scatter(sol[0] , sol[1] , marker="x" , color='green' , label="PSO")

    # so2= SimplexOptimze(objective)
    # sol2 = so2.x
    # poss2 = so2.GetPoses()
    # p3  = ax.scatter(sol2[0] , sol2[1] , marker="x" , color='blue' , label="Simplex")
    # plots.append(p2)
    # plots.append(p3)
    # Sensors plot
    labels =["S1" ,"S2" , "S3", "S4"]
    sensor_pos_x = [sensor[0] for sensor in sensor_matrix]
    sensor_pos_y = [sensor[1] for sensor in sensor_matrix]
    # plt.scatter(sensor_pos_x,sensor_pos_y , color="red" ,s=100)
    # for i, txt in enumerate(labels):
    #     ax.annotate(txt, (sensor_pos_x[i]-0.3, sensor_pos_y[i]+0.3) ,fontsize = 18)

    # ## objective function
    # poss = so.GetPoses()
    # fit = so.GetFitness()
    # X_v,Y_v = np.meshgrid(X,Y)
    # Z = objective([X_v,Y_v])
    # ax2 = figure.add_subplot(projection='3d')
    # ax2.plot_wireframe(X_v, Y_v, Z,color ='b' , linewidth=1)
    # ax2.contour(X_v,Y_v,Z , zdir='z' , offset=0)

    # ax2.set_title('Objective Function', fontsize =18 )
    # tlt = ax2.title
    # tlt.set_position([.5, .8])
    # ax2.set_xlim3d(X[0], X[-1])
    # ax2.set_ylim3d(Y[0], Y[-1])
    # ax2.set_xlabel(r"$x$",  fontsize= 20)
    # ax2.set_ylabel(r"$y$",  fontsize= 20)
    # ax2.set_zlabel(r"$f(x,y)$",  fontsize= 18)
    # ax2.zaxis.offsetText.set_visible(False)
    # u = 0
    # x,y = zip(*poss[u])
    # ax2.scatter3D(x,y,fit[u], 'o' , color='red')
    # # ax3 = figure.add_subplot(224)
    # fitness = so.GetAll() 

    # images =[]
    # # line, = ax3.plot(0, fitness[0], color='k')
    # for i in range(len(poss2)):
    #     x,y = zip(*poss2[i])
    #     # image = ax2.scatter3D(x,y,fit[i], 'o' , color='red')
    #     image2 = ax.scatter(x,y, s=8,color='blue')
    #     # line.set_data(range(i), fitness[:i])
    #     images.append([image2])
    # animated_image = animation.ArtistAnimation(figure, images)
    # ax.legend(handles=plots)
    # ax2.view_init(34,-20)
    # ax2.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax2.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax2.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    # ax2.xaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax2.yaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # ax2.zaxis._axinfo["grid"]['color'] =  (1,1,1,0)
    # plt.grid(False)
    # figure.set_size_inches(w=5, h=4)
    # plt.show()
    m =21
    ax.set_xlim(0,m-1)
    ax.set_xlabel("Iterations")
    ax.set_ylabel("Deviation (cm)")
    # ax.set_ylim(0,m)
    pso_deviation_lst_x = []
    pso_deviation_lst_y = []

    simplex_deviation_lst_x =[]
    simplex_deviation_lst_y =[]

    # bs = brute_force_minimize()
    # for i in range(m):
    #     so= PSOptimize(objective)
    #     so2= SimplexOptimze(objective)
    #     pso_deviation_lst_x.append(so.x[0] - bs[0])
    #     pso_deviation_lst_y.append(so.x[1] - bs[1])
    #     simplex_deviation_lst_x.append(so2.x[0] - bs[0])
    #     simplex_deviation_lst_y.append(so2.x[1] - bs[1])



    # p1, = ax.plot(pso_deviation_lst_y , color="blue" , label="PSO: Deviation in y")
    # p2, = ax.plot(simplex_deviation_lst_y , color="red" , label="Simplex: Deviation in y")
    # ax.scatter(range(m),pso_deviation_lst_y ,color='blue' , marker="s",s=18)
    # ax.scatter(range(m),simplex_deviation_lst_y ,color='red' , marker="s" , s=18)
    # plots = [p1,p2]
    # ax.legend(handles=plots)

    so2= SimplexOptimze(objective)
    ob =
    # plt.show()
    plt.savefig('../Final Report/figures/devy.pgf', bbox_inches = 'tight')

    # animated_image.save('./test2.gif', writer='pillow') 
