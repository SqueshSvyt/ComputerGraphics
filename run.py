import numpy as np
import glfw
from OpenGL.GL import *
from app import Application

from tesselation.cube import Cube
from tesselation.split import Split
from tesselation.sphere import Sphere


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

        glViewport(0, 0, width, height)
        glEnable(GL_DEPTH_TEST)  # Тест глибини для 3D
        self.running = True
        self.render_system = None

    def key_callback(self, window, key, scancode, action, mods):
        """Обробка клавіш"""
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            self.running = False
            glfw.set_window_should_close(window, True)

        if self.render_system and (action == glfw.PRESS or action == glfw.REPEAT):
            if key == glfw.KEY_W:
                self.render_system.transform(dx=0, dy=0.1, dz=0)  # Вгору по Y
            elif key == glfw.KEY_S:
                self.render_system.transform(dx=0, dy=-0.1, dz=0)  # Вниз по Y
            elif key == glfw.KEY_A:
                self.render_system.transform(dx=-0.1, dy=0, dz=0)  # Вліво по X
            elif key == glfw.KEY_D:
                self.render_system.transform(dx=0.1, dy=0, dz=0)  # Вправо по X
            elif key == glfw.KEY_Q:
                self.render_system.transform(dx=0, dy=0, dz=0.1)  # Углиб по Z
            elif key == glfw.KEY_E:
                self.render_system.transform(dx=0, dy=0, dz=-0.1)  # Назад по Z
            elif key == glfw.KEY_I:
                self.render_system.transform(rx=5)  # Обертання навколо X (вгору)
            elif key == glfw.KEY_K:
                self.render_system.transform(rx=-5)  # Обертання навколо X (вниз)
            elif key == glfw.KEY_J:
                self.render_system.transform(ry=5)  # Обертання навколо Y (вліво)
            elif key == glfw.KEY_L:
                self.render_system.transform(ry=-5)  # Обертання навколо Y (вправо)
            elif key == glfw.KEY_U:
                self.render_system.transform(rz=5)  # Обертання навколо Z (за годинниковою)
            elif key == glfw.KEY_O:
                self.render_system.transform(rz=-5)  # Обертання навколо Z (проти годинникової)
        print(f"Key pressed: {key}, Action: {action}")

    def mouse_button_callback(self, window, button, action, mods):
        print(f"Mouse button: {button}, Action: {action}")

    def cursor_pos_callback(self, window, xpos, ypos):
        print(f"Mouse position: ({xpos}, {ypos})")

    def run(self, render_system):
        """Основний цикл рендерингу"""
        self.render_system = render_system
        while self.running and not glfw.window_should_close(self.window):
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            render_system.render()
            glfw.swap_buffers(self.window)
            glfw.poll_events()
        glfw.terminate()


class GLRenderSystem:
    def __init__(self):
        shape = Cube(L=0.5, origin=[0, 0, 0], filepath="cube.stl")
        #shape = Sphere(R=10, origin=[0, 0, 0], N=7, filepath="sphere.stl")
        vertices, faces = shape.tessellate()

        self.vertices = vertices.astype(np.float32)
        self.triangle_indices = faces.flatten().astype(np.uint32)

        self.line_indices = np.array([
            0, 1, 1, 2, 2, 3, 3, 0,  # Передня грань
            4, 5, 5, 6, 6, 7, 7, 4,  # Задня грань
            0, 4, 1, 5, 2, 6, 3, 7  # З’єднання передньої та задньої граней
        ], dtype=np.uint32)

        self.position = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]

        # Налаштування буфера вершин
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)

    def transform(self, dx=0, dy=0, dz=0, rx=0, ry=0, rz=0):
        """Зміна позиції та обертання куба"""
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz
        self.rotation[0] += rx
        self.rotation[1] += ry
        self.rotation[2] += rz
        print(f"Cube position: {self.position}, Rotation: {self.rotation}")

    def move(self, dx, dy, dz):
        """Зміна позиції куба"""
        self.position[0] += dx
        self.position[1] += dy
        self.position[2] += dz
        print(f"Cube position: {self.position}")

    def render(self):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glPushMatrix()

        # Застосовуємо переміщення
        glTranslatef(self.position[0], self.position[1], self.position[2])

        # Застосовуємо обертання
        glRotatef(self.rotation[0], 1, 0, 0)  # Навколо X
        glRotatef(self.rotation[1], 0, 1, 0)  # Навколо Y
        glRotatef(self.rotation[2], 0, 0, 1)  # Навколо Z

        # Рендеринг трикутників
        glColor3f(0.5, 0.5, 0.5)
        glDrawElements(GL_TRIANGLES, len(self.triangle_indices), GL_UNSIGNED_INT, self.triangle_indices)

        # Рендеринг країв
        glColor3f(1.0, 0.0, 0.0)
        glLineWidth(2.0)
        glDrawElements(GL_LINES, len(self.line_indices), GL_UNSIGNED_INT, self.line_indices)

        glPopMatrix()



window = GLWindow()
render_system = GLRenderSystem()
window.run(render_system)
