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
from typing import Tuple
from ECL.curve import Curve
from ECL.utility import is_square, EclError, square_root
from ECL.point import Point

__author__ = 'ivansarno'
__version__ = 'V.5.5'
__doc__ = """Implementation of Koblitz algorithm.

functions: encode, decode, iterative_encode

exceptions: KoblitzFailError
"""


def encode(message: int, padding: int, curve: Curve) -> Point:
    """Conversion int to Point using Koblitz algorithm.

    :param curve: Curve of point returned
    :return: Point of curve
    :raise KoblitzFailError:

    All curves are supported but performances depends on prime number
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
    padding = 1
    while message * (padding + 1) < curve.prime:
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
            point = Point(curve, x, ex)
            return point, padding
        padding += 1
    raise KoblitzFailError("point not found")



class KoblitzFailError(EclError):
    """Koblitz algorithm fail, point not found."""
    pass
