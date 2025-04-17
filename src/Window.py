# --- Window.py ---
import glfw
from OpenGL.GL import *

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

        self.last_x = 0
        self.last_y = 0
        self.left_mouse_pressed = False
        self.right_mouse_pressed = False
        self.middle_mouse_pressed = False

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

        # Middle mouse drag: Move the figure
        if self.middle_mouse_pressed:
            move_sensitivity = 0.01  # Adjust for faster/slower movement
            position = self.render_system.position
            position[0] += dx * move_sensitivity  # Mouse X -> World X
            position[1] -= dy * move_sensitivity  # Mouse Y -> World Y (inverted for intuitive drag)
            self.render_system.position = position
            print(f"New position (mouse): {position}")  # For debugging

        # Camera controls (unchanged)
        cam = self.render_system.camera
        sensitivity = 0.005
        if self.left_mouse_pressed:
            cam.pan(-dx * sensitivity, dy * sensitivity)
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
