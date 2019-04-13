import pygame
import numpy as np
import lib
from lib.constants import TILE_SIZE

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
        self.grid = grid
        self.rel_x = TILE_SIZE // 2
        self.rel_y = TILE_SIZE // 2
        self.speed = 0
        self.velocity = (0, 0)
        self.degree = 0
        return

    def update(self):
        self.rel_x += self.velocity[1]
        self.rel_y += self.velocity[0]
        self.update_grid()

    def update_grid(self):
        if self.rel_x > TILE_SIZE:
            self.grid.x += 1
            self.rel_x -= TILE_SIZE
        if self.rel_x < 0:
            self.grid.x -= 1
            self.rel_x += TILE_SIZE
        if self.rel_y > TILE_SIZE:
            self.grid.y += 1
            self.rel_y -= TILE_SIZE
        if self.rel_y < 0:
            self.grid.y -= 1
            self.rel_y += TILE_SIZE

    def handle_events(self, events):
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

    def get_velocity(self):
        return np.matmul(_R(np.radians(self.degree)), (0, 1)) * self.speed

    def get_surface(self):
        return pygame.transform.rotate(self.__image, self.degree)

    def get_rect(self):
        self.rect.center = (
            (self.grid.x * TILE_SIZE) + self.rel_x,
            (self.grid.y * TILE_SIZE) + self.rel_y,
        )
        return self.rect
