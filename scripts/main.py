import copy
from random import choice, randint
from time import time
import pygame_gui
from pygame import gfxdraw

from misc import *
import config

# pip install -r requirements.txt

FPS = config.FPS
delay = config.delay

field = config.field
music_volume = config.music_volume
theme = config.theme

dev_flag = config.dev_flag
digits_flag = config.digits_flag
music_flag = config.music_flag
pause_flag = config.pause_flag
stress_test_flag = config.stress_test_flag

WIN_WIDTH = config.WIN_WIDTH
WIN_HEIGHT = config.WIN_HEIGHT
X = config.X
Y = config.Y
A = config.A
MAP_WIDTH = config.MAP_WIDTH

pg.init()
pg.display.set_icon(icon)
clock = pg.time.Clock()

window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pg.display.set_caption("Antiyoy")

objects = ['flag', 'house', 'lord', 'peasant', 'knight', 'tree', 'tower']
moving_objects = ['peasant', 'knight', 'lord']
static_objects = ['house', 'tree', 'tower', 'flag']
upgrading_objects = ['peasant', 'knight']
defense_objects = ['flag', 'tower', 'peasant', 'knight', 'lord']


class Players:

    def __init__(self, dots, state, money=10):
        self.dots = dots
        self.state = state
        self.money = money

    def salary(self):
        for dot in self.dots:
            if dot.state == self.state:
                if dot.obj == 'house':
                    self.money += 4
                if dot.obj != 'tree':
                    self.money += 1
                if dot.obj == 'peasant':
                    self.money -= 2
                if dot.obj == 'knight':
                    self.money -= 6
                if dot.obj == 'lord':
                    self.money -= 18

        if self.money < 0:
            for dot in self.dots:
                if dot.obj in moving_objects:
                    dot.change_object('')
                    print(f"State {['red', 'blue'][self.state - 1]} is starving due to lack of money ({self.money})")

    def move(self, cell, dest):
        available_move_flag = True
        if (self.dots[cell].obj in moving_objects) and cell != dest and self.dots[cell].state == self.state and \
                dest in dfs_moves(self.dots, cell) and self.dots[cell].blocked == 0:
            if self.dots[dest].state == self.dots[cell].state:
                if self.dots[dest].obj not in ['house', 'flag', 'tower']:
                    if self.dots[dest].obj == 'lord' or (
                            self.dots[dest].obj == 'knight' and self.dots[cell].obj in ['knight', 'lord']) or (
                            self.dots[dest].obj == 'peasant' and self.dots[cell].obj == 'lord'):
                        print(
                            f"No moves from cell {cell} to cell {dest} for state {['red', 'blue'][self.state - 1]} #1")
                        available_move_flag = False
                    else:
                        self.dots[dest].change_object(self.dots[cell].obj)
                else:
                    print(f"No moves from cell {cell} to cell {dest} for state {['red', 'blue'][self.state - 1]} #2")
                    available_move_flag = False
            else:
                self.dots[dest].obj = self.dots[cell].obj
                self.dots[dest].state = self.dots[cell].state

            if available_move_flag:
                self.dots[cell].obj = ''
                self.dots[cell].change_object('block0')
                self.dots[dest].change_object('block1')
                self.dots[dest].change()
                self.dots[cell].change()
        else:
            print(f"No moves from cell {cell} to cell {dest} for state {['red', 'blue'][self.state - 1]} #3")

    def build(self, obj, cell):
        near = False
        block = 0
        if self.dots[cell].land and self.dots[cell].obj not in ['house', 'flag', 'tower']:
            if obj == 'house':
                if self.money >= 12 and self.dots[cell].state == self.state and self.dots[cell].obj == '':
                    self.dots[cell].change_object(obj)
                    self.money -= 12
                else:

                    print(f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money}) "
                          f"for building {obj} or another problem occurred")
            elif obj == 'tower':
                if self.money >= 15 and self.dots[cell].state == self.state and self.dots[cell].obj == '':
                    self.dots[cell].change_object(obj)
                    self.money -= 15
                    print(f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money}) "
                          f"for building {obj} or another problem occurred")
            else:
                for i in self.dots[cell].friends:
                    if self.dots[i].state == self.state:
                        near = True
                        break
                if near:
                    if self.dots[cell].blocked == 1 or self.dots[cell].state != self.state or \
                            self.dots[cell].obj == 'tree':
                        block = 1
                    elif self.dots[cell].blocked == 0 or (
                            self.dots[cell].state == self.state and self.dots[cell].obj == ''):
                        block = 0
                    if obj == 'peasant':
                        if (self.money >= 10 and self.dots[cell].state != self.state and self.dots[
                            cell].defense <= 0) or (
                                self.money >= 10 and self.dots[cell].state == self.state):
                            if self.dots[cell].state != self.state:
                                self.dots[cell].obj = ''
                                self.dots[cell].state = self.state
                                self.dots[cell].change()
                            if block == 1:
                                self.dots[cell].change_object('block1')
                            else:
                                self.dots[cell].change_object('block0')
                            self.dots[cell].change_object(obj)
                            self.money -= 10
                        else:
                            print(f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money}) "
                                  f"for building {obj} or another problem occurred")
                    elif obj == 'knight':
                        if (self.money >= 20 and self.dots[cell].state != self.state and self.dots[
                            cell].defense <= 0) or \
                                (self.money >= 20 and self.dots[cell].state == self.state):
                            if self.dots[cell].state != self.state:
                                self.dots[cell].obj = ''
                                self.dots[cell].state = self.state
                                self.dots[cell].change()
                            if block == 1:
                                self.dots[cell].change_object('block1')
                            else:
                                self.dots[cell].change_object('block0')
                            self.dots[cell].change_object(obj)
                            self.money -= 20
                        else:
                            print(f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money}) "
                                  f"for building {obj} or another problem occurred")
                    elif obj == 'lord':
                        if (self.money >= 30 and self.dots[cell].state != self.state and self.dots[
                            cell].defense <= 0) or (
                                self.money >= 30 and self.dots[cell].state == self.state):
                            if self.dots[cell].state != self.state:
                                self.dots[cell].obj = ''
                                self.dots[cell].state = self.state
                                self.dots[cell].change()
                            if block == 1:
                                self.dots[cell].change_object('block1')
                            else:
                                self.dots[cell].change_object('block0')
                            self.dots[cell].change_object(obj)
                            self.money -= 30
                        else:
                            print(f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money}) "
                                  f"for building {obj} or another problem occurred")
        else:
            print(f'No land to build on cell {cell}')


