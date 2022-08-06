'''
Неклассическая Game of life.
Состояние клеток меняется плавно.
Кнопками q и w изменяется питательность
среды, ниже 44 наблюдается
спад популяции, выше 46 рост.
r сбрасывает всё
'''

import sys  # ◀◁
sys.path.append('../pga')  # ◀◁

import random
import w_pga_06 as pga
from w_pga_06 import text, background, width, height, point, stroke, translate
from math import sin, cos


from tinynumpy import tinynumpy as tnp

pga.rampnumber = 12 ##
pga.rampinvert = 1


grow = 42

seed = -1

generation = 0

def ask(i, j):
    def cx(x):  # constraint
        if x < 0:
            x = width-1
        if x == width:
            x = 0
        return x
    def cy(y):
        if y < 0:
            y = height-1
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

    text('THEGAMEOFLIFE42', width - 16, 1)

    global generation
    text('generation: ' + str(generation), 1, 1)
    generation += 1


    cd = tnp.zeros((width, height))  # модификатор следующего поколения

    global grow
    if key == 'q':
        grow -= 2
    if key == 'w':
        grow += 2
    text('grow: ' + str(grow), 1, 2)

    text('fieldsize: ' + str(width) + 'x' + str(height), 1, height-1)

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

    global seed
    if key == 'u':
        seed = -666
        background(0)
        translate(width/2, height/2, 1)

        stroke(210)
        point(2, 1, 1)
        stroke(255)
        point(0, 2, 1)
        point(1, 1, 1)
        point(1, 3, 1)
        point(2, 2, 1)

    all_dead = False
    if generation % 50 == 0:
        sum = 0
        for j in range(height):
            for i in range(width):
                sum += pga.canvas[i, j]
        if sum == 0:
            all_dead = True


    text('seed: ' + str(seed), 1, height-2)
    if pga.framecount == -1 or key == 'r' or all_dead:
        # if pga.framecount > -1:
            # seed = int(random.random()*1000)
        random.seed(seed)
        seed += 1
        generation = 0
        for j in range(height):
            for i in range(width):
                c = random.random() * 255
                pga.canvas[i, j] = c


    pga.frameRender()


pga.interact(draw)


'''
conway's game of life variation
https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life
cool-retro-term
'''
