import struct

import numpy as np


class STLParser:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.normals = []

    def write(self, filepath, vertices, faces, normals=None):
        if normals is None:
            normals = [self.calculate_normal([vertices[idx] for idx in face]) for face in faces]
        with open(filepath, 'w') as f:
            f.write("solid MeshEditor\n")
            for i, face in enumerate(faces):
                normal = normals[i]
                f.write(f"facet normal {normal[0]} {normal[1]} {normal[2]}\n")
                f.write("    outer loop\n")
                for vertex_idx in face:
                    vertex = vertices[vertex_idx]
                    f.write(f"        vertex {vertex[0]} {vertex[1]} {vertex[2]}\n")
                f.write("    endloop\n")
                f.write("endfacet\n")
            f.write("endsolid MeshEditor\n")
        print(f"STL saved to {filepath}")

    def read(self, filepath):
        self.vertices = []
        self.faces = []
        self.normals = []
        vertex_map = {}
        with open(filepath, 'r') as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("facet normal"):
                    normal = [float(x) for x in line.split()[2:5]]
                    self.normals.append(normal)
                    i += 1
                    current_vertices = []
                    for j in range(3):
                        vertex_line = lines[i + j].strip()
                        if vertex_line.startswith("vertex"):
                            vertex = tuple(float(x) for x in vertex_line.split()[1:4])
                            if vertex not in vertex_map:
                                vertex_map[vertex] = len(self.vertices)
                                self.vertices.append(vertex)
                            current_vertices.append(vertex_map[vertex])
                    self.faces.append(current_vertices)
                    i += 3
                i += 1
        self.vertices = np.array(self.vertices)
        self.faces = np.array(self.faces)
        print(f"STL loaded from {filepath}: {len(self.faces)} facets")


    def read_binary(self, file_path):
        """Read a binary STL file."""
        self.vertices = []
        self.faces = []
        vertex_map = {}
        current_vertex_index = 0

        with open(file_path, 'rb') as f:
            f.seek(80)
            num_triangles = struct.unpack('<I', f.read(4))[0]

            for _ in range(num_triangles):
                f.read(12)
                vertex_indices = []
                for _ in range(3):
                    vertex_data = struct.unpack('<fff', f.read(12))  # x, y, z
                    vertex = tuple(vertex_data)
                    if vertex not in vertex_map:
                        vertex_map[vertex] = current_vertex_index
                        self.vertices.append(vertex)
                        current_vertex_index += 1
                    vertex_indices.append(vertex_map[vertex])
                self.faces.append(vertex_indices)
                f.read(2)

    def calculate_normal(self, vertices):
        v0, v1, v2 = vertices
        edge1 = np.array(v1) - np.array(v0)
        edge2 = np.array(v2) - np.array(v0)
        normal = np.cross(edge1, edge2)
        norm = np.linalg.norm(normal)
        return normal / norm if norm != 0 else normal