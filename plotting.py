import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib import rc
from statistics import variance 
import json 
import os 
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'

def CheckCache(hit_num ,sensor_num ):

    dir_path = f"./Cache/hit_{hit_num}/"
    file_path = dir_path + f"sensor{sensor_num}.json"

    if os.path.exists(dir_path):
       
        if os.path.exists(file_path):
           
            return True  # cache exists
    else:
        os.mkdir(dir_path)

        return False

def CacheData(hit_num,sensor_num, data):

    file_path = f'./Cache/hit_{hit_num}/sensor{sensor_num}.json'

    with open(file_path, 'w', encoding='utf-8') as file:

        json.dump(data, file, ensure_ascii=False, indent=4)

    return 1

def LoadCache(hit_num,sensor_num):

    file_path = f'./Cache/hit_{hit_num}/sensor{sensor_num}.json'

    with open(file_path, 'r', encoding='utf-8') as file:
        cache_data = json.load(file)

    return cache_data

def LoadData(hit_num , sensor_num ):

    df = pd.read_csv(f'./Wave Forms/localization/hit_{hit_num}/sensor{sensor_num}.csv')
    data = df[df.columns[0]].values.tolist()
    return data

def AIC(hit_num , sensor_num ,data):

    if CheckCache(hit_num ,sensor_num):

        cache_data = LoadCache(hit_num,sensor_num)
        return cache_data

    else:

        aic_data = []
        
        T = len(data)

        for t in range(T):

            if t not in [0,1,T-1 ,T] :
                #print(t)
                aic = t* np.log10(variance(data[0:t])) + (T-t-1)* np.log10(variance(data[t:T]))        
                aic_data.append(aic)

        CacheData(hit_num,sensor_num,aic_data)

        return aic_data



def Plot(hit_num,sensor_num ,data, x,y):

    axis  = np.linspace(0,8.4922692)
    aic_data  = AIC(hit_num, sensor_num , data)

    ax2 = ax[x, y].twinx()

    p1 , = ax[x,y].plot(aic_data, color='black' , label = "AIC function" , linewidth =1)

    p2 , = ax2.plot(data[3:], color='red' , label = "signal" , linewidth =1)

    p3 , = ax[x,y].plot(np.argmin(aic_data), 
                        np.amin(aic_data), marker="o", 
                        markersize=5, markerfacecolor="green" , 
                        label="AIC_min" )

    plt.axvline(x = aic_data.index(np.amin(aic_data)), color = 'black', ls="--")

    ax[x,y].legend(handles=[p1, p2,p3])

    ax[x,y].set_ylabel("AIC" ,fontsize = 15 )
    ax2.set_ylabel("Amplitude[V]" ,fontsize = 15 )
    ax[x,y].set_xlabel(r'time $[\mu s]$' ,fontsize = 15)
    plt.title(f"Hit {hit_num} - Sensor {sensor_num} Data" , fontsize = 15)

    plt.subplots_adjust(left=0.055,
                    bottom=0.07, 
                    right=0.948, 
                    top=0.912, 
                    wspace=0.249, 
                    hspace=0.315)

data1 = LoadData(1,1)
data2 = LoadData(1,2)

data3 = LoadData(1,3)
data4 = LoadData(1,4)

aic_data = AIC(1,1,data1)
if __name__ == "__main__" :

    figure, ax = plt.subplots(2, 2)

    figure.suptitle("Sensor Data" , fontsize =22)
    
    Plot(1,1,data1,1,0)
    Plot(1,2,data2,1,1)
    Plot(1,3,data3,0,1)
    Plot(1,4,data4,0,0)
    plt.show()