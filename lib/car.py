import pygame
import numpy as np
import lib
from lib.constants import TILE_WIDTH, TILE_HEIGHT

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

class Car():
    __image = load_image("./rsc/img/tiny_car.png")

    def __init__(self, grid):
        self.rect = self.__image.get_rect()
        self.grid_x = grid[0]
        self.grid_y = grid[1]
        self.x = (self.grid_x * TILE_WIDTH) + (TILE_WIDTH // 2)
        self.y = (self.grid_y * TILE_HEIGHT) + (TILE_HEIGHT // 2)
        self.rect.center = (self.x, self.y)
        self.speed = 0
        return
    
    def update(self, events):
        if events.acc:
            self.speed += 0.2
        if events.dec:
            self.speed -= 0.2
        self.x += self.speed
        self.rect.center = (self.x, self.y)

    def get_surface(self):
        return self.__image
