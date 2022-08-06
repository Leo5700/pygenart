'''
Неклассическая Game of life.
Состояние клеток меняется плавно.
Кнопками q и w изменяется питательность 
среды, ниже 44 наблюдается 
спад популяции, выше 46 рост.
'''

import w_pga_04 as pga
from w_pga_04 import text, background, width, height, point, stroke
from math import sin, cos
from random import random, choice


from tinynumpy import tinynumpy as tnp

pga.rampnumber = 12 ##
pga.rampinvert = 1


def draw(key=''):
    pga.resetTransRot()
    
    swh = 'termsize: ' + str(width) + 'x' + str(height) 
    text(str(swh), 1, 1)

    x = 1
    y = 2
    for i in range(256):
        text(str(i), x, y)
        stroke(i)
        point(x + 4, y, ys=1)
        y += 1
        if y == height - 1:
            y = 2
            x += 9

    
    pga.frameRender()
    
    
#draw() ####
pga.interact(draw)












