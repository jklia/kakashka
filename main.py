import pygame as pg
from random import randint
from fields import Fields
from pygame import gfxdraw

state_colors = [(131, 46, 46), (31, 51, 154)]
flag_red_image = pg.image.load('flag_red.png')
flag_blue_image = pg.image.load('flag_blue.png')
house_image = pg.image.load('house.png')
person1_image = pg.transform.scale(pg.image.load('person1.png'), (40, 40))

win_width = 574
win_height = 730
background_color = (24, 44, 37)
main_color = (48, 104, 68)
# background_color = ('#312527')
# main_color= ('#9be654')
objects = ['flag', 'house', 'person']


def dev_mode(e):
    break_flag = False
    if e.type == pg.QUIT:
        break_flag = True
    elif e.type == pg.MOUSEBUTTONDOWN:
        if e.button == 1:
            xm, ym = e.pos
            for dot in dots:
                if dot.inside(xm, ym):
                    dot.state = 1
                    dot.change()
                    break_flag = True
        if e.button == 2:
            xm, ym = e.pos
            for dot in dots:
                if dot.inside(xm, ym):
                    dot.state = 0
                    dot.change()
                    break_flag = True
        if e.button == 3:
            xm, ym = e.pos
            for dot in dots:
                if dot.inside(xm, ym):
                    dot.state = 2
                    dot.change()
                    break_flag = True

    elif e.type == pg.KEYDOWN:
        if e.key == pg.K_g:
            xm, ym = pg.mouse.get_pos()
            change_land(xm, ym)
            break_flag = True
        elif e.key == pg.K_f:
            xm, ym = pg.mouse.get_pos()
            change_object(xm, ym, 'flag')
            break_flag = True
        elif e.key == pg.K_h:
            xm, ym = pg.mouse.get_pos()
            change_object(xm, ym, 'house')
            break_flag = True
        elif e.key == pg.K_j:
            xm, ym = pg.mouse.get_pos()
            change_object(xm, ym, 'person')
            break_flag = True
    return break_flag


def get_main(len):
    a = randint(0, len)
    b = randint(0, len)
    if b == a:
        b += randint(1, len - b)
    return [a, b]


def change_land(xm, ym):
    for dot in dots:
        if dot.inside(xm, ym):
            if dot.land == 1:
                dot.land = 0
            else:
                dot.land = 1
            dot.change()


def change_object(xm, ym, object):
    for dot in dots:
        if dot.inside(xm, ym):
            if dot.object == object:
                dot.object = ''
            else:
                dot.object = object
            dot.change()


cords = get_main(156)
cord1 = cords[0]
cord2 = cords[1]

x = 40
y = 40
a = 30

map_width = 6


class GameSprite(pg.sprite.Sprite):

    def __init__(self, x, y, land, state, object, colors):
        super().__init__()
        self.colors = colors
        self.state = state
        self.land = land
        self.x = x
        self.y = y
        self.a = a
        self.object = object
        self.point1 = (x + a, y)
        self.point4 = (x - a, y)
        self.point2 = (x + (a / 2), y + ((a * (3 ** 0.5)) / 2))
        self.point3 = (x - (a / 2), y + ((a * (3 ** 0.5)) / 2))
        self.point5 = (x - (a / 2), y - ((a * (3 ** 0.5)) / 2))
        self.point6 = (x + (a / 2), y - ((a * (3 ** 0.5)) / 2))

        self.rect = pg.Rect(self.point3[0], self.point5[1], 30, 60)

        if self.land == 0:
            self.color = background_color

        else:
            if self.state == 0:
                self.color = main_color
            else:
                self.color = self.colors[self.state - 1]

    def reset(self):
        # pg.draw.polygon(window, self.color,
        #                (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6))
        # pg.draw.polygon(window, background_color,
        #                (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6), 3)
        # обычная прорисовка ^

        gfxdraw.aapolygon(window, (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6),
                          self.color)
        gfxdraw.filled_polygon(window, (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6),
                               self.color)
        pg.draw.aalines(window, background_color, True, (
            (self.point1[0] + 1, self.point1[1]), (self.point2[0], self.point2[1] + 1),
            (self.point3[0] - 1, self.point3[1] + 1),
            (self.point4[0] - 1, self.point4[1]), (self.point5[0] - 1, self.point5[1] - 1),
            (self.point6[0], self.point6[1] - 1)))

        if self.object == 'flag':
            if self.state == 1:
                window.blit(flag_red_image, (self.x - 15, self.y - 15))
            elif self.state == 2:
                window.blit(flag_blue_image, (self.x - 15, self.y - 15))
        elif self.object == 'house':
            window.blit(house_image, (self.x - 15, self.y - 15))
        elif self.object == 'person':
            window.blit(person1_image, (self.x - 20, self.y - 20))

    def inside(self, x, y):
        return self.rect.collidepoint(x, y)

    def change(self):
        if self.land == 0:
            self.object = ''
            self.state = 0
            self.color = background_color
        else:
            if self.state == 0:
                self.color = main_color
            elif self.state != 0:
                self.color = self.colors[self.state - 1]


window = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Antiyoy")
window.fill(background_color)

dots = []
field = Fields.maps[3]  # 0 - стандартное поле, 1 - карта №1, 2 - пустое поле, 3 - карта №2

for i in range(156):
    if (i // map_width) % 1 == 0 and (i // map_width) % 2 == 1:
        dot = GameSprite(x + (a * 3 * (i % map_width)) + (a * 1.5), y + ((a * (3 ** 0.5)) / 2) * (i // map_width),
                         field[i][0], field[i][1], field[i][2], state_colors)
    else:
        dot = GameSprite(x + (a * 3 * (i % map_width)), y + ((a * (3 ** 0.5)) / 2) * (i // map_width), field[i][0],
                         field[i][1], field[i][2], state_colors)
    dots.append(dot)

game = True
finish = False
clock = pg.time.Clock()
FPS = 60

dev = True

while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        if dev and dev_mode(e):
            break

    for dot in dots:
        dot.reset()

    pg.display.update()
    clock.tick(FPS)

if dev:
    new_map = []
    for dot in dots:
        new_map.append((dot.land, dot.state, dot.object))
    print(new_map)
