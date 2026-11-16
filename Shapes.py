from MathClasses import Vec3

class Ray:
    def __init__(self,origin:Vec3,direction:Vec3):
        self.origin = origin
        self.direction = direction

class Scene:
    def __init__(self,shapeList:list['Sphere']):
        self.shapeList = shapeList

class Sphere:
    def __init__(self,center:Vec3,radius:float):
        self.center = center
        self.radius = radius

class Triangle:
    def __init__(self,p0:Vec3,p1:Vec3,p2:Vec3):
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

        self.normal:Vec3
        self.generateNormal()

    def generateNormal(self):
        a1 = (self.p0-self.p1).normalized()
        a2 = (self.p0-self.p2).normalized()
        self.normal = Vec3.cross(a1,a2)