class GameProcess:
    sec_counter = 0

    def __init__(self, players, dots):
        self.players = players
        self.dots = dots

    def bot(self, player):
        # count = False  # Нужен ли этот count, а если нужен, то зачем?
        for cell in self.dots:
            if cell.state == player.state:
                if cell.obj == '':
                    choice_object = choice(['peasant', 'knight', 'house', 'tower', 'lord'])
                    print(f"State {['red', 'blue'][cell.state - 1]} is building {choice_object} on cell {cell.counter}")
                    player.build(choice_object, cell.counter)
                elif cell.obj in moving_objects:
                    moves_list = list(dfs_moves(self.dots, cell.counter))
                    list_to_move = []
                    for move in moves_list:
                        if self.dots[move].state != cell.state:
                            list_to_move.append(move)
                    if not list_to_move:
                        list_to_move = moves_list
                    choice_move = choice(list_to_move)
                    print(
                        f"State {['red', 'blue'][cell.state - 1]} is moving {cell.obj} from "
                        f"cell {cell.counter} to cell {choice_move}")
                    player.move(cell.counter, choice_move)
                    # count = True
                    break
            # if count:
            #     break
        # print(player.money)

    def game(self):
        for cell in self.dots:
            cell.reset()
        pg.display.update()

    def bots(self):
        self.dots = set_defense(self.dots)
        self.players[0] = Players(self.dots, 1, self.players[0].money)
        self.players[1] = Players(self.dots, 2, self.players[0].money)
        if pause_flag:
            for player in self.players:
                self.bot(player)
                self.dots = set_defense(self.dots)
                for i in player.dots:
                    i.change_object('block0')
                for i in range(len(self.players)):
                    self.players[i] = Players(self.dots, i + 1, self.players[i].money)
                    self.players[i].salary()
                for cell in self.dots:
                    cell.reset()
            self.dots = tree_spreading(self.dots)
            for cell in self.dots:
                cell.reset()

    def main(self, timer, delay_time):
        self.game()
        if delay_time == 0:
            self.bots()
        else:
            if (timer // delay_time) != self.sec_counter:
                self.bots()
                self.sec_counter = timer // delay_time


class GameSprite:

    def __init__(self, x, y, x_cord, y_cord, land, state, obj, colors, friends, counter, defense, blocked):
        self.defense = defense
        self.blocked = blocked
        self.colors = colors
        self.state = state
        self.land = land
        self.friends = friends
        self.x = x
        self.y = y
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.a = A
        self.obj = obj
        self.counter = counter
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
                          (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6), width=1)

        if self.obj == 'flag':
            if self.state == 1:
                window.blit(flag_shadow_image, (self.x - 9, self.y - 12))
                window.blit(flag_red_image, (self.x - 10, self.y - 30))
            elif self.state == 2:
                window.blit(flag_shadow_image, (self.x - 9, self.y - 12))
                window.blit(flag_blue_image, (self.x - 10, self.y - 30))
        elif self.obj == 'house':
            window.blit(house_shadow_image, (self.x - 30, self.y - 20))
            window.blit(house_image, (self.x - 15, self.y - 22))
        elif self.obj == 'tower':
            window.blit(tower_shadow_image, (self.x - 29, self.y - 20))
            window.blit(tower_image, (self.x - 21, self.y - 34))
        elif self.obj == 'peasant':
            window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            window.blit(peasant_image, (self.x - 18, self.y - 27))
        elif self.obj == 'knight':
            window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            window.blit(knight_image, (self.x - 18, self.y - 27))
        elif self.obj == 'lord':
            window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            window.blit(lord_image, (self.x - 18, self.y - 27))
        elif self.obj == 'tree':
            window.blit(tree_shadow_image, (self.x - 26, self.y - 22))
            window.blit(tree_image, (self.x - 19, self.y - 30))
        if digits_flag:
            text = f1.render(str(self.counter), True, (196, 196, 30))
            text.set_alpha(210)
            text_shadow = f1.render(str(self.counter), True, (0, 0, 0))
            text_shadow.set_alpha(190)
            place = text.get_rect(center=(self.x, self.y))
            place_shadow1 = text_shadow.get_rect(center=(self.x + 1, self.y + 2))
            place_shadow2 = text_shadow.get_rect(center=(self.x, self.y - 1))
            window.blit(text_shadow, place_shadow1)
            window.blit(text_shadow, place_shadow2)
            window.blit(text, place)

    def inside(self, x, y):  # dev function
        return self.rect.collidepoint(x, y)

    def change(self):
        if self.land == 0:
            self.obj = ''
            self.state = 0
            self.color = background_color
        else:
            if self.state == 0:
                self.color = main_color
            elif self.state != 0:
                self.color = self.colors[self.state - 1]

    def change_object(self, obj):
        if obj == 'block0':
            self.blocked = 0
        elif obj == 'block1':
            self.blocked = 0
        elif obj not in moving_objects:
            if self.obj == '':
                self.obj = obj
                if obj == 'tower':
                    self.defense = 2
            if obj == '':
                self.obj = obj
        else:
            if self.obj == '' or self.obj == 'tree':
                self.obj = obj
                if obj == 'knight':
                    self.defense = 1
                if obj == 'lord':
                    self.defense = 2
            elif self.obj == 'peasant' and obj == 'peasant':
                self.obj = 'knight'
                self.defense = 1
            elif (self.obj == 'peasant' and obj == 'knight') or (self.obj == 'knight' and obj == 'peasant'):
                self.obj = 'lord'
                self.defense = 2

    def get_defense(self):
        defense = 0
        if self.obj in ['flag', 'knight']:
            defense = 1
        elif self.obj in ['lord', 'tower']:
            defense = 2
        return defense


