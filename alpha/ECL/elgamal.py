from typing import Callable, Tuple
from ECL import utility, PointWOrder, Point

__author__ = 'ivansarno'
__version__ = 'V.4.alpha'
__doc__ = """ElGamal's cipher.

fun:
-keygen
-encrypt
-decrypt
"""


def keygen(base_point: PointWOrder, curve_size: int, generator: Callable[[int], int]=utility.generator) \
        -> Tuple[int, Point]:
    """Cipher's key generator.

    :param base_point: Point used as base, can be used a standard point from StdCurves
    :param generator: random number generator, return a random int of size passed by parameter,
    use the built-in by default
    :return: key composed by a secret number and a point
    """

    secret = generator(curve_size) % base_point.order
    key_point = base_point * secret
    return secret, key_point


def encrypt(message: Point, pubkey: Point, base_point: Point, generator: Callable[[int], int]=utility.generator) -> \
        Tuple[Point, Point]:
    """ElGamal encryption fun.

    :param message: Point that expresses the message
    :param pubkey: Point used as public key
    :param base_point: Point used as base, can be used a standard point from ECL_standardcurves
    :param generator: random number generator, return a random int of size passed by parameter,
    use the built-in by default
    :return: encrypted message composed by a couple of point
    """

    fact = generator(64)  # standard 64bit int
    cipher_point1 = base_point * fact
    cipher_point2 = message + (pubkey * fact)
    return cipher_point1, cipher_point2


def decrypt(message_point1: Point, message_point2: Point, privkey: int) -> Point:
    """ElGamal decryption fun

    :return: Point that expresses the message decrypted
    """

    temp = message_point1 * privkey
    return message_point2 - temp
