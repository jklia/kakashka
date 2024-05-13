import os
import pygame as pg
from config import theme

pg.init()

if theme == 'Dark':
    flag_red_image = pg.transform.scale(pg.image.load('../content/sprites_dark/flag_red.png'), (36, 36))
    flag_blue_image = pg.transform.scale(pg.image.load('../content/sprites_dark/flag_blue.png'), (36, 36))
    house_image = pg.transform.scale(pg.image.load('../content/sprites_dark/house.png'), (30, 30))
    tower_image = pg.transform.scale(pg.image.load('../content/sprites_dark/tower.png'), (43, 43))
    knight_image = pg.transform.scale(pg.image.load('../content/sprites_dark/knight.png'), (36, 37))
    peasant_image = pg.transform.scale(pg.image.load('../content/sprites_dark/peasant.png'), (36, 37))
    lord_image = pg.transform.scale(pg.image.load('../content/sprites_dark/lord.png'), (36, 37))
    tree_image = pg.transform.scale(pg.image.load('../content/sprites_dark/tree.png'), (36, 36))
    icon = pg.image.load('../content/sprites_dark/icon.png')
    background_image = pg.image.load('../content/sprites_dark/background.png')

    background_color = (15, 15, 30)
    main_color = (45, 46, 58)
    state_colors = [(114, 46, 48), (23, 59, 112)]

elif theme == 'Light':
    flag_red_image = pg.transform.scale(pg.image.load('../content/sprites_light/flag_red.png'), (36, 36))
    flag_blue_image = pg.transform.scale(pg.image.load('../content/sprites_light/flag_blue.png'), (36, 36))
    house_image = pg.transform.scale(pg.image.load('../content/sprites_light/house.png'), (30, 30))
    tower_image = pg.transform.scale(pg.image.load('../content/sprites_light/tower.png'), (43, 43))
    knight_image = pg.transform.scale(pg.image.load('../content/sprites_light/knight.png'), (36, 37))
    peasant_image = pg.transform.scale(pg.image.load('../content/sprites_light/peasant.png'), (36, 37))
    lord_image = pg.transform.scale(pg.image.load('../content/sprites_light/lord.png'), (36, 37))
    tree_image = pg.transform.scale(pg.image.load('../content/sprites_light/tree.png'), (36, 36))
    icon = pg.image.load('../content/sprites_light/icon.png')
    background_image = pg.image.load('../content/sprites_light/background.png')

    background_color = (15, 15, 30)
    main_color = (45, 46, 58)
    state_colors = [(131, 46, 46), (17, 62, 125)]

person_shadow_image = pg.transform.scale(pg.image.load('../content/sprites_dark/shadow.png'), (38, 48))
person_shadow_image.set_alpha(70)
house_shadow_image = pg.transform.scale(pg.image.load('../content/sprites_dark/shadow.png'), (60, 52))
house_shadow_image.set_alpha(70)
tower_shadow_image = pg.transform.scale(pg.image.load('../content/sprites_dark/shadow.png'), (59, 54))
tower_shadow_image.set_alpha(70)
tree_shadow_image = pg.transform.scale(pg.image.load('../content/sprites_dark/shadow.png'), (52, 52))
tree_shadow_image.set_alpha(70)
flag_shadow_image = pg.transform.scale(pg.image.load('../content/sprites_dark/shadow.png'), (16, 32))
flag_shadow_image.set_alpha(70)

pg.font.init()
f1 = pg.font.SysFont('arialblack', 18)

tracks = []
for track in os.listdir('../content//music'):
    tracks.append(f'../content/music/{track}')
