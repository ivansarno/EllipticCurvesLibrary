from ECL.curve import Curve
from ECL.point import Point
__author__ = 'ivansarno'
__version__ = 'V.4.alpha'
__doc__ = """Point with extra member, the order"""


class PointWOrder (Point):
    """EC Point with order parameter.

    order == -1 is garbage value
    """
    def __init__(self, curve: Curve, x_init: int, y_init: int, order: int):
        """

        :param curve: Curve of the point
        :param x_init: abscissa
        :param y_init: ordinata
        :param order: order of Point
        """
        super().__init__(curve, x_init, y_init)
        self.__order = order

    @property
    def order(self):
        return self.__order

    def copy(self):
        """Return a copy of self.

        :return: Point copy of self
        :rtype: Point
        """

        if self.__bool__():
            if self.__order < 0:
                return Point(self.curve, self.x, self.y)
            else:
                return PointWOrder(self.curve, self.x, self.y, self.__order)
        else:
            return Point.infinitepoint(self.curve)

    def _add(self, p):
        """ Add a Point to self without creates a new Point, set order = -1.

        :type p: Point
        """
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

    def _mul(self, other):
        """Multiplies self without create a new Point, set order = -1.

        :param other: number >=2
        :type other: int
        """
        super()._mul(other)
        self.__order = -1

    def __str__(self):
        if self.order < 0:
            return super().__str__()
        else:
            return "x: %x\ny: %x\norder: %x\n" % (self.x, self.y, self.order) + self.curve.__str__()

    def __repr__(self):
        if self.order < 0:
            return super().__repr__()
        else:
            return "PointWOrder(%s, 0x%x, 0x%x, 0x%x)" % (self.curve.__repr__(), self.x, self.y, self.order)