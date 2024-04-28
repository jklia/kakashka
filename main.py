import copy
import pygame as pg
from random import sample, choice
from fields import Fields
from pygame import gfxdraw

pg.init()

flag_red_image = pg.transform.scale(pg.image.load('sprites/flag_red.png'), (36, 36))
flag_blue_image = pg.transform.scale(pg.image.load('sprites/flag_blue.png'), (36, 36))
house_image = pg.transform.scale(pg.image.load('sprites/house.png'), (30, 30))
tower_image = pg.transform.scale(pg.image.load('sprites/tower.png'), (44, 44))
knight_image = pg.transform.scale(pg.image.load('sprites/knight.png'), (36, 37))
peasant_image = pg.transform.scale(pg.image.load('sprites/peasant.png'), (36, 37))
lord_image = pg.transform.scale(pg.image.load('sprites/lord.png'), (36, 37))
tree_image = pg.transform.scale(pg.image.load('sprites/tree.png'), (36, 36))

person_shadow_image = pg.transform.scale(pg.image.load('sprites/shadow.png'), (38, 48))
person_shadow_image.set_alpha(70)
house_shadow_image = pg.transform.scale(pg.image.load('sprites/shadow.png'), (60, 52))
house_shadow_image.set_alpha(70)
tower_shadow_image = pg.transform.scale(pg.image.load('sprites/shadow.png'), (58, 52))
tower_shadow_image.set_alpha(70)
tree_shadow_image = pg.transform.scale(pg.image.load('sprites/shadow.png'), (52, 52))
tree_shadow_image.set_alpha(70)
flag_shadow_image = pg.transform.scale(pg.image.load('sprites/shadow.png'), (16, 32))
flag_shadow_image.set_alpha(70)

f1 = pg.font.Font(None, 36)

WIN_WIDTH = 574
WIN_HEIGHT = 730
X = 40
Y = 40
A = 30
MAP_WIDTH = 6

icon = pg.image.load('sprites/icon.png')
pg.display.set_icon(icon)
background_image = pg.image.load('sprites/background.png')
background_color = (30, 30, 45)
main_color = (45, 46, 58)
state_colors = [(131, 46, 46), (17, 62, 125)]

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
            dev_change_object(xm, ym, 'flag')
            break_flag = True
        elif e.key == pg.K_h:
            xm, ym = pg.mouse.get_pos()
            dev_change_object(xm, ym, 'house')
            break_flag = True
        elif e.key == pg.K_j:
            xm, ym = pg.mouse.get_pos()
            for dot in dots:
                if dot.inside(xm, ym):
                    if dot.object == '':
                        dev_change_object(xm, ym, 'peasant')
                    elif dot.object == 'peasant':
                        dev_change_object(xm, ym, 'knight')
                    elif dot.object == 'knight':
                        dev_change_object(xm, ym, 'lord')
                    elif dot.object == 'lord':
                        dev_change_object(xm, ym, '')
                    else:
                        dev_change_object(xm, ym, 'peasant')
            break_flag = True
        elif e.key == pg.K_t:
            xm, ym = pg.mouse.get_pos()
            dev_change_object(xm, ym, 'tree')
            break_flag = True
        elif e.key == pg.K_y:
            xm, ym = pg.mouse.get_pos()
            dev_change_object(xm, ym, 'tower')
            break_flag = True
    return break_flag


