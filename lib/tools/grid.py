# this is mostly to simplify the codes in other modules
import numpy as np

import lib.constants as const

class Grid:
    def __init__(self, x=0, y=0):
        if (not isinstance(x, int)) or (not isinstance(y, int)):
            raise Exception("only integer is allowed")
        self.x = x
        self.y = y

    def __add__(self, other):
        return Grid(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Grid(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

    def __bool__(self):
        return self.x != 0 or self.y != 0

    def adjacents(self):
        return [self + cardinal for cardinal in Cardinals()]

    @property
    def N(self):
        return self + Cardinals.N

    @property
    def E(self):
        return self + Cardinals.E

    @property
    def S(self):
        return self + Cardinals.S

    @property
    def W(self):
        return self + Cardinals.W

    @property
    def scaled(self):
        return np.array([self.x, self.y]) * const.TILE_SIZE

class Cardinals:
    __instance = None
    N = Grid(0, -1)
    E = Grid(1, 0)
    S = Grid(0, 1)
    W = Grid(-1, 0)

    # implementing this class as a singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.count = 0
        return

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        self.count += 1
        if self.count == 1:
            return self.N
        elif self.count == 2:
            return self.E
        elif self.count == 3:
            return self.S
        elif self.count == 4:
            return self.W
        else:
            raise StopIteration

    @classmethod
    def to_degrees(cls, grid):
        if grid == cls.E:
            return 0
        if grid == cls.N:
            return 90
        if grid == cls.W:
            return 180
        if grid == cls.S:
            return 270
        raise Exception("non cardinal direction grid was given")

    @classmethod
    def to_grid(cls, degrees):
        if degrees == 0:
            return cls.E
        if degrees == 90:
            return cls.N
        if degrees == 180:
            return cls.W
        if degrees == 270:
            return cls.S
        raise Exception("non cardinal direction degrees was given")

class Walls:
    __instance = None

    # implementing this class as a singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @staticmethod
    def N():
        return (Grid(0, 0), Grid(1, 0))

    @staticmethod
    def E():
        return (Grid(1, 0), Grid(1, 1))

    @staticmethod
    def S():
        return (Grid(0, 1), Grid(1, 1))

    @staticmethod
    def W():
        return (Grid(0, 0), Grid(0, 1))

    @classmethod
    def char_to_wall(cls, char):
        if char == "n" or char == "N":
            return cls.N()
        elif char == "e" or char == "E":
            return cls.E()
        elif char == "s" or char == "S":
            return cls.S()
        elif char == "w" or char == "W":
            return cls.W()
        else:
            raise Exception("non cardinal character was given")

    @classmethod
    def direction_to_wall(cls, direction):
        if direction.degrees % 90 == 0:
            idx = direction.degrees // 90
            return cls.char_to_wall("ensw"[idx])
        else:
            raise Exception("non cardinal direction object was given")

    @classmethod
    def grid_to_wall(cls, grid):
        if grid in Cardinals():
            idx = Cardinals.to_degrees(grid) // 90
            return cls.char_to_wall("ensw"[idx])
        else:
            raise Exception("non cardinal grid object was given")
