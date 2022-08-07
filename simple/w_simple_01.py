import sys  # ◀◁
import math

sys.path.append('../pga')  # ◀◁ подцеплялка pga из отдельной папки
import w_pga_13 as pga  # ◀◁ создай симлинк из папки pga для того, чтобы pycharm подцеплял библиотеки


def draw(key=''):  # ◀◁
    pga.resetTransRot()  # ◀◁

    pga.background(0, 2)
    pga.stroke(255)
    pga.translate(pga.width/2, pga.height/2)
    pga.point(0, 0)
    a = pga.framecount * 0.1
    x = math.sin (a / 3) * 30 + math.cos (a / 2) * 10
    pga.rotate(a)
    pga.point(x, 0)

    pga.frame_render()  # ◀◁


pga.interact(draw)  # ◀◁
