import numpy as np
from tesselation.command import Command


class Sphere(Command):
    def __init__(self, R, origin, N, filepath):
        super().__init__(filepath)
        self.R = R
        self.origin = np.array(origin)
        self.N = N

    def execute(self):
        vertices = []
        faces = []
        for i in range(self.N + 1):
            phi = i * np.pi / self.N
            for j in range(self.N + 1):
                theta = j * 2 * np.pi / self.N
                x = self.R * np.sin(phi) * np.cos(theta)
                y = self.R * np.sin(phi) * np.sin(theta)
                z = self.R * np.cos(phi)
                vertices.append([x, y, z])

        vertices = np.array(vertices) + self.origin
        for i in range(self.N):
            for j in range(self.N):
                v0 = i * (self.N + 1) + j
                v1 = v0 + 1
                v2 = (i + 1) * (self.N + 1) + j
                v3 = v2 + 1
                faces.append([v0, v1, v2])
                faces.append([v1, v3, v2])

        self.save_stl(vertices, np.array(faces))
