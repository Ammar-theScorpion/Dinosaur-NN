import pygame
import random
from defs import *
class Bird:
    def __init__(self, window, y) -> None:
        self.window = window
        self.state = CATCUS_MOVING
        self.img = [pygame.image.load(BIRD_0), pygame.image.load(BIRD_1)]
        self.rect = self.img[0].get_rect()
        self.speed = 2
        self.index = 0
        self.time = 0
        self.shift = 90
        self.set_position(CATCUS_X, CATCUS_Y+y)

    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
    
    def check_status(self):
        if self.rect.right<0:
            self.state = CATCUS_DONE

    def frame(self):
        if self.time>=self.shift:
            self.time = 0
            self.index = not self.index
        return self.img [self.index]

    def tick(self, dx):
        self.rect.centerx += dx

    
    def render(self, dt):
        self.time+=dt
        self.window.blit(self.frame(), self.rect)

    def alltick(self, dt):
        if self.state == CATCUS_MOVING:
            self.tick(-(60/dt*self.speed))
            self.render(dt)
            return self.check_status()
        return CATCUS_DONE
        
class BirdHandler:
    def __init__(self, window) -> None:
        self.window = window
        self.add = 50
        self.time = 0
        self.cactuses = []
    
    def tick(self, dt):
        rm = []
        for c in self.cactuses:
            s = c.alltick(dt)
            if s == CATCUS_DONE:
                rm.append(c)
        for x in rm:
            self.cactuses.remove(x)

    def append(self):
        self.cactuses.append(Bird(self.window, random.choice([0, -80, -175])))
