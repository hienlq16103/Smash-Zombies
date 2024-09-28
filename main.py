import sys
import pygame
from pygame.locals import *
from Scripts.spawn_data import SpawnData
from Scripts.zombie_head import ZombieHead  # Import ZombieHead class from a separate file
import random
import time

# Screen resolution
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 400


class App:
    """
    Handle execution of the game loop.
    """

    def __init__(self):
        """
        Construct the app.
        """
        self.__is_running = True
        self.__displaying_surface = None
        self.size = self.width, self.height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.background = None
        self.all_sprites = pygame.sprite.Group()
        self.spawn_data = SpawnData()
        self.spawn_timer = time.time() + random.uniform(1, 3)  # Random time interval for spawning zombies

    def on_init(self):
        """
        Init pygame and create gameplay window.
        """
        pygame.init()
        self.__displaying_surface = pygame.display.set_mode(self.size)
        self.background = pygame.image.load('img/background.jpg').convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        pygame.mixer.init()

        return self.__displaying_surface

    def spawn_zombie(self):
        """
        Spawn a new zombie at a random location.
        """
        zombie = ZombieHead(self.spawn_data)
        self.all_sprites.add(zombie)

    def on_event(self, event):
        """
        Handle system event.

        :param event Event: Event to handle
        """
        if event.type == pygame.QUIT:
            self.__is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for sprite in self.all_sprites:
                if sprite.rect.collidepoint(event.pos):
                    sprite.on_smashed()

    def on_loop(self):
        """
        Updating the game world each frame.
        """
        # Check if it's time to spawn a new zombie
        if time.time() > self.spawn_timer:
            self.spawn_zombie()
            self.spawn_timer = time.time() + random.uniform(1, 3)  # Reset spawn timer

        for sprite in self.all_sprites:
            sprite.despawn()  # Check and despawn zombies

        self.all_sprites.update()

    def on_render(self):
        """
        Rendering the game each frame.
        """
        self.__displaying_surface.blit(self.background, (0, 0))
        self.all_sprites.draw(self.__displaying_surface)
        pygame.display.flip()

    def on_cleanup(self):
        """
        Clean up the app after being closed.
        """
        pygame.quit()
        sys.exit()

    def on_execute(self):
        """
        Handle the gameplay loop.
        """
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
