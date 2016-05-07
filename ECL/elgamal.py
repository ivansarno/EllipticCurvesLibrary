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
from typing import Callable

from ECL import koblitz
from ECL.utility import EclException
from ECL.point import Point
from ECL.point_with_order import PointWOrder

__author__ = 'ivansarno'
__version__ = 'V.5.1'
__doc__ = """El Gamal's cipher.

classes: ElGamalMessage, PublicKey, PrivateKey

exception: ElGamalError
"""


class ElGamalMessage:
    def __init__(self, first: Point, second: Point, padding: int):
        """This constructor is for internal use, user must resume a message from a representation string"""
        self.__first = first
        self.__second = second
        self.__padding = padding

    @property
    def first(self) -> Point:
        return self.__first

    @property
    def second(self) -> Point:
        return self.__second

    @property
    def padding(self) -> int:
        return self.__padding

    def __str__(self):
        return "first point:\n%s\nsecond point:\n%s\npadding: 0x%x\n" % (self.__first, self.__second, self.__padding)

    def __repr__(self):
        return "ECL.elgamal.ElGamalMessage(%s, %s, 0x%x)" % (self.__first.__repr__(), self.__second.__repr__(), self.__padding)


class PublicKey:
    def __init__(self, base_point: PointWOrder, key_point: Point):
        """This constructor is for internal use, user must generates the public key from a PrivateKey object
        or resume it from a representation string"""
        self.__key = key_point
        self.__base = base_point

    def encrypt(self, message: int, generator: Callable[[int], int]) -> ElGamalMessage:
        """
        :param generator: random number generator, return a positive integer with bit length passed as parameter
        """
        if message > self.__base.order:
            raise ElGamalError("Message too large for this curve")

        message, padding = koblitz.iterative_encode(message, self.__base.curve)
        fact = generator(self.__base.order.bit_length()) % self.__base.order
        while fact < 2:
            fact = generator(self.__base.order.bit_length()) % self.__base.order
        return ElGamalMessage(self.__base * fact, message + self.__key * fact, padding)

    def __repr__(self):
        return "ECL.elgamal.PublicKey( %s, %s)" % (self.__base.__repr__(), self.__key.__repr__())


class PrivateKey:
    def __init__(self, base_point: PointWOrder, key: int):
        """This constructor is for internal use, user must generates the private key with keygen method
        or resume it from a representation string"""
        self.__key = key
        self.__base = base_point

    @staticmethod
    def keygen(base_point: PointWOrder, generator: Callable[[int], int]):
        """
            :param generator: random number generator, return a positive integer with bit length passed as parameter
        """
        secret = generator(base_point.order.bit_length()) % base_point.order
        while secret < 2:
            secret = generator(base_point.order.bit_length()) % base_point.order
        return PrivateKey(base_point, secret)

    @property
    def public_key(self) -> PublicKey:
        return PublicKey(self.__base, self.__base * self.__key)

    def decrypt(self, message: ElGamalMessage) -> int:
        temp = message.first * self.__key
        temp = message.second - temp
        return koblitz.decode(temp, message.padding)

    def __repr__(self):
        return "ECL.elgamal.PrivateKey( %s, 0x%x)" % (self.__base.__repr__(), self.__key)


class ElGamalError(EclException):
    """ElGamal algorithm fail."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__repr__()
