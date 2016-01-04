# 2016-01-04|17:04|EST
import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

WIDTH = 640
HEIGHT = 480

windowSurfaceObj = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Test")
pygame.draw.circle(windowSurfaceObj, (255,0,0), (WIDTH/2, HEIGHT/2)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
