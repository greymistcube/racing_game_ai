import numpy as np

def R(degrees):
    rad = np.radians(degrees)
    return np.array([
        [np.cos(rad), -np.sin(rad)],
        [np.sin(rad), np.cos(rad)],
    ])

class Direction:
    def __init__(self, degrees):
        self.degrees = degrees % 360
        self.vector = self.__degrees_to_vector(self.degrees)

    def rotate(self, degrees):
        self.degrees = (self.degrees + degrees) % 360
        self.vector = self.__degrees_to_vector(self.degrees)

    def __degrees_to_vector(self, degrees):
        return np.matmul(R(degrees), (0, 1))
