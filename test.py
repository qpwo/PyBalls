import pygame, sys, pdb
from pygame.locals import *
from random import randint
from math import sqrt

WIDTH, HEIGHT = 640, 480
GWIDTH, GHEIGHT = 10,10
UWIDTH, UHEIGHT = WIDTH * GWIDTH, HEIGHT * GHEIGHT
MAXSPEED = min(WIDTH, HEIGHT) / 30.0

def makeColor():
    notUsing = randint(0,2)
    split = randint(0,255)
    color = [0,0,0]
    color[(notUsing - 1) % 3] = split
    color[(notUsing + 1) % 3] = 255 - split
    return tuple(color)


class Ball:
    def __init__(self, r, (x, y)):
        self.color = makeColor()
        self.r = float(r)
        self.xv, self.yv = 0.0, 0.0
        self.x, self.y = float(x), float(y)
        self.move()
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
        speed = sqrt(self.xv**2 + self.yv**2)
        if speed > MAXSPEED:
            self.xv = (self.xv / speed) * MAXSPEED
            self.yv = (self.yv / speed) * MAXSPEED

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
    magnitude = 10000 * areaRatio / dist**2
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

    keyValues = pygame.key.get_pressed()

    if keyValues[K_w]: myBall.accelerate((0,-1))
    if keyValues[K_s]: myBall.accelerate((0,1))
    if keyValues[K_a]: myBall.accelerate((-1,0))
    if keyValues[K_d]: myBall.accelerate((1,0))

    myBall.move()

    if keyValues[K_n]: myBall.r = max(myBall.r - 1, 1)
    if keyValues[K_m]: myBall.r += 1

    drawBall(myBall)

    for ball1 in worldBalls:
        #if not keyValues[K_g]:
        #if (ball.gx, ball.gy) == (myBall.gx, myBall.gy):
                #ball.accelerate(attraction(myBall, ball))
        myBall.accelerate(attraction(ball1,myBall))
        for ball2 in worldBalls - {ball1}:
            if (ball1.gx, ball1.gy) == (ball2.gx, ball2.gy):
                ball2.accelerate(attraction(ball1, ball2))
        ball1.move()
        drawBall(ball1)

    msg = "{}, {}".format(myBall.gx, myBall.gy)
    msgSurfaceObj = fontObj.render(msg, False, (100,100,100))
    msgRectObj = msgSurfaceObj.get_rect()
    msgRectObj.topleft = (10,10)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectObj)

    pygame.display.update()

    fpsClock.tick(30)
