# todo:
#  -finalize code and commit
#  -add in full map feature
import pygame, sys
from pygame.locals import *
from ball import Ball
import pdb

WIDTH = 640
HEIGHT = 480

myBall = Ball(min(WIDTH, HEIGHT)/8.0, (WIDTH//2, HEIGHT//2))

pygame.init()
fpsClock = pygame.time.Clock()
windowSurfaceObj = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Fun")

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_p:
                pdb.set_trace()

    keyValues = pygame.key.get_pressed()
    # get wasd keys
    if keyValues[K_w]:
        myBall.yv -= 1
    if keyValues[K_s]:
        myBall.yv += 1
    if keyValues[K_a]:
        myBall.xv -= 1
    if keyValues[K_d]:
        myBall.xv += 1

    myBall.move()

    windowSurfaceObj.fill((0,0,0))
    pygame.draw.circle(windowSurfaceObj, (255,0,0),
            (int(myBall.x) % WIDTH, int(myBall.y) % HEIGHT), int(myBall.r))
    pygame.display.update()

    fpsClock.tick(30)
