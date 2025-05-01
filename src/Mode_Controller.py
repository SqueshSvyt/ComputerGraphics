from enum import Enum, auto


class ControlMode(Enum):
    CAMERA = auto()
    SHAPE = auto()
    TRIANGLE = auto()


class ModeController:
    def __init__(self):
        self.mode = ControlMode.CAMERA
        self.selected_shape_index = 0
        self.selected_vertex_index = 0

    def toggle_mode(self):
        """Cycle through CAMERA, SHAPE, and TRIANGLE modes."""
        if self.mode == ControlMode.CAMERA:
            self.mode = ControlMode.SHAPE
        elif self.mode == ControlMode.SHAPE:
            self.mode = ControlMode.TRIANGLE
        else:
            self.mode = ControlMode.CAMERA
        print(f"Switched to: {self.mode.name}")

    def select_next_shape(self, shape_count):
        if shape_count == 0:
            return
        self.selected_shape_index = (self.selected_shape_index + 1) % shape_count
        self.selected_triangle_index = 0  # Reset triangle index when switching shapes
        print(f"Selected shape index: {self.selected_shape_index}")

    def select_previous_shape(self, shape_count):
        if shape_count == 0:
            return
        self.selected_shape_index = (self.selected_shape_index - 1) % shape_count
        self.selected_triangle_index = 0  # Reset triangle index when switching shapes
        print(f"Selected shape index: {self.selected_shape_index}")

    def select_next_triangle(self, triangle_count):
        if triangle_count == 0:
            return
        self.selected_triangle_index = (self.selected_triangle_index + 1) % triangle_count
        print(f"Selected triangle index: {self.selected_triangle_index}")

    def select_previous_triangle(self, triangle_count):
        if triangle_count == 0:
            return
        self.selected_triangle_index = (self.selected_triangle_index - 1) % triangle_count
        print(f"Selected triangle index: {self.selected_triangle_index}")

    def select_next_vertex(self, vertex_count):
        self.selected_vertex_index = (self.selected_vertex_index + 1) % max(1, vertex_count)

        return self.selected_vertex_index, self.selected_shape_index

    def select_previous_vertex(self, vertex_count):
        self.selected_vertex_index = (self.selected_vertex_index - 1) % max(1, vertex_count)

        return self.selected_vertex_index, self.selected_shape_index

    def is_camera_mode(self):
        return self.mode == ControlMode.CAMERA

    def is_shape_mode(self):
        return self.mode == ControlMode.SHAPE

    def is_triangle_mode(self):
        return self.mode == ControlMode.TRIANGLE