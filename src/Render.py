# --- Render.py ---
from enum import Enum

import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from OpenGL.raw.GLU import gluPerspective

from src.Camera import Camera

from Parsers.stl import STLParser

class RenderMode(Enum):
    ALL = 0
    FILLED = 1
    WIREFRAME = 2


class GLRenderSystem:
    def __init__(self, shape):
        vertices, faces = shape.tessellate()

        self.vertices = vertices.astype(np.float32)
        self.triangle_indices = faces.flatten().astype(np.uint32)

        self.position = [0.0, 0.0, 0.0]
        self.rotation = [0.0, 0.0, 0.0]

        self.camera = Camera()
        self.render_mode = RenderMode.FILLED
        self.show_axes = True

        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertices)

    def set_render_mode(self, mode):
        """Встановлює режим рендерингу: для прикладу FILLED або WIREFRAME."""
        if isinstance(mode, RenderMode):
            self.render_mode = mode
        else:
            raise ValueError("Невірний режим рендерингу. Використовуйте RenderMode.FILLED або RenderMode.WIREFRAME")

    def toggle_axes(self):
        """Toggle visibility of coordinate axes."""
        self.show_axes = not self.show_axes
        print(f"Coordinate axes: {'visible' if self.show_axes else 'hidden'}")

    def render_axes(self):
        """Render coordinate axes (X: red, Y: green, Z: blue)."""
        glPushMatrix()
        glTranslatef(*self.position)  # Follow the figure's position
        glLineWidth(2.0)  # Thicker lines for visibility

        glBegin(GL_LINES)
        # X-axis (red)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(1.0, 0.0, 0.0)

        # Y-axis (green)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 1.0, 0.0)

        # Z-axis (blue)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 1.0)
        glEnd()

        glLineWidth(1.0)  # Reset line width
        glPopMatrix()

    def create_shader_program(self):
        vertex_shader = """
        #version 330 core
        layout(location = 0) in vec3 aPos;
        layout(location = 1) in vec3 aNormal;
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        out vec3 Normal;
        out vec3 FragPos;
        void main() {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
            FragPos = vec3(model * vec4(aPos, 1.0));
            Normal = mat3(transpose(inverse(model))) * aNormal;
        }
        """
        fragment_shader = """
        #version 330 core
        in vec3 Normal;
        in vec3 FragPos;
        out vec4 FragColor;
        uniform vec3 lightPos;
        uniform vec3 lightColor;
        uniform vec3 objectColor;
        void main() {
            vec3 norm = normalize(Normal);
            vec3 lightDir = normalize(lightPos - FragPos);
            float diff = max(dot(norm, lightDir), 0.0);
            vec3 diffuse = diff * lightColor;
            float ambientStrength = 0.1;
            vec3 ambient = ambientStrength * lightColor;
            vec3 result = (ambient + diffuse) * objectColor;
            FragColor = vec4(result, 1.0);
        }
        """
        vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
        return compileProgram(vertex_shader, fragment_shader)

    def render(self):
        glClearColor(0.2, 0.3, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищення буфера глибини

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, 800 / 600, 0.1, 100.0)

        glMatrixMode(GL_MODELVIEW)
        view_matrix = np.array(self.camera.calc_view_matrix().to_list(), dtype=np.float32)
        glLoadMatrixf(view_matrix)

        glPushMatrix()

        glTranslatef(*self.position)
        glRotatef(self.rotation[0], 1, 0, 0)
        glRotatef(self.rotation[1], 0, 1, 0)
        glRotatef(self.rotation[2], 0, 0, 1)

        glColor3f(0.5, 0.5, 0.5)

        if self.render_mode == RenderMode.FILLED:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)  # Заливка трикутників
        elif self.render_mode == RenderMode.WIREFRAME:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Лише контури
        elif self.render_mode == RenderMode.ALL:
            # First, draw filled triangles
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glColor3f(0.5, 0.5, 0.5)  # Gray for filled
            glDrawElements(GL_TRIANGLES, len(self.triangle_indices), GL_UNSIGNED_INT, self.triangle_indices)

            # Then, draw wireframe overlay
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glColor3f(0.5, 0.0, 0.0)  # Yellow for wireframe
            glEnable(GL_POLYGON_OFFSET_LINE)  # Avoid z-fighting
            glPolygonOffset(-1.0, -1.0)  # Push lines slightly forward
            glDrawElements(GL_TRIANGLES, len(self.triangle_indices), GL_UNSIGNED_INT, self.triangle_indices)
            glDisable(GL_POLYGON_OFFSET_LINE)


        glDrawElements(GL_TRIANGLES, len(self.triangle_indices), GL_UNSIGNED_INT, self.triangle_indices)

        glPopMatrix()

        if self.show_axes:
            self.render_axes()
