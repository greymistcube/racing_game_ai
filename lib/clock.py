import pygame

import lib.common as common

# initializing module
pygame.init()

class Clock:
    __instance = None

    # implementing this class as singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            raise Exception("only single instance is allowed")

    def __init__(self):
        self.clock = pygame.time.Clock()
        return

    def tick(self):
        self.clock.tick(common.settings.tickrate)
        return

    def get_FPS(self):
        return 1000 // self.clock.get_time()
