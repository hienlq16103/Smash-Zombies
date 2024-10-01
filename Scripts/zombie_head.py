import pygame
import time

class ZombieHead(pygame.sprite.Sprite):
    """
    A class to represent a zombie head in the game. It includes spawning, exploding, 
    and animation behavior, as well as hit detection.
    """
    
    def __init__(self, spawn_data):
        """
        Initializes the ZombieHead sprite, setting its image, position, and 
        preparing for animations and explosions.
        """
        super().__init__()
        self.original_image = pygame.image.load('img/zombie_head.png').convert_alpha()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.kill_audio = pygame.mixer.Sound('audio/punch.wav')
        self.rect.center = spawn_data.spawn_point()

        self.spawn_time = time.time()
        self.despawn_time = self.spawn_time + 5

        self.mask = pygame.mask.from_surface(self.image)

        smaller_size = (int(self.rect.width * 0.6), int(self.rect.height * 0.6))
        self.collision_rect = pygame.Rect(0, 0, *smaller_size)
        self.collision_rect.center = self.rect.center

        original_boom = pygame.image.load('img/boom.png').convert_alpha()
        self.boom_image = pygame.transform.scale(original_boom, self.rect.size)
        
        self.is_exploding = False
        self.explosion_start_time = 0
        self.explosion_duration = 0.5

        # Animation parameters
        self.animation_duration = 0.5
        self.current_scale = 0.1
        self.current_alpha = 0

    def despawn(self):
        """
        Despawns the zombie head by removing it from the sprite group
        after its despawn time has passed.
        """
        if time.time() > self.despawn_time:
            self.kill()

    def on_smashed(self):
        """
        Handles the event when the zombie head is smashed by playing the sound, 
        setting the exploding state, and changing the image to the explosion image.
        """
        self.kill_audio.play()
        self.is_exploding = True
        self.explosion_start_time = time.time()
        self.image = self.boom_image

    def update(self):
        """
        Updates the zombie head's state, handling animations and explosions. It manages the 
        scaling and transparency during the spawn and despawn animations, as well as the 
        explosion state.
        """
        current_time = time.time()
        
        if self.is_exploding:
            if current_time - self.explosion_start_time > self.explosion_duration:
                self.kill()
        else:
            # Spawn animation
            if current_time - self.spawn_time < self.animation_duration:
                progress = (current_time - self.spawn_time) / self.animation_duration
                self.current_scale = 0.1 + 0.9 * progress
                self.current_alpha = int(255 * progress)
            # Despawn animation
            elif self.despawn_time - current_time < self.animation_duration:
                progress = (self.despawn_time - current_time) / self.animation_duration
                self.current_scale = 0.1 + 0.9 * progress
                self.current_alpha = int(255 * progress)
            else:
                self.current_scale = 1
                self.current_alpha = 255

            scaled_size = (int(self.rect.width * self.current_scale), int(self.rect.height * self.current_scale))
            scaled_image = pygame.transform.scale(self.original_image, scaled_size)
            self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            self.image.blit(scaled_image, ((self.rect.width - scaled_size[0]) // 2, (self.rect.height - scaled_size[1]) // 2))
            self.image.set_alpha(self.current_alpha)

        self.collision_rect.center = self.rect.center

    def check_hit(self, pos):
        """
        Checks if the given position (typically the mouse position) hits the zombie head.
        A hit is only detected if the head is not exploding and is sufficiently visible.
        """
        if not self.is_exploding and self.current_alpha > 200:  # Only allow hits when mostly visible
            offset_x = pos[0] - self.rect.x
            offset_y = pos[1] - self.rect.y
            if 0 <= offset_x < self.rect.width and 0 <= offset_y < self.rect.height:
                if self.mask.get_at((offset_x, offset_y)):
                    return True
        return False