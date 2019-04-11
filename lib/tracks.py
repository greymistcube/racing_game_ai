import numpy as np

import pygame

import lib
from lib.constants import RESOLUTION, WIDTH, HEIGHT, GREEN

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

class Track():
    __image = load_image("./rsc/img/track_tile.png")

    def __init__(self):
        temp = np.zeros((12, 18), dtype='int')
        temp[:, 0] = 1
        temp[:, -1] = 1
        temp[0, :] = 1
        temp[-1, :] = 1
        temp[0, 0] = 2
        self.track = np.zeros((15, 20), dtype='int')
        self.track[1:-2, 1:-1] += temp
        self.surface = self.create_surface()
    
    def create_surface(self):
        surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        surface.fill(GREEN)
        for i in range(15):
            for j in range(20):
                if self.track[i][j] > 0:
                    surface.blit(self.__image, (j * 16, i * 16))
        return surface

    def get_surface(self):
        return self.surface
        