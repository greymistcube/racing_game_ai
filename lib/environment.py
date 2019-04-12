import pygame

from lib.constants import RESOLUTION, GREEN
from lib.tracks import Track
from lib.car import Car

pygame.init()

class Environment:
    def __init__(self):
        self.track = Track()
        self.start_grid = self.track.get_start_grid()
        self.car = Car(self.start_grid)
#        self.start_pos = self.track.get_start_pos()
    
    def get_surface(self):
        surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        surface.fill(GREEN)
        surface.blit(self.track.get_surface(), (0, 0))
        surface.blit(self.car.get_surface(), self.car.rect)
        return surface
