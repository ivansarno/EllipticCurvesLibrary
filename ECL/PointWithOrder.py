from ECL.Point import Point
__author__ = 'ivansarno'
__version__ = 'V.3.0'
__doc__ = """Point with extra member, the order"""


class PointWOrder (Point):
    """EC Point with order parameter.

    member:
    curve: Curve object, the Elliptic Curve that contain the point
    x: int abscissa
    y: int ordinate
    order: order of Point, if == -1 is a garbage value
    order: int
    """
    def __init__(self, curve, x_init, y_init, order):
        """

        :param curve: Curve of the point
        :type curve: Curve
        :param x_init: abscissa
        :type x_init: int
        :param y_init: ordinata
        :type y_init: int
        :param order: order of Point
        :type order: int
        """
        super().__init__(curve, x_init, y_init)
        self.order = order

    def copy(self):
        """Return a copy of self.

        :return: Point copy of self
        :rtype: Point
        """
        ris = PointWOrder(self.curve, self.x, self.y, self.order)
        ris.infinite = self.infinite
        return ris

    def add(self, p):
        """ Add a Point to self without creates a new Point, set order = -1.

        :type p: Point
        """
        super().add(p)
        self.order = -1  # garbage value

    def negation(self):
        """Changes the sign of the Point and set order = -1."""
        super().negation()
        self.order = -1

    def doubles(self):
        """ Duplicates self without creates a new Point, set order = -1."""
        super().doubles()
        self.order = -1

    def mul(self, other):
        """Multiplies self without create a new Point, set order = -1.

        :param other: number >=2
        :type other: int
        """
        super().mul(other)
        self.order = -1

    def __str__(self):
        return 'x: ' + self.x.__repr__() + '\ny: ' + self.y.__repr__() + '\norder: ' + self.order.__repr__() + '\n' +\
               self.curve.__str__()

    def __repr__(self):
        return 'x:' + self.x.__repr__() + ' y:' + self.y.__repr__() + ' order:' + self.order.__repr__() + ' ' + \
               self.curve.__repr__()
