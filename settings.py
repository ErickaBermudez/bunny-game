import pygame as pg
from random import choice
from os import path

WIDTH = 360
HEIGHT = 600
FPS = 60
TITLE = "Bunny Game"
FONT_TITLES = "fonts/titles.ttf"
FONT_TEXT = "fonts/text.ttf"

# sprites 
BUNNY_NORMAL = "imgs/bunny_normal.png"
BUNNY_LEFT = "imgs/bunny_left.png"
BUNNY_JUMP = "imgs/bunny_jump_left.png"
PAD_BIG = "imgs/pad.png"
PAD_MINI = "imgs/pad-mini.png"

# highscore saver
HS_FILE = "highscore.txt"

# Jugador
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = 20

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

# Directorio de archivos
MAIN_DIR = path.dirname(__file__)
SND_DIR = path.join(MAIN_DIR, "sounds")