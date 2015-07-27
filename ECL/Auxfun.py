import os
__author__ = 'ivansarno'
__version__ = 'V.3.0'
__doc__ = """ built-in random number generator,
implementation of Extended Euclide algorithm, inverse calculation and modular square check"""


def extended_euclide(a, b):
    """Extende Euclide algorithm.

    :type a: int
    :type b: int
    :return: MCD(a,b), inverse of a mod b, aux int
    :rtype: (int,int,int)
    """
    if b == 0:
        return a, 1, 0
    temp = extended_euclide(b, a % b)
    return temp[0], temp[2], temp[1] - (a // b) * temp[2]


def inverse(number, module):
    """Inverse operation in modular arihtmetic.

    :type number: int
    :param module: module
    :type module: int
    :return: inverse of number mod module
    :rtype: int
    """
    temp = extended_euclide(number, module)
    return temp[1]


def is_square(num, module):
    """Return if num is a square mod module.

    :type num: int
    :type module: int
    :return: exist y ** 2 mod module == num
    :rtype: bool
    """
    e = module // 2
    r = pow(num, e, module)
    if r == 1:
        return True
    else:
        return False


class Generator:
    """built-in random number generator.

        method:
            get(int) -> int
    """

    @staticmethod
    def get(size):
        """ return a andom number.

    :return: random int of size bit
    :rtype: int
    """
        temp = os.urandom(size // 8)
        return int.from_bytes(temp, 'little')
