__author__ = 'ivansarno'
__version__ = 'V.1.5'
from ECL_Auxfun import inverse


class Curve:
    """Prime Elliptic Curve, parameters a and b, field prime"""
    def __init__(self, a_init, b_init, prime_init):
        self.a = a_init
        self.b = b_init
        self.prime = prime_init


class Point:
    """Point of Curve, parameters x,y, the curve of point and if is the infinite point"""
    def __init__(self, curve, x_init, y_init):
        self.curve = curve
        self.x = x_init
        self.y = y_init
        self.infinite = False

    def doubles(self):
        """duplicates the point"""
        if not self.infinite:
            if self.y == 0:
                self.infinite = True
            else:
                lam = ((3 * self.x ** 2 + self.curve.a) * inverse(2 * self.y, self.curve.prime)) % self.curve.prime
                newx = ((lam ** 2)-self.x-self.x) % self.curve.prime
                newy = (lam * (self.x-newx)-self.y) % self.curve.prime
                self.y = newy
                self.x = newx

    def add(self, p):
        """sum the the point p at the point"""
        if not p.infinite:
            if self.infinite:
                self.infinite = False
                self.x = p.x
                self.y = p.y
            elif are_opposites(self, p):
                self.infinite = True
            elif same_point(self, p):
                self.doubles()
            else:
                lam = ((p.y-self.y) * inverse(p.x-self.x, self.curve.prime)) % self.curve.prime
                newx = ((lam**2)-self.x-p.x) % self.curve.prime
                newy = (lam*(self.x-newx)-self.y) % self.curve.prime
                self.y = newy
                self.x = newx

    def opposite(self):
        """do the arithmetic negation of the point"""
        self.y = -self.y % self.curve.prime


def same_curve(c1, c2):
    return (c1.a == c2.a) and (c1.b == c2.b) and (c1.prime == c2.prime)


def same_point(p1, p2):
    return (p1.x == p2.x) and (p1.y == p2.y) and same_curve(p1.curve, p2.curve) and (p1.infinite == p2.infinite)


def are_opposites(p1, p2):
    return (not p1.infinite) and (not p2.infinite) and same_curve(p1.curve, p2.curve) and (p1.x == p2.x) and (p1.y == -p2.y % p2.curve.prime)


class PointWOrder (Point):
    """point with order"""
    def __init__(self, curve, x, y, order):
        super().__init__(curve, x, y)
        self.order = order
