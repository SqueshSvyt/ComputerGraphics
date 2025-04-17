# --- Camera.py ---
import glm
import math


class Camera:
    def __init__(self, eye=glm.vec3(0, 0, 5), target=glm.vec3(0, 0, 0), up=glm.vec3(0, 1, 0)):
        self.eye = eye
        self.target = target
        self.up = up

    def calc_view_matrix(self):
        return glm.lookAt(self.eye, self.target, self.up)

    def move(self, direction: glm.vec3):
        self.eye += direction
        self.target += direction

    def zoom(self, factor):
        direction = glm.normalize(self.target - self.eye)
        self.eye += direction * factor

    def orbit(self, angle_x, angle_y):
        radius = glm.distance(self.eye, self.target)
        theta = math.atan2(self.eye.z - self.target.z, self.eye.x - self.target.x)
        phi = math.acos((self.eye.y - self.target.y) / radius)

        theta += glm.radians(angle_x)
        phi += glm.radians(angle_y)
        phi = glm.clamp(phi, 0.01, math.pi - 0.01)

        x = radius * math.sin(phi) * math.cos(theta)
        y = radius * math.cos(phi)
        z = radius * math.sin(phi) * math.sin(theta)

        self.eye = self.target + glm.vec3(x, y, z)

    def pan(self, dx, dy):
        right = glm.normalize(glm.cross(self.target - self.eye, self.up))
        up = glm.normalize(self.up)

        self.eye += right * dx + up * dy
        self.target += right * dx + up * dy