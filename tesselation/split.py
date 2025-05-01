import numpy as np
from stl import mesh
from tesselation.command import Shape


class Split(Shape):
    def __init__(self, input_filepath, filepath):
        super().__init__(filepath)
        self.input_filepath = input_filepath

    def execute(self):
        input_mesh = mesh.Mesh.from_file(self.input_filepath)
        vertices = input_mesh.vectors.reshape(-1, 3)
        faces = np.arange(len(vertices)).reshape(-1, 3)

        new_vertices = []
        new_faces = []
        for f in faces:
            v0, v1, v2 = vertices[f[0]], vertices[f[1]], vertices[f[2]]
            v01 = (v0 + v1) / 2
            new_vertices.extend([v0, v01, v2])
            new_vertices.extend([v1, v01, v2])
            new_faces.append([len(new_vertices) - 6, len(new_vertices) - 5, len(new_vertices) - 4])
            new_faces.append([len(new_vertices) - 3, len(new_vertices) - 2, len(new_vertices) - 1])

        self.save_stl(np.array(new_vertices), np.array(new_faces))