# created by max lux 

# KidsCanCode - Game Development with Pygame video series
# Jumpy! (a platform game) - Part 2
# Video link: https://www.youtube.com/watch?v=8LRI0RLKyt0
# Player movement
# © 2019 KidsCanCode LLC / All rights reserved.

# Week of march 23 - Lore
# Modularity, Github, import as
# Modularity is file dependencies
# Classes, methods, functions, data types, ...


#So everything in my code was broken and I was having trouble trying to 

import pygame as pg
from pygame.sprite import Group
# from pg.sprite import Group
import random

# some settings
TITLE = "PLATFORM"
WIDTH = 470
HEIGHT = 600
FPS = 60

# environment 
GRAVITY = 9.8

# Player properties
PLAYER_ACC = 1.0
PLAYER_FRICTION = -0.03
PLAYER_JUMPPOWER = 20

# all the colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

#the new color 
LIGHTYELLOW = (255, 255, 150)



import pygame as pg
from pygame.sprite import Sprite
from settings import *
vec = pg.math.Vector2



class Player(Sprite):
    # include game parameter to pass game class as argument in main...
    def __init__(self, game):
        Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((30, 40))
        self.image.fill(LIGHTYELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 4, HEIGHT / 4)
        self.pos = vec(WIDTH / 4, HEIGHT / 4) 
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.hitpoints = 100
    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits: 
            self.vel.y = -15
    def update(self):
        self.acc = vec(0, 0.5)
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_d]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_w]:
            pass
            # self.acc.y = -PLAYER_ACC
        if keys[pg.K_s]:
            self.acc.y = PLAYER_ACC
        # ALERT - Mr. Cozort did this WAY differently than Mr. Bradfield...
        if keys[pg.K_SPACE]:
            self.jump()
        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # self.acc.y += self.vel.y * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        if self.pos.y > HEIGHT:
            self.pos.y = 0

        self.rect.midbottom = self.pos
class Platform(Sprite):
    def __init__(self, x, y, w, h):
        Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vx = 1
    def blitme(self, x, y):
        self.screen.blit(self.image, (x, y))
    def update(self):
        pass





# DA health bar
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

    if pct == 0: 
        print ("GAME OVER") # Proud that I did this but I am not sure how to put it on screen 
      # create the display surface object 
# of specific dimension..e(X, Y). 

    

class Game:
    def __init__(self):
        # initialize game window, etc
            pg.init()
            pg.mixer.init()
            self.screen = pg.display.set_mode((WIDTH, HEIGHT))
            pg.display.set_caption(TITLE)
            self.clock = pg.time.Clock()
            self.running = True

    def new(self):
        # start a new game
        self.all_sprites = Group()
        self.platforms = Group()
        self.player = Player(self)
        self.all_sprites.add(self.player)
        ground = Platform(0, HEIGHT-40, WIDTH, 40)
        plat1 = Platform(200, 400, 150, 20)
        plat2 = Platform(150, 300, 150, 20)
        plat3 = Platform(10, 200, 400, 20)
        self.all_sprites.add(ground)
        self.platforms.add(ground)
        self.all_sprites.add(plat1)
        self.platforms.add(plat1)
        self.all_sprites.add(plat2)
        self.platforms.add(plat2)
        # you need to add new instances of the platform class to groups or it wont update or draw
        self.all_sprites.add(plat3)
        self.platforms.add(plat3)
        for plat in range(1,10):
            plat = Platform(random.randint(0, WIDTH), random.randint(0, HEIGHT), 200, 20)
            self.all_sprites.add(plat)
            self.platforms.add(plat)
        self.run()


    def run(self):
        # Game Loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()
        hits = pg.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            if self.player.rect.top > hits[0].rect.top:
                print("i hit my head")
                self.player.vel.y = 15 #I tried playing with this and set it to 100 weird...wouldn't recommend
                self.player.rect.top = hits[0].rect.bottom + 5 #don't know exactly what this does
                self.player.hitpoints -= 20 #takes more health away higher stakes
                print("hitpoints are now " + str(self.player.hitpoints))
                # print(self.player.hitpoints)
            # print("it collided")
            else:
                self.player.vel.y = 0
                self.player.pos.y = hits[0].rect.top+1
            

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            #  the windo closing check 
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # Game Loop - draw
        self.screen.fill(GREEN)
        self.all_sprites.draw(self.screen)
        draw_player_health(self.screen, 10, 10, self.player.hitpoints/100)
        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        # game splash/start screen
        pass

    def show_go_screen(self):
        # game over/continue
        pass

g = Game()
# g.show_start_screen()
while g.running:
    g.new()
    # g.show_go_screen()

pg.quit()