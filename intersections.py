from math import sqrt

from MathClasses import Vec3, EPSILON
from Shapes import Ray, Sphere, Triangle

def raySphereIntersection(ray:Ray,sphere:Sphere) -> tuple[bool, Vec3, Vec3]:

    emptyReturn = (False,Vec3.ZERO,Vec3.ZERO)

    c = sphere.center
    r = sphere.radius
    o = ray.origin
    u = ray.vector.normalized()

    nabla = (Vec3.dot(u,o-c))**2 - (o-c).lengthSquared() + r**2
    if nabla == 0:
        d = -Vec3.dot(u,o-c)
        hitPoint = o+u*d
        normal = Vec3.getNormal(hitPoint,c)
        if d >= 0:
            return True,hitPoint,normal
        else:
            return emptyReturn
    elif nabla > 0:
        d = -Vec3.dot(u,o-c) - sqrt(nabla)
        # dFurthest = -Vec3.dot(u,o-c) + sqrt(nabla)
        hitPoint = o+u*d
        normal = Vec3.getNormal(hitPoint,c)
        if d >= 0:
            return True,hitPoint,normal
        else:
            return emptyReturn

    else:
        return emptyReturn

def rayTriangleIntersection(ray:Ray,triangle:Triangle) -> tuple[bool, Vec3, Vec3]:

    emptyReturn = (False,Vec3.ZERO,Vec3.ZERO)

    e1 = triangle.b-triangle.a
    e2 = triangle.c-triangle.a    

    normal = triangle.normal
    if Vec3.dot(normal,ray.vector) > 0:
        return emptyReturn
    
    rayCross_e2 = Vec3.cross(ray.vector,e2)
    det = Vec3.dot(e1,rayCross_e2)

    if abs(det) < EPSILON:
        return emptyReturn
    
    invDet = 1 / det
    s = ray.origin - triangle.a
    u = invDet * Vec3.dot(s,rayCross_e2)

    if (u < -EPSILON) or (u - 1 > EPSILON):
        return emptyReturn

    sCross_e1 = Vec3.cross(s,e1)
    v = invDet * Vec3.dot(ray.vector,sCross_e1)

    if (v < -EPSILON) or (u + v - 1 > EPSILON):
        return emptyReturn
    
    t = invDet * Vec3.dot(e2,sCross_e1)

    if t > EPSILON:
        return True,ray.origin+ray.vector * t,normal
    else:
        return emptyReturn

'''
https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm

Copied and translated the C++ implementation

'''