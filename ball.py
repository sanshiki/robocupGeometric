import pygame as pg
import geometry as geo
import pgUtils
from math import pi

class Ball:
    def __init__(self, radius, ratio, decay):
        self.pos = geo.GeoPoint(0, 0)
        self.vel = geo.GeoVector(0, 0)
        self.decay = decay
        self.frame = 60
        self.radius = radius * ratio
        self.color = (255,193,37)

        # mouse flag
        self.isDragging = False
        self.isTurning = False

    def draw(self, screen, verbose=False):
        self.calculatePos()
        pg.draw.circle(screen, self.color, self.pos, self.radius)
        pgUtils.drawArrow(screen, self.pos, self.vel.dir, self.color, 20, 2)

        # verbose
        if verbose:
            pgUtils.drawRay(screen, self.pos, self.vel.dir, self.color, isDotted=False)
            pgUtils.drawRay(screen, self.pos, self.vel.dir+pi, self.color, isDotted=True)
            screen.blit(pg.font.Font(None, 20).render('Ball', True, self.color), self.pos + geo.Polar2Vector(-pi/2, self.radius*3))
            screen.blit(pg.font.Font(None, 20).render(str(self.pos)+' '+str(round(self.vel.dir,2)), True, self.color), self.pos + geo.Polar2Vector(-pi/2, self.radius*4.5))


    def move(self, x, y):
        self.vel = geo.GeoVector(0, 0)
        self.pos = geo.GeoPoint(x, y)

    def setVel(self, x, y):
        self.vel = geo.GeoVector(x - self.pos.x, y - self.pos.y)

    def calculatePos(self):
        self.pos = self.pos + self.vel / self.frame
        acc = geo.Polar2Vector(self.vel.dir, self.decay)

        if self.vel.mod <= 5:
            polar_dir = self.vel.dir
            polar_mod = 1
            self.vel = geo.GeoVector(0, 0, polar_dir, polar_mod)

        else:
            self.vel = self.vel + acc / self.frame


    def onMouse(self, pos):
        if (self.pos - pos).mod <= self.radius:
            return True
        return False
    
    def onDrag(self):
        return self.isDragging
    
    def setDrag(self):
        self.isDragging = True
    
    def resetDrag(self):
        self.isDragging = False

    def onTurn(self):
        return self.isTurning
    
    def setTurn(self):
        self.isTurning = True

    def resetTurn(self):
        self.isTurning = False