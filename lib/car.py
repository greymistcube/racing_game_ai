import random

import pygame

import lib.constants as const
from lib.tools import Direction
from lib.grid import Grid

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

_axis_offset = lambda val: 1 if val > const.TILE_SIZE else -1 if val < 0 else 0
_grid_offset = lambda x, y: Grid(_axis_offset(x), _axis_offset(y))

# a car is only aware of the tile it is currently on
class Car():
    _image = load_image("./rsc/img/tiny_car.png")
    _images = {
        "blue": load_image("./rsc/img/blue_car.png"),
        "green": load_image("./rsc/img/green_car.png"),
        "yellow": load_image("./rsc/img/yellow_car.png"),
        "red": load_image("./rsc/img/red_car.png"),
    }

    def __init__(self, tile, color=None):
        self.rect = self._image.get_rect()
        if color is None:
            self.surface = random.choice(list(self._images.values()))
        else:
            self.surface = self._images[color]
        self.start_tile = tile
        self.tile = tile
        # initially starts at the middle of the starting tile
        self.rel_x = const.TILE_SIZE // 2
        self.rel_y = const.TILE_SIZE // 2

        self.speed = 0
        # requires a new instance since car's direction will change
        self.direction = Direction(self.tile.direction.degrees)
        self.velocity = self.direction.vector * self.speed
        self.laps = 0
        self.score = 0
        self.timer = const.TIMER
        self.alive = True
        return

    def update(self):
        self.timer -= 1
        self.rel_x += self.velocity[1]
        self.rel_y += self.velocity[0]
        self.check_crash()
        if self.alive:
            self.update_tile()

    # lazy implementation of collision
    # it's easier to crash the car if it doesn't land on
    # one of its immediate neighbor tiles
    # although this doesn't fully cover the diagonally crossing cases
    # those should be rather extreme edge cases
    # this only makes corner turning slightly more tighter
    def check_crash(self):
        grid_offset = _grid_offset(self.rel_x, self.rel_y)
        if self.timer < 0:
            self.alive = False
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
        if grid_offset != Grid(0, 0):
            self.score += self.timer // 2
            self.timer = const.TIMER
        if self.tile.grid + grid_offset == self.tile.next.grid:
            self.score += const.TILE_SCORE
            self.tile = self.tile.next
            if self.tile.grid == self.start_tile.grid:
                self.laps += 1
                self.score += const.LAP_BONUS
                if self.laps >= const.LAPS_PER_GAME:
                    self.alive = False
        elif self.tile.grid + grid_offset == self.tile.prev.grid:
            self.score -= const.TILE_SCORE
            self.tile = self.tile.prev
            # just kill off the car if it goes backwards
            self.alive = False
        self.rel_x += const.TILE_SIZE * (x_axis_offset * (-1))
        self.rel_y += const.TILE_SIZE * (y_axis_offset * (-1))
        return

    def handle_events(self, events):
        if events.acc and self.speed < const.SPD_LIMIT:
            self.speed += const.ACC_RATE
        if events.dec and self.speed > -const.SPD_LIMIT:
            self.speed -= const.ACC_RATE
        if events.stop:
            self.speed = 0
        if events.left:
            self.direction.rotate(const.TURN_SPD)
        if events.right:
            self.direction.rotate(-const.TURN_SPD)
        self.velocity = self.direction.vector * self.speed

    def get_surface(self):
        return pygame.transform.rotate(self.surface, self.direction.degrees)

    def get_rect(self):
        self.rect.center = (
            (self.tile.grid.x * const.TILE_SIZE) + self.rel_x,
            (self.tile.grid.y * const.TILE_SIZE) + self.rel_y,
        )
        return self.rect
