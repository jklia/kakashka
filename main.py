import copy
import pygame as pg
from random import sample, choice
from fields import Fields
from pygame import gfxdraw

pg.init()

state_colors = [(131, 46, 46), (17, 62, 125)]
flag_red_image = pg.transform.scale(pg.image.load('flag_red.png'), (35, 35))
flag_blue_image = pg.transform.scale(pg.image.load('flag_blue.png'), (35, 35))
house_image = pg.transform.scale(pg.image.load('house.png'), (35, 35))
tower_image = pg.transform.scale(pg.image.load('tower.png'), (35, 35))
knight_image = pg.transform.scale(pg.image.load('knight.png'), (35, 35))
peasant_image = pg.transform.scale(pg.image.load('peasant.png'), (35, 35))
lord_image = pg.transform.scale(pg.image.load('lord.png'), (35, 35))
tree_image = pg.transform.scale(pg.image.load('tree.png'), (35, 35))
f1 = pg.font.Font(None, 36)

win_width = 574
win_height = 730

# background_color = (24, 44, 37)
# main_color = (48, 104, 68)
background_image = pg.image.load('background.png')
background_color = (30, 30, 45)
main_color = (59, 59, 74)

objects = ['flag', 'house', 'lord', 'peasant', 'knight', 'tree', 'tower']


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
                    dot.change('simple')
                    break_flag = True
        if e.button == 2:
            xm, ym = e.pos
            for dot in dots:
                if dot.inside(xm, ym):
                    dot.state = 0
                    dot.change('simple')
                    break_flag = True
        if e.button == 3:
            xm, ym = e.pos
            for dot in dots:
                if dot.inside(xm, ym):
                    dot.state = 2
                    dot.change('simple')
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
            for dot in dots:
                if dot.inside(xm, ym):
                    if dot.object == '':
                        change_object(xm, ym, 'peasant')
                    elif dot.object == 'peasant':
                        change_object(xm, ym, 'knight')
                    elif dot.object == 'knight':
                        change_object(xm, ym, 'lord')
                    elif dot.object == 'lord':
                        change_object(xm, ym, '')
                    else:
                        change_object(xm, ym, 'peasant')
            break_flag = True
        elif e.key == pg.K_t:
            xm, ym = pg.mouse.get_pos()
            change_object(xm, ym, 'tree')
            break_flag = True
        elif e.key == pg.K_y:
            xm, ym = pg.mouse.get_pos()
            change_object(xm, ym, 'tower')
            break_flag = True
    return break_flag


# def get_main(len):
#     a = randint(0, len)
#     b = randint(0, len)
#     if b == a:
#         b += randint(1, len - b)
#     return [a, b]


def change_land(xm, ym):
    for dot in dots:
        if dot.inside(xm, ym):
            if dot.land == 1:
                dot.land = 0
            else:
                dot.land = 1
            dot.change('simple')


def change_object(xm, ym, object):
    for dot in dots:
        if dot.inside(xm, ym):
            if dot.object == object and dot.object:
                dot.object = ''
            else:
                dot.object = object
            dot.change('simple')


def next_change_object(cell, object):
    if cell.object == '':
        cell.object = object


def tree_spreading():
    global count
    global dots
    j = choice([0, 0, 1])
    if j != 1:
        return
    count += 1
    dots_copy = [i for i in (dots)]
    if dot.object == 'tree':
        k = choice([0, 0, 1])
        if k != 0:
            f = sample(dot.friends, k)
            for cell in f:
                if cell and dots_copy[cell].land != 0:
                    next_change_object(dots_copy[cell], 'tree')
    dots = dots_copy


x = 40
y = 40
a = 30

map_width = 6


