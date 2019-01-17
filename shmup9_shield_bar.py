# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#this is a comment
import pygame
#import os
import sys
import random
from os import path

img_dir = path.join(path.dirname(__file__),'img')
sound_dir = path.join(path.dirname(__file__),'sound')

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
YELLOW = (255,255,0)

#NOW THE INITIALIZING SECTION
pygame.init()
pygame.mixer.init()  #needed for game sounds

#defining the screen for gameplay
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shmup")
clock = pygame.time.Clock()

#defining a function to draw text into the screen as it is needed again and again
font_name = pygame.font.match_font('Arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name,size)
    text_sur = font.render(text, True, WHITE)
    text_rect = text_sur.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_sur,text_rect)
    

#creating the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.score=0    ->no longer required we add a new score to this game based on radius

        #scaling the image
        self.image = pygame.transform.scale(player_img, (50,35))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20#testing down
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-10
        self.xspeed = 0  #inititally speed in x direction 0
        self.shield = 100 #adding shield life
        self.shoot_delay=250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        self.xspeed=0  # the player should not move simply without keypress
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
            self.xspeed = -5
        if keystate[pygame.K_RIGHT]: #checking right key pressed
            self.xspeed = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        #if a key is needed for left press use pygame.K_a similarly k_d for d key
        self.rect.x += self.xspeed

    def shoot(self):
            now = pygame.time.get_ticks()
            if (now-self.last_shot)> self.shoot_delay :
                self.last_shot = now
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()

#generic name for objects that move around in game is mob
#the red pieces falls down from the sky
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig= random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        #spawn from the top of window
        self.rect.x = random.randrange(0,WIDTH-self.rect.width)
        self.rect.y = random.randrange(-150,-100)#randomly scattered
        self.yspeed = random.randrange(1,8)
        self.xspeed = random.randrange(-3,3)
        self.rot = 0
        self.rot_speed = random.randrange(-10,10)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 40: #checking the time period for rotating
            self.last_update = now
            '''Do not do this
            self.image = pygame.transform.rotate(self.image, self.rot_speed)
            because it causes the meteor to be deformed and game lags very much
            because each time the image loses a bit of info in ne rotate
            '''
            self.rot=(self.rot + self.rot_speed) % 360
            #creating animation for smooth rotation
            #for each rotation new rectangle is found so that it fits to the rotating image
            new_image = pygame.transform.rotate(self.image_orig, self.rot) 
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        #rotating the meteor
        self.rotate()
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
        

#creating a sprite for bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y): #bullets are spawned at a particular point from player
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.yspeed=-10

    def update(self):
        self.rect.y += self.yspeed
        #kill the sprite
        if self.rect.bottom < 0:
            self.kill()

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf,x,y,percent):
    if percent<0:
        percent=0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percent/100)*BAR_LENGTH
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    pygame.draw.rect(surf,GREEN,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,2)

#load all graphics
background = pygame.image.load(path.join(img_dir, "starfield.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,"playerShip2_blue.png")).convert()
#meteor_img = pygame.image.load(path.join(img_dir,"meteorBrown_big3.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir,"laserBlue03.png")).convert()
meteor_images = []

meteor_list = ['meteorBrown_big1.png','meteorBrown_big2.png','meteorBrown_big3.png',
'meteorBrown_big4.png','meteorBrown_med1.png','meteorBrown_med3.png',
'meteorBrown_small1.png','meteorBrown_small2.png','meteorBrown_tiny1.png',
'meteorGrey_big2.png','meteorGrey_big4.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())

#------------------------------
#load all game sounds
shoot_sound = pygame.mixer.Sound(path.join(sound_dir,"Laser_Shoot.wav"))
ship_expl_sound = pygame.mixer.Sound(path.join(sound_dir,"ship_explosion.wav"))
met_expl_sound = pygame.mixer.Sound(path.join(sound_dir,"explosion.wav"))
pygame.mixer.music.load(path.join(sound_dir,"background_music.mp3"))
pygame.mixer.music.set_volume(0.3)


all_sprites = pygame.sprite.Group()
#mob group created inorder to contain mobs such that collisions are working
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(10):
    newmob()

#creating score variable
score=0

pygame.mixer.music.play(loops=-1)  #loops=-1 tells to loop around over and over again
#game loop
running=True
while running:
    clock.tick(FPS)
    #process inputs
    for event in pygame.event.get():
        #checking if close button is clicked
        if event.type==pygame.QUIT:
            running = False
    
    #update
    all_sprites.update()
    #check to see if a bullet hit mob
    hits= pygame.sprite.groupcollide(mobs,bullets,True,True)# if bul hits mob both of them gets killed
    #after this we have to rejuvenate the mobs died
    for hit in hits:
        met_expl_sound.play()
        score += 50 - hit.radius
        newmob()
           
    '''Check to see if the mob hits the player
    spritecollide returns a list'''
    hits = pygame.sprite.spritecollide(player,mobs,True, pygame.sprite.collide_circle)#true implies shield is there
    for hit in hits:
        player.shield-=hit.radius*2
        ship_expl_sound.play()
        if player.shield<=0:
            running=False

    #draw/render
    screen.fill(BLACK)
    #draw background
    screen.blit(background, background_rect) #copy the pixels from one to another thing
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,(WIDTH/2),10)
    draw_shield_bar(screen,5,5,player.shield)
    pygame.display.flip()

print(score)
pygame.quit()
sys.exit()

