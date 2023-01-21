import numpy as np 
import random
from globals import * 


__all__ = ['PSOptimize']

class Particle:
    def __init__(self,dim,objective):

        self.position       = np.random.uniform(low=grid_min, high=grid_max, size=(dim,))  # intialize a random position for a particle
        self.velocity       = np.zeros((dim,))
        self.best_pos       = self.position
        self.fitness        = objective(self.position)
        self.best_fitness   = self.fitness  

class PSOptimize:
    def __init__(   self , objective , inertia = 1, c1 = 0.1 , 
                    c2 = 0.1 , dim = 2 , MAX = grid_max , 
                    MIN = grid_min , population=60 , generation=100):

        self.objective  = objective               # the objective function needed to minimize 
        self.inertia    = inertia                 # interia weight
        self.c1         = c1                      # cognitive weight (the weight of leaning towards the particle best pos)
        self.c2         = c2                      # social weight (the weight of leaning towards the swarm best pos)
        self.dim        = dim                     # dimension of the decision vector (X)
        self.MAX        = MAX                     # upper bound for the vector X 
        self.MIN        = MIN                     # lower bound for the vector X
        self.generation = generation              # maximum number of generations
        self.VMAX       = .2*(self.MAX-self.MIN)  # upper bound for the velocity vector
        self.VMIN       = -self.VMAX              # lower bound for the velocity vector
        self.population = population              # number of particles within each generation              
        self.particles  = []                      # particles array 
        self.best_fitness_swarm = np.inf          # intialize the global best fitness to infinity 
        self.best_pos_swarm = None                # intialize the global best pos to Null
        self.__PSO_MAIN_LOOP()                      # excute the main loop
        self.x = self.best_pos_swarm              # assign the solution to the best pos among the swarm 
        self.fun = self.best_fitness_swarm        # assign the min fitness to the best fitness among the swarm 


    def __PSO_MAIN_LOOP(self):

        # intiailize some arrays to store the particles data among generations for plotting
        self.poses      = np.zeros((self.generation,self.population,self.dim)) 
        self.fitnesses  = np.zeros((self.generation,self.population)) 
        self.all_best   = np.zeros((self.generation,))
        # intiailize particles 
        for _ in range(self.population):
            particle = Particle(self.dim , self.objective)
            self.particles.append(particle)
            if particle.fitness <  self.best_fitness_swarm :
                self.best_fitness_swarm = particle.fitness   # select the best fitness among the particles 
                self.best_pos_swarm = particle.position           # select the corresponding pos to the best fitness 

        # main loop 
        for i in range(self.generation):
            for j, particle in enumerate(self.particles) :
                r1 = random.uniform(0,1)
                r2 = random.uniform(0,1)
                # update the velocity vector
                particle.velocity = self.inertia*particle.velocity+\
                                    r1*self.c1*(particle.best_pos - particle.position) +\
                                    r2*self.c2*(self.best_pos_swarm - particle.position)

                # checking the range of the velocity vector
                for vel in particle.velocity:
                    if  vel < self.VMIN :
                        vel = self.VMIN
                    elif vel > self.VMAX :
                        vel = self.VMAX

                # update the position of the particle
                particle.position += particle.velocity 

                for  pos in particle.position:
                    if  pos < self.MIN or pos > self.MAX  :
                        pos = random.uniform(self.MIN,self.MAX)
                        
                self.poses[i,j] = particle.position


                # update the best_fitness and best_position of the particle 
                if particle.fitness < particle.best_fitness:
                    particle.best_fitness = particle.fitness
                    particle.position = particle.best_position
                self.fitnesses[i,j] = particle.fitness
                # update the global best fitness and global best position
                if particle.fitness < self.best_fitness_swarm :
                    self.best_fitness_swarm = particle.fitness
                    self.best_position_swarm     = particle.position

            self.all_best[i] = self.best_fitness_swarm

    def GetPoses(self):
        # export an array of positiones for all paricles within each generation
        return self.poses

    def GetFitness(self):
        # export an array of fitness for all paricles within each generation
        return self.fitnesses
    def GetAll(self):
        return self.all_best


