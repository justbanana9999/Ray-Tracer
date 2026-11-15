from RayTracer import Camera
from MathClasses import Vec3

cam = Camera(Vec3(0,0,0),Vec3(-1,-1,-1),(500,500),25)

cam.render()