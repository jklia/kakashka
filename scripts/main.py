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
logs_flag = config.logs_flag
color_cor_flag = config.color_cor_flag

WIN_WIDTH = config.WIN_WIDTH
WIN_HEIGHT = config.WIN_HEIGHT
X = config.X
Y = config.Y
A = config.A
MAP_WIDTH = config.MAP_WIDTH

pg.init()
pg.display.set_icon(icon)
clock = pg.time.Clock()

pg.display.set_caption("Python Antiyoy")

window = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
window.fill(background_color)

game_window = pg.Surface((WIN_WIDTH, WIN_HEIGHT - 50))

if color_cor_flag:
    color_cor = pg.Surface((WIN_WIDTH, WIN_HEIGHT - 50))
    color_cor.fill((22, 9, 50))
    color_cor.set_alpha(30)

objects = ['flag', 'house', 'lord', 'peasant', 'knight', 'tree', 'tower']
moving_objects = ['peasant', 'knight', 'lord']
static_objects = ['house', 'tree', 'tower', 'flag']
upgrading_objects = ['peasant', 'knight']
defense_objects = ['flag', 'tower', 'peasant', 'knight', 'lord']


class Players:

    def __init__(self, dots, state, money=None, cells=0):
        if money is None:
            money = {-1: 10}
        self.dots = dots
        self.state = state
        self.money = money
        self.flags = []
        self.cells_amount = cells
        self.cells_indexes = []

    def start_money(self):
        for i in self.flags:
            self.money[i] = self.money[-1]
        del self.money[-1]

    def find_flag(self, start):
        if self.dots[start].obj == 'flag':
            return start
        else:
            visited = []
            queue = []
            flag = 0
            visited.append(start)
            queue.append(start)
            start_state = self.state
            while queue:
                cell = queue.pop(0)
                for neighbour in self.dots[cell].friends:
                    if (neighbour is not False and neighbour not in visited and
                            self.dots[neighbour].state == start_state):
                        visited.append(neighbour)
                        queue.append(neighbour)
                        if self.dots[neighbour].obj == 'flag':
                            flag = neighbour
                            break
            return flag

    def salary(self):
        for cell in self.flags:
            area = bfs_group(self.dots, cell)
            for dot in area:
                if self.dots[dot].state == self.state:
                    if self.dots[dot].obj == 'house':
                        self.money[cell] += 4
                    if self.dots[dot].obj != 'tree':
                        self.money[cell] += 1
                    if self.dots[dot].obj == 'peasant':
                        self.money[cell] -= 2
                    if self.dots[dot].obj == 'knight':
                        self.money[cell] -= 6
                    if self.dots[dot].obj == 'lord':
                        self.money[cell] -= 18

            if self.money[cell] < 0:
                for dot in area:
                    if self.dots[dot].obj in moving_objects:
                        self.dots[dot].change_object('')
                        if logs_flag:
                            print(
                                f"State {['red', 'blue'][self.state - 1]}"
                                f" is starving due to lack of money ({self.money})")

    def move(self, cell, dest):
        available_move_flag = True
        if (self.dots[cell].obj in moving_objects) and cell != dest and self.dots[cell].state == self.state and \
                dest in dfs_moves(self.dots, cell) and self.dots[cell].blocked == 0:
            if self.dots[dest].state == self.dots[cell].state:
                if self.dots[dest].obj not in ['house', 'flag', 'tower']:
                    if self.dots[dest].obj == 'lord' or (
                            self.dots[dest].obj == 'knight' and self.dots[cell].obj in ['knight', 'lord']) or (
                            self.dots[dest].obj == 'peasant' and self.dots[cell].obj == 'lord'):
                        if logs_flag:
                            print(
                                f"No moves from cell {cell} to cell {dest}"
                                f" for state {['red', 'blue'][self.state - 1]} #1")
                        available_move_flag = False
                    else:
                        self.dots[dest].change_object(self.dots[cell].obj)
                else:
                    if logs_flag:
                        print(
                            f"No moves from cell {cell} to cell {dest} for state {['red', 'blue'][self.state - 1]} #2")
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
            if logs_flag:
                print(f"No moves from cell {cell} to cell {dest} for state {['red', 'blue'][self.state - 1]} #3")

    def build(self, obj, cell):
        near = False
        block = 0
        change_back = True
        changed = False
        first_state = 0
        first_object = ''
        if self.dots[cell].state != self.state:
            changed = True
            first_state = self.dots[cell].state
            first_object = self.dots[cell].obj
            self.dots[cell].obj = ''
            self.dots[cell].state = self.state
            self.dots[cell].change()
        flag = self.find_flag(cell)
        if self.dots[cell].land:
            if obj == 'house':
                if self.money[flag] >= 12 and self.dots[cell].state == self.state and self.dots[cell].obj == '':
                    self.dots[cell].change_object(obj)
                    self.money[flag] -= 12
                else:
                    if logs_flag:
                        print(f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money})"
                              f" for building {obj} or another problem occurred")
            elif obj == 'tower':
                if self.money[flag] >= 15 and self.dots[cell].state == self.state and self.dots[cell].obj == '':
                    self.dots[cell].change_object(obj)
                    self.money[flag] -= 15
                    if logs_flag:
                        print(f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money})"
                              f" for building {obj} or another problem occurred")
            else:
                if self.dots[cell].state == self.state:
                    near = True
                else:
                    for i in self.dots[cell].friends:
                        if self.dots[i].state == self.state:
                            near = True
                            break
                if near:
                    if self.dots[cell].blocked == 1 or changed or self.dots[cell].obj == 'tree':
                        block = 1
                    elif self.dots[cell].blocked == 0 or (not changed and self.dots[cell].obj == ''):
                        block = 0
                    if obj == 'peasant':
                        if ((self.money[flag] >= 10 and changed and self.dots[cell].defense <= 0) or
                                (self.money[flag] >= 10 and not changed)):
                            change_back = False
                            if block == 1:
                                self.dots[cell].change_object('block1')
                            else:
                                self.dots[cell].change_object('block0')
                            self.dots[cell].change_object(obj)
                            self.money[flag] -= 10
                        else:
                            if logs_flag:
                                print(
                                    f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money})"
                                    f" for building {obj} or another problem occurred")
                    elif obj == 'knight':
                        if (self.money[flag] >= 20 and changed and self.dots[cell].defense <= 1) or \
                                (self.money[flag] >= 20 and not changed):
                            change_back = False
                            if block == 1:
                                self.dots[cell].change_object('block1')
                            else:
                                self.dots[cell].change_object('block0')
                            self.dots[cell].change_object(obj)
                            self.money[flag] -= 20

                        else:
                            if logs_flag:
                                print(
                                    f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money})"
                                    f" for building {obj} or another problem occurred")
                    elif obj == 'lord':
                        if (self.money[flag] >= 30 and changed) or (
                                self.money[flag] >= 30 and not changed):
                            change_back = False
                            if block == 1:
                                self.dots[cell].change_object('block1')
                            else:
                                self.dots[cell].change_object('block0')
                            self.dots[cell].change_object(obj)
                            self.money[flag] -= 30
                        else:
                            if logs_flag:
                                print(
                                    f"State {['red', 'blue'][self.state - 1]} does not have enough money ({self.money})"
                                    f" for building {obj} or another problem occurred")
                if changed and change_back:
                    self.dots[cell].obj = first_object
                    self.dots[cell].state = first_state
                    self.dots[cell].change()
        else:
            if logs_flag:
                print(f'No land to build on cell {cell}')

    def group_count(self):
        for cell in self.dots:
            if cell.state == self.state:
                self.cells_amount += 1
                self.cells_indexes.append(cell.counter)
                if cell.obj == 'flag':
                    self.flags += [cell.counter]


