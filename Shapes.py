from MathClasses import Vec3

class Ray:
    def __init__(self,origin:Vec3,vector:Vec3):
        self.origin = origin
        self.vector = vector
    def __repr__(self):
        return f'ori = {self.origin}, vec = {self.vector}'

class Scene:
    def __init__(self,shapeList:list['Sphere|Triangle']):
        self.shapeList = shapeList

class Sphere:
    def __init__(self,center:Vec3,radius:float):
        self.center = center
        self.radius = radius

class Triangle:
    def __init__(self,a:Vec3,b:Vec3,c:Vec3):
        self.a = a
        self.b = b
        self.c = c

        self.normal:Vec3
        self.generateNormal()
    
    def __repr__(self):
        return f' a = {self.a}, b = {self.b}, c = {self.c}'

    def generateNormal(self):
        e1 = (self.b-self.a).normalized()
        e2 = (self.c-self.a).normalized()
        self.normal = Vec3.cross(e1,e2)
    
    @staticmethod
    def generatePlane(center:Vec3,size:tuple[float,float],orientation:str='UP'):
        if orientation == 'UP':
            return [
                Triangle(
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    Vec3(center.x-size[0],center.y-size[1],center.z),
                ),
                Triangle(
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    Vec3(center.x+size[0],center.y+size[1],center.z),
                ),
            ]
        elif orientation == 'DOWN':
            return [
                Triangle(
                    Vec3(center.x-size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                ),
                Triangle(
                    Vec3(center.x+size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                ),
            ]
        else:
            return [
                Triangle(
                    Vec3(center.x-size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                ),
                Triangle(
                    Vec3(center.x+size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                ),
            ]