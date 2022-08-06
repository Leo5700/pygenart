##

import curses  # pip3 install curses
import math
import os
import time
import decimal

from tinynumpy import tinynumpy as tnp  # pip3 install tinynumpy


def get_term_size():
    """
    ширина и высота терминала в символах
    w, h = getTermSize()
    """
    (width_term, height_term) = os.get_terminal_size()
    return width_term, height_term


width, height = get_term_size()
canvas = tnp.zeros((width, height))

ramp_name = 'main'  ## выбор палитры из ramps
rampinvert = True  ## инверсия палитры
framecount = -1  # это -1й кадр, setup
texts = {}


ramps = {
    '0': '▓-',
    'main': '$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`. ',
    '2': 'MMMMMMM@@@@@@@WWWWWWWWWBBBBBBBB000000008888888ZZZZZZZZZaZaaaaaa2222222SSSSSSSXXXXXXXXXXX7777777rrrrrrr;;;;;;;;iiiiiiiii:::::::,:,,,,,,.........       ',
    '3': '@@@@@@@######MMMBBHHHAAAA&&GGhh9933XXX222255SSSiiiissssrrrrrrr;;;;;;;;:::::::,,,,,,,........        ',
    '4': '#WMBRXVYIti+=;:,. ',
    '5': '##XXxxx+++===---;;,,...    ',
    '6': '@%#*+=-:. ',
    '7': '#¥¥rrOO$$o0oo°++=-,.    ',
    '8': '█▓▒░ ',
    'srapa': '    ....----papaSRAPA',
    '10': '    ####::::helloworld!',
    '11': '~!@#$%^&*()+QWERTYUIOP{|ASDFGHJKL:"ZXCVBNM<>?`1234567890-=qwertyuiop[]asdfghjkl;zxcvbnm,./№ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮйцукенгшщзхъфывапролджэячсмитьбю②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇⒜⒝⒞⒟⒠⒡⒢⒣⒤⒥⒦⒧⒨⒩⒪⒫⒬⒭⒮⒯⒰⒱⒲⒳⒴⒵ⒶⒷⒸⒹⒺⒻⒼⒽⒾⒿⓀⓁⓂⓃⓄⓅⓆⓇⓈⓉⓊⓋⓌⓍⓎⓏⓐⓑⓒⓓⓔⓕⓖⓗⓘ ',
    '12': '─━│┃┄┅┆┇┈┉┊┋┌┍┎┏┐┑┒┓└┕┖┗┘┙┚┛├┝┞┟┠┡┢┣┤┥┦┧┨┩┪┫┬┭┮┯┰┱┲┳┴┵┶┷┸┹┺┻┼┽┾┿╀╁╂╃╄╅╆╇╈╉╊╋╌╍╎╏═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬╭╮╯╰╱╲╳╴╵╶╷╸╹╺╻╼╽╾╿▀▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐░▒▓▔▕▖▗▘▙▚▛▜▝▞▟■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄ ',
    '13': '█▉▊▋▌▍▎▏ ',
    '14': ' ▁▂▃▄▅▆▇█▉'
}


strokecolor = 150
strokealpha = 255

eyeX, eyeY, eyeZ = -20, 0, 20  # положение камеры (смотрит она в 0, 0, 0)
fovx = 60  # угол зрения камеры по горизонтали в градусах


# ======================== графические объекты

def background(color, alpha=255):
    '''
        увы, tiny numpy это не numpy и складывать и умножать
        матрицу и число он не умеет, поэтому перебор
        с учётом прозрачности заливки
        '''
    for j in range(height):
        for i in range(width):
            canvas[i, j] = mixColorsByAlpha(canvas[i, j], color, alpha)


def text(s, x, y, ys=1):
    '''
        собираем все тексты в словарь, потом в draw
        выводим строку в pixels после матрицы цветов
        TODO тексты пока выводятся минуя translate и rotate т.к. вписываются
        в pixels напрямую, в последнюю очередь. Необходимо ввести в функцию
        frameRender отдельную обработку перемещений и поворотов для текста
        '''
    texts.update({s: [x, y * ys]})  # это потом вспоминаем по ключам в draw


def point(x, y, ys=0.5):
    '''
    рисуем точку, ys это масштаб по высоте т.к. в терминале символы
    вписаны в прямоугольники с соотношением сторон 1:2
    '''
    x += modx
    y += mody
    if modangle != 0:
        x, y = rotate_coordinates((modx, mody), (x, y), modangle)
    y = y * ys
    if 0 <= x < width and 0 <= y < height:
        i, j = int(x), int(y)
        pointcolor = mixColorsByAlpha(canvas[i, j], strokecolor, strokealpha)
        if pointcolor > 255:
            pointcolor = 255
        if pointcolor < 0:
            pointcolor = 0
        canvas[i, j] = pointcolor
    else:
        pass


# ======================== рисование


def mixColorsByAlpha(old_color, color, alpha):
    '''
    к старому цвету добавляем новый, но не весь, а часть пропорциональную alpha
    '''
    dc = color - old_color
    new_old_color = old_color + dc * mmap(alpha, 0, 255, 0, 1)
    return new_old_color


def mmap(value, start1, stop1, start2, stop2):
    '''
    мапинг value из диапазона start1..stop1 к диапазону start2..stop2
    '''
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))


def reversedString(s):
    '''
    строка задом наперёд
    '''
    return s[::-1]


