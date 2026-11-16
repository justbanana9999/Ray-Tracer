from RayTracer import Camera
from MathClasses import Vec3
from Shapes import Scene, Sphere

from time import time

# scene = Scene([Sphere(Vec3(0,3,0),1),Sphere(Vec3(2,3,0),1)])
scene = Scene([Sphere(Vec3(0,-3,0),1)])

cam = Camera(Vec3(0,0,0),Vec3(0,1,0),(500,500),25,scene,0)

tStart = time()

cam.render()

tEnd = time()
print(f'{round(tEnd-tStart,3)} s')