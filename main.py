import copy
import pygame as pg
from random import sample, choice, randint
from fields import Fields
from pygame import gfxdraw
import pygame_gui

from game_render import (flag_red_image, flag_blue_image, house_image, tower_image, knight_image, peasant_image,
                         lord_image, tree_image, person_shadow_image, house_shadow_image, tower_shadow_image,
                         tree_shadow_image, flag_shadow_image, icon, background_image, background_color, main_color,
                         state_colors, f1, tracks)

# from dev import Dev

pg.init()
pg.display.set_icon(icon)

WIN_WIDTH = 574
# Изначально 730
WIN_HEIGHT = 780
X = 40
Y = 40
A = 30
MAP_WIDTH = 6

objects = ['flag', 'house', 'lord', 'peasant', 'knight', 'tree', 'tower']
moving_objects = ['peasant', 'knight', 'lord']
static_objects = ['house', 'tree', 'tower']
defense_objects = ['flag', 'tower', 'peasant', 'knight', 'lord']


class Players:

    def __init__(self, field, id, state, money=10):
        self.field = field
        self.id = id
        self.state = state
        self.money = money

    def count(self):
        for cell in self.field:
            if cell.state == self.state:
                if cell.object == 'house':
                    self.money += 4
                if cell.object != 'tree':
                    self.money += 1
                if cell.object == 'peasant':
                    self.money -= 2
                if cell.object == 'knight':
                    self.money -= 6
                if cell.object == 'lord':
                    self.money -= 18

    def default(self, cell):
        self.field[cell].object = ''
        self.field[cell].defense = 0

    def move(self, cell, dest):
        # добавить условия по дфсу, сделать дфс для досту
        if (self.field[cell].object in moving_objects) and (
                self.field[dest].object not in static_objects or self.field[dest].object == 'tree') and cell != dest:
            self.field[dest].change_object(self.field[cell].object)
            self.field[dest].state = self.field[cell].state
            self.default(cell)
            self.field[dest].change()
            self.field[cell].change()

    def build(self, object, cell):
        near = 0
        if object == 'house':
            if self.money >= 12 and self.field[cell].state == self.state:
                self.field[cell].change_object(object)
                self.money -= 12
        elif object == 'tower':
            if self.money >= 15 and self.field[cell].state == self.state:
                self.field[cell].change_object(object)
                self.money -= 15
        else:
            for i in self.field[cell].friends:
                if self.field[i].state == self.state:
                    near = 1
                    break
            if near == 1:
                if object == 'peasant':
                    if (self.money >= 10 and self.field[cell].state != self.state and self.field[cell].defense <= 0) or \
                            (self.money >= 10 and self.field[cell].state == self.state):
                        if self.field[cell].state != self.state:
                            self.default(cell)
                        self.field[cell].change_object(object)
                        self.money -= 10
                        if self.field[cell].state != self.state:
                            self.field[cell].state = self.state
                            self.field[cell].change()
                elif object == 'knight':
                    if (self.money >= 20 and self.field[cell].state != self.state and self.field[cell].defense <= 1) or \
                            (self.money >= 20 and self.field[cell].state == self.state):
                        if self.field[cell].state != self.state:
                            self.default(cell)
                        self.field[cell].change_object(object)
                        self.money -= 20
                        if self.field[cell].state != self.state:
                            self.field[cell].state = self.state
                            self.field[cell].change()
                elif object == 'lord':
                    if (self.money >= 30 and self.field[cell].state != self.state and self.field[cell].defense <= 2) or \
                            (self.money >= 30 and self.field[cell].state == self.state):
                        if self.field[cell].state != self.state:
                            self.default(cell)
                        self.field[cell].change_object(object)
                        self.money -= 30
                        if self.field[cell].state != self.state:
                            self.field[cell].state = self.state
                            self.field[cell].change()


