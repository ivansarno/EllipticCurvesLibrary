__author__ = 'ivansarno'
__version__ = 'V.4.alpha'
__doc__ = """Implemetation of Prime Elliptic Curves"""


class Curve:
    """Prime Elliptic Curve.

    member:
    :type __a: int
    :type __b: int
    prime:  prime number that define the field of the __curve
    :type __prime: int

    method:
    - __eq__
    - copy
    - __repr__
    - __str__
    """
    def __init__(self, a_init, b_init, prime_init):
        """

        :type a_init: int
        :type b_init: int
        :param prime_init: prime number
        :type prime_init: int
        """
        self.__a = a_init
        self.__b = b_init
        self.__prime = prime_init

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b

    @property
    def prime(self):
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
        return "a: %x\nb: %x\nprime: %x\n" % (self.__a, self.__b, self.__prime)

    def __repr__(self):
        return "Curve(0x%x, 0x%x, 0x%x)" % (self.__a, self.__b, self.__prime)
