import sys
import pygame

import lib

pygame.init()

if __name__ == "__main__":
    # pygame initialization
    pygame.init()
    screen = pygame.display.set_mode((320 * 3, 240 * 3))
    clock = pygame.time.Clock()
    env = lib.Environment()

    # main loop
    while True:
        # set tick rate to 60 per second
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        env.update()

        surface = env.get_surface()
        surface = pygame.transform.scale(surface, screen.get_size())
        screen.blit(surface, surface.get_rect())
        pygame.display.flip()
