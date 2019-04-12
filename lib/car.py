import pygame
import numpy as np
import lib
from lib.constants import TILE_WIDTH, TILE_HEIGHT

ACC_RATE = 0.2
SPD_LIMIT = 2
TURN_SPD = 4.5

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

_R = lambda theta: np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta), np.cos(theta)],
])

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
        self.velocity = (0, 0)
        self.degree = 0
        return

    def update(self, events):
        if events.acc and self.speed < SPD_LIMIT:
            self.speed += ACC_RATE
        if events.dec and self.speed > -SPD_LIMIT:
            self.speed -= ACC_RATE
        if events.left:
            self.degree += TURN_SPD
        if events.right:
            self.degree -= TURN_SPD
        self.degree = self.degree % 360
        self.velocity = self.get_velocity()

        self.x += self.velocity[1]
        self.y += self.velocity[0]
        self.rect.center = (self.x, self.y)

    def get_velocity(self):
        return np.matmul(_R(np.radians(self.degree)), (0, 1)) * self.speed

    def get_surface(self):
        return pygame.transform.rotate(self.__image, self.degree)
