from math import dist
from typing import ClassVar
from random import uniform

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