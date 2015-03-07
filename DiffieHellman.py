__author__ = 'ivansarno'
__version__ = 'V.1.5'
from ECL_operator import *
import os

#
# Diffie-Hellman public key algorithm on Elliptic Curves

#
# define of constant and replaceable function

DH_Curve_size = 192  # size in bit of integer in the operation (192,224,256,384 or 521)
#######

def randint():
    """random number generator"""
    temp = os.urandom(DH_Curve_size // 8)
    return int.from_bytes(temp, 'little')


class DHkeycreator:
    """this object creates and stores a key"""
    def __init__(self, point):
        """take a PointWOrder as base"""
        self.point = copy(point)

    def step1(self):
        """start protocol and return a Point to send to partner"""
        self.secret = randint() % self.point.order
        return product(self.point, self.secret)

    def step2(self, partnerpoint):
        """take result of partener step1 and return the key as Point abject"""
        self.key = product(partnerpoint, self.secret)
        return self.key

    def returnkey(self):
        """return the key as Point abject"""
        return self.key
