from RayTracer import Camera
from MathClasses import Vec3
from Shapes import Scene, Sphere, Triangle, Color

scene = Scene(
    [
        Sphere(Vec3(0,3,0),1,Color(Vec3(1,0,0))),
        Sphere(Vec3(0,20,0),10,Color(emission=Vec3(1,1,1))),
        
        *Triangle.generatePlane(Vec3(0,3,-1),(3,3),'UP'),
    ]
    )

cam = Camera(Vec3(-4,2,0),Vec3(0,3,0),(500,500),25,scene,4,10)

cam.render(True)