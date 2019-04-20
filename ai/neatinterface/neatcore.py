import pygame

import lib
import lib.constants as const
import lib.common as common

import ai.neat.neat as neat
from ai.neatinterface.smartcar import SmartCar

pygame.init()

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
            pop_size=common.settings.num_cars
        )
        self.best_score = 0
        self.walls = None
        return

    def new_game(self):
        super().new_game()
        self.best_score = 0
        # preprocessing data for later use for optimization
        # for tile in self.env.track.track_tiles:
        #     tile.scaled_neighbor_walls = sensor.get_scaled_neighbor_walls(tile)
        return

    def new_cars(self):
        return [SmartCar(self.env.track.start_tile, genome) for genome in self.population.genomes]

    def update(self):
        common.events.update()
        common.settings.update()
        # only cycle through cars alive in the environment for optimization
        for car in self.env.cars:
            car.think(self.get_x(car))
        self.env.update()
        self.best_score = max(self.best_score, self.env.score)

    def game_over(self):
        if self.env.game_over():
            # added incentives

            scores = [
                car.score \
                # negate crossing the start line bonus
                - const.LAP_BONUS \
                # strong time incentive once a lap is finished
                + car.time_bonus * car.laps * 10 \
                # if the direction of the car is closer to the direction of
                # the tile grid, give reward
                + (180 - abs(car.get_sensor_data()["degrees"])) * 10 \
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
            " Best Score: {}".format(self.best_score),
            " Alive: {}".format(self.env.num_alive),
            " (Blue) Survived: {}".format(num_survived),
            " (Green) Mutated: {}".format(num_mutated),
            " (Yellow) Bred: {}".format(num_bred)
        ]

        return common.display.texts_to_surface(texts)

    def get_debug_surface(self):
        texts = [
            " Top Speed: {0: .1f}".format(
                max([car.speed for car in self.env.cars])
            ),
            " FPS: {}".format(common.clock.get_FPS()),
        ]

        return common.display.texts_to_surface(texts)

    # extended methods
    def get_x(self, car):
        if car.alive:
            sensor_data = car.get_sensor_data()
            return [
                car.speed,
                sensor_data["degrees"] / 180,
                sensor_data["front"] / const.TILE_SIZE,
                sensor_data["back"] / const.TILE_SIZE,
                sensor_data["left"] / const.TILE_SIZE,
                sensor_data["right"] / const.TILE_SIZE,
            ]
        # this part shouldn't really happen since
        # only living cars are called to think
        else:
            return [0] * self._num_input
