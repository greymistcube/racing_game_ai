# this is mostly to simplify the codes in other modules
class Grid:
    def __init__(self, x=0, y=0):
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

    def adjacents(self):
        return [self + direction for direction in Directions()]

    @property
    def N(self):
        return self + Directions.N

    @property
    def E(self):
        return self + Directions.E

    @property
    def S(self):
        return self + Directions.S

    @property
    def W(self):
        return self + Directions.W

class Directions:
    __instance = None
    N = Grid(0, -1)
    E = Grid(1, 0)
    S = Grid(0, 1)
    W = Grid(-1, 0)

    # implementing this class as singleton
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
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
