import random

import numpy as np
import pygame

import neat
import lib

import lib.constants as const
from lib.settings import Settings
from lib.grid import Directions

pygame.init()
settings = Settings()

def load_image(file):
    image = pygame.image.load(file)
    return image

# game specific neat interface
# this straps on to the original Core class
# by inheriting it and overriding necessary methods
# and adding extensions
class NeatCore(lib.Core):
    # game specific variables
    _num_input = 4
    _num_output = 4

    # overriden methods
    def __init__(self):
        super().__init__()
        self.population = neat.Population(
            self._num_input,
            self._num_output,
            pop_size=settings.num_cars
        )
        return

    def new_cars(self):
        return [SmartCar(self.env.track.start_tile, genome) for genome in self.population.genomes]

    def update(self):
        self.events.update()
        settings.update(self.events)
        # only cycle through balls alive in the environment for optimization
        for car in self.env.cars:
            car.think(self.get_x(car))
        self.env.update()

    def game_over(self):
        if self.env.game_over():
            scores = [car.score for car in self.cars]
            self.population.score_genomes(scores)
            self.population.evolve_population()
            return True
        else:
            return False

    def get_info_surface(self):
        num_survived = sum([
            car.genome.genome_type == "survived" and car.alive
            for car in self.env.cars
        ])
        num_mutated = sum([
            car.genome.genome_type == "mutated" and car.alive
            for car in self.env.cars
        ])
        num_bred = sum([
            car.genome.genome_type == "bred" and car.alive
            for car in self.env.cars
        ])

        texts = [
            " Game: {}".format(self.game_count),
            " Score: {}".format(self.env.score),
            " Alive: {}".format(self.env.num_alive),
            " (Blue) Survived: {}".format(num_survived),
            " (Green) Mutated: {}".format(num_mutated),
            " (Yellow) Bred: {}".format(num_bred)
        ]

        return self.text_renderer.texts_to_surface(texts)

    # extended methods
    def get_x(self, car):
        if car.alive:
            degrees_diff = (car.degrees - Directions.to_degrees(car.tile.direction)) % 360
            return [
                # car.rel_x / const.TILE_SIZE,
                # car.rel_y / const.TILE_SIZE,
                # const.TILE_SIZE - (car.rel_x / const.TILE_SIZE),
                # const.TILE_SIZE - (car.rel_y / const.TILE_SIZE),
                (car.rel_x - const.TILE_SIZE // 2) / const.TILE_SIZE,
                (car.rel_y - const.TILE_SIZE // 2) / const.TILE_SIZE,
                car.speed,
                # car.velocity[0],
                # car.velocity[1],
                # car.tile.direction.x,
                # car.tile.direction.y,
                # np.dot(car.velocity, car.tile.direction.vec),
                (degrees_diff / 180) if degrees_diff < 180 else (degrees_diff - 360) / 180,
            ]
        # this part shouldn't really happen since
        # only living cars are called to think
        else:
            return [0] * self._num_input

class SmartCar(lib.car.Car):
    _genome_to_color = {
        "survived": "blue",
        "mutated": "green",
        "bred": "yellow",
        "diverged": "red"
    }

    def __init__(self, tile, genome, color=None):
        super().__init__(tile)

        # override randomized color
        self.genome = genome
        self.surface = self._images[self.get_color(genome)]
        # randomize starting angle
        self.degrees += (random.randint(-10, 10) * 4.5) % 360

    def get_color(self, genome):
        return self._genome_to_color[genome.genome_type]

    def think(self, x):
        pred = self.genome.predict(x)
        if pred[0] and self.speed < const.SPD_LIMIT:
            self.speed += const.ACC_RATE
        if pred[1] and self.speed > -const.SPD_LIMIT:
            self.speed -= const.ACC_RATE
        if pred[2]:
            self.degrees += const.TURN_SPD
        if pred[3]:
            self.degrees -= const.TURN_SPD
        self.degrees = self.degrees % 360
        self.velocity = self.get_velocity()
        return
