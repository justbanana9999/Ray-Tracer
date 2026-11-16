from math import sqrt

from MathClasses import Vec3
from Shapes import Ray, Sphere


def raySphereIntersection(ray:Ray,sphere:Sphere) -> tuple[bool, Vec3,Vec3]:
    c = sphere.center
    r = sphere.radius
    o = ray.origin
    u = ray.direction.normalized()

    nabla = (Vec3.dot(u,o-c))**2 - (o-c).lengthSquared() + r**2
    if nabla == 0:
        d = -Vec3.dot(u,o-c)
        hitPoint = o+u*d
        normal = Vec3.getNormal(hitPoint,c)
        return True,hitPoint,normal
    elif nabla > 0:
        d = -Vec3.dot(u,o-c) - sqrt(nabla)
        # dFurthest = -Vec3.dot(u,o-c) + sqrt(nabla)
        hitPoint = o+u*d
        normal = Vec3.getNormal(hitPoint,c)
        return True,hitPoint,normal
    else:
        return False,Vec3.ZERO,Vec3.ZERO