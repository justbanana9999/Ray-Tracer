from MathClasses import Vec3

class Ray:
    def __init__(self,origin:Vec3,vector:Vec3):
        self.origin = origin
        self.vector = vector
        self.color = Vec3.ONE
        self.incoming = Vec3.ZERO
    def __repr__(self):
        return f'ori = {self.origin}, vec = {self.vector}'

class Material:
    def __init__(self,diffuse:Vec3=Vec3.ONE,roughness:float=1,emission:Vec3=Vec3.ZERO):
        self.diffuse = diffuse
        self.roughness = roughness
        self.emission = emission

class Sphere:
    def __init__(self,center:Vec3,radius:float,material:Material=Material(Vec3.ONE*0.95)):
        self.center = center
        self.radius = radius
        self.color = material

class Triangle:
    def __init__(self,a:Vec3,b:Vec3,c:Vec3,material:Material=Material(Vec3.ONE*0.95)):
        self.a = a
        self.b = b
        self.c = c

        self.normal:Vec3
        self.generateNormal()

        self.color = material
    
    def __repr__(self):
        return f' a = {self.a}, b = {self.b}, c = {self.c}'

    def generateNormal(self):
        e1 = (self.b-self.a)
        e2 = (self.c-self.a)
        self.normal = Vec3.cross(e1,e2).normalized()
    
    @staticmethod
    def generatePlane(center:Vec3,size:tuple[float,float],material:Material=Material(),orientation:str='UP'):
        if orientation == 'UP':
            return [
                Triangle(
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    Vec3(center.x-size[0],center.y-size[1],center.z),
                    material,
                ),
                Triangle(
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    Vec3(center.x+size[0],center.y+size[1],center.z),
                    material,
                ),
            ]
        elif orientation == 'DOWN':
            return [
                Triangle(
                    Vec3(center.x-size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    material,
                ),
                Triangle(
                    Vec3(center.x+size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    material,
                ),
            ]
        else:
            return [
                Triangle(
                    Vec3(center.x-size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    material,
                ),
                Triangle(
                    Vec3(center.x+size[0],center.y+size[1],center.z),
                    Vec3(center.x+size[0],center.y-size[1],center.z),
                    Vec3(center.x-size[0],center.y+size[1],center.z),
                    material,
                ),
            ]

# class Shape:
#     def __init__(self,shape:Sphere|Triangle,color:Vec3):
#         self.shape = shape
#         self.color = color

class Scene:
    def __init__(self,shapeList:list[Sphere|Triangle]):
        self.shapeList = shapeList