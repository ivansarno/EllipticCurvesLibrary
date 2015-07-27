from ECL import Auxfun
from ECL.Point import Point

__author__ = 'ivansarno'
__version__ = 'V.3.0'
__doc__ = """ElGamal's cipher.

fun:
-keygen
-encrypt
-decrypt
"""


def keygen(base_point, curve_size, generator=Auxfun.Generator()):
    """Cipher's key generator.

    :param base_point: Point used as base, can be used a standard point from StdCurves
    :type base_point: PointWOrder
    :rtype: int * Point
    :return: key composed by a secret number and a point
    """
    secret = generator.get(curve_size) % base_point.order
    key_point = base_point * secret
    return secret, key_point


def encrypt(message, pubkey, base_point, generator=Auxfun.Generator()):
    """ElGamal encryption fun.

    :param message: Point that expresses the message
    :param pubkey: Point used as public key
    :param base_point: Point used as base, can be used a standard point from ECL_standardcurves
    :type message: Point
    :type pubkey: Point
    :type base_point: Point
    :return: encrypted message composed by a couple of point
    :rtype: Point * Point
    """
    fact = generator.get(64)  # standard 64bit int
    cipher_point1 = base_point * fact
    cipher_point2 = message + (pubkey * fact)
    return cipher_point1, cipher_point2


def decrypt(message_point1, message_point2, privkey):
    """ElGamal decryption fun

    :type message_point1: Point
    :type message_point2: Point
    :type privkey: int
    :return: Point that expresses the message decrypted
    :rtype: Point
    """

    temp = message_point1 * privkey
    return message_point2 - temp
