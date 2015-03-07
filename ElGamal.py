__author__ = 'ivansarno'
__version__ = 'V.1.5'
from ECL_operator import *
from ECL_Auxfun import is_square
import os
#
# EL Gamal public key cipher on Elliptic Curves

#
#  define of constant and replaceable function

# size in bit integer in the operation
DH_Curve_size = 192


# random number generator for big integer
def randint():
    temp = os.urandom(DH_Curve_size // 8)
    return int.from_bytes(temp, 'little')


# random number generator for standard int
def randfact():
    temp = os.urandom(8)
    return int.from_bytes(temp, 'little')

#########


class EGkey:
    """object that contain cipher's key"""
    def __init__(self, priv, pub):
        self.public = pub
        self.private = priv


class EGmessage:
    """cipher's message format"""
    def __init__(self, vpoint, wpoint):
        self.v = vpoint
        self.w = wpoint


def eg_keygen(bpoint):
    """ take a standard Point as base and return the key as EGkey object"""
    secret = randint() % bpoint.order
    kpoint = product(bpoint, secret)
    return EGkey(secret, kpoint)


def eg_encrypt(message, pubkey, stpoint):
    """El Gamal encrypt fun: stpoint is a standard point of EC, message is a Point,
     pubkey an EGkey object with public key of receiver, return an EGmessage object"""
    fact = randfact()
    vpoint = product(stpoint, fact)
    wpoint = addition(message, product(pubkey, fact))
    return EGmessage(vpoint, wpoint)


def eg_decrypt(message, key):
    """El Gamal decrypt fun: take an EGmessage object as massage and an EGkey object as key, return a Point"""
    v = product(message.v, key.private)
    v.opposite()
    return addition(message.w, v)


def koblitz_encode(msg, h, curve):
    """converts a number in a Point"""
    if msg * (h + 1) < curve.prime:
        msg *= h
        i = 0
        x = msg
        y = (x**3 + curve.a * x + curve.b) % curve.prime
        while not is_square(y, curve.prime):
            i += 1
            x = msg + i
            y = (x**3 + curve.a * x + curve.b) % curve.prime
        return Point(curve, x, y)
    else:
        nil = Point(curve, 0, 0)
        nil.infinite = True
        return nil


def koblitz_decode(point, h):
    """converts a Point in a int deleting the padding"""
    return point.x // h
