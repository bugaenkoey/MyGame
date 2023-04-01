import random
from os import listdir 
import pygame
from pygame.constants import QUIT,K_DOWN,K_UP,K_LEFT,K_RIGHT,K_ESCAPE

pygame.init()
FPS = pygame.time.Clock()

Red     = 255,0,0
Green   = 0,255,0
Blue    = 0,0,255
Yellow  = 255,255,0
Blue    = 0,255,255
Magenta = 255,0,255
Black   = 0,0,0
# colors = [Red,Green,Blue,Yellow,Blue,Magenta,Black]
# font = pygame.font.SysFont('Verdana',20)
# font = pygame.font.SysFont('chalkduster.ttf', 72)
font = pygame.font.SysFont(None, 32)

screen = width, heigth = 800,600

color = Yellow
background_color = Black

main_surface = pygame.display.set_mode(screen)

IMGS_PATH ='goose'
# player = pygame.Surface((20,20))
# player.fill(color)
player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()
player_speed = 5

def create_enemy():
    enemy_size = 100,33
    enemy_img = pygame.image.load('enemy.png').convert_alpha()
    enemy = pygame.transform.scale(enemy_img,enemy_size)    
    enemy_rect = pygame.Rect(width-50,random.randint(200,heigth-200), *enemy.get_size())
    enemy_speed = random.randint(2,5)
    return [enemy,enemy_rect,enemy_speed,enemy.get_size(),enemy_img]

def create_bonus():
    bonus_size = 70,70
    bonus_img = pygame.image.load('bonus.png').convert_alpha()
    bonus = pygame.transform.scale(bonus_img,bonus_size)
    bonus_rect = pygame.Rect(random.randint(200,width -200),0, *bonus.get_size())
    bonus_speed = random.randint(1,3)
    return [bonus,bonus_rect,bonus_speed,bonus.get_size(),bonus_img]

def shaker(items):
    for item in items:
                item_rnd = random.randint(item[2],item[2]*5)
                item[0] = pygame.transform.scale(item[4],(item[3][0] - item_rnd,item[3][1] + item_rnd))

bg = pygame.transform.scale(pygame.image.load('background.png').convert(),screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY,500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS,1000)

CHNGE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHNGE_IMG,150)

SHAKE = pygame.USEREVENT + 4
pygame.time.set_timer(SHAKE,50)

enemies = []
bonuses = []

scores = 1
img_index = 0
is_working = True

while is_working:
    FPS.tick(60)
    pressed_keys = pygame.key.get_pressed()

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg,(bgX,0))
    main_surface.blit(bg,(bgX2,0))


    main_surface.blit(player,player_rect) 
    main_surface.blit(font.render(str(scores),True,Red), (0,0))   

    for event in pygame.event.get():
        if event.type == QUIT or pressed_keys[K_ESCAPE]:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())

        if event.type == CHNGE_IMG:
            img_index +=1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index] 

        if event.type == SHAKE:
            shaker(enemies)
            shaker(bonuses)
            
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2],0)
        main_surface.blit(enemy[0],enemy[1])
        
        if enemy[1].left < 2 - enemy[3][0] :
            enemies.pop(enemies.index(enemy))

        if player_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy)) 
            scores -= 1
  
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0,bonus[2])
        main_surface.blit(bonus[0],bonus[1])
        
        if bonus[1].bottom > heigth + bonus[3][0]:
            bonuses.pop(bonuses.index(bonus))

        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= heigth:
        player_rect = player_rect.move(0,player_speed)
    
    if pressed_keys[K_UP] and  player_rect.top > 0:
        player_rect = player_rect.move(0,-player_speed)
    
    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed,0)
    
    if pressed_keys[K_LEFT] and  player_rect.left > 0:
        player_rect = player_rect.move(-player_speed,0)
        
    pygame.display.flip()
