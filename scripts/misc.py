from scripts.fields import *
import os
import copy
from random import sample, choice, randint
from time import time

import pygame as pg
import pygame_gui
from pygame import gfxdraw


pg.init()

flag_red_image = pg.transform.scale(pg.image.load('../content/sprites/flag_red.png'), (36, 36))
flag_blue_image = pg.transform.scale(pg.image.load('../content/sprites/flag_blue.png'), (36, 36))
house_image = pg.transform.scale(pg.image.load('../content/sprites/house.png'), (30, 30))
tower_image = pg.transform.scale(pg.image.load('../content/sprites/tower.png'), (43, 43))
knight_image = pg.transform.scale(pg.image.load('../content/sprites/knight.png'), (36, 37))
peasant_image = pg.transform.scale(pg.image.load('../content/sprites/peasant.png'), (36, 37))
lord_image = pg.transform.scale(pg.image.load('../content/sprites/lord.png'), (36, 37))
tree_image = pg.transform.scale(pg.image.load('../content/sprites/tree.png'), (36, 36))
icon = pg.image.load('../content/sprites/icon.png')
background_image = pg.image.load('../content/sprites/background.png')

person_shadow_image = pg.transform.scale(pg.image.load('../content/sprites/shadow.png'), (38, 48))
person_shadow_image.set_alpha(70)
house_shadow_image = pg.transform.scale(pg.image.load('../content/sprites/shadow.png'), (60, 52))
house_shadow_image.set_alpha(70)
tower_shadow_image = pg.transform.scale(pg.image.load('../content/sprites/shadow.png'), (59, 54))
tower_shadow_image.set_alpha(70)
tree_shadow_image = pg.transform.scale(pg.image.load('../content/sprites/shadow.png'), (52, 52))
tree_shadow_image.set_alpha(70)
flag_shadow_image = pg.transform.scale(pg.image.load('../content/sprites/shadow.png'), (16, 32))
flag_shadow_image.set_alpha(70)

background_color = (15, 15, 30)
main_color = (45, 46, 58)
state_colors = [(131, 46, 46), (17, 62, 125)]

pg.font.init()
f1 = pg.font.SysFont('arialblack', 18)

tracks = []
for track in os.listdir('../content//music'):
    tracks.append(f'../content/music/{track}')
