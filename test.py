# todo:
#  X-finalize code and commit
#  X-add in full map feature
#    X-ten by ten grid of squares, randomly filled with stuff. edges either loop
#     over or bounce off
#  X-max velocity on balls (1 grid per second?)
#  X-balls attracted to you if in same square
#   -make total velocity constant instead of componentwise
import pygame, sys, pdb
from pygame.locals import *
from random import randint
from math import sqrt

WIDTH, HEIGHT = 640, 480 # displaywidth, displayheight
GWIDTH, GHEIGHT = 10, 12 # gridwidth, gridheight
UWIDTH, UHEIGHT = WIDTH * GWIDTH, HEIGHT * GHEIGHT #universewidth,universeheight
MAXV = min(WIDTH, HEIGHT) / 30.0 # maximum allowed velocity for balls

def sign(number):
    if number < 0: return -1
    return 1

class Ball:
    def __init__(self, r, (x, y)):
        self.color = (randint(1, 255), randint(1, 255), randint(1, 255))
        self.r = float(r) # radius
        self.xv, self.yv = 0.0, 0.0 # x velocity, y velocity
        self.x, self.y = float(x), float(y) # x & y universe coordinates
        x, y = int(x), int(y)
        self.gx, self.gy = x // WIDTH, y // HEIGHT # location in grid
        self.dx, self.dy = x % WIDTH, y % HEIGHT # location on display (omit?)
    def __repr__(self):
        return "<Ball. color: {}, r: {}, x: {}, y: {}, xv: {}, yv: {}>".format(
                self.color, self.r, self.x, self.y, self.xv, self.yv)
    def move(self):
        self.x = (self.x + self.xv) % UWIDTH
        self.y = (self.y + self.yv) % UHEIGHT
        x, y = int(self.x), int(self.y)
        self.gx, self.gy = x // WIDTH, y // HEIGHT
        self.dx, self.dy = x % WIDTH, y % HEIGHT
    def accelerate(self, (xa, ya)):
        self.xv += xa
        self.yv += ya
        if abs(self.xv) > MAXV: self.xv = sign(self.xv) * MAXV
        if abs(self.yv) > MAXV: self.yv = sign(self.yv) * MAXV

myBall = Ball(min(WIDTH, HEIGHT)/8.0, (WIDTH//2, HEIGHT//2))
#worldBalls = {Ball(10, (40, 50)), Ball(25, (900, 200)), Ball(15, (-1000, 40))} 
worldBalls = {Ball(randint(20,40), (randint(0,UWIDTH), randint(0,UHEIGHT)))
              for __ in xrange(randint(100, 200))}
for ball in worldBalls:
    ball.xv = randint(-10,10)
    ball.yv = randint(-10,10)

def drawBall(ball):
    if (ball.gx, ball.gy) == (myBall.gx, myBall.gy):
        pygame.draw.circle(windowSurfaceObj, ball.color,
                (ball.dx, ball.dy), int(ball.r))

def attraction(ball1, ball2):
    # acceleration on ball2 due to ball1
    xDist, yDist = ball1.x - ball2.x, ball1.y - ball2.y
    dist = sqrt(xDist**2 + yDist**2)
    areaRatio = ball1.r**2 / ball2.r**2
    xdir, ydir = xDist/dist, yDist/dist
    magnitude = 1000 * areaRatio / dist**2
    return (xdir * magnitude, ydir * magnitude)

pygame.init()
fpsClock = pygame.time.Clock()

windowSurfaceObj = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Fun")

fontObj = pygame.font.Font("freesansbold.ttf", 32)
msg = "initial message"

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_p:
                pdb.set_trace()

    windowSurfaceObj.fill((0,0,0))
    for ball in worldBalls:
        if (ball.gx, ball.gy) == (myBall.gx, myBall.gy):
            ball.accelerate(attraction(myBall, ball))
        ball.move()
        drawBall(ball)

    keyValues = pygame.key.get_pressed()
    # get wasd keys
    if keyValues[K_w]: myBall.accelerate((0,-1))
    if keyValues[K_s]: myBall.accelerate((0,1))
    if keyValues[K_a]: myBall.accelerate((-1,0))
    if keyValues[K_d]: myBall.accelerate((1,0))

    myBall.move()
    drawBall(myBall)

    msg = "{}, {}".format(myBall.gx, myBall.gy)
    msgSurfaceObj = fontObj.render(msg, False, (100,100,100))
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (10,10)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)

    pygame.display.update()

    fpsClock.tick(30)
