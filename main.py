from RayTracer import Camera
from MathClasses import Vec3
from Shapes import Scene, Sphere, Triangle

from time import time

scene = Scene(
    [
        Sphere(Vec3(0,3,0),1),Sphere(Vec3(2,3,0),1),Sphere(Vec3(-2,3,0),1),
        # Triangle(Vec3(3,0,-1),Vec3(-3,6,-1),Vec3(-3,0,-1)),Triangle(Vec3(3,6,-1),Vec3(-3,6,-1),Vec3(3,0,-1)),
        *Triangle.generatePlane(Vec3(0,3,-1),(3,3),'UP'),
        *Triangle.generatePlane(Vec3(0,3,1),(3,3),'DOWN'),
    ]
    )
# scene = Scene([Sphere(Vec3(0,3,0),1)])

cam = Camera(Vec3(0,0,0),Vec3(0,1,0),(500,500),25,scene,10)
# cam = Camera(Vec3(0,0,0),Vec3(0,1,0),(10,10),25,scene,4)

tStart = time()

cam.render()

tEnd = time()
print(f'{round(tEnd-tStart,3)} s')