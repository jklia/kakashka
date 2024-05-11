# class Dev:
#     def __init(self, pg, dots):
#         self.pg = pg
#         self.dots = dots
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
#
