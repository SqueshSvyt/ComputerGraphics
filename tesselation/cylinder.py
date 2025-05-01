from tesselation.command import Shape
import numpy as np


class Cylinder(Shape):
    def __init__(self, radius, height, sectors, origin, filepath):
        super().__init__(filepath)
        self.radius = radius
        self.height = height
        self.sectors = sectors
        self.origin = np.array(origin, dtype=np.float32)

    def tessellate(self):
        vertices = []
        faces = []

        # Вершини для нижньої та верхньої основ
        for i in range(self.sectors):
            theta = 2.0 * np.pi * i / self.sectors
            x = self.radius * np.cos(theta)
            y = self.radius * np.sin(theta)
            # Нижня основа (z = 0)
            vertices.append([x, y, 0])
            # Верхня основа (z = height)
            vertices.append([x, y, self.height])

        # Центри основ
        vertices.append([0, 0, 0])  # центр нижньої основи
        vertices.append([0, 0, self.height])  # центр верхньої основи

        vertices = np.array(vertices, dtype=np.float32) + self.origin

        # Грані
        # Нижня основа
        center_bottom = len(vertices) - 2
        for i in range(self.sectors):
            next_i = (i + 1) % self.sectors
            faces.append([center_bottom, 2 * next_i, 2 * i])

        # Верхня основа
        center_top = len(vertices) - 1
        for i in range(self.sectors):
            next_i = (i + 1) % self.sectors
            faces.append([center_top, 2 * i + 1, 2 * next_i + 1])

        # Бічна поверхня
        for i in range(self.sectors):
            next_i = (i + 1) % self.sectors
            # Два трикутники для кожної бічної грані
            faces.append([2 * i, 2 * next_i, 2 * i + 1])
            faces.append([2 * next_i, 2 * next_i + 1, 2 * i + 1])

        faces = np.array(faces, dtype=np.uint32)
        return vertices, faces

    def execute(self):
        vertices, faces = self.tessellate()
        self.save_stl(vertices, faces)
