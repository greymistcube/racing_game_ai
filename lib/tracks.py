import numpy as np

import pygame

import lib
from lib.constants import RESOLUTION, WIDTH, HEIGHT, GREEN, TILE_WIDTH, TILE_HEIGHT

pygame.init()


def load_image(file):
    image = pygame.image.load(file)
    return image

# temporary method for creating an array representation of a track
def get_track_arr():
    temp = np.zeros((12, 18), dtype='int')
    temp[:, 0] = 1
    temp[:, -1] = 1
    temp[0, :] = 1
    temp[-1, :] = 1
    temp[0, 0] = 2
    result = np.zeros((15, 20), dtype='int')
    result[1:-2, 1:-1] += temp
    return result

def get_track_pos_list(arr):
    result = []
    # find the most upper left coordinate with value not equal to zero
    # and set it as a temporary starting point
    for i, _ in enumerate(arr):
        for j, _ in enumerate(arr):
            if arr[i][j]:
                result.append((j, i))
                break
        if result:
            break
    
    while(True):
        current = result[-1]
        
        # four adjacent coordinates to check
        adjacents = (
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1),
        )

        # if any of the adjacent position is the same as the starting position
        # and the length of the result is sufficient, we've completed the loop
        if any([pos == result[0] for pos in adjacents]) and len(result) > 2:
            break
        
        for pos in adjacents:
            if arr[pos[1]][pos[0]] and pos not in result:
                result.append(pos)
                break

    return result

def get_track_tile_list(track_pos_list):
    result = []
    start_tile = TrackTile(track_pos_list[0][0], track_pos_list[0][1])
    previous_tile = start_tile

    for pos in track_pos_list:
        if result:
            previous_tile = result[-1]
            current_tile = TrackTile(pos[0], pos[1])
            previous_tile.next = current_tile
            current_tile.prev = previous_tile
            result.append(current_tile)
        else:
            result.append(TrackTile(pos[0], pos[1]))
    
    # connect the end points to complete the loop
    result[-1].next = result[0]
    result[0].prev = result[-1]
    return result

# this process is pretty mess at the moment
# might need some cleanup
def create_track():
    arr = get_track_arr()
    track_pos_list = get_track_pos_list(arr)
    result = get_track_tile_list(track_pos_list)
    return result

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
        surface = pygame.Surface(RESOLUTION, pygame.SRCALPHA)
        for track_tile in self.track_tiles:
            surface.blit(self.__image, track_tile.rect)
        return surface

    def get_start_grid(self):
        return (self.start_tile.grid_x, self.start_tile.grid_y)

    def get_surface(self):
        return self.surface

class TrackTile():
    __image = load_image("./rsc/img/track_tile.png")

    def __init__(self, grid_x, grid_y):
        self.rect = self.__image.get_rect()
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.x = (self.grid_x * TILE_WIDTH) + (TILE_WIDTH // 2)
        self.y = (self.grid_y * TILE_HEIGHT) + (TILE_HEIGHT // 2)
        self.rect.center = (self.x, self.y)
        self.prev = None
        self.next = None
    
    def get_surface(self):
        return self.__image