def dot_init():
    x_cord = 1
    y_cord = 0

    left = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144]
    right = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119, 131, 143, 155]
    up = [6, 7, 8, 9, 10, 11]
    very_up = [0, 1, 2, 3, 4, 5]
    down = [144, 145, 146, 147, 148, 149]
    very_down = [150, 151, 152, 152, 154, 155]

    friends = []
    x_cord = (i % 6) + 1
    if i % 6 == 0:
        y_cord += 1
    text1 = f1.render(str(i), 1, (180, 0, 0))

    if (i // MAP_WIDTH) % 1 == 0 and (i // MAP_WIDTH) % 2 == 1:
        friends = [i - 12, i - 5, i + 7, i + 12, i + 6, i - 6]

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

        return GameSprite(X + (A * 3 * (i % MAP_WIDTH)) + (A * 1.5), Y + ((A * (3 ** 0.5)) / 2) * (i // MAP_WIDTH),
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

            return GameSprite(X + (A * 3 * (i % MAP_WIDTH)), Y + ((A * (3 ** 0.5)) / 2) * (i // MAP_WIDTH), x_cord,
                              y_cord,
                              field[i][0],
                              field[i][1], field[i][2], state_colors, friends)


def change_land(xm, ym):
    for dot in dots:
        if dot.inside(xm, ym):
            if dot.land == 1:
                dot.land = 0
            else:
                dot.land = 1
            dot.change('simple')


def dev_change_object(xm, ym, object):
    for dot in dots:
        if dot.inside(xm, ym):
            if dot.object == object and dot.object:
                dot.object = ''
            else:
                dot.object = object
            dot.change('simple')


def change_object(cell, object):
    if cell.object == '':
        cell.object = object
    # добавить условие для деревьев, если на них наступит человек


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
                    change_object(dots_copy[cell], 'tree')
    dots = dots_copy


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
        self.a = A
        self.object = object
        self.point1 = (x + A, y)
        self.point4 = (x - A, y)
        self.point2 = (x + (A / 2), y + ((A * (3 ** 0.5)) / 2))
        self.point3 = (x - (A / 2), y + ((A * (3 ** 0.5)) / 2))
        self.point5 = (x - (A / 2), y - ((A * (3 ** 0.5)) / 2))
        self.point6 = (x + (A / 2), y - ((A * (3 ** 0.5)) / 2))

        self.rect = pg.Rect(self.point3[0], self.point5[1], 30, 60)
        self.tree = pg.Rect(self.x - 15, self.y - 15, 30, 60)

        if self.land == 0:
            self.color = background_color
        else:
            if self.state == 0:
                self.color = main_color
            else:
                self.color = self.colors[self.state - 1]

    def reset(self):
        if self.land != 0:
            gfxdraw.filled_polygon(window, (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6), self.color)
            # можно заменить lines на aalines для сглаживания — но не будет никакого ретро! :(
            pg.draw.lines(window, background_color, True, (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6))

        if self.object == 'flag':
            if self.state == 1:
                window.blit(flag_shadow_image, (self.x - 9, self.y - 12))
                window.blit(flag_red_image, (self.x - 10, self.y - 30))
            elif self.state == 2:
                window.blit(flag_shadow_image, (self.x - 9, self.y - 12))
                window.blit(flag_blue_image, (self.x - 10, self.y - 30))
        elif self.object == 'house':
            window.blit(house_shadow_image, (self.x - 30, self.y - 20))
            window.blit(house_image, (self.x - 15, self.y - 22))
        elif self.object == 'tower':
            window.blit(tower_shadow_image, (self.x - 29, self.y - 19))
            window.blit(tower_image, (self.x - 22, self.y - 34))
        elif self.object == 'peasant':
            window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            window.blit(peasant_image, (self.x - 18, self.y - 27))
        elif self.object == 'knight':
            window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            window.blit(knight_image, (self.x - 18, self.y - 27))
        elif self.object == 'lord':
            window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            window.blit(lord_image, (self.x - 18, self.y - 27))
        elif self.object == 'tree':
            window.blit(tree_shadow_image, (self.x - 26, self.y - 22))
            window.blit(tree_image, (self.x - 19, self.y - 30))

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


window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Antiyoy")
field = Fields.maps[3]  # 0 - стандартное поле, 1 - карта №1, 2 - пустое поле, 3 - карта №2

dots = []
for i in range(156):
    dot = dot_init()
    dots.append(dot)

game = True
finish = False
clock = pg.time.Clock()
FPS = 60

dev = True

while game:
    window.blit(background_image, (0, 0))
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        if dev and dev_mode(e):
            break
    for dot in dots:
        # tree_spreading()
        dot.reset()
    pg.display.update()
    clock.tick(FPS)

if dev:
    new_map = []
    for dot in dots:
        new_map.append((dot.land, dot.state, dot.object))
    print(new_map)
