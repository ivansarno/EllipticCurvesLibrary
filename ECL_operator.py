__author__ = 'ivansarno'
#
# deprecate
# These functions have been replaced by overloaded operators
# may not be supported in the next release

from ECL_class import *


def duplication(point):
    """duplication of point of elliptic curve"""
    if point.infinite:
        return point
    elif point.y == 0:
        point.infinite = True
        return point
    else:
        lam = ((3 * point.x ** 2 + point.curve.a) * inverse(2 * point.y, point.curve.prime)) % point.curve.prime
        newx = ((lam ** 2)-point.x-point.x) % point.curve.prime
        newy = (lam * (point.x-newx) - point.y) % point.curve.prime
        p = Point(point.curve, newx, newy)
        return p


def addition(a, b):
    """sum of point of elliptic curve"""
    if a.infinite:
        return b
    elif b.infinite:
        return a
    elif same_point(a, b):
        return duplication(a)
    elif are_opposites(a, b):
        a.infinite = True
        return a
    else:
        lam = ((b.y-a.y) * inverse(b.x-a.x, a.curve.prime)) % a.curve.prime
        newx = ((lam**2)-a.x-b.x) % a.curve.prime
        newy = (lam*(a.x-newx)-a.y) % a.curve.prime
        ris = Point(a.curve, newx, newy)
        return ris


def negation(point):
    """arithmetic negation of a point"""
    ris = Point(point.curve, point.x, -point.y % point.curve.prime)
    return ris


def copy(point):
    """return a copy of point"""
    ris = Point(point.curve, point.x, point.y)
    ris.infinite = point.infinite
    return ris


def product(point, num):
    """mul operation on elliptic curves"""
    if num >= 2 and (not point.infinite):
        temp = copy(point)
        pointlist = [point]
        i = 1
        j = 0
        while i < num:
            j += 1
            i *= 2
            temp.doubles()
            pointlist.append(copy(temp))
        temp.infinite = True
        while num > 0:
            if num - i >= 0:
                temp.add(pointlist[j])
                num = num - i
            j -= 1
            i //= 2
        return temp
    else:
        return copy(point)


def same_curve(c1, c2):
    return (c1.a == c2.a) and (c1.b == c2.b) and (c1.prime == c2.prime)


def same_point(p1, p2):
    return (p1.x == p2.x) and (p1.y == p2.y) and same_curve(p1.curve, p2.curve) and (p1.infinite == p2.infinite)
