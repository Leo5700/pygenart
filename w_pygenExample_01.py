import time
import curses
import w_pygenTools_06 as tls  ## проверь версию

tls.frameRate(30)  ##
width, height = tls.getTermSize()
frm = tls.Frame(width, height)
frm.rampnumber = 1  ## цветовая палитра
frm.rampinvert = True  ## инверсия палитры
tls.sketchStarting()

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv sketch code

from math import sin, cos, pi
from random import random

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ sketch code

def draw(key=''):
    tls.frameStart()
    frm.initFrame()

    # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv sketch code
    
    '''
    точки перемещаются по +- круговым траекториям, число точек
    меняется по кнопкам 1..9, при этом экран заливается
    кнопки "-" и "=" меняют размер картинки, 
    выход по Crtl+c
    '''

    if frm.frameCount == -1: # setup
        #### frm.key = 5
        #### # cr = 24
        frm.const.update({'cr' : 24})  # новая константа
        frm.const.update({'key' : 5})
        pass


    if key:
        frm.background(150)
        pass

    frm.background(0, 8) ## постепенная заливка фоном

    # отрисуем пиксели в углах
    frm.stroke(10)
    frm.point(1, 1, 1)
    frm.point(width-1, 1, 1)
    frm.point(1, height-1, 1)
    frm.point(width-1, height-1, 1)
    
    # отрисуем траектории точек
    sh = frm.frameCount*.5
    frm.stroke(30)
    frm.translate(width/2,height/2, 2)
    a0 = sh*.15
    if key:
        try:
            frm.const['key'] = int(key)
        except ValueError:
            pass
    k = frm.const['key']
    
    if key == '=':
        frm.const['cr'] += 1
    if key == '-':
        frm.const['cr'] -= 1

    for i in range(k):
        a = i/k * 2*pi
        frm.rotate(a + a0)
        r = frm.const['cr'] * (sin(a0) + cos(a0)/7) ##
        frm.point(r, 3, .5) ##
        frm.rotate(-(a + a0))

    frm.text(str(k), 3, 3, ys=1) 
    frm.text(str(frm.const['cr']), 3, 4, ys=1)

    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ sketch code

    frm.drawFrame()
    tls.frameEnd()


def run(win, timeout=.05):  ## ожидание кнопки, сек
    '''
    оборачиваем draw при помощи либы для рисования интерфейсов
    для того, чтобы раз в кадр читать нажатую кнопку,
    timeout немного снижает framerate, но сильнее его
    снижает termux, в котором всё это крутится
    '''

    curses.curs_set(0)
    while True:
        win.timeout(0)  # non-block read
        c=-1  # номер клавиши
        start = time.time()
        wait_key = True
        key = ''
        while wait_key:
            c = win.getch()
            time_taken = time.time() - start
            if c < 0:
                pass
            else:
                key=chr(c)
            if time_taken >= timeout:
                c = -1 
                wait_key = False
        draw(key) 

# draw() ####
curses.wrapper(run)


