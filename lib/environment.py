import pygame

from lib.constants import RESOLUTION, GREEN
from lib.events import Events
from lib.tracks import Track
from lib.car import Car

pygame.init()

class Environment:
    def __init__(self):
        self.track = Track()
        self.start_grid = self.track.get_start_grid()
        self.cars = [Car(self.start_grid)]
        self.events = Events()
    
    def update(self):
        self.events.update()
        for car in self.cars:
            car.update(self.events)
    
    def get_surface(self):
        surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        surface.fill(GREEN)
        surface.blit(self.track.get_surface(), (0, 0))
        for car in self.cars:
            surface.blit(car.get_surface(), car.rect)
        return surface
