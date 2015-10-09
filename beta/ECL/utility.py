import os
from typing import Tuple

__author__ = 'ivansarno'
__version__ = 'V.4.beta'
__doc__ = """ built-in random number generator, root exception,
implementation of Extended Euclide algorithm, inverse calculation and modular square check"""


def extended_euclide(a: int, b: int) -> Tuple[int, int]:
    """Extende Euclide algorithm.

    :return: MCD(a,b), inverse of a mod b, aux int
    """
    if b == 0:
        return a, 1, 0
    temp = extended_euclide(b, a % b)
    return temp[0], temp[2], temp[1] - (a // b) * temp[2]


def inverse(number: int, module: int) -> int:
    """Inverse operation in modular arihtmetic.

    :return: inverse of number mod module
    """
    temp = extended_euclide(number, module)
    return temp[1]


def is_square(num: int, module: int) -> bool:
    """Return if num is a square mod module.

    :return: exist y ** 2 mod module == num
    """
    e = module // 2
    r = pow(num, e, module)
    if r == 1:
        return True
    else:
        return False


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
