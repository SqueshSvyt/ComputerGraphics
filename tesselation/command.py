import numpy as np

from Parsers.stl import STLParser


class Shape:
    def __init__(self, filepath):
        self.filepath = filepath
        self.origin = None

    def execute(self):
        raise NotImplementedError("Subclasses should implement this!")

    def save_stl(self, vertices, faces):
        parser = STLParser()
        parser.write(self.filepath, vertices, faces)
        print(f"STL saved to {self.filepath}")

    def tessellate(self):
        return NotImplementedError("Subclasses should implement this!")