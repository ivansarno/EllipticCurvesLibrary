"""
    Elliptic Curve Library

    Copyright 2015 Ivan Sarno

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from typing import Callable, Tuple

from ECL.utility import EclException
from ECL.point import Point
from ECL.point_with_order import PointWOrder

__author__ = 'ivansarno'
__version__ = 'V.5.0'
__doc__ = """ElGamal's cipher.

fun:
-keygen
-encrypt
-decrypt

exception:
ElGamalError
"""


def keygen(base_point: PointWOrder, generator: Callable[[int], int]) \
        -> Tuple[int, Point]:
    """Cipher's key generator.

    :param base_point: Point used as base, can be used a standard point from ECL.std_curves
    :param generator: random number generator, return a random int of size passed by parameter
    :return: key composed by a secret number and a point
    """

    secret = generator(base_point.order.bit_length()) % base_point.order
    key_point = base_point * secret
    return secret, key_point


def encrypt(message: Point, pubkey: Point, base_point: PointWOrder, generator: Callable[[int], int]) -> \
        Tuple[Point, Point]:
    """ElGamal encryption fun.

    :param message: Point that expresses the message
    :param pubkey: Point used as public key
    :param base_point: Point used as base, can be used a standard point from ECL.std_curves
    :param generator: random number generator, return a random int of size passed by parameter
    :return: encrypted message composed by a couple of point
    """
    if not base_point.check(pubkey.curve):
            raise ElGamalError("the public key and the base point are not on the same curve")
    fact = generator(base_point.order.bit_length()) % base_point.order
    while fact == 0:
        fact = generator(base_point.order.bit_length()) % base_point.order
    cipher_point1 = base_point * fact
    cipher_point2 = message + (pubkey * fact)
    return cipher_point1, cipher_point2


def decrypt(message_point1: Point, message_point2: Point, privkey: int) -> Point:
    """ElGamal decryption fun

    :return: Point that expresses the message decrypted
    """

    temp = message_point1 * privkey
    return message_point2 - temp


class ElGamalError(EclException):
    """ElGamal algorithm fail."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__repr__()
