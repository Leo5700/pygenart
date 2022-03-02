##

import w_pga_02 as pga
from w_pga_02 import text, background, width, height, point, stroke
from math import sin, cos
from random import random


pga.rampnumber = 9 ##
cmin, cmax = 0, 0


def draw(key=''):
    pga.resetTransRot()
    
    text(str(pga.frameCount), 1, 1)
    
    sh = pga.frameCount * .1
    for j in range(height):
        for i in range(width):
#            c = random() * 255
            c1 = (sin(j*.5+sh)+1)
            c2 = (sin(j*.4+i*.4+sh/2)+1)
            c3 = (sin(j*.3+i*-.5+sh/3)+2)
            c = c1 + c2 + c3
    
            global cmin, cmax
            if c < cmin: # выясним размах и пронормируемся на него
                cmin = c
            if c > cmax:
                cmax = c
            c = pga.mmap(c, cmin, cmax, 0, 255)
    
            stroke(c)
            point(i, j, ys=1)
    
    pga.frameRender()
    
    
#draw() ####
pga.interact(draw)
