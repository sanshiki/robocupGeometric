import pygame as pg
import pgUtils
from math import pi, atan2
import geometry as geo


class Player:
    def __init__(self, radius, ratio, team):
        self.pos = geo.GeoPoint(0, 0)
        self.dir = 0.5
        self.ratio = ratio
        self.radius = radius * self.ratio
        
        self.team = team
        self.color = (0, 0, 255) if team == 0 else (255, 255, 0)

        # mouse flag
        self.isDragging = False
        self.isTurning = False

    def draw(self,screen,verbose=False):
        pg.draw.circle(screen, self.color, self.pos, self.radius)
        pgUtils.drawArrow(screen, self.pos, self.dir, self.color, 25, 2)

        # verbose
        if verbose:
            pgUtils.drawRay(screen, self.pos, self.dir, self.color, isDotted=False)
            pgUtils.drawRay(screen, self.pos, self.dir+pi, self.color, isDotted=True)
            screen.blit(pg.font.Font(None, 20).render('Player', True, self.color), self.pos+geo.Polar2Vector(-pi/2, self.radius*2))
            screen.blit(pg.font.Font(None, 20).render(str(self.pos)+' '+str(round(self.dir,2)), True, self.color), self.pos+geo.Polar2Vector(-pi/2, self.radius*3))

    def move(self, x, y):
        self.pos = geo.GeoPoint(x, y)

    def turn(self, facepoint):
        self.dir = atan2(facepoint[1] - self.pos[1], facepoint[0] - self.pos[0])

    def onMouse(self, pos):
        if (self.pos - pos).mod <= self.radius:
            return True
        return False
    
    def onDrag(self):
        return self.isDragging
    
    def onTurn(self):
        return self.isTurning
    
    def setDrag(self):
        self.isDragging = True

    def setTurn(self):
        self.isTurning = True
    
    def resetDrag(self):
        self.isDragging = False

    def resetTurn(self):
        self.isTurning = False
    