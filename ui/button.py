import pygame, sys, time 
from pygame.locals import *

pygame.font.init()

class Button:
    def __init__(   self,width,height,
                    pos,text, screen, 
                    color_inactive ,
                    color_active  ,  
                    func =None , *args):

        self.func =func
        self.args = args
        self.pressed = False
        self.elevation = 2
        self.dynamic_elecation = 2
        self.original_y_pos = pos[1]
        self.screen = screen
        self.acolor = color_active
        self.incolor = color_inactive

        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = self.incolor
        self.text_color = "#FFFFFF"

        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = self.incolor
        self.text = text
        font = pygame.font.SysFont("monospace", 30 ,bold =True)
        self.text_surf = font.render(text,True,self.text_color)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        self.perm_pressed = False

    def draw(self):

        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(self.screen,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(self.screen,self.top_color, self.top_rect,border_radius = 12)
        self.screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = self.acolor
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                self.perm_pressed = True
                # return True

            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False

                  
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = self.incolor
            # return False