class Dev:
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
                Dev.dev_change_object(xm, ym, 'flag')
                break_flag = True
            elif e.key == pg.K_h:
                xm, ym = pg.mouse.get_pos()
                Dev.dev_change_object(xm, ym, 'house')
                break_flag = True
            elif e.key == pg.K_j:
                xm, ym = pg.mouse.get_pos()
                for dot in dots:
                    if dot.inside(xm, ym):
                        if dot.object == '':
                            Dev.dev_change_object(xm, ym, 'peasant')
                        elif dot.object == 'peasant':
                            Dev.dev_change_object(xm, ym, 'knight')
                        elif dot.object == 'knight':
                            Dev.dev_change_object(xm, ym, 'lord')
                        elif dot.object == 'lord':
                            Dev.dev_change_object(xm, ym, '')
                        else:
                            Dev.dev_change_object(xm, ym, 'peasant')
                break_flag = True
            elif e.key == pg.K_t:
                xm, ym = pg.mouse.get_pos()
                Dev.dev_change_object(xm, ym, 'tree')
                break_flag = True
            elif e.key == pg.K_y:
                xm, ym = pg.mouse.get_pos()
                Dev.dev_change_object(xm, ym, 'tower')
                break_flag = True
        return break_flag

    def dev_change_object(xm, ym, object):
        for dot in dots:
            if dot.inside(xm, ym):
                if dot.object == object and dot.object:
                    dot.object = ''
                else:
                    dot.object = object
                dot.change()


def dfs_moves(cell, depth=3, visited=None, ally=True, origin=None):
    global dots
    friends = set()
    if origin is None: origin = dots[cell].state
    if visited is None: visited = set()
    if dots[cell].state == 0:
        ally = False
    else:
        ally = True

    if depth >= 0:
        depth -= 1
        if cell:
            for friend in dots[cell].friends:
                if ally:
                    for n_friend in dots[friend].friends:
                        if dots[n_friend].state == origin:
                            friends.add(friend)
            visited.add(cell)
        for next in friends:
            dfs_moves(next, depth, visited, ally, origin)
    return visited


def dfs_defense(cell, depth=1, visited=None, origin=None):
    global dots
    friends = set()
    if origin is None: origin = dots[cell].state
    if visited is None: visited = set()
    if depth >= 0:
        depth -= 1
        if cell:
            for friend in dots[cell].friends:
                if dots[friend].state == origin:
                    friends.add(friend)
            visited.add(cell)
        for next in friends:
            dfs_defense(next, depth, visited, origin)
    return visited


def change_land(xm, ym):
    for dot in dots:
        if dot.inside(xm, ym):
            if dot.land == 1:
                dot.land = 0
            else:
                dot.land = 1
            dot.change()


