import pygame
import lib.shared.constants as const

pygame.init()

class Display:
    def __init__(self, args):
        self.screen = pygame.display.set_mode(
            (const.WIDTH * args.z, const.HEIGHT * args.z)
        )
        return

    def draw(self, surface):
        surface = pygame.transform.scale(surface, self.screen.get_size())
        self.screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        return
