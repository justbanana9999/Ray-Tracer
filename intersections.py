from math import sqrt

from MathClasses import Vec3
from Shapes import Ray, Sphere, Triangle

def raySphereIntersection(ray:Ray,sphere:Sphere) -> tuple[bool, Vec3, Vec3]:
    c = sphere.center
    r = sphere.radius
    o = ray.origin
    u = ray.direction.normalized()

    nabla = (Vec3.dot(u,o-c))**2 - (o-c).lengthSquared() + r**2
    if nabla == 0:
        d = -Vec3.dot(u,o-c)
        hitPoint = o+u*d
        normal = Vec3.getNormal(hitPoint,c)
        if d >= 0:
            return True,hitPoint,normal
        else:
            return False,Vec3.ZERO,Vec3.ZERO
    elif nabla > 0:
        d = -Vec3.dot(u,o-c) - sqrt(nabla)
        # dFurthest = -Vec3.dot(u,o-c) + sqrt(nabla)
        hitPoint = o+u*d
        normal = Vec3.getNormal(hitPoint,c)
        if d >= 0:
            return True,hitPoint,normal
        else:
            return False,Vec3.ZERO,Vec3.ZERO

    else:
        return False,Vec3.ZERO,Vec3.ZERO

def rayTriangleIntersection(ray:Ray,triangle:Triangle) -> tuple[bool, Vec3, Vec3]:
    p0,p1,p2 = triangle.p0,triangle.p1,triangle.p2

    e1 = p1-p0
    e2 = p2-p0
    h = Vec3.cross(ray.direction,e2)
    a = Vec3.dot(e1,h)

    return False,Vec3.ZERO,Vec3.ZERO

'''
https://en.wikipedia.org/wiki/M%C3%B6ller%E2%80%93Trumbore_intersection_algorithm
'''