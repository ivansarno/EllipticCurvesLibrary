from typing import Callable
from ECL import utility
from ECL.point import Point
from ECL.point_with_order import PointWOrder

__author__ = 'ivansarno'
__version__ = 'V.4.2'
__doc__ = """Diffie-Hellman's public key system.

class:
DiffieHellman
"""


class DiffieHellman:
    """Object that creates and stores a key.

    method:
    -step1
    -step2
    """

    def __init__(self, base_point: PointWOrder, curve_size: int, generator: Callable[[int], int]=utility.generator):
        """
        :param base_point: Point used as base, can be used a standard point from ECL.std_curves
        :param curve_size: number of bit of order of the curve
        :param generator: random number generator, return a random int of size passed by parameter,
        use the built-in by default
        """

        self.__point = base_point
        self.__size = curve_size
        self.__gen = generator
        self.__secret = self.__gen(self.__size) % self.__point.order
        self.__key = None

    def step1(self) -> Point:
        """Start protocol and return a Point to send to partner.

        :return: Point to sand to partner
        """
        return self.__point * self.__secret

    def step2(self, partnerpoint: Point) -> Point:
        """Take result of partener step1 and return the key as Point

        :param partnerpoint: Point received by partner
        :return: the key
        """
        self.__key = partnerpoint * self.__secret
        return self.__key

    @property
    def key(self) -> Point:
        """
        :return: the key or None if step2 has not been executed
        """
        return self.__key
