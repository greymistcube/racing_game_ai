import pygame

from lib.constants import RESOLUTION, WIDTH, HEIGHT, TILE_SIZE
from lib.track import Track

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

class Environment:
    __grass_image = load_image("./rsc/img/grass_tile.png")

    def __init__(self):
        self.track = Track()
        self.start_grid = self.track.get_start_grid()
        self.cars = []

    def add_cars(self, cars):
        self.cars += cars

    def update(self, events):
        for car in self.cars:
            car.update()

    # should have a template surface to only add cars
    def get_surface(self):
        surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        for i in range(HEIGHT // TILE_SIZE):
            for j in range(WIDTH // TILE_SIZE):
                surface.blit(self.__grass_image, (j * TILE_SIZE, i * TILE_SIZE))

        surface.blit(self.track.get_surface(), (0, 0))
        for car in self.cars:
            surface.blit(car.get_surface(), car.rect)
        return surface
