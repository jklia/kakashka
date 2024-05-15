from fields import Fields

FPS = 0
delay = 2 # задержка между ходами в секундах

field = Fields.fields[3]  # 0 - стандартное поле, 1 - карта №1, 2 - пустое поле, 3 - карта №2
music_volume = 0.1
theme = 'Dark'  # 'Dark' — темная тема, 'Light' — светлая тема

dev_flag = False # режим разработчика (пока не работает)
digits_flag = True # отображение номера клетки (сейчас есть кнопка)
music_flag = True # включение музыки (сейчас есть кнопка)
bots_flag = True # работа ботов (сейчас есть кнопка)

# Не менять!
WIN_WIDTH = 574
WIN_HEIGHT = 780 # Без кнопок 730
X = 40
Y = 40
A = 30
MAP_WIDTH = 6
