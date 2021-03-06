# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#this is a comment
import pygame
import os
import sys
import random

#for the window
WIDTH = 480
HEIGHT = 600
FPS = 60   #so game doesnt lag and be smooth

#defining colours
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)

#NOW THE INITIALIZING SECTION
pygame.init()
pygame.mixer.init()

#defining the screen for gameplay
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shmup")
clock = pygame.time.Clock()

#creating the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((50,40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.speedx = 0  #inititally speed in x direction 0

    def update(self):
        self.speedx=0  # the player should not move simply without keypress
        #ususally this done but here borders should be walls and cannot go through them
        '''if self.rect.left>WIDTH:
            self.rect.right=0
        if self.rect.right<0:
            self.rect.left=WIDTH'''
        #crewating wall effect
        if self.rect.right>WIDTH:
            self.rect.right=WIDTH
        if self.rect.left<0:
            self.rect.left=0

        keystate = pygame.key.get_pressed() #-> this function returns a list of keys pressed
        if keystate[pygame.K_LEFT]:  #checking left key pressed
            self.speedx = -5
        if keystate[pygame.K_RIGHT]: #checking right key pressed
            self.speedx = 5
        #if a key is needed for left press use pygame.K_a similarly k_d for d key
        self.rect.x += self.speedx


#generic name for objects that move around in game is mob
#the red pieces falls down from the sky
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        #spawn from the top of window
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-100,-40)#randomly scattered
        self.yspeed = random.randrange(1,8)
        self.xspeed = random.randrange(-3,3)

    def update(self):
        self.rect.y+=self.yspeed
        self.rect.x+=self.xspeed
        if self.rect.top > HEIGHT+10: #if it goes down the screen
            self.rect.x = random.randrange(0,WIDTH-self.rect.width)
            self.rect.y = random.randrange(-100,-40)#randomly scattered
            self.yspeed = random.randrange(1,8)
        if self.rect.left>(WIDTH-self.rect.width):
            self.xspeed = -(self.xspeed)
        if self.rect.right<(self.rect.width):
            self.xspeed = -(self.xspeed)


all_sprites = pygame.sprite.Group()
#mob group created inorder to contain mobs such that collisions are working
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

#game loop
running=True
while running:
    clock.tick(FPS)
    #process inputs
    for event in pygame.event.get():
        #checking if close button is clicked
        if event.type==pygame.QUIT:
            running = False
        #checking for key sprites
    
    #update
    all_sprites.update()
    #draw/render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    
    pygame.display.flip()
    
    
pygame.quit()
sys.exit()