def dot_init(i):
    left = [0, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120, 132, 144]
    right = [11, 23, 35, 47, 59, 71, 83, 95, 107, 119, 131, 143, 155]
    up = [6, 7, 8, 9, 10, 11]
    very_up = [0, 1, 2, 3, 4, 5]
    down = [144, 145, 146, 147, 148, 149]
    very_down = [150, 151, 152, 152, 154, 155]

    defense = 0
    blocked = -1

    x_cord = (i % 6) + 1
    y_cord = 0

    if i % 6 == 0:
        y_cord += 1

    if field[i][2] in moving_objects:
        blocked = 0

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
                          field[i][0], field[i][1], field[i][2], state_colors, friends, i, defense, blocked)

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
                              field[i][1], field[i][2], state_colors, friends, i, defense, blocked)


def dots_init():
    dots = []
    for i in range(156):
        dot = dot_init(i)
        dots.append(dot)
    return dots


def set_defense(dots):
    dots_copy = copy.deepcopy(dots)
    for dot in dots_copy:
        if dot.obj not in defense_objects:
            dot.defense = 0
    for dot in dots:
        if dot.obj in defense_objects:
            dfs_list = dfs_defense(dots, dot.counter)
            defense = dot.get_defense()
            for i in dfs_list:
                if dots_copy[i].defense < defense:
                    dots_copy[i].defense = defense
    return dots_copy


