from src.Window import GLWindow
from src.Render import GLRenderSystem

from tesselation.cube import Cube
from tesselation.cylinder import Cylinder
from tesselation.sphere import Sphere
from tesselation.pyramid import Pyramid

cube = Cube(
    L=1, origin=[3, 0, 0],
    filepath="stl_figures/cube.stl"
)

sphere = Sphere(
    R=1, origin=[0, 0, 1],
    N=12,
    filepath="stl_figures/sphere.stl"
)

cylinder = Cylinder(
    radius=1.0,  # Base radius
    height=2.0,  # Height
    sectors=32,  # Number of segments
    origin=[-2, 0, 0],  # Position offset
    filepath="output/cylinder.stl"
)


window = GLWindow()
render_system = GLRenderSystem([cube])
window.run(render_system)
