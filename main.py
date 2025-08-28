import pygame
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()

while True:
    for event in pygame.event.get():
        if event.type == QUIT: # para sair
            pygame.quit()
            exit()
    pygame.display.update()