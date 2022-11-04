import pygame
from bird import BirdHandler
from player import PlayerHandler
from cactus import CactusHandler
from defs import *
import random
def update_label(data, title, font, x, y, window):
    label = font.render('{} {}'.format(title, data), 1, DATA_FONT_COLOR)
    window.blit(label, (x, y))
    return y

def update_data_labels(gameDisplay, dt, game_time, num_iterations, num_alive, font):
    y_pos = 10
    gap = 20
    x_pos = 10
    y_pos = update_label(round(1000/dt,2), 'FPS', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(round(game_time/1000,2),'Game time', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_iterations,'Iteration', font, x_pos, y_pos + gap, gameDisplay)
    y_pos = update_label(num_alive,'Alive', font, x_pos, y_pos + gap, gameDisplay)


def run():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGTH))
    pygame.display.set_caption("Dino")
    p = PlayerHandler(window)

    bg_rect = pygame.Rect(DINO_X-10, DINO_Y+DINO_H, 30, 30)

    running = True
    label_font = pygame.font.SysFont("monospace", DATA_FONT_SIZE)

    catcus = CactusHandler(window)
    birds = BirdHandler(window)

    clock = pygame.time.Clock()
    dt = 0
    game_time = 0
    add = 30
    time = 0
    num_iterations = 1
    while running:
        dt = clock.tick(FPS)
        game_time+=dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        window.fill((255, 255, 255))

        catcus.tick(int(dt-game_time/9000))
        if game_time>=2000:
            birds.tick(int(dt-game_time/9000))
        temp = random.randint(0,1)

        time += 4/dt

        if time >= add:
            add = random.randint(40, 100)
            time = 0

            if temp and game_time>=20000:
                birds.append()
            else:
                catcus.append()
        num_alive = p.tick(int(dt-game_time/9000), bg_rect, catcus.cactuses, birds.cactuses)
        if num_alive == 0:
            game_time = 0
            num_iterations += 1
            p.evolve_population()
            birds.cactuses=[] 
            catcus.cactuses=[]
        
        update_data_labels(window, dt, game_time, num_iterations, num_alive, label_font)
        pygame.display.update()

if __name__ == '__main__':
    run()


