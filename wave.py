import numpy as np 
import pandas as pd 
from globals import *
from statistics import variance 
from scipy import stats
from cache import *
from pathlib import Path
from itertools import accumulate

import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'
plt.style.use('seaborn-talk')

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

__all__ = [ "Wave" ]

"""
two modes available
- localization 
- attenuation 
"""
class Wave:
    def __init__(self , hit_num , sensor_num , mode="localization"):

        self.mode           = mode         # localization or attenuation
        self.hit_num        = hit_num      # hit number -> serves like an ID
        self.sensor_num     = sensor_num   
        self.data_path      = Path(f'./Wave Forms/{self.mode}/hit_{self.hit_num}/sensor{self.sensor_num}.csv')
        self.cache_path     = Path(f'./Cache/{mode}/hit_{self.hit_num}/sensor{self.sensor_num}.json')
        self.signal_data    = self.__LoadData()
        self.time_vector    = np.linspace(self.time_of_test , self.time_of_test + self.sample_interval * (self.samples) ,self.samples)
        self.AIC_data       = self.__AIC(self.signal_data)
        self.arrival_time   = (self.AIC_data[0][0]+1)*self.sample_interval + self.time_of_test
        self.index_time     = self.arrival_time - self.time_of_test 
        self.max_amp        = max(self.signal_data)
        self.time_max_amp   = np.argmax(self.signal_data) * self.sample_interval + self.time_of_test # time of max amplitude
        self.PDT            = self.time_max_amp - self.arrival_time # peak def time

    def __LoadData(self):

        df = pd.read_csv(self.data_path)
        df = df[df.columns[0]]
        self.time_of_test   = float(df.iloc[[9]].to_string()[18:])
        self.sample_interval= float(df.iloc[[2]].to_string()[31:])
        self.samples    = int(df.iloc[[6]].to_string()[40:])
        data = df.iloc[10:].to_numpy(dtype=float) # convert dataframe to list 
        return data

    def __AIC(self , data):

        if CheckCache(self.cache_path):
            cache_data = LoadCache(self.cache_path)
            return cache_data
        else:
            aic_min , index_min = 0 , 0
            aic_data = []
            T = len(data)
            for t  in range(T):
                if t not in [0,1,T-1] :
                    aic_entry = t* np.log10(variance(data[0:t])) + (T-t-1)* np.log10(variance(data[t:T]))        
                    aic_data.append(aic_entry)
                    if (aic_entry < aic_min and  aic_entry != -np.inf):
                        aic_min = aic_entry 
                        index_min = t
            aic_data.insert(0,[index_min,aic_min]) # add meta data to cache 
            CacheData(self.cache_path,aic_data)
            return aic_data

    def PlotSignal(self, figure , ax , AIC = False):
        
        # ax.set_title(f"{self.mode.upper()} -- HIT {self.hit_num} -- CHANNEL {self.sensor_num}" , fontsize =19 )
        # ax.set_ylabel("Amplitude[V]" ,fontsize = 11 )
        # ax.set_xlabel(r'time $[s]$' ,fontsize = 11)
        ax.grid()
        p1, = ax.plot(self.time_vector, self.signal_data , color='b' , linewidth =1,  label='signal')
        # p1,  = ax.plot(self.time_vector, self.energy , color='r' , linewidth =1,  label='signal')
        plots = [p1]
        if AIC:
            ax2 = ax.twinx()
            p2 ,= ax2.plot( self.time_vector[3:], self.AIC_data[1:] ,
                            color = 'black' , linewidth = 1.2  , label= "AIC")

            p3 ,= ax2.plot( self.arrival_time, 
                            self.AIC_data[0][1], marker="o", 
                            markersize=5, markerfacecolor="green" , 
                            label="AIC_min" )

            ax2.set_ylabel("AIC" ,fontsize = 17 )
            plt.axvline(x = self.arrival_time , color = 'black', ls="--" , linewidth = 1)
            plots+=[p2,p3]

        # p4 = plt.axhline(y=self.max_amp*.1 , color="red" , ls="--", linewidth = 1 , label="threshold")
        # plt.axhline(y=-self.max_amp*.1 , color="red" , ls="--", linewidth = 1)
        # plots.append(p4)
        # ax.legend(handles=plots)
        # plt.show()


import scipy.io

