import pygame
from lib.shared.settings import Settings

pygame.init()
settings = Settings()

class Clock:
    def __init__(self):
        self.clock = pygame.time.Clock()
        return

    def tick(self):
        self.clock.tick(settings.tickrate)
        return
