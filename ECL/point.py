"""
    Elliptic Curve Library

    Copyright 2015 Ivan Sarno

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from ECL.curve import Curve
from ECL.utility import inverse

__author__ = 'ivansarno'
__version__ = 'V.5.1'
__doc__ = """Implementation of Point of Elliptic Curve

classes: Point

Functions: are_opposites
"""


class Point:
    """Point of Curve.

    method:
    __eq__, _doubles, _add, _negation, copy, __neg__, __add__,
    __sub__, __mul__, _mul, __bool__, __str__, __repr__, check, infinitepoint
    """

    def __init__(self, curve: Curve, x_init: int, y_init: int):
        """

        :param curve: Curve object
        :param x_init: abscissa
        :param y_init: ordinate
        """
        self.__curve = curve
        self.__x = x_init
        self.__y = y_init
        self.__infinite = False

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def curve(self) -> Curve:
        return self.__curve

    def __eq__(self, other):
        """

        :type other: Point
        :return: self == other
        """
        if other and not self.__infinite:
            return (self.__x == other.__x) and (self.__y == other.__y) and (self.__curve == other.__curve)
        else:
            return self.__infinite == other.__infinite

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
        if self.__infinite:
            return self.copy()
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
        """Subtraction on Elliptic Curves.

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

    def __mul__(self, other: int):
        """Multiplication on Elliptic Curve.

        :param other: number >= 2
        :returns: p = other * self (if other < 2 return self.copy())
        :rtype: Point
        """
        if self.__infinite:
            return self.infinitepoint(self.curve)
        if other == 1:
            return self.copy()

        result = self.infinitepoint(self.curve)
        temp = self.copy()
        while other != 0:
            if other & 1:
                result._add(temp)
            temp._doubles()
            other >>= 1
        return result

    def _mul(self, other: int):
        """Multiplies self without create a new Point.

        :param other: number >=2
        """
        if self.__infinite or other == 1:
            return
        temp = self.infinitepoint(self.curve)
        while other != 0:
            if other & 1:
                temp._add(self)
            self._doubles()
            other >>= 1
        self.__x = temp.__x
        self.__y = temp.__y
        self.__infinite = temp.__infinite

    def check(self, curve: Curve) -> bool:
        """Check if self is a valid point of __curve.

        :param curve: curve whose membership tested point
        :return: True if self is a valid point of curve
        """

        if not self.__curve == curve:
            return False
        y = (self.__x ** 3 + curve.a * self.__x + curve.b) % curve.prime
        return y == (self.__y ** 2) % curve.prime

    def __bool__(self):
        """Return not self == infinite.

        """
        return not self.__infinite

    @staticmethod
    def infinitepoint(curve: Curve):
        """Creates an infinite point of a Curve.

        :return: infinite point of curve
        :rtype: Point
        """
        i = Point(curve, 0, 0)
        i.__infinite = True
        return i

    def __str__(self):
        return "x: 0x%x\ny: 0x%x\n" % (self.__x, self.__y) + self.__curve.__str__()

    def __repr__(self):
        return "ECL.Point(%s, 0x%x, 0x%x)" % (self.__curve.__repr__(), self.__x, self.__y)


def are_opposites(p1: Point, p2: Point) -> bool:
    """EC Point opposites control.

    :return: p1 == -p2

    not creates new object, more speed then p1 == -P2
    """
    return p1 and p2 and p1.curve == p2.curve and (p1.x == p2.x) and (p1.y == -p2.y % p2.curve.prime)
