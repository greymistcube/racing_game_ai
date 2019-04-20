import pygame

import lib.constants as const
import lib.common as common

# initializing module
pygame.init()

class Display:
    __instance = None
    _font = pygame.font.Font("./rsc/font/monogram.ttf", 16)
    _line_height = _font.get_linesize()

    # implementing this class as singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            return cls.__instance
        else:
            raise Exception("only single instance is allowed")

    def __init__(self):
        self.screen = pygame.display.set_mode(
            common.settings.display_size
        )
        return

    def draw(self, surface):
        surface = pygame.transform.scale(surface, self.screen.get_size())
        self.screen.blit(surface, surface.get_rect())
        pygame.display.flip()
        return

    # render a single line of text
    def text_to_surface(self, text):
        return self._font.render(text, False, const.BLACK)

    # render multiple lines of texts
    def texts_to_surface(self, texts):
        text_surfaces = [self.text_to_surface(text) for text in texts]

        # create a big enough surface to paste all single line surfaces
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
