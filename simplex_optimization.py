import numpy as np
import random
from globals import *

__all__ = ['SimplexOptimze']

class Simplex:

    def __init__(self, dim , objective):

        self.objective = objective
        self.dim = dim
        self.best  = np.random.uniform(low=grid_min, high=grid_max, size=(dim,))
        self.other = np.random.uniform(low=grid_min, high=grid_max, size=(dim,))
        self.worst = np.random.uniform(low=grid_min, high=grid_max, size=(dim,))
        self.Sort_Simplex()
        self.lst = [self.best, self.other, self.worst]
        # print(objective(self.best) < objective(self.other) < objective(self.worst) )
        self.centroid = np.zeros((dim,))
        self.reflected = np.zeros((dim,))
        self.expanded = np.zeros((dim,))
        self.contracted =  np.zeros((dim,))


    def Sort_Simplex(self):
        tmp = sorted([self.best, self.other, self.worst], key=self.objective)
        self.best=tmp[0]
        self.other=tmp[1]
        self.worst=tmp[2]
     
        # print(self.objective(self.best) < self.objective(self.other) < self.objective(self.worst) )

    # def check_pos(self):
    #     for i in range(self.dim):
    #         if self.best[i] < grid_min or self.best[i] > grid_max :
    #             self.best[i] = np.random.uniform(self.other[i], self.worst[i])
    #             print("i am here 1") 
    #         if self.other[i] < grid_min or self.other[i] > grid_max :
    #             self.other[i] = np.random.uniform(self.best[i], self.worst[i])
    #             print("i am here 2")
    #         if self.worst[i] < grid_min or self.worst[i] > grid_max :
    #             self.worst[i] = np.random.uniform(self.best[i], self.other[i])
    #             print("i am here 3")

    def check(self):
        return self.objective(self.best) < self.objective(self.other) < self.objective(self.worst) 

class SimplexOptimze:
    
    def __init__(self , objective, dim = 2 , MAX = grid_max , MIN = grid_min , MAX_Iter=2000):

        self.objective = objective
        self.dim = dim
        self.MAX = MAX
        self.MIN = MIN
        self.tolerance = 1e-17
        self.rng = 0.002
        self.MAX_Iter = MAX_Iter
        self.simplex = Simplex(self.dim ,self.objective)
        self.poses      = []
        self.MAIN_LOOP(self.simplex)
        # print("-----", self.simplex.best[0]-self.simplex.worst[0])
        # print(self. __Check_Convergence(self.simplex))
        self.simplex.Sort_Simplex()
        self.x = self.simplex.best


    def MAIN_LOOP(self , simplex):
        i = 0
        while(i < self.MAX_Iter and self. __Check_Convergence(simplex)):

            self.__Compute_Centroid(simplex)
            self.__Compute_Reflected(simplex)

            f_r = self.objective(simplex.reflected)
            f_b = self.objective(simplex.best)
            f_o = self.objective(simplex.other)
            f_w = self.objective(simplex.worst)

            if (f_b <= f_r < f_o) :

                simplex.worst = simplex.reflected
                # simplex.Sort_Simplex()

            elif (f_r < f_b):
                self.__Compute_Expanded(simplex)
                f_e = self.objective(simplex.expanded)
                if (f_e < f_r):
                    simplex.worst = simplex.expanded
                else:
                    simplex.worst = simplex.reflected
                # simplex.Sort_Simplex()

            elif (f_o <= f_r < f_w):
                self.__Outside_Contraction(simplex)
                f_c = self.objective(simplex.contracted)

                if (f_c <= f_r):
                    simplex.worst = simplex.contracted
                    # simplex.Sort_Simplex()
                else:
                    self.__Shrink(simplex)
                    # simplex.Sort_Simplex()

            else:
                self.__Inside_Contraction(simplex)
                f_c = self.objective(simplex.contracted)
                if (f_c < f_w):
                    simplex.worst = simplex.contracted
                else:
                    self.__Shrink(simplex)

            simplex.Sort_Simplex()
            self.poses.append (self.objective(simplex.best))
            # print(self.__Check_Convergence(simplex))

            i+=1    
        # print(i)  
        
    def __Check_Convergence(self,simplex):
        f_w = self.objective(simplex.worst)
        f_b = self.objective(simplex.best)

        sigma = 2*  (f_w-f_b)/(f_w + f_b + self.tolerance)
        return sigma > self.tolerance
        # return (abs(simplex.best[0] - simplex.worst[0]) > self.rng and abs(simplex.best[1] - simplex.worst[1]) > self.rng )
    def __Compute_Centroid(self, simplex):
        
        for i in range(self.dim):
            simplex.centroid[i] = (simplex.best[i] + simplex.other[i])/2

    def __Compute_Reflected(self , simplex):

        alpha = 1 
        for i in range(self.dim):
            simplex.reflected[i] = simplex.centroid[i] + alpha*\
                                (simplex.centroid[i] - simplex.worst[i])

    def __Compute_Expanded(self , simplex):
        
        gamma = 2
        for i in range(self.dim):
            simplex.expanded[i] = simplex.centroid[i] + gamma*\
                                (simplex.reflected[i] - simplex.centroid[i])

    def __Inside_Contraction(self , simplex):

        beta = 0.5 
        for i in range(self.dim):
            simplex.contracted[i] = simplex.centroid[i] + beta*\
                                (simplex.worst[i] - simplex.centroid[i])

    def __Outside_Contraction(self , simplex):

        beta = 0.5 
        for i in range(self.dim):
            simplex.contracted[i] = simplex.centroid[i] + beta*\
                                (simplex.reflected[i] - simplex.centroid[i])

    def __Shrink(self, simplex):

        delta = 0.5 
        for i in range(self.dim):
            simplex.worst[i] = simplex.best[i] + delta*\
                                (simplex.worst[i] - simplex.best[i])

            simplex.other[i] = simplex.best[i] + delta*\
                                (simplex.other[i] - simplex.best[i])
    
    def GetPoses(self):
        return self.poses

