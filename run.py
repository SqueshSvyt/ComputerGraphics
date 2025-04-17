from src.Window import GLWindow
from src.Render import GLRenderSystem

from tesselation.cube import Cube
from tesselation.sphere import Sphere

shape1 = Cube(L=2, origin=[0, 0, 0], filepath="stl_figures/cube.stl")
shape2 = Sphere(R=2, origin=[0, 0, 0], N=8, filepath="stl_figures/sphere.stl")

window = GLWindow()
render_system = GLRenderSystem(shape2)
window.run(render_system)
