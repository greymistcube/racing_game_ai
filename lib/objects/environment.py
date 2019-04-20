import pygame

import lib.constants as const
from lib.objects.track import Track

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

class Environment:
    _grass_image = load_image("./rsc/img/grass_tile.png")

    def __init__(self):
        self.score = 0
        self.track = Track()
        self.cars = []
        self.crashed_cars = []
        self.num_alive = 0
        self.background = self.set_background()

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
                self.crashed_cars.append(car)
                self.num_alive -= 1

    def game_over(self):
        return self.num_alive == 0

    def set_background(self):
        surface = pygame.Surface(const.RESOLUTION, pygame.SRCALPHA)
        for i in range(const.HEIGHT // const.TILE_SIZE):
            for j in range(const.WIDTH // const.TILE_SIZE):
                surface.blit(
                    self._grass_image,
                    (j * const.TILE_SIZE, i * const.TILE_SIZE)
                )

        surface.blit(self.track.get_surface(), (0, 0))
        return surface

    # should have a template surface to only add cars
    def get_surface(self):
        surface = pygame.Surface(const.RESOLUTION, pygame.SRCALPHA)
        surface.blit(self.background, (0, 0))
        for car in self.cars:
            surface.blit(car.get_surface(), car.get_rect())
        for car in self.crashed_cars[:]:
            surface.blit(car.get_surface(), car.get_rect())
            if car.crashed_timer < 0:
                self.crashed_cars.remove(car)
        return surface
