import pygame
import random

WIDTH = 360
HEIGHT = 600
FPS = 60
TITLE = "Bunny Game"
FONT_TITLES = "fonts/titles.ttf"
FONT_TEXT = "fonts/text.ttf"

# Jugador
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.5
PLAYER_JUMP = 14

# plataformas para empezar
PLATFORM_LIST = [
    (0, HEIGHT - 40, WIDTH, 40),
    (WIDTH / 2 - 50, HEIGHT * 3 / 4, 100, 20),
    (20, HEIGHT - 250, 100, 20),
    (190, 200, 100, 20),
    (180, 100, 50, 20)
]

# Tema
WHITE = (255, 255, 255)
BLACK = (52, 52, 52)
RED = (230, 150, 117)
GREEN = (204, 223, 134)
BLUE = (0, 0, 255)
YELLOW = (248, 229, 153)
LIGHTBLUE = (146, 191, 230)