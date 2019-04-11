import pygame

from lib.tracks import Track
from lib.car import Car

pygame.init()

class Environment:
    def __init__(self):
        self.track = Track()
        self.car = Car()
    
    def get_surface(self):
        return self.track.get_surface()
