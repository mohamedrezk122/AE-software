import pygame 
from pygame.locals import *
import sys
import time 
import random
import os 
import numpy as np 
from globals import * 
from sensor import Sensor
from grid import Grid
from panel import Panel
from button import Button
from simplex_optimization import *
 

clock = pygame.time.Clock()
pygame.display.set_caption("Demo")

screen = pygame.display.set_mode((WIDTH, HEIGHT))

x = sensor_StartPos - sensor_GridSize*random.random()
y = sensor_StartPos - sensor_GridSize*random.random()


sensor1 =   Sensor( sensor_StartPos - sensor_GridSize,
                    sensor_StartPos ,1,
                    screen , red)

sensor2 =   Sensor( sensor_StartPos,
                    sensor_StartPos ,2,
                    screen,blue)

sensor3 =   Sensor( sensor_StartPos,
                    sensor_StartPos - sensor_GridSize ,3,
                    screen,green)

sensor4 =   Sensor( sensor_StartPos - sensor_GridSize ,
                    sensor_StartPos - sensor_GridSize ,4,
                    screen,purple)


ShowSource_button   = Button( WIDTH - HEIGHT -40 ,
                            button_height,
                            (panel_x+20,  HEIGHT-200), 
                            "Create Source" , 
                            screen ,button_bg ,
                            red2)

Estimate_button     = Button( WIDTH - HEIGHT -40 ,
                            button_height,
                            (panel_x+20,  HEIGHT-130), 
                            "Estimate Pos" , 
                            screen ,button_bg ,
                            blue )

panel = Panel(  screen,
                [bg_color, border_color],
                WIDTH - HEIGHT ,
                HEIGHT-50,
                panel_x)


Sensor_Array = [sensor1 , sensor2 ,sensor3 , sensor4]


def show_source(x,y):
    pygame.draw.circle(screen , red , (x,y), 5)
    pygame.display.flip() 


def show_EstimatedSource(source_pos , sensor_array):

    for sensor in sensor_array:
        pygame.draw.line(screen, white , (sensor.cpos),(source_pos),3)
    
    pygame.draw.circle(screen , white ,(source_pos),15,2)


def simplex(best,other,worst):
    pygame.draw.circle(screen, green, (best),10,2)
    pygame.draw.circle(screen, blue, (other),10,2)
    pygame.draw.circle(screen, red, (worst),10,2)
    pygame.draw.line(screen, white , (best),(other),3)
    pygame.draw.line(screen, white , (worst),(other),3)
    pygame.draw.line(screen, white , (best),(worst),3)


h = 2
d = 0 
so2= SimplexOptimze(objective)
sol2 = so2.x
poss2 = so2.GetPoses()
i = 0
def draw_stuff(i):
    global h ,d
    screen.fill(bg_color)
    Grid(20,20, HEIGHT , HEIGHT,screen,border_color)

    # h += 1

    # f  =   random.randint( 200 , 500)
    # b =   random.randint( 200 , 500)
    # show_EstimatedSource((f,b), Sensor_Array)
    # d += 1

    for sensor in Sensor_Array:
        sensor.draw()

    panel.draw()
    # panel.add_field("Acc" , h, 2)
    # panel.add_field("Trials" , h, 3)

    # ShowSource_button.draw()

    # if ShowSource_button.perm_pressed:
    #     show_source(x,y)

    # Estimate_button.draw()
    simplex(poss2[i][0], poss2[i][1], poss2[i][2])

def main():

    i = 0
  
    while True :

        draw_stuff(i)
        i+=1

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                quit()
                sys.exit()


        pygame.display.update()
        clock.tick(60)
        

if __name__ == "__main__":

    pygame.init()
    pygame.font.init()
    main()              