from ECL.Auxfun import inverse

__author__ = 'ivansarno'
__version__ = 'V.3.2'
__doc__ = """Implementation of Point of Elliptic Curve

classes:
-Point

Functions:
-are_opposites
-infinitepoint
"""


class Point:
    """Point of Curve.

    member:
    curve: Curve object, the Elliptic Curve that contain the point
    x: int abscissa
    y: int ordinate

    method:
    __eq__, doubles, add, negation, copy, __neg__, __add__,
    __sub__, __mul__, mul, __bool__, __str__, __repr__, are_opposites, check
    """

    def __init__(self, curve, x_init, y_init):
        """

        :param curve: Curve object
        :param x_init: abscissa
        :param y_init: ordinate
        :type curve: Curve
        :type x_init: int
        :type y_init: int
        """
        self.curve = curve
        self.x = x_init
        self.y = y_init
        self.infinite = False

    def __eq__(self, other):
        """

        :type other: Point
        :return: self == other
        :rtype: bool
        """
        return (self.x == other.x) and (self.y == other.y) and (self.curve == other.curve) and \
               (self.infinite == other.infinite)

    def doubles(self):
        """ Duplicates self without creates a new Point."""
        if not self.infinite:
            if self.y == 0:
                self.infinite = True
            else:
                lam = ((3 * self.x ** 2 + self.curve.a) * inverse(2 * self.y, self.curve.prime)) % self.curve.prime
                newx = ((lam ** 2) - self.x - self.x) % self.curve.prime
                newy = (lam * (self.x - newx) - self.y) % self.curve.prime
                self.y = newy
                self.x = newx

    def add(self, p):
        """ Add a Point to self without creates a new Point.

        :type p: Point
        """
        if not p.infinite:
            if self.infinite:
                self.infinite = False
                self.x = p.x
                self.y = p.y
            elif are_opposites(self, p):
                self.infinite = True
            elif self == p:
                self.doubles()
            else:
                lam = ((p.y - self.y) * inverse(p.x - self.x, self.curve.prime)) % self.curve.prime
                newx = ((lam ** 2) - self.x - p.x) % self.curve.prime
                newy = (lam * (self.x - newx) - self.y) % self.curve.prime
                self.y = newy
                self.x = newx

    def negation(self):
        """Changes the sign of the Point."""
        self.y = -self.y % self.curve.prime

    def copy(self):
        """Return a copy of self.

        :return: Point copy of self
        :rtype: Point
        """
        ris = Point(self.curve, self.x, self.y)
        ris.infinite = self.infinite
        return ris

    def __neg__(self):
        """Arithmetic negation of a Point.

        :return: -self
        :rtype: Point
        """
        ris = Point(self.curve, self.x, -self.y % self.curve.prime)
        return ris

    def __add__(self, other):
        """ Addition on Elliptic Curves.

        :type other: Point
        :return: self + other
        :rtype: Point
        """
        if self.infinite:
            return other.copy()
        elif other.infinite:
            return self.copy
        elif self == other:
            return self * 2
        elif are_opposites(self, other):
            return infinitepoint(self.curve)
        else:
            lam = ((other.y - self.y) * inverse(other.x - self.x, self.curve.prime)) % self.curve.prime
            newx = ((lam ** 2) - self.x - other.x) % self.curve.prime
            newy = (lam * (self.x - newx) - self.y) % self.curve.prime
            ris = Point(self.curve, newx, newy)
            return ris

    def __sub__(self, other):
        """Subraction on Elliptic Curves.

        :type other: Point
        :return: self - other
        :rtype: Point
        """
        if self.infinite:
            return other.__neg__()
        elif other.infinite:
            return self.copy
        elif are_opposites(self, other):
            return self * 2
        elif self == other:
            return infinitepoint(self.curve)
        else:
            lam = (((-other.y % other.curve.prime) - self.y) * inverse(other.x - self.x,
                                                                       self.curve.prime)) % self.curve.prime
            newx = ((lam ** 2) - self.x - other.x) % self.curve.prime
            newy = (lam * (self.x - newx) - self.y) % self.curve.prime
            ris = Point(self.curve, newx, newy)
            return ris

    def __mul__(self, other):
        """Moltiplication on Elliptic Curve.

        :param other: number >= 2
        :type other: int
        :returns: p = other * self (if other < 2 return self.copy())
        :rtype: Point
        """
        if other == 2 and not self.infinite:
            ris = self.copy()
            ris.doubles()
            return ris
        elif other > 2 and not self.infinite:
            temp = self.copy()
            pointlist = [self]  # contains temp result for iterative version of mul
            i = 1
            j = 0
            while i < other:
                j += 1
                i *= 2
                temp.doubles()  # generate intermediates protucts
                pointlist.append(temp.copy())  # contains log other intermediates result
            temp.infinite = True  # is set to add identity element
            while other > 0:  # roll back and add intermediates protucts
                if other - i >= 0:
                    temp.add(pointlist[j])
                    other -= i
                j -= 1
                i //= 2
            return temp
        else:
            return self.copy()

    def mul(self, other):
        """Multiplies self without create a new Point.

        :param other: number >=2
        :type other: int
        """
        if other == 2 and not self.infinite:
            self.doubles()
        elif other > 2 and not self.infinite:
            temp = self.copy()
            pointlist = [self]
            i = 1
            j = 0
            while i < other:
                j += 1
                i *= 2
                temp.doubles()
                pointlist.append(temp.copy())
            temp.infinite = True
            while other > 0:
                if other - i >= 0:
                    temp.add(pointlist[j])
                    other = other - i
                j -= 1
                i //= 2
            self.x = temp.x
            self.y = temp.y
            self.infinite = temp.infinite

    def check(self, curve):
        """Check if self is a valid point of curve.
        :param curve: curve whose membership tested point
        :type curve: Curve
        :return: True if self is a valid point of curve
        :rtype: bool
        """

        if not self.curve == curve:
            return False
        y = (self.x ** 3 + curve.a * self.x + curve.b) % curve.prime
        return y == (self.y ** 2) % curve.prime

    def __bool__(self):
        """Return not self == infinite.

        :rtype: bool
        """
        return not self.infinite

    def __str__(self):
        return "x: %x\ny: %x\n" % (self.x, self.y) + self.curve.__str__()

    def __repr__(self):
        return "Point(%s, %x, %x)" % (self.curve.__repr__(), self.x, self.y)


def are_opposites(p1, p2):
    """EC Point opposites control.

    :type p1: Point
    :type p2: Point
    :return: p1 == -p2
    :rtype: bool

    not creates new object, more speed then p1 == -P2
    """
    return (not p1.infinite) and (not p2.infinite) and p1.curve == p2.curve and (p1.x == p2.x) and \
           (p1.y == -p2.y % p2.curve.prime)


def infinitepoint(curve):
    """Creates an infinite point of a Curve.

    :type curve: Curve
    :return: infinite point of curve
    :rtype: Point
    """
    i = Point(curve, 0, 0)
    i.infinite = True
    return i
