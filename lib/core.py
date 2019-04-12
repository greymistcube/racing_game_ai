import numpy as np

from lib.events import Events
from lib.environment import Environment
from lib.car import Car

class Core:
    def __init__(self):
        self.game_count = 0
        self.events = Events()
        self.cars = None
        self.env = None
        return
    
    def new_game(self):
        self.game_count += 1
        self.env = Environment()
        start_grid = self.env.track.get_start_grid()
        self.cars = [Car(start_grid)]
        self.env.add_cars(self.cars)
        return
    
    def update(self):
        self.events.update()
        for car in self.cars:
            car.update(self.events)
        self.env.update(self.events)

    def game_over(self):
        return False
    
    def get_surface(self):
        return self.env.get_surface()
