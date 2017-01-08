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
from ECL.point import Point
__author__ = 'ivansarno'
__version__ = 'V.5.3'
__doc__ = """Point with extra member, the order"""


class PointWOrder(Point):
    """EC Point with order member.

    order == -1 is garbage value
    """
    def __init__(self, curve: Curve, x_init: int, y_init: int, order: int):
        """

        :param curve: Curve of the point
        :param x_init: abscissa
        :param y_init: ordinate
        :param order: order of Point
        """
        super().__init__(curve, x_init, y_init)
        self.__order = order

    @property
    def order(self) -> int:
        return self.__order

    def copy(self) -> Point:
        """Return a copy of self.

        :return: Point copy of self, if order is defined return a PointWOrder
        """

        if self.__bool__():
            if self.__order < 0:
                return Point(self.curve, self.x, self.y)
            else:
                return PointWOrder(self.curve, self.x, self.y, self.__order)
        else:
            return Point.infinitepoint(self.curve)

    def _add(self, p: Point):
        """ Add a Point to self without creates a new Point, set order = -1."""
        super()._add(p)
        self.__order = -1  # garbage value

    def _negation(self):
        """Changes the sign of the Point and set order = -1."""
        super()._negation()
        self.__order = -1

    def _doubles(self):
        """ Duplicates self without creates a new Point, set order = -1."""
        super()._doubles()
        self.__order = -1

    def _mul(self, other: int):
        """Multiplies self without create a new Point, set order = -1.

        :param other: number >=2
        """
        super()._mul(other)
        self.__order = -1

    def __str__(self):
        if self.order < 0:
            return super().__str__()
        else:
            return "x: %x\ny: 0x%x\norder: 0x%x\n" % (self.x, self.y, self.order) + self.curve.__str__()

    def __repr__(self):
        if self.order < 0:
            return super().__repr__()
        else:
            return "ECL.PointWOrder(%s, 0x%x, 0x%x, 0x%x)" % (self.curve.__repr__(), self.x, self.y, self.order)
