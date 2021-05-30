import pygame as pg
from random import choice

WIDTH = 360
HEIGHT = 600
FPS = 60
TITLE = "Bunny Game"
FONT_TITLES = "fonts/titles.ttf"
FONT_TEXT = "fonts/text.ttf"

# sprites 
BUNNY_NORMAL = "imgs/bunny_normal.png"
PAD_BIG = "imgs/pad.png"
PAD_MINI = "imgs/pad-mini.png"

# Jugador
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = 14

# plataformas para empezar
PLATFORM_LIST = [
    (0, HEIGHT - 40),
    (WIDTH / 2 - 50, HEIGHT * 3 / 4),
    (20, HEIGHT - 250),
    (190, 200),
    (180, 100)
]

# Tema
WHITE = (255, 255, 255)
BLACK = (52, 52, 52)
RED = (230, 150, 117)
GREEN = (204, 223, 134)
BLUE = (0, 0, 255)
YELLOW = (248, 229, 153)
LIGHTBLUE = (146, 191, 230)