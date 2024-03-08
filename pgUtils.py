import pygame as pg
import math

def drawCenterRect(screen,center,length,width,color,border=-1):
    pg.draw.rect(screen, color, (center[0]-length/2, center[1]-width/2, length, width), border)


def drawArrow(screen, start, dir, color, length, width):
    # dir = dir * 180 / math.pi
    end = (start[0] + length * math.cos(dir), start[1] + length * math.sin(dir))
    pg.draw.line(screen, color, start, end, width)
    
def drawRay(screen, start, dir, color):
    length = 9999
    end = (start[0] + length * math.cos(dir), start[1] + length * math.sin(dir))
    pg.draw.line(screen, color, start, end, 1)

def drawTarget(screen, center, radius, color):
    line_ratio = 1.2
    pg.draw.circle(screen, color, center, radius, 1)
    pg.draw.line(screen, color, (center[0] - radius*line_ratio, center[1]), (center[0] + radius*line_ratio, center[1]), 1)
    pg.draw.line(screen, color, (center[0], center[1] - radius*line_ratio), (center[0], center[1] + radius*line_ratio), 1)