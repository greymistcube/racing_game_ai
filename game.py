import pygame

import lib

pygame.init()

if __name__ == "__main__":
    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((320 * 3, 240 * 3))
    clock = pygame.time.Clock()

    core = lib.Core()
    core.new_game()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(60)

        core.update()

        if core.game_over():
            core.new_game()
            continue

        surface = core.get_surface()
        surface = pygame.transform.scale(surface, screen.get_size())
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
