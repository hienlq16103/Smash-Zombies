import sys
import pygame
from pygame.locals import *
from Scripts.spawn_data import SpawnData
import random
import time 
# Screen resolution
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400

class ZombieHead(pygame.sprite.Sprite):
    def __init__(self, spawn_data):
        super().__init__()
        self.image = pygame.image.load('img/zombie_head.png')
        self.rect = self.image.get_rect()
        self.kill_audio = pygame.mixer.Sound('audio/punch.wav')

        self.rect.topleft = spawn_data.spawn_point()
        self.despawn_time = time.time() + 1  # The zombie despawns after 5 seconds

    def spawn(self):
        pass

    def despawn(self):
        if time.time() > self.despawn_time:
            self.kill()

    def on_smashed(self):
        self.kill_audio.play()
        self.kill()  


class App:
    """
    Handle execution of the game loop.
    """

    def __init__(self):
        self.__is_running = True
        self.__displaying_surface = None
        self.size = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.background = None
        self.all_sprites = pygame.sprite.Group()
        self.spawn_data = SpawnData()

    def on_init(self):
        pygame.init()
        self.__displaying_surface = pygame.display.set_mode(self.size)
        self.background = pygame.image.load('img/background.jpg')
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        pygame.mixer.init()

        # Create and spawn a zombie head
        self.spawn_zombie()

        return self.__displaying_surface

    def spawn_zombie(self):
        zombie = ZombieHead(self.spawn_data)
        self.all_sprites.add(zombie)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.__is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in self.all_sprites:
                if sprite.rect.collidepoint(event.pos):
                    sprite.on_smashed()

    def on_loop(self):
        for sprite in self.all_sprites:
            sprite.despawn()  # Check if zombies need to despawn
        self.all_sprites.update()

    def on_render(self):
        self.__displaying_surface.blit(self.background, (0, 0))
        self.all_sprites.draw(self.__displaying_surface)
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()
        sys.exit()

    def on_execute(self):
        if self.on_init() is None:
            self.__is_running = False

        while self.__is_running:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    the_app = App()
    the_app.on_execute()
