import os
from typing import Tuple

__author__ = 'ivansarno'
__version__ = 'V.4.2'
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