def dot_init(i):
    x_cord = 1
    y_cord = 0

    left = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144]
    right = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119, 131, 143, 155]
    up = [6, 7, 8, 9, 10, 11]
    very_up = [0, 1, 2, 3, 4, 5]
    down = [144, 145, 146, 147, 148, 149]
    very_down = [150, 151, 152, 152, 154, 155]

    friends = []
    defense = 0
    x_cord = (i % 6) + 1
    if i % 6 == 0:
        y_cord += 1

    # text1 = f1.render(str(i), 1, (180, 0, 0))

    if field[i][2] == 'knight' or field[i][2] == 'flag':
        defense = 1
    elif field[i][2] == 'lord' or field[i][2] == 'tower':
        defense = 2

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
            for j in range(len(friends)):
                if friends[j] >= 155 or field[friends[j]][0] == 0:
                    friends[j] = False
        while False in friends:
            friends.remove(False)
        return GameSprite(X + (A * 3 * (i % MAP_WIDTH)) + (A * 1.5), Y + ((A * (3 ** 0.5)) / 2) * (i // MAP_WIDTH),
                          x_cord, y_cord,
                          field[i][0], field[i][1], field[i][2], state_colors, friends, i, defense)

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
            for j in range(len(friends)):
                if friends[j] >= 155 or field[friends[j]][0] == 0:
                    friends[j] = False
            while False in friends:
                friends.remove(False)
            return GameSprite(X + (A * 3 * (i % MAP_WIDTH)), Y + ((A * (3 ** 0.5)) / 2) * (i // MAP_WIDTH), x_cord,
                              y_cord,
                              field[i][0],
                              field[i][1], field[i][2], state_colors, friends, i, defense)


def tree_spreading(count=0):
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
                    dots_copy[cell].change_object('tree')
    dots = dots_copy


class GameSprite():

    def __init__(self, x, y, x_cord, y_cord, land, state, object, colors, friends, id, defense, text=''):
        self.defense = defense
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
        self.id = id
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
            gfxdraw.filled_polygon(window,
                                   (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6),
                                   self.color)
            pg.draw.lines(window, background_color, True,
                          (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6))

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
        if digits:
            text = f1.render(str(self.id), True, (156, 156, 1))
            place = text.get_rect(center=(self.x, self.y))
            window.blit(text, place)

    def set_defense(self):
        if self.object in defense_objects:
            dfs_list = dfs_defense(self.id)
            for i in dfs_list:
                if dots[i].defense < self.defense:
                    dots[i].defense = self.defense
            # print(i, dots[i].defense, self.defense)

    def inside(self, x, y):  # dev function
        return self.rect.collidepoint(x, y)

    def change(self, way='simple'):
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

    def change_object(self, object):
        if object != 'peasant' and object != 'knight' and object != 'lord':
            if self.object == '':
                self.object = object
                if object == 'tower':
                    self.defense = 2
                    for i in self.friends:
                        dots[i].defense = 2
        else:
            if self.object == '' or self.object == 'tree':
                self.object = object
                if object == 'knight':
                    self.defense = 1
                if object == 'lord':
                    self.defense = 2
            elif self.object == 'peasant' and object == 'peasant':
                self.object = 'knight'
                self.defense = 1
            elif (self.object == 'peasant' and object == 'knight') or (self.object == 'knight' and object == 'peasant'):
                self.object = 'lord'
                self.defense = 2


window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Antiyoy")

field = Fields.maps[3]  # 0 - стандартное поле, 1 - карта №1, 2 - пустое поле, 3 - карта №2

game = True
finish = False
clock = pg.time.Clock()
FPS = 60

dev = True
digits = True
music = True

manager = pygame_gui.UIManager((WIN_WIDTH, WIN_HEIGHT))
music_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((5, WIN_HEIGHT - 45), (90, 40)),
                                            text='Music OFF',
                                            manager=manager)


# print(music_button.colours)

# music_button.colours['normal_bg'][0] = 76
# music_button.colours['normal_bg'][1] = 24
# music_button.colours['normal_bg'][2] = 24


def pause(self, button):
    if e.type == pygame_gui.UI_BUTTON_PRESSED:
        if e.ui_element == button:
            if pg.mixer.music.get_busy():
                pg.mixer.music.pause()
                button.set_text('Music ON')
            else:
                pg.mixer.music.unpause()
                button.set_text('Music OFF')


# def field_init():
#     global dots
#     for i in range(156):
#         dot = dot_init(i)
#         dots.append(dot)
#     for dot in dots:
#         dot.set_defense()
#
# dots = field_init()


dots = []
for i in range(156):
    dot = dot_init(i)
    dots.append(dot)
for dot in dots:
    dot.set_defense()

if music:
    pg.mixer.music.load(tracks[randint(0, len(tracks) - 1)])
    pg.mixer.music.set_volume(0.2)
    pg.mixer.music.play(-1)


# Как работает DFS
def dfs_show(start, depth, mode):
    if mode == 'defense':
        dfs_list = dfs_defense(start)
    elif mode == 'moves':
        dfs_list = dfs_moves(start, depth)
    dots[start].color = (dots[start].color[0] + 75, dots[start].color[1] + 75, dots[start].color[2] + 75)
    for i in dfs_list:
        dots[i].color = (dots[i].color[0] + 45, dots[i].color[1] + 45, dots[i].color[2] + 45)
        dots[i].reset()


player1 = Players(dots, 1, 1)
player1.move(130, 130)

print(dots[130].object)

dfs_show(136, 3, 'defense')
dfs_show(25, 3, 'moves')

while game:
    time_delta = clock.tick(60) / 1000
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        pause(e, music_button)

        if dev and Dev.dev_mode(e):
            break

        manager.process_events(e)

    manager.update(time_delta)

    window.blit(background_image, (0, 0))
    manager.draw_ui(window)

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
