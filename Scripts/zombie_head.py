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
        self.image = pygame.image.load('img/zombie_head.png').convert_alpha()  # Load image with transparency
        self.rect = self.image.get_rect()
        self.kill_audio = pygame.mixer.Sound('audio/punch.wav')
        self.rect.center = spawn_data.spawn_point()

        self.despawn_time = time.time() + 5  # The zombie despawns after 5 seconds

        # Tạo mask cho collision detection
        self.mask = pygame.mask.from_surface(self.image)

        # Tạo một rect nhỏ hơn cho collision (ví dụ: 60% kích thước gốc)
        smaller_size = (int(self.rect.width * 0.6), int(self.rect.height * 0.6))
        self.collision_rect = pygame.Rect(0, 0, *smaller_size)
        self.collision_rect.center = self.rect.center

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

    def update(self):
        """
        Update the zombie's state. This method should be called every frame.
        """
        self.collision_rect.center = self.rect.center
        self.despawn()

    def check_hit(self, pos):
        """
        Check if the given position hits the zombie.
        """
        offset_x = pos[0] - self.rect.x
        offset_y = pos[1] - self.rect.y
        if 0 <= offset_x < self.rect.width and 0 <= offset_y < self.rect.height:
            if self.mask.get_at((offset_x, offset_y)):
                return True

        return False