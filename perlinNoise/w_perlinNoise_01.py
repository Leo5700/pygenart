import sys  # ◀◁
sys.path.append('../pga')  # ◀◁
import w_pga_09 as pga  # ◀◁

from perlin_noise import PerlinNoise  # pip3 install perlin_noise


pga.rampnumber = 2

noise = PerlinNoise(octaves=3)
xpix, ypix = pga.width, pga.height

noise_shift = 0


def draw(key=''):  # ◀◁
    pga.resetTransRot()  # ◀◁

    global noise_shift
    if key:
        noise_shift += 0.10
    else:
        noise_shift += 0.07

    pic = [[noise([i / xpix, j / ypix / 4, noise_shift]) for j in range(xpix)] for i in range(ypix)]
    # pga.text(str(pic[0]), 1, 1)
    for y in range(len(pic)):
        for x in range(len(pic[0])):
            color = pga.mmap(pic[y][x], -0.4, 0.4, 0, 255)
            pga.stroke(color)
            pga.point(x, y, 1)

    pga.frame_render()  # ◀◁


pga.interact(draw)  # ◀◁
