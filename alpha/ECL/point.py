from ECL.utility import inverse

__author__ = 'ivansarno'
__version__ = 'V.4.alpha'
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
    __curve: Curve object, the Elliptic Curve that contain the point
    __x: int abscissa
    __y: int ordinate

    method:
    __eq__, _doubles, _add, _negation, copy, __neg__, __add__,
    __sub__, __mul__, _mul, __bool__, __str__, __repr__, are_opposites, check
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
        self.__curve = curve
        self.__x = x_init
        self.__y = y_init
        self.__infinite = False

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def curve(self):
        return self.__curve

    def __eq__(self, other):
        """

        :type other: Point
        :return: self == other
        :rtype: bool
        """
        return (self.__x == other.__x) and (self.__y == other.__y) and (self.__curve == other.__curve) and \
               (self.__infinite == other.__infinite)

    def _doubles(self):
        """ Duplicates self without creates a new Point."""
        if not self.__infinite:
            if self.__y == 0:
                self.__infinite = True
            else:
                lam = ((3 * self.__x ** 2 + self.__curve.a) * inverse(2 * self.__y,
                                                                      self.__curve.prime)) % self.__curve.prime
                newx = ((lam ** 2) - self.__x - self.__x) % self.__curve.prime
                newy = (lam * (self.__x - newx) - self.__y) % self.__curve.prime
                self.__y = newy
                self.__x = newx

    def _add(self, p):
        """ Add a Point to self without creates a new Point.

        :type p: Point
        """
        if not p.__infinite:
            if self.__infinite:
                self.__infinite = False
                self.__x = p.__x
                self.__y = p.__y
            elif are_opposites(self, p):
                self.__infinite = True
            elif self == p:
                self._doubles()
            else:
                lam = ((p.__y - self.__y) * inverse(p.__x - self.__x, self.__curve.prime)) % self.__curve.prime
                newx = ((lam ** 2) - self.__x - p.__x) % self.__curve.prime
                newy = (lam * (self.__x - newx) - self.__y) % self.__curve.prime
                self.__y = newy
                self.__x = newx

    def _negation(self):
        """Changes the sign of the Point."""
        self.__y = -self.__y % self.__curve.prime

    def copy(self):
        """Return a copy of self.

        :return: Point copy of self
        :rtype: Point
        """
        ris = Point(self.__curve, self.__x, self.__y)
        ris.__infinite = self.__infinite
        return ris

    def __neg__(self):
        """Arithmetic _negation of a Point.

        :return: -self
        :rtype: Point
        """
        ris = Point(self.__curve, self.__x, -self.__y % self.__curve.prime)
        return ris

    def __add__(self, other):
        """ Addition on Elliptic Curves.

        :type other: Point
        :return: self + other
        :rtype: Point
        """
        if self.__infinite:
            return other.copy()
        elif other.__infinite:
            return self.copy
        elif self == other:
            return self * 2
        elif are_opposites(self, other):
            return self.infinitepoint(self.__curve)
        else:
            lam = ((other.__y - self.__y) * inverse(other.__x - self.__x, self.__curve.prime)) % self.__curve.prime
            newx = ((lam ** 2) - self.__x - other.__x) % self.__curve.prime
            newy = (lam * (self.__x - newx) - self.__y) % self.__curve.prime
            ris = Point(self.__curve, newx, newy)
            return ris

    def __sub__(self, other):
        """Subraction on Elliptic Curves.

        :type other: Point
        :return: self - other
        :rtype: Point
        """
        if self.__infinite:
            return other.__neg__()
        elif other.__infinite:
            return self.copy
        elif are_opposites(self, other):
            return self * 2
        elif self == other:
            return self.infinitepoint(self.__curve)
        else:
            lam = (((-other.__y % other.__curve.prime) - self.__y) * inverse(other.__x - self.__x,
                                                                             self.__curve.prime)) % self.__curve.prime
            newx = ((lam ** 2) - self.__x - other.__x) % self.__curve.prime
            newy = (lam * (self.__x - newx) - self.__y) % self.__curve.prime
            ris = Point(self.__curve, newx, newy)
            return ris

    def __mul__(self, other):
        """Moltiplication on Elliptic Curve.

        :param other: number >= 2
        :type other: int
        :returns: p = other * self (if other < 2 return self.copy())
        :rtype: Point
        """
        if other == 2 and not self.__infinite:
            ris = self.copy()
            ris._doubles()
            return ris
        elif other > 2 and not self.__infinite:
            temp = self.copy()
            pointlist = [self]  # contains temp result for iterative version of _mul
            i = 1
            j = 0
            while i < other:
                j += 1
                i *= 2
                temp._doubles()  # generate intermediates protucts
                pointlist.append(temp.copy())  # contains log other intermediates result
            temp.__infinite = True  # is set to _add identity element
            while other > 0:  # roll back and _add intermediates protucts
                if other - i >= 0:
                    temp._add(pointlist[j])
                    other -= i
                j -= 1
                i //= 2
            return temp
        else:
            return self.copy()

    def _mul(self, other):
        """Multiplies self without create a new Point.

        :param other: number >=2
        :type other: int
        """
        if other == 2 and not self.__infinite:
            self._doubles()
        elif other > 2 and not self.__infinite:
            temp = self.copy()
            pointlist = [self]
            i = 1
            j = 0
            while i < other:
                j += 1
                i *= 2
                temp._doubles()
                pointlist.append(temp.copy())
            temp.__infinite = True
            while other > 0:
                if other - i >= 0:
                    temp._add(pointlist[j])
                    other = other - i
                j -= 1
                i //= 2
            self.__x = temp.__x
            self.__y = temp.__y
            self.__infinite = temp.__infinite

    def check(self, curve):
        """Check if self is a valid point of __curve.
        :param curve: __curve whose membership tested point
        :type curve: Curve
        :return: True if self is a valid point of __curve
        :rtype: bool
        """

        if not self.__curve == curve:
            return False
        y = (self.__x ** 3 + curve.a * self.__x + curve.b) % curve.prime
        return y == (self.__y ** 2) % curve.prime

    def __bool__(self):
        """Return not self == __infinite.

        :rtype: bool
        """
        return not self.__infinite

    @staticmethod
    def infinitepoint(curve):
        """Creates an infinite point of a Curve.

        :type curve: Curve
        :return: infinite point of curve
        :rtype: Point
        """
        i = Point(curve, 0, 0)
        i.__infinite = True
        return i

    def __str__(self):
        return "x: %x\ny: %x\n" % (self.__x, self.__y) + self.__curve.__str__()

    def __repr__(self):
        return "Point(%s, %x, %x)" % (self.__curve.__repr__(), self.__x, self.__y)


def are_opposites(p1, p2):
    """EC Point opposites control.

    :type p1: Point
    :type p2: Point
    :return: p1 == -p2
    :rtype: bool

    not creates new object, more speed then p1 == -P2
    """
    return p1 and p2 and p1.curve == p2.curve and (p1.x == p2.x) and (p1.y == -p2.y % p2.curve.prime)
