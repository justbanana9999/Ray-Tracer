from RayTracer import Camera
from MathClasses import Vec3
from Shapes import Scene, Sphere, Triangle, Material

scene = Scene(
    [
        Sphere(Vec3(0,3,0),1,Material(roughness=0.5)),
        
        *Triangle.generatePlane(Vec3(0,3,-1),(2,2),Material(diffuse=Vec3(0,1,0))),
        *Triangle.generatePlane(Vec3(0,3,2),(2,2),Material(),'DOWN'),
        *Triangle.generatePlane(Vec3(0,3,1.9),(1,1),Material(emission=Vec3(4,4,4)),'DOWN'),
        *Triangle.generatePlane(Vec3(-2,3,1),(2,2),Material(diffuse=Vec3(1,0,0)),'RIGHT'),
        *Triangle.generatePlane(Vec3(2,3,1),(2,2),Material(diffuse=Vec3(0,0,1)),'LEFT'),
        *Triangle.generatePlane(Vec3(0,5,1),(2,2),Material(diffuse=Vec3(1,0,1)),'BACK'),
        *Triangle.generatePlane(Vec3(0,1,1),(2,2),Material(diffuse=Vec3(1,1,1)),'FRONT'),
    ]
    )

# cam = Camera(Vec3(0,0,0),Vec3(0,3,0),(200,200),25,scene,4,10)

cam = Camera(Vec3(0,0,0),Vec3(0,3,0),(200,200),25,scene,4,100)

cam.render(True)