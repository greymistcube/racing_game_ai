import numpy as np

from lib.grid import Grid
import lib.tools as tools
import lib.shared.constants as const

grid_walls = {
    "n": (Grid(0, 0), Grid(1, 0)),
    "e": (Grid(1, 0), Grid(1, 1)),
    "s": (Grid(0, 1), Grid(1, 1)),
    "w": (Grid(0, 0), Grid(0, 1)),
}

def get_car_vision(car):
    # get all the walls in its neighboring tiles
    walls = car.tile.scaled_neighbor_walls
    # get distances in four directions
    distances = get_distances(car, walls)

    return distances

def get_scaled_neighbor_walls(tile):
    grid_delta_prev = tile.prev.grid - tile.grid
    grid_delta_next = tile.next.grid - tile.grid

    cardinals = "nesw"
    walls = []

    for cardinal in cardinals:
        if cardinal in tile.key:
            walls.append(grid_walls[cardinal])
        if cardinal in tile.prev.key:
            walls.append(
                (
                    grid_walls[cardinal][0] + grid_delta_prev,
                    grid_walls[cardinal][1] + grid_delta_prev,
                )
            )
        if cardinal in tile.next.key:
            walls.append(
                (
                    grid_walls[cardinal][0] + grid_delta_next,
                    grid_walls[cardinal][1] + grid_delta_next,
                )
            )

    # convert to scaled pixel coordinates and return it as a numpy array
    walls = np.array([[wall[0].scaled, wall[1].scaled] for wall in walls])
    return walls

def get_distances(car, walls):
    pt = np.array([car.rel_x, car.rel_y])

    # change of coordinates when taking pt to (0, 0)
    center = lambda v: v - pt
    walls = np.apply_along_axis(center, 2, walls)

    # rotation transformation when aligning vec to (1, 0)
    # still haven't figured out why this should be positive
    # most likely because y axis is flipped upside down
    # direction class and rotation method should be overhauled
    # to keep better track of what is going on
    rotate = lambda v: np.matmul(tools.R(car.direction.degrees), v)
    walls = np.apply_along_axis(rotate, 2, walls)
    x_intersects = []
    y_intersects = []
    # now we only need to check sign differences in x or y coordinates
    for wall in walls:
        # if x signs differ, then it crosses the y axis
        if wall[0][0] * wall[1][0] < 0:
            y_intersects.append(wall)
        # if y signs differ, then it crosses the x axis
        # elif should not be used since line segments
        # close to the origin may cross both axes
        if wall[0][1] * wall[1][1] < 0:
            x_intersects.append(wall)

    # two point line equation for reference:
    # y - y1 = ((y2 - y1) / (x2 - x1)) * (x - x1)
    # division by zero should have been avoided when checking signs
    # compute x and y intercepts
    # +TILE_SIZE and -TILE_SIZE are added in as limits and for normalization
    x_intercepts = [-const.TILE_SIZE, const.TILE_SIZE]
    y_intercepts = [-const.TILE_SIZE, const.TILE_SIZE]
    for wall in x_intersects:
        x_intercepts.append(
            (-wall[0][1]) * (wall[1][0] - wall[0][0]) / (wall[1][1] - wall[0][1]) \
            + wall[0][0]
        )
    for wall in y_intersects:
        y_intercepts.append(
            ((wall[1][1] - wall[0][1]) / (wall[1][0] - wall[0][0])) \
            * (-wall[0][0]) + wall[0][1]
        )
    front = min([x for x in x_intercepts if x > 0]) / 20
    back = min([-x for x in x_intercepts if x < 0]) / 20
    # left and right might be swapped
    # shouldn't really matter for the end result
    left = min([-y for y in y_intercepts if y < 0]) / 20
    right = min([y for y in y_intercepts if y > 0]) / 20
    return {
        "front": front,
        "back": back,
        "left": left,
        "right": right
    }

def get_singed_degrees_delta(car):
    delta = (car.direction.degrees - car.tile.direction.degrees) % 360
    return delta if delta < 180 else (delta - 360)
