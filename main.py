import sys
import pygame
from pygame.locals import *
from Scripts.spawn_data import SpawnData
from Scripts.game_stats import GameStat
from Scripts.zombie_head import ZombieHead
import random
import time
import math

# Screen resolution
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768

# Hammer constants
HAMMER_ROTATION_SPEED = 720  # degrees per second
HAMMER_ROTATION_ANGLE = 45  # degrees
HAMMER_ROTATION_TIME = 0.1  # seconds

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
        self.__background = None
        self.all_sprites = pygame.sprite.Group()
        self.spawn_data = SpawnData()
        self.spawn_timer = time.time() + random.uniform(1, 3)
        self.__game_stat = GameStat()

        # Hammer attributes
        self.hammer_image = None
        self.hammer_rect = None
        self.hammer_rotation = 0
        self.hammer_rotating = False
        self.hammer_rotation_start_time = 0

    def on_init(self):
        """
        Init pygame and create gameplay window.
        """
        pygame.init()
        self.__displaying_surface = pygame.display.set_mode(self.size)
        
        # Load background image and resize it to fit the window
        self.__background = pygame.image.load('img/background.jpg').convert()
        self.__background = pygame.transform.scale(self.__background, (self.width, self.height))
        
        # Load hammer image
        self.hammer_image = pygame.image.load('img/hammer.png').convert_alpha()
        self.hammer_image = pygame.transform.scale(self.hammer_image, (64, 64))
        self.hammer_rect = self.hammer_image.get_rect()
        
        # Hide the default cursor
        pygame.mouse.set_visible(False)
        
        return self.__displaying_surface

    def spawn_zombie(self):
        """
        Spawn a new zombie at a random location.
        """
        zombie = ZombieHead(self.spawn_data)
        self.all_sprites.add(zombie)

    def rotate_hammer(self):
        if self.hammer_rotating:
            current_time = time.time()
            elapsed_time = current_time - self.hammer_rotation_start_time
            if elapsed_time < HAMMER_ROTATION_TIME:
                progress = elapsed_time / HAMMER_ROTATION_TIME
                self.hammer_rotation = HAMMER_ROTATION_ANGLE * math.sin(progress * math.pi)
            else:
                self.hammer_rotating = False
                self.hammer_rotation = 0

    def on_event(self, event):
        """
        Handle system event.

        :param event Event: Event to handle
        """
        if event.type == pygame.QUIT:
            self.__is_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.hammer_rotating = True
            self.hammer_rotation_start_time = time.time()
            for sprite in self.all_sprites:
                if isinstance(sprite, ZombieHead) and sprite.check_hit(event.pos):
                    sprite.on_smashed()
                    self.__game_stat.update_score(hit=True)
                else:
                    self.__game_stat.update_score(hit=False)

    def on_loop(self):
        """
        Updating the game world each frame.
        """
        if time.time() > self.spawn_timer:
            self.spawn_zombie()
            self.spawn_timer = time.time() + random.uniform(1, 3)  # Reset spawn timer
        for sprite in self.all_sprites:
            sprite.update()  # Call update method for each sprite
        self.all_sprites.update()
        self.rotate_hammer()

    def on_render(self):
        """
        Rendering the game each frame.
        """
        self.__displaying_surface.blit(self.__background, (0, 0))
        self.all_sprites.draw(self.__displaying_surface)
        
        # Draw hammer cursor
        mouse_pos = pygame.mouse.get_pos()
        rotated_hammer = pygame.transform.rotate(self.hammer_image, self.hammer_rotation)
        hammer_rect = rotated_hammer.get_rect(center=mouse_pos)
        self.__displaying_surface.blit(rotated_hammer, hammer_rect)
        
        # Display score on screen
        self.__game_stat.display_stat(self.__displaying_surface)

        # Update the display
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