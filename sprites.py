import pygame as pg
from settings import *
from random import choice, randrange
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
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
        
        self.mask = pg.mask.from_surface(self.image)


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
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        pad_mini = pg.image.load(PAD_BIG).convert()
        pad_mini = pg.transform.scale(pad_mini, (70, 50))
        pad_big = pg.image.load(PAD_BIG).convert()
        pad_big = pg.transform.scale(pad_mini, (200, 60))
        self.images = [pad_big, pad_mini]
        self.image = choice(self.images)
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POWERUP_SPAWN_RATE:
            Powerup(self.game, self)

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, platform):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.platform = platform
        self.type = "boost"
        self.image = pg.image.load(BOOST).convert()
        self.image = pg.transform.scale(self.image, (40, 50))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.platform.rect.centerx
        self.rect.bottom = self.platform.rect.top - 5
    
    def update(self):
        self.rect.bottom = self.platform.rect.top - 5
        if not self.game.platforms.has(self.platform):
            self.kill()

class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = pg.image.load(MOB_UP).convert()
        self.image_up = pg.transform.scale(self.image_up, (70, 70))
        self.image_up.set_colorkey((255, 255, 255))
        self.image_down = pg.image.load(MOB_DOWN).convert()
        self.image_down = pg.transform.scale(self.image_down, (70, 70))
        self.image_down.set_colorkey((255, 255, 255))
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])

        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= 1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5
    
    def update(self):
        # movimiento en x
        self.rect.x += self.vx
        # movimiento en y
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy

        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        scale = randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale), int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH + 2 - self.rect.width)
        self.rect.y = randrange(-500, -50)
    
    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()
