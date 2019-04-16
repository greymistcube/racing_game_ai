import sys
import pygame

pygame.init()

class Events:
    def __init__(self):
        self.multiplier = 1
        self.acc = False
        self.dec = False
        self.left = False
        self.right = False
        self.info = False
        # temporary debugging feature
        self.stop = False
        return

    def update(self):
        # check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # check for pressed keys and update variables accordingly
        pressed_keys = pygame.key.get_pressed()
        self.acc = pressed_keys[pygame.K_UP]
        self.dec = pressed_keys[pygame.K_DOWN]
        self.left = pressed_keys[pygame.K_LEFT]
        self.right = pressed_keys[pygame.K_RIGHT]
        self.stop = pressed_keys[pygame.K_SPACE]
        self.info = pressed_keys[pygame.K_i]
        for i, pressed in enumerate(pressed_keys[pygame.K_0:pygame.K_0 + 10]):
            if pressed:
                self.multiplier = i
                break
        return
