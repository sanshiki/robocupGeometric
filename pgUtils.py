import pygame as pg
import math
import geometry as geo

def drawCenterRect(screen,center,length,width,color,border=-1):
    pg.draw.rect(screen, color, (center[0]-length/2, center[1]-width/2, length, width), border)


def drawArrow(screen, start, dir, color, length, width):
    # dir = dir * 180 / math.pi
    end = (start[0] + length * math.cos(dir), start[1] + length * math.sin(dir))
    pg.draw.line(screen, color, start, end, width)
    
def drawRay(screen, start, dir, color, isDotted=False):
    length = 9999
    end = (start[0] + length * math.cos(dir), start[1] + length * math.sin(dir))
    if isDotted:
        drawDottedLine(screen, start, end, color)
    else:
        pg.draw.line(screen, color, start, end, 1)

def drawTarget(screen, center, radius, color):
    line_ratio = 1.2
    pg.draw.circle(screen, color, center, radius, 1)
    pg.draw.line(screen, color, (center[0] - radius*line_ratio, center[1]), (center[0] + radius*line_ratio, center[1]), 1)
    pg.draw.line(screen, color, (center[0], center[1] - radius*line_ratio), (center[0], center[1] + radius*line_ratio), 1)

def calcProjection(point, start, end):
    line_vec = end - start
    point_vec = point - start
    theta = point_vec.dir - line_vec.dir
    proj_mod = point_vec.mod * math.cos(theta)
    proj = start + geo.Polar2Vector(line_vec.dir, proj_mod)
    return proj

def drawDottedLine(screen, start, end, color, interval=50):
    if type(end) == tuple:
        end = geo.GeoPoint(*end)
    if type(start) == tuple:
        start = geo.GeoPoint(*start)
    line_vec = end - start
    mod = line_vec.mod
    unit_vec = line_vec / mod
    for i in range(int(mod // interval)):
        pg.draw.line(screen, color, start + unit_vec * interval * i, start + unit_vec * interval * (i + 0.5), 1)