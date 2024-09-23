import sys
import pygame
from pygame.locals import *
from Scripts.spawn_data import SpawnData

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

    def on_init(self):
        """
        Init pygame and create gameplay window.
        """
        pygame.init()
        self.__displaying_surface = pygame.display.set_mode(self.size)
        
        # Tải hình nền và thay đổi kích thước cho vừa cửa sổ
        self.background = pygame.image.load('img/background.jpg').convert()
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        
        return self.__displaying_surface

    def on_event(self, event):
        """
        Handle system event.

        :param event Event: Event to handle
        """
        if event.type == pygame.QUIT:
            self.__is_running = False

    def on_loop(self):
        """
        Updating the game world each frame.
        """
        pass

    def on_render(self):
        """
        Rendering the game each frame.
        """
        # Vẽ hình nền lên màn hình
        self.__displaying_surface.blit(self.background, (0, 0))

        # Cập nhật màn hình
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
