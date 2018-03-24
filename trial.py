#!/usr/bin/env python3
import pygame 

pygame.init()

D_WIDTH = 1215 
D_HEIGHT= 717

black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((D_WIDTH, D_HEIGHT))
pygame.display.set_caption('TESTING')
clock = pygame.time.Clock()

car_img = pygame.image.load('Zed_0.jpg')

def car(x,y): 
    gameDisplay.blit(car_img, (x,y))


crashed = False 

while not crashed: 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True 
    
    gameDisplay.fill(white)
    car(0,0)

    
    pygame.display.update()
    clock.tick(40)

pygame.quit()
quit()
