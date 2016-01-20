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
from ECL.utility import EclException
from ECL.point import Point
from ECL.point_with_order import PointWOrder

__author__ = 'ivansarno'
__version__ = 'V.5.0'
__doc__ = """Diffie-Hellman's public key system.

class:
DiffieHellman

exception:
DiffieHellmanError
"""


class DiffieHellman:
    """Object that creates and stores a key.

    method:
    -step1
    -step2
    """

    def __init__(self, base_point: PointWOrder, generator: Callable[[int], int]):
        """
        :param base_point: Point used as base, can be used a standard point from ECL.std_curves
        :param generator: random number generator, return a random int of size passed by parameter
        """

        self.__point = base_point
        self.__gen = generator
        self.__secret = 0
        self.__key = None
        self.__synch = False

    def step1(self) -> Point:
        """Start protocol and return a Point to send to partner.

        :return: Point to sand to partner
        """
        self.__secret = self.__gen(self.__point.order.bit_length()) % self.__point.order
        self.__synch = True
        return self.__point * self.__secret

    def step2(self, partnerpoint: Point) -> Point:
        """Take result of partener step1 and return the key as Point

        :param partnerpoint: Point received by partner
        :return: the key
        :raise: DiffieHellmanError
        """
        if not self.__synch:
            raise DiffieHellmanError("called step2 before calling step1")
        if not partnerpoint.check(self.__point.curve):
            raise DiffieHellmanError("point of partner and the base point are not on the same curve")
        self.__synch = False
        self.__key = partnerpoint * self.__secret
        return self.__key

    @property
    def key(self) -> Point:
        """
        :return: the key or None if step2 has not been executed
        """
        if self.__synch or self.__key is None:
            raise DiffieHellmanError("key not found, run step2")
        return self.__key


class DiffieHellmanError(EclException):
    """DiffieHellman algorithm fail."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__repr__()
