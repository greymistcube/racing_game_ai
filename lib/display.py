import pygame

import lib.common as common

# initializing module
pygame.init()

class Display:
    __instance = None

    # implementing this class as singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            raise Exception("only single instance is allowed")

    def __init__(self):
        self.screen = pygame.display.set_mode(
            common.settings.display_size
        )
        return

    def draw(self, surface):
        surface = pygame.transform.scale(surface, self.screen.get_size())
        self.screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        return