def dfs_moves(dots, cell, depth=3, visited=None, origin=None, attack=0):
    friends = set()
    if attack == 0:
        if dots[cell].obj == 'peasant':
            attack = 1
        elif dots[cell].obj == 'knight':
            attack = 2
        elif dots[cell].obj == 'lord':
            attack = 3
    if origin is None:
        origin = dots[cell]
    if visited is None:
        visited = set()
    if depth >= 0:
        depth -= 1
        if origin.obj in moving_objects:
            for friend in dots[cell].friends:
                if dots[cell].state and (dots[friend].defense < attack or dots[friend].state == origin.state):
                    for n_friend in dots[friend].friends:
                        if dots[n_friend].state == origin.state:
                            friends.add(friend)
            visited.add(cell)
        elif origin.obj in static_objects:
            return visited
        for next_friend in friends:
            dfs_moves(dots, next_friend, depth, visited, origin, attack)
    return visited


def dfs_defense(dots, cell, depth=1, visited=None, origin=None):
    friends = set()
    if origin is None:
        origin = dots[cell].state
    if visited is None:
        visited = set()
    if depth >= 0:
        depth -= 1
        if cell:
            for friend in dots[cell].friends:
                if dots[friend].state == origin:
                    friends.add(friend)
            visited.add(cell)
        for next_friend in friends:
            dfs_defense(dots, next_friend, depth, visited, origin)
    return visited


def tree_spreading(dots):
    j = randint(1, 5)
    dots_copy = copy.deepcopy(dots)
    if j != 1:
        return dots_copy
    else:
        for dot in dots:
            if dot.obj == 'tree':
                k = randint(1, 5)
                if k == 1:
                    cell = choice(dot.friends)
                    if cell and dots_copy[cell].land != 0:
                        dots_copy[cell].change_object('tree')
        return dots_copy


# Демонстрация работы DFS
def dfs_show(dots, start, mode, dfs_list=None):
    if mode == 'defense':
        dfs_list = dfs_defense(dots, start)
    elif mode == 'moves':
        dfs_list = dfs_moves(dots, start)
    dots[start].color = (dots[start].color[0] + 75, dots[start].color[1] + 75, dots[start].color[2] + 75)
    if dfs_list is not None:
        for i in dfs_list:
            dots[i].color = (dots[i].color[0] + 45, dots[i].color[1] + 45, dots[i].color[2] + 45)
            dots[i].reset()


