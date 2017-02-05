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
from ECL import elgamal, utility, std_curves
import random

__author__ = 'ivansarno'
__version__ = 'V.5.4'

def point_test():
    point = ECL.std_curves.PointP192()
    dpoint = point._doubles()
    return point == eval(point.__repr__()) and dpoint == eval(dpoint.__repr__())


def test():
    return True


