import random
# import time
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
 

screen = width, heigth = 800,600

color = Yellow
background_color = Black

main_surface = pygame.display.set_mode(screen)
main_surface.fill(background_color)

ball = pygame.Surface((20,20))
ball.fill(color)
ball_rect = ball.get_rect()
ball_speed = 5

enemy_0 = [Red,(2,5),(screen[0],random.randint(0,heigth))]

def create_element(color,speed = (1,1),start = (0,0),size = (20,20)):
    # size = size
    element = pygame.Surface(size)
    element.fill(color)
    
    element_rect = pygame.Rect(start[0],start[1], *element.get_size())
    element_speed = random.randint(speed)
    return [element,element_rect,element_speed,*element.get_size()]
    

def create_enemy():
    enemy_sise = [20,20]
    enemy = pygame.Surface(enemy_sise)
    enemy.fill(Red)
    enemy_rect = pygame.Rect(width, random.randint(0,heigth), *enemy.get_size())
    enemy_speed = random.randint(2,5)
    return [enemy,enemy_rect,enemy_speed,enemy_sise]

def create_bonus():
    bonus_sise = [20,20]
    bonus = pygame.Surface(bonus_sise)
    bonus.fill(Green)
    bonus_rect = pygame.Rect(random.randint(0,width),0, *bonus.get_size())
    bonus_speed = random.randint(1,3)
    return [bonus,bonus_rect,bonus_speed,bonus_sise]



CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY,1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS,500)

enemies = []
bonuses = []

is_working = True

while is_working:
    # time.sleep(0.005)
    FPS.tick(60)
    pressed_keys = pygame.key.get_pressed()
    
    # enemies.append(create_enemy())
    for event in pygame.event.get():

        if event.type == QUIT or pressed_keys[K_ESCAPE]:
            is_working = False

        if event.type == CREATE_ENEMY:
            # enemies.append(create_enemy())
            # enemies.append(create_element(Red,(2,5),(screen[0],random.randint(0,heigth))))
            enemies.append(create_element(enemy_0))

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())


    ball.fill(background_color)
    main_surface.blit(ball,ball_rect) 
    ball.fill(color)       

    for bonus in bonuses:
        bonus[0].fill(background_color)
        main_surface.blit(bonus[0],bonus[1])
        bonus[1] = bonus[1].move(0,bonus[2])
        bonus[0].fill(Green)
        main_surface.blit(bonus[0],bonus[1])
        

        if bonus[1].width < 2 - bonus[3][0] :
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            bonus[0].fill(background_color)
            main_surface.blit(bonus[0],bonus[1]) 
            

    for enemy in enemies:
        enemy[0].fill(background_color)
        main_surface.blit(enemy[0],enemy[1])
        enemy[1] = enemy[1].move(-enemy[2],0)
        enemy[0].fill(Red)
        main_surface.blit(enemy[0],enemy[1])
        

        if enemy[1].left < 2 - enemy[3][0] :
            enemies.pop(enemies.index(enemy))

        if ball_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy)) 
            enemy[0].fill(background_color)
            main_surface.blit(enemy[0],enemy[1])
  
    
    if pressed_keys[K_DOWN] and not ball_rect.bottom >= heigth:
        ball_rect = ball_rect.move(0,ball_speed)
    
    if pressed_keys[K_UP] and  ball_rect.top > 0:
        ball_rect = ball_rect.move(0,-ball_speed)
    
    if pressed_keys[K_RIGHT] and not ball_rect.right >= width:
        ball_rect = ball_rect.move(ball_speed,0)
    
    if pressed_keys[K_LEFT] and  ball_rect.left > 0:
        ball_rect = ball_rect.move(-ball_speed,0)

        
    main_surface.blit(ball,ball_rect)
    pygame.display.flip()