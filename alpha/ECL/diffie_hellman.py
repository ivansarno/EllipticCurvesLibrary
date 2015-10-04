from typing import Callable
from ECL import utility, PointWOrder, Point

__author__ = 'ivansarno'
__version__ = 'V.4.alpha'
__doc__ = """Diffie-Hellman's public key system.

class:
DiffieHellman
"""


class DiffieHellman:
    """Object that creates and stores a key.

    method:
    -step1
    -step2
    -returnkey
    """

    def __init__(self, base_point: PointWOrder, curve_size: int, generator: Callable[[int], int]=utility.generator):
        """Take a Point as base.

        :param base_point: Point used as base, can be used a standard point from ECL_standardcurves
        :param curve_size: nember of bit of order of the curve
        :param generator: random number generator, return a rondom int of size passed by parameter,
        use the built-in by default
        """

        self.point = base_point.copy()
        self.size = curve_size
        self.gen = generator
        self.secret = None
        self.key = None

    def step1(self) -> Point:
        """Start protocol and return a Point to send to partner.

        :return: Point to sand to partner
        """
        self.secret = self.gen(self.size) % self.point.order
        return self.point * self.secret

    def step2(self, partnerpoint: Point) -> Point:
        """Take result of partener step1 and return the key as Point

        :param partnerpoint: Point received by partner
        :return: the key
        """
        self.key = partnerpoint * self.secret
        return self.key

    def returnkey(self) -> Point:
        """
        :return: the key
        """
        return self.key
