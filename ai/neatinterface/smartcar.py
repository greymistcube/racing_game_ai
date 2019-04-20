import random

import lib
import lib.constants as const
from lib.tools.sensor import Sensor

class SmartCar(lib.objects.car.Car):
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
        self.death_type = 0

    def update(self):
        super().update()
        # if car is still on the same tile, countdown the timer
        if self.prev_tile.grid == self.tile.grid:
            self.timer -= 1
        # if car went backwards, kill it off
        elif self.prev_tile.grid == self.tile.next.grid:
            self.alive = False
            self.death_type = 1
        # if car went forwards, reset timer
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
            self.death_type = 2
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
