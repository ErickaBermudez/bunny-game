import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((30, 40))
        #self.image.fill(YELLOW)
        self.walking = False
        self.jumping = False
        self.current_frame = 0 
        self.last_update = 0
        self.load_images()
        self.image = pg.image.load(BUNNY_NORMAL).convert()
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self): 
        # idle
        self.idle_frame = pg.image.load(BUNNY_NORMAL).convert()
        self.idle_frame.set_colorkey((0, 0, 0))

        self.walking_frame_left = pg.image.load(BUNNY_LEFT).convert()
        self.walking_frame_left.set_colorkey((0, 0, 0))

        self.walking_frame_right = pg.transform.flip(self.walking_frame_left, True, False)
        self.walking_frame_left.set_colorkey((0, 0, 0))

        self.jumping_frame = pg.image.load(BUNNY_JUMP).convert()
        self.jumping_frame.set_colorkey((0, 0, 0))

    def update(self):
        self.animate()

        self.acc = vec(0, PLAYER_GRAVITY)
        keys = pg.key.get_pressed()

        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # Friccion
        self.acc.x += self.vel.x * PLAYER_FRICTION

        # Motion
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc

        # Lados de la pantalla
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos
    
    def animate(self):
        now = pg.time.get_ticks()

        if self.vel.x != 0: 
            self.walking = True
        else:
            self.walking = False

        if not self.walking: 
            self.current_frame = 1
            self.image = self.idle_frame;
        
        if self.walking: 
            if self.vel.x > 0: 
                self.current_frame = 2
                self.image = self.walking_frame_right
            else: 
                self.current_frame = 3
                self.image = self.walking_frame_left
        
        # for jumping
        if self.vel.y != 0:
            self.current_frame = 4
            self.image = self.jumping_frame

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -PLAYER_JUMP

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.images = [pg.image.load(PAD_BIG).convert(), pg.image.load(PAD_MINI).convert()]
        self.image = choice(self.images)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y