def signaltonoise(a, axis=0, ddof=0):
    a = np.asanyarray(a)
    m = a.mean(axis)
    sd = a.std(axis=axis, ddof=ddof)
    return np.where(sd == 0, 0, m/sd)

if __name__ == "__main__" :
    figure, ax = plt.subplots()
    tot  = 0
    vl = []
    # for i in range(1,6):
    #     t1 = Wave(i,2, "velocity1").index_time
    #     t2 = Wave(i,3, "velocity1").index_time
    #     vl.append((0.25)/abs(t1-t2))
    #     tot += (0.25)/abs(t1-t2)

    # for i in range(5):
    #     Wave(i+1,2, "attenuation").PlotSignal(figure,ax[i,0])
        
    #     ax[i,0].set_title(f"hit {i+1}")
    # for i ,j in enumerate(range(5,10)):
    #     Wave(2*(i+1),2, "attenuation").PlotSignal(figure,ax[i,1])
    #     ax[i,1].set_title(f"hit {j+1}")

    # # # ax.set_ylabel("Amplitude[V]" ,fontsize = 11 )
    # # # ax.set_xlabel(r'time $[s]$' ,fontsize = 11)
    # figure.text(0.5, 0, r'time $[s]$', ha='center' ,fontsize = 17)
    # figure.text(0, 0.5, r'Amplitude[V]', va='center', rotation='vertical',fontsize = 17)
    # plt.tight_layout()
    # ax.set_xlabel("Hit")
    # ax.set_ylabel(r"velocity(m/s)")
    # ax.plot(range(1,6),vl,color='blue')
    # ax.scatter(range(1,6),vl , color='blue')


    # s1.PlotSignal(figure , ax ,True)
    # lst = []
    # for i in range(1,11):
    #     # if i not in [1,8,10]:
    #     lst.append(Wave(i,2, "attenuation").max_amp)
    # # w.PlotSignal(figure , ax ,True)
    # print(lst)
    # figure2, ax2 = plt.subplots()
    # lst.sort(reverse=True)
    
    # ax2.plot(list(range(1,11)) , lst)
    # ax2.plot(w.time_vector, fft(w.signal_data),color="green")
    # plt.show()
    # plt.savefig('../Final Report/figures/att1.pgf', bbox_inches = 'tight')
    # ll = []

    # for i in range(1,11):
    #     ll.append(signaltonoise(Wave(i,2, "attenuation").signal_data, axis = 0, ddof = 0) )

    # print(ll)
    # ll = sorted(ll)
    # print(ll)

    # s1.PlotSignal(figure , ax ,True)

    ax.set_ylabel("Maximum Amplitude[V]" ,fontsize = 14 )
    ax.set_xlabel(r'distance(cm)' ,fontsize = 14)
    lst = []
    for i in range(1,11):
        if i not in [5,8,10]:
            lst.append(Wave(i,2, "attenuation").max_amp)
    # # w.PlotSignal(figure , ax ,True)

    lst.sort(reverse=True)
    # ax.plot(list(range(0,35,5)) , lst,color='red')
    # ax.scatter(list(range(0,35,5)) , lst , color ='red')

    y = np.array(lst)
    x = np.array(range(5,40,5))
    print(x)
    p = np.polyfit(x, np.log(y), 1, w=np.sqrt(y))

    # # Convert the polynomial back into an exponential
    a = np.exp(p[1])
    b = p[0]
    x_fitted = np.linspace(np.min(x), np.max(x), 100)
    y_fitted = a * np.exp(b * x_fitted)
    x_fitted_weighted = np.linspace(np.min(x), np.max(x), 100)
    y_fitted_weighted = a * np.exp(b * x_fitted_weighted)
    print(a,b)
    # # Plot
    # ax = plt.axes()
    ax.scatter(x, y, label='Raw data' , color="red")
    # ax.plot(x_fitted, y_fitted, 'k', label='Fitted curve, unweighted')
    ax.plot(x_fitted_weighted, y_fitted_weighted, 'b--', label='Fitted curve, weighted')
    # ax.set_title('Using polyfit() to fit an exponential function')
    # ax.set_ylabel('y-Values')
    ax.set_xlim(4, 36)
    # ax.set_xlabel('x-Values')
    ax.legend()



    # ax.plot(w.time_vector, fft(w.signal_data),color="green")
    # plt.show()
    plt.savefig('../Final Report/figures/att3.pgf', bbox_inches = 'tight')


"""
2
3
4
5
6
7
9
"""