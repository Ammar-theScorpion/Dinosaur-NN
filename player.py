import random
import pygame
from nnet import Nnet
from defs import *
import numpy as np

class Player:
    def __init__(self, window) -> None:
        self.window = window
        self.state = DINO_S_R
        self.img = [pygame.image.load(DINO_RUN0), pygame.image.load(DINO_RUN1), pygame.image.load(DINO_DUCK0), pygame.image.load(DINO_DUCK1), pygame.image.load(DINO_JUMP)]
        self.rect = self.img[0].get_rect()
        self.speed = 8
        self.time = 0
        self.index = 1
        self.fitness = 0
        self.time_lived = 0
        self.shift = 7
        self.current = self.state
        self.set_position(DINO_X, DINO_Y)

        self.nnet = Nnet(NUM_INPUT, NUM_HID, NUM_OUTPUT)

    def reset(self):
        self.state = DINO_S_R
        self.speed = 8
        self.time = 0
        self.index = 1
        self.fitness = 0
        self.time_lived = 0
        self.shift = 7
        self.set_position(DINO_X, DINO_Y)


    def set_position(self, x, y):
        self.rect.centerx = x
        self.rect.centery = y
    
    def jump(self):
        self.state = DINO_S_J

    def duck(self):
        self.current = DINO_S_D
        self.state = DINO_S_D

    def run(self):
        self.set_position(DINO_X, DINO_Y)
        self.state = DINO_S_R
        self.current = DINO_S_R

    def check_staus(self, bk_rect, catus, birds):
        if self.rect.colliderect(bk_rect):
            self.speed = 8
            self.state = self.current
        self.check_hit(catus, birds)

    def check_hit(self, catus, birds):
        for c in catus:
            if self.rect.colliderect(c.rect):
                self.state = DINO_DEAD
        for b in birds:
            if self.rect.colliderect(b.rect):
                self.state = DINO_DEAD

    def tick(self, dt):
        self.time += 10/dt
            
        if self.state == DINO_S_J:
            
            if self.speed>0:
                F = (0.5*1*(self.speed**2))
            else:
                F = -(0.5*1*(self.speed**2))
            
            self.speed-=0.3
            self.rect.centery -= F
        
        elif self.state == DINO_S_D:
            self.set_position(DINO_X, DINO_Y+55)



    def render(self):
        pygame.draw.rect(self.window, (25,0,0), self.rect)
        self.window.blit(self.frame(), self.rect)


    def alltick(self, dt, bg_rect, catcus, birds):
        if self.state != DINO_DEAD:
            input = self.get_input(catcus, birds)
            value = self.nnet.get_max_output(input)
            if value>=0.5:
                self.jump()
            elif value>=0.35:
                self.duck()
            self.tick(dt)
            self.check_staus(bg_rect, catcus, birds)
            self.render()
            self.time_lived += dt/1000

    def frame(self):
        if self.time>=self.shift:
            self.index = not self.index
            self.time = 0
        if self.state == DINO_S_J:
            return self.img[-1]
        return self.img[self.index+self.state]


    def get_input(self, catus, birds):
        closest = WIDTH*2
        closesty = 0
        gap = closest
        for i, c in enumerate(catus):
            if c.rect.right<self.rect.left:
                self.fitness+=1
            if c.rect.right<closest and c.rect.right>self.rect.left:
                closest = c.rect.right
                closesty = c.rect.centery
                if i<len(catus)-1:
                    gap = catus[i+1].rect.left
        for i, c in  enumerate(birds):
            if c.rect.right<self.rect.left:
                self.fitness+=1
            if c.rect.right<closest and c.rect.right>self.rect.left:
                closest = c.rect.right
                closesty = c.rect.centery
                if i<len(birds)-1:
                    gap = birds[i+1].rect.left


        horizontal_dis = closest-self.rect.centerx
        virtical_dis = abs(closesty-self.rect.centery)
        gap = gap-horizontal_dis
        inputs = [
            ((horizontal_dis/WIDTH)*0.99)+0.01,
            ((virtical_dis/HEIGTH)*0.99)+0.01,
            ((gap/WIDTH)*0.99)+0.01
        ]
        return inputs

    def create_offspring(p1, p2, window):
        dino = Player(window)
class PlayerHandler:
    def __init__(self, window) -> None:
        self.window = window
        self.dinos = []
        self.create_generation()

    def create_generation(self):
        self.dinos = []
        for i in range(GENERATION_SIZE):
            self.dinos.append(Player(self.window))
    
    def tick(self, dt, bg_rect, catcus, birds):
        num_alive = 0
        for b in self.dinos:
            b.alltick(dt, bg_rect, catcus, birds)

            if b.state != DINO_DEAD:
                num_alive += 1

        return num_alive

    def evolve_population(self):
        for b in self.dinos:
            b.fitness += b.time_lived 
        self.dinos.sort(key=lambda x: x.fitness, reverse=True)

        for b in self.dinos[0:10]:
            print('fitness:', b.fitness)

        self.create_generation()