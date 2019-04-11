import pygame

import lib

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

class Car():
    __image = load_image("./rsc/img/tiny_car.png")

    def __init__(self):
        return
