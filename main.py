import pygame as pg
from fields import Fields
from pygame import gfxdraw




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
                    break_flag = True
        if e.button == 2:
            xm, ym = e.pos
            for dot in dots:
                if dot.inside(xm, ym):
                    dot.state = 0
                    break_flag = True
        if e.button == 3:
            xm, ym = e.pos
            for dot in dots:
                if dot.inside(xm, ym):
                    dot.state = 2
                    break_flag = True

    elif e.type == pg.KEYDOWN:
        if e.key == pg.K_g:
            xm, ym = pg.mouse.get_pos()
            change_land(xm, ym)
            break_flag = True
        elif e.key == pg.K_f:
            xm, ym = pg.mouse.get_pos()
            break_flag = True
        elif e.key == pg.K_h:
            xm, ym = pg.mouse.get_pos()
            break_flag = True
        elif e.key == pg.K_j:
            xm, ym = pg.mouse.get_pos()
            break_flag = True
    return break_flag




def change_land(xm, ym):
    for dot in dots:
        if dot.inside(xm, ym):
            if dot.land == 1:
                dot.land = 0
            else:
                dot.land = 1


    for dot in dots:
        if dot.inside(xm, ym):
                dot.object = ''
            else:
                dot.object = object






class GameSprite(pg.sprite.Sprite):

        self.colors = colors
        self.state = state
        self.land = land
        self.x = x
        self.y = y
        self.object = object
        self.rect = pg.Rect(self.point3[0], self.point5[1], 30, 60)
        if self.land == 0:
            self.color = background_color
        else:
            if self.state == 0:
                self.color = main_color
            else:
                self.color = self.colors[self.state - 1]

    def reset(self):
                                   self.color)

        if self.object == 'flag':
            if self.state == 1:
            elif self.state == 2:
        elif self.object == 'house':

    def inside(self, x, y):
        return self.rect.collidepoint(x, y)

            if self.land == 0:
                self.object = ''
                self.state = 0
                self.color = background_color
            else:
                if self.state == 0:
                    self.color = main_color
                elif self.state != 0:
                    self.color = self.colors[self.state - 1]


pg.display.set_caption("Antiyoy")

dots = []
for i in range(156):
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
