import pygame
import numpy as np

from lib.constants import TILE_SIZE
from lib.grid import Grid

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

_axis_offset = lambda val: 1 if val > TILE_SIZE else -1 if val < 0 else 0
_grid_offset = lambda x, y: Grid(_axis_offset(x), _axis_offset(y))

# a car is only aware of the tile it is currently on
class Car():
    __image = load_image("./rsc/img/tiny_car.png")

    def __init__(self, tile):
        self.rect = self.__image.get_rect()
        self.tile = tile
        self.rel_x = TILE_SIZE // 2
        self.rel_y = TILE_SIZE // 2
        self.speed = 0
        self.velocity = (0, 0)
        self.degree = 0
        self.score = 0
        self.alive = True
        return

    def update(self):
        self.rel_x += self.velocity[1]
        self.rel_y += self.velocity[0]
        self.check_crash()
        if self.alive:
            self.update_tile()
            # debug logging
            print("{} {}".format(self.tile.grid, self.tile.direction))

    # lazy implementation of collision
    # it's easier to crash the car if it doesn't land on
    # one of its immediate neighbor tiles
    # although this doesn't fully cover the diagonally crossing cases
    # those should be rather extreme edge cases
    # this only makes corner turning slightly more tighter
    def check_crash(self):
        grid_offset = _grid_offset(self.rel_x, self.rel_y)
        if self.tile.grid + grid_offset not in [
                self.tile.prev.grid,
                self.tile.grid,
                self.tile.next.grid,
            ]:
            self.alive = False
        return

    def update_tile(self):
        x_axis_offset = _axis_offset(self.rel_x)
        y_axis_offset = _axis_offset(self.rel_y)
        grid_offset = _grid_offset(self.rel_x, self.rel_y)
        if self.tile.grid + grid_offset == self.tile.next.grid:
            self.score += 1
            self.tile = self.tile.next
        elif self.tile.grid + grid_offset == self.tile.prev.grid:
            self.score -= 1
            self.tile = self.tile.prev
        self.rel_x += TILE_SIZE * (x_axis_offset * (-1))
        self.rel_y += TILE_SIZE * (y_axis_offset * (-1))
        return

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
            (self.tile.grid.x * TILE_SIZE) + self.rel_x,
            (self.tile.grid.y * TILE_SIZE) + self.rel_y,
        )
        return self.rect
