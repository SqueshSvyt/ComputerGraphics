from tesselation.command import Shape
import numpy as np


class Pyramid(Shape):
    def __init__(self, base_size, height, origin, filepath):
        super().__init__(filepath)
        self.base_size = base_size
        self.height = height
        self.origin = np.array(origin, dtype=np.float32)

    def tessellate(self):
        # Вершини піраміди
        half_base = self.base_size / 2.0
        vertices = np.array([
            # Основа (квадрат)
            [-half_base, -half_base, 0],  # 0
            [ half_base, -half_base, 0],  # 1
            [ half_base,  half_base, 0],  # 2
            [-half_base,  half_base, 0],  # 3
            # Вершина піраміди
            [0, 0, self.height]           # 4
        ], dtype=np.float32) + self.origin

        # Грані
        faces = np.array([
            # Основа
            [0, 1, 2], [2, 3, 0],
            # Бічні грані
            [0, 1, 4],  # передня
            [1, 2, 4],  # права
            [2, 3, 4],  # задня
            [3, 0, 4]   # ліва
        ], dtype=np.uint32)

        return vertices, faces

    def execute(self):
        vertices, faces = self.tessellate()
        self.save_stl(vertices, faces)