import argparse

from tesselation.cube import Cube
from tesselation.split import Split
from tesselation.sphere import Sphere
from app import Application


parser = argparse.ArgumentParser(description="Mesh Editor for Lab 0")
parser.add_argument("command", choices=["Cube", "Sphere", "Split"], help="Command to execute")
parser.add_argument("--L", type=float, help="Side length for Cube")
parser.add_argument("--R", type=float, help="Radius for Sphere")
parser.add_argument("--N", type=int, default=4, help="Tessellation level for Sphere")
parser.add_argument("--origin", type=lambda s: [float(x) for x in s.split(",")], help="Origin in format x,y,z")
parser.add_argument("--filepath", type=str, help="Path to output STL file")
parser.add_argument("--input", type=str, help="Input STL file for Split")
args = parser.parse_args()

app = Application()
app.register_command("Cube", lambda **kwargs: Cube(kwargs["L"], kwargs["origin"], kwargs["filepath"]))
app.register_command("Sphere", lambda **kwargs: Sphere(kwargs["R"], kwargs["origin"], kwargs["N"], kwargs["filepath"]))
app.register_command("Split", lambda **kwargs: Split(kwargs["input"], kwargs["filepath"]))

if args.command == "Cube":
    app.execute("Cube", L=args.L, origin=args.origin, filepath=args.filepath)
elif args.command == "Sphere":
    app.execute("Sphere", R=args.R, origin=args.origin, N=args.N, filepath=args.filepath)
elif args.command == "Split":
    app.execute("Split", input=args.input, filepath=args.filepath)
