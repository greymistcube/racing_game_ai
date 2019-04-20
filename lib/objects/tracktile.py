import pygame

import lib.constants as const
from lib.tools.grid import Cardinals, Walls
from lib.tools.direction import Direction

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

class TrackTile():
    _image = load_image("./rsc/img/track_tile.png")
    _images = {
        "ne": load_image("./rsc/img/track_tile_ne.png"),
        "nw": load_image("./rsc/img/track_tile_nw.png"),
        "se": load_image("./rsc/img/track_tile_se.png"),
        "sw": load_image("./rsc/img/track_tile_sw.png"),
        "ns": load_image("./rsc/img/track_tile_ns.png"),
        "ew": load_image("./rsc/img/track_tile_ew.png"),
    }

    def __init__(self, grid):
        self.rect = self._image.get_rect()
        self.grid = grid
        self.x = (self.grid.x * const.TILE_SIZE) + (const.TILE_SIZE // 2)
        self.y = (self.grid.y * const.TILE_SIZE) + (const.TILE_SIZE // 2)
        self.rect.center = (self.x, self.y)
        self.prev = None
        self.next = None
        self.direction = None
        self.walls = []
        self.key = ""
        self.surface = self._image
        self.is_start_tile = False
        return

    def set_track_properties(self):
        # cardinal direction naming order: n, s, e, w
        cardinals = "nsew"
        hole = ""
        if self.grid.N == self.prev.grid or self.grid.N == self.next.grid:
            hole += "n"
        if self.grid.S == self.prev.grid or self.grid.S == self.next.grid:
            hole += "s"
        if self.grid.E == self.prev.grid or self.grid.E == self.next.grid:
            hole += "e"
        if self.grid.W == self.prev.grid or self.grid.W == self.next.grid:
            hole += "w"
        for cardinal in cardinals:
            if cardinal not in hole:
                self.key += cardinal
                self.walls.append(Walls.char_to_wall(cardinal))
        self.direction = Direction(Cardinals.to_degrees(self.next.grid - self.grid))
        self.surface = self._images[self.key]
        return

    def get_surface(self):
        return self.surface
