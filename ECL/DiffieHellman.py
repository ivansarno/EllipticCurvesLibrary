__author__ = 'ivansarno'
__version__ = 'V.2.3'
__doc__ = """Diffie_Hellman's cipher.

class:
DHkeycreator
"""

import os

#
# Diffie-Hellman public key algorithm on Elliptic Curves

#
# define of constant and replaceable function

DH_Curve_size = 192  # size in bit of integer in the operation (192,224,256,384 or 521 for standard curves)


def randint():
    """ Random number generator for big integer.

    :return: random int of DH_curve_size bit
    :rtype: int
    """
    temp = os.urandom(DH_Curve_size // 8)
    return int.from_bytes(temp, 'little')


#######

class DHkeycreator:
    """Object that creates and stores a key.

    method:
    -step1
    -step2
    -returnkey
    """
    def __init__(self, point):
        """Take a Point as base.

        :param point: Point used as base, can be used a standard point from ECL_standardcurves
        :type point: PointWOrder
        """
        self.point = point.copy()

    def step1(self):
        """Start protocol and return a Point to send to partner.

        :return: Point to sand to partner
        :rtype: Point
        """
        self.secret = randint() % self.point.order
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
