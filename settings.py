import pygame as pg
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
CLOUD1 = "imgs/cloud1.png"
CLOUD2 = "imgs/cloud2.png"
CLOUD3 = "imgs/cloud3.png"
BOOST = "imgs/boost.png"
MOB_DOWN = "imgs/mob_down.png"
MOB_UP = "imgs/mob_up.png"
# highscore saver
HS_FILE = "highscore.txt"

# Jugador
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = 20

# propiedades del juego
BOOST_POWER = 30
POWERUP_SPAWN_RATE = 7
MOB_SPAWN_RATE = 5000

# capas de los sprites
PLAYER_LAYER = 2 
MOB_LAYER = 2
POW_LAYER = 1 
PLATFORM_LAYER = 1
CLOUD_LAYER = 0


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