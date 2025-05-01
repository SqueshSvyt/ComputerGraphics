import numpy as np
from tesselation.command import Shape


class Cube(Shape):
    def __init__(self, L, origin, filepath):
        super().__init__(filepath)
        self.L = L
        self.origin = np.array(origin)

    def execute(self):
        vertices, faces = self.tessellate()
        self.save_stl(vertices, faces)

    def tessellate(self):
        vertices = np.array([
            [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
            [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
        ]) * self.L + self.origin

        faces = np.array([
            [0, 1, 2], [2, 3, 0],
            [4, 5, 6], [6, 7, 4],
            [0, 1, 5], [5, 4, 0],
            [2, 3, 7], [7, 6, 2],
            [0, 3, 7], [7, 4, 0],
            [1, 2, 6], [6, 5, 1]
        ])

        return vertices, faces

