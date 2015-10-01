from ECL import Auxfun
from ECL.Point import Point

__author__ = 'ivansarno'
__version__ = 'V.3.2'
__doc__ = """ElGamal's cipher.

fun:
-keygen
-encrypt
-decrypt
"""


def keygen(base_point, curve_size, generator=Auxfun.generator):
    """Cipher's key generator.

    :param base_point: Point used as base, can be used a standard point from StdCurves
    :param generator: random number generator, return a rondom int of size passed by parameter,
    use the built-in by default
    :type base_point: PointWOrder
    :type generator: int -> int
    :rtype: int * Point
    :return: key composed by a secret number and a point
    """

    secret = generator(curve_size) % base_point.order
    key_point = base_point * secret
    return secret, key_point


def encrypt(message, pubkey, base_point, generator=Auxfun.generator):
    """ElGamal encryption fun.

    :param message: Point that expresses the message
    :param pubkey: Point used as public key
    :param base_point: Point used as base, can be used a standard point from ECL_standardcurves
    :param generator: random number generator, return a rondom int of size passed by parameter,
    use the built-in by default
    :type message: Point
    :type pubkey: Point
    :type base_point: Point
    :type generator: int -> int
    :return: encrypted message composed by a couple of point
    :rtype: Point * Point
    """

    fact = generator(64)  # standard 64bit int
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
