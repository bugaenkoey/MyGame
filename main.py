import random
import time
import pygame
from pygame.constants import QUIT 
pygame.init()

def random_color():
  #return(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
  Red     = 255,0,0
  Green   = 0,255,0
  Blue    = 0,0,255
  Yellow  = 255,255,0
  Blue    = 0,255,255
  Magenta = 255,0,255
  Black   = 0,0,0

  colors = [Red,Green,Blue,Yellow,Blue,Magenta,Black]
 
  return random.choice(colors)

screen = width, heigth = 800,600

color = random_color()
background_color = random_color()

main_surface = pygame.display.set_mode(screen)
main_surface.fill(background_color)

ball = pygame.Surface((20,20))
ball.fill(color)
ball_rect = ball.get_rect()
ball_speed = [3,1]

is_working = True

while is_working:
    time.sleep(0.005)
    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

    ball.fill(background_color)
    main_surface.blit(ball,ball_rect) 
    ball.fill(color)       
    ball_rect = ball_rect.move(ball_speed) 

    if ball_rect.bottom >=heigth or ball_rect.top <= 0:
        ball_speed[1] = -ball_speed[1]
        color = random_color()
        
    if ball_rect.right >= width or ball_rect.left <= 0:
        ball_speed[0] = -ball_speed[0]
        color = random_color()
        
    main_surface.blit(ball,ball_rect)
    pygame.display.flip()