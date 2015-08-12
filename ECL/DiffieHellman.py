from ECL import Auxfun

__author__ = 'ivansarno'
__version__ = 'V.3.0'
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

    def __init__(self, base_point, curve_size, generator=None):
        """Take a Point as base.

        :param base_point: Point used as base, can be used a standard point from ECL_standardcurves
        :type base_point: PointWOrder
        :param curve_size: nember of bit of order of the curve
        :type curve_size: int
        :param generator: random number generator, by default use built-in generator
        :type generator: ECL.Auxfun.Generator
        """
        if generator is None:
            generator = Auxfun.Generator()
        self.point = base_point.copy()
        self.size = curve_size
        self.gen = generator
        self.secret = None
        self.key = None

    def step1(self):
        """Start protocol and return a Point to send to partner.

        :return: Point to sand to partner
        :rtype: Point
        """
        self.secret = self.gen.get(self.size) % self.point.order
        return self.point * self.secret

    def step2(self, partnerpoint):
        """Take result of partener step1 and return the key as Point

        :type partnerpoint: Point
        :param partnerpoint: Point received by partner
        :return: the key
        :rtype: Point
        """
        self.key = partnerpoint * self.secret
        return self.key

    def returnkey(self):
        """
        :return: the key
        :rtype: Point
        """
        return self.key
