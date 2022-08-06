import sys  # ◀◁
sys.path.append('../pga')  # ◀◁
import w_pga_10 as pga  # ◀◁

pga.rampnumber = 1
pga.rampinvert = 1


def draw(key=''):  # ◀◁
    pga.resetTransRot()  # ◀◁

    swh = 'termsize: ' + str(pga.width) + 'x' + str(pga.height)
    pga.text(str(swh), 1, 1)
    pga.text('rampnumber: ' + str(pga.rampnumber), 20, 1)
    pga.text('rampinvert: ' + str(pga.rampinvert), 40, 1)

    x = 1
    y = 2
    for i in range(256):
        pga.text(str(i), x, y)
        pga.stroke(i)
        pga.point(x + 4, y, ys=1)
        y += 1
        if y == pga.height - 1:
            y = 2
            x += 9

    pga.frame_render()  # ◀◁
pga.interact(draw)  # ◀◁