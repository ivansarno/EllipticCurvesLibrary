from ECL.Auxfun import is_square, EclException
from ECL.Point import Point

__author__ = 'ivansarno'
__version__ = 'V.3.2'
__doc__ = """Implementation of Koblitz algorithm.

functions:
-encode
-decode
-iterative_encode

exceptions:
-KoblitzFailError
"""


def encode(msg, padding, curve):
    """Conversion int to Point using Koblitz algorithm.

AAA this implementation of Kobitz algorithm work only whene prime field of curve = 3 mod 4
it work whit stdcurves exept P224
raise KoblitzFailError

    :param msg: message
    :type msg: int
    :param padding: express the padding and number of maximum attempts
    :type padding: int
    :param curve: Curve of point returned
    :type curve: Curve
    :return: Point of curve
    :rtype: Point
    :raise: KoblitzFailError
    """
    if curve.prime % 4 != 3:
        raise KoblitzFailError("curve.prime % 4 != 3")
    if msg * (padding + 1) < curve.prime:
        msg *= padding
        i = 0
        x = msg
        y = (x**3 + curve.a * x + curve.b) % curve.prime
        while (not is_square(y, curve.prime)) and i < padding:
            i += 1
            x = msg + i
            y = (x**3 + curve.a * x + curve.b) % curve.prime
        if i < padding:
            ex = pow(y, (curve.prime + 1) // 4, curve.prime)
            return Point(curve, x, ex)
    raise KoblitzFailError("point not found")


def decode(point, padding):
    """Converts Point to int deleting the padding.

    :param point: Point that contain a message
    :type point: Point
    :param padding: padding used to create the Point
    :type padding: int
    :return: the message, abscissa of point without the padding
    :rtype: int
    """
    return point.x // padding


def iterative_encode(msg, curve):
    """ Conversion int to Point by iterating koblitz_encode until find a point.
    :param msg: message
    :type msg: int
    :param curve: Curve of point returned
    :type curve: Curve
    :return: (point, padding)
    :rtype: Point * int
    """

    if curve.prime % 4 != 3:
        raise KoblitzFailError("curve.prime % 4 != 3")
    not_found = True
    point = None
    padding = 1
    while not_found:
        try:
            point = encode(msg, padding, curve)
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
