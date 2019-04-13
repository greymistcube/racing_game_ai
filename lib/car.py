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

    def __init__(self, tile):
        self.rect = self.__image.get_rect()
        self.tile = tile
        self.grid = tile.grid
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
            self.update_grid()
            print("{} {}".format(self.tile.grid, self.grid))

    # lazy implementation of collision for now
    # currently, only checks if the center crashed into a wall
    def check_crash(self):
        if self.rel_x > TILE_SIZE and self.tile.walls.E:
            self.alive = False
        elif self.rel_x < 0 and self.tile.walls.W:
            self.alive = False
        elif self.rel_y > TILE_SIZE and self.tile.walls.S:
            self.alive = False
        elif self.rel_y < 0 and self.tile.walls.N:
            self.alive = False
        return

    def update_tile(self):
        if self.rel_x > TILE_SIZE:
            if self.grid.E == self.tile.next.grid:
                self.tile = self.tile.next
                self.score += 1
            else:
                self.tile = self.tile.prev
                self.score -= 1
        elif self.rel_x < 0:
            if self.grid.W == self.tile.next.grid:
                self.tile = self.tile.next
                self.score += 1
            else:
                self.tile = self.tile.prev
                self.score -= 1
        elif self.rel_y > TILE_SIZE:
            if self.grid.S == self.tile.next.grid:
                self.tile = self.tile.next
                self.score += 1
            else:
                self.tile = self.tile.prev
                self.score -= 1
        elif self.rel_y < 0:
            if self.grid.N == self.tile.next.grid:
                self.tile = self.tile.next
                self.score += 1
            else:
                self.tile = self.tile.prev
                self.score -= 1

    def update_grid(self):
        if self.rel_x > TILE_SIZE:
            self.grid = self.grid.E
            self.rel_x -= TILE_SIZE
        elif self.rel_x < 0:
            self.grid = self.grid.W
            self.rel_x += TILE_SIZE
        elif self.rel_y > TILE_SIZE:
            self.grid = self.grid.S
            self.rel_y -= TILE_SIZE
        elif self.rel_y < 0:
            self.grid = self.grid.N
            self.rel_y += TILE_SIZE
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
            (self.grid.x * TILE_SIZE) + self.rel_x,
            (self.grid.y * TILE_SIZE) + self.rel_y,
        )
        return self.rect
