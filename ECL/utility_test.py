from ECL.utility import *
import random


def test_inverse():
    t = 0
    while t == 0:
        t = random.randint(0, 30)
    return (inverse(t, 31) * t) % 31 == 1


def test_is_square():
    t = 0
    while t == 0:
        t = random.randint(0, 30)
    s = t*t % 31
    return is_square(s, 31)


def test_square_root():
    t = 0
    while t == 0:
        t = random.randint(0, 7)

    s = square_root(t * t % 7, 7)
    r1 = s == t or 7 - t == s

    t = random.randint(0, 13)
    while t == 0:
        t = random.randint(0, 12)

    s = square_root(t * t % 13, 13)
    r2 = s == t or 13 - t == s

    t = random.randint(0, 16)
    while t == 0:
        t = random.randint(0, 16)

    s = square_root(t * t % 17, 17)
    r3 = s == t or 17 - t == s
    return r1 and r2 and r3


def test_utility():
    return test_inverse() and test_is_square() and test_square_root()
