
import os
import time
import datetime
import math

from tinynumpy import tinynumpy as tnp  # это для класса Frame

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
'█▓▒░ '
]

def mapp(value, start1, stop1, start2, stop2):
    '''
    мапинг value из диапазона start1..stop1 к диапазону start2..stop2 
    '''
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

def getTermSize():
    '''
    ширина и высота терминала в символах
    w, h = getTermSize()
    '''
    (width, height) = os.get_terminal_size()
    return (width, height)

def millisTotal():
    ''' милисекунды от сотворения мира '''
    return round(time.time() * 1000)

def sketchStarting():
    '''
    начинаем считать милисекунды скетча
    '''
    global millis_start
    millis_start = datetime.datetime.now()

def millis():
    ''' милисекунды от начала скетча '''
    dt = datetime.datetime.now() - millis_start
    return dt.total_seconds() * 1000

def frameStart():
    '''
    начинаем считать милисекунды кадра
    '''
    global millis_framestart
    millis_framestart = datetime.datetime.now()

def frameRate(f):
    '''
    задаём глобальные переменные числа кадров и длительности кадра
    '''
    global frame_rate, frame_period_millis
    frame_rate = f
    frame_period_millis = 1/f*1000

def frameEnd():
    '''
    в конце кадра спим в соответствии с фреймрейтом
    если конечно фреймрейт из-за тормозом не ниже заданного =)
    '''
    now = datetime.datetime.now()
    dtf = now-millis_framestart
    frame_millis = dtf.total_seconds()*1000
    if frame_millis < frame_period_millis:
        time.sleep((frame_period_millis-frame_millis)*0.001)



class Frame:
    '''
    Кадр это по сути матрица width на height заполненная числами
    от 0 до 255, которые соответствуют нужной яркости пикселя,
    который визуализируется через тот или иной символ строки из ramps.
    '''
    
    rampnumber = 1  ## выбор палитры из ramps
    rampinvert = False ## инверсия палитры

    frameCount = -1  # это -1й кадр, setup
    modx, mody, modangle = 0, 0, 0  ## это для tramslate и rotate
    strokecolor = 255  # цвет контура по умолчанию
    pixels = ''
    #### key = ''  # интерактивность, храним кнопку с клавы
    const = {}  # хранилище всяких констант скетча, 
    # пока из-за обёртки curses.wrapper(run) их не получается 
    # нормально хранить иначе 
 
    def __init__(self, w, h):
        self.canvas = tnp.zeros((h,w))
        self.w = w
        self.h = h
    def translate(self, x, y, ys=2): # ys это масштаб по у
        '''
        масштаб ys при переносе и при отрисовке соотносится как
        1/ys, пока оставим разные умолчания чтобы не замедлять 
        работу лишними делениями в больших циклах
        '''
        self.modx += x
        self.mody += y*ys
    def rotate(self, angle):
        '''
        все повороты и переносы копим в переменных, это удобно
        '''
        self.modangle += angle
    def initFrame(self):
        '''
        пока здесь только обновление координат, можно сюда
        втащить frame start и всё такое прочее, чтобы не 
        раздувать код каждого отдельного скетча
        '''
        self.modx, self.mody, self.modangle = 0, 0, 0
   
    def stroke(self, color, alpha=255):
        '''
        pass
        '''
        self.strokecolor = color
        self.strokealpha = alpha


    def background(self, color, alpha=255):
        '''
        увы, tiny numpy это не numpy и складывать и умножать 
        матрицу и число он не умеет, поэтому перебор
        с учётом прозрачности заливки
        '''
        for j in range(self.w):
            for i in range(self.h):
                self.canvas[i, j] = mixColorsByAlpha(self.canvas[i, j], color, alpha)


    def point(self, x, y, ys=0.5):
        '''
        рисуем точку, ys это масштаб по высоте т.к. в терминале символы
        вписаны в прямоугольники с соотношением сторон 1:2
        '''
        if self.modx!=0:
            x+=self.modx
        if self.mody!=0:
            y+=self.mody
        if self.modangle!=0:
            x, y = rotateCoords((self.modx, self.mody), (x, y), self.modangle)
        y = y*ys
        if 0<=x<self.w and 0<=y<self.h:
            i, j = int(x), int(y)  # итое и житое периодически меняются местами =)

            self.canvas[j, i] = mixColorsByAlpha(self.canvas[j, i], 
                self.strokecolor, 
                self.strokealpha)

            if self.canvas[j,i] > 255:
                self.canvas[j,i] = 255
            if self.canvas[j,i] < 0:
                self.canvas[j,i] = 0
        else:
            pass
    
    texts = {}
    def text(self, s, x, y, ys=0.5):
        '''
        собираем все тексты в словарь, потом в draw 
        выводим строку в pixels после матрицы цветов
        '''
        self.texts.update({s : [x, y*ys]}) # это потом вспоминаем по ключам в draw. кстати надо draw переименовать бы. и вовсе загнать всё в frm

    def drawFrame(self):
        '''
        превращаем матрицу в строку в соотв. цветами из ramp,
        вписываем тексты, что надо зануляем, что надо прибавляем
        '''
        for j in range(self.h):
            for i in range(self.w):
                pixel = num2pixel(self.canvas[j,i], ramps[self.rampnumber], reverse=self.rampinvert)
                self.pixels+=pixel
        for key in self.texts.keys():  # тексты
            x, y = self.texts[key]
            pos = self.w * int(y) + x
            self.pixels = strInsert(self.pixels, key, pos)
        print(self.pixels)
        self.pixels = ''
        self.frameCount += 1

# Функции для Frame:

def reversedString(s):
    '''
    строка задом наперёд
    '''
    return s[::-1]

def num2pixel(num, ramp, reverse=False):
    '''
    перевод числа num от 0 до 255 в номер символа строки ramp
    reverse "инвертирует" "цвет"
    '''
    if reverse:
        ramp = reversedString(ramp)
    i = int(mapp(num, 0, 255, 0, len(ramp)-1))
    return ramp[i]

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

def mixColorsByAlpha(old_color, color, alpha):
    '''
    для Frame
    '''
    dc = color - old_color
    new_old_color = old_color + dc * mapp(alpha, 0, 255, 0, 1)
    return new_old_color

