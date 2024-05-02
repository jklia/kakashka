import pygame as pg
import os
pg.init()

flag_red_image = pg.transform.scale(pg.image.load('sprites/flag_red.png'), (36, 36))
flag_blue_image = pg.transform.scale(pg.image.load('sprites/flag_blue.png'), (36, 36))
house_image = pg.transform.scale(pg.image.load('sprites/house.png'), (30, 30))
tower_image = pg.transform.scale(pg.image.load('sprites/tower.png'), (44, 44))
knight_image = pg.transform.scale(pg.image.load('sprites/knight.png'), (36, 37))
peasant_image = pg.transform.scale(pg.image.load('sprites/peasant.png'), (36, 37))
lord_image = pg.transform.scale(pg.image.load('sprites/lord.png'), (36, 37))
tree_image = pg.transform.scale(pg.image.load('sprites/tree.png'), (36, 36))
icon = pg.image.load('sprites/icon.png')
background_image = pg.image.load('sprites/background.png')

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

background_color = (30, 30, 45)
main_color = (45, 46, 58)
state_colors = [(131, 46, 46), (17, 62, 125)]

pg.font.init()
f1 = pg.font.SysFont('arialblack', 18)

tracks = []
for track in os.listdir('music'):
    tracks.append(f'music/{track}')
