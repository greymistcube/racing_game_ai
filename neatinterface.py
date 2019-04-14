import pygame

import neat
import lib

from lib.settings import Settings
import lib.constants as const

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
    __num_input = 6
    __num_output = 4

    # overriden methods
    def __init__(self):
        super().__init__()
        self.population = neat.Population(
            self.__num_input,
            self.__num_output,
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
            return [
                car.rel_x / const.TILE_SIZE,
                car.rel_y / const.TILE_SIZE,
                car.velocity[0],
                car.velocity[1],
                car.tile.direction.x,
                car.tile.direction.y,
            ]
        # this part shouldn't really happen since
        # only living cars can think
        else:
            return [0] * self.__num_input

class SmartCar(lib.car.Car):
    __genome_to_color = {
        "survived": "blue",
        "mutated": "green",
        "bred": "yellow",
        "diverged": "red"
    }
    # dunder variables don't get inherited?
    __images = {
        "blue": load_image("./rsc/img/blue_car.png"),
        "green": load_image("./rsc/img/green_car.png"),
        "yellow": load_image("./rsc/img/yellow_car.png"),
        "red": load_image("./rsc/img/red_car.png"),
    }

    def __init__(self, tile, genome, color=None):
        super().__init__(tile)

        # override randomized color
        self.genome = genome
        self.surface = self.__images[self.get_color(genome)]

    def get_color(self, genome):
        return self.__genome_to_color[genome.genome_type]

    def think(self, x):
        pred = self.genome.predict(x)
        if pred[0] and self.speed < const.SPD_LIMIT:
            self.speed += const.ACC_RATE
        if pred[1] and self.speed > -const.SPD_LIMIT:
            self.speed -= const.ACC_RATE
        if pred[2]:
            self.degree += const.TURN_SPD
        if pred[3]:
            self.degree -= const.TURN_SPD
        self.degree = self.degree % 360
        self.velocity = self.get_velocity()
        return
