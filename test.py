import pygame, sys
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

mousex, mousey = 0, 0
WIDTH = 640
HEIGHT = 480

circleRadius = min(width, height)/2.0

windowSurfaceObj = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Test")

while True:
    windowSurfaceObj.fill((0,0,0))

    pygame.draw.circle(windowSurfaceObj, (255,0,0), (mousex, mousey),
                       int(circleRadius))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                circleRadius += 10

    circleRadius *= 0.99
    pygame.display.update()

    fpsClock.tick(30)
