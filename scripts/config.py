from fields import Fields
from random import randint

FPS = 0
delay = 2  # Задержка между ходами в секундах

field = Fields.fields[randint(0, 4)]  # 0 - Стандартное поле, 1 - карта №1, 2 - пустое поле, 3 - карта №2
# field = Fields.fields[2]

music_volume = 0.1
theme = 'Dark'  # 'Dark' — темная тема, 'Light' — светлая тема

dev_flag = False  # Режим разработчика (пока не работает)
digits_flag = False  # Отображение номера клетки (сейчас есть кнопка)
music_flag = False  # Включение музыки (сейчас есть кнопка)
pause_flag = True  # Работа ботов (сейчас есть кнопка)
stress_test_flag = False  # Стресс-тест игры
logs_flag = False  # Логи в консоль
color_cor_flag = True  # Цветокоррекция

# Не менять!
WIN_WIDTH = 574
WIN_HEIGHT = 780  # Без кнопок 730
X = 40
Y = 40
A = 30
MAP_WIDTH = 6