def game_pause(e, button):
    global pause_flag
    if e.type == pygame_gui.UI_BUTTON_PRESSED:
        if e.ui_element == button:
            if pause_flag:
                pause_flag = False
                button.set_text('Game ON')
            else:
                pause_flag = True
                button.set_text('Game OFF')


def digits_show(e, button):
    global digits_flag
    if e.type == pygame_gui.UI_BUTTON_PRESSED:
        if e.ui_element == button:
            if digits_flag:
                digits_flag = False
                button.set_text('Digits ON')
            else:
                digits_flag = True
                button.set_text('Digits OFF')


orig_delay = delay


def freeze(e, button):
    global delay
    if e.type == pygame_gui.UI_BUTTON_PRESSED:
        if e.ui_element == button:
            if delay == 0:
                delay = orig_delay
                button.set_text('Speed up')
            else:
                delay = 0
                button.set_text('Slow down')


def music_pause(e, button):
    global music_flag
    if e.type == pygame_gui.UI_BUTTON_PRESSED:
        if e.ui_element == button:
            if pg.mixer.music.get_busy():
                pg.mixer.music.pause()
                button.set_text('Music ON')
            else:
                pg.mixer.music.unpause()
                button.set_text('Music OFF')


def button_manager():
    manager = pygame_gui.UIManager((WIN_WIDTH, WIN_HEIGHT))
    if music_flag:
        mb_text = 'Music OFF'
    else:
        mb_text = 'Music ON'
    music_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((WIN_WIDTH - 141, WIN_HEIGHT - 45), (131, 40)),
                                                text=mb_text, manager=manager)
    if digits_flag:
        dg_text = 'Digits OFF'
    else:
        dg_text = 'Digits ON'
    digits_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((WIN_WIDTH - 282, WIN_HEIGHT - 45), (131, 40)),
                                                 text=dg_text, manager=manager)
    if pause_flag:
        p_text = 'Game OFF'
    else:
        p_text = 'Game ON'
    game_pause_button = pygame_gui.elements.UIButton(
        relative_rect=pg.Rect((WIN_WIDTH - 423, WIN_HEIGHT - 45), (131, 40)),
        text=p_text, manager=manager)

    if delay == orig_delay:
        fr_text = 'Speed up'
    else:
        fr_text = 'Slow down'
    freezer_button = pygame_gui.elements.UIButton(relative_rect=pg.Rect((WIN_WIDTH - 564, WIN_HEIGHT - 45), (131, 40)),
                                                  text=fr_text, manager=manager)
    return manager, music_button, digits_button, game_pause_button, freezer_button


def game_init():
    manager, music_button, digits_button, game_pause_button, freezer_button = button_manager()

    pg.mixer.music.load(tracks[randint(0, len(tracks) - 1)])
    pg.mixer.music.set_volume(music_volume)
    pg.mixer.music.play(-1)
    if not music_flag:
        pg.mixer.music.pause()

    # player1 - красный, player2 - синий
    dots = set_defense(dots_init())
    player1 = Players(dots, 1, 200)
    player2 = Players(dots, 2, 200)
    gp = GameProcess([player1, player2], dots)

    starting_timer = time()

    # dfs_show(dots, 130, 'moves')  # Визуализация работы DFS для нахождения возможных ходов для 130 клетки

    game = True

    while game:
        time_delta = clock.tick(FPS) / 1000
        for e in pg.event.get():
            if e.type == pg.QUIT:
                game = False

            music_pause(e, music_button)
            game_pause(e, game_pause_button)
            digits_show(e, digits_button)
            freeze(e, freezer_button)

            manager.process_events(e)

        manager.update(time_delta)
        window.blit(background_image, (0, 0))
        manager.draw_ui(window)

        # Стресс-тест игры:
        if stress_test_flag:
            listw = []
            for i in range(1, 1000):
                for j in range(i):
                    listw.append(j ** 10)

        ending_timer = time()
        timer = ending_timer - starting_timer
        gp.main(timer, delay)  # delay = 0 без ограничений, delay > 0 — задержка между ходами в секундах

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    game_init()
