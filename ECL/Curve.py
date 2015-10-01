__author__ = 'ivansarno'
__version__ = 'V.3.2'
__doc__ = """Implemetation of Prime Elliptic Curves"""


class Curve:
    """Prime Elliptic Curve.

    member:
    :type a: int
    :type b: int
    prime:  prime number that define the field of the curve
    :type prime: int

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
        self.a = a_init
        self.b = b_init
        self.prime = prime_init

    def __eq__(self, other):
        """

        :type other: Curve
        :return: self == other
        :rtype: bool
        """
        return (self.a == other.a) and (self.b == other.b) and (self.prime == other.prime)

    def copy(self):
        """Return a copy of self.

        :return: Curve copy of self
        :rtype: Curve
        """
        ris = Curve(self.a, self.b, self.prime)
        return ris

    def __str__(self):
        return "a: %x\nb: %x\nprime: %x\n" % (self.a, self.b, self.prime)

    def __repr__(self):
        return "Curve(0x%x, 0x%x, 0x%x)" % (self.a, self.b, self.prime)
