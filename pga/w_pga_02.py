##

import os, curses, time, math
from tinynumpy import tinynumpy as tnp


def getTermSize():
    '''
    ширина и высота терминала в символах
    w, h = getTermSize()
    '''
    (width, height) = os.get_terminal_size()
    return (width, height)

width, height = getTermSize()
canvas = tnp.zeros((width, height))


rampnumber = 1  ## выбор палитры из ramps
rampinvert = False ## инверсия палитры
frameCount = -1  # это -1й кадр, setup
texts = {}
ramps = [
'▓-',
'$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`. ',
' .:-=+*#%@',
'MMMMMMM@@@@@@@WWWWWWWWWBBBBBBBB000000008888888ZZZZZZZZZaZaaaaaa2222222SSSSSSSXXXXXXXXXXX7777777rrrrrrr;;;;;;;;iiiiiiiii:::::::,:,,,,,,.........       ',
'@@@@@@@######MMMBBHHHAAAA&&GGhh9933XXX222255SSSiiiissssrrrrrrr;;;;;;;;:::::::,,,,,,,........        ',
'#WMBRXVYIti+=;:,. ',
'##XXxxx+++===---;;,,...    ',
'@%#*+=-:. ',
'#¥¥rrOO$$o0oo°++=-,.    ',
'█▓▒░ ',
'    ....----papaSRAPA',
'    ####::::helloworld!'
]
strokecolor = 150
strokealpha = 255


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
        texts.update({s : [x, y*ys]}) # это потом вспоминаем по ключам в draw


def point(x, y, ys=0.5):
    '''
    рисуем точку, ys это масштаб по высоте т.к. в терминале символы
    вписаны в прямоугольники с соотношением сторон 1:2
    '''
    x += modx
    y += mody
    if modangle != 0:
        x, y = rotateCoords((modx, mody), (x, y), modangle)
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
    i = int(mmap(num, 0, 255, 0, len(ramp)-1))  # -1?
    return ramp[i]


def strInsert(s0, s1, pos):
    '''
    вставляем строку в строку с подменой
    strInsert(s0='012345678', s1='aaa', pos=2)
    >>> 01aaa567890
    если позиция окажется за строкой s0, s1 окажется на краю s0 
    '''
    if pos < 0:
        pos = 0
    return s0[:pos] + s1 + s0[(pos + len(s1)):]


def rotateCoords(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


def stroke(color, alpha=255):
    '''
    pass
    '''
    global strokecolor, strokealpha
    strokecolor = color
    strokealpha = alpha


def resetTransRot():
    '''
    сброс переносов и поворотов
    '''
    global modx, mody, modangle
    modx, mody, modangle = 0, 0, 0


def translate(x, y, ys=2): # ys это масштаб по у
    '''
    масштаб ys при переносе и при отрисовке соотносится как
    1/ys, пока оставим разные умолчания чтобы не замедлять 
    работу лишними делениями в больших циклах
    '''
    global modx, mody
    modx += x
    mody += y*ys
    
    
def rotate(angle):
    '''
    все повороты и переносы копим в переменных, это удобно
    '''
    global modangle
    modangle += angle


# ======================== вывод на экран

def frameRender():
    '''
    превращаем матрицу в строку в соотв. цветами из ramp,
    вписываем тексты, что надо зануляем, что надо прибавляем
    '''
    pixels = ''
    for j in range(height):
        for i in range(width):
            pixel = num2pixel(canvas[i, j], ramps[rampnumber], reverse=rampinvert)
            pixels += pixel
    for key in texts.keys():  # тексты
        x, y = texts[key]
        pos = width * int(y) + x
        pixels = strInsert(pixels, key, pos)
    print(pixels)
    global frameCount
    frameCount += 1



def interact(draw):
    '''
    отрисовка всего что есть в функции draw с таймаутом на ввод с клавиатуры
    FIXME нулевого столбца и строки не выводится после первого кадра
    '''
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
    curses.wrapper(run)
    
# ======================== вывод на экран
    
    
