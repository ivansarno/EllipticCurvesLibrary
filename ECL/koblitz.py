from typing import Tuple
from ECL.curve import Curve
from ECL.utility import is_square, EclException, square_root
from ECL.point import Point

__author__ = 'ivansarno'
__version__ = 'V.4.2'
__doc__ = """Implementation of Koblitz algorithm.

functions:
-encode
-decode
-iterative_encode

exceptions:
-KoblitzFailError
"""


def encode(message: int, padding: int, curve: Curve) -> Point:
    """Conversion int to Point using Koblitz algorithm.

    :param curve: Curve of point returned
    :return: Point of curve
    :raise: KoblitzFailError

    All curves are supported but performances depends from prime number
    """
    if message * (padding + 1) < curve.prime:
        message *= padding
        i = 0
        x = message
        y = (x**3 + curve.a * x + curve.b) % curve.prime
        while (not is_square(y, curve.prime)) and i < padding:
            i += 1
            x = message + i
            y = (x**3 + curve.a * x + curve.b) % curve.prime
        if i < padding:
            ex = square_root(y, curve.prime)
            return Point(curve, x, ex)
    raise KoblitzFailError("point not found")


def decode(point: Point, padding: int) -> int:
    """Converts Point to int deleting the padding.

    :param point: Point that contain a message
    :param padding: padding used to create the Point
    :return: the message, abscissa of point without the padding
    """
    return point.x // padding


def iterative_encode(message: int, curve: Curve) -> Tuple[Point, int]:
    """ Conversion int to Point by iterating koblitz.encode until find a point.

    :param curve: Curve of point returned
    :return: (point, padding)
    """
    not_found = True
    point = None
    padding = 1
    while not_found:
        try:
            point = encode(message, padding, curve)
        except KoblitzFailError:
            padding += 1
        else:
            not_found = False
    return point, padding


class KoblitzFailError(EclException):
    """Koblitz algorithm fail, point not found."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__repr__()