class Country:
    def __init__(self, dots, players):
        self.dots = dots
        self.players = players

    def analyse(self):
        for player in self.players:
            cells = player.cells_indexes
            multiple_flags = []
            multiple = []
            for cell in self.dots:
                if cell.obj == 'flag' and cell.state == player.state:
                    country_cells = bfs_group(self.dots, cell.counter)
                    if sorted(country_cells) in multiple_flags:
                        ind = multiple_flags.index(sorted(country_cells))
                        player.money[multiple[ind]] += player.money[cell.counter]
                        del player.money[cell.counter]
                        cell.change_object('')
                    else:
                        multiple_flags.append(sorted(country_cells))
                        multiple.append(cell.counter)
                        for cell_to_del in country_cells:
                            if cell_to_del in cells:
                                cells.remove(cell_to_del)
            if cells:
                while cells:
                    country_cells = bfs_group(self.dots, cells[0])
                    for cell_to_del in country_cells:
                        if cell_to_del in cells:
                            cells.remove(cell_to_del)
                    if len(country_cells) <= 3:
                        for cell_to_change in country_cells:
                            self.dots[cell_to_change].state = 0
                            self.dots[cell_to_change].change()
                            self.dots[cell_to_change].change_object('')
                    if len(country_cells) > 3:
                        k = choice(country_cells)
                        self.dots[k].change_object('flag')
                        player.money[k] = 0
        return self.dots


