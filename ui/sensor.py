import pygame 
from pygame.locals import *




class Sensor(pygame.sprite.Sprite):

    def __init__(self , pos_x , pos_y, sensor_number, surface, color) : 

        super().__init__()
        self.sensor_number = sensor_number
        self.width   =  50
        self.height  = 50
        # self.image   = pygame.Surface([self.width, self.height])
        #self.image.fill(color)
        self.surface = surface
        self.color   = color
        self.pos_x   = pos_x 
        self.pos_y   = pos_y
        self.cpos    = pos_x+self.width/2,pos_y+self.height/2
        self.rect    = pygame.Rect(self.pos_x , self.pos_y , self.width , self.height)

        # pygame.draw.rect(self.image , self.color , self.rect , border_radius = 4)
        #self.add_text(f"S{self.sensor_number}")
        

    def draw(self):

        pygame.draw.rect(self.surface , self.color , self.rect , border_radius = 4)
        self.add_text(f"S{self.sensor_number}")

    def add_text(self ,txt):

        font = pygame.font.SysFont("monospace", 30,bold=True)
        text = font.render( txt, True , '#FFFFFF')
        w = text.get_width()
        h = text.get_height()
        self.surface.blit(text ,(self.pos_x + ((self.width - w)*.5) ,
                                (self.pos_y + ((self.height- h)*.5))))


