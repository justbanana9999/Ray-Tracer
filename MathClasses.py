from math import cos, dist, pi, sin, sqrt
from typing import ClassVar
from random import uniform, random

EPSILON = 0.0000001

class Vec3:
    def __init__(self, x:float, y:float, z:float):
        self.x:float = x
        self.y:float = y
        self.z:float = z
    
    UP:ClassVar['Vec3']
    RIGHT:ClassVar['Vec3']
    FORWARD:ClassVar['Vec3']
    ZERO:ClassVar['Vec3']
    ONE:ClassVar['Vec3']

    def __repr__(self):
        return f'Vec3({str(round(self.x,3)).ljust(6,'0')}, {str(round(self.y,3)).ljust(6,'0')}, {str(round(self.z,3)).ljust(6,'0')})'
    
    def __mul__(self,other:'Vec3|int|float'):
        if isinstance(other,Vec3):
            return Vec3(
                self.x*other.x,
                self.y*other.y,
                self.z*other.z,
                )
        return Vec3(
            self.x*other,
            self.y*other,
            self.z*other,
            )
    
    def __truediv__(self,other:'Vec3|int|float'):
        if isinstance(other,Vec3):
            return Vec3(
                self.x/other.x,
                self.y/other.y,
                self.z/other.z,
                )
        return Vec3(
            self.x/other,
            self.y/other,
            self.z/other,
            )
    
    def __sub__(self,other:'Vec3'):
        return Vec3(
            self.x-other.x,
            self.y-other.y,
            self.z-other.z,
            )
    
    def __add__(self,other:'Vec3'):
        return Vec3(
            self.x+other.x,
            self.y+other.y,
            self.z+other.z,
            )
    
    def __neg__(self):
        return self*-1
    
    def __eq__(self,other:object):
        if isinstance(other,Vec3):
            return (self.x==other.x) and (self.y==other.y) and (self.z==other.z)
        else:
            return False
    
    def __pow__(self,other:int):
        return Vec3(self.x**other,self.y**other,self.z**other)

    def length(self):
        return dist((0,0,0),(self.x,self.y,self.z))
    
    def lengthSquared(self):
        return Vec3.dot(self,self)
    
    def normalized(self):
        return self/self.length()
    
    @staticmethod
    def getNormal(a:'Vec3',b:'Vec3'):
        return (a-b).normalized()
    
    @staticmethod
    def dot(a:'Vec3',b:'Vec3'):
        return a.x*b.x + a.y*b.y + a.z*b.z
    
    @staticmethod
    def cross(a:'Vec3',b:'Vec3'):
        return Vec3(
            a.y*b.z-a.z*b.y,
            a.z*b.x-a.x*b.z,
            a.x*b.y-a.y*b.x,
            )
    
    def toTuple(self):
        return (self.x,self.y,self.z)
    
    def toIntTuple(self):
        return (int(self.x),int(self.y),int(self.z))
    
    def toTupleRounded(self,digits:int):
        return f'({str(round(self.x,digits)).ljust(digits+2,'0')}, {str(round(self.y,digits)).ljust(digits+2,'0')}, {str(round(self.z,digits)).ljust(digits+2,'0')})'
    
    @staticmethod
    def reflect(incoming:'Vec3',normal:'Vec3'):
        return  incoming - normal*2*Vec3.dot(incoming,normal)

    @staticmethod
    def getRelativeAxes(diffVector:'Vec3'):
        if diffVector == 0:
            front = -Vec3.UP
        else:
            front = diffVector.normalized()

        if front == Vec3.UP:
            right = -Vec3.RIGHT
        elif front == -Vec3.UP:
            right = Vec3.RIGHT
        else:
            right = Vec3.cross(front,Vec3.UP)

        up = Vec3.cross(right,front)

        return (front,right,up)

    @staticmethod
    def scatterTowardsNormal(incoming:'Vec3',normal:'Vec3'):
        
        up,right,front = Vec3.getRelativeAxes(normal)

        randomPoint = Vec3.randomVector()

        if randomPoint.length() == 0:
            randomPoint = Vec3.UP

        scatterVector = (normal + right*randomPoint.x+front*randomPoint.y+up*randomPoint.z).normalized()

        return scatterVector
    
    @staticmethod
    def ggx(incoming:'Vec3',normal:'Vec3',roughness:float):
        
        up,right,front = Vec3.getRelativeAxes(normal)
        
        a,b = random(),random()
        phi = 2*pi*a
        cosTheta = sqrt((1-b)/(1+(roughness**4-1)*b))
        sinTheta = sqrt(1-cosTheta**2)

        x = sinTheta*cos(phi)
        y = sinTheta*sin(phi)
        z = cosTheta

        worldNormal = (right*x+front*y+up*z).normalized()

        reflected = Vec3.reflect(incoming,worldNormal).normalized()

        # D = (roughness**4)/(pi*(Vec3.dot(normal,worldNormal)**2*(roughness**4-1)+1)**2)

        # p = (D*Vec3.dot(normal,worldNormal))/(4*Vec3.dot(incoming,worldNormal))

        G_V = (2*Vec3.dot(normal,incoming))/(Vec3.dot(normal,incoming)+sqrt(roughness**4+(1-roughness**4)*(Vec3.dot(normal,incoming))**2))
        G_L = (2*Vec3.dot(normal,reflected))/(Vec3.dot(normal,reflected)+sqrt(roughness**4+(1-roughness**4)*(Vec3.dot(normal,reflected))**2))

        G = G_V*G_L

        F = Vec3(0.8,0.8,0.8)+(Vec3.ONE-Vec3(0.8,0.8,0.8))*(1-(Vec3.dot(incoming,worldNormal))**5)

        weight = (F*G*Vec3.dot(incoming,worldNormal))/(Vec3.dot(normal,incoming)*Vec3.dot(normal,worldNormal))

        return reflected,weight

    @staticmethod
    def vectorSum(vectorList:list['Vec3']):
        s = Vec3.ZERO
        for l in vectorList:
            s += l
        return s

    @staticmethod
    def average(vectorList:list['Vec3']):
        return Vec3.vectorSum(vectorList)/len(vectorList)
    
    @staticmethod
    def randomVector():
        return Vec3(uniform(-1,1),uniform(-1,1),uniform(-1,1)).normalized()
    
    @staticmethod
    def interpolate(a:'Vec3',b:'Vec3',w:float):
        return a+(b-a)*w
    
    '''
    @MISC {13263,
        TITLE = {How to get a reflection vector?},
        AUTHOR = {Phrogz (https://math.stackexchange.com/users/4241/phrogz)},
        HOWPUBLISHED = {Mathematics Stack Exchange},
        NOTE = {URL:https://math.stackexchange.com/q/13263 (version: 2010-12-06)},
        EPRINT = {https://math.stackexchange.com/q/13263},
        URL = {https://math.stackexchange.com/q/13263}
    }
    '''
    
Vec3.UP         = Vec3(0,0,1)
Vec3.RIGHT      = Vec3(1,0,0)
Vec3.FORWARD    = Vec3(0,1,0)
Vec3.ZERO       = Vec3(0,0,0)
Vec3.ONE        = Vec3(1,1,1)