class GameProcess:
    def __init__(self, players, dots, analyzer):
        self.players = players
        self.dots = dots
        self.analyzer = analyzer
        self.available_area = 0
        for dot in self.dots:
            if dot.land != 0:
                self.available_area += 1
        self.last_count = state_counter(self.dots, self.players)
        self.sec_counter = 0
        self.changes_timer = 0
        self.win_flag = False
        self.winner = None
        self.players_area = dict()
        self.logs_deployed = False

    def bot(self, player):
        for cell in self.dots:
            if cell.state == player.state:
                if cell.obj == '':
                    choice_object = choice(['peasant', 'knight', 'house', 'tower', 'lord'])
                    if logs_flag:
                        print(
                            f"State {['red', 'blue'][cell.state - 1]}"
                            f" is building {choice_object} on cell {cell.counter}")
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
                    if logs_flag:
                        print(
                            f"State {['red', 'blue'][cell.state - 1]} is moving {cell.obj} from"
                            f" cell {cell.counter} to cell {choice_move}")
                    player.move(cell.counter, choice_move)
                    break

    def adaptive_bot(self, player):
        available_area = 0
        our_area = 0
        for dot in self.dots:
            if dot.land != 0:
                available_area += 1
            if dot.state == player.state:
                our_area += 1
        if our_area / ((available_area / 100) + 0.00000000001) < 40:
            for flag in player.flags:
                area = bfs_group(self.dots, flag)
                get = 0
                spend = 0
                for dot in area:
                    if self.dots[dot].obj == 'knight':
                        spend += 6
                    if self.dots[dot].obj == 'lord':
                        spend += 18
                    if self.dots[dot].obj == 'peasant':
                        spend += 2
                    if self.dots[dot].obj != 'tree' and self.dots[dot].obj not in moving_objects:
                        get += 1
                    if self.dots[dot].obj == 'house':
                        get += 4
                    if self.dots[dot].obj in moving_objects:
                        cells = list(dfs_moves(self.dots, dot))
                        g = 0
                        if flag < 78:
                            cells.sort()
                        else:
                            cells.sort(reverse=True)
                        for cell in cells:
                            if self.dots[cell].state != player.state and \
                                    self.dots[dot].defense >= self.dots[cell].defense:
                                g += 1
                                player.move(dot, cell)
                                break
                            elif self.dots[cell].state == player.state and self.dots[cell].obj == 'tree':
                                g += 1
                                player.move(dot, cell)
                                break

                        if g == 0:
                            if flag < 78:
                                player.move(dot, max(cells))
                            else:
                                player.move(dot, min(cells))
                if get - spend >= 2:
                    border_cells = bfs_borders(self.dots, flag)
                    for i in range(min((get - spend) // 2, len(border_cells))):
                        if self.dots[border_cells[i]].defense == 0:
                            player.build('peasant', border_cells[i])
        else:
            for flag in player.flags:
                area = bfs_group(self.dots, flag)
                get = 0
                spend = 0
                free_area_cells = []
                for dot in area:
                    if self.dots[dot].obj == 'knight':
                        spend += 6
                    if self.dots[dot].obj == 'lord':
                        spend += 18
                    if self.dots[dot].obj == 'peasant':
                        spend += 2
                    if self.dots[dot].obj != 'tree' and self.dots[dot].obj not in moving_objects:
                        get += 1
                    if self.dots[dot].obj == 'house':
                        get += 4
                    if self.dots[dot].obj == '':
                        free_area_cells.append(dot)
                if 30 <= get - spend < 50:
                    for dot in area:
                        if self.dots[dot].obj in moving_objects:
                            cells = list(dfs_moves(self.dots, dot))
                            if flag < 78:
                                cells.sort()
                            else:
                                cells.sort(reverse=True)
                                for cell in cells:
                                    if self.dots[cell].state != player.state and \
                                            self.dots[dot].defense >= self.dots[cell].defense:
                                        player.move(dot, cell)
                                        break
                                    elif self.dots[cell].state == player.state and self.dots[cell].obj == 'tree':
                                        player.move(dot, cell)
                                        break
                    if flag < 78:
                        free_area_cells.sort()
                    else:
                        free_area_cells.sort(reverse=True)
                    for i in range(min((get - spend) // 12, len(free_area_cells))):
                        player.build('house', free_area_cells[i])

                elif get - spend < 30:
                    for dot in area:
                        if self.dots[dot].obj in moving_objects:
                            cells = list(dfs_moves(self.dots, dot))
                            if flag < 78:
                                cells.sort(reverse=True)
                            else:
                                cells.sort()
                            for cell in cells:
                                if self.dots[cell].state != player.state and \
                                        self.dots[dot].defense >= self.dots[cell].defense:
                                    player.move(dot, cell)
                                    break
                                elif self.dots[cell].state == player.state and self.dots[cell].obj == 'tree':
                                    player.move(dot, cell)
                                    break
                    border_cells = bfs_borders(self.dots, flag)
                    # i = 0
                    while border_cells:
                        for fri in self.dots[border_cells[0]].friends:
                            ind = 0
                            if self.dots[fri].state == player.state:
                                if self.dots[fri].defense != 2:
                                    player.build('tower', fri)
                                    ind += 1
                                for f in self.dots[fri].friends:
                                    if f in border_cells:
                                        border_cells.remove(f)
                                    elif player.state == self.dots[f].state and ind > 0:
                                        self.dots[f].defense = 2
                        # i += 1
                elif 50 <= get - spend < 70:
                    for dot in area:
                        if self.dots[dot].obj in moving_objects:
                            cells = list(dfs_moves(self.dots, dot))
                            g = 0
                            if flag < 78:
                                cells.sort()
                            else:
                                cells.sort(reverse=True)
                            for cell in cells:
                                if self.dots[cell].state != player.state and \
                                        self.dots[dot].defense >= self.dots[cell].defense:
                                    g += 1
                                    player.move(dot, cell)
                                    break
                                elif self.dots[cell].state == player.state and \
                                        self.dots[cell].defense + self.dots[dot].defense <= 3:
                                    g += 1
                                    player.move(dot, cell)
                                    break
                            if g == 0:
                                if flag < 78:
                                    player.move(dot, choice(self.dots[dot].friends))
                                else:
                                    player.move(dot, choice(self.dots[dot].friends))
                    if get - spend >= 6:
                        border_cells = bfs_borders(self.dots, flag)
                        for i in range(min((get - spend) // 6, len(border_cells))):
                            player.build('knight', border_cells[i])

                else:
                    for dot in area:
                        if self.dots[dot].obj in moving_objects:
                            cells = list(dfs_moves(self.dots, dot))
                            g = 0
                            if flag < 78:
                                cells.sort()
                            else:
                                cells.sort(reverse=True)
                            for cell in cells:
                                if self.dots[cell].state != player.state and \
                                        self.dots[dot].defense >= self.dots[cell].defense:
                                    g += 1
                                    player.move(dot, cell)
                                    break
                                elif self.dots[cell].state == player.state and \
                                        self.dots[cell].defense + self.dots[dot].defense <= 3:
                                    g += 1
                                    player.move(dot, cell)
                                    break
                            if g == 0:
                                if flag < 78:
                                    player.move(dot, choice(self.dots[dot].friends))
                                else:
                                    player.move(dot, choice(self.dots[dot].friends))
                    if get - spend >= 18:
                        border_cells = bfs_borders(self.dots, flag)
                        for i in range(min((get - spend) // 18, len(border_cells))):
                            player.build('lord', border_cells[i])

    def win_checker(self):
        self.players_area = state_counter(self.dots, self.players)
        for player in self.players:
            if self.players_area[player.state] > self.available_area * 0.75:
                self.win_flag = True
                self.winner = player
                if logs_flag and not self.logs_deployed:
                    self.logs_deployed = True
                    print(f"State {['red', 'blue'][self.winner.state - 1]} wins due to the capture of most territories")

    def game(self):
        for cell in self.dots:
            cell.reset()
        window.blit(game_window, (0, 0))
        if color_cor_flag:
            window.blit(color_cor, (0, 0))
        if self.win_flag:
            win_screen(self.winner)
        pg.display.update()

    def bots(self):
        if not pause_flag:
            if self.last_count == state_counter(self.dots, self.players):
                self.changes_timer += 1
            else:
                self.changes_timer = 0
            self.last_count = state_counter(self.dots, self.players)

            for i in range(len(self.players)):
                self.players[i] = Players(self.dots, i + 1, self.players[i].money)
                self.players[i].group_count()

            for player in self.players:
                if player.state == 2:
                    self.adaptive_bot(player)
                elif player.state == 1:
                    self.bot(player)
                self.dots = set_defense(self.dots)
                for i in player.dots:
                    i.change_object('block0')
                for i in range(len(self.players)):
                    self.players[i] = Players(self.dots, i + 1, self.players[i].money)
                    self.players[i].group_count()
                self.analyzer = Country(self.dots, self.players)
                self.dots = self.analyzer.analyse()
                for i in range(len(self.players)):
                    self.players[i] = Players(self.dots, i + 1, self.players[i].money)
                    self.players[i].group_count()
                    self.players[i].salary()
                for cell in self.dots:
                    cell.reset()

            self.win_checker()
            self.dots = set_defense(self.dots)
            self.dots = tree_spreading(self.dots)
            for cell in self.dots:
                cell.reset()

    def main(self, timer, delay_time):
        self.game()
        if not self.win_flag and self.changes_timer < 10:
            if delay_time == 0:
                self.bots()
            else:
                if (timer // delay_time) != self.sec_counter:
                    self.bots()
                    self.sec_counter = timer // delay_time

        else:
            self.win_flag = True
            players_dict = state_counter(self.dots, self.players)
            self.winner = self.players[max(players_dict, key=players_dict.get) - 1]
            if logs_flag and not self.logs_deployed:
                self.logs_deployed = True
                print(f"State {['red', 'blue'][self.winner.state - 1]} wins due to passivity of all states")


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
            gfxdraw.filled_polygon(game_window,
                                   (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6),
                                   self.color)
            pg.draw.lines(game_window, background_color, True,
                          (self.point1, self.point2, self.point3, self.point4, self.point5, self.point6), width=1)

        if self.obj == 'flag':
            if self.state == 1:
                game_window.blit(flag_shadow_image, (self.x - 9, self.y - 12))
                game_window.blit(flag_red_image, (self.x - 10, self.y - 30))
            elif self.state == 2:
                game_window.blit(flag_shadow_image, (self.x - 9, self.y - 12))
                game_window.blit(flag_blue_image, (self.x - 10, self.y - 30))
        elif self.obj == 'house':
            game_window.blit(house_shadow_image, (self.x - 30, self.y - 20))
            game_window.blit(house_image, (self.x - 15, self.y - 22))
        elif self.obj == 'tower':
            game_window.blit(tower_shadow_image, (self.x - 29, self.y - 20))
            game_window.blit(tower_image, (self.x - 21, self.y - 34))
        elif self.obj == 'peasant':
            game_window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            game_window.blit(peasant_image, (self.x - 18, self.y - 27))
        elif self.obj == 'knight':
            game_window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            game_window.blit(knight_image, (self.x - 18, self.y - 27))
        elif self.obj == 'lord':
            game_window.blit(person_shadow_image, (self.x - 19, self.y - 16))
            game_window.blit(lord_image, (self.x - 18, self.y - 27))
        elif self.obj == 'tree':
            game_window.blit(tree_shadow_image, (self.x - 26, self.y - 22))
            game_window.blit(tree_image, (self.x - 19, self.y - 30))
        if digits_flag:
            text = f1.render(str(self.counter), True, (196, 196, 30))
            text.set_alpha(210)
            text_shadow = f1.render(str(self.counter), True, (0, 0, 0))
            text_shadow.set_alpha(190)
            place = text.get_rect(center=(self.x, self.y))
            place_shadow1 = text_shadow.get_rect(center=(self.x + 1, self.y + 2))
            place_shadow2 = text_shadow.get_rect(center=(self.x, self.y - 1))
            game_window.blit(text_shadow, place_shadow1)
            game_window.blit(text_shadow, place_shadow2)
            game_window.blit(text, place)

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
        elif obj == 'flag':
            self.obj = obj
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

    land = field[i][0]
    state = field[i][1]
    obj = field[i][2]

    x_cord = (i % 6) + 1
    y_cord = 0

    if i % 6 == 0:
        y_cord += 1

    if land == 0:
        state = 0
        obj = ''

    if obj in moving_objects:
        blocked = 0

    if obj == 'knight' or obj == 'flag':
        defense = 1
    elif obj == 'lord' or obj == 'tower':
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
                          x_cord, y_cord, land, state, obj, state_colors, friends, i, defense, blocked)

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
            return GameSprite(X + (A * 3 * (i % MAP_WIDTH)), Y + ((A * (3 ** 0.5)) / 2) * (i // MAP_WIDTH),
                              x_cord, y_cord, land, state, obj, state_colors, friends, i, defense, blocked)


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
                if dots[cell].state and (dots[friend].defense < attack or dots[friend].state == origin.state) and \
                        dots[friend] not in visited:
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
        if cell is not False:
            for friend in dots[cell].friends:
                if dots[friend].state == origin and dots[friend] not in visited:
                    friends.add(friend)
            visited.add(cell)
        for next_friend in friends:
            dfs_defense(dots, next_friend, depth, visited, origin)
    return visited


def bfs_group(dots, start):
    visited = []
    queue = []
    visited.append(start)
    queue.append(start)
    origin = dots[start].state
    while queue:
        cell = queue.pop(0)
        for neighbour in dots[cell].friends:
            if neighbour is not False and neighbour not in visited and dots[neighbour].state == origin:
                visited.append(neighbour)
                queue.append(neighbour)
    return visited


def bfs_borders(dots, start):
    visited = []
    queue = []
    ret = []
    visited.append(start)
    queue.append(start)
    origin = dots[start].state
    while queue:
        cell = queue.pop(0)
        for neighbour in dots[cell].friends:
            if neighbour is not False and neighbour not in visited and dots[neighbour].state == origin:
                visited.append(neighbour)
                queue.append(neighbour)
            if neighbour is not False and dots[neighbour].state != origin and neighbour not in ret:
                ret.append(neighbour)
    return ret


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
def show(dots, start, mode, dfs_list=None):
    if mode == 'defense':
        dfs_list = dfs_defense(dots, start)
    elif mode == 'moves':
        dfs_list = dfs_moves(dots, start)
    elif mode == 'groups':
        dfs_list = bfs_group(dots, start)
    elif mode == 'borders':
        dfs_list = bfs_borders(dots, start)
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
                button.set_text('Game OFF')
            else:
                pause_flag = True
                button.set_text('Game ON')


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
        p_text = 'Game ON'
    else:
        p_text = 'Game OFF'
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


def win_screen(winner):
    end_window = pg.Surface((WIN_WIDTH, WIN_HEIGHT - 50))

    text = f2.render('GAME OVER', False, (166, 166, 0))
    place = text.get_rect(center=(WIN_WIDTH // 2, (WIN_HEIGHT - 200) // 2))

    text_shadow = f2.render('GAME OVER', False, (0, 0, 0))
    place_shadow = text.get_rect(center=(WIN_WIDTH // 2, (WIN_HEIGHT - 200) // 2 + 3))

    info_text = f3.render(f'Player #{winner.state} wins', False, state_accent_colors[winner.state - 1])
    place_info = info_text.get_rect(center=(WIN_WIDTH // 2, (WIN_HEIGHT - 200) // 2 + 100))

    info_shadow = f3.render(f'Player #{winner.state} wins', False, (0, 0, 0))
    place_shadow_info = info_text.get_rect(center=(WIN_WIDTH // 2, (WIN_HEIGHT - 200) // 2 + 103))

    end_window.fill((0, 0, 0))
    end_window.set_alpha(200)

    window.blit(end_window, (0, 0))
    window.blit(text_shadow, place_shadow)
    window.blit(text, place)
    window.blit(info_shadow, place_shadow_info)
    window.blit(info_text, place_info)


def state_counter(dots, players):
    players_area = dict.fromkeys([player.state for player in players], 0)
    for player in players:
        for dot in dots:
            if dot.state == player.state:
                players_area[player.state] += 1
    return players_area


def game_init():
    manager, music_button, digits_button, game_pause_button, freezer_button = button_manager()

    pg.mixer.music.load(tracks[randint(0, len(tracks) - 1)])
    pg.mixer.music.set_volume(0)
    pg.mixer.music.play(-1)
    if not music_flag:
        pg.mixer.music.pause()
    pg.mixer.music.set_volume(music_volume)

    # player1 - красный, player2 - синий
    dots = set_defense(dots_init())
    player1 = Players(dots, 1)
    player1.group_count()
    player1.start_money()
    player2 = Players(dots, 2)
    player2.group_count()
    player2.start_money()
    analyser = Country(dots, [player1, player2])
    dots = analyser.analyse()
    gp = GameProcess([player1, player2], dots, analyser)

    starting_timer = time()
    # show(dots, 145, 'borders')  # Визуализация работы DFS для нахождения возможных ходов для 130 клетки

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
        game_window.blit(background_image, (0, 0))
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
