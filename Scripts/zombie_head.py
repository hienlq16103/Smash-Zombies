import pygame
import time

class ZombieHead(pygame.sprite.Sprite):
    """
    The ZombieHead class represents a zombie object in the game.
    It can be spawned, smashed by the player, and automatically despawned after a set amount of time.
    """

    def __init__(self, spawn_data):
        """
        Initialize the ZombieHead with its image, sound, and spawn location.
        """
        super().__init__()
        self.image = pygame.image.load('img/zombie_head.png')  # Optimized for performance with convert()
        self.rect = self.image.get_rect()
        self.kill_audio = pygame.mixer.Sound('audio/punch.wav')
        self.rect.topleft = spawn_data.spawn_point()  # Set spawn location
        self.despawn_time = time.time() + 5  # The zombie despawns after 5 seconds

    def despawn(self):
        """
        Check if it's time to despawn the zombie and remove it from the game.
        """
        if time.time() > self.despawn_time:
            self.kill()

    def on_smashed(self):
        """
        Handle the event when the zombie is smashed by the player.
        Play the smash sound and remove the zombie from the game.
        """
        self.kill_audio.play()
        self.kill()
