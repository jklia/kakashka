#
# from scripts.config import (WIN_WIDTH, WIN_HEIGHT, MAP_WIDTH, X, Y, A, FPS, delay, dev_flag, digits_flag, bots_flag,
#                             music_flag, game, field)
#
# from scripts.misc import (flag_red_image, flag_blue_image, house_image, tower_image, knight_image, peasant_image,
#                           lord_image, tree_image, person_shadow_image, house_shadow_image, tower_shadow_image,
#                           tree_shadow_image, flag_shadow_image, icon, background_image, background_color, main_color,
#                           state_colors, f1, tracks)
#
# import os
# import copy
# from random import sample, choice, randint
# from time import time
#
# import pygame as pg
# import pygame_gui
# from pygame import gfxdraw

# class Dev:
#     def dev_mode(self, e):
#         break_flag = False
#         if e.type == pg.QUIT:
#             break_flag = True
#         elif e.type == pg.MOUSEBUTTONDOWN:
#             if e.button == 1:
#                 xm, ym = e.pos
#                 for dot in dots:
#                     if dot.inside(xm, ym):
#                         dot.state = 1
#                         dot.change()
#                         break_flag = True
#             if e.button == 2:
#                 xm, ym = e.pos
#                 for dot in dots:
#                     if dot.inside(xm, ym):
#                         dot.state = 0
#                         dot.change()
#                         break_flag = True
#             if e.button == 3:
#                 xm, ym = e.pos
#                 for dot in dots:
#                     if dot.inside(xm, ym):
#                         dot.state = 2
#                         dot.change()
#                         break_flag = True
#
#         elif e.type == pg.KEYDOWN:
#             if e.key == pg.K_g:
#                 xm, ym = pg.mouse.get_pos()
#                 self.dev_change_land(xm, ym)
#                 break_flag = True
#             elif e.key == pg.K_f:
#                 xm, ym = pg.mouse.get_pos()
#                 self.dev_change_object(xm, ym, 'flag')
#                 break_flag = True
#             elif e.key == pg.K_h:
#                 xm, ym = pg.mouse.get_pos()
#                 self.dev_change_object(xm, ym, 'house')
#                 break_flag = True
#             elif e.key == pg.K_j:
#                 xm, ym = pg.mouse.get_pos()
#                 for dot in dots:
#                     if dot.inside(xm, ym):
#                         if dot.object == '':
#                             self.dev_change_object(xm, ym, 'peasant')
#                         elif dot.object == 'peasant':
#                             self.dev_change_object(xm, ym, 'knight')
#                         elif dot.object == 'knight':
#                             self.dev_change_object(xm, ym, 'lord')
#                         elif dot.object == 'lord':
#                             self.dev_change_object(xm, ym, '')
#                         else:
#                             self.dev_change_object(xm, ym, 'peasant')
#                 break_flag = True
#             elif e.key == pg.K_t:
#                 xm, ym = pg.mouse.get_pos()
#                 self.dev_change_object(xm, ym, 'tree')
#                 break_flag = True
#             elif e.key == pg.K_y:
#                 xm, ym = pg.mouse.get_pos()
#                 self.dev_change_object(xm, ym, 'tower')
#                 break_flag = True
#         return break_flag
#
#     @staticmethod
#     def dev_change_object(xm, ym, object):
#         for dot in dots:
#             if dot.inside(xm, ym):
#                 if dot.object == object and dot.object:
#                     dot.object = ''
#                 else:
#                     dot.object = object
#                 dot.change()
#
#     @staticmethod
#     def dev_change_land(xm, ym):
#         for dot in dots:
#             if dot.inside(xm, ym):
#                 if dot.land == 1:
#                     dot.land = 0
#                 else:
#                     dot.land = 1
#                 dot.change()

# player1.move(130, 136)
# dots = set_defense(dots)
# player1 = Players(dots, 1)
# player2 = Players(dots, 2)
#
# player2.move(148, 136)
# dots = set_defense(dots)
# player1 = Players(dots, 1)
# player2 = Players(dots, 2)

# dev = Dev()

# if dev_flag and dev.dev_mode(e):
#     break
# (после кнопок)

# if dev_flag:
#     new_map = []
#     for dot in dots:
#         new_map.append((dot.land, dot.state, dot.object))
#     print(new_map)