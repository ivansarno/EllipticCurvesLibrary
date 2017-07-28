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
import ECL
from ECL import *
import random

__author__ = 'ivansarno'
__version__ = 'V.1.0'


def test_rapresentation() -> bool:
    point = ECL.std_curves.PointP192()
    dpoint = point._doubles()
    return point == eval(point.__repr__()) and dpoint == eval(dpoint.__repr__())


def test_arithmetic() -> bool:
    point = ECL.std_curves.PointP192()
    inf = point.infinitepoint(point.curve)
    if point != (point + inf) or point != (point - inf):
        return False
    p = point.copy()
    p._doubles()
    inf2 = inf.copy()
    inf2._doubles()
    if point + point != p or inf2 != inf:
        return False
    if -point != inf - point:
        return False
    a = random.randrange(100)
    b = random.randrange(a // 2)
    p = inf.copy()
    for i in range(0, a):
        p += point
    if point * a != p:
        return False
    if point * (a - b) != (point * a) - (point * b):
        return False
    return True


def test_point():
    return test_rapresentation() and test_arithmetic()
