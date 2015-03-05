__author__ = 'ivansarno'
#
# implementation of Extended Euclide algorithm and inverse calculation


def extended_euclide(a, b):
    if b == 0:
        return (a, 1, 0)
    temp = extended_euclide(b, a % b)
    return (temp[0], temp[2], temp[1] - (a // b) * temp[2])


def inverse(a, b):
    """inverse operatin in modular arihtmetic """
    temp = extended_euclide(a, b)
    return temp[1]
