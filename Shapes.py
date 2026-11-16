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