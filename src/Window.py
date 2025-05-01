# --- Window.py ---
import glfw
from OpenGL.GL import *

from src.Mode_Controller import ModeController
from src.Mode_Controller import ControlMode
from src.Render import RenderMode


class GLWindow:
    def __init__(self, width=800, height=600, title="Lab 1: OpenGL Window"):
        if not glfw.init():
            raise Exception("Failed to initialize GLFW")

        self.window = glfw.create_window(width, height, title, None, None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create GLFW window")

        glfw.make_context_current(self.window)

        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        glfw.set_cursor_pos_callback(self.window, self.cursor_pos_callback)
        glfw.set_scroll_callback(self.window, self.scroll_callback)

        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)
        self.running = True
        self.render_system = None
        self.mode_controller = ModeController()

        self.last_x = 0
        self.last_y = 0
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.middle_mouse_pressed = False

        self.move_sensitivity = 0.05

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            self.running = False
            glfw.set_window_should_close(window, True)

        elif key == glfw.KEY_M and action == glfw.PRESS:
            if self.render_system:
                current_mode = self.render_system.render_mode
                if current_mode == RenderMode.FILLED:
                    new_mode = RenderMode.WIREFRAME
                elif current_mode == RenderMode.WIREFRAME:
                    new_mode = RenderMode.ALL
                else:
                    new_mode = RenderMode.FILLED
                self.render_system.set_render_mode(new_mode)
                print(f"Switched to render mode: {new_mode}")

        elif key == glfw.KEY_TAB and action == glfw.PRESS:
            self.mode_controller.toggle_mode()

        elif key == glfw.KEY_RIGHT and action == glfw.PRESS:
            if self.render_system:
                self.mode_controller.select_next_shape(len(self.render_system.shapes))

        elif key == glfw.KEY_LEFT and action == glfw.PRESS:
            if self.render_system:
                self.mode_controller.select_previous_shape(len(self.render_system.shapes))

        elif key == glfw.KEY_UP and action == glfw.PRESS:
            if self.render_system and self.mode_controller.is_triangle_mode():
                shape_index = self.mode_controller.selected_shape_index
                if 0 <= shape_index < len(self.render_system.shapes):
                    vertex_count = len(self.render_system.shapes[shape_index].vertices)
                    vertex_index, shape_index = self.mode_controller.select_next_vertex(vertex_count)
                    self.render_system.set_vertex_index(shape_index, vertex_index)
                    print(f"Selected vertex: {self.mode_controller.selected_vertex_index}")

        elif key == glfw.KEY_DOWN and action == glfw.PRESS:
            if self.render_system and self.mode_controller.is_triangle_mode():
                shape_index = self.mode_controller.selected_shape_index
                if 0 <= shape_index < len(self.render_system.shapes):
                    vertex_count = len(self.render_system.shapes[shape_index].vertices)
                    vertex_index, shape_index = self.mode_controller.select_previous_vertex(vertex_count)
                    self.render_system.set_vertex_index(shape_index, vertex_index)
                    print(f"Selected vertex: {self.mode_controller.selected_vertex_index}")

        elif key == glfw.KEY_D and action == glfw.PRESS:
            if self.render_system and self.mode_controller.is_triangle_mode():
                shape_index = self.mode_controller.selected_shape_index
                vertex_index = self.mode_controller.selected_vertex_index
                if 0 <= shape_index < len(self.render_system.shapes):
                    try:
                        self.render_system.delete_vertex(shape_index, vertex_index)
                        print(f"Deleted vertex {vertex_index} from shape {shape_index}")
                        # Reset vertex index if necessary
                        vertex_count = len(self.render_system.shapes[shape_index].vertices)
                        if self.mode_controller.selected_vertex_index >= vertex_count:
                            self.mode_controller.selected_vertex_index = max(0, vertex_count - 1)
                    except ValueError as e:
                        print(f"Error deleting vertex: {e}")

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            self.left_mouse_pressed = (action == glfw.PRESS)
        elif button == glfw.MOUSE_BUTTON_RIGHT:
            self.right_mouse_pressed = (action == glfw.PRESS)
        elif button == glfw.MOUSE_BUTTON_MIDDLE:
            self.middle_mouse_pressed = (action == glfw.PRESS)

    def cursor_pos_callback(self, window, xpos, ypos):
        dx = xpos - self.last_x
        dy = ypos - self.last_y
        self.last_x = xpos
        self.last_y = ypos

        if self.render_system is None:
            return

        # Camera controls (unchanged)
        cam = self.render_system.camera

        if self.mode_controller.is_triangle_mode():
            shape_index = self.mode_controller.selected_shape_index
            vertex_index = self.mode_controller.selected_vertex_index
            if 0 <= shape_index < len(self.render_system.shapes):
                shape = self.render_system.shapes[shape_index]
                if vertex_index < len(shape.vertices):
                    current_pos = shape.vertices[vertex_index].copy()
                    if self.left_mouse_pressed:
                        current_pos[0] += dx * self.move_sensitivity
                        current_pos[1] -= dy * self.move_sensitivity
                        self.render_system.move_vertex(shape_index, vertex_index, current_pos)
                        print(f"[Vertex] Moved vertex {vertex_index} of shape {shape_index} to {current_pos}")
                    elif self.right_mouse_pressed:
                        current_pos[2] -= dy * self.move_sensitivity
                        self.render_system.move_vertex(shape_index, vertex_index, current_pos)
                        print(f"[Vertex] Moved vertex {vertex_index} of shape {shape_index} to {current_pos}")

        elif self.mode_controller.is_shape_mode():
            index = self.mode_controller.selected_shape_index
            if 0 <= index < len(self.render_system.shapes):
                shape = self.render_system.shapes[index]

                if self.left_mouse_pressed:
                    shape.position[0] += dx * self.move_sensitivity
                    shape.position[1] -= dy * self.move_sensitivity
                    print(f"[Shape] Moved shape {index} to {shape.position}")
                elif self.right_mouse_pressed:
                    shape.position[2] -= dy * self.move_sensitivity
                elif self.middle_mouse_pressed:
                    shape.rotation[1] += dx * 0.5
                    shape.rotation[0] += dy * 0.5
                    print(f"[Shape] Rotated shape {index} to {shape.rotation}")


            # 🎥 CAMERA mode: move camera with left/right mouse
        else:
            if self.left_mouse_pressed:
                cam.pan(-dx * self.move_sensitivity, dy * self.move_sensitivity)
            elif self.right_mouse_pressed:
                cam.orbit(-dx * 0.5, -dy * 0.5)

    def scroll_callback(self, window, xoffset, yoffset):
        if self.render_system:
            self.render_system.camera.zoom(-yoffset * 0.5)

    def run(self, render_system):
        self.render_system = render_system
        while self.running and not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            render_system.render()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()
