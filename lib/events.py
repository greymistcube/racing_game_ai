import sys
import pygame

pygame.init()

class Events:
    def __init__(self):
        self.acc = False
        self.dec = False
        self.left = False
        self.right = False
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
        return
