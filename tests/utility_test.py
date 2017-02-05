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
__version__ = 'V.5.4'


def test_inverse() -> bool:
    t = 0
    while t == 0:
        t = random.randint(0, 30)
    return (inverse(t, 31) * t) % 31 == 1


def test_is_square() -> bool:
    t = 0
    while t == 0:
        t = random.randint(0, 30)
    s = t*t % 31
    return is_square(s, 31)


def test_square_root() -> bool:
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


def test_utility() -> bool:
    return test_inverse() and test_is_square() and test_square_root()
