import random

import numpy as np
import pygame

import lib
import lib.constants as const
from lib.settings import Settings

import neat
import carvision

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
    _num_input = 6
    _num_output = 4

    # overriden methods
    def __init__(self):
        super().__init__()
        self.population = neat.Population(
            self._num_input,
            self._num_output,
            pop_size=settings.num_cars
        )
        self.walls = None
        return

    def new_game(self):
        super().new_game()
        for tile in self.env.track.track_tiles:
            tile.scaled_neighbor_walls = carvision.get_scaled_neighbor_walls(tile)
        return

    def new_cars(self):
        return [SmartCar(self.env.track.start_tile, genome) for genome in self.population.genomes]

    def update(self):
        self.clock.tick(settings.tickrate)
        self.events.update()
        settings.update(self.events)
        # only cycle through cars alive in the environment for optimization
        for car in self.env.cars:
            car.think(self.get_x(car))
        self.env.update()
        self.best_score = max(self.best_score, self.env.score)

    def game_over(self):
        if self.env.game_over():
            # added incentive
            # if the direction of the car is closer to the direction of
            # the tile grid, give reward
            scores = [
                car.score + car.time_bonus \
                + (180 - abs(carvision.get_singed_degrees_delta(car))) * 10 \
                for car in self.cars
            ]
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
            " Top Score: {}".format(self.best_score),
            " Alive: {}".format(self.env.num_alive),
            " (Blue) Survived: {}".format(num_survived),
            " (Green) Mutated: {}".format(num_mutated),
            " (Yellow) Bred: {}".format(num_bred)
        ]

        return self.text_renderer.texts_to_surface(texts)

    def get_debug_surface(self):
        texts = [
            " Top Speed: {0: .1f}".format(
                max([car.speed for car in self.env.cars])
            ),
            " FPS: {}".format(1000 // self.clock.get_time()),
        ]

        return self.text_renderer.texts_to_surface(texts)

    # extended methods
    def get_x(self, car):
        if car.alive:
            degrees_delta = carvision.get_singed_degrees_delta(car)
            distances = carvision.get_car_vision(car)
            return [
                car.speed,
                degrees_delta / 180,
                distances[0],
                distances[1],
                distances[2],
                distances[3],
            ]
            """
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
            """
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

        # extra features to incentivize going faster
        self.time_bonus = 0
        self.timer = const.TIMER
        self.prev_tile = self.tile

        # randomize starting angle
        self.direction.rotate(random.randint(-10, 10) * const.TURN_SPD)

    def update(self):
        super().update()
        # if car is still on the same tile, countdown the timer
        if self.prev_tile.grid == self.tile.grid:
            self.timer -= 1
        # if car went backwards, kill it off
        elif self.prev_tile.grid == self.tile.next.grid:
            self.alive = False
        # if car went worwards, reset timer
        elif self.prev_tile.grid == self.tile.prev.grid:
            self.time_bonus += self.timer
            self.timer = const.TIMER
            self.prev_tile = self.tile
        # if not any of the cases above, something went wrong
        else:
            raise Exception("tile update error")
        # if timer ran out, kill off the car
        if self.timer < 0:
            self.alive = False
        # fixing rounding error
        self.speed = round(self.speed, 1)
        return

    def get_color(self, genome):
        return self._genome_to_color[genome.genome_type]

    def think(self, x):
        pred = self.genome.predict(x)
        if pred[0] and self.speed < const.SPD_LIMIT:
            self.speed += const.ACC_RATE
        elif pred[1] and self.speed > -const.SPD_LIMIT:
            self.speed -= const.ACC_RATE
        elif self.speed > 0:
            self.speed -= const.ACC_RATE / 2
        elif self.speed < 0:
            self.speed += const.ACC_RATE / 2
        if pred[2]:
            self.direction.rotate(const.TURN_SPD)
        if pred[3]:
            self.direction.rotate(-const.TURN_SPD)
        self.velocity = self.direction.vector * self.speed
        return