def num2pixel(num, ramp, reverse=False):
    '''
    перевод числа num от 0 до 255 в номер символа строки ramp
    reverse "инвертирует" "цвет"
    TODO по краям не дочитывается символ, поправить при случае
    '''
    if reverse:
        ramp = reversedString(ramp)
    if num < 0:
        num = 0
    if num > 255:
        num = 255
    i = int(mmap(num, 0, 255, 0, len(ramp) - 1))  # -1?
    return ramp[i]


def strInsert(s0, s1, pos):
    """
    вставляем строку в строку с подменой
    strInsert(s0='012345678', s1='aaa', pos=2)
        01aaa567890
    если позиция окажется за строкой s0, s1 окажется на краю s0
    """
    if pos < 0:
        pos = 0
    return s0[:pos] + s1 + s0[(pos + len(s1)):]


def rotate_coordinates(origin_crd, point_crd, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    ox, oy = origin_crd
    px, py = point_crd

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def stroke(color, alpha=255):
    """
    pass
    """
    global strokecolor, strokealpha
    strokecolor = color
    strokealpha = alpha


def resetTransRot():
    """
    сброс переносов и поворотов
    """
    global modx, mody, modangle
    global modx3d, mody3d, modz3d, modangleX, modangleY, modangleZ
    modx, mody = 0, 0
    modangle = 0
    modx3d, mody3d, modz3d = 0, 0, 0
    modangleX, modangleY, modangleZ = 0, 0, 0


def translate(x, y, ys=2):  # ys это масштаб по у
    '''
    масштаб ys при переносе и при отрисовке соотносится как
    1/ys, пока оставим разные умолчания чтобы не замедлять
    работу лишними делениями в больших циклах
    '''
    global modx, mody
    modx += x
    mody += y * ys


def translate3d(x, y, z):
    global modx3d, mody3d, modz3d
    modx3d += x
    mody3d += y
    modz3d += z


def rotate(angle):
    """
    все повороты и переносы копим в переменных, это удобно
    """
    global modangle
    modangle += angle


def rotateX(angleX):
    global modangleX
    modangleX += angleX


def rotateY(angleY):
    global modangleY
    modangleY += angleY


def rotateZ(angleZ):
    global modangleZ
    modangleZ += angleZ


def get_angle(a, b, c, positive=False, radians=False):
    """
    Угол между отрезками по трём точкам,
    positive -90 станет 270,
    radians ответ будет в радианах.

    print(get_angle((0, 0), (-5, 5), (-10, 0), positive=False, radians=True))
    -1.5707963267948966
    """
    if radians:
        ang = math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0])
    else:
        ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    if positive:
        return ang + 360 if ang < 0 else ang
    else:
        return ang


def point3d(xp, yp, zp):
    # Задаём координаты камеры (ранее), она будет смотреть в точку 0, 0, 0
    # Вычисляем углы между вектором из камеры на ноль и из камеры на точку
    # по горизонтали и вертикали
    # учитывая транслэйты и ротэйты
    xp += modx3d
    yp += mody3d
    zp += modz3d
    if modangleX != 0:
        pass
        # TODO доделать поворот по X
    if modangleY != 0:
        pass
        # TODO доделать поворот по Y
    if modangleZ != 0:
        xp, yp = rotate_coordinates((modx3d, mody3d), (xp, yp), modangleZ)
    aw = get_angle((0, 0), (eyeX, eyeY), (xp, yp))
    ah = get_angle((0, 0), (eyeX, eyeZ), (xp, zp))
    # Задаём угол зрения камеры в градусах по горизонтали (ранее)
    # и вычисляем угол зрения по вертикали
    ah_max = fovx * height / width
    # Если точка попала в воображаемый экран,
    # отрисуем её, сдвинув на центр экрана
    if aw <= fovx and ah <= fovx:
        pw = aw / fovx * width
        ph = ah / ah_max * height
        translate(width / 2, height / 2)
        point(pw, -ph)  # минус т.к. h считается сверху вниз
        translate(-width / 2, -height / 2)


def float_range(start, stop, step):
    while start < stop:
        yield float(start)
        start += decimal.Decimal(step)


    # ======================== вывод на экран


def frame_render():
    """
    превращаем матрицу в строку в соотв. цветами из ramp,
    вписываем тексты, что надо зануляем, что надо прибавляем
    """
    pixels = ''
    for j in range(height):
        for i in range(width):
            pixel = num2pixel(canvas[i, j], ramps[ramp_name], reverse=rampinvert)
            pixels += pixel
    global texts
    for key in texts.keys():  # тексты
        x, y = texts[key]
        pos = width * int(y) + x
        pixels = strInsert(pixels, key, pos)
    print(pixels)
    texts = {}  ####
    global framecount
    framecount += 1


def interact(draw):
    """
    отрисовка всего что есть в функции draw с таймаутом на ввод с клавиатуры
    FIXME нулевого столбца и строки не выводится после первого кадра
    """

    def run(win, timeout=.05):  # ожидание кнопки, сек (.05 это 1/20 сек.)
        '''
        оборачиваем draw при помощи либы для рисования интерфейсов
        для того, чтобы раз в кадр читать нажатую кнопку,
        timeout немного снижает framerate, но сильнее его
        снижает termux, в котором всё это крутится
        '''
        curses.curs_set(0)
        while True:
            win.timeout(0)  # non-block read
            c = -1  # номер клавиши
            start = time.time()
            wait_key = True
            key = ''
            while wait_key:
                c = win.getch()
                time_taken = time.time() - start
                if c < 0:
                    pass
                else:
                    key = chr(c)
                if time_taken >= timeout:
                    c = -1
                    wait_key = False
            draw(key)

    curses.wrapper(run)

# ======================== вывод на экран
