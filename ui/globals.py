import numpy as np 
# screen dimensions
WIDTH = 1200
HEIGHT = 900


# some colors
green          = '#00EE76'
purple         = '#836FFF'
red 	       = '#CD0000'
red2           = '#E44337'
blue	       = '#1C86EE'
bg_color       = '#343434'
border_color   = '#6B6464'
button_bg      = '#222222'  
white          = '#FFFFFF'
# some constants
sensor_StartPos = 600 
sensor_GridSize = 480

button_height = 50
panel_x = HEIGHT


# physical constants

grid_scale 		= 1/4    	 # in cm 
grid_max        = 15         # in cm 
grid_min        = 0
velocity 	    = 300000	 # in cm/s for fiberglass 

# sensor pos in cm 
S1  = 	(grid_min,grid_min)
S2	=	(grid_max,grid_min)
S3  = 	(grid_max,grid_max)
S4  = 	(grid_min,grid_max)


