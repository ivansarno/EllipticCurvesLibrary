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
import hashlib
from typing import Callable, Tuple
from ECL.point import Point
from ECL.point_with_order import PointWOrder
from ECL.utility import inverse, EclException

__author__ = 'ivansarno'
__version__ = 'V.5.0'
__doc__ = """ECDSA digital signatore algorithm

fun:
-sign
-check
-keygen

exception:
ECDSAError
"""


def sign(message: bytearray, privkey: int, base_point: PointWOrder, generator: Callable[[int], int]) ->Tuple[int, int]:
    """Digital signature algorithm.

    AAA order of the curve with length > 512 not supported, raise ECDSAError exception.

    :param message: bytes represented the message
    :param privkey: user private key
    :param base_point: Point used as base, can be used a standard point from ECL.std_curves
    :param generator: random number generator, return a random int of size passed by parameter
    :return: a couple of integer represented the signature
    """
    if base_point.order.bit_length() > 512:
        raise ECDSAError("bit length of order of base point > 512")
    sha = hashlib.sha512()
    sha.update(message)
    message_hash = int(sha.digest().hex(), 16)
    z = message_hash >> (512-base_point.order.bit_length())
    r = 0
    s = 0
    while r == 0 or s == 0:
        k = generator(base_point.order.bit_length()) % base_point.order
        while k == 0:
            k = generator(base_point.order.bit_length()) % base_point.order
        p = base_point * k
        r = p.x % base_point.order
        s = (inverse(k, base_point.order) * (z + (privkey * r))) % base_point.order
    return r, s


def check(message, r: int, s: int, pubkey: Point, base_point: PointWOrder) -> bool:
    """ Digital signature verification algorithm.

    AAA order of the curve with length > 512 not supported, raise ECDSAError exception.

    :param message: bytes represented the message
    :param r: first member of the signature
    :param s: second member of the signature
    :param pubkey: user public key
    :param base_point: Point used as base, can be used a standard point from ECL.std_curves
    :return: true is the signaure is verified, else false
    """
    if not pubkey:
        return False
    if not pubkey.check(base_point.curve):
        return False
    if pubkey * base_point.order:
        return False
    if r < 1 or r >= base_point.order:
        return False
    if s < 1 or s >= base_point.order:
        return False
    if base_point.order.bit_length() > 512:
        raise ECDSAError("bit length of order of base point > 512")
    sha = hashlib.sha512()
    sha.update(message)
    message_hash = int(sha.digest().hex(), 16)
    z = message_hash >> (512-base_point.order.bit_length())
    w = inverse(s, base_point.order)
    u1 = (z * w) % base_point.order
    u2 = (r * w) % base_point.order
    p = (base_point * u1) + (pubkey * u2)
    return r == p.x % base_point.order


def keygen(base_point: PointWOrder, generator: Callable[[int], int]) -> Tuple[int, Point]:
    """
    :param base_point: Point used as base, can be used a standard point from ECL.std_curves
    :param generator: random number generator, return a random int of size passed by parameter
    :return: the couple (private key, public key)
    """
    privkey = generator(base_point.order.bit_length()) % base_point.order
    while privkey == 0:
        privkey = generator(base_point.order.bit_length()) % base_point.order
    pubkey = base_point * privkey
    return privkey, pubkey


class ECDSAError(EclException):
    """ECDSAError algorithm fail."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__repr__()
