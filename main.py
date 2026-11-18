from RayTracer import Camera
from MathClasses import Vec3
from Shapes import Scene, Sphere, Triangle, Material

print(Triangle.generatePlane(Vec3(2,1,1),(2,2),Material(diffuse=Vec3(1,1,1)),'FRONT')[0].normal,
Triangle.generatePlane(Vec3(2,1,1),(2,2),Material(diffuse=Vec3(1,1,1)),'FRONT')[1].normal)

scene = Scene(
    [
        Sphere(Vec3(0,3,0),1,Material(roughness=0.3)),
        
        *Triangle.generatePlane(Vec3(0,3,-1),(2,2),Material(diffuse=Vec3(0,1,0))),
        *Triangle.generatePlane(Vec3(0,3,2),(2,2),Material(emission=Vec3(1,1,1)),'DOWN'),
        *Triangle.generatePlane(Vec3(-2,3,1),(2,2),Material(diffuse=Vec3(1,0,0)),'RIGHT'),
        *Triangle.generatePlane(Vec3(2,3,1),(2,2),Material(diffuse=Vec3(0,0,1)),'LEFT'),
        *Triangle.generatePlane(Vec3(0,5,1),(2,2),Material(diffuse=Vec3(0.1,0.1,0.1)),'BACK'),
        *Triangle.generatePlane(Vec3(0,1,1),(2,2),Material(diffuse=Vec3(1,1,1)),'FRONT'),
    ]
    )

cam = Camera(Vec3(0,0,0),Vec3(0,3,0),(200,200),25,scene,4,10)

cam.render(True)