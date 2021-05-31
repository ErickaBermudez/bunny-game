from settings import *
import pygame
import random
from sprites import *
from os import path

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.2)
        self.BGCOLOR = LIGHTBLUE
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.load_data()

    def load_data(self):
        # cargar highscores 
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, HS_FILE), "r") as f:
            try: 
                self.highscore = int(f.read())
            except: 
                self.highscore = 0 
        
        self.jump_sound = pygame.mixer.Sound(path.join(SND_DIR, "jump.wav"))
        self.boost_sound = pygame.mixer.Sound(path.join(SND_DIR, "boost.wav"))
        self.jump_sound.set_volume(0.1)

        # cargar imagenes de nubes 
        self.cloud_images = []
        self.cloud_images.append(pg.image.load(CLOUD1).convert())
        self.cloud_images.append(pg.image.load(CLOUD2).convert())
        self.cloud_images.append(pg.image.load(CLOUD3).convert())

    def new(self):
        # Empezar el juego
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()

        self.player = Player(self)

        for platform in PLATFORM_LIST:
            Platform(self, *platform)

        self.mob_timer = 0
        pygame.mixer.music.load(path.join(SND_DIR, "pixelland.ogg")) 

        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500 

        self.run()

    def run(self):
        # Main loop
        pygame.mixer.music.play(loops=-1)
        self.playing =  True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(500)

    def events(self):
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_cut()    
            
    def update(self):
        # Actualizaciones en el loop
        self.all_sprites.update()

        # spawn un enemigo
        now = pg.time.get_ticks()
        if now - self.mob_timer > MOB_SPAWN_RATE + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        # checamos si el jugador colisiona con un mob
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False)
        if mob_hits:
            self.playing = False

        # revisamos si el jugador le pega a una plataforma en su caída
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.centery:
                        lowest = hit
                    if self.player.pos.x < lowest.rect.right + 10 and \
                        self.player.pos.x > lowest.rect.left - 10:
                        if self.player.pos.y < lowest.rect.bottom:
                            self.player.pos.y = hits[0].rect.top + 1
                            self.player.vel.y = 0
                            self.player.jumping = False

        # cuando el jugador llega a la parte más arriba
        # movemos todos los sprites hacia abajo
        if self.player.rect.top <= HEIGHT / 4: 
            if random.randrange(100) < 5: 
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud_scroll = random.randrange(1, 7)
                cloud.rect.y += max(abs(self.player.vel.y / cloud_scroll), 2)

            for platform in self.platforms: 
                platform.rect.y += abs(self.player.vel.y)
                if platform.rect.top >= HEIGHT: 
                    # eliminamos la plataforma que dejamos 
                    # para no saturar nuestro juego de plataformas
                    # que no podemos ver
                    platform.kill()

                    # añadimos esa plataforma a nuestro score
                    self.score += 1
            
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)

                    

        # añadimos continuamente nuevas plataformas
        while len(self.platforms) < 6: 
            width = random.randrange(50, 100)
            p = Platform(self, 
                random.randrange(0, WIDTH - width),
                random.randrange(-75, -30)
            )

        pow_hits = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == "boost":
                self.boost_sound.play()
                self.boost_sound.set_volume(0.05)
                self.player.vel.y = -BOOST_POWER
                self.player.jumping = False

        # el conejo se cae (rip)
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0: 
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False   

    def draw(self):
        # Game loop draw
        self.screen.fill(self.BGCOLOR)
        self.all_sprites.draw(self.screen)

        self.draw_text("Score: ", 22, FONT_TITLES, BLACK, WIDTH / 2 - 90, 15)
        self.draw_text(str(self.score), 22, FONT_TITLES, BLACK, WIDTH / 2 - 30, 15)

        pygame.display.flip()

    def show_start_screen(self):
        pygame.mixer.music.load(path.join(SND_DIR, "intro.wav"))
        pygame.mixer.music.play(loops=-1)
        self.screen.fill(self.BGCOLOR)
        self.draw_text("High Score: " + str(self.highscore), 16, FONT_TEXT, WHITE, WIDTH / 2, 15)
        self.draw_text(TITLE, 48, FONT_TITLES, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("UACH", 48, FONT_TITLES, WHITE, WIDTH / 2, HEIGHT / 4 + 48)
        self.draw_text("Usa <- -> para moverte y la barra de espacio para saltar", 14, FONT_TEXT, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Uriel / Abraham / Alex / Ericka", 14, FONT_TEXT, WHITE, WIDTH / 2, HEIGHT / 2 - 30)
        self.draw_text("Presiona una tecla para jugar", 22, FONT_TEXT, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(1000)

    def show_gameover_screen(self):
        pygame.mixer.music.load(path.join(SND_DIR, "intro.wav"))
        pygame.mixer.music.play(loops=-1)
        if not self.running: 
            return 
        self.screen.fill(self.BGCOLOR)
        self.draw_text("GAME OVER", 48, FONT_TITLES, WHITE, WIDTH/2, HEIGHT/4)
        self.draw_text("Puntuación: " + str(self.score), 30, FONT_TEXT, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Presiona una tecla para jugar de nuevo ", 22, FONT_TEXT, WHITE, WIDTH / 2, HEIGHT * 3 / 4)

        if self.score > self.highscore: 
            self.highscore = self.score
            with open(path.join(self.dir, HS_FILE), "w") as f:
                f.write(str(self.score))
            self.draw_text("NUEVO HIGHSCORE!", 20, FONT_TITLES, WHITE, WIDTH/2, HEIGHT / 2 + 40)
        else: 
            self.draw_text("Highscore: " + str(self.highscore), 20, FONT_TEXT, WHITE, WIDTH/2, HEIGHT / 2 + 40)

        pygame.display.flip()
        self.wait_for_key()
        pygame.mixer.music.fadeout(1000)
    
    def wait_for_key(self):
        # método para esperar hasta obtener una tecla de parte del usuario
        waiting = True
        while waiting: 
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    if self.playing:
                        self.playing = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, font_name, color, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

if __name__ == "__main__":
    game = Game()
    game.show_start_screen()
    while game.running: 
        game.new()
        game.show_gameover_screen()

pygame.quit()
