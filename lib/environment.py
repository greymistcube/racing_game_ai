import pygame

import lib.constants as const
from lib.track import Track

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

class Environment:
    __grass_image = load_image("./rsc/img/grass_tile.png")

    def __init__(self):
        self.score = 0
        self.track = Track()
        self.start_grid = self.track.get_start_grid()
        self.cars = []
        self.num_alive = 0

    def add_cars(self, cars):
        self.cars += cars
        self.num_alive += len(cars)

    def update(self):
        for car in self.cars:
            car.update()
        self.score = max([car.score for car in self.cars])
        for car in self.cars[:]:
            if not car.alive:
                self.cars.remove(car)
                self.num_alive -= 1

    # should have a template surface to only add cars
    def get_surface(self):
        surface = pygame.Surface(const.RESOLUTION, pygame.SRCALPHA)
        for i in range(const.HEIGHT // const.TILE_SIZE):
            for j in range(const.WIDTH // const.TILE_SIZE):
                surface.blit(
                    self.__grass_image,
                    (j * const.TILE_SIZE, i * const.TILE_SIZE)
                )

        surface.blit(self.track.get_surface(), (0, 0))
        for car in self.cars:
            surface.blit(car.get_surface(), car.get_rect())
        return surface
