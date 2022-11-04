import pygame
import random
from defs import *
class Cactus:
    def __init__(self, window, catcus_type) -> None:
        self.window = window
        self.state = CATCUS_MOVING
        self.img = pygame.image.load(catcus_type)
        self.rect = self.img.get_rect()
        self.speed = 2
        self.set_position(CATCUS_X, CATCUS_Y)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
    
    def check_status(self):
        if self.rect.right<0:
            self.state = CATCUS_DONE

    def tick(self, dx):
        self.rect.centerx += dx
    
    def render(self):
        self.window.blit(self.img, self.rect)

    def alltick(self, dt):
        if self.state == CATCUS_MOVING:
            self.tick(-(60/dt*self.speed))
            self.render()
            return self.check_status()
        return CATCUS_DONE
        
class CactusHandler:
    def __init__(self, window) -> None:
        self.window = window
        self.add = 30
        self.time = 0
        self.cactuses = []
    
    def tick(self, dt):
        self.time += 4/dt

        rm = []
        for c in self.cactuses:
            s = c.alltick(dt)
            if s == CATCUS_DONE:
                rm.append(c)
        for x in rm:
            self.cactuses.remove(x)

    def append(self):
        self.cactuses.append(Cactus(self.window, random.choice([CATCUS_T_0, CATCUS_T_1, CATCUS_T_2])))
