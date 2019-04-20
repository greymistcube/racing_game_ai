import pygame

import lib.constants as const
from lib.settings import Settings
from lib.events import Events
from lib.environment import Environment
from lib.car import Car

import carvision

pygame.init()
settings = Settings()

class TextRenderer:
    _font = pygame.font.Font("./rsc/font/monogram.ttf", 16)
    # simulate bold font
    # better readability but uglier
    # _font.set_bold(True)
    _line_height = _font.get_linesize()

    # render a single line of text
    def text_to_surface(self, text):
        return self._font.render(text, False, const.BLACK)

    # render multiple lines of texts
    def texts_to_surface(self, texts):
        text_surfaces = [self.text_to_surface(text) for text in texts]
        surface = pygame.Surface(
            (
                max(text_surface.get_width() for text_surface in text_surfaces),
                len(text_surfaces) * self._line_height
            ),
            pygame.SRCALPHA
        )
        for i, text_surface in enumerate(text_surfaces):
            surface.blit(text_surface, (0, self._line_height * i))
        return surface

class Core:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.text_renderer = TextRenderer()
        self.game_count = 0
        self.events = Events()
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
        return [Car(self.env.track.start_tile) for _ in range(settings.num_cars)]

    def update(self):
        self.clock.tick(settings.tickrate)
        self.events.update()
        settings.update(self.events)
        for car in self.cars:
            car.handle_events(self.events)
        self.env.update()

    def game_over(self):
        return self.env.game_over()

    def get_surface(self):
        surface = self.env.get_surface()
        info_surface = self.get_info_surface()
        debug_surface = self.get_debug_surface()
        debug_y_offset = info_surface.get_height()
        if settings.info:
            surface.blit(info_surface, (0, 0))
        if settings.debug:
            surface.blit(debug_surface, (0, debug_y_offset))
        return surface

    def get_info_surface(self):
        texts = [
            " Game: {}".format(self.game_count),
            " Score: {}".format(self.env.score),
            " Alive: {}".format(self.env.num_alive)
        ]

        return self.text_renderer.texts_to_surface(texts)

    def get_debug_surface(self):
        texts = [
            " Speed: {0: .1f}".format(self.env.cars[0].speed),
            " FPS: {}".format(1000 // self.clock.get_time()),
        ]
        car = self.cars[0]
        walls = carvision.get_scaled_neighbor_walls(car.tile)
        distances = carvision.get_distances(car, walls)
        distance_texts = [
            " Front: {0: .1f}".format(distances["front"]),
            " Back: {0: .1f}".format(distances["back"]),
            " Left: {0: .1f}".format(distances["left"]),
            " Right: {0: .1f}".format(distances["right"]),
        ]
        degrees_delta_text = [
            " Degrees Delta: {}".format(carvision.get_singed_degrees_delta(car))
        ]

        return self.text_renderer.texts_to_surface(
            texts + distance_texts + degrees_delta_text
        )
