from settings import BLACK, FPS, HEIGHT, TITLE, WIDTH
import pygame
import random

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        pass

    def new(self):
        # Empezar el juego
        self.all_sprites = pygame.sprite.Group()
        self.run()
        pass

    def run(self):
        # Main loop
        self.playing =  True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pass

    def events(self):
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
        pass

    def update(self):
        # Actualizaciones en el loop
        self.all_sprites.update()
        pass

    def draw(self):
        # Game loop draw
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        pygame.display.flip()
        pass

    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass


if __name__ == "__main__":
    game = Game()
    game.show_start_screen()
    while game.running: 
        game.new()
        game.show_gameover_screen()

pygame.quit()
