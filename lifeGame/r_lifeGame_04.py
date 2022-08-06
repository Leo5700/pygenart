'''
Неклассическая Game of life.
Состояние клеток меняется плавно.
Кнопками q и w изменяется питательность 
среды, ниже 44 наблюдается 
спад популяции, выше 46 рост.
'''

import sys  # ◀◁
sys.path.append('../pga')  # ◀◁

import w_pga_03 as pga
from w_pga_03 import text, background, width, height, point, stroke
from math import sin, cos
from random import random, choice


from tinynumpy import tinynumpy as tnp

pga.rampnumber = 1 ##
pga.rampinvert = 1


grow = 42

def ask(i, j):
    def cx(x):  # constraint
        if x < 0:
            x = width-1
        if x == width:                             x = 0
        return x
    def cy(y):
        if y < 0:                                  y = height-1
        if y == height:
            y = 0
        return y
    n = 0
    n += pga.canvas[cx(i-1), cy(j-1)]
    n += pga.canvas[cx(i-1), j]
    n += pga.canvas[cx(i-1), cy(j+1)]
    n += pga.canvas[i, cy(j-1)]
    n += pga.canvas[i, cy(j+1)]
    n += pga.canvas[cx(i+1), cy(j-1)]
    n += pga.canvas[cx(i+1), j]
    n += pga.canvas[cx(i+1), cy(j+1)]
    return n


def draw(key=''):
    pga.resetTransRot()
    
    text(str(pga.framecount), 1, 1)

    if pga.framecount == -1:
        for j in range(height):
            for i in range(width):
                #c = choice((0, 255))
                c = random() * 255
                pga.canvas[i, j] = c
    
    cd = tnp.zeros((width, height))  # модификатор следующего поколения
    
    global grow
    if key == 'q':
        grow -= 2
    if key == 'w':
        grow += 2
    text(str(grow), 1, 2)

    for j in range(0, height):
        for i in range(0, width):
            n = ask(i, j)
            if n < 2*255 or n > 3*255: 
                cd[i, j] = -50
            elif 2*255 <= n <= 3*255:
                cd[i, j] = grow
            else:
                cd[i, j] = 0

    for j in range(0, height):
        for i in range(0, width):
            pga.canvas[i, j] += cd[i, j]
            if pga.canvas[i, j] < 0:
                pga.canvas[i, j] = 0
            if pga.canvas[i, j] > 255:
                pga.canvas[i, j] = 255
    
    pga.frameRender()
    
    
#draw() ####
pga.interact(draw)












