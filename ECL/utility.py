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

__author__ = 'ivansarno'
__version__ = 'V.5.0'
__doc__ = """ built-in random number generator, root exception,
implementation of Extended Euclide algorithm, inverse calculation and modular square root.
This functions are ued by other modules"""


def inverse(number: int, modulus: int) -> int:
    """Inverse operation in modular arihtmetic.

    :return: inverse of number mod module
    """
    if modulus == 0:
        return 0
    buffer = [number, modulus]
    while buffer[-1] != 0:
        buffer.append(buffer[-2] % buffer[-1])

    buffer.pop()
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
    """Return if num is a square mod module.

    :return: exist y ** 2 mod module == num
    """
    e = module // 2
    r = pow(num, e, module)
    return r == 1


def generator(size: int) -> int:
        """ return a random number.

    :param size: number of bit of random number
    :return: random int of size bit
    """
        temp = os.urandom(size // 8)
        return int.from_bytes(temp, 'little')


class EclException(Exception):
    """Generic ECL exception."""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value.__repr__()


def square_root(number: int, prime: int) -> int:
    """Return square roots of number mod prime

    the cases in which number == 0 or prime == 2 is not supported because not occurs in this program
    """
    if (prime % 4) == 3:
        return pow(number, (prime + 1) // 4, prime)
    if (prime % 8) == 5:
        sign = pow(number, (prime - 1) // 4, prime)
        if sign == 1:
            return pow(number, (prime + 3) // 8, prime)
        else:
            return (2 * number) * pow((4 * number), (prime - 5) // 8, prime)
    r = shanks(number, prime)
    return r[1]


def legendre_symbol(nember: int, prime: int) -> int:
    ls = pow(nember, (prime - 1) // 2, prime)
    if ls == prime - 1:
        return -1
    return ls


def shanks(number: int, prime: int) -> Tuple[int, int]:
    """Return square roots of number mod prime

    the cases in which number == 0 or prime == 2 is not supported because not occurs in this program
    """
    q = prime - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2

    z = 1
    while legendre_symbol(z, prime) != -1:
        z += 1

    c = pow(z, q, prime)
    x = pow(number, (q + 1) // 2, prime)
    t = pow(number, q, prime)
    m = s

    while t != 1:
        i = 0
        e = 2
        for i in range(1, m):
            if pow(t, e, prime) == 1:
                break
            e *= 2

        b = pow(c, 2 ** (m - i - 1), prime)
        x = (x * b) % prime
        t = (t * b * b) % prime
        c = (b * b) % prime
        m = i

    return x, prime - x