'''
import random
from re import S
import pygame
import math

pygame.font.init()  # init font
STAT_FONT = pygame.font.SysFont("comicsans", 50)
gen=1
image = pygame.image.load('CpQSF.png')
background_image = image.subsurface((0, 96, 2400,31))
dino_0 = image.subsurface((1340, 0, 83, 96))
dino_1 = image.subsurface((1518, 0, 83, 96))
dino_2 = image.subsurface((1602, 0, 83, 96))
dino_3 = image.subsurface((1865, 34, 117, 57))
dino_4 = image.subsurface((1984, 34, 117, 57))

dino_d = image.subsurface((1694, 0, 83, 96))
catcs_0 = image.subsurface((653, 0, 47, 100))
catcs_1 = image.subsurface((802, 0, 47, 100))
catcs_2 = image.subsurface((903, 0, 47, 100))
bird_1 = image.subsurface((260, 15, 90, 62))
bird_2 = image.subsurface((354, 15, 90, 55))
catcs_list = [catcs_1, catcs_0, catcs_2, bird_1, bird_2]
width, height = 1280, 720
background_height = 400
bk_bounds = pygame.Rect(0, background_height+90, 2400, 31)

window = pygame.display.set_mode((width, height))
tiles = math.ceil(background_image.get_width()/width)+1
class Dino:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
        self.is_duck = False
        self.animation_time = 4
        self.counter = 0
        self.index=0
        self.score = 0
        self.v=0
        self.V = 8
        self.is_jump = False
        self.img = [dino_0, dino_1, dino_2, dino_3, dino_4]
        self.bounds = pygame.Rect(self.x+20, self.y+30, 60, 82)

    def collide(self, img):
        return self.bounds.colliderect(img)

    def render(self):
        window.blit(self.img[self.index], (self.x, self.y))
    def jump(self):
        if not self.is_jump:
            self.V = 8
            self.v = 8
        self.is_jump = True
        self.bounds = pygame.Rect(self.x+20, self.y+20, 60, 82)
    def short_jump(self):
        if not self.is_jump:
            self.V = 6.5
            self.v = 6.5
        self.is_jump = True


    def duck(self):
        if self.index<3:
            self.y = background_height+55
            self.index = 3
            self.bounds.w = 85
            self.bounds.y=  self.y
            self.h = 10

        self.is_duck = True

    def scoref(self, bounds):
        if bounds.x<self.bounds.x:
            self.score+=1
            return True
        return False
       
    def tick(self):
        if self.is_duck:
            self.counter+=1
            if self.counter >= self.animation_time:
                self.index+=1
                self.counter=0
            if self.index>len(self.img)-1:
                self.index = 3
        else:
            if self.is_jump:
                self.index = 0
                if self.v>0:
                    F = (0.5*1*(self.v**2))
                else:
                    F = -(0.5*1*(self.v**2))

                self.y-=F
                self.v-=0.5
                self.bounds.y = self.y
            if self.bounds.colliderect(bk_bounds):
                self.is_jump = False
                self.v = self.V
            
            if not self.is_jump:
                if self.counter>= self.animation_time:
                    self.index+=1
                    self.counter=0
                if self.index>2:
                    self.index = 0
                self.counter+=1
        
        

        
class Catcs:
    def __init__(self, x, y, img, w=44, h=95) -> None:
        self.x = x
        self.y = y
        self.img = img
        self.bounds = pygame.Rect(self.x+10, self.y+10, w-10, h-20)
        self.passed = False
    def render_catcs(self,  scroll):
        window.blit(self.img, (self.x, self.y))
        self.x+=scroll
        self.bounds.x = self.x+7

    def tick(self):
        if self.bounds.x<100:
            return True
        return False
        

def render_background(scroll):
    for i in range(0, tiles):
        limit = 100+i*background_image.get_width()+scroll
        if limit<100:
            window.blit(background_image, (limit, background_height+80))
def render(scroll):
    window.fill((255, 255, 255))
    render_background(scroll)

def main(genomes, config):
    dino = []
    global gen
    gen+=1
    nets = []
    ge = []
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        dino.append(Dino(150, background_height+10))
        nets.append(net)
        ge.append(genome)



    catcs = [Catcs(1500, background_height+10, catcs_0), Catcs(2000, background_height+10, catcs_0)]
    time = 50
    counter_time = 0
    inc = 1
    d = False

    score = 0

    clock = pygame.time.Clock()
    running = True
    scroll = 0
    s = -8
    n = False
    while running and len(dino) > 0:
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
        rem = []
    
        render(s)
        score+=1*inc

        index = 0
        score_label = STAT_FONT.render("Score: " + str(score),1,(0,0,0))
        window.blit(score_label, (width - score_label.get_width() - 15, 10))
        score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(0,0,0))
        window.blit(score_label, (10, 10))
        for c in range(len(catcs)):
            for d in dino:
                if d.scoref(catcs[c].bounds):
                    for genome in ge:
                        genome.fitness += 2
                    index = c
            if catcs[c].tick():
                rem.append(catcs[c])

        for x, d in enumerate(dino):
            ge[x].fitness+=0.1
            d.render()
            dec = 1
            if index<len(catcs):
                pygame.draw.rect(window, (255,0,0 ), catcs[index].bounds)
                gap = 0
                if index+1<len(catcs):
                    gap = abs(catcs[index].x - catcs[index+1].x) 
                output = nets[dino.index(d)].activate((d.y, catcs[index].y, abs(d.x - catcs[index].x), gap, s ))
                dec = output.index(max(output))
            if dec == 0:
                d.is_duck = False
                pass
            elif dec == 3:
                d.duck()
            elif dec == 1:
                d.is_duck = False
                d.short_jump() 
            elif dec == 2:
                d.is_duck = False
                d.jump() 
            
  

            d.tick()
            if keys[pygame.K_UP] or keys[pygame.K_SPACE]:
                d.short_jump()
            if keys[pygame.K_DOWN]:
                d.duck()
                d = True
            elif d:
                 
                d.is_duck = False
                d =False
        scroll+=s




        

        if counter_time >= time:
           
            img = random.choice(catcs_list)
            h = background_height+10
            if img == bird_1 or img == bird_2:
                h=random.choice([h, h-25, h-45, h-60, h-120]  )
            ca = Catcs(random.randint(1600, 2000) , h, img, img.get_width(), img.get_height() )
            if len(catcs) :
                ca.x+=catcs[-1].x//2
            if len(catcs)<3:
                catcs.append(ca)
            counter_time = 0
            time = random.randint(40, 100)
            inc = random.randint(1, 5) 
            s-=(0.1)
         
        for r in rem:
            catcs.remove(r)

        for c in catcs:
            c.render_catcs(s)
            for b in dino:
                if b.collide(c.bounds):
                    rem.append(b)
                    ge[dino.index(b)].fitness -= 1
                    nets.pop(dino.index(b))
                    ge.pop(dino.index(b))
                    dino.pop(dino.index(b))
        counter_time+=inc
        pygame.display.update()

def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(main, 900)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
'''