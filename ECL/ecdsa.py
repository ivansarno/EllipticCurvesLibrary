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
from ECL.utility import inverse, EclError

__author__ = 'ivansarno'
__version__ = 'V.5.3'
__doc__ = """ECDSA digital signature algorithm

classes: PrivateKey, PublicKey, Signature

exception: ECDSAError
"""


def _standard_hash(message: bytearray) -> Tuple[int, int]:
    """Default hash fun, sha512, little endian, unsigned"""
    sha = hashlib.sha512()
    sha.update(message)
    message_hash = int.from_bytes(sha.digest(), byteorder='little', signed=False)
    return message_hash, 512


class Signature:
    def __init__(self, first: int, second: int):
        """This constructor is for internal use, user must resume a message from a representation string or use deserialization"""
        self.__first = first
        self.__second = second

    @property
    def first(self) -> int:
        return self.__first

    @property
    def second(self) -> int:
        return self.__second

    def __str__(self):
        return "( 0x%x, 0x%x)\n" % (self.__first, self.__second)

    def __repr__(self):
        return "ECL.ecdsa.Signature(0x%x, 0x%x)" % (self.__first, self.__second)


class PublicKey:
    def __init__(self, base_point: PointWOrder, key_point: Point):
        """This constructor is for internal use, user must generates the public key from a PrivateKey object
        or resume it from a representation string or use deserialization"""
        self.__key = key_point
        self.__base = base_point

    def __repr__(self):
        return "ECL.ecdsa.PublicKey( %s, %s)" % (self.__base.__repr__(), self.__key.__repr__())

    def check(self, message: bytearray, signature: Signature, hash_fun=_standard_hash) -> bool:
        """ Digital signature verification algorithm.

        :param hash_fun: hash fun, return 2 int, first the hash of the message, second the length of the hash in bits.
        by default use sha512.
        :type hash_fun: Callable[[bytearray], Tuple[int, int]]
        """

        if self.__key * self.__base.order:
            return False
        if signature.first < 1 or signature.first >= self.__base.order:
            return False
        if signature.second < 1 or signature.second >= self.__base.order:
            return False

        message_hash, hash_length = hash_fun(message)
        z = message_hash >> (hash_length - self.__base.order.bit_length())
        w = inverse(signature.second, self.__base.order)
        u1 = (z * w) % self.__base.order
        u2 = (signature.first * w) % self.__base.order
        p = (self.__base * u1) + (self.__key * u2)
        return signature.first == p.x % self.__base.order


class PrivateKey:
    def __init__(self, base_point: PointWOrder, key: int):
        """This constructor is for internal use, user must generates the private key with keygen method
        or resume it from a representation string or use deserialization"""
        self.__key = key
        self.__base = base_point

    @staticmethod
    def keygen(base_point: PointWOrder, generator: Callable[[int], int]):
        """
            :param generator: random number generator, return a positive integer with bit length passed as parameter

            AAA order of the curve with length > 512 not supported, raise ECDSAError exception.
        """
        if base_point.order.bit_length() > 512:
            raise ECDSAError("bit length of order of base point > 512")
        secret = generator(base_point.order.bit_length()) % base_point.order
        while secret < 2:
            secret = generator(base_point.order.bit_length()) % base_point.order
        return PrivateKey(base_point, secret)

    @property
    def public_key(self) -> PublicKey:
        return PublicKey(self.__base, self.__base * self.__key)

    def sign(self, message: bytearray, generator: Callable[[int], int], hash_fun=_standard_hash) -> Signature:
        """Digital signature algorithm.

        :param hash_fun: hash fun, return 2 int, first the hash of the message, second the length of the hash in bits.
        by default use sha512.
        :type hash_fun: Callable[[bytearray], Tuple[int, int]]
        """

        message_hash, hash_length = hash_fun(message)
        z = message_hash >> (hash_length - self.__base.order.bit_length())
        r = 0
        s = 0
        while r == 0 or s == 0:
            k = generator(self.__base.order.bit_length()) % self.__base.order
            while k == 0:
                k = generator(self.__base.order.bit_length()) % self.__base.order
            p = self.__base * k
            r = p.x % self.__base.order
            s = (inverse(k, self.__base.order) * (z + (self.__key * r))) % self.__base.order
        return Signature(r, s)

    def __repr__(self):
        return "ECL.ecdsa.PrivateKey( %s, 0x%x)" % (self.__base.__repr__(), self.__key)


class ECDSAError(EclError):
    """ECDSAError algorithm fail."""
    pass

