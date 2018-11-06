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

import os
from typing import Tuple

import sys

__author__ = 'ivansarno'
__version__ = 'V.5.5'
__doc__ = """ built-in random number generator, root exception, inverse calculation and modular square root.
This functions are used by other modules"""


def inverse(number: int, modulus: int) -> int:
    """Inverse operation in modular arithmetic.

    :return: inverse of number mod module
    use iterative version of extended euclide's algorithm
    """
    if modulus == 0:
        return 0
    buffer = [number, modulus]
    while buffer[-1] != 0:
        buffer.append(buffer[-2] % buffer[-1])

    buffer.pop() #remove unused temorary value
    temp = 0
    intermediate = 1
    result = 1
    while len(buffer) > 1:
        result = temp
        temp = intermediate - ((buffer[-2] // buffer[-1]) * temp)
        intermediate = result
        buffer.pop()

    if result > 0:
        return result
    else:
        return modulus + result


def is_square(num: int, module: int) -> bool:
    """Return if num is a square mod module when module is a prime number != 2.

    :return: exist y ** 2 mod module == num
    """
    return pow(num, module >> 1, module) == 1


if sys.version_info.minor < 6:
    def generator(size: int) -> int:
        """ Random Number generator for test, is not safe.

        :param size: number of bit of random number
        :return: random int of size bit
        """
        temp = os.urandom(size // 8 + 1)
        return int.from_bytes(temp, 'little')
else:
    def generator(size: int) -> int:
        """ Random Number generator, use Python's secrets module.

        :param size: number of bit of random number
        :return: random int of size bit
        """
        import secrets
        return abs(secrets.randbits(size))


class EclError(Exception):
    """Generic ECL exception."""
    pass


def square_root(number: int, prime: int) -> int:
    """Return square roots of number mod prime

    the cases in which prime == 2 is not supported because not occurs in this program
    """
    if number == 0:
        return 0
    if (prime & 3) == 3:
        return pow(number, (prime + 1) >> 2, prime)
    if (prime & 7) == 5:
        v = pow(number << 1, (prime-5) >> 3)
        i = ((number * (v ** 2)) << 1) % prime
        return (number * v * (i - 1)) % prime
    r = shanks(number, prime)
    return r[1]


def legendre_symbol(number: int, prime: int) -> int:
    ls = pow(number, prime >> 1, prime)
    if ls == prime - 1:
        return -1
    return ls


def shanks(number: int, prime: int) -> Tuple[int, int]:
    """Return square roots of number mod prime."""
    q = prime - 1
    s = 0
    while q & 1 == 0:
        s += 1
        q >>= 1

    z = 1
    while legendre_symbol(z, prime) != -1:
        z += 1

    c = pow(z, q, prime)
    x = pow(number, (q + 1) >> 1, prime)
    t = pow(number, q, prime)
    m = s

    while t != 1:
        i = 0
        e = 2
        for i in range(1, m):
            if pow(t, e, prime) == 1:
                break
            e <<= 1

        b = pow(c, 1 << (m - i - 1), prime)
        x = (x * b) % prime
        t = (t * b * b) % prime
        c = (b * b) % prime
        m = i

    return x, prime - x
