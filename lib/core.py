import pygame

import lib.common as common

from lib.objects.environment import Environment
from lib.objects.car import Car

# initializing module
pygame.init()

class Core:
    def __init__(self):
        self.game_count = 0
        self.cars = None
        self.env = None
        return

    def new_game(self):
        self.game_count += 1
        self.env = Environment()
        self.cars = self.new_cars()
        self.env.add_cars(self.cars)
        return

    def new_cars(self):
        return [Car(self.env.track.start_tile) for _ in range(common.settings.num_cars)]

    def update(self):
        common.events.update()
        common.settings.update()
        for car in self.cars:
            car.handle_events()
        self.env.update()

    def game_over(self):
        return self.env.game_over()

    def get_surface(self):
        surface = self.env.get_surface()
        info_surface = self.get_info_surface()
        debug_surface = self.get_debug_surface()
        debug_y_offset = info_surface.get_height()
        if common.settings.info:
            surface.blit(info_surface, (0, 0))
        if common.settings.debug:
            surface.blit(debug_surface, (0, debug_y_offset))
        return surface

    def get_info_surface(self):
        texts = [
            " Game: {}".format(self.game_count),
            " Score: {}".format(self.env.score),
            " Alive: {}".format(self.env.num_alive)
        ]

        return common.display.texts_to_surface(texts)

    def get_debug_surface(self):
        texts = [
            " Speed: {0: .1f}".format(self.env.cars[0].speed),
            " FPS: {}".format(common.clock.get_FPS()),
        ]
        car = self.cars[0]
        sensor_data = car.get_sensor_data()

        distance_texts = [
            " Front: {0: .1f}".format(sensor_data["front"]),
            " Back: {0: .1f}".format(sensor_data["back"]),
            " Left: {0: .1f}".format(sensor_data["left"]),
            " Right: {0: .1f}".format(sensor_data["right"]),
        ]
        degrees_delta_text = [
            " Degrees Delta: {}".format(sensor_data["degrees"])
        ]

        return common.display.texts_to_surface(
            texts + distance_texts + degrees_delta_text
        )
