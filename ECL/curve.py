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
__author__ = 'ivansarno'
__version__ = 'V.5.2'
__doc__ = """Implementation of Prime Elliptic Curves"""


class Curve:
    """Prime Elliptic Curve.

    member: a, b, prime
    method: __eq__, copy, __repr__, __str__
    """
    def __init__(self, a_init: int, b_init: int, prime_init: int):
        """

        :param prime_init: prime number
        """
        self.__a = a_init
        self.__b = b_init
        self.__prime = prime_init

    @property
    def a(self) -> int:
        return self.__a

    @property
    def b(self) -> int:
        return self.__b

    @property
    def prime(self) -> int:
        return self.__prime

    def __eq__(self, other):
        """

        :type other: Curve
        :return: self == other
        :rtype: bool
        """
        return (self.__a == other.__a) and (self.__b == other.__b) and (self.__prime == other.__prime)

    def copy(self):
        """Return a copy of self.

        :return: Curve copy of self
        :rtype: Curve
        """
        ris = Curve(self.__a, self.__b, self.__prime)
        return ris

    def __str__(self):
        return "a: %x\nb: 0x%x\nprime: 0x%x\n" % (self.__a, self.__b, self.__prime)

    def __repr__(self):
        return "ECL.Curve(0x%x, 0x%x, 0x%x)" % (self.__a, self.__b, self.__prime)
