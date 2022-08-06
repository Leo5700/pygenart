# Уравнения рукавов https://arxiv.org/pdf/0908.0892.pdf

import sys  # ◀◁

sys.path.append('../pga')  # ◀◁ подцеплялка pga из отдельной папки
import w_pga_12 as pga  # ◀◁ создай симлинк из папки pga для того, чтобы pycharm подцеплял библиотеки

import random
import math

# Сгенерируем рукав галактики
flow = []
A, B, N = 13, 0.5, 4
phi_step = 0.1
for phi in pga.float_range(0, math.pi * 2, phi_step):
    try:
        r = A / math.log(B * math.tan(phi / (2 * N)))
        for i in range(3):
            xs = r + random.gauss(0, r * 0.05)
            zs = random.gauss(0, 1)
            ash = phi + random.random() * phi_step - phi_step / 2
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

    # pga.eyeX = -20 + math.sin(fc / 10) / 2 * 30
    # pga.eyeZ = 20 + (math.cos(fc / 10) - 1) / 2 * 15

    d = 2
    if key == 'w':
        pga.eyeX += d
    elif key == 's':
        pga.eyeX -= d
    elif key == 'a':
        pga.eyeZ += d
    elif key == 'd':
        pga.eyeZ -= d

    pga.text(str(pga.eyeX), 1, 2)
    pga.text(str(pga.eyeZ), 1, 3)

    pga.rotateZ(fc * 0.05)
    pga.stroke(222)
    n_flows = 2
    for flow_phi in pga.float_range(0, math.pi * 2, math.pi * 2 / n_flows):  ##
        pga.rotateZ(flow_phi)
        for star_phi, x, z in flow:
            pga.rotateZ(star_phi)
            pga.point3d(x, 0, z)
            pga.rotateZ(-star_phi)
        pga.rotateZ(-flow_phi)

    pga.frame_render()  # ◀◁


pga.interact(draw)  # ◀◁
