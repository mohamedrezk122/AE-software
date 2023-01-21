import pygame 
from pygame.locals import *



class Panel:

    def __init__(self ,surface, color,width , height, pos_x, pos_y = 0):

        self.height = height
        self.width  = width
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.surface= surface
        self.color  = color

    def draw(self):
        
        self.add_text(  "Readings" , 50  , self.pos_y , "horizental" )
 
    def add_field(self, text ,var, num):

        field_height = 70
        pygame.draw.rect(self.surface, self.color[num%2==0], (self.pos_x, (num-1)*field_height , self.width , field_height))

        self.add_text(  text+ " : " + str(var) ,
                        30  , align="vertical" ,
                        rect_y= (num-1)*field_height,
                        rect_height = field_height )

    def add_text(   self, txt ,
                    f_size ,
                    rect_y ,
                    align = "vertical" , 
                    rect_height = 0 ):


        font = pygame.font.SysFont("monospace", f_size,bold=True)
        text = font.render( txt, True , '#FFFFFF')
        w = text.get_width()
        h = text.get_height()

        if align == "vertical" :
            y =  rect_y + (rect_height - h)*.5
            x =  self.pos_x + 20

        elif align == "horizental" :
            x = self.pos_x + (self.width - w)*.5
            y = self.pos_y

        self.surface.blit(text , (x,y))
