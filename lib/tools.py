import numpy as np

_R = lambda theta: np.array([
    [np.cos(theta), -np.sin(theta)],
    [np.sin(theta), np.cos(theta)],
])

class Direction:
    def __init__(self, degrees):
        self.degrees = degrees
        self.vector = self.__degrees_to_vector(self.degrees)

    def rotate(self, degrees):
        self.degrees = (self.degrees + degrees) % 360
        self.vector = self.__degrees_to_vector(self.degrees)

    def __degrees_to_vector(self, degrees):
        return np.matmul(_R(np.radians(degrees)), (0, 1))
