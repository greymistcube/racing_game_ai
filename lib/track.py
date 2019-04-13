import numpy as np

import pygame

import lib
from lib import constants as const
from lib.grid import Grid, Directions

pygame.init()

def load_image(file):
    image = pygame.image.load(file)
    return image

# temporary method for creating an array representation of a track
def create_track_arr():
    temp = np.zeros((10, 14), dtype='int')
    temp[:, 0] = 1
    temp[:, -1] = 1
    temp[0, :] = 1
    temp[-1, :] = 1
    temp[0, 0] = 2
    result = np.zeros((12, 16), dtype='int')
    result[1:-1, 1:-1] += temp
    return result

def arr_to_grids(arr):
    result = []
    # find the most upper left coordinate with value not equal to zero
    # and set it as a temporary starting point
    for i, _ in enumerate(arr):
        for j, _ in enumerate(arr):
            if arr[i][j]:
                result.append(Grid(j, i))
                break
        if result:
            break

    start = result[0]
    while True:
        current = result[-1]

        # get four adjacent grids to check
        adjacents = current.adjacents()

        # if any of the adjacent grid is the same as the starting grid
        # and the length of the result is sufficient, we've completed the loop
        if (
            any([adjacent == start for adjacent in adjacents]) and
            len(result) > 2
        ):
            break

        for adjacent in adjacents:
            if arr[adjacent.y][adjacent.x] and adjacent not in result:
                result.append(adjacent)
                break

    return result

def grids_to_tiles(grids):
    result = []

    for grid in grids:
        if result:
            previous_tile = result[-1]
            current_tile = TrackTile(grid)
            previous_tile.next = current_tile
            current_tile.prev = previous_tile
            result.append(current_tile)
        else:
            result.append(TrackTile(grid))

    # connect the end points to complete the loop
    result[-1].next = result[0]
    result[0].prev = result[-1]
    """
    for track_tile in result:
        prev_tile = track_tile.prev
        next_tile = track_tile.next
        if track_tile.grid_x < next_tile.grid_x:
            track_tile.walls['r'] = False
        if track_tile.grid_x > next_tile.grid_x:
            track_tile.walls['l'] = False
        if track_tile.grid_y < next_tile.grid_y:
            track_tile.walls['b'] = False
        if track_tile.grid_y > next_tile.grid_y:
            track_tile.walls['t'] = False
        if track_tile.grid_x < prev_tile.grid_x:
            track_tile.walls['r'] = False
        if track_tile.grid_x > prev_tile.grid_x:
            track_tile.walls['l'] = False
        if track_tile.grid_y < prev_tile.grid_y:
            track_tile.walls['b'] = False
        if track_tile.grid_y > prev_tile.grid_y:
            track_tile.walls['t'] = False
    """
    return result

# this process is pretty mess at the moment
# might need some cleanup
def create_track():
    arr = create_track_arr()
    grids = arr_to_grids(arr)
    tiles = grids_to_tiles(grids)
    return tiles

# track object is basically a wrapper for a doubly linked list
# the object itself does not handle the creation process
class Track():
    __image = load_image("./rsc/img/track_tile.png")

    def __init__(self):
        self.track_tiles = create_track()
        # set starting tile. this should be randomized at some point
        self.start_tile = self.track_tiles[0]
        self.surface = self.create_surface()

    def create_surface(self):
        surface = pygame.Surface(const.RESOLUTION, pygame.SRCALPHA)
        for track_tile in self.track_tiles:
            surface.blit(track_tile.get_surface(), track_tile.rect)
        return surface

    def get_start_grid(self):
        return (self.start_tile.grid)

    def get_surface(self):
        return self.surface

class TrackTile():
    __image = load_image("./rsc/img/track_tile.png")
    __images = {
        "tb": load_image("./rsc/img/track_tile_tb.png"),
        "tl": load_image("./rsc/img/track_tile_tl.png"),
        "tr": load_image("./rsc/img/track_tile_tr.png"),
        "bl": load_image("./rsc/img/track_tile_bl.png"),
        "br": load_image("./rsc/img/track_tile_br.png"),
        "lr": load_image("./rsc/img/track_tile_lr.png"),
    }

    def __init__(self, grid):
        self.rect = self.__image.get_rect()
        self.grid = grid
        self.x = (self.grid.x * const.TILE_SIZE) + (const.TILE_SIZE // 2)
        self.y = (self.grid.y * const.TILE_SIZE) + (const.TILE_SIZE // 2)
        self.rect.center = (self.x, self.y)
        self.prev = None
        self.next = None

    def get_surface(self):
        return self.__image
