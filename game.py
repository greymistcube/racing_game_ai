import pygame

import lib
from lib.settings import Settings
import lib.constants as const
import argparser

pygame.init()

if __name__ == "__main__":
    args = argparser.get_args()

    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode(
        (const.WIDTH * args.z, const.HEIGHT * args.z)
    )
    clock = pygame.time.Clock()

    settings = Settings(args)
    core = lib.Core()
    core.new_game()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(settings.tickrate)

        core.update()

        if core.game_over():
            core.new_game()
            continue

        surface = core.get_surface()
        surface = pygame.transform.scale(surface, screen.get_size())
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
