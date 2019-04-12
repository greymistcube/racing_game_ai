import pygame

from lib.constants import RESOLUTION, GREEN
from lib.events import Events
from lib.track import Track
from lib.car import Car

pygame.init()

class Environment:
    def __init__(self):
        self.track = Track()
        self.start_grid = self.track.get_start_grid()
        self.cars = []

    def add_cars(self, cars):
        self.cars += cars

    def update(self, events):
        pass

    def get_surface(self):
        surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        surface.fill(GREEN)
        surface.blit(self.track.get_surface(), (0, 0))
        for car in self.cars:
            surface.blit(car.get_surface(), car.rect)
        return surface