class GameSprite(pg.sprite.Sprite):

    def __init__(self, x, y, x_cord, y_cord, land, state, object, colors, friends, text=''):
        super().__init__()
        self.colors = colors
        self.state = state
        self.land = land
        self.friends = friends
        self.x = x
        self.y = y
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.a = a
        self.object = object
        self.point1 = (x + a, y)
        self.point4 = (x - a, y)
        self.point2 = (x + (a / 2), y + ((a * (3 ** 0.5)) / 2))
        self.point3 = (x - (a / 2), y + ((a * (3 ** 0.5)) / 2))
        self.point5 = (x - (a / 2), y - ((a * (3 ** 0.5)) / 2))
        self.point6 = (x + (a / 2), y - ((a * (3 ** 0.5)) / 2))

        self.rect = pg.Rect(self.point3[0], self.point5[1], 30, 60)
        self.tree = pg.Rect(self.x - 15, self.y - 15, 30, 60)

        self.text = text

        if self.land == 0:
            self.color = background_color
        else:
            if self.state == 0:
                self.color = main_color
            else:
                self.color = self.colors[self.state - 1]

    def reset(self):
        if self.land !=0:
            gfxdraw.filled_polygon(window, (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6),
                               self.color)
            # заменить lines на aalines для сглаживания — но не будет никакого ретро! :(
            pg.draw.lines(window, background_color, True, (
                (self.point1[0] + 0.5, self.point1[1]), (self.point2[0] + 1, self.point2[1] + 1),
                (self.point3[0] - 2.5, self.point3[1] + 1),
                (self.point4[0], self.point4[1]), (self.point5[0] - 1, self.point5[1] - 1),
                (self.point6[0] + 1, self.point6[1] - 1)))

        if self.object == 'flag':
            if self.state == 1:
                window.blit(flag_red_image, (self.x - 10, self.y - 35))
            elif self.state == 2:
                window.blit(flag_blue_image, (self.x - 10, self.y - 35))
        elif self.object == 'house':
            window.blit(house_image, (self.x - 17, self.y - 30))
        elif self.object == 'tower':
            window.blit(tower_image, (self.x - 17, self.y - 30))
        elif self.object == 'peasant':
            window.blit(peasant_image, (self.x - 17, self.y - 30))
        elif self.object == 'knight':
            window.blit(knight_image, (self.x - 17, self.y - 30))
        elif self.object == 'lord':
            window.blit(lord_image, (self.x - 17, self.y - 30))
        elif self.object == 'tree':
            window.blit(tree_image, (self.x - 18, self.y - 30))

        #window.blit(self.text, (self.x - 15, self.y - 15))

    def inside(self, x, y):
        return self.rect.collidepoint(x, y)

    def change(self, way):
        if way == 'simple':
            if self.land == 0:
                self.object = ''
                self.state = 0
                self.color = background_color
            else:
                if self.state == 0:
                    self.color = main_color
                elif self.state != 0:
                    self.color = self.colors[self.state - 1]
        elif way == 'tree':
            if self.object == '':
                self.object = 'tree'
            # elif self.object == 'tree':
            #     self.object = ''



window = pg.display.set_mode((win_width, win_height))
pg.display.set_caption("Antiyoy")
# window.fill(background_color)
window.blit(background_image, (0, 0))
dots = []
field = Fields.maps[3]  # 0 - стандартное поле, 1 - карта №1, 2 - пустое поле, 3 - карта №2

x_cord = 1
y_cord = 0
left = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144]
right = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119, 131, 143, 155]
up = [6, 7, 8, 9, 10, 11]
very_up = [0, 1, 2, 3, 4, 5]
down = [144, 145, 146, 147, 148, 149]
very_down = [150, 151, 152, 152, 154, 155]

for i in range(156):
    friends = []

    x_cord = (i % 6) + 1
    if i % 6 == 0:
        y_cord += 1
    text1 = f1.render(str(i), 1, (180, 0, 0))

    if (i // map_width) % 1 == 0 and (i // map_width) % 2 == 1:
        friends = [i - 12, i - 5, i + 7, i + 12, i + 6, i - 6]

        for f in range(6):
            # if friends[f] < 0 or friends[f] > 155:
            if i in up:
                friends[0] = False
            if i in very_up:
                friends[0] = False
                friends[1] = False
                friends[5] = False
            if i in down:
                friends[3] = False
            if i in very_down:
                friends[2] = False
                friends[3] = False
                friends[4] = False
            if i in right:
                friends[1] = False
                friends[2] = False
            if i in left:
                friends[4] = False
                friends[5] = False

        dot = GameSprite(x + (a * 3 * (i % map_width)) + (a * 1.5), y + ((a * (3 ** 0.5)) / 2) * (i // map_width),
                         x_cord, y_cord,
                         field[i][0], field[i][1], field[i][2], state_colors, friends)
    else:
        friends = [i - 12, i - 6, i + 6, i + 12, i + 5, i - 7]

        for f in range(6):
            if i in up:
                friends[0] = False
            if i in very_up:
                friends[0] = False
                friends[1] = False
                friends[5] = False
            if i in down:
                friends[3] = False
            if i in very_down:
                friends[2] = False
                friends[3] = False
                friends[4] = False
            if i in right:
                friends[1] = False
                friends[2] = False
            if i in left:
                friends[4] = False
                friends[5] = False
            # if friends[f] < 0 or friends[f] > 155:
            # friends[f] = '-'

        dot = GameSprite(x + (a * 3 * (i % map_width)), y + ((a * (3 ** 0.5)) / 2) * (i // map_width), x_cord, y_cord,
                         field[i][0],
                         field[i][1], field[i][2], state_colors, friends)

    dots.append(dot)
    # print(i, friends, x_cord, y_cord)
game = True
finish = False
clock = pg.time.Clock()
FPS = 60

dev = True
count = 0
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        if dev and dev_mode(e):
            break
    for dot in dots:
        #tree_spreading()
        dot.reset()
    pg.display.update()
    clock.tick(FPS)

if dev:
    new_map = []
    for dot in dots:
        new_map.append((dot.land, dot.state, dot.object))
    print(new_map)
