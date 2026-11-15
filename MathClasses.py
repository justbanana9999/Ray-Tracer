from math import dist
from typing import ClassVar

class Vec3:
    def __init__(self, x:float, y:float, z:float):
        self.x:float = x
        self.y:float = y
        self.z:float = z
    
    UP:ClassVar[Vec3]
    RIGHT:ClassVar[Vec3]
    ZERO:ClassVar[Vec3]
    ONE:ClassVar[Vec3]

    def __repr__(self):
        return f'Vec3({self.x}, {self.y}, {self.z})'
    
    def __mul__(self,other:Vec3|int|float):
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
    
    def __truediv__(self,other:Vec3|int|float):
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
    
    def __sub__(self,other:Vec3):
        return Vec3(
            self.x-other.x,
            self.y-other.y,
            self.z-other.z,
            )
    
    def __add__(self,other:Vec3):
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
    
    def normalized(self):
        return self/self.length()
    
    @staticmethod
    def dot(a:Vec3,b:Vec3):
        return a.x*b.x + a.y*b.y + a.z*b.z
    
    @staticmethod
    def cross(a:Vec3,b:Vec3):
        return Vec3(
            a.y*b.z-a.z*b.y,
            a.z*b.x-a.x*b.z,
            a.x*b.y-a.y*b.x,
            )
    
Vec3.UP     = Vec3(0,0,1)
Vec3.RIGHT  = Vec3(0,0,1)
Vec3.ZERO   = Vec3(0,0,0)
Vec3.ONE    = Vec3(1,1,1)