__author__ = 'ivansarno'
__version__ = 'V.2.3'
__doc__ = """ElGamal's cipher and Koblitz's int_to_point algorithms.

fun:
-eg_keygen
-eg_encrypt
-eg_decrypt
-koblitz_encode
-koblitz_decode
-iterative_koblitz

class:
-EGkey
-EGmessage

exeption:
-KoblitzFailError
"""


import os

from ECL.Classes import Point
from ECL.Auxfun import is_square

#
# ELGamal public key cipher on Elliptic Curves and Koblitz algorithm

#
#  define of constant and replaceable function

# size in bit integer in the operation (192,224,256,384 or 521 for standard curves)
EG_Curve_size = 192


def randint():
    """ Random number generator for big integer.

    :return: random int of EG_curve_size bit
    :rtype: int
    """
    temp = os.urandom(EG_Curve_size // 8)
    return int.from_bytes(temp, 'little')


def randfact():
    """Random number generator for standard int.

    :return: random 64 bit int
    :rtype: int
    """
    temp = os.urandom(8)
    return int.from_bytes(temp, 'little')

#########


class EGkey:
    """Object that contain cipher's key.

    member:
    private: private key
    public: public key
    :type private: int
    :type public: int
    """
    def __init__(self, priv, pub):
        """

        :param priv: int private key
        :param pub: Point puplic key
        """
        self.public = pub
        self.private = priv


class EGmessage:
    """Cipher's message format.

    member: v, w
    :type v: Point
    :type w: Point
    """

    def __init__(self, vpoint, wpoint):
        """

        :param vpoint: Point to initialize v member
        :param wpoint: Point to initialize w member
        :type vpoint: Point
        :type wpoint: Point
        """
        self.v = vpoint
        self.w = wpoint


def eg_keygen(bpoint):
    """Cipher's key generator.

    :param bpoint: Point used as base, can be used a standard point from ECL_standardcurves
    :type bpoint: PointWOrder
    :rtype: EGkey
    :return: the key
    """
    secret = randint() % bpoint.order
    kpoint = bpoint * secret
    return EGkey(secret, kpoint)


def eg_encrypt(message, pubkey, stpoint):
    """ElGamal encryption fun.

    :param message: Point that expresses the message
    :param pubkey: Point used as puplic key
    :param stpoint: Point used as base, can be used a standard point from ECL_standardcurves
    :type message: Point
    :type pubkey: Point
    :type stpoint: Point
    :return: encrypted message
    :rtype: EGmessage
    """
    fact = randfact()
    vpoint = stpoint * fact
    wpoint = message + (pubkey * fact)
    return EGmessage(vpoint, wpoint)


def eg_decrypt(message, key):
    """ElGamal decryption fun

    :type message: EGmessage
    :type key: EGkey
    :return: Point thet expresses the message decrypted
    :rtype: Point
    """
    v = message.v * key.private
    v.negation()
    return message.w + v

#
# AAA this implementation of Kobitz algorithm work only whene prime field of curve = 3 mod 4
# it work whit stdcurves exept P224
# raise KoblitzFailError


def koblitz_encode(msg, padding, curve):
    """Conversion int to Point using Koblitz algorithm. Raise KoblitzFailError.

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


def koblitz_decode(point, padding):
    """Converts Point to int deleting the padding.

    :param point: Point that contain a message
    :type point: Point
    :param padding: padding used to create the Point
    :type padding: int
    :return: the message, abscissa of point without the padding
    :rtype: int
    """
    return point.x // padding


class KoblitzFailError(Exception):
    """Koblitz algorithm fail, point not found."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__repr__()


def iterative_koblitz(msg, curve):
    """ Conversion int to Point by iterating koblitz_encode until find a point.
    :param msg: message
    :type msg: int
    :param curve: Curve of point returned
    :type curve: Curve
    :return: (point, padding)
    :rtype: Point * int
    """
    found = False
    padding = 1
    while not found:
        try:
            point = koblitz_encode(msg, padding, curve)
        except KoblitzFailError:
            padding += 1
        else:
            found = True
    return point, padding