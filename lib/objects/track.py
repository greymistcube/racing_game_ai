import random

import pygame

import lib.constants as const
from lib.tools import trackgenerator

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

# track object is basically a wrapper for a doubly linked list
# with a reference to its starting node
# the object itself does not handle the creation process
class Track():
    __start_line_image = load_image("./rsc/img/start_line.png")

    def __init__(self):
        self.track_tiles = trackgenerator.create_track(
            const.WIDTH // const.TILE_SIZE,
            const.HEIGHT // const.TILE_SIZE
        )
        # set the starting tile
        self.start_tile = random.choice(self.track_tiles)
        self.start_tile.is_start_tile = True
        self.surface = self.set_surface()

    # as a track is static throught a game, create a surface
    # during initialization
    def set_surface(self):
        surface = pygame.Surface(const.RESOLUTION, pygame.SRCALPHA)
        for track_tile in self.track_tiles:
            surface.blit(track_tile.get_surface(), track_tile.rect)
        surface.blit(
            pygame.transform.rotate(
                self.__start_line_image,
                self.start_tile.direction.degrees
            ),
            self.start_tile.rect
        )

        return surface

    def get_surface(self):
        return self.surface
