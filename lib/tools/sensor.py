import numpy as np

from lib.tools.direction import R
import lib.constants as const

class Sensor:
    def __init__(self):
        pass

    @classmethod
    def get_sensor_data(cls, tile, rel_x, rel_y, direction):
        pt = np.array([rel_x, rel_y])
        walls = []
        neighbors = [tile.prev, tile, tile.next]

        # collect all walls from neighboring tiles
        for neighbor in neighbors:
            grid_delta = neighbor.grid - tile.grid
            for wall in neighbor.walls:
                walls.append((
                    wall[0] + grid_delta,
                    wall[1] + grid_delta,
                ))

        # convert to relative pixel coordinates
        walls = np.array([[wall[0].scaled, wall[1].scaled] for wall in walls])

        result = cls.get_distances(pt, direction, walls)
        result.update(cls.get_signed_degrees_delta(tile.direction, direction))
        return result

    @classmethod
    def get_distances(cls, pt, direction, walls):
        # change of coordinates when taking pt to (0, 0)
        center = lambda v: v - pt
        walls = np.apply_along_axis(center, 2, walls)

        # rotation transformation when aligning vec to (1, 0)
        # still haven't figured out why this should be positive
        # most likely because y axis is flipped upside down
        # direction class and rotation method should be overhauled
        # to keep better track of what is going on
        rotate = lambda v: np.matmul(R(direction.degrees), v)
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
        front = min([x for x in x_intercepts if x > 0])
        back = min([-x for x in x_intercepts if x < 0])
        # left and right might be swapped
        # shouldn't really matter for the end result
        left = min([-y for y in y_intercepts if y < 0])
        right = min([y for y in y_intercepts if y > 0])

        return {
            "front": front,
            "back": back,
            "left": left,
            "right": right
        }

    @classmethod
    def get_signed_degrees_delta(cls, base_direction, target_direction):
        delta = (target_direction.degrees - base_direction.degrees) % 360
        return {
            "degrees": delta if delta < 180 else (delta - 360)
        }
