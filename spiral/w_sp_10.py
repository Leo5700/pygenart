import sys  # ◀◁

sys.path.append('../pga')  # ◀◁ подцеплялка pga из отдельной папки
import w_pga_12 as pga  # ◀◁ создай симлинк из папки pga для того, чтобы pycharm подцеплял библиотеки

import random
import math

# Сгенерируем рукав галактики
flow = []
A, B, N = 13, 0.5, 4
a_step = 0.1
for a in pga.float_range(0, math.pi * 2, a_step):
    try:
        r = A / math.log(B * math.tan(a / (2 * N)))
        for i in range(3):
            xs = r + random.gauss(0, r * 0.05)
            zs = random.gauss(0, 1)
            ash = a + random.random() * a_step - a_step / 2
            flow.append([ash, xs, zs])
    except ValueError:
        pass


# print(flow)

def draw(key=''):  # ◀◁
    pga.resetTransRot()  # ◀◁
    fc = pga.framecount

    pga.background(0)

    pga.stroke(5)
    pga.point3d(0, 0, 0)
    pga.text(str(len(flow)), 1, 1)

    pga.eyeX = -20 + math.sin(fc / 10) / 2 * 30
    pga.eyeZ = 20 + (math.cos(fc / 10) - 1) / 2 * 15
    pga.text(str(pga.eyeX), 1, 2)
    pga.text(str(pga.eyeZ), 1, 3)

    pga.rotateZ(fc * 0.05)
    pga.stroke(222)
    n_flows = 2
    for base_angle in pga.float_range(0, math.pi * 2, math.pi * 2 / n_flows):  ##
        pga.rotateZ(base_angle)
        for ash, xs, zs in flow:
            pga.rotateZ(ash)
            pga.point3d(xs, 0, zs)
            pga.rotateZ(-ash)
        pga.rotateZ(-base_angle)

    pga.frame_render()  # ◀◁


pga.interact(draw)  # ◀◁
