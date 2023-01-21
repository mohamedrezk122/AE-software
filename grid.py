import pygame 
from pygame.locals import *

def Grid(rows , cols , s_width , s_height , surface ,color):

	width  = s_width // cols
	height = s_height // rows

	for i in range(rows):
		for j in range(cols):

			pygame.draw.rect(surface, color, (i*width,j*height ,
												width ,height) , 1 ,4)

