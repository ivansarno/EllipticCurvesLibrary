"""
    Elliptic Curve Library

    Copyright 2017 Ivan Sarno

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
from ECL.utility import *
import random

__author__ = 'ivansarno'
__version__ = 'V.1.0'

primes = [17,	19,	23,	29,	31,	37,	41,	43,	47,	53,	59,	61,	67,	71,	73,	79,	83,	89,	97,	101, 103, 107, 109,	113, 127,
          131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
          251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379,
          383, 389, 397, 401, 409]


def test_inverse() -> bool:
    p = random.choice(primes)
    t = random.randint(2, p-1)
    return (inverse(t, p) * t) % p == 1


def test_is_square() -> bool:
    p = random.choice(primes)
    t = random.randint(2, p - 1)
    s = t*t % p
    return is_square(s, p)


def test_square_root() -> bool:
    t = random.randint(1, 7)
    s = square_root(t * t % 7, 7)
    r1 = s == t or 7 - t == s

    t = random.randint(1, 13)
    s = square_root(t * t % 13, 13)
    r2 = s == t or 13 - t == s

    t = random.randint(1, 16)
    s = square_root(t * t % 17, 17)
    r3 = s == t or 17 - t == s
    return r1 and r2 and r3


def test_utility() -> bool:
    return test_inverse() and test_is_square() and test_square_root()
