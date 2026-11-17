from RayTracer import Camera
from MathClasses import Vec3
from Shapes import Scene, Sphere, Triangle, Color

from time import perf_counter

scene = Scene(
    [
        Sphere(Vec3(-2,3,0),1,Color(Vec3(1,0,0))),Sphere(Vec3(0,3,0),1,Color(Vec3(0,1,0))),Sphere(Vec3(2,3,0),1,Color(Vec3(0,0,1))),
        Sphere(Vec3(0,20,0),10,Color(emission=Vec3(5,5,5))),
        
        *Triangle.generatePlane(Vec3(0,3,-1),(20,20),'UP'),
        # *Triangle.generatePlane(Vec3(0,3,1),(3,3),'DOWN'),
    ]
    )
# scene = Scene([Sphere(Vec3(0,3,0),1)])

# cam = Camera(Vec3(0,0,0),Vec3(0,1,0),(1920,1080),25,scene,20)

# cam = Camera(Vec3(0,0,0),Vec3(0,1,0),(100,100),25,scene,4)
cam = Camera(Vec3(0,0,0),Vec3(0,1,0),(500,500),25,scene,4,100)

tStart = perf_counter()

cam.render(True)

tEnd = perf_counter()
print(f'{round(tEnd-tStart,3